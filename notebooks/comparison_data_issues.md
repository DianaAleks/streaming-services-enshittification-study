# Data issues and mappings: comparison_2022_2023_2026.ipynb

Read this before quoting any number from the notebook. Everything the loader (`titles_loader.py`) changes or drops is listed here.

## Sources used

| Snapshot | Files |
|---|---|
| Netflix 2022 | `content_libraries/netflix_2022/titles.csv` |
| Amazon 2022 | `content_libraries/amazon_2022/titles.csv` |
| Netflix / Amazon 2023 | `content_libraries/netflix_2023/netflix_titles_2023.csv`, `content_libraries/amazon_2023/amazon_titles_2023.csv` |
| Both 2026 | `all_titles_2026.csv`, split by service using `netflix_us_all.csv` |

The 2022 files are **not in git** (`content_libraries/` is gitignored) and must be obtained from the shared cloud folder or Kaggle (`victorsoeiro` Netflix/Amazon datasets). The notebook will not run without them.

## Mappings applied (same thing, different spelling)

| What | 2022 / 2023 | 2026 | Mapped to |
|---|---|---|---|
| Title type | `MOVIE`, `SHOW` | `movie`, `series` | `movie`, `show` |
| Genre list | Python list string, e.g. `['drama']` | list of `{id, name}` | list of lower-case ids |
| Documentary genre | `documentation` | `documentary` | `documentary` |
| Country list | Python list string | column empty | list (empty for 2026) |
| 2026 service | n/a | one file, Netflix rows first then Amazon rows | split by the row count of `netflix_us_all.csv` (verified: row 7,805 is the first Amazon title) |

## Same title across years

Titles are matched **within a service** on `imdb_id`. About 6.5% of 2022-2023 titles have no `imdb_id`; for those the match key is normalised title + release year + type. Remaining risk: a title whose IMDb id changed, or whose title/year differ between sources, appears as one removal plus one addition.

## Issues that affect the results

1. **No countries for 2026.** `production_countries` is empty in `all_titles_2026.csv`. The countries chart covers 2022 and 2023 only. A source would have to be joined on `imdb_id` (for example IMDb basics/akas or TMDB) to extend it.
2. **2026 genre tags are sparser.** Titles carry about 1.8-2.0 genre tags in 2026 against 2.1-2.6 in 2022-2023. Genre shares are therefore computed as the share of all genre tags (not of titles), otherwise almost every genre would appear to decline.
3. **Genre vocabularies differ.** `european` and `sport` exist only in 2022-2023; `adventure`, `mystery`, `news` and `talk` only in 2026. They are dropped from the genre comparison, which slightly changes the remaining shares.
4. **2026 runtime is often missing** (56.6% present for Netflix, 82.4% for Amazon; 100% in 2022-2023). Runtime is not used in the notebook.
5. **2026 has no age certification**, so age certification is not compared.
6. **IMDb coverage differs.** 2022-2023: about 90-92% of titles have an IMDb score. 2026: 98.6-99.4%. Quality figures describe the *rated* titles only, and the extra rated titles in 2026 may be less-known ones.
7. **IMDb votes and scores come from different scrape dates.** 2022 and 2023 come from Kaggle exports, 2026 from another source. Vote counts naturally grow with time, so higher 2026 votes are not by themselves evidence of more audience interest, and score changes on the same title mix real drift with source differences.
8. **Duplicates.** 5 rows in 2022, 3 in 2023 and 5 in 2026 share a key within a service and snapshot; the row with the most IMDb votes is kept. 99 titles appear on both services in 2026, which is expected and kept (analysis is per service).
9. **Snapshot years are approximate.** Netflix 2022 is July 2022, Amazon 2022 is May 2022, 2023 is March 2023, and 2026 is a partial year (only about 620 titles released in 2026). Title age is `snapshot year - release year`, so the newest age bucket is slightly understated for 2026.
10. **"Removed" is not the same as "pulled".** The datasets come from different sources and may define the catalogue differently. Amazon looks the most suspect: 24% of the 2022 titles are gone by 2023 (10 months), but 77% of the 2023 titles are gone by 2026, and 77% of the 2026 titles are new. This is more likely a change in what the 2026 export covers than a real turnover that large. Treat Amazon 2023 to 2026 churn as unverified. Netflix 2022 to 2023 (19% removed) is the most reliable comparison because both sources are similar Kaggle exports.
11. **The 2026 title list is the current catalogue only.** It has no history, so it cannot tell how long a title was available.

## Other places in the repo that still mention the Bayesian score

`analysis_2023.ipynb` (3 mentions) and `analysis_2023_guide.md` (2 mentions). The README, `analysis_2022.ipynb` and the 2026 notebook are clean. These files belong to whoever did the 2023 work and were not edited.
