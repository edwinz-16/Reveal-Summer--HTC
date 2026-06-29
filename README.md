# Hard-to-Count Population Dashboard

A dashboard to identify and describe communities with characteristics associated with hard-to-count populations, built using Consumer Expenditure Survey (CE) paradata from the Bureau of Labor Statistics.

---

## Project Overview

"Hard to Count" (HTC) populations are groups with characteristics that make accurate counting more difficult in the census or surveys. The Census Bureau organizes these characteristics into four conceptual segments of the HTC framework:

- **Hard to Interview** — language barriers, literacy issues, or other factors that make the interview itself difficult to complete
- **Hard to Locate** — situations where a household's physical location is difficult to confirm (address issues, household moved, unit uncertainty)
- **Hard to Persuade** — reluctance driven by distrust of government, privacy concerns, or hostility toward interviewers
- **Hard to Contact** — situations where the location is known but the interviewer cannot actually reach or engage with anyone there (gated access, repeated no-answers, scheduling challenges)

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
| **Hard to Persuade** | Government distrust | `RSPDNT07` | Respondent expressed privacy concerns |
| **Hard to Persuade** | Government distrust | `RSPDNT08` | Respondent expressed anti-government or local/state/federal concerns |
| **Hard to Persuade** | Government distrust | `RSPDNT11` | Respondent hung up or slammed door on interviewer |
| **Hard to Persuade** | Government distrust | `RSPDNT12` | Respondent was hostile or threatened the interviewer |
| **Hard to Persuade** | Government distrust | `NONINTR3` | Respondent was reluctant to participate |
| **Hard to Persuade** | Government distrust | `FNLOTCME=321` | Final outcome: refused, hostile respondent |
| **Hard to Contact** | Entry blocked | `NCTPER07` | Unable to reach household — locked gate or buzzer-entry building |
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
| Hard to Contact | `NCTPER07`, `NONINTR2`, `RSPDNT02`, `RSPDNT05`, `FNLOTCME=216` |

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
2. Do indicators from multiple HTC segments appear in the same household, suggesting some populations face compounding disadvantages?
3. Which HTC segment indicators are associated with the highest interviewer effort (contact attempts, days in field), and what outreach strategies were used in response?

---

## Key Findings

### HTC Indicator Prevalence
Analysis of the 36,270 households in the MCHI 2023–2024 data shows that Hard to Contact indicators are by far the most widespread, while Hard to Interview indicators are the rarest but likely the most severe to resolve.

| HTC Framework Segment | Households Flagged | % of Total |
|---|---|---|
| Hard to Contact | 25,304 | 69.8% |
| Hard to Persuade | 11,453 | 31.6% |
| Hard to Locate | 8,950 | 24.7% |
| Hard to Interview | 1,365 | 3.8% |

### Indicator Clustering
A key focus of this analysis is understanding how HTC indicators **cluster** — whether the same households tend to show characteristics from multiple HTC segments simultaneously. This matters because households flagged across multiple segments require significantly more interviewer effort and are far less likely to complete.

Among the 36,270 households:

| Number of HTC Segments Flagged | Households | % of Total |
|---|---|---|
| 0 (no indicators) | 4,811 | 13.3% |
| 1 segment | 18,193 | 50.2% |
| 2 segments | 11,023 | 30.4% |
| 3 segments | 2,139 | 5.9% |
| 4 segments | 104 | 0.3% |

**86.7% of households have at least one HTC indicator.** Nearly one in three shows indicators from two or more segments simultaneously.

### The Compounding Effect
As the number of HTC segments flagged per household increases, interviewer effort rises and completion rates fall:

| Segments Flagged | Avg Contact Attempts | Completion Rate |
|---|---|---|
| 0 | 7.8 | 49.1% |
| 1 | 12.9 | 48.6% |
| 2 | 17.0 | 28.9% |
| 3 | 20.3 | 20.2% |
| 4 | 24.0 | 23.1% |

The jump from 1 to 2 segments is the critical threshold — completion drops nearly 20 percentage points. Households showing indicators from multiple HTC segments are not simply harder to reach additively; they interact in ways that compound the difficulty.

### Most Common Co-occurring Segment Pairs

| Segment Pair | Households | % of Total |
|---|---|---|
| Hard to Persuade + Hard to Contact | 8,919 | 24.6% |
| Hard to Locate + Hard to Contact | 8,056 | 22.2% |
| Hard to Persuade + Hard to Locate | 4,060 | 11.2% |
| Hard to Interview + Hard to Contact | 1,004 | 2.8% |
| Hard to Interview + Hard to Locate | 597 | 1.6% |
| Hard to Interview + Hard to Persuade | 581 | 1.6% |

> *Further findings will be added as analysis continues, including patterns by interview wave, season, and language group.*

---

## References

- Bureau of Labor Statistics. *Consumer Expenditure Survey Public Use Microdata.* [https://www.bls.gov/cex/pumd_doc.htm](https://www.bls.gov/cex/pumd_doc.htm)
- Counting Every Voice: Understanding Hard-to-Count and Historically Undercounted Populations
