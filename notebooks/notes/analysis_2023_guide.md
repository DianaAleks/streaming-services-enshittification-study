# Guide to `analysis_2023.ipynb`

What each section does, what it can be used for, and a few of the numbers it produces.
Figures are from the current run (Netflix 2023: 6,137 titles, Amazon Prime 2023: 10,873 titles).

Terms used throughout:
- **kept / added / removed**: a title (matched on `id`) is *kept* if it is in both the 2022 and 2023 snapshots, *added* if only in 2023, *removed* if only in 2022.
- **high quality**: IMDb score ≥ 7 and ≥ 7,000 votes.
- **weighted IMDb**: Bayesian average that pulls scores with few votes towards the overall mean.

## Part A: One snapshot (2023), Netflix vs Amazon

| Section | What it does | Useful for | Example data points |
|---|---|---|---|
| 0 Import | Loads titles and credits for both services | Setup | – |
| 1.0–1.2 Dataset info | `info()`, `describe()`, share of missing values per column | Checking data quality before trusting any ratio | Netflix `imdb_score` missing for ~8%, `age_certification` for ~45% |
| 2.0 Combine | Stacks both services into one `catalog` table with a `service` column | Everything below compares services | – |
| 3.0–3.1 Movies vs shows | Counts and % split of type per service | Seeing how the catalog is composed | Shows are a much larger part of Netflix's catalog than of Amazon's; among 2023 additions it is 31.5% vs 16.7% (see 9.3) |
| 4.0 Content age | `2023 − release_year`, boxplot | Back-catalog vs fresh content | Mean release year: Netflix 2017, Amazon 2004 |
| 5.0 IMDb distribution | Histogram + mean/median/std | A first look at perceived quality | Mean IMDb: Netflix 6.54, Amazon 5.97 |
| 5.1 High quality + weighted score | Count and share of high-quality titles, Bayesian-weighted rating | A fairer measure than the plain mean, because a big catalog shouldn't be punished for its long tail | High-quality share: Netflix 13.2% (812 titles) vs Amazon 5.9% (641 titles) |
| 6.0 Genre distribution | Titles per genre per service | Where each service puts its volume | Drama and comedy lead on both |
| 6.1 Quality by genre | Mean (weighted) IMDb per genre | Which genres are rated highest | Documentation is the top-rated big genre (about 7.0) |
| 7.0 Country of origin | Share of each catalog per production country | How US-centric or international a catalog is | US: Amazon 55.4% vs Netflix 37.9%; South Korea: Netflix 4.4% vs Amazon 1.2% |

## Part B: 2022 → 2023 change (section 8)

The "enshittification" question: did the catalogs get bigger, older, or worse?

| Section | What it does | Useful for | Example data points |
|---|---|---|---|
| 8.0 Churn table | Titles in 2022 and 2023, kept / removed / added | The headline: how much of a catalog is replaced in a year | Amazon: 9,868 → 10,873 (+10.2%), 18.3% of the 2022 catalog removed. Netflix: 5,850 → 6,137 (+4.9%), 13.4% removed |
| 8.1 Movies vs shows per year | Type split per snapshot | Spotting a shift towards one format | |
| 8.2 Content age | Age distribution per snapshot | Whether catalogs are getting fresher or older | |
| 8.3 Quality per snapshot | Mean IMDb, weighted IMDb, high-quality count/share with one shared prior so all four snapshots are comparable | Quality trend over time | |
| 8.4 Genres per year | Genre counts 2022 vs 2023 and the change | Which genres grew or shrank | |
| 8.5 Added vs removed | One row per title with a status; profile per status; release-year histogram; removal rate per genre. Also writes `content_libraries/title_diff_2022_2023.csv` | Seeing what *leaves* vs what *replaces* it | Netflix removed titles have median 4,433 IMDb votes vs 1,529 for added ones, so better-known titles left and less-known ones came in. Amazon removed: median release year 2005, added: 2017 |
| 8.6 Kept titles | Change in votes and score for titles present in both years; how many had metadata rewritten | Separating "the title changed" from "the catalog changed" | |

## Part C: Only the difference (section 9)

Ignores everything that stayed and looks only at what is new or gone.

| Section | What it does | Useful for | Example data points |
|---|---|---|---|
| 9.0 Profile of added vs removed | Type split, median release year, share released in 2022 or later, IMDb, high-quality count | A compact "what changed" table | Netflix: 59% of added titles were released in 2022 or later, vs 0.5% of the removed. Amazon: 17.8% vs 0.55% |
| 9.1 Quality of the new titles | Boxplot and per-type (movie / show) quality of added vs removed; top 10 new high-quality titles per service | Whether new content is better or worse than what it replaces | Netflix movies: high-quality share 11.1% added vs 17.7% removed. Amazon shows: 14.7% added vs 11.2% removed |
| 9.2 Genre change relative to the catalog | See below | Which genres grew, and whether their rating moved | |
| 9.3 Origin and age of new titles | Country mix of added vs removed, release year of additions, movie/show split | Is new content local, international, recent, or back-catalog | |
| 9.4 Caveat: IMDb remapping | Counts kept titles whose `imdb_id` changed | Warning on interpreting score changes | 6.8% of Amazon and 6.2% of Netflix kept titles point to a different IMDb entry |

### 9.2 in detail

Every number is relative to the **2022 catalog of the same service and view**, so genres of very different sizes can be compared.

| Column | Meaning |
|---|---|
| Added % | Titles with this genre added in 2023, as % of the 2022 catalog |
| Removed % | Titles with this genre removed, as % of the 2022 catalog |
| **Net added %** | Added % − Removed %. Positive means the genre takes up more of the catalog |
| IMDb 2022 / 2023 / **change** | Mean IMDb score of the genre in each snapshot, and the difference |
| Rated % | Share of the genre's titles that have an IMDb score. A low value means the mean is less reliable |
| Metadata net titles | Titles that gained or lost the genre tag without being added or removed. A sanity check, usually close to 0 |

"Net added %" and "IMDb change" are colour-coded (green up, red down). Set `GENRE_VIEW` at the top of the cell to `"ALL"`, `"MOVIE"` or `"SHOW"` to switch between all titles, movies only or series only. The bar charts underneath show the top 10 genres by 2023 size for net added % and IMDb change.

Examples (all titles):

- **Netflix drama**: +9.47% added, −7.28% removed, so **+2.19%** net of the 2022 catalog; mean IMDb 6.62 → 6.63 (+0.01).
- **Netflix comedy**: **+2.41%** net; IMDb +0.05.
- **Netflix European**: **−1.06%** net, one of the few genres that shrank.
- **Amazon drama**: +14.87% added, −9.33% removed, **+5.53%** net; IMDb 6.13 → 6.11 (−0.02).
- **Amazon thriller**: **+3.09%** net; IMDb 5.54 → 5.51 (−0.03).

The reading: both services grew mostly in drama, comedy and thriller, and the average rating inside a genre barely moved (within ±0.1). Quality changes come from *which* titles are in the catalog (section 9.1), not from the genres themselves.

## Caveats

- A title can have several genres or countries, so genre and country shares add up to more than 100%.
- Roughly 6–7% of kept titles changed `imdb_id` between the snapshots (9.4), so some score changes are a different IMDb entry, not a re-rating.
- A few `id`s appear twice inside one snapshot (3 dropped in total); the first is kept.
