# AI annotation run: method and caveats

Recreation of the Gemini annotation (`automatic_annotation.ipynb`) using Claude, run on 2026-10-26.

## Pipeline
1. `collect_reviews.py` scraped US English Google Play reviews (newest first) back to 2022-01-01: 386,200 Netflix and 304,600 Prime reviews.
2. `create_samples.py` drew 1,000 reviews per service and year (2022, 2023, 2026; seed 42) after dropping empty and duplicate texts. Texts were cut at 500 characters for annotation.
3. Ten Claude (Sonnet) subagents each annotated 3 chunks of 200 reviews with `codebook.md` (zero-shot: no human-labelled examples exist in the repo). Each chunk was checked for row count, sample ids and valid codes.
4. `merge_annotations.py` merged and re-validated all 6,000 labels, applied the recode below, and wrote `*_sample_completed.csv`, `annotation_summary.csv` and `human_validation_set.csv` in `content_libraries/annotation_samples/` (gitignored).

## Caveats
- **Accuracy is unmeasured.** Nothing has been compared with human labels yet. Label the 100 reviews in `human_validation_set.csv` by hand (without looking at the AI labels), then compute agreement.
- **Different agents annotated different chunks.** Borderline calls differ between chunks. The one found so far is the Cleopatra campaign below; others may exist.
- **Cleopatra review-bombing (Netflix 2023).** 84 of the 1,000 Netflix 2023 reviews are about the Cleopatra docudrama ("falsifying Egyptian history"). Agents coded them `o-`, `c-` or `m-` depending on the chunk. Where the label was a single `o-`, `c-` or `m-` it is now `m-` (51 recoded); the original is kept in `annotation_raw` and the flag in `cleopatra_campaign`. Consider excluding flagged rows when comparing years, since this is a one-off event, not a trend.
- **Prime 2023 chunk 0** had repeated topic codes dropped inside a review, so a review with both praise and criticism of the app keeps one `a` code.
- **`x` (cannot annotate)** covers non-English, emoji-only, gibberish and too-vague reviews: 7.9% overall, 14.6% for Netflix 2022 down to 2.7% for Prime 2026.
- Culture-war complaints about religious or LGBTQ content were coded `o-` (no better topic in the codebook).
- Review text limited to 500 characters; samples are random within a year, not weighted by thumbs-up.
