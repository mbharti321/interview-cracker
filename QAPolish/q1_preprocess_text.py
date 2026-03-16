import re


def preprocess_text(text: str) -> str:
    """Sanitize input text for LLM consumption.

    Steps:
    1. Remove all non-alphanumeric characters (except spaces).
    2. Replace multiple spaces with a single space.
    3. Trim leading/trailing spaces.

    Args:
        text: Raw input string.

    Returns:
        Normalized string.
    """
    if text is None:
        return ""
    # Remove any character that is not a letter, digit or space
    cleaned = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    # Collapse whitespace (tabs/newlines) into single spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()


if __name__ == '__main__':
    examples = [
        " Hello, world!!!\nThis is  a test. ",
        "Special_chars: #$%&*@ are removed.",
        None,
    ]
    for e in examples:
        print(repr(e), '->', repr(preprocess_text(e)))
