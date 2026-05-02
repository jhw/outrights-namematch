"""Sanity checks for the bundled team data."""
import pytest

from outrights_namematch import (
    Team,
    get_teams,
    get_teams_raw,
    list_leagues,
    match,
)


def test_list_leagues_includes_eng1_eng2():
    leagues = list_leagues()
    assert "ENG1" in leagues
    assert "ENG2" in leagues


def test_get_teams_raw_eng1_has_20_teams():
    teams = get_teams_raw("ENG1")
    assert len(teams) == 20
    assert all("name" in t for t in teams)


def test_get_teams_eng1_returns_team_dataclass():
    teams = get_teams("ENG1")
    assert all(isinstance(t, Team) for t in teams)
    arsenal = next(t for t in teams if t.name == "Arsenal")
    assert "Arsenal FC" in arsenal.altNames


def test_unknown_league_raises():
    with pytest.raises(KeyError):
        get_teams_raw("XXX1")


def test_bundled_data_works_with_matcher():
    teams = get_teams_raw("ENG1")
    assert match("Spurs", teams) == "Tottenham"
    assert match("Man Utd", teams) == "Man United"
    assert match("Forest", teams) == "Nott'm Forest"


def test_bundled_data_eng2_works():
    teams = get_teams_raw("ENG2")
    # ENG2 should resolve some Championship teams; just sanity-check non-empty
    assert len(teams) >= 20
