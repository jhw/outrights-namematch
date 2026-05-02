# outrights-namematch

Fuzzy team-name resolution and canonical team data shared by the outrights services (`outrights-events`, `outrights-feed`, `outrights-hub`, `outrights-mip`).

## Install

Pin to a tag (the `picobeats-server -> beatwav` pattern):

```
outrights-namematch @ git+https://github.com/jhw/outrights-namematch.git@v0.1.0
```

## Usage

```python
from outrights_namematch import match, match_matchup, get_teams_raw, list_leagues

teams = get_teams_raw("ENG1")
match("Spurs", teams)                        # -> "Tottenham"
match("Man Utd", teams)                      # -> "Man United"
match("Barcelona", teams)                    # -> None  (not in ENG1)
match_matchup("Man Utd vs Spurs", teams)     # -> "Man United vs Tottenham"

list_leagues()                               # -> ["ENG1", "ENG2", ...]
```

`get_teams(league)` returns `Team` dataclasses if you want a typed view. The matcher operates on plain dicts (`{"name": str, "altNames": [str, ...]}`) so the raw form is more convenient for most call sites.

## Cascade

Order is fixed: exact → Levenshtein ≤ 2 → abbreviation → token overlap ≥ 50%. Levenshtein runs before abbreviation so diacritic-only pairs like "Atletico" / "Atlético" don't get token-captured by an unrelated team.

True-alias pairs (Tottenham / Spurs) are **not** fuzzy-recoverable. They must be listed explicitly under `altNames` in the league YAML.

## Adding a league

1. Drop a YAML file at `outrights_namematch/data/teams/<LEAGUE>.yaml`.
2. Bump `__version__` in `outrights_namematch/__init__.py` and `setup.py`.
3. Tag and push.

## Tests

```
pip install -r requirements.txt
pytest
```
