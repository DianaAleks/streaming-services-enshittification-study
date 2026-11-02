"""Merge AI labels for the word-length cuts, validate, summarise, and compare with the first run.

Reads  ../*_sample_cuts/*.csv and labels/<app>_cut<N>_<NN>.csv
Writes annotated/<original cut file name>, summary_by_cut.csv, summary_by_cut_and_year.csv,
       overlap_with_first_run.csv (reviews annotated in both runs).
"""
import glob
import os
import re
from pathlib import Path

import pandas as pd

import sys
# usage: python merge_word_length_results.py <path to word_lenght folder>   (needs results/labels there)
ROOT = Path(sys.argv[1])
BASE = ROOT / "results"
FIRST_RUN = Path(__file__).resolve().parent.parent.parent / "content_libraries" / "annotation_samples"
CODE = re.compile(r"^[cpamuo][+0-]$")
TOPICS = {"c": "catalogue", "p": "pricing", "a": "app", "m": "title", "u": "unspecified", "o": "other"}
CUT_NAMES = {"1": "3+ words", "2": "5+ words", "3": "8+ words", "4": "10+ words", "5": "10+ words & 5+ likes"}
CAMPAIGN = r"cleopatra|egypt|falsif|black.?wash|black.?wish|blakc|history fak"

problems, frames = [], []
for f in sorted(glob.glob(str(ROOT / "*_sample_cuts" / "*.csv"))):
    d = pd.read_csv(f)
    app = d["app"].iloc[0]
    cut = os.path.basename(f).split("_samples_")[1].split("_")[0]
    lab = pd.concat([pd.read_csv(x, dtype=str, keep_default_na=False)
                     for x in sorted(glob.glob(str(BASE / "labels" / f"{app}_cut{cut}_*.csv")))])
    if lab.sample_id.duplicated().any():
        problems.append(f"{app} cut{cut}: duplicate ids in labels")
    d = d.merge(lab.rename(columns={"sample_id": "reviewId"}), on="reviewId", how="left")
    d["annotation"] = d["annotation"].fillna("").str.strip()
    miss = (d.annotation == "").sum()
    bad = [a for a in d.annotation if a and a != "x" and not all(CODE.match(t) for t in a.split())]
    if miss: problems.append(f"{app} cut{cut}: {miss} unlabeled")
    if bad: problems.append(f"{app} cut{cut}: {len(bad)} invalid e.g. {bad[:3]}")
    d["annotation_raw"] = d["annotation"]
    d["cleopatra_campaign"] = d["content"].fillna("").str.contains(CAMPAIGN, case=False, regex=True)
    d.insert(0, "cut", CUT_NAMES[cut])
    os.makedirs(BASE / "annotated", exist_ok=True)
    d.to_csv(BASE / "annotated" / os.path.basename(f), index=False)
    frames.append(d)
print("PROBLEMS:", problems or "none")
all_ = pd.concat(frames, ignore_index=True)

rows = []
for r in all_.itertuples():
    for t in (r.annotation.split() if r.annotation else []):
        rows.append((r.app, r.cut, r.year, r.reviewId, "x" if t == "x" else TOPICS[t[0]], "" if t == "x" else t[1]))
codes = pd.DataFrame(rows, columns=["app", "cut", "year", "reviewId", "topic", "sentiment"])


def summarise(keys):
    n = all_.groupby(keys).size().rename("n_reviews")
    share = codes.groupby(keys + ["topic"]).reviewId.nunique().unstack("topic").fillna(0).div(n, axis=0)
    neg = (codes[codes.sentiment == "-"].groupby(keys + ["topic"]).reviewId.nunique()
           .unstack("topic").fillna(0).div(n, axis=0).add_suffix("_negative"))
    wc = all_.groupby(keys).word_count.median().rename("median_words")
    return pd.concat([n, wc, share, neg], axis=1).round(3)


s1 = summarise(["app", "cut"]); s2 = summarise(["app", "cut", "year"])
order = {v: i for i, v in enumerate(CUT_NAMES.values())}
s1 = s1.sort_index(key=lambda ix: ix.map(order) if ix.name == "cut" else ix)
s2 = s2.sort_index(key=lambda ix: ix.map(order) if ix.name == "cut" else ix)
s1.to_csv(BASE / "summary_by_cut.csv"); s2.to_csv(BASE / "summary_by_cut_and_year.csv")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(s1.to_string())

# agreement with the first run on reviews that were annotated in both
first = pd.concat([pd.read_csv(FIRST_RUN / f"{s}_reviews_{y}_sample_completed.csv", keep_default_na=False)
                   for s in ("netflix", "prime") for y in (2022, 2023, 2026)])
m = all_.merge(first[["reviewId", "annotation_raw", "annotation"]].rename(
    columns={"annotation_raw": "run1_raw", "annotation": "run1"}), on="reviewId")
if len(m):
    topics = lambda a: set(t[0] for t in a.split() if t != "x") or {"x"}
    full = lambda a: set(a.split())
    m["exact_match"] = [full(a) == full(b) for a, b in zip(m.annotation, m.run1)]
    m["topic_match"] = [topics(a) == topics(b) for a, b in zip(m.annotation, m.run1)]
    m[["app", "cut", "year", "reviewId", "content", "run1", "annotation", "exact_match", "topic_match"]].to_csv(
        BASE / "overlap_with_first_run.csv", index=False)
    print(f"\noverlap with first run: {len(m)} reviews | exact match {m.exact_match.mean():.1%} | "
          f"same topics {m.topic_match.mean():.1%}")
