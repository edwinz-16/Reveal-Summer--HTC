# MCHI 2023–2024 Findings Report
## Hard-to-Count Population Analysis
**Consumer Expenditure Survey Paradata | Bureau of Labor Statistics**

---

## Executive Summary

Analysis of the 2023–2024 Mode and Contact History Interview (MCHI) paradata reveals that the majority of households surveyed by the CE Interview program face at least one barrier associated with hard-to-count (HTC) populations. More critically, nearly one in three households faces two or more barriers simultaneously — and when barriers stack, completion rates drop sharply while interviewer effort climbs.

The single most important finding is the **compounding effect**: a household with one barrier completes at roughly the same rate as a household with no barriers. But a household with two barriers completes at less than half that rate. This suggests that multi-barrier households, not single-barrier households, are the primary challenge for survey outreach planning.

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

## Finding 1 — Barrier Prevalence

Four HTC barrier categories were constructed from MCHI interviewer-recorded flags:

| HTC Barrier | Households Flagged | % of Total |
|---|---|---|
| Scheduling / time constraints | 25,304 | 69.8% |
| Government distrust / reluctance | 11,453 | 31.6% |
| Hard to locate / housing instability | 8,950 | 24.7% |
| Language barrier | 1,365 | 3.8% |

**What this means:** Scheduling is by far the most widespread barrier — nearly 7 in 10 households had at least one flag indicating time or scheduling as an obstacle. Language is the rarest barrier at 3.8%, but as shown in Finding 3, it is among the most severe when it comes to completion.

---

## Finding 2 — Barrier Clustering

The core question is not just how common each barrier is, but how often they appear together in the same household.

| Number of Barriers | Households | % of Total |
|---|---|---|
| 0 — no HTC flags | 4,811 | 13.3% |
| 1 barrier | 18,193 | 50.2% |
| 2 barriers | 11,023 | 30.4% |
| 3 barriers | 2,139 | 5.9% |
| 4 barriers (all) | 104 | 0.3% |

**What this means:** 86.7% of households carry at least one HTC barrier. Nearly one in three faces two at the same time. The 6.2% of households with three or four barriers represent the most resource-intensive cases for interviewers and are the hardest to reach.

### Most Common Co-occurring Barrier Pairs

| Barrier Pair | Households | % of Total |
|---|---|---|
| Distrust + Scheduling | 8,919 | 24.6% |
| Hard to locate + Scheduling | 8,056 | 22.2% |
| Distrust + Hard to locate | 4,060 | 11.2% |
| Language + Scheduling | 1,004 | 2.8% |
| Language + Hard to locate | 597 | 1.6% |
| Language + Distrust | 581 | 1.6% |

Distrust and scheduling is the most common combination, present in 1 of every 4 households. This likely reflects a pattern where government-wary respondents use time-related excuses as a repeated deflection — the interviewer logs both a scheduling flag and a reluctance flag across multiple visits.

---

## Finding 3 — The Compounding Effect

As the number of barriers per household increases, interviewer effort rises and completion rates fall dramatically.

| Barriers | Avg Contact Attempts | Completion Rate |
|---|---|---|
| 0 | 7.8 | 49.1% |
| 1 | 12.9 | 48.6% |
| 2 | 17.0 | 28.9% |
| 3 | 20.3 | 20.2% |
| 4 | 24.0 | 23.1% |

**What this means:** One barrier alone does not significantly reduce completion — households with one barrier complete at nearly the same rate (48.6%) as households with none (49.1%). The critical threshold is **two barriers**, where completion drops nearly 20 percentage points to 28.9%. This is the most actionable finding for outreach planning: identifying households likely to carry two or more barriers before the first contact attempt would allow resources to be allocated more effectively.

---

## Finding 4 — Which Individual Barriers Are Most Severe

Looking at each barrier in isolation, hard to locate has the most severe impact on completion — even more than language.

| Barrier | Completion With Barrier | Completion Without | Avg Attempts With |
|---|---|---|---|
| Hard to locate | 11.8% | 48.5% | 16.4 |
| Government distrust | 25.6% | 45.8% | 16.0 |
| Language barrier | 30.3% | 39.8% | 18.5 |
| Scheduling | 46.2% | 23.8% | 16.1 |

**What this means:**

- **Hard to locate is the most severe single barrier** — only 1 in 9 households flagged as hard to locate ever completes the interview. This covers households where the address couldn't be verified, entry was blocked, or the household moved.
- **Government distrust** cuts completion nearly in half compared to households without it.
- **Language barriers**, while rare, require the most contact attempts on average (18.5) — likely because interviewers keep trying while searching for a translator.
- **Scheduling** appears less severe because it is so widespread — it captures many households that eventually complete after rescheduling, alongside those that never do.

---

## Finding 5 — Language Barrier Detail

Among the 1,365 households with a language barrier flag, Spanish-speaking households make up the largest group by a significant margin.

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

**1. The two-barrier threshold is the critical cutoff.**
Completion is nearly the same for zero-barrier and one-barrier households (~49%). At two barriers it falls to 29%. Outreach resources should be concentrated on households showing signs of multiple barriers early in the contact process.

**2. Hard to locate is the most severe single barrier — not language.**
Only 11.8% of hard-to-locate households ever complete. These households are often physically inaccessible (gated communities, moved addresses, non-existent addresses) and may need address verification or alternative contact strategies before any interview is attempted.

**3. Distrust + scheduling is the most common multi-barrier pattern.**
Present in 1 in 4 households, this combination likely represents government-wary households using scheduling as a repeated excuse. Standard follow-up strategies (calling, leaving notes) are probably insufficient for this group — trust-building approaches may be more effective.

**4. Language households need the most contact attempts but complete at 30%.**
A 30% completion rate is low but not as low as hard-to-locate. The high attempt count (18.5 average) suggests interviewers are persistent — the barrier is translator availability, not household willingness. Earlier coordination of translation resources could improve completion for this group.

**5. Interviewer effort grows significantly across waves.**
The tripling of contact attempts from Wave 1 to Wave 4 suggests that hard-to-count households are not resolved early — they accumulate and consume increasing resources over the panel period. Early identification of HTC households at Wave 1 would allow more proactive planning before effort escalates.

---

*Analysis based on MCHI 2023–2024 paradata. All figures are at the household (CUID) level.*
*Data source: Bureau of Labor Statistics, Consumer Expenditure Survey Public Use Microdata.*
