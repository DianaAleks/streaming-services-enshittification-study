"""Stratified review samples for annotation: 1000 reviews per service and year.

Reads content_libraries/reviews/<service>_reviews.csv (from collect_reviews.py) and writes
content_libraries/annotation_samples/<service>_reviews_<year>_sample.csv plus
chunks/<service>_<year>_NN.csv (200 reviews each) used for the AI annotation run.
Run from the repo root or the annotation folder.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REVIEWS = ROOT / "content_libraries" / "reviews"
OUT = ROOT / "content_libraries" / "annotation_samples"
YEARS = [2022, 2023, 2026]
N_PER_STRATUM = 1000
CHUNK = 200
SEED = 42

(OUT / "chunks").mkdir(parents=True, exist_ok=True)
summary = []
for service in ("netflix", "prime"):
    df = pd.read_csv(REVIEWS / f"{service}_reviews.csv")
    df["at"] = pd.to_datetime(df["at"])
    df["year"] = df["at"].dt.year
    df["content"] = df["content"].fillna("").astype(str).str.strip()
    raw = len(df)
    df = df[df["content"].str.len() > 0].drop_duplicates(["year", "content"])
    for year in YEARS:
        pool = df[df["year"] == year]
        n = min(N_PER_STRATUM, len(pool))
        s = pool.sample(n=n, random_state=SEED).reset_index(drop=True)
        s.insert(0, "sample_id", [f"{service[0]}{year}-{i:04d}" for i in range(len(s))])
        s["annotation"] = ""
        s[["sample_id", "reviewId", "year", "score", "content", "annotation"]].to_csv(
            OUT / f"{service}_reviews_{year}_sample.csv", index=False)
        s["text"] = s["content"].str.replace(r"\s+", " ", regex=True).str[:500]
        for k in range(0, len(s), CHUNK):
            s.iloc[k:k + CHUNK][["sample_id", "score", "text"]].to_csv(
                OUT / "chunks" / f"{service}_{year}_{k // CHUNK:02d}.csv", index=False)
        summary.append((service, year, len(pool), n))
print(pd.DataFrame(summary, columns=["service", "year", "pool_after_dedupe", "sampled"]))
