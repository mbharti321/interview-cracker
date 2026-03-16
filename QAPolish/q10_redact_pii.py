from typing import Any, Dict, List


def _redact_value(value: Any, sensitive_keys: List[str], placeholder: str) -> Any:
    if isinstance(value, dict):
        return redact_pii(value, sensitive_keys, placeholder)
    if isinstance(value, list):
        return [_redact_value(v, sensitive_keys, placeholder) for v in value]
    return value


def redact_pii(data: Dict[str, Any], sensitive_keys: List[str], redaction_placeholder: str = '***REDACTED***') -> Dict[str, Any]:
    """Deeply redact sensitive keys in a nested dictionary or lists of dicts.

    Args:
        data: Input dictionary (may contain nested dicts/lists).
        sensitive_keys: List of keys (exact match) to redact.
        redaction_placeholder: Replacement value.

    Returns:
        New dictionary with sensitive values replaced.
    """
    if data is None:
        return {}
    result: Dict[str, Any] = {}
    for k, v in data.items():
        if k in sensitive_keys:
            result[k] = redaction_placeholder
        else:
            if isinstance(v, dict):
                result[k] = redact_pii(v, sensitive_keys, redaction_placeholder)
            elif isinstance(v, list):
                new_list = []
                for item in v:
                    if isinstance(item, dict):
                        new_list.append(redact_pii(item, sensitive_keys, redaction_placeholder))
                    else:
                        new_list.append(item)
                result[k] = new_list
            else:
                result[k] = v
    return result


if __name__ == '__main__':
    sample = {
        'name': 'Alice',
        'email': 'alice@example.com',
        'profile': {
            'phone': '+1234567890',
            'addresses': [
                {'line1': '123 Main St', 'ssn': '111-22-3333'},
                {'line1': '456 Other St'}
            ]
        }
    }
    redacted = redact_pii(sample, ['email', 'ssn', 'phone'])
    print(redacted)
