from __future__ import annotations

import re


def active_filter_terms(value: str, *, min_length: int = 3) -> tuple[str, ...]:
    return tuple(token.casefold() for token in re.split(r"\s+", value.strip()) if len(token) >= min_length)


def text_matches_filter_terms(value: str, terms: tuple[str, ...]) -> bool:
    normalized = value.casefold()
    return any(term in normalized for term in terms)
