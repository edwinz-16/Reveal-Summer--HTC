# MCHI 2023–2024 Findings Report
## Hard-to-Count Population Analysis
**Consumer Expenditure Survey Paradata | Bureau of Labor Statistics**

---

## Executive Summary

Analysis of the 2023–2024 Mode and Contact History Interview (MCHI) paradata reveals that the vast majority of households surveyed by the CE Interview program show indicators corresponding to at least one Census Hard-to-Count (HTC) framework segment — 95.5% show at least one, and nearly two-thirds (62.5%) show indicators for two or more HTC segments simultaneously.

The single most important finding is the **compounding effect** — but the steepest drop happens earlier than segment count alone suggests: completion falls from 70.2% (no indicators) to 44.1% (one indicator), a 26-point drop, which is the largest single-step fall in the data. Completion keeps declining with each additional segment, down to 21.4% at four, but a single HTC indicator already marks a substantially harder household. This suggests HTC risk should be flagged as soon as the first indicator appears, not held until multiple indicators stack.

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
| Hard to Persuade | RSPDNT07, RSPDNT08, RSPDNT11, RSPDNT12, NONINTR3, NONINTR2, RSPDNT02, RSPDNT05, FNLOTCME=321/322 | 28,720 | 79.2% |
| Hard to Contact | NCTPER07, NCTPER01, NCTPER04, NCTPER11, FNLOTCME=216 | 28,092 | 77.5% |
| Hard to Interview | NONINTR4, LNGUAGE2, LNGUAGE4, LNGUAGE5, LANGLIST, FNLOTCME=323 | 1,365 | 3.8% |
| Hard to Locate | NCTPER08, FNLOTCME=341 | 335 | 0.9% |

**What this means:** Hard to Persuade and Hard to Contact are both extremely widespread — 79.2% and 77.5% of households respectively — reflecting that reluctance once contact is made (Hard to Persuade) and scheduling/access friction (Hard to Contact) are the dominant challenges, not rare edge cases. Hard to Locate is the rarest at 0.9% because it is defined narrowly: only households where the physical address could not be found or the household had moved. Because these two large segments overlap heavily (see Finding 2), most households show indicators for both, not just one.

---

## Finding 2 — HTC Segment Clustering

The core question is not just how common each HTC segment is, but how often they appear together in the same household.

| HTC Segments Flagged | Households | % of Total |
|---|---|---|
| 0 — no HTC indicators | 1,628 | 4.5% |
| 1 segment | 11,935 | 32.9% |
| 2 segments | 21,558 | 59.4% |
| 3 segments | 1,135 | 3.1% |
| 4 segments (all) | 14 | 0.0% |

**What this means:** 95.5% of households show indicators for at least one HTC segment. Nearly 3 in 5 (59.4%) are flagged for exactly two segments at the same time — and 62.5% for two or more. Multi-segment households are the norm, not the exception. Households flagged for three or four segments are rarer but represent the most resource-intensive cases for interviewers.

### Most Common Co-occurring HTC Segment Pairs

| HTC Segment Pair | Households | % of Total |
|---|---|---|
| Hard to Contact + Hard to Persuade | 22,244 | 61.3% |
| Hard to Contact + Hard to Interview | 1,144 | 3.2% |
| Hard to Persuade + Hard to Interview | 1,104 | 3.0% |
| Hard to Contact + Hard to Locate | 289 | 0.8% |
| Hard to Persuade + Hard to Locate | 248 | 0.7% |
| Hard to Locate + Hard to Interview | 18 | 0.0% |

Hard to Contact and Hard to Persuade is the most common combination by a wide margin, present in 61.3% of all households — nearly 2 in 3. Because both segments are individually very common (79.2% and 77.5% of households), heavy overlap between them is expected; this pairing dominates because most households show indicators for both, not because it reflects an unusually correlated subgroup.

---

## Finding 3 — The Compounding Effect

As the number of HTC segments flagged per household increases, interviewer effort rises and completion rates fall dramatically.

| HTC Segments Flagged | Households | Avg Contact Attempts | Completion Rate |
|---|---|---|---|
| 0 | 1,628 | 4.2 | 70.2% |
| 1 | 11,935 | 10.3 | 44.1% |
| 2 | 21,558 | 17.1 | 35.0% |
| 3 | 1,135 | 20.6 | 30.8% |
| 4 | 14 | 23.0 | 21.4% |

**What this means:** The steepest drop happens between **zero and one segment**, where completion falls from 70.2% to 44.1% — a 26.1 percentage point fall, larger than any later transition. This is the most actionable finding for outreach planning: a single HTC indicator already signals substantially higher non-completion risk, so the priority is catching households at the first indicator rather than waiting for multiple segments to accumulate. Completion continues to decline with each additional segment, but at a slower rate.

---

## Finding 4 — Which HTC Segments Are Most Severe

Looking at each HTC segment in isolation, Hard to Contact has the most severe impact on completion.

| HTC Segment | Completion With Segment | Completion Without | Avg Attempts With |
|---|---|---|---|
| Hard to Contact | 31.8% | 65.9% | 16.1 |
| Hard to Locate | 26.0% | 39.6% | 17.7 |
| Hard to Interview | 30.3% | 39.8% | 18.5 |
| Hard to Persuade | 41.8% | 30.6% | 15.6 |

**What this means:**

- **Hard to Contact is the most severe segment by a wide margin** — households with access/no-contact indicators complete at only 31.8%, compared to 65.9% for households without those flags, a 34-point gap. Simply never being reached is the single biggest driver of non-completion.
- **Hard to Locate**, while rare (0.9% of households), still cuts completion significantly — only 26.0% of households where the address could not be found ever complete, versus 39.6% for others.
- **Hard to Interview** requires the most contact attempts on average (18.5) — likely because interviewers keep trying while searching for a translator — and still completes at only 30.3%, versus 39.8% without.
- **Hard to Persuade households complete *more* often than households without any Persuade indicator** (41.8% vs. 30.6%). This is a definitional artifact, not evidence that reluctance helps completion: Hard to Persuade now covers 79.2% of all households (including scheduling-related indicators), so the small remaining "without Persuade" group is disproportionately households that were never contacted at all — not a comparable baseline. Read this row as a caution about interpreting "without a segment" as a clean control group when that segment covers most of the population, not as a finding that persuasion resistance is harmless.

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

**Seasonality (by calendar quarter):** unlike wave, calendar quarter shows no meaningful pattern at all.

| Quarter | Households | Completion Rate |
|---|---|---|
| 2023 Q1 | 11,302 | 40.2% |
| 2023 Q2 | 3,155 | 39.5% |
| 2023 Q3 | 3,143 | 38.6% |
| 2023 Q4 | 3,173 | 37.6% |
| 2024 Q1 | 3,078 | 38.0% |
| 2024 Q2 | 3,079 | 37.9% |
| 2024 Q3 | 3,094 | 39.3% |
| 2024 Q4 | 3,179 | 41.9% |
| 2025 Q1 | 3,067 | 40.3% |

Completion ranges narrowly from 37.6% to 41.9% across all 9 quarters on hand, with no rising or falling trend — households aren't meaningfully easier or harder to reach in any particular season. This closes the "patterns by season" item that had been an open to-do since the first check-in deck.

---

## Finding 7 — FMLI: Who and Where HTC Concentrates

MCHI has no geographic or demographic variables on its own. Linking to FMLI (household income/demographics, combined across 12 available quarters, 2022 Q2–2025 Q1) lets us describe *who* and *where* — for the 20,396 households (56.2% of MCHI) with a matching record. This is close to the practical ceiling: FMLI can only ever contain households that completed at least one interview wave, and only 55 of the 19,177 MCHI households with an ever-completed wave are still unmatched. **This subset skews toward completed interviews (70.1% vs. 39.5% baseline)**, so treat these as directional, not population-representative.

| Breakdown | Group | Households | Completion Rate | Avg HTC Segments |
|---|---|---|---|---|
| Tenure | Rented | 7,005 | 68.6% | 1.63 |
| | Owned w/ mortgage | 7,406 | 69.1% | 1.61 |
| | Owned w/o mortgage | 5,641 | 73.5% | 1.51 |
| Age of reference person | ≤34 | 3,950 | 65.4% | 1.62 |
| | 35–49 | 5,020 | 67.6% | 1.67 |
| | 50–64 | 5,237 | 69.8% | 1.61 |
| | 65+ | 6,189 | 75.2% | 1.48 |
| Urban/Rural | Rural | 1,200 | 71.7% | 1.42 |
| | Urban | 19,196 | 70.0% | 1.60 |

**What this means:** Renters and reference persons under 35 consistently show more HTC segments and lower completion than homeowners and older reference persons. Region and income quartile show only modest differences, not enough on their own to justify a geography-first outreach strategy. Urban/rural has flipped direction on this larger sample (rural now completes slightly better, 71.7% vs. 70.0%) but the gap remains small — treat it as noise, not a signal, unless it holds up with further data. The clearest, most consistent signal is tenure and age, not location.

**Why age matters — it's Hard to Contact, not Hard to Persuade:**

| HTC Segment | ≤34 (n=3,950) | 65+ (n=6,189) | Gap |
|---|---|---|---|
| Hard to Persuade | 83.3% | 83.0% | +0.3 pts |
| Hard to Contact | 74.7% | 62.4% | **+12.3 pts** |
| Hard to Interview | 3.7% | 2.1% | +1.6 pts |
| Hard to Locate | 0.6% | 0.7% | -0.1 pts |

Younger households aren't harder to persuade once reached — that rate is nearly identical across age. The whole gap is Hard to Contact: younger reference persons are simply harder to physically catch at home.

**Caveat — age and tenure are confounded:** 63.2% of ≤34 households rent vs. 21.6% of 65+ households (52.2% of whom own outright). Because age and tenure move together this strongly, "renters are harder" and "under-35s are harder" are likely **the same underlying signal** — residential/schedule stability — not two independent findings. Don't cite both as separate reasons in the same argument.

---

## Finding 8 — FPAR: What Happens After Refusal, and Interview Mode as a Warning Sign

FPAR adds wave-level detail MCHI's contact log can't: whether a refusal was later reversed, and how the interview that succeeded was actually conducted. Unlike FMLI, FPAR covers 99.9% of MCHI households, so these findings describe the real population.

| Metric | Group | Households | Completion Rate |
|---|---|---|---|
| Converted refusal (any wave) | Yes | 5,284 | 74.4% |
| | No | 30,986 | 33.5% |
| Hard-to-Persuade households only | Converted | 4,832 | 73.7% |
| | Never converted | 23,888 | 35.4% |

**What this means:**
- **Refusal conversion works, but is rare.** Only 16.8% of Hard-to-Persuade households were ever successfully talked out of a refusal — doing so nearly doubled their completion rate (35.4% → 73.7%). This is the clearest evidence in the data that interviewer follow-up technique, not just persistence, changes outcomes.

**Correction — interview mode has a real but modest relationship with difficulty, not the large one first reported.** FPAR has two mode fields that are easy to conflate: `TELPV` is populated on 94% of *non-completed* waves (it records the attempted mode when a wave fails) and essentially 0% of completed ones; `HOW_INTV` is the reverse — populated on 99% of *completed* waves. An earlier version of this finding used `TELPV` to claim phone-collected households complete far less often (11.2% vs. 51.8%) — that comparison is close to circular, since "had a phone-attempted wave" is nearly synonymous with "had an additional failed wave." It has been retracted.

Using `HOW_INTV` (the mode of the wave that actually completed) instead:

| Mode of completed interview | Households | Avg HTC Segments | Avg Contact Attempts | Avg Interview Time |
|---|---|---|---|---|
| Personal visit (all/most) | 16,204 | 1.57 | 13.9 | 4,603 sec (~77 min) |
| Phone (all/most) | 25,443 | 1.65 | 16.7 | 4,242 sec (~71 min) |

Phone-completed cases carry modestly more segments and take more attempts to reach — consistent with phone often being a later-resort channel — but the completed interview itself isn't longer or more burdensome. Real effect, much smaller than first reported.

---

## Most Important Findings for Outreach Planning

Ranked by relevance to planning and resource allocation:

**1. A single HTC indicator is already the critical cutoff.**
Completion drops from 70.2% (no indicators) to 44.1% (one indicator) — a 26.1 percentage point fall, the steepest of any transition in the data. Outreach resources should treat the first HTC indicator as a risk signal, not wait for multiple indicators to accumulate before flagging a household.

**2. Hard to Contact is the most severe single HTC segment.**
Only 31.8% of Hard to Contact households complete, compared to 65.9% for households without those indicators — a 34-point gap, the largest of any single segment. Simply being unreachable is the single biggest obstacle to completion.

**3. Hard to Contact + Hard to Persuade is by far the most common multi-segment pattern.**
Present in 61.3% of all households — nearly 2 in 3 — this combination reflects that most flagged households face both access friction and reluctance simultaneously, not one or the other. Standard follow-up strategies likely need to address both dimensions at once, not just increase contact volume.

**4. Hard to Interview households need the most contact attempts but complete at 30%.**
The high attempt count (18.5 average) suggests interviewers are persistent — the challenge is translator availability, not household willingness. Earlier coordination of translation resources could improve completion for this group.

**5. Interviewer effort grows significantly across waves.**
The tripling of contact attempts from Wave 1 to Wave 4 suggests that HTC households are not resolved early — they accumulate and consume increasing resources over the panel period. Early identification of HTC households at Wave 1 would allow more proactive planning before effort escalates.

**6. Refusal conversion is rare but nearly doubles completion — worth formalizing as a technique (FPAR).**
Only 16.8% of Hard-to-Persuade households were ever converted from refusal to completion, but conversion took completion from 35.4% to 73.7%. Whatever interviewers are doing in these cases works; it's worth identifying what distinguishes a successful conversion attempt and building it into standard training rather than leaving it to individual interviewer skill.

**7. Interview mode has only a modest relationship with difficulty (FPAR).**
Among completed interviews, phone-completed cases carry somewhat more HTC segments (1.65 vs. 1.57) and take more contact attempts (16.7 vs. 13.9) than personal-visit-completed cases, consistent with phone often being a later-resort channel for harder cases — but the completed interview itself isn't longer or more burdensome. This is a real but modest effect; an earlier draft of this finding overstated it using a mismeasured variable (see Finding 8).

**8. Renters and younger households are consistently harder to complete, though on a smaller/skewed sample (FMLI).**
Across tenure and age, the same pattern holds: renters and reference persons under 35 show more HTC segments and lower completion than owners and older reference persons. Geography (region, urban/rural) shows only a weak signal by comparison — demographic targeting looks more promising than geographic targeting based on what's available so far.

---

---

## Data Quality Notes

**Outcome code 313 resolved — "Stop Work (Type A Noninterview)"**
Outcome code 313, previously undocumented, has been confirmed as "Stop Work (Type A Noninterview)." It is now decoded explicitly in `clean_mchi.py`/`clean_fpar.py` rather than falling into "Other/Unknown." 1,625 households have this as their final recorded outcome.

**A second undocumented outcome code (314) — found via FPAR**
FPAR's `OUTCOME` field contains code 314 (6,434 occurrences), still missing from the data dictionary. This is a separate code from 313 — it doesn't appear anywhere in MCHI's `FNLOTCME` field, so it wasn't visible until FPAR was cleaned. Recommendation stands: confirm with BLS before treating these as any specific outcome type.

**Aggregation bug fixed — final outcome label was mismatched with final outcome code for ~6,440 households**
`clean_mchi.py` previously computed each household's final-outcome label by aggregating a pre-mapped, pre-`fillna`'d label column with `"last"`. Because pandas' `"last"` skips nulls independently per column, a household whose truly-last contact attempt had a blank `FNLOTCME` would have its label drawn from that blank row's `fillna`'d "Other/Unknown" — even though `final_outcome_code` correctly reported the real last code from an earlier attempt. This silently mislabeled ~6,440 households as "Other/Unknown" that, in fact, had a documented final outcome. The fix derives `final_outcome` from the already-correct `final_outcome_code` after aggregation instead of aggregating a separate label column.

**Households with unclassified final outcomes: 11, not 4.5%**
With the aggregation bug fixed and code 313 resolved, only 11 households (0.03%) remain in "Other/Unknown" for final outcome — split across codes 225, 226, 332, and 233, each appearing in only 2–3 households and likely representing data entry artifacts. These households are included in HTC segment counts but their completion status is ambiguous.

**Wave 5 is absent from the dataset**
The CE panel runs up to 5 interview waves, but no Wave 5 records appear in this data. This is likely expected — the 2023–2024 file was probably cut before Wave 5 households completed their panel — but it means the dataset does not capture the full longitudinal arc of the hardest-to-reach households, who tend to persist into later waves.

**Q1 2023 is disproportionately large**
Quarter 20231 (Q1 2023) contains 11,302 households — roughly 3.5x the size of every other quarter (~3,100 each). This appears to reflect the panel's enrollment baseline rather than a data error. Aggregate statistics are influenced by this imbalance and should be interpreted with that in mind.

**872 households show 0 days in field**
These households had a final outcome recorded on day 0. This may represent same-day refusals or a data entry artifact and should be reviewed before using days-in-field as an analysis variable.

---

*Analysis based on MCHI 2023–2024 paradata. All figures are at the household (CUID) level.*
*Data source: Bureau of Labor Statistics, Consumer Expenditure Survey Public Use Microdata.*
