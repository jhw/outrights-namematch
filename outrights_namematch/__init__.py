"""outrights-namematch — fuzzy team-name resolution + canonical team data.

Quick example:

    from outrights_namematch import match, get_teams_raw

    teams = get_teams_raw("ENG1")
    canonical = match("Spurs", teams)        # -> "Tottenham"
    canonical = match("Man Utd", teams)      # -> "Man United"
    canonical = match("Barcelona", teams)    # -> None  (not in ENG1)

`match`/`match_matchup`/`clean_text` depend on `rapidfuzz` (a compiled
extension) and are imported lazily (PEP 562, below) so a consumer that
only needs the bundled static data (`get_markets_raw`, `get_teams_raw`,
`parse_payoff`, ...) can `pip install outrights-namematch` without it —
`pip install outrights-namematch[fuzzy]` (or a separate `rapidfuzz`
install) is required before touching the three matcher symbols.
"""

from .leagues import get_leagues_raw, get_markets_raw
from .payoff import parse_payoff
from .teams import Team, get_teams, get_teams_raw, list_leagues

__all__ = [
    "match",
    "match_matchup",
    "clean_text",
    "Team",
    "get_teams",
    "get_teams_raw",
    "list_leagues",
    "get_leagues_raw",
    "get_markets_raw",
    "parse_payoff",
]

__version__ = "0.4.0"

_MATCHER_SYMBOLS = {"match", "match_matchup", "clean_text"}


def __getattr__(name):
    if name in _MATCHER_SYMBOLS:
        from . import matcher
        return getattr(matcher, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
