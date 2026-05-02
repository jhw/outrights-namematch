"""Bundled per-league team data.

Team configs ship inside the package (``data/teams/<LEAGUE>.yaml``) so a
``pip install`` of this library is the single source of truth — consumers
do not maintain their own copies.

Public surface:

  list_leagues()              -> list[str]
  get_teams(league)           -> list[Team]
  get_teams_raw(league)       -> list[dict]   # for matcher.match()
"""
from __future__ import annotations

from dataclasses import dataclass, field
from importlib import resources
from typing import Iterator

import yaml


@dataclass(frozen=True)
class Team:
    name: str
    altNames: tuple[str, ...] = field(default_factory=tuple)

    def all_names(self) -> tuple[str, ...]:
        return (self.name,) + self.altNames


def _data_dir():
    return resources.files(__package__).joinpath("data", "teams")


def list_leagues() -> list[str]:
    """League codes for which team data is bundled."""
    return sorted(p.stem for p in _data_dir().iterdir() if p.suffix == ".yaml")


def get_teams_raw(league: str) -> list[dict]:
    """Return the raw dict list — the form `matcher.match()` accepts."""
    path = _data_dir().joinpath(f"{league}.yaml")
    if not path.is_file():
        raise KeyError(f"no team data bundled for league {league!r}")
    return yaml.safe_load(path.read_text()) or []


def get_teams(league: str) -> list[Team]:
    """Return Team dataclasses for the league."""
    return [
        Team(name=t["name"], altNames=tuple(t.get("altNames") or ()))
        for t in get_teams_raw(league)
    ]


def __iter_all_teams() -> Iterator[tuple[str, Team]]:
    for league in list_leagues():
        for team in get_teams(league):
            yield league, team
