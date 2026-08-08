from setuptools import setup, find_packages

setup(
    name="outrights-namematch",
    version="0.1.0",
    description="Fuzzy team-name resolution + canonical team data for outrights-* services.",
    url="https://github.com/jhw/outrights-namematch",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"outrights_namematch": ["data/teams/*.yaml", "data/markets/*.yaml", "data/leagues.yaml"]},
    include_package_data=True,
    install_requires=[
        "PyYAML>=6.0",
        "rapidfuzz>=3.0",
    ],
    python_requires=">=3.9",
)
