# Hard-to-Count Population Dashboard

A dashboard to identify and describe communities with characteristics associated with hard-to-count populations, built using Consumer Expenditure Survey (CE) paradata from the Bureau of Labor Statistics.

---

## Project Overview

"Hard to Count" (HTC) populations are groups with characteristics that make accurate counting more difficult in the census or surveys. The Census Bureau organizes these characteristics into four conceptual segments of the HTC framework:

- **Hard to Interview** — situations where language, health, or technological factors make it difficult to conduct the interview itself
- **Hard to Locate** — situations where a household's physical location is difficult to confirm (address issues, household moved, unit uncertainty)
- **Hard to Persuade** — situations where contact with the household was established, but the respondent declined to participate — whether due to privacy concerns, government distrust, or stated reasons such as being too busy or scheduling constraints
- **Hard to Contact** — situations where the household's location is known but the interviewer was unable to make any contact with anyone there (no one home, locked gate, no answer at door)

**Important distinction:** These HTC framework segments are *conceptual categories* from the Census literature. The MCHI dataset does not measure them directly — instead, it contains interviewer-recorded indicators that *correspond to* certain segments of the HTC framework. This project maps those MCHI-derived indicators to the appropriate HTC framework segment. The indicators should not be treated as equivalent to the framework categories themselves.

This project uses CE paradata — data about *how* the survey was conducted — to identify patterns in contact difficulty that correspond to HTC populations. The goal is a dashboard that helps planners and outreach staff understand where these characteristics concentrate and what factors drive them.

---

## Data Sources

**Consumer Expenditure Survey Public Use Microdata (CE-PUMD)**
Bureau of Labor Statistics — [https://www.bls.gov/cex/pumd_doc.htm](https://www.bls.gov/cex/pumd_doc.htm)

| File | Description |
|---|---|
| `mchi2324.csv` | Mode and Contact History Interview paradata, 2023–2024. One row per contact attempt (~522K rows, ~36K households). Primary data source. |
| `fpar2324.csv` | Final Paradata, 2023–2024. One row per household **per wave** (~102,733 rows, ~36,270 households, up to 4 waves each). Records final wave outcome, converted-refusal flag, interview mode (personal visit vs phone), and interview timing/burden. Covers virtually the same households as MCHI (99.9% overlap), so findings here are not subject to the small-subset caveat that applies to FMLI. |
| `fmli2202.csv`–`fmli2501.csv` | Family/household characteristics and income files, 12 quarterly extracts (2022 Q2 – 2025 Q1), combined, deduplicated, and restricted to MCHI-matching households — 20,396 households, one row per household. Adds geography, demographics, tenure, and income — variables MCHI does not have. |
| `ce-pumd-interview-diary-dictionary.xlsx` | Official data dictionary for all CE-PUMD variables and coded values. |

> **Note:** Raw data files are not included in this repository. Download them directly from the BLS CE-PUMD page linked above.

> **Coverage caveat for FMLI:** `clean_fmli.py` combines all quarterly FMLI extracts currently on hand (2022 Q2 through 2025 Q1), keeps the most recent wave per household, and restricts the output to households that also appear in MCHI (dropping FMLI households outside the HTC study, so the saved file can't be misread as covering more than it does). This covers 20,396 of the 36,270 MCHI households (56.2%) — up from 12.9% with a single quarter, 32.8% with five quarters, 47.8% with eight — and is close to the practical ceiling: only 55 of the 19,177 MCHI households with an ever-completed wave are still unmatched. The overlap is still skewed toward completed interviews (70.1% completion vs. 39.5% in the full MCHI sample), since FMLI can only ever contain households that completed at least one wave. Treat any FMLI-based demographic finding as descriptive of this larger but still non-representative subset, not the full HTC population.

---

## HTC Framework to MCHI Crosswalk

The table below maps each Census HTC framework segment to the MCHI-derived indicators used in this analysis, along with the specific variable codes and their descriptions.

| HTC Framework Segment | MCHI Indicator | MCHI Variable | Variable Description |
|---|---|---|---|
| **Hard to Interview** | Language barrier | `NONINTR4` | Language was the reason the interview could not be conducted |
| **Hard to Interview** | Language barrier | `LNGUAGE2` | No household member was able to translate |
| **Hard to Interview** | Language barrier | `LNGUAGE4` | Interviewer was unable to find a translator |
| **Hard to Interview** | Language barrier | `LNGUAGE5` | No time left to find a translator |
| **Hard to Interview** | Language barrier | `LANGLIST` | Language spoken by the household (coded list) |
| **Hard to Interview** | Language barrier | `FNLOTCME=323` | Final outcome: refused due to language problem |
| **Hard to Interview** | Health barrier | `NONINTR5` | Respondent or household had a health problem preventing the interview |
| **Hard to Locate** | Address instability | `NCTPER08` | Address does not exist or interviewer was unable to locate it |
| **Hard to Locate** | Address instability | `FNLOTCME=341` | Final outcome: household moved during survey period |
| **Hard to Persuade** | Privacy / participation concerns | `RSPDNT07` | Interviewer recorded: respondent cited privacy concerns |
| **Hard to Persuade** | Privacy / participation concerns | `RSPDNT08` | Interviewer recorded: respondent cited concerns about government data collection |
| **Hard to Persuade** | Privacy / participation concerns | `RSPDNT11` | Interviewer recorded: contact was ended abruptly by respondent |
| **Hard to Persuade** | Privacy / participation concerns | `RSPDNT12` | Interviewer recorded: respondent expressed strong objection to continued contact |
| **Hard to Persuade** | Privacy / participation concerns | `NONINTR3` | Interviewer recorded: respondent indicated hesitation to participate |
| **Hard to Persuade** | Scheduling / availability decline | `NONINTR2` | Respondent indicated the time was inconvenient (contact was established) |
| **Hard to Persuade** | Scheduling / availability decline | `RSPDNT02` | Respondent said they were too busy (contact was established) |
| **Hard to Persuade** | Scheduling / availability decline | `RSPDNT05` | Respondent cited scheduling difficulties (contact was established) |
| **Hard to Persuade** | Scheduling / availability decline | `FNLOTCME=321` | Final outcome: interview not completed due to respondent non-participation |
| **Hard to Persuade** | Scheduling / availability decline | `FNLOTCME=322` | Final outcome: interview not completed, respondent cited time-related reasons |
| **Hard to Contact** | Contact not established | `NCTPER07` | Unable to reach household — locked gate or buzzer-entry building |
| **Hard to Contact** | Contact not established | `NCTPER01` | No one home on personal visit |
| **Hard to Contact** | Contact not established | `NCTPER04` | Someone appeared to be home but did not answer the door |
| **Hard to Contact** | Contact not established | `NCTPER11` | Interviewer had to go through building management or doorman |
| **Hard to Contact** | Contact not established | `FNLOTCME=216` | Final outcome: no one home, unable to make any contact |

---

## Methodology

### Step 1 — Data Aggregation
The MCHI file is structured as one row per **contact attempt**. Because a single household can have many contact attempts, we first aggregate to the **household level** using the `CUID` field (household identifier).

For each household we compute:
- Total number of contact attempts
- Days in the field (`DYSINFLD` max)
- Final interview outcome (`FNLOTCME`)
- Whether any indicator for each HTC segment was flagged across any contact attempt
- Count of each respondent characteristic flag (`RSPDNT*`)
- Count of each non-interview reason flag (`NONINTR*`)

### Step 2 — HTC Indicator Construction
Each household is assigned a binary flag (0 or 1) for each of the four HTC framework segments based on whether any corresponding MCHI indicator was recorded across all contact attempts:

| HTC Segment | MCHI Indicators Used |
|---|---|
| Hard to Interview | `NONINTR4`, `LNGUAGE2`, `LNGUAGE4`, `LNGUAGE5`, `LANGLIST`, `FNLOTCME=323`, `NONINTR5` |
| Hard to Locate | `NCTPER08`, `FNLOTCME=341` |
| Hard to Persuade | `RSPDNT07`, `RSPDNT08`, `RSPDNT11`, `RSPDNT12`, `NONINTR3`, `NONINTR2`, `RSPDNT02`, `RSPDNT05`, `FNLOTCME=321`, `FNLOTCME=322` |
| Hard to Contact | `NCTPER07`, `NCTPER01`, `NCTPER04`, `NCTPER11`, `FNLOTCME=216` |

### Step 3 — Analysis
Patterns are analyzed across:
- Interview wave (`INTERI`) — does contact difficulty increase in later waves?
- Quarter (`QYEAR`) — seasonal patterns in contact success
- Language group (`LANGLIST`) — which language communities have the most Hard to Interview indicators
- HTC indicator combinations — which segment indicators co-occur most often

### Step 4 — Dashboard
An interactive dashboard built in Python (Plotly Dash) displays the HTC indicators and allows users to filter and explore the data.

---

## Project Structure

```
.
├── data/
│   ├── raw/            # Source CSV files (not tracked in git)
│   └── processed/      # Cleaned, aggregated outputs
├── scripts/
│   ├── clean_mchi.py         # Aggregates MCHI to household level, creates HTC indicators
│   ├── clean_fmli.py         # Cleans FMLI household demographics/income, decodes coded values
│   ├── clean_fpar.py         # Cleans FPAR wave-level outcomes, mode, and interview timing
│   └── visualizations.py     # Generates interactive charts from cleaned data
├── dashboard/
│   ├── app.py                 # Dash app -- layout, tabs, callbacks
│   ├── data.py                 # Loads/joins mchi_clean, fpar_clean, fmli_clean
│   └── charts.py               # Figure-building functions
├── findings_report.md        # Detailed findings from MCHI analysis
├── README.md
└── .gitignore
```

---

## Research Focus

### Primary Research Question
*What patterns of contact difficulty in the CE Interview survey correspond to characteristics associated with hard-to-count populations, and do these characteristics tend to cluster together within the same households?*

### Sub-questions
1. Which HTC framework segments — Hard to Interview, Hard to Locate, Hard to Persuade, Hard to Contact — are most prevalent among households that did not complete the survey?
2. Do indicators from multiple HTC segments appear in the same household, and how does the presence of multiple segment indicators relate to interview completion rates?
3. Which HTC segment indicators are associated with the highest interviewer effort (contact attempts, days in field), and what outreach strategies were used in response?

---

## Key Findings

### HTC Indicator Prevalence
Analysis of the 36,270 households in the MCHI 2023–2024 data shows that Hard to Persuade and Hard to Contact are nearly equally prevalent, each present in roughly 3 in 4 households. Hard to Locate is the rarest.

| HTC Framework Segment | Households Flagged | % of Total |
|---|---|---|
| Hard to Persuade | 28,720 | 79.2% |
| Hard to Contact | 28,092 | 77.5% |
| Hard to Interview | 3,754 | 10.4% |
| Hard to Locate | 335 | 0.9% |

*Hard to Interview grew from 1,365 (3.8%) after `NONINTR5` (health problem) was added to the indicator set alongside the language codes — see Limitations for the technological-barrier gap this doesn't close.*

### Indicator Clustering
A key focus of this analysis is understanding how HTC indicators **cluster** — whether the same households tend to show indicators from multiple HTC segments simultaneously. This matters because households flagged across multiple segments are associated with significantly more interviewer contact attempts and lower completion rates.

Among the 36,270 households:

| Number of HTC Segments Flagged | Households | % of Total |
|---|---|---|
| 0 (no indicators) | 1,579 | 4.4% |
| 1 segment | 11,381 | 31.4% |
| 2 segments | 20,442 | 56.4% |
| 3 segments | 2,836 | 7.8% |
| 4 segments | 32 | 0.1% |

### The Compounding Effect
As the number of HTC segments flagged per household increases, interviewer effort rises and completion rates fall:

| Segments Flagged | Households | Avg Contact Attempts | Completion Rate |
|---|---|---|---|
| 0 | 1,579 | 4.1 | 71.1% |
| 1 | 11,381 | 10.2 | 43.7% |
| 2 | 20,442 | 16.8 | 35.4% |
| 3 | 2,836 | 19.8 | 34.1% |
| 4 | 32 | 21.0 | 37.5% |

### Most Common Co-occurring Segment Pairs

| Segment Pair | Households | % of Total |
|---|---|---|
| Hard to Contact + Hard to Persuade | 22,244 | 61.3% |
| Hard to Contact + Hard to Interview | 3,013 | 8.3% |
| Hard to Persuade + Hard to Interview | 3,306 | 9.1% |
| Hard to Contact + Hard to Locate | 289 | 0.8% |
| Hard to Persuade + Hard to Locate | 248 | 0.7% |
| Hard to Locate + Hard to Interview | 42 | 0.1% |

Checked statistically (chi-square test of independence, plus expected-vs-observed lift): the dominant pair, Hard to Contact + Hard to Persuade, is indistinguishable from what pure independence predicts (lift = 1.00, p = 1.0) — its size on paper is fully explained by both segments being individually common, not a special relationship. The other five pairs show statistically real but small associations (lift 0.93–1.21), detectable mainly because of the large sample size.

Wave, season, and language patterns are now all covered: wave and language above, and seasonality (completion by calendar quarter) in the dashboard's MCHI Segments tab and `findings_report.md` — completion holds flat across all 9 quarters on hand (37.6–41.9%), no meaningful seasonal signal.

---

## FMLI Supplement — Geography, Demographics & Income

MCHI contains no geographic or demographic variables, so on its own it can't say *where* HTC patterns concentrate or *who* they affect. The FMLI files fill that gap: household-level Consumer Expenditure data keyed by the same `CUID`, adding Census region/division, urban/rural status, housing tenure, income, and reference-person demographics (age, sex, race, Hispanic origin, education, marital status).

`clean_fmli.py` combines every quarterly FMLI extract currently available — `fmli2202.csv` through `fmli2501.csv` (2022 Q2 – 2025 Q1, 12 quarters) — since each quarter's file only contains households interviewed in that specific quarter, and the same household reappears in a later quarter once it reaches its next wave. Combining all 12 quarters raised the MCHI match rate from 12.9% (one quarter) → 32.8% (five quarters, 2024 Q1–2025 Q1) → 47.8% (eight quarters, adding 2023 Q2–Q4) → **56.2%** now that 2022 Q2–2023 Q1 are included.

**This is close to the practical ceiling, not a coverage gap.** FMLI only contains households that *completed* at least one interview wave — a household that never completed any of its up-to-5 waves will never generate an FMLI record, no matter how many quarters are added. Checking directly: 19,177 MCHI households have a completed wave somewhere in their contact history (not just their final one), and the current match already covers 20,396 of them (more, since some FMLI-eligible completions — e.g. insufficient partials — aren't coded `201` in MCHI). Only 55 ever-completed households are still unmatched, and their completions fall inside quarters we already have, so they're likely CUID/data-quality edge cases rather than a missing-quarter problem. The remaining 43.8% of MCHI households simply never completed an interview — structurally invisible to FMLI, not a gap more quarters can close.

**What it adds that MCHI can't:**
- Census region, division, urban/rural, and metro-area status
- Housing tenure (own w/ mortgage, own outright, rent, no cash rent, student housing)
- Household income (raw, quartile, and % of poverty threshold) and family size/type
- Reference-person age, sex, race, Hispanic origin, education, and marital status

**Coverage caveat:** 20,396 of the 36,270 MCHI households (56.2%) have a matching `CUID` across the 12 combined FMLI quarters (2022 Q2 – 2025 Q1) — close to the practical ceiling described above. It still skews toward completed interviews (70.1% completion here vs. 39.5% in the full MCHI sample) — a household only reaches a given wave's FMLI file if it completed at least one wave. The patterns below describe **this larger but still non-representative subset** — treat them as a secondary angle (which households, among those who ever engage, look different), not a population-level finding about the full HTC population.

### Patterns in the matched subset (n = 20,396)

| Breakdown | Group | Households | Completion Rate | Avg HTC Segments |
|---|---|---|---|---|
| **Tenure** | Rented | 7,005 | 68.6% | 1.70 |
| | Owned w/ mortgage | 7,406 | 69.1% | 1.68 |
| | Owned w/o mortgage | 5,641 | 73.5% | 1.62 |
| **Age of reference person** | ≤34 | 3,950 | 65.4% | 1.66 |
| | 35–49 | 5,020 | 67.6% | 1.72 |
| | 50–64 | 5,237 | 69.8% | 1.69 |
| | 65+ | 6,189 | 75.1% | 1.61 |
| **Urban/Rural** | Rural | 1,200 | 71.7% | 1.51 |
| | Urban | 19,196 | 70.0% | 1.68 |
| **Region** | Midwest | 3,872 | 70.3% | 1.65 |
| | Northeast | 3,305 | 68.9% | 1.64 |
| | South | 7,230 | 70.7% | 1.65 |
| | West | 5,595 | 70.2% | 1.71 |

**What this suggests (patterns held up after nearly doubling the matched sample):**
- **Renters and younger reference-person households still show more HTC segments flagged and lower completion** than owners and older reference-person households.
- **Older households (65+) remain the easiest to complete** (75.1%) but no longer carry the fewest HTC segments (1.61 avg, close to the overall average) — this shifted after `NONINTR5` (health problem) was added to Hard to Interview, since health barriers skew older.
- **Income quartile still shows no clean monotonic relationship** with completion or segment count — this looks like a genuine null result, not small-sample noise, now that the subset is more than 2.5x its original size.
- **Region differences remain modest** (a couple of points of completion). **Urban/rural has flipped direction** on this larger sample — rural now completes slightly *better* than urban (71.7% vs. 70.0%, a reversal from the earlier 75.5%/75.4% near-tie) — but the gap is still small enough that it shouldn't drive outreach strategy on its own; treat it as noise unless it holds up with even more data.

**Digging into *why* age matters — it's Hard to Contact, not Hard to Persuade:**

| HTC Segment | ≤34 (n=3,950) | 65+ (n=6,189) | Gap |
|---|---|---|---|
| Hard to Persuade | 83.3% | 83.0% | +0.3 pts |
| Hard to Contact | 74.7% | 62.4% | **+12.3 pts** |
| Hard to Interview | 7.0% | 15.2% | **-8.2 pts** |
| Hard to Locate | 0.6% | 0.7% | -0.1 pts |

Younger reference-person households aren't harder to *persuade* — the persuade rate is nearly identical across age. The entire *contact* gap runs the other way from Hard to Interview: younger households are simply harder to physically catch at home (busier or less predictable schedules), while older households are more than twice as likely to be flagged Hard to Interview — a direct consequence of `NONINTR5` (health problem preventing the interview), since health barriers to being interviewed rise with age even though barriers to being reached in the first place don't.

**Age and tenure are confounded, so treat them as one signal, not two:** 63.2% of ≤34 households rent, versus only 21.6% of 65+ households (who are 52.2% mortgage-free owners). Because age and tenure move together this strongly, the "renters are harder" and "under-35s are harder" findings above are likely capturing the **same underlying pattern** — residential/schedule stability — rather than two independent effects. Don't cite them as two separate reasons in the same argument.

---

## FPAR Supplement — Conversion, Interview Mode & Burden

MCHI records every contact *attempt*, but it doesn't record what actually happened once an interview took place — whether the interviewer talked the household out of an initial refusal, whether the interview was ultimately done in person or by phone, or how long it took. FPAR (`fpar2324.csv`) fills that gap. Unlike FMLI (56.2% match rate even combining 12 quarters), FPAR covers virtually the entire MCHI population (36,270 of 36,271 households, 99.9%), so its findings are not subject to the subset caveat that applies to the FMLI supplement — they describe the real population.

FPAR is structured one row per household **per wave** (up to 4 waves each), which is finer-grained than MCHI's household-level aggregate. `clean_fpar.py` keeps that wave-level granularity rather than collapsing it, because wave-to-wave change is itself the interesting signal.

**What it adds that MCHI can't:**
- `CONVREF` — whether a wave was a **converted refusal** (household initially refused, interviewer got them to complete anyway)
- Interview mode per wave (`HOW_INTV`, `TELPV`) — personal visit vs. phone, and why phone was used (`TEL_RESN`)
- Interview burden: total interview time, time per section, number of "Don't Know"/"Refused" answers, whether the respondent used records/bills
- Housing unit type (`HSG_UNIT`) and interview language (`LANGUAGE`)

### Finding — Converted refusals are rare but highly effective
Among the 28,720 households flagged Hard to Persuade in MCHI, interviewers successfully **converted** only 16.8% from refusal to a completed interview. But when they did, the payoff was large:

| Hard-to-Persuade Households | n | Completion Rate |
|---|---|---|
| Ever converted refusal | 4,832 | 73.7% |
| Never converted | 23,888 | 35.4% |

Across **all** households (not just Hard to Persuade), 5,284 (14.6%) had at least one wave flip from refusal to completion, and those households completed at 74.4% vs. 33.5% for the rest. This is a direct, measurable signal of interviewer persuasion technique working — something MCHI's binary reluctance flags alone can't show.

### Finding — Interview mode has only a modest relationship with difficulty (corrected)
FPAR has two mode-related fields that are easy to conflate: `TELPV` ("how did you collect most of the data for this case") is populated on 94% of **non-completed** waves and essentially 0% of completed ones — it's filled in when a wave fails, describing the attempted mode. `HOW_INTV` is the reverse: populated on 99% of **completed** waves, describing how the successful interview was actually conducted. An earlier draft of this finding compared completion rates using `TELPV`, which is close to circular — "had a phone-attempted wave" is nearly synonymous with "had an additional failed wave," so of course it correlated with lower completion. That comparison has been retracted.

Using `HOW_INTV` (the mode of the wave that actually completed) instead gives a much smaller, more defensible effect:

| Mode of completed interview | Households | Avg HTC Segments | Avg Contact Attempts | Avg Interview Time |
|---|---|---|---|---|
| Personal visit (all/most) | 6,925 | 1.62 | 13.2 | 4,540 sec (~76 min) |
| Phone (all/most) | 12,075 | 1.71 | 15.9 | 4,263 sec (~71 min) |

*Counted one row per household (each household's most recent completed wave), to match how the dashboard aggregates FPAR — not one row per wave, so these totals (19,000) are lower than the 36,270-household population and won't match a wave-level count.*

**What this means:** phone-completed cases carry modestly more HTC segments and take more contact attempts to get there — consistent with phone often being a later-resort channel for harder cases — but the completed interview itself isn't longer or more burdensome; if anything it's slightly shorter. This is a real but small effect, not the dramatic mode-driven completion gap the earlier version of this finding implied.

### Data quality note — a second undocumented outcome code
FPAR's `OUTCOME` field contains code **314** (6,434 occurrences), which does not appear in the CE-PUMD data dictionary. Code 313 — previously undocumented and flagged the same way — has since been confirmed as "Stop Work (Type A Noninterview)" and is now decoded explicitly rather than bucketed as Other/Unknown. Code 314 does not appear in MCHI's `FNLOTCME` at all, so it wasn't visible until FPAR was cleaned, and remains unresolved; it's labeled explicitly as "Other/Unknown (undocumented code 314)" so it can be filtered or investigated separately. Clarification from BLS or an updated dictionary would help confirm what it represents.

---

## Limitations

**HTC indicators are interviewer-recorded observations, not verified facts**
All MCHI indicators used in this analysis are logged by the interviewer during or after each contact attempt. They reflect the interviewer's observations and judgments — not independently verified characteristics of the household. For example, a flag for privacy concerns (RSPDNT07) means the interviewer recorded that concern; it does not confirm what the household's actual reasons for non-participation were.

**HTC segment flags are binary and do not capture intensity**
Each household receives a 0 or 1 flag per HTC segment, indicating only whether any corresponding indicator appeared across all contact attempts. The flags do not capture how many times an indicator appeared, how strongly it was expressed, or how early in the contact process it occurred.

**No geographic identifiers**
The processed dataset does not include geographic variables such as state, county, or census tract. Findings describe patterns across the full CE sample and cannot be mapped to specific locations or regions without additional data linkage.


---

## Missing Data & Data Quality Notes

**Outcome code 313 resolved — "Stop Work (Type A Noninterview)"**
Outcome code 313 appears 38,362 times in the raw data across 3,063 households, and was previously undocumented in the CE-PUMD data dictionary. It has since been confirmed as "Stop Work (Type A Noninterview)" and is now decoded explicitly in `clean_mchi.py`/`clean_fpar.py` rather than falling into "Other/Unknown." 1,625 households have this as their final recorded outcome.

**Second undocumented outcome code (314) found in FPAR — 6,434 occurrences, still unresolved**
FPAR's `OUTCOME` field contains code 314, which is also missing from the CE-PUMD data dictionary. This is distinct from code 313 above — 314 does not appear anywhere in MCHI's `FNLOTCME`, so it wasn't visible until FPAR was cleaned. It's labeled explicitly (not silently bucketed as generic "Other/Unknown") in `fpar_clean.csv` so it can be filtered or investigated separately.

**Aggregation bug fixed — final outcome label was mismatched with final outcome code for ~6,440 households**
`clean_mchi.py` previously derived each household's final-outcome label by aggregating a pre-mapped, pre-`fillna`'d label column with `"last"`. Pandas' `"last"` skips nulls per column independently, so a household whose truly-last contact attempt had a blank `FNLOTCME` would get its label from that blank row's `fillna`'d "Other/Unknown" — even though `final_outcome_code` correctly reported the real last code from an earlier attempt. This silently mislabeled roughly 6,440 households as "Other/Unknown" that actually had a documented final outcome. The fix now derives `final_outcome` from the (already-correct) `final_outcome_code` after aggregation, rather than aggregating a separate label column.

**Households with unclassified final outcomes: 11, not 4.5%**
With the aggregation bug fixed and code 313 resolved, only 11 households (0.03%) remain in the "Other/Unknown" final outcome category — split across codes 225, 226, 332, and 233, each appearing in only 2–3 households and likely representing data entry artifacts. These households are included in HTC segment counts but their interview completion status is ambiguous.

**Q1 2023 is disproportionately large**
Quarter 20231 (Q1 2023) contains 11,302 households — approximately 3.5 times the size of every other quarter (~3,100 each). This appears to reflect the panel's enrollment baseline rather than a data error, but it means aggregate statistics are influenced by Q1 2023 households more heavily than any other period.

**Extreme outliers in contact attempts**
The maximum number of contact attempts for a single household is 108, against a mean of 14.4 and a median of 13. A small number of households account for a disproportionate share of total interviewer effort and may influence averages in segment-level comparisons.

---

## References

- Bureau of Labor Statistics. *Consumer Expenditure Survey Public Use Microdata.* [https://www.bls.gov/cex/pumd_doc.htm](https://www.bls.gov/cex/pumd_doc.htm)
- Counting Every Voice: Understanding Hard-to-Count and Historically Undercounted Populations
