# Streaming Services Enshittification Study

## Objective

This study investigates whether the development of **Netflix and Amazon Prime Video between 2022–2026 in the US** is consistent with the process of **enshittification**.

The analysis focuses on how **price, content availability, content quality, and consumer value** change over time.

### Research Questions

**Q1:** How have subscription prices and the cost of ad-free viewing changed across Netflix and Amazon Prime over time?

**Q2:** How has the relationship between **service quality (price and content availability)** and **consumer value** changed over time, as measured by **content quality and customer satisfaction**?

WE ARE MISSING A CUSTOMER SATISFACTION SECTION (WILL DEFINE LATER)

# Dataset Analysis Approach

**For Sections 2 and 3**, Netflix and Amazon Prime datasets from 2022, 2023, and 2026 will first be analysed separately.

Step 1 - Individual analysis

Analyse each platform/year separately for:

- Content availability
- Release year
- Title origin
- IMDb score and votes
- Bayesian IMDb score

---

# 1. Price - Q1

Analyse changes in subscription and ad-free prices between **2022–2026**.

Measure:

- Monthly subscription price
- Ad-free price
- Absolute and percentage price changes
- Nominal vs. inflation-adjusted prices

This establishes how the **cost of the service has changed over time**.

---

# 2. Content Availability - Q1 & Q2

Analyse how the available catalogue changes between **2022–2026**:

- Number of titles available
- Release-year distribution
- New vs. older content
- Country/origin distribution
- Changes in catalogue composition

An influence function may be used to account for the effect of **release year/title age**.

This allows us to assess whether changes in price are accompanied by changes in the **amount and type of content available**.

---

# 3. Content Quality - Q2

Content quality will be measured using a **Bayesian weighted IMDb score**.

## Bayesian IMDb Score

[
WR = \frac{v}{v+m}R + \frac{m}{v+m}C
]

Where:

- **WR** = Bayesian weighted rating
- **R** = IMDb rating
- **v** = number of IMDb votes
- **m** = minimum vote threshold
- **C** = average IMDb rating

The Bayesian approach reduces the influence of titles with very few votes.

### Vote Threshold

The minimum vote threshold (**m**) will be determined by analysing the distribution of IMDb votes.

We will examine:

- Distribution of votes across titles
- Rating stability at different vote levels
- The appropriate threshold for reliable comparisons
- Titles with very low/no votes

Low IMDb votes will be treated as a **potential indicator of limited audience interest**, but not as a direct measure of viewing.

### Content Quality vs. Audience Interest

Using **Tudum viewing data**, compare:

- **What people watch** → viewing performance
- **What is considered good** → Bayesian weighted IMDb score

This will show whether **consumer interest aligns with perceived content quality**.

### IMDb Score Over Time

For titles that appear in multiple datasets, match the same titles across 2022, 2023, and 2026.

Compare:

- IMDb score in 2022 vs. 2026
- IMDb score in 2023 vs. 2026
- Number of IMDb votes across the years
- Bayesian weighted IMDb score across the years

This allows us to determine whether the quality of the same content changes over time, rather than simply comparing different catalogues each year.

---

# 4. Consumer Value & Satisfaction - Q2

The analysis will examine whether consumers receive more or less value from the service as prices and content change.

We will compare:

**Price + Content Availability → Service Quality → Consumer Value**

Key questions:

- Does a higher price correspond to more or better content?
- Does content quality improve, decline, or remain stable as prices increase?
- Does the catalogue become larger, smaller, newer, or older?
- Does consumer satisfaction change alongside price and content developments?
- Is there a growing gap between **what consumers pay and the value they receive**?

**Consumer satisfaction will be incorporated using available customer satisfaction data.**

---

# 5. Enshittification Analysis

The analysis will look for patterns such as:

> **Price ↑ + Content quality/availability ↓ or stagnates + Consumer value/satisfaction ↓**

The results will be compared across **2022–2026** and between **Netflix and Amazon Prime**.
