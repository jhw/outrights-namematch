from outrights_namematch import match, match_matchup


TEAMS = [
    {"name": "Arsenal"},
    {"name": "Manchester City", "altNames": ["Man City"]},
    {"name": "Manchester United", "altNames": ["Man United", "Man Utd"]},
    {"name": "Tottenham", "altNames": ["Spurs", "Tottenham Hotspur"]},
    {"name": "Nott'm Forest", "altNames": ["Nottingham Forest"]},
    {"name": "Wolves", "altNames": ["Wolverhampton Wanderers"]},
]


def test_exact_match():
    assert match("Arsenal", TEAMS) == "Arsenal"


def test_altname_match_for_true_alias():
    # Tottenham / Spurs is NOT fuzzy-recoverable — explicit altNames are the path.
    assert match("Spurs", TEAMS) == "Tottenham"


def test_altname_match_recovers_abbreviation_via_altname():
    assert match("Man City", TEAMS) == "Manchester City"


def test_punctuation_tolerance():
    assert match("Nottingham Forest", TEAMS) == "Nott'm Forest"


def test_levenshtein_close_match():
    # one-letter typo — within the <=2 threshold
    assert match("Arsenall", TEAMS) == "Arsenal"


def test_levenshtein_rejects_short_name_distance_two():
    # "Bolton" is a real club, distance 2 from "Burton", but not in this
    # roster — a raw source string for it must NOT resolve to the wrong
    # in-roster team. Regression for the Burton/Bolton event merge bug.
    teams = [{"name": "Burton"}, {"name": "Mansfield"}]
    assert match("Bolton", teams) is None
    assert match("Luton", teams) is None


def test_abbrev_match():
    # Abbreviation walker: "MC" -> "Manchester City"
    assert match("MC", TEAMS) == "Manchester City"


def test_unrecoverable_returns_none():
    assert match("Barcelona", TEAMS) is None


def test_empty_input_returns_none():
    assert match("", TEAMS) is None
    assert match("   ", TEAMS) is None


def test_matchup_splits_and_canonicalises():
    # "Man Utd vs Spurs" -> canonical names on both sides
    assert match_matchup("Man Utd vs Spurs", TEAMS) == "Manchester United vs Tottenham"


def test_matchup_rejects_duplicate_sides():
    # Same canonical team on both sides is a parsing bug, return None.
    assert match_matchup("Arsenal vs Arsenal", TEAMS) is None


def test_matchup_rejects_unparseable():
    assert match_matchup("just one team", TEAMS) is None


def test_matchup_v_or_vs():
    assert match_matchup("Man Utd v Spurs", TEAMS) == "Manchester United vs Tottenham"
