"""Payoff shorthand parser — shared by any consumer that needs to reason
about a market's payoff shape (currently outrights-mip's season
simulator; also outrights-browser, choosing which outright markets to
display and in what order from get_markets_raw()'s bundled payoffs).

Grammar: chunks separated by "|", each either a literal number or
"Nxvalue" (N repetitions of value):

    "1|19x0"     -> [1, 0, 0, ..., 0]      (20 entries)
    "17x0|3x1"   -> [0, ..., 0, 1, 1, 1]   (20 entries)
    "2x1|4x0.25|18x0" -> [1, 1, 0.25, 0.25, 0.25, 0.25, 0, ..., 0]

An already-expanded list/tuple of numbers is returned unchanged (as a
list), so callers don't need to branch on which form they were given.
"""
from __future__ import annotations

from typing import Sequence, Union

Payoff = Union[str, Sequence[float]]


def parse_payoff(payoff: Payoff, expected_length: int | None = None) -> list[float]:
    """Expand a payoff shorthand string (or pass through a list) into a
    flat list of floats. Raises ValueError on malformed shorthand, or if
    `expected_length` is given and the expansion doesn't match it.
    """
    if isinstance(payoff, (list, tuple)):
        parts = [float(v) for v in payoff]
    else:
        if not isinstance(payoff, str):
            raise ValueError(f"Payoff must be a string or list, got {type(payoff).__name__}")
        parts = []
        for chunk in payoff.split("|"):
            chunk = chunk.strip()
            if not chunk:
                raise ValueError(f"Empty chunk in payoff {payoff!r}")
            if "x" in chunk:
                count_str, value_str = chunk.split("x", 1)
                try:
                    count = int(count_str)
                    value = float(value_str)
                except ValueError as e:
                    raise ValueError(f"Bad chunk {chunk!r} in payoff {payoff!r}: {e}")
                if count < 1:
                    raise ValueError(f"Chunk {chunk!r}: count must be >= 1")
                parts.extend([value] * count)
            else:
                try:
                    parts.append(float(chunk))
                except ValueError as e:
                    raise ValueError(f"Bad chunk {chunk!r} in payoff {payoff!r}: {e}")

    if expected_length is not None and len(parts) != expected_length:
        raise ValueError(f"Payoff {payoff!r} expanded to length {len(parts)}, expected {expected_length}")
    return parts
