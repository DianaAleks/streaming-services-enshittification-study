# Word-length cuts: AI annotation results (run 2)

10,000 reviews (Netflix and Prime, 5 minimum-length cuts x 1,000) annotated with Claude (Sonnet subagents) using
`streaming-services-enshittification-study/annotation/codebook.md`, rules 1-11. Run on 2026-11-03.

## Files
- `summary_by_cut.csv`: per app and cut, share of reviews with each topic and with a *negative* comment on it, plus `x` share and median word count.
- `summary_by_cut_and_year.csv`: the same split by review year (2022, 2023, 2026). Cut files are not balanced by year (2026 is only 14-22% of each file), so read year splits with care.
- `annotated/`: the original cut files with `annotation`, `annotation_raw` and a `cleopatra_campaign` flag (not used to recode in this run, since the new codebook rules handle it).
- `labels/`, `chunks/`: raw AI labels and the 200-review chunks they were made from.
- `overlap_with_first_run.csv`: the 200 reviews that were also annotated in the first run (6,000-review run).
- `merge_results.py`: merge, validation and summary script (re-runnable).

## Main pattern (share of reviews, by cut)
Topic mix changes strongly with the length filter, so conclusions depend on which cut is used.

| | Netflix 3+ words | Netflix 10+ & 5+ likes | Prime 3+ words | Prime 10+ & 5+ likes |
|---|---|---|---|---|
| Negative pricing | 9% | 21% | 16% | 30% |
| Negative app | 27% | 57% | 38% | 60% |
| Unspecified (`u`) | 35% | 10% | 22% | 4% |
| Specific title (`m`) | 8.4% | 1.1% | 0.9% | 0.4% |

Short reviews are dominated by generic praise/complaint (`u`); long and well-liked reviews are mostly app and price complaints. The Netflix `m` share falls sharply with length because the short 2023 Cleopatra review-bombing reviews are filtered out.

## Reliability
- Same 200 reviews, two runs (different agents, codebook tightened between runs): 78.5% identical labels, 80.5% same topics. Disagreement is scattered (an extra or missing secondary code, and the `a`/`o` boundary), not systematic. Agreement is lowest in the 10+ words & 5+ likes cut (65%), where reviews have more topics.
- **Not yet checked against human labels.**
- Three agents mentioned fixing label/text misalignment; a 10-row spot check of each affected file found no misaligned rows, and the format check passes for all 50 files, but only a human review would rule out small shifts.

## Caveats
- Annotated by many agents in parallel; borderline rules were applied slightly differently (e.g. generic "blackwashing" complaints `o-` vs `m-`, rental complaints `p-` vs `a-`).
- Amazon shopping/delivery reviews were coded `o`; they are not about Prime Video.
- `x` (cannot annotate) is 0-2% in every cut.
