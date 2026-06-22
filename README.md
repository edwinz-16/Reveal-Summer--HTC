# Hard-to-Count Population Dashboard

A dashboard to identify and describe communities that may face barriers to accurate census and survey participation, built using Consumer Expenditure Survey (CE) paradata from the Bureau of Labor Statistics.

---

## Project Overview

"Hard to Count" (HTC) populations are groups that face barriers in being accurately counted in the census or surveys. These barriers include:

- Language barriers
- Distrust of government or privacy concerns
- Housing instability or difficulty being located
- Scheduling or time-related constraints
- Survey fatigue

This project uses CE paradata — data about *how* the survey was conducted — to identify patterns in contact difficulty that may indicate HTC populations. The goal is a dashboard that helps planners and outreach staff understand where these barriers concentrate and what factors drive them.

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

## Methodology

### Step 1 — Data Aggregation
The MCHI file is structured as one row per **contact attempt**. Because a single household can have many contact attempts, we first aggregate to the **household level** using the `CUID` field (household identifier).

For each household we compute:
- Total number of contact attempts
- Days in the field (`DYSINFLD` max)
- Final interview outcome (`FNLOTCME`)
- Whether any language barrier was flagged (`NONINTR4`, `LANGLIST`, `LNGUAGE2–5`)
- Count of respondent concern flags (`RSPDNT*`)
- Count of non-interview reason flags (`NONINTR*`)

### Step 2 — HTC Indicator Construction
Each household is assigned binary flags for four HTC barrier categories:

| HTC Barrier | Key Variables |
|---|---|
| Language barrier | `NONINTR4`, `LANGLIST`, `LNGUAGE2`, `FNLOTCME=323` |
| Government distrust / reluctance | `RSPDNT07`, `RSPDNT08`, `RSPDNT12`, `FNLOTCME=321` |
| Hard to locate / housing instability | `FNLOTCME=216/341`, `NCTPER07`, `NCTPER08`, high attempt count |
| Time / scheduling barriers | `NONINTR2`, `RSPDNT02`, `RSPDNT03`, `FNLOTCME=322` |

### Step 3 — Analysis
Patterns are analyzed across:
- Interview wave (`INTERI`) — does difficulty increase in later waves?
- Quarter (`QYEAR`) — seasonal patterns in contact success
- Language group (`LANGLIST`) — which language communities face the most barriers
- HTC barrier combinations — which barriers co-occur most often

### Step 4 — Dashboard
An interactive dashboard built in Python (Streamlit) displays the HTC indicators and allows users to filter and explore the data.

---

## Project Structure

```
.
├── data/
│   ├── raw/          # Source CSV files (not tracked in git)
│   └── processed/    # Cleaned, aggregated outputs
├── scripts/
│   └── aggregate_mchi.py   # Aggregates MCHI to household level
├── dashboard/
│   └── app.py              # Streamlit dashboard
├── README.md
└── .gitignore
```

---

## How to Run

### Install dependencies
```bash
pip install pandas streamlit plotly
```

### Aggregate the data
```bash
python scripts/aggregate_mchi.py
```

### Launch the dashboard
```bash
streamlit run dashboard/app.py
```

---

## Research Focus

### Primary Research Question
*What patterns of contact difficulty in the CE Interview survey reflect barriers commonly associated with hard-to-count populations, and do these barriers tend to cluster together within the same households?*

### Sub-questions
1. Which HTC barriers — language, government distrust, housing instability, and scheduling difficulty — are most prevalent among households that did not complete the survey?
2. Do certain barriers co-occur within the same household, suggesting some populations face compounding disadvantages?
3. Which barriers are associated with the highest interviewer effort (contact attempts, days in field), and what outreach strategies were used in response?

---

## Key Findings

### Barrier Prevalence
Analysis of the 36,270 households in the MCHI 2023–2024 data shows that scheduling and time-related barriers are by far the most widespread HTC signal, while language barriers are the rarest but likely the most severe.

| HTC Barrier | Households Flagged | % of Total |
|---|---|---|
| Scheduling / time constraints | 25,233 | 69.6% |
| Hard to locate / housing instability | 12,851 | 35.4% |
| Government distrust / reluctance | 11,821 | 32.6% |
| Language barrier | 1,449 | 4.0% |

### Barrier Clustering
A key focus of this analysis is understanding how barriers **cluster** — meaning whether the same households tend to face multiple barriers simultaneously rather than just one. This matters because compounding barriers likely make households significantly harder to reach than any single barrier alone.

Among the 36,270 households:

| Number of Barriers | Households | % of Total |
|---|---|---|
| 0 (no HTC flags) | 4,168 | 11.5% |
| 1 barrier | 16,626 | 45.8% |
| 2 barriers | 11,889 | 32.8% |
| 3 barriers | 3,398 | 9.4% |
| 4 barriers (all) | 189 | 0.5% |

**88.5% of households carry at least one HTC barrier.** Nearly half face two or more simultaneously.

### The Compounding Effect
The most compelling pattern is how barriers compound. As the number of barriers per household increases, interviewer effort goes up sharply and completion rates drop:

| Barriers | Avg Contact Attempts | Completion Rate |
|---|---|---|
| 0 | 7.8 | 49.1% |
| 1 | 12.9 | 48.6% |
| 2 | 17.0 | 28.9% |
| 3 | 20.3 | 20.2% |
| 4 | 24.0 | 23.1% |

The jump from 1 to 2 barriers is particularly striking — completion falls nearly 20 percentage points and contact attempts increase by a third. This suggests that multiple barriers are not simply additive; they interact in ways that make households significantly harder to reach.

### Most Common Barrier Combinations
Among households with 2 or more barriers, the most frequent co-occurring pairs are:

| Barrier Pair | Households | % of Total |
|---|---|---|
| Distrust + Scheduling | 8,919 | 24.6% |
| Hard to locate + Scheduling | 8,056 | 22.2% |
| Distrust + Hard to locate | 4,060 | 11.2% |
| Language + Scheduling | 1,004 | 2.8% |
| Language + Hard to locate | 597 | 1.6% |
| Language + Distrust | 581 | 1.6% |

Distrust and scheduling is the most common pairing, appearing in 1 in 4 households. This likely reflects a pattern where government-wary respondents use scheduling excuses as a repeated deflection strategy.

> *Further findings will be added as analysis continues, including patterns by interview wave, season, and language group.*

---

## References

- Bureau of Labor Statistics. *Consumer Expenditure Survey Public Use Microdata.* [https://www.bls.gov/cex/pumd_doc.htm](https://www.bls.gov/cex/pumd_doc.htm)
- Counting Every Voice: Understanding Hard-to-Count and Historically Undercounted Populations
