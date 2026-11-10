"""Collect US English Google Play reviews (newest first) back to a cutoff date.

Usage: python collect_reviews.py netflix|prime [cutoff_year]
Writes content_libraries/reviews/<service>_reviews.csv (gitignored). The file is appended
to after every page, so a stopped run still leaves usable data.
"""
import sys
import time
from pathlib import Path

import pandas as pd
from google_play_scraper import Sort, reviews

APPS = {"netflix": "com.netflix.mediaclient", "prime": "com.amazon.avod.thirdpartyclient"}
COLUMNS = ["reviewId", "content", "score", "thumbsUpCount", "at", "appVersion"]
OUT = Path(__file__).resolve().parent.parent / "content_libraries" / "reviews"


def collect(service, cutoff_year=2022, page_size=200, max_retries=6):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{service}_reviews.csv"
    path.unlink(missing_ok=True)
    token, total, pages = None, 0, 0
    while True:
        for attempt in range(max_retries):
            try:
                if token is None:
                    batch, token = reviews(APPS[service], lang="en", country="us",
                                           sort=Sort.NEWEST, count=page_size)
                else:
                    batch, token = reviews(APPS[service], continuation_token=token)
                break
            except Exception as e:  # network hiccups / rate limits
                print(f"  error: {e} (retry {attempt + 1}/{max_retries})", flush=True)
                time.sleep(3 * (attempt + 1))
        else:
            print("giving up after repeated errors", flush=True)
            return
        if not batch:
            return
        df = pd.DataFrame(batch)[COLUMNS]
        df.to_csv(path, mode="a", header=not path.exists(), index=False)
        total += len(df)
        pages += 1
        oldest = pd.to_datetime(df["at"]).min()
        if pages % 25 == 0:
            print(f"{service}: {total:,} reviews, oldest so far {oldest:%Y-%m-%d}", flush=True)
        if oldest.year < cutoff_year or token is None or token.token is None:
            print(f"{service}: done, {total:,} reviews, oldest {oldest:%Y-%m-%d}", flush=True)
            return
        time.sleep(0.3)


if __name__ == "__main__":
    collect(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2022)
