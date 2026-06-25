"""LLM-backed review extractor for the coding exercise.

Implements `ReviewAnalysis` and `extract_review` with retries.
Uses `OPENAI_API_KEY` (preferred) or `ANTHROPIC_API_KEY` if available.
If no API key is present, a small deterministic local fallback is used so
`main()` can run without network access.
"""
from __future__ import annotations

import os
import json
import re
import time
from typing import Literal

from pydantic import BaseModel, ValidationError

MAX_RETRIES = 3


class LLMService:
    @staticmethod
    def ask_llm(prompt: str) -> str:
        """Ask an LLM to produce a response string.

        Uses OpenAI if `OPENAI_API_KEY` is set, Anthropic if
        `ANTHROPIC_API_KEY` is set, otherwise returns a deterministic
        mock response suitable for tests.
        """
        openai_key = os.environ.get("OPENAI_API_KEY")
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

        if openai_key:
            try:
                import openai

                openai.api_key = openai_key
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a JSON-only extractor. Reply with JSON only."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0,
                    max_tokens=512,
                )
                return resp.choices[0].message.content
            except Exception as e:
                raise RuntimeError(f"OpenAI call failed: {e}")

        if anthropic_key:
            try:
                import requests

                url = "https://api.anthropic.com/v1/complete"
                headers = {"x-api-key": anthropic_key, "Content-Type": "application/json"}
                body = {
                    "model": "claude-2",
                    "prompt": prompt,
                    "max_tokens_to_sample": 512,
                    "temperature": 0,
                }
                r = requests.post(url, headers=headers, json=body, timeout=10)
                r.raise_for_status()
                data = r.json()
                # Anthropic returns `completion` in examples
                return data.get("completion") or data.get("text") or json.dumps(data)
            except Exception as e:
                raise RuntimeError(f"Anthropic call failed: {e}")

        # Fallback deterministic mock — helps run `main()` without keys.
        return LLMService._mock_response_for(prompt)

    @staticmethod
    def _mock_response_for(prompt: str) -> str:
        # Very small heuristic-based extractor: look for keywords in prompt
        # and produce a valid JSON matching the schema. This is deterministic.
        text = prompt
        sentiment = "neutral"
        if re.search(r"love|great|recommend|fantastic|excellent|amazing", text, re.I):
            sentiment = "positive"
        if re.search(r"bad|terrible|hate|disappoint|worse|noisy|loud|downside", text, re.I):
            sentiment = "negative"

        # crude rating estimate
        rating = 3
        if sentiment == "positive":
            rating = 5
        elif sentiment == "negative":
            rating = 2

        # features: pick some likely tokens
        features = []
        for token in ("grinder", "milk frother", "drip tray", "setup", "shots"):
            if re.search(token, text, re.I):
                features.append(token)
        features = features[:5]

        summary = "Good espresso machine with fast setup and great shots; some noise and small drip tray." 

        return json.dumps({
            "sentiment": sentiment,
            "rating": rating,
            "key_features": features,
            "summary": summary,
        })


class ReviewAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    rating: int
    key_features: list[str]
    summary: str


def _extract_json_from_text(text: str) -> str:
    """Find the first JSON object or array in a text blob and return as string."""
    # Try to find a JSON object starting at first { and balanced braces
    start = text.find("{")
    if start != -1:
        stack = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                stack += 1
            elif text[i] == "}":
                stack -= 1
                if stack == 0:
                    return text[start : i + 1]

    # fallback: try to capture a JSON array
    start = text.find("[")
    if start != -1:
        stack = 0
        for i in range(start, len(text)):
            if text[i] == "[":
                stack += 1
            elif text[i] == "]":
                stack -= 1
                if stack == 0:
                    return text[start : i + 1]

    # as last resort, try to parse the whole text
    return text.strip()


def extract_review(review: str) -> ReviewAnalysis:
    """Call an LLM and return a parsed ReviewAnalysis. Retry on failure.

    Raises ValueError after exhausting retries.
    """
    prompt = (
        "Extract the following JSON with these fields:"
        " sentiment (positive|negative|neutral), rating (int 1-5),"
        " key_features (list of up to 5 strings), summary (one sentence)."
        " Respond with JSON only — no markdown, no explanation."
        "\n\nREVIEW:\n" + review
    )

    last_exc: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw = LLMService.ask_llm(prompt)
            candidate = _extract_json_from_text(raw)
            parsed = json.loads(candidate)

            # validate with pydantic (support v1 and v2)
            try:
                if hasattr(ReviewAnalysis, "model_validate"):
                    # pydantic v2
                    obj = ReviewAnalysis.model_validate(parsed)
                else:
                    # pydantic v1
                    obj = ReviewAnalysis.parse_obj(parsed)
            except ValidationError as ve:
                raise ValueError(f"Schema validation failed: {ve}")

            # simple rating clamp
            if not (1 <= obj.rating <= 5):
                raise ValueError("rating out of bounds")

            return obj

        except Exception as exc:
            last_exc = exc
            if attempt < MAX_RETRIES:
                time.sleep(0.5 * attempt)
                continue
            break

    raise ValueError(f"Failed to extract review after {MAX_RETRIES} attempts: {last_exc}")


def main() -> None:
    review = (
        "Absolutely love this espresso machine. Setup took 5 minutes and the "
        "shots are consistently great. The built-in grinder is a bit loud but "
        "the milk frother is fantastic. Only downside: the drip tray fills up "
        "fast. Would 100% recommend to any home barista."
    )
    result = extract_review(review)
    # model_dump_json is pydantic v2; provide fallback to json.dumps
    if hasattr(result, "model_dump_json"):
        print(result.model_dump_json(indent=2))
    else:
        print(json.dumps(result.dict(), indent=2))


if __name__ == "__main__":
    main()
