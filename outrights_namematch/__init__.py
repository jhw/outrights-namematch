"""outrights-namematch — fuzzy team-name resolution + canonical team data.

Quick example:

    from outrights_namematch import match, get_teams_raw

    teams = get_teams_raw("ENG1")
    canonical = match("Spurs", teams)        # -> "Tottenham"
    canonical = match("Man Utd", teams)      # -> "Man United"
    canonical = match("Barcelona", teams)    # -> None  (not in ENG1)
"""

from .leagues import get_leagues_raw, get_markets_raw
from .matcher import clean_text, match, match_matchup
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

__version__ = "0.3.0"
