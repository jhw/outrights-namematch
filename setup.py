from setuptools import setup, find_packages

setup(
    name="outrights-namematch",
    version="0.5.4",
    description="Fuzzy team-name resolution + canonical team/market data for outrights-* services.",
    url="https://github.com/jhw/outrights-namematch",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"outrights_namematch": ["data/teams/*.yaml", "data/markets/*.yaml", "data/leagues.yaml"]},
    include_package_data=True,
    install_requires=[
        "PyYAML>=6.0",
    ],
    extras_require={
        # Only match()/match_matchup()/clean_text() need this — a consumer
        # of just the bundled static data (get_markets_raw, get_teams_raw,
        # parse_payoff, ...) doesn't pay for a compiled extension it never
        # calls into (see outrights_namematch/__init__.py's lazy __getattr__).
        "fuzzy": ["rapidfuzz>=3.0"],
    },
    python_requires=">=3.9",
)
