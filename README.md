# outrights-namematch

Fuzzy team-name resolution and canonical team data shared by the outrights services (`outrights-events`, `outrights-feed`, `outrights-hub`, `outrights-mip`).

## Install

Pin to a tag (the `picobeats-server -> beatwav` pattern):

```
outrights-namematch @ git+https://github.com/jhw/outrights-namematch.git@v0.2.1
```

## Usage

```python
from outrights_namematch import match, match_matchup, get_teams_raw, list_leagues, get_leagues_raw, get_markets_raw

teams = get_teams_raw("ENG1")
match("Spurs", teams)                        # -> "Tottenham"
match("Man Utd", teams)                      # -> "Man United"
match("Barcelona", teams)                    # -> None  (not in ENG1)
match_matchup("Man Utd vs Spurs", teams)     # -> "Man United vs Tottenham"

list_leagues()                               # -> ["ENG1", "ENG2", ...]
get_leagues_raw()                            # -> [{"code": "ENG1", "oddscheckerPath": "football/english/premier-league", ...}, ...]
get_markets_raw("ENG1")                      # -> [{"name": "Winner", "payoff": "1|19x0", "oddscheckerUrl": "https://...", ...}, ...]
```

`get_teams(league)` returns `Team` dataclasses if you want a typed view. The matcher operates on plain dicts (`{"name": str, "altNames": [str, ...]}`) so the raw form is more convenient for most call sites.

`get_leagues_raw()` and `get_markets_raw(league)` return the bundled `data/leagues.yaml` and `data/markets/<LEAGUE>.yaml` rows verbatim — this library is the single source of truth for league/market metadata (oddschecker URLs, payoff vectors) as well as team names, so consumers don't maintain their own copies. Neither carries an `isActive` flag; that's a per-consumer deployment choice, not canonical data.

## Cascade

Order is fixed: exact → Levenshtein ≤ 2 → abbreviation → token overlap ≥ 50%. Levenshtein runs before abbreviation so diacritic-only pairs like "Atletico" / "Atlético" don't get token-captured by an unrelated team.

True-alias pairs (Tottenham / Spurs) are **not** fuzzy-recoverable. They must be listed explicitly under `altNames` in the league YAML.

## Adding a league

1. Drop a YAML file at `outrights_namematch/data/teams/<LEAGUE>.yaml`, and
   optionally `outrights_namematch/data/markets/<LEAGUE>.yaml` +  a row in
   `outrights_namematch/data/leagues.yaml`.
2. Bump `__version__` in `outrights_namematch/__init__.py` and `setup.py`.
3. Tag and push.

## Tests

```
pip install -r requirements.txt
pytest
```
