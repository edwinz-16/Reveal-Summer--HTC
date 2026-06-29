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
| Hard to Contact | NCTPER07, NONINTR2, RSPDNT02, RSPDNT05 | 25,304 | 69.8% |
| Hard to Persuade | RSPDNT07, RSPDNT08, RSPDNT11, RSPDNT12 | 11,453 | 31.6% |
| Hard to Locate | NCTPER08 | 8,950 | 24.7% |
| Hard to Interview | NONINTR4, LNGUAGE2 | 1,365 | 3.8% |

**What this means:** Hard to Contact is by far the most widespread segment — nearly 7 in 10 households had at least one MCHI indicator for scheduling or access difficulty. Hard to Interview is the rarest at 3.8%, but as shown in Finding 3, it is among the most severe when it comes to completion.

---

## Finding 2 — HTC Segment Clustering

The core question is not just how common each HTC segment is, but how often they appear together in the same household.

| HTC Segments Flagged | Households | % of Total |
|---|---|---|
| 0 — no HTC indicators | 4,811 | 13.3% |
| 1 segment | 18,193 | 50.2% |
| 2 segments | 11,023 | 30.4% |
| 3 segments | 2,139 | 5.9% |
| 4 segments (all) | 104 | 0.3% |

**What this means:** 86.7% of households show indicators for at least one HTC segment. Nearly one in three is flagged for two segments at the same time. The 6.2% of households flagged for three or four segments represent the most resource-intensive cases for interviewers and are the hardest to reach.

### Most Common Co-occurring HTC Segment Pairs

| HTC Segment Pair | Households | % of Total |
|---|---|---|
| Hard to Persuade + Hard to Contact | 8,919 | 24.6% |
| Hard to Locate + Hard to Contact | 8,056 | 22.2% |
| Hard to Persuade + Hard to Locate | 4,060 | 11.2% |
| Hard to Interview + Hard to Contact | 1,004 | 2.8% |
| Hard to Interview + Hard to Locate | 597 | 1.6% |
| Hard to Interview + Hard to Persuade | 581 | 1.6% |

Hard to Persuade and Hard to Contact is the most common combination, present in 1 of every 4 households. This likely reflects a pattern where government-wary respondents use time-related excuses as a repeated deflection — the interviewer logs both scheduling and reluctance indicators across multiple visits.

---

## Finding 3 — The Compounding Effect

As the number of HTC segments flagged per household increases, interviewer effort rises and completion rates fall dramatically.

| HTC Segments Flagged | Avg Contact Attempts | Completion Rate |
|---|---|---|
| 0 | 7.8 | 49.1% |
| 1 | 12.9 | 48.6% |
| 2 | 17.0 | 28.9% |
| 3 | 20.3 | 20.2% |
| 4 | 24.0 | 23.1% |

**What this means:** One HTC segment alone does not significantly reduce completion — households flagged for one segment complete at nearly the same rate (48.6%) as households with no flags (49.1%). The critical threshold is **two segments**, where completion drops nearly 20 percentage points to 28.9%. This is the most actionable finding for outreach planning: identifying households likely to be flagged for two or more HTC segments before the first contact attempt would allow resources to be allocated more effectively.

---

## Finding 4 — Which HTC Segments Are Most Severe

Looking at each HTC segment in isolation, Hard to Locate has the most severe impact on completion.

| HTC Segment | Completion With Segment | Completion Without | Avg Attempts With |
|---|---|---|---|
| Hard to Locate | 11.8% | 48.5% | 16.4 |
| Hard to Persuade | 25.6% | 45.8% | 16.0 |
| Hard to Interview | 30.3% | 39.8% | 18.5 |
| Hard to Contact | 46.2% | 23.8% | 16.1 |

**What this means:**

- **Hard to Locate is the most severe single segment** — only 1 in 9 households with address instability indicators ever completes the interview. This covers households where the address couldn't be verified or the household had moved (NCTPER08).
- **Hard to Persuade** cuts completion nearly in half compared to households without those indicators.
- **Hard to Interview**, while rare, requires the most contact attempts on average (18.5) — likely because interviewers keep trying while searching for a translator.
- **Hard to Contact** appears less severe because it is so widespread — it captures many households that eventually complete after rescheduling, alongside those that never do.

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
Completion is nearly the same for zero-segment and one-segment households (~49%). At two HTC segments it falls to 29%. Outreach resources should be concentrated on households showing indicators for multiple HTC segments early in the contact process.

**2. Hard to Locate is the most severe single HTC segment.**
Only 11.8% of Hard to Locate households ever complete. These households are often physically inaccessible (moved addresses, non-existent addresses per NCTPER08) and may need address verification before any interview is attempted.

**3. Hard to Persuade + Hard to Contact is the most common multi-segment pattern.**
Present in 1 in 4 households, this combination likely represents government-wary households using scheduling as a repeated excuse. Standard follow-up strategies (calling, leaving notes) are probably insufficient for this group — trust-building approaches may be more effective.

**4. Hard to Interview households need the most contact attempts but complete at 30%.**
A 30% completion rate is low but not as low as Hard to Locate. The high attempt count (18.5 average) suggests interviewers are persistent — the challenge is translator availability, not household willingness. Earlier coordination of translation resources could improve completion for this group.

**5. Interviewer effort grows significantly across waves.**
The tripling of contact attempts from Wave 1 to Wave 4 suggests that HTC households are not resolved early — they accumulate and consume increasing resources over the panel period. Early identification of HTC households at Wave 1 would allow more proactive planning before effort escalates.

---

*Analysis based on MCHI 2023–2024 paradata. All figures are at the household (CUID) level.*
*Data source: Bureau of Labor Statistics, Consumer Expenditure Survey Public Use Microdata.*
