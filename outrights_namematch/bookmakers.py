"""Bundled bookmaker catalog.

Bookmaker identity data ships inside the package (``data/bookmakers.yaml``)
alongside league/market/team data, so it has one canonical source across
outrights-* apps — the same reasoning outrights-feed's config/loader.py
already gives for why leagues and markets moved here rather than staying
hand-maintained per app.

Flat, not per-league (a bookmaker isn't scoped to one league the way a
market is), so this mirrors leagues.py's shape rather than teams.py's.

Deliberately just identity data (name + known alternate spellings), not
app-specific curation: which of these a given app actually cares about
(outrights-portfolio's "soft retail books only" selection, an app's own
active/inactive flag) stays local to that app, exactly the way
consumer-side market-team-subset resolution stays local rather than living
here.

Public surface:

  get_bookmakers_raw()   -> list[dict]   # every bundled bookmaker row
"""
from __future__ import annotations

from importlib import resources

import yaml


def _data_dir():
    return resources.files(__package__).joinpath("data")


def get_bookmakers_raw() -> list[dict]:
    """Return every bundled bookmaker row (name, altNames)."""
    path = _data_dir().joinpath("bookmakers.yaml")
    return yaml.safe_load(path.read_text()) or []
