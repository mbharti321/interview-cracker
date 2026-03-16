from typing import List


def route_llm_request(prompt: str, available_models: List[str]) -> str:
    """Choose a model based on prompt length and available models.

    Rules:
    1. If 'openai-gpt4' is available and prompt length < 500 -> use it.
    2. Else if 'anthropic-claude' is available and 500 <= length <= 2000 -> use it.
    3. Else if 'local-llama' is available -> use it.
    4. Otherwise raise ValueError.
    """
    length = len(prompt or "")
    models = set(available_models or [])

    if 'openai-gpt4' in models and length < 500:
        return 'openai-gpt4'
    if 'anthropic-claude' in models and 500 <= length <= 2000:
        return 'anthropic-claude'
    if 'local-llama' in models:
        return 'local-llama'
    raise ValueError('No suitable model available')


if __name__ == '__main__':
    print(route_llm_request('short prompt', ['openai-gpt4', 'local-llama']))
