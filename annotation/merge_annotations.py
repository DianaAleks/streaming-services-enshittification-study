"""Merge AI labels into the samples, validate them, and summarise topics/sentiment per service and year.

Reads  content_libraries/annotation_samples/<service>_reviews_<year>_sample.csv and labels/<chunk>.csv
Writes <service>_reviews_<year>_sample_completed.csv, annotation_summary.csv and human_validation_set.csv
(100 reviews, 'annotation' left blank, for the team to label by hand for an accuracy check).
"""
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "content_libraries" / "annotation_samples"
CODE = re.compile(r"^[cpamuo][+0-]$")
CAMPAIGN = r"cleopatra|egypt|falsif|black.?wash|black.?wish|blakc|history fak"
TOPICS = {"c": "catalogue", "p": "pricing", "a": "app", "m": "title", "u": "unspecified", "o": "other"}
frames, problems = [], []
for service in ("netflix", "prime"):
    for year in (2022, 2023, 2026):
        s = pd.read_csv(DIR / f"{service}_reviews_{year}_sample.csv")
        parts = [pd.read_csv(f, dtype=str, keep_default_na=False)
                 for f in sorted((DIR / "labels").glob(f"{service}_{year}_*.csv"))]
        lab = pd.concat(parts) if parts else pd.DataFrame(columns=["sample_id", "annotation"])
        if lab.sample_id.duplicated().any():
            problems.append(f"{service} {year}: duplicate sample_ids in labels")
        s = s.drop(columns="annotation").merge(lab, on="sample_id", how="left")
        s["annotation"] = s["annotation"].fillna("").str.strip()
        s["annotation_raw"] = s["annotation"]
        # Review-bombing about the Cleopatra docudrama ("falsifying Egyptian history"): the annotators
        # coded it as o-, c- and m- in different chunks. Flag it and use one code (m-, a named title).
        s["cleopatra_campaign"] = s["content"].fillna("").str.contains(CAMPAIGN, case=False, regex=True)
        single_neg = s["annotation"].isin(["o-", "c-", "m-"])
        s.loc[s["cleopatra_campaign"] & single_neg, "annotation"] = "m-"
        missing = (s["annotation"] == "").sum()
        bad = [a for a in s["annotation"] if a and a != "x" and not all(CODE.match(t) for t in a.split())]
        if missing:
            problems.append(f"{service} {year}: {missing} reviews without a label")
        if bad:
            problems.append(f"{service} {year}: {len(bad)} invalid labels, e.g. {bad[:3]}")
        s.insert(0, "service", service)
        s.to_csv(DIR / f"{service}_reviews_{year}_sample_completed.csv", index=False)
        frames.append(s)
all_ = pd.concat(frames, ignore_index=True)
print("PROBLEMS:", problems or "none")
print("Cleopatra-campaign reviews per service/year (recoded where single o-/c-/m-):")
print(all_.groupby(["service", "year"]).cleopatra_campaign.sum().to_string())
print("recoded:", int((all_.annotation != all_.annotation_raw).sum()))

# one row per review x code
rows = []
for r in all_.itertuples():
    toks = r.annotation.split() if r.annotation else []
    for t in toks:
        rows.append((r.service, r.year, r.sample_id, "x" if t == "x" else TOPICS[t[0]],
                     "" if t == "x" else t[1]))
codes = pd.DataFrame(rows, columns=["service", "year", "sample_id", "topic", "sentiment"])
n_reviews = all_.groupby(["service", "year"]).size().rename("n_reviews")
topic_share = (codes.groupby(["service", "year", "topic"]).sample_id.nunique().unstack("topic").fillna(0)
               .div(n_reviews, axis=0).round(3))
neg = (codes[codes.sentiment == "-"].groupby(["service", "year", "topic"]).sample_id.nunique()
       .unstack("topic").fillna(0).div(n_reviews, axis=0).round(3).add_suffix("_negative"))
summary = pd.concat([n_reviews, topic_share, neg], axis=1)
summary.to_csv(DIR / "annotation_summary.csv")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(summary.to_string())

val = (all_.groupby(["service", "year"], group_keys=False).sample(n=17, random_state=7)
       .sample(n=100, random_state=7)[["sample_id", "service", "year", "score", "content"]])
val["annotation"] = ""
val.to_csv(DIR / "human_validation_set.csv", index=False)
print("validation set:", len(val), "reviews")
