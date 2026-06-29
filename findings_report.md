# MCHI 2023–2024 Findings Report
## Hard-to-Count Population Analysis
**Consumer Expenditure Survey Paradata | Bureau of Labor Statistics**

---

## Executive Summary

Analysis of the 2023–2024 Mode and Contact History Interview (MCHI) paradata reveals that the majority of households surveyed by the CE Interview program show indicators corresponding to at least one Census Hard-to-Count (HTC) framework segment. More critically, nearly one in three households shows indicators for two or more HTC segments simultaneously — and when segments stack, completion rates drop sharply while interviewer effort climbs.

The single most important finding is the **compounding effect**: a household flagged for one HTC segment completes at roughly the same rate as a household with no HTC flags. But a household flagged for two segments completes at less than half that rate. This suggests that multi-segment households, not single-segment households, are the primary challenge for survey outreach planning.

---

## Data Overview

| Metric | Value |
|---|---|
| Total households analyzed | 36,270 |
| Total contact attempt records | 522,313 |
| Average contact attempts per household | 14.4 |
| Average days in field per household | 21.4 |
| Overall completion rate | 39.5% (14,313 households) |
| Households that never completed | 60.5% (21,957 households) |

The MCHI file records every contact attempt an interviewer makes with a household — not just the final outcome. Each row is one attempt, which is why 522,313 rows collapse to 36,270 unique households. All analysis here is at the household level.

---

## Finding 1 — HTC Segment Prevalence

Households were classified into four Census HTC framework segments using MCHI-derived indicators:

| HTC Segment | MCHI Indicators Used | Households Flagged | % of Total |
|---|---|---|---|
| Hard to Contact | NCTPER07, NONINTR2, RSPDNT02, RSPDNT05 | 28,425 | 78.4% |
| Hard to Persuade | RSPDNT07, RSPDNT08, RSPDNT11, RSPDNT12 | 15,384 | 42.4% |
| Hard to Interview | NONINTR4, LNGUAGE2 | 1,365 | 3.8% |
| Hard to Locate | NCTPER08 | 335 | 0.9% |

**What this means:** Hard to Contact is overwhelmingly the most widespread segment — more than 3 in 4 households had at least one MCHI indicator for scheduling or access difficulty. Hard to Locate is the rarest at 0.9% because it is defined narrowly: only households where the physical address could not be found or the household had moved (NCTPER08). Hard to Persuade, at 42.4%, is the segment with the most severe impact on completion rates.

---

## Finding 2 — HTC Segment Clustering

The core question is not just how common each HTC segment is, but how often they appear together in the same household.

| HTC Segments Flagged | Households | % of Total |
|---|---|---|
| 0 — no HTC indicators | 4,549 | 12.5% |
| 1 segment | 18,643 | 51.4% |
| 2 segments | 12,378 | 34.1% |
| 3 segments | 690 | 1.9% |
| 4 segments (all) | 10 | 0.0% |

**What this means:** 87.5% of households show indicators for at least one HTC segment. More than one in three is flagged for two segments at the same time. Households flagged for three or four segments are rare but represent the most resource-intensive cases for interviewers.

### Most Common Co-occurring HTC Segment Pairs

| HTC Segment Pair | Households | % of Total |
|---|---|---|
| Hard to Contact + Hard to Persuade | 12,321 | 34.0% |
| Hard to Contact + Hard to Interview | 1,060 | 2.9% |
| Hard to Persuade + Hard to Interview | 688 | 1.9% |
| Hard to Contact + Hard to Locate | 276 | 0.8% |
| Hard to Persuade + Hard to Locate | 145 | 0.4% |
| Hard to Locate + Hard to Interview | 18 | 0.0% |

Hard to Contact and Hard to Persuade is the most common combination by a large margin, present in 1 in 3 households. This likely reflects a pattern where government-wary respondents use time-related excuses as a repeated deflection — the interviewer logs both scheduling and reluctance indicators across multiple visits.

---

## Finding 3 — The Compounding Effect

As the number of HTC segments flagged per household increases, interviewer effort rises and completion rates fall dramatically.

| HTC Segments Flagged | Households | Avg Contact Attempts | Completion Rate |
|---|---|---|---|
| 0 | 4,549 | 8.5 | 47.1% |
| 1 | 18,643 | 13.7 | 45.9% |
| 2 | 12,378 | 17.3 | 27.7% |
| 3 | 690 | 20.8 | 27.1% |
| 4 | 10 | 21.7 | 20.0% |

**What this means:** One HTC segment alone does not significantly reduce completion — households flagged for one segment complete at nearly the same rate (45.9%) as households with no flags (47.1%). The critical threshold is **two segments**, where completion drops nearly 18 percentage points to 27.7%. This is the most actionable finding for outreach planning: identifying households likely to be flagged for two or more HTC segments before the first contact attempt would allow resources to be allocated more effectively.

---

## Finding 4 — Which HTC Segments Are Most Severe

Looking at each HTC segment in isolation, Hard to Locate has the most severe impact on completion.

| HTC Segment | Completion With Segment | Completion Without | Avg Attempts With |
|---|---|---|---|
| Hard to Persuade | 24.4% | 50.6% | 16.1 |
| Hard to Locate | 26.0% | 39.6% | 17.7 |
| Hard to Interview | 30.3% | 39.8% | 18.5 |
| Hard to Contact | 41.2% | 33.0% | 15.7 |

**What this means:**

- **Hard to Persuade is the most severe segment** — households with distrust or hostility indicators complete at only 24.4%, compared to 50.6% for households without those flags.
- **Hard to Locate**, while rare (0.9% of households), still cuts completion significantly — only 26% of households where the address could not be found ever complete.
- **Hard to Interview** requires the most contact attempts on average (18.5) — likely because interviewers keep trying while searching for a translator.
- **Hard to Contact** shows a counterintuitive pattern: households with Hard to Contact indicators actually complete at a slightly *higher* rate than those without (41.2% vs 33.0%). This is because Hard to Contact is so widespread (78.4% of households) that the "without" group is a small, unusual subset — not because being Hard to Contact helps completion.

---

## Finding 5 — Hard to Interview: Language Detail

Among the 1,365 households flagged under the Hard to Interview segment, Spanish-speaking households make up the largest group by a significant margin.

| Language | Households |
|---|---|
| Spanish | 833 |
| Other (unspecified) | 89 |
| Chinese | 63 |
| Vietnamese | 42 |
| Russian | 36 |
| Korean | 30 |
| Arabic | 25 |
| Portuguese | 13 |
| Polish | 10 |
| Japanese | 8 |
| Tagalog | 5 |
| French | 5 |
| Italian | 4 |
| Urdu | 1 |

**What this means:** Spanish-speaking households account for 61% of all language-flagged cases. However, the 89 "Other" cases and 11 "Unknown language" cases indicate situations where the interviewer could not even identify the language, which likely represents the most difficult language barrier scenarios.

---

## Finding 6 — Interview Wave Patterns

The CE Interview is a rotating panel — households participate in up to 5 waves (interviews) over time. Contact difficulty increases with each successive wave.

| Wave | Households | Completion Rate | Avg Contact Attempts |
|---|---|---|---|
| 1 | 3,570 | 38.2% | 5.8 |
| 2 | 3,495 | 41.3% | 10.4 |
| 3 | 3,534 | 38.9% | 14.6 |
| 4 | 25,671 | 39.5% | 16.1 |

**What this means:** Contact attempts roughly triple from Wave 1 (5.8) to Wave 4 (16.1), showing that interviewers invest significantly more effort in later waves. Completion rates stay relatively stable across waves (~39–41%), which means interviewers are compensating for growing difficulty with greater effort — not that later waves are easier. Wave 4 contains most households because records accumulate there over the panel period.

---

## Most Important Findings for Outreach Planning

Ranked by relevance to planning and resource allocation:

**1. The two-segment threshold is the critical cutoff.**
Completion is nearly the same for zero-segment and one-segment households (~47% and ~46%). At two HTC segments it falls to 27.7%. Outreach resources should be concentrated on households showing indicators for multiple HTC segments early in the contact process.

**2. Hard to Persuade is the most severe single HTC segment.**
Only 24.4% of Hard to Persuade households complete, compared to 50.6% for households without those indicators. Government distrust and hostility represent the most significant individual barrier to completion.

**3. Hard to Contact + Hard to Persuade is by far the most common multi-segment pattern.**
Present in 1 in 3 households (34%), this combination likely represents government-wary respondents using scheduling as a repeated deflection. Standard follow-up strategies may be insufficient — trust-building approaches may be more effective.

**4. Hard to Interview households need the most contact attempts but complete at 30%.**
The high attempt count (18.5 average) suggests interviewers are persistent — the challenge is translator availability, not household willingness. Earlier coordination of translation resources could improve completion for this group.

**5. Interviewer effort grows significantly across waves.**
The tripling of contact attempts from Wave 1 to Wave 4 suggests that HTC households are not resolved early — they accumulate and consume increasing resources over the panel period. Early identification of HTC households at Wave 1 would allow more proactive planning before effort escalates.

---

---

## Data Quality Notes

**Undocumented outcome code (313) — 1,625 households**
Outcome code 313 appears 1,625 times in the raw data but is not listed in the CE-PUMD data dictionary. These households currently fall into the "Other/Unknown" outcome category. The meaning of this code is unclear and should be confirmed with BLS documentation or a data contact before these cases are excluded or interpreted.

**21.5% of households have unclassified final outcomes**
7,781 households (21.5%) are classified as "Other/Unknown" for final outcome. The bulk of this is driven by code 313 (1,625 cases) alongside a small number of other undocumented codes (225, 226, 233). These households are included in HTC segment counts but their completion status is ambiguous.

**Wave 5 is absent from the dataset**
The CE panel runs up to 5 interview waves, but no Wave 5 records appear in this data. This is likely expected — the 2023–2024 file was probably cut before Wave 5 households completed their panel — but it means the dataset does not capture the full longitudinal arc of the hardest-to-reach households, who tend to persist into later waves.

**Q1 2023 is disproportionately large**
Quarter 20231 (Q1 2023) contains 11,302 households — roughly 3.5x the size of every other quarter (~3,100 each). This appears to reflect the panel's enrollment baseline rather than a data error. Aggregate statistics are influenced by this imbalance and should be interpreted with that in mind.

**872 households show 0 days in field**
These households had a final outcome recorded on day 0. This may represent same-day refusals or a data entry artifact and should be reviewed before using days-in-field as an analysis variable.

---

*Analysis based on MCHI 2023–2024 paradata. All figures are at the household (CUID) level.*
*Data source: Bureau of Labor Statistics, Consumer Expenditure Survey Public Use Microdata.*
