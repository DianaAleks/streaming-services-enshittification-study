# Annotation results (label-only)

Output of the AI annotation (Claude subagents, `annotation/codebook.md`). These files hold **labels and review ids only**, no review text and no scraped data, so the datasets are not in git. Re-join on `reviewId` with the Google Play review data (`annotation/collect_reviews.py`) or the word-length cut files.

| File | Content |
|---|---|
| `run1_labels_6000.csv` | Run 1: 1,000 random reviews per service (Netflix, Prime) and year (2022, 2023, 2026). `annotation_raw` is the AI label, `annotation` the label after recoding the Cleopatra campaign reviews to `m-`, flag in `cleopatra_campaign` |
| `run1_summary.csv` | Topic and negative-topic share per service and year for run 1 |
| `run2_word_length_labels_10000.csv` | Run 2: 10,000 reviews from the word-length cuts (5 minimum-length cuts x 2 apps x 1,000), annotated under codebook rules 1-11 |
| `run2_summary_by_cut.csv`, `run2_summary_by_cut_and_year.csv` | Topic shares per cut, and per cut and year |
| `run2_word_length_README.md` | Method, main pattern and caveats for run 2 |
| `run1_vs_run2_overlap_200.csv` | The 200 reviews annotated in both runs, with both labels and whether they match (78.5% identical, 80.5% same topics) |
| `merge_word_length_results.py` | Merge, validation and summary script for run 2 (`python merge_word_length_results.py <word_lenght folder>`) |

Codes: topic `c` catalogue, `p` pricing, `a` app, `m` specific title, `u` unspecified, `o` other, `x` cannot annotate; sentiment `+`, `0`, `-`.

**Not yet validated against human labels.** Run 1 and run 2 were annotated under slightly different codebooks (rules 8-11 were added for run 2).
