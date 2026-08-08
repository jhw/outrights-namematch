"""Data-integrity checks across all bundled leagues, teams, and markets.

Guards against the season-to-season editing mistakes that are easy to
introduce by hand: duplicate teams, roster/market drift after a
promotion/relegation update, and payoff vectors that no longer match
the current team count.
"""
from __future__ import annotations

from importlib import resources

import pytest
import yaml

from outrights_namematch import get_teams_raw, list_leagues


ALL_LEAGUES = list_leagues()


def _country(league: str) -> str:
    """3-letter prefix identifying a league's promotion/relegation pyramid."""
    return league[:3]


def _load_markets(league: str) -> list[dict]:
    path = resources.files("outrights_namematch").joinpath("data", "markets", f"{league}.yaml")
    if not path.is_file():
        return []
    return yaml.safe_load(path.read_text()) or []


def _payoff_length(payoff: str) -> int:
    total = 0
    for part in payoff.split("|"):
        if "x" in part:
            n, _ = part.split("x")
            total += int(n)
        else:
            total += 1
    return total


def test_all_leagues_present():
    # Sanity check on the parametrization source itself — if this list is
    # empty or short, every test below would trivially "pass".
    assert len(ALL_LEAGUES) == 18


@pytest.mark.parametrize("league", ALL_LEAGUES)
def test_league_has_teams(league):
    assert len(get_teams_raw(league)) > 0


@pytest.mark.parametrize("league", ALL_LEAGUES)
def test_no_duplicate_teams_within_league(league):
    names = [t["name"] for t in get_teams_raw(league)]
    dupes = {n for n in names if names.count(n) > 1}
    assert not dupes, f"duplicate team(s) in {league}: {dupes}"


@pytest.mark.parametrize("league", ALL_LEAGUES)
def test_team_entries_are_well_formed(league):
    for t in get_teams_raw(league):
        assert isinstance(t.get("name"), str) and t["name"], f"malformed team in {league}: {t}"
        if "altNames" in t:
            assert isinstance(t["altNames"], list)
            assert all(isinstance(a, str) and a for a in t["altNames"])


def test_no_cross_league_duplicates_within_country():
    by_country: dict[str, list[str]] = {}
    for league in ALL_LEAGUES:
        by_country.setdefault(_country(league), []).append(league)

    for country, leagues in by_country.items():
        seen: dict[str, str] = {}
        for league in leagues:
            for t in get_teams_raw(league):
                name = t["name"]
                assert name not in seen, (
                    f"{name!r} appears in both {seen.get(name)} and {league} "
                    f"— same {country} pyramid"
                )
                seen[name] = league


@pytest.mark.parametrize("league", ALL_LEAGUES)
def test_market_include_exclude_reference_current_roster(league):
    roster = {t["name"] for t in get_teams_raw(league)}
    for market in _load_markets(league):
        for field in ("include", "exclude"):
            for name in market.get(field) or []:
                assert name in roster, (
                    f"{league} market {market['name']!r} {field} references "
                    f"{name!r}, not in current {league} roster"
                )


@pytest.mark.parametrize("league", ALL_LEAGUES)
def test_market_payoff_length_matches_roster(league):
    team_count = len(get_teams_raw(league))
    for market in _load_markets(league):
        payoff = market.get("payoff")
        if not payoff:
            continue
        length = _payoff_length(payoff)
        if market.get("include"):
            expected = len(market["include"])
        elif market.get("exclude"):
            expected = team_count - len(market["exclude"])
        else:
            expected = team_count
        assert length == expected, (
            f"{league} market {market['name']!r} payoff covers {length} "
            f"positions, expected {expected}"
        )
