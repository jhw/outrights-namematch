import pytest

from outrights_namematch import parse_payoff
from outrights_namematch.payoff import parse_payoff as parse_payoff_direct


def test_parse_payoff_simple_shorthand():
    assert parse_payoff("1|19x0") == [1.0] + [0.0] * 19


def test_parse_payoff_multiple_repeated_chunks():
    assert parse_payoff("2x1|4x0.25|18x0") == [1.0, 1.0] + [0.25] * 4 + [0.0] * 18


def test_parse_payoff_bottom_shorthand():
    assert parse_payoff("17x0|3x1") == [0.0] * 17 + [1.0, 1.0, 1.0]


def test_parse_payoff_passes_through_a_list_unchanged_as_floats():
    assert parse_payoff([1, 0, 0]) == [1.0, 0.0, 0.0]


def test_parse_payoff_validates_expected_length():
    with pytest.raises(ValueError):
        parse_payoff("1|19x0", expected_length=10)


def test_parse_payoff_expected_length_ok_when_matching():
    assert parse_payoff("1|19x0", expected_length=20) == [1.0] + [0.0] * 19


def test_parse_payoff_rejects_malformed_chunk():
    with pytest.raises(ValueError):
        parse_payoff("1|notanumber")


def test_parse_payoff_rejects_zero_count():
    with pytest.raises(ValueError):
        parse_payoff("0x1|19x0")


def test_parse_payoff_rejects_empty_chunk():
    with pytest.raises(ValueError):
        parse_payoff("1||19x0")


def test_parse_payoff_rejects_non_string_non_list():
    with pytest.raises(ValueError):
        parse_payoff(42)


def test_parse_payoff_importable_from_submodule_directly():
    assert parse_payoff_direct("1|1x0") == [1.0, 0.0]


def test_parse_payoff_matches_every_bundled_market_shorthand():
    """Every real payoff shorthand shipped in data/markets/*.yaml must
    parse cleanly — catches a malformed config as much as a parser bug."""
    from outrights_namematch import get_leagues_raw, get_markets_raw

    for league in get_leagues_raw():
        for market in get_markets_raw(league["code"]):
            parse_payoff(market["payoff"])
