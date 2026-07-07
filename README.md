# Hard-to-Count Population Dashboard

A dashboard to identify and describe communities with characteristics associated with hard-to-count populations, built using Consumer Expenditure Survey (CE) paradata from the Bureau of Labor Statistics.

---

## Project Overview

"Hard to Count" (HTC) populations are groups with characteristics that make accurate counting more difficult in the census or surveys. The Census Bureau organizes these characteristics into four conceptual segments of the HTC framework:

- **Hard to Interview** — situations where language or communication factors make it difficult to conduct the interview itself
- **Hard to Locate** — situations where a household's physical location is difficult to confirm (address issues, household moved, unit uncertainty)
- **Hard to Persuade** — situations where households express concerns about data privacy, government data collection, or survey participation
- **Hard to Contact** — situations where the household's location is known but the interviewer was unable to reach or connect with anyone there (gated access, repeated no-contact visits, scheduling constraints)

**Important distinction:** These HTC framework segments are *conceptual categories* from the Census literature. The MCHI dataset does not measure them directly — instead, it contains interviewer-recorded indicators that *correspond to* certain segments of the HTC framework. This project maps those MCHI-derived indicators to the appropriate HTC framework segment. The indicators should not be treated as equivalent to the framework categories themselves.

This project uses CE paradata — data about *how* the survey was conducted — to identify patterns in contact difficulty that correspond to HTC populations. The goal is a dashboard that helps planners and outreach staff understand where these characteristics concentrate and what factors drive them.

---

## Data Sources

**Consumer Expenditure Survey Public Use Microdata (CE-PUMD)**
Bureau of Labor Statistics — [https://www.bls.gov/cex/pumd_doc.htm](https://www.bls.gov/cex/pumd_doc.htm)

| File | Description |
|---|---|
| `mchi2324.csv` | Mode and Contact History Interview paradata, 2023–2024. One row per contact attempt (~522K rows, ~36K households). Primary data source. |
| `fpar2324.csv` | Final Paradata, 2023–2024. One row per completed or attempted interview (~102K rows). Records interview timing and section completion. |
| `ce-pumd-interview-diary-dictionary.xlsx` | Official data dictionary for all CE-PUMD variables and coded values. |

> **Note:** Raw data files are not included in this repository. Download them directly from the BLS CE-PUMD page linked above.

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
| **Hard to Locate** | Address instability | `NCTPER08` | Address does not exist or interviewer was unable to locate it |
| **Hard to Locate** | Address instability | `FNLOTCME=341` | Final outcome: household moved during survey period |
| **Hard to Persuade** | Privacy / participation concerns | `RSPDNT07` | Interviewer recorded: respondent cited privacy concerns |
| **Hard to Persuade** | Privacy / participation concerns | `RSPDNT08` | Interviewer recorded: respondent cited concerns about government data collection |
| **Hard to Persuade** | Privacy / participation concerns | `RSPDNT11` | Interviewer recorded: contact was ended abruptly by respondent |
| **Hard to Persuade** | Privacy / participation concerns | `RSPDNT12` | Interviewer recorded: respondent expressed strong objection to continued contact |
| **Hard to Persuade** | Privacy / participation concerns | `NONINTR3` | Interviewer recorded: respondent indicated hesitation to participate |
| **Hard to Persuade** | Privacy / participation concerns | `FNLOTCME=321` | Final outcome: interview not completed due to respondent non-participation |
| **Hard to Contact** | Entry blocked | `NCTPER07` | Unable to reach household — locked gate or buzzer-entry building |
| **Hard to Contact** | No one home | `NCTPER01` | No one home on personal visit |
| **Hard to Contact** | Access via management | `NCTPER11` | Interviewer had to go through building management or doorman |
| **Hard to Contact** | Scheduling / availability | `NONINTR2` | Contact attempt failed due to inconvenient time |
| **Hard to Contact** | Scheduling / availability | `RSPDNT02` | Respondent said they were too busy |
| **Hard to Contact** | Scheduling / availability | `RSPDNT05` | Scheduling difficulties noted by interviewer |
| **Hard to Contact** | Scheduling / availability | `FNLOTCME=216` | Final outcome: no one home, unable to contact |

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
| Hard to Interview | `NONINTR4`, `LNGUAGE2`, `LNGUAGE4`, `LNGUAGE5`, `LANGLIST`, `FNLOTCME=323` |
| Hard to Locate | `NCTPER08`, `FNLOTCME=341` |
| Hard to Persuade | `RSPDNT07`, `RSPDNT08`, `RSPDNT11`, `RSPDNT12`, `NONINTR3`, `FNLOTCME=321` |
| Hard to Contact | `NCTPER07`, `NCTPER01`, `NCTPER11`, `NONINTR2`, `RSPDNT02`, `RSPDNT05`, `FNLOTCME=216` |

### Step 3 — Analysis
Patterns are analyzed across:
- Interview wave (`INTERI`) — does contact difficulty increase in later waves?
- Quarter (`QYEAR`) — seasonal patterns in contact success
- Language group (`LANGLIST`) — which language communities have the most Hard to Interview indicators
- HTC indicator combinations — which segment indicators co-occur most often

### Step 4 — Dashboard
An interactive dashboard built in Python (Streamlit) displays the HTC indicators and allows users to filter and explore the data.

---

## Project Structure

```
.
├── data/
│   ├── raw/            # Source CSV files (not tracked in git)
│   └── processed/      # Cleaned, aggregated outputs
├── scripts/
│   ├── clean_mchi.py         # Aggregates MCHI to household level, creates HTC indicators
│   └── visualizations.py     # Generates interactive charts from cleaned data
├── dashboard/
│   └── app.py                # Streamlit dashboard (in progress)
├── findings_report.md        # Detailed findings from MCHI analysis
├── README.md
└── .gitignore
```

---

## How to Run

### Install dependencies
```bash
pip install pandas streamlit plotly
```

### Clean and aggregate the data
```bash
python scripts/clean_mchi.py
```

### Generate visualizations
```bash
python scripts/visualizations.py
```

### Launch the dashboard
```bash
streamlit run dashboard/app.py
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
Analysis of the 36,270 households in the MCHI 2023–2024 data shows that Hard to Contact indicators are the most widespread, present in over 9 in 10 households. Hard to Locate indicators are the rarest, reflecting the narrow definition of address instability.

| HTC Framework Segment | Households Flagged | % of Total |
|---|---|---|
| Hard to Contact | 33,362 | 92.0% |
| Hard to Persuade | 15,384 | 42.4% |
| Hard to Interview | 1,365 | 3.8% |
| Hard to Locate | 335 | 0.9% |

### Indicator Clustering
A key focus of this analysis is understanding how HTC indicators **cluster** — whether the same households tend to show indicators from multiple HTC segments simultaneously. This matters because households flagged across multiple segments are associated with significantly more interviewer effort and lower completion rates.

Among the 36,270 households:

| Number of HTC Segments Flagged | Households | % of Total |
|---|---|---|
| 0 (no indicators) | 1,822 | 5.0% |
| 1 segment | 19,260 | 53.1% |
| 2 segments | 14,388 | 39.7% |
| 3 segments | 790 | 2.2% |
| 4 segments | 10 | 0.0% |

**95% of households have at least one HTC indicator.** Nearly 2 in 5 show indicators from two or more segments simultaneously.

### The Compounding Effect
As the number of HTC segments flagged per household increases, interviewer effort rises and completion rates fall:

| Segments Flagged | Households | Avg Contact Attempts | Completion Rate |
|---|---|---|---|
| 0 | 1,822 | 4.4 | 64.5% |
| 1 | 19,260 | 13.4 | 48.3% |
| 2 | 14,388 | 16.7 | 25.3% |
| 3 | 790 | 20.2 | 25.8% |
| 4 | 10 | 21.7 | 20.0% |

The jump from 1 to 2 segments is the critical threshold — completion falls nearly 23 percentage points. Households with indicators from multiple HTC segments show substantially lower completion rates that do not appear to be simply additive.

### Most Common Co-occurring Segment Pairs

| Segment Pair | Households | % of Total |
|---|---|---|
| Hard to Contact + Hard to Persuade | 14,376 | 39.6% |
| Hard to Contact + Hard to Interview | 1,275 | 3.5% |
| Hard to Persuade + Hard to Interview | 688 | 1.9% |
| Hard to Contact + Hard to Locate | 316 | 0.9% |
| Hard to Persuade + Hard to Locate | 145 | 0.4% |
| Hard to Locate + Hard to Interview | 18 | 0.0% |

> *Further findings will be added as analysis continues, including patterns by interview wave, season, and language group.*

---

## Limitations

**HTC indicators are interviewer-recorded observations, not verified facts**
All MCHI indicators used in this analysis are logged by the interviewer during or after each contact attempt. They reflect the interviewer's observations and judgments — not independently verified characteristics of the household. For example, a flag for privacy concerns (RSPDNT07) means the interviewer recorded that concern; it does not confirm what the household's actual reasons for non-participation were.

**HTC segment flags are binary and do not capture intensity**
Each household receives a 0 or 1 flag per HTC segment, indicating only whether any corresponding indicator appeared across all contact attempts. The flags do not capture how many times an indicator appeared, how strongly it was expressed, or how early in the contact process it occurred.

**MCHI indicators are proxies for HTC segments, not direct measures**
The Census HTC framework is a conceptual model. The MCHI dataset does not directly measure HTC segment membership — this analysis maps MCHI-derived indicators to the most appropriate HTC segment based on indicator definitions and manager guidance. The mapping reflects a methodological judgment and may be revised as definitions are refined.

**No geographic identifiers**
The processed dataset does not include geographic variables such as state, county, or census tract. Findings describe patterns across the full CE sample and cannot be mapped to specific locations or regions without additional data linkage.

**Dataset covers CE Interview households only**
This analysis is based solely on Consumer Expenditure Interview Survey households. Findings should not be generalized to the broader U.S. population or to other survey programs without additional validation.

**Wave 5 is absent**
The 2023–2024 MCHI file contains no Wave 5 records. The CE panel runs up to 5 waves, so this dataset does not capture the full panel lifecycle. Households that persist to Wave 5 may represent the most difficult-to-reach cases and their absence may affect estimates of contact effort and completion in later waves.

---

## Missing Data & Data Quality Notes

**Undocumented outcome code 313 — 1,625 households**
Outcome code 313 appears 38,362 times in the raw data across 3,063 households but is not listed in the CE-PUMD data dictionary. These households are currently classified as "Other/Unknown" for final outcome. Based on the pattern of predominantly non-contact attempts, the code may represent a non-eligibility category, but this has not been confirmed. Final interpretation of these cases should await clarification from BLS or an updated data dictionary.

**21.5% of households have unclassified final outcomes**
7,781 households (21.5%) fall into the "Other/Unknown" final outcome category due to outcome codes not present in the data dictionary (primarily code 313). These households are included in HTC segment counts but their interview completion status is uncertain.

**Q1 2023 is disproportionately large**
Quarter 20231 (Q1 2023) contains 11,302 households — approximately 3.5 times the size of every other quarter (~3,100 each). This appears to reflect the panel's enrollment baseline rather than a data error, but it means aggregate statistics are influenced by Q1 2023 households more heavily than any other period.

**872 households show 0 days in field**
These households have a final outcome recorded on the same day as first contact (DYSINFLD = 0). This may represent same-day refusals, immediate non-eligibility determinations, or a data recording artifact. These cases should be reviewed before using days-in-field as an analysis variable.

**Extreme outliers in contact attempts**
The maximum number of contact attempts for a single household is 108, against a mean of 14.4 and a median of 13. A small number of households account for a disproportionate share of total interviewer effort and may influence averages in segment-level comparisons.

---

## References

- Bureau of Labor Statistics. *Consumer Expenditure Survey Public Use Microdata.* [https://www.bls.gov/cex/pumd_doc.htm](https://www.bls.gov/cex/pumd_doc.htm)
- Counting Every Voice: Understanding Hard-to-Count and Historically Undercounted Populations
