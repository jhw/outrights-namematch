"""Cross-source team-name reconciliation.

Cascade order: exact -> levenshtein <= 2 -> abbreviation -> token overlap
>= 50%. Levenshtein runs before abbreviation so diacritic-only pairs like
"Atletico" / "Atletico" don't get token-captured by an unrelated team.

`rapidfuzz` provides distance + token counts (native C, MIT licence). The
cascade itself stays in this module because altNames handling and
per-matcher ordering are domain choices the library shouldn't push to a
third-party.

True-alias pairs (Tottenham / Spurs) are NOT recoverable by the cascade.
They must appear explicitly in the team's `altNames`.
"""
from __future__ import annotations

import re
from typing import Optional

from rapidfuzz.distance import Levenshtein


_CLEAN_CHARS_RE = re.compile(r"['\-\.,:;()/]")
_REJECT_TOKENS = frozenset({"Real"})
_PURE_DIGIT_RE = re.compile(r"^\d+$")


def clean_text(text: str) -> str:
    """Lowercase the text, strip punctuation and pure-digit tokens.

    Exposed so callers wanting to pre-normalise their own dictionary keys
    (e.g. for caching match results) can use the same canonical form the
    matcher does.
    """
    tokens = []
    for tok in text.split():
        tok = _CLEAN_CHARS_RE.sub("", tok)
        if not tok or tok in _REJECT_TOKENS or _PURE_DIGIT_RE.match(tok):
            continue
        tokens.append(tok.lower())
    return " ".join(tokens)


def _names_for(entity: dict) -> list[str]:
    names = [entity["name"]]
    for n in entity.get("altNames") or []:
        if n:
            names.append(n)
    return names


_SHORT_NAME_LEN = 8


def _levenshtein_le_2(x: str, y: str) -> bool:
    """Distance <=2, but capped at <=1 when either side is a short (<8-char)
    single-word-ish name.

    Short English town names are dense in this space — "Burton"/"Bolton"
    and "Luton"/"Burton" both sit at distance 2, as do unrelated clubs
    like "Roma"/"Como". A raw source string for a team that isn't even in
    the current roster (e.g. a division-mate from a prior season) can
    then silently resolve to the wrong in-roster team instead of falling
    through to token/abbrev matching or None. Longer names have enough
    entropy that distance <=2 stays safe (typos, diacritics).
    """
    if abs(len(x) - len(y)) > 2:
        return False
    cutoff = 1 if min(len(x), len(y)) < _SHORT_NAME_LEN else 2
    return Levenshtein.distance(x, y, score_cutoff=cutoff) <= cutoff


def _is_abbrev(abbrev: str, text: str) -> bool:
    """Walk character-by-character: consume next-word-start or jump within current word."""
    if not abbrev:
        return True
    if not text:
        return False
    if abbrev[0] != text[0]:
        return False

    words = text.split(" ")
    first = words[0]
    if _is_abbrev(abbrev[1:], " ".join(words[1:])):
        return True
    for i in range(len(first)):
        if _is_abbrev(abbrev[1:], text[i + 1:]):
            return True
    return False


def _token_overlap(x: str, y: str) -> float:
    x_tokens = x.split()
    y_tokens = y.split()
    if not x_tokens or not y_tokens:
        return 0.0
    count = 0
    for xt in x_tokens:
        for yt in y_tokens:
            if xt == yt:
                count += 1
    return count / (len(x_tokens) * len(y_tokens))


_MATCHERS = (
    ("exact",       lambda x, y: x == y),
    ("levenshtein", _levenshtein_le_2),
    ("abbrev0",     lambda x, y: _is_abbrev(x, y)),
    ("abbrev1",     lambda x, y: _is_abbrev(y, x)),
    ("token",       lambda x, y: _token_overlap(x, y) >= 0.5),
)


def match(text: str, entities: list[dict]) -> Optional[str]:
    """Resolve `text` to a canonical entity `name`, or None.

    Each entity is a dict `{name: str, altNames?: list[str]}`. Matching is
    case- and punctuation-insensitive; altNames participate in matching
    but only the canonical `name` is returned.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return None
    for _name, fn in _MATCHERS:
        for entity in entities:
            for candidate in _names_for(entity):
                if fn(cleaned, clean_text(candidate)):
                    return entity["name"]
    return None


def match_matchup(text: str, teams: list[dict]) -> Optional[str]:
    """Resolve "Team A vs Team B" into "Canonical A vs Canonical B".

    Returns None if either side fails to match or both sides resolve to
    the same canonical name (a parsing bug — not a valid fixture).
    """
    parts = re.split(r"\s+vs?\s+", text, flags=re.IGNORECASE, maxsplit=1)
    if len(parts) != 2:
        return None
    home = match(parts[0], teams)
    away = match(parts[1], teams)
    if not home or not away or home == away:
        return None
    return f"{home} vs {away}"
