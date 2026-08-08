"""Sanity checks for the bundled league + market data."""
from outrights_namematch import get_leagues_raw, get_markets_raw, list_leagues


def test_get_leagues_raw_matches_bundled_team_leagues():
    codes = {l["code"] for l in get_leagues_raw()}
    assert codes == set(list_leagues())


def test_get_leagues_raw_rows_are_well_formed():
    for league in get_leagues_raw():
        assert isinstance(league.get("code"), str) and league["code"]
        assert isinstance(league.get("oddscheckerPath"), str) and league["oddscheckerPath"]


def test_get_markets_raw_eng1_has_winner_and_relegation():
    markets = get_markets_raw("ENG1")
    names = {m["name"] for m in markets}
    assert "Winner" in names
    assert "Relegation" in names


def test_get_markets_raw_entries_have_oddschecker_url_and_payoff():
    for market in get_markets_raw("ENG1"):
        assert isinstance(market.get("name"), str) and market["name"]
        assert isinstance(market.get("payoff"), str) and market["payoff"]
        assert market.get("oddscheckerUrl", "").startswith("https://www.oddschecker.com/")


def test_get_markets_raw_unknown_league_returns_empty():
    assert get_markets_raw("XXX1") == []
