# Review annotation codebook

Used for both the AI annotation and the manual (human) annotation, so the two can be compared.
It follows the codes in `automatic_annotation.ipynb`, with the rules below added so annotators resolve borderline cases the same way.

## Format

One annotation per review: one or more **topic+sentiment** codes separated by spaces, most prominent topic first, at most 3.
Examples: `p-`, `u+`, `a- c-`, `m+ c-`.

## Topics

| Code | Topic | Use when the review is about |
|---|---|---|
| `c` | Catalogue | Content selection, variety, what is or isn't available, titles removed, "nothing to watch" |
| `p` | Pricing | Subscription cost, price rises, ad tiers or ads, plan tiers, password-sharing fees, value for money |
| `a` | App | Bugs, crashes, buffering/playback, casting, downloads, login errors, interface, profiles |
| `m` | Specific title | The review is about one named movie/show (plot, acting, ending), not the service |
| `u` | Unspecified | General praise or complaint with no specific topic ("great app", "I love it", "terrible") |
| `o` | Other | Account and billing problems, cancellation, customer service, anything not covered above |
| `x` | Cannot annotate | Empty, unintelligible, spam or not in English (extension to the original codes) |

## Sentiment

| Code | Meaning |
|---|---|
| `+` | Positive toward that topic |
| `0` | Neutral or genuinely mixed |
| `-` | Negative toward that topic |

Each topic gets its own sentiment. "Love the shows but far too expensive" is `c+ p-`. `x` takes no sentiment.

## Rules for borderline cases

1. **Annotate the text, not the star rating.** The score is context only, for sarcasm or when the sentiment is truly unclear.
2. **Price vs billing.** Complaints about *how much it costs* or about ads are `p`. A wrong charge, a refund, or failed cancellation is `o`.
3. **Title vs catalogue.** Praise or criticism of one named title is `m`. A complaint that titles were removed, or that the library is small, is `c`.
4. **Playback vs app.** Buffering, crashes, freezing and cast failures are `a`, even when the user blames the content.
5. **Only code what is stated.** Do not infer a topic the review does not mention.
6. **Short generic reviews** ("good", "bad app") are `u` with the matching sentiment.
7. Use at most 3 codes. If more topics appear, keep the three most prominent.
