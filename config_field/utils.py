from re import sub
from typing import Optional, Union

REGEX_PATTERN_VALUES = [
    '\n',
    '\\\\',
    '\t',
    '\r',
]


def remove_unacceptable_chars(
    value: Optional[str],
    pattern_values: list = REGEX_PATTERN_VALUES,
    default_value: Optional[Union[str, int, list]] = 'none',
) -> str:
    pattern = r'|'.join(v for v in pattern_values)
    if value is None:
        return default_value
    value = sub(pattern, ' ', str(value)).strip()
    words = value.split()
    return ' '.join(sorted(set(words), key=words.index))
