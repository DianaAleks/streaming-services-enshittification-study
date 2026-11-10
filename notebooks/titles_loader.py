"""Load the 2022, 2023 and 2026 Netflix/Amazon catalogues into one normalised table.

Run from the notebooks/ folder (paths are relative to the repo root via ROOT).
Every mapping done here is listed in comparison_data_issues.md.
"""
import ast
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "content_libraries"

SOURCES = {
    ("Netflix", 2022): LIB / "netflix_2022" / "titles.csv",
    ("Amazon", 2022): LIB / "amazon_2022" / "titles.csv",
    ("Netflix", 2023): LIB / "netflix_2023" / "netflix_titles_2023.csv",
    ("Amazon", 2023): LIB / "amazon_2023" / "amazon_titles_2023.csv",
}
ALL_2026 = ROOT / "all_titles_2026.csv"
NETFLIX_2026 = ROOT / "netflix_us_all.csv"  # used only to split all_titles_2026 by service

TYPE_MAP = {"MOVIE": "movie", "SHOW": "show", "movie": "movie", "series": "show"}
GENRE_MAP = {"documentation": "documentary"}  # 2022/23 name for the 2026 "documentary"
# genres that exist in only one of the two vocabularies; dropped from genre comparisons
GENRES_OLD_ONLY = {"european", "sport"}
GENRES_2026_ONLY = {"adventure", "mystery", "news", "talk"}


def _genres_old(s):
    try:
        return [GENRE_MAP.get(g, g) for g in ast.literal_eval(s)]
    except (ValueError, SyntaxError):
        return []


def _genres_2026(s):
    try:
        return [GENRE_MAP.get(d["id"], d["id"]) for d in ast.literal_eval(s)]
    except (ValueError, SyntaxError):
        return []


def _countries(s):
    try:
        return ast.literal_eval(s) if isinstance(s, str) else []
    except (ValueError, SyntaxError):
        return []


def _norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", str(t).lower()).strip()


def _prepare(df, service, year, genre_fn):
    out = pd.DataFrame({
        "service": service,
        "snapshot": year,
        "title": df["title"],
        "type": df["type"].map(TYPE_MAP),
        "release_year": df["release_year"],
        "runtime": df["runtime"],
        "genres": df["genres"].map(genre_fn),
        "countries": df["production_countries"].map(_countries),
        "seasons": df["seasons"],
        "imdb_id": df["imdb_id"],
        "imdb_score": df["imdb_score"],
        "imdb_votes": df["imdb_votes"],
    })
    # same title across years: IMDb id when we have it, otherwise title + year + type
    fallback = ("t:" + out["title"].map(_norm_title) + "|" + out["release_year"].astype(str)
                + "|" + out["type"].astype(str))
    out["key"] = out["imdb_id"].where(out["imdb_id"].notna(), fallback)
    return out


def load_titles():
    """Return (titles, report). `titles` has one row per title per service per snapshot."""
    frames, report = [], []
    for (service, year), path in SOURCES.items():
        frames.append(_prepare(pd.read_csv(path), service, year, _genres_old))

    a = pd.read_csv(ALL_2026)
    n_netflix = len(pd.read_csv(NETFLIX_2026))
    # all_titles_2026.csv is the Netflix export followed by the Amazon export
    for service, part in (("Netflix", a.iloc[:n_netflix]), ("Amazon", a.iloc[n_netflix:])):
        frames.append(_prepare(part, service, 2026, _genres_2026))

    raw = pd.concat(frames, ignore_index=True)
    # one row per key per service/snapshot: keep the row with the most IMDb votes
    raw = raw.sort_values("imdb_votes", ascending=False, na_position="last")
    titles = raw.drop_duplicates(["service", "snapshot", "key"]).copy()
    titles = titles.sort_values(["service", "snapshot"]).reset_index(drop=True)

    cov = raw.groupby(["service", "snapshot"]).size().rename("raw_rows").to_frame()
    cov["after_dedupe"] = titles.groupby(["service", "snapshot"]).size()
    cov["duplicates_dropped"] = cov["raw_rows"] - cov["after_dedupe"]
    cov["no_imdb_id_%"] = (titles.groupby(["service", "snapshot"])["imdb_id"]
                           .apply(lambda s: s.isna().mean() * 100).round(1))
    cov["imdb_score_%"] = (titles.groupby(["service", "snapshot"])["imdb_score"]
                           .apply(lambda s: s.notna().mean() * 100).round(1))
    cov["countries_%"] = (titles.groupby(["service", "snapshot"])["countries"]
                          .apply(lambda s: (s.str.len() > 0).mean() * 100).round(1))
    cov["runtime_%"] = (titles.groupby(["service", "snapshot"])["runtime"]
                        .apply(lambda s: s.notna().mean() * 100).round(1))
    return titles, cov
