"""Bundled per-league metadata and market data.

League configs and market definitions ship inside the package
(``data/leagues.yaml``, ``data/markets/<LEAGUE>.yaml``) alongside the team
data in :mod:`outrights_namematch.teams` — a ``pip install`` of this
library is the single source of truth for all three.

Public surface:

  get_leagues_raw()           -> list[dict]   # every bundled league row
  get_markets_raw(league)     -> list[dict]   # a league's market definitions
"""
from __future__ import annotations

from importlib import resources

import yaml


def _data_dir():
    return resources.files(__package__).joinpath("data")


def get_leagues_raw() -> list[dict]:
    """Return every bundled league row (code, footballDataId, oddscheckerPath, ...)."""
    path = _data_dir().joinpath("leagues.yaml")
    return yaml.safe_load(path.read_text()) or []


def get_markets_raw(league: str) -> list[dict]:
    """Return a league's bundled market definitions (name, payoff, oddscheckerUrl, ...).

    Returns an empty list for a league with no bundled market data, rather
    than raising — several bundled leagues (teams-only) have none.
    """
    path = _data_dir().joinpath("markets", f"{league}.yaml")
    if not path.is_file():
        return []
    return yaml.safe_load(path.read_text()) or []
