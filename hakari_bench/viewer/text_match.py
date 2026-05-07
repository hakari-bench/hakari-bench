from __future__ import annotations

import re


def active_filter_terms(value: str) -> tuple[str, ...]:
    return tuple(token.casefold() for token in re.split(r"\s+", value.strip()) if len(token) >= 3)


def text_matches_filter_terms(value: str, terms: tuple[str, ...]) -> bool:
    normalized = value.casefold()
    return any(term in normalized for term in terms)
