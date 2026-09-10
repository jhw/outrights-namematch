"""Sanity checks for the bundled bookmaker catalog."""
from outrights_namematch import get_bookmakers_raw


def test_get_bookmakers_raw_returns_non_empty_list():
    bookmakers = get_bookmakers_raw()
    assert len(bookmakers) > 30
    assert all("name" in b for b in bookmakers)


def test_bet365_present_with_alt_names():
    bookmakers = get_bookmakers_raw()
    bet365 = next(b for b in bookmakers if b["name"] == "bet365")
    assert "Bet365" in bet365["altNames"]


def test_no_duplicate_bookmaker_names():
    names = [b["name"] for b in get_bookmakers_raw()]
    dupes = {n for n in names if names.count(n) > 1}
    assert not dupes, f"duplicate bookmaker(s): {dupes}"


def test_no_duplicate_alt_names_within_a_bookmaker():
    for b in get_bookmakers_raw():
        alt = b.get("altNames") or []
        assert len(alt) == len(set(alt)), f"duplicate altNames in {b['name']!r}: {alt}"
