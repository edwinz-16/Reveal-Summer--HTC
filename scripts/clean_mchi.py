"""
clean_mchi.py
-------------
Reads the raw MCHI 2023-2024 paradata file, selects HTC-relevant variables,
aggregates from contact-attempt level to household level, creates HTC barrier
flags, decodes coded values, and saves a clean CSV to data/processed/.

Input:  data/raw/mchi2324.csv
Output: data/processed/mchi_clean.csv
"""

import pandas as pd
import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
RAW_PATH  = os.path.join("data", "raw", "mchi2324.csv")
OUT_PATH  = os.path.join("data", "processed", "mchi_clean.csv")

# ---------------------------------------------------------------------------
# Step 1 — Load raw data
# ---------------------------------------------------------------------------
print("Loading raw MCHI data...")
df = pd.read_csv(RAW_PATH, dtype=str, low_memory=False)
print(f"  Raw shape: {df.shape[0]:,} rows x {df.shape[1]} columns")

# ---------------------------------------------------------------------------
# Step 2 — Select only the columns we need
#
# We drop administrative/technical columns that don't contribute to HTC
# analysis: CNTCKEY (record ordering key), LAUNCH (system flag),
# CHI_TIME (instrument open time), ATMPT1-7 (interviewer admin actions).
# ---------------------------------------------------------------------------
KEEP_COLS = [
    # --- Identifiers ---
    "CUID",         # Household ID (7-digit) — our grouping key
    "NEWID",        # Full record ID
    "QYEAR",        # Year + quarter (e.g. 20231 = Q1 2023)
    "INTERI",       # Interview wave (1–5)

    # --- Contact outcome ---
    "FNLOTCME",     # Final outcome code for the household
    "CTTYPE",       # Was this attempt completed, partial, or unable?
    "CTSTATUS",     # Who was contacted: sample member, non-member, or no contact
    "CNTCTYP",      # Contact method: personal visit, phone (out), phone (in), none

    # --- Contact effort metrics ---
    "DYSINFLD",     # Days since first contact attempt

    # --- Visit timing ---
    "VISIT_MO",     # Month of visit
    "VISIT_YR",     # Year of visit
    "VISIT_HR",     # Hour of visit (0–23)
    "VISTWKDY",     # Day of week (1=Sun … 7=Sat)

    # --- Language barrier signals ---
    "LANGLIST",     # Language spoken by household
    "NONINTR4",     # Language was reason interview couldn't happen
    "LNGUAGE1",     # Specify language
    "LNGUAGE2",     # No household member could translate
    "LNGUAGE3",     # Contacted regional office about language
    "LNGUAGE4",     # Could not find a translator
    "LNGUAGE5",     # Ran out of time to find translator

    # --- Government distrust / reluctance signals ---
    "RSPDNT07",     # Privacy concerns
    "RSPDNT08",     # Anti-government / local/state/federal concerns
    "RSPDNT11",     # Hung up or slammed door on interviewer
    "RSPDNT12",     # Hostile or threatened interviewer
    "RSPDNT06",     # Invoked that survey is voluntary

    # --- Scheduling / time barrier signals ---
    "NONINTR2",     # Inconvenient time
    "RSPDNT02",     # Respondent said too busy
    "RSPDNT03",     # Interview takes too much time
    "RSPDNT05",     # Scheduling difficulties

    # --- Hard to locate / housing instability signals ---
    "NCTPER07",     # Unable to reach — locked gate or buzzer entry
    "NCTPER08",     # Address does not exist or can't be located
    "NCTPER04",     # Someone clearly home but won't answer door
    "NCTPER01",     # No one home on personal visit
    "NCTPER11",     # Had to go through building management / doorman

    # --- General non-interview reasons ---
    "NONINTR1",     # Eligible person not available
    "NONINTR3",     # Respondent is reluctant
    "NONINTR5",     # Health problem
    "NONINTR7",     # Other
    "NONINTR8",     # Other (second catch-all)

    # --- Respondent concern flags (additional context) ---
    "RSPDNT01",     # Not interested / doesn't want to be bothered
    "RSPDNT09",     # Doesn't understand the survey
    "RSPDNT21",     # Intends to quit the survey
    "RSPDNT22",     # No concerns noted

    # --- Telephone non-contact reasons ---
    "NCTTEL1",      # Got answering machine
    "NCTTEL2",      # No answer
    "NCTTEL4",      # Disconnected number

    # --- Outreach strategies used ---
    "STRATG01",     # Advance letter given
    "STRATG02",     # Scheduled an appointment
    "STRATG03",     # Left a note or appointment card
    "STRATG05",     # Called the household
    "STRATG11",     # Staked out / waited for respondent
    "STRATG14",     # Contacted property manager
    "STRATG19",     # Offered an incentive
]

df = df[KEEP_COLS].copy()
print(f"  After column selection: {df.shape[1]} columns kept")

# ---------------------------------------------------------------------------
# Step 3 — Convert numeric columns from string
# ---------------------------------------------------------------------------
NUMERIC_COLS = ["DYSINFLD", "VISIT_HR", "INTERI", "QYEAR"]
for col in NUMERIC_COLS:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Flag columns are '1' or blank — convert to 0/1 integers
FLAG_COLS = [c for c in KEEP_COLS if c not in
             ["CUID","NEWID","QYEAR","INTERI","FNLOTCME","CTTYPE",
              "CTSTATUS","CNTCTYP","DYSINFLD","VISIT_MO","VISIT_YR",
              "VISIT_HR","VISTWKDY","LANGLIST"]]
for col in FLAG_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# ---------------------------------------------------------------------------
# Step 4 — Decode coded values into readable labels
# ---------------------------------------------------------------------------

FNLOTCME_LABELS = {
    "201": "Completed",
    "216": "No one home - unable to contact",
    "217": "Temporarily absent",
    "219": "Other non-interview",
    "321": "Refused - hostile respondent",
    "322": "Refused - time related",
    "323": "Refused - language problem",
    "324": "Refused - other",
    "341": "Household moved",
    "203": "Transmit - no more follow-up possible",
    "215": "Insufficient partial",
    "583": "Salvaged case",
}

LANGLIST_LABELS = {
    "11": "Spanish",
    "12": "Arabic",
    "13": "Chinese",
    "14": "French",
    "15": "German",
    "16": "Greek",
    "17": "Italian",
    "18": "Japanese",
    "19": "Korean",
    "20": "Polish",
    "21": "Portuguese",
    "22": "Russian",
    "23": "Tagalog",
    "24": "Urdu",
    "25": "Vietnamese",
    "97": "Other - hard of hearing",
    "98": "Unknown language",
    "99": "Other",
}

VISTWKDY_LABELS = {
    "1": "Sunday", "2": "Monday", "3": "Tuesday",
    "4": "Wednesday", "5": "Thursday", "6": "Friday", "7": "Saturday",
}

CNTCTYP_LABELS = {
    "1": "Personal visit",
    "2": "Phone - outgoing",
    "3": "Phone - incoming",
    "4": "No contact attempted",
}

df["FNLOTCME_label"] = df["FNLOTCME"].map(FNLOTCME_LABELS).fillna("Other/Unknown")
df["LANGLIST_label"] = df["LANGLIST"].map(LANGLIST_LABELS).fillna("None recorded")
df["VISTWKDY_label"] = df["VISTWKDY"].map(VISTWKDY_LABELS).fillna("Unknown")
df["CNTCTYP_label"] = df["CNTCTYP"].map(CNTCTYP_LABELS).fillna("Unknown")

# ---------------------------------------------------------------------------
# Step 5 — Aggregate from contact-attempt level to household level
#
# Each CUID can have many rows (one per contact attempt). We collapse these
# into one row per household by:
#   - summing flag columns (how many times each flag appeared)
#   - taking the max of DYSINFLD (most days spent in field)
#   - counting total rows (= total contact attempts)
#   - taking the last recorded FNLOTCME (final outcome)
#   - taking the most common LANGLIST value that isn't blank
# ---------------------------------------------------------------------------
print("Aggregating to household level...")

agg_dict = {}

# Sum all flag columns — gives count of how many attempts had each flag
for col in FLAG_COLS:
    if col in df.columns:
        agg_dict[col] = "sum"

# Max days in field
agg_dict["DYSINFLD"] = "max"

# Total contact attempts = number of rows per CUID
df["contact_attempts"] = 1

# Keep QYEAR and INTERI from first record
agg_dict["QYEAR"] = "first"
agg_dict["INTERI"] = "max"  # highest wave reached

# Final outcome: take the last non-empty value recorded
agg_dict["FNLOTCME"] = "last"
agg_dict["FNLOTCME_label"] = "last"

# Language: take first non-null language recorded
def first_language(s):
    non_null = s[s != "None recorded"]
    return non_null.iloc[0] if len(non_null) > 0 else "None recorded"

household = df.groupby("CUID").agg(
    contact_attempts=("contact_attempts", "sum"),
    days_in_field=("DYSINFLD", "max"),
    qyear=("QYEAR", "first"),
    max_wave=("INTERI", "max"),
    final_outcome_code=("FNLOTCME", "last"),
    final_outcome=("FNLOTCME_label", "last"),
    language=("LANGLIST_label", first_language),
    **{col: (col, "sum") for col in FLAG_COLS if col in df.columns},
).reset_index()

print(f"  Aggregated shape: {household.shape[0]:,} households x {household.shape[1]} columns")

# ---------------------------------------------------------------------------
# Step 6 — Create HTC barrier flags
#
# Each household gets a binary flag (0 or 1) for each of the four HTC
# barrier categories. A flag is set to 1 if any contact attempt recorded
# that barrier for this household.
# ---------------------------------------------------------------------------

# --- HTC Segment flags ---
# These correspond to the four Census HTC framework segments.
# Each flag is 1 if any MCHI indicator for that segment appeared
# across any contact attempt for this household.

# Hard to Interview — language barriers that prevent the interview itself
household["htc_hard_to_interview"] = (
    (household["NONINTR4"] > 0) |
    (household["LNGUAGE2"] > 0) |
    (household["LNGUAGE4"] > 0) |
    (household["LNGUAGE5"] > 0) |
    (household["language"] != "None recorded") |
    (household["final_outcome_code"] == "323")
).astype(int)

# Hard to Persuade — contact was made but respondent declined to participate
# Includes privacy/distrust concerns AND scheduling/availability declines
# (scheduling codes go here because the respondent communicated a reason — contact was established)
household["htc_hard_to_persuade"] = (
    (household["RSPDNT07"] > 0) |
    (household["RSPDNT08"] > 0) |
    (household["RSPDNT11"] > 0) |
    (household["RSPDNT12"] > 0) |
    (household["NONINTR3"] > 0) |
    (household["NONINTR2"] > 0) |   # inconvenient time — respondent communicated this
    (household["RSPDNT02"] > 0) |   # respondent said too busy
    (household["RSPDNT05"] > 0) |   # scheduling difficulties
    (household["final_outcome_code"] == "321") |
    (household["final_outcome_code"] == "322")  # refused, time-related excuses
).astype(int)

# Hard to Locate — address instability: address can't be found or household moved
# Distinct from Hard to Contact: here the physical location itself is unknown/uncertain
household["htc_hard_to_locate"] = (
    (household["NCTPER08"] > 0) |
    (household["final_outcome_code"] == "341")
).astype(int)

# Hard to Contact — location is known but interviewer cannot reach/engage anyone
# Covers entry barriers (gated buildings), repeated no-contact visits, and scheduling/availability issues
household["htc_hard_to_contact"] = (
    (household["NCTPER07"] > 0) |   # locked gate or buzzer-entry building
    (household["NCTPER01"] > 0) |   # no one home on personal visit
    (household["NCTPER04"] > 0) |   # someone home but not answering door
    (household["NCTPER11"] > 0) |   # had to go through building management/doorman
    (household["final_outcome_code"] == "216")  # final outcome: no one home, unable to contact
).astype(int)

# Total number of HTC segments flagged per household
household["htc_segment_count"] = (
    household["htc_hard_to_interview"] +
    household["htc_hard_to_persuade"] +
    household["htc_hard_to_locate"] +
    household["htc_hard_to_contact"]
)

# Completed interview flag
household["completed"] = (household["final_outcome_code"] == "201").astype(int)

# ---------------------------------------------------------------------------
# Step 7 — Reorder columns for readability
# ---------------------------------------------------------------------------
ID_COLS     = ["CUID", "qyear", "max_wave"]
METRIC_COLS = ["contact_attempts", "days_in_field", "completed",
               "final_outcome_code", "final_outcome", "language"]
HTC_COLS    = ["htc_hard_to_interview", "htc_hard_to_persuade",
               "htc_hard_to_locate", "htc_hard_to_contact", "htc_segment_count"]
DETAIL_COLS = [c for c in household.columns
               if c not in ID_COLS + METRIC_COLS + HTC_COLS]

household = household[ID_COLS + METRIC_COLS + HTC_COLS + DETAIL_COLS]

# ---------------------------------------------------------------------------
# Step 8 — Save output
# ---------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
household.to_csv(OUT_PATH, index=False)
print(f"\nSaved clean file to: {OUT_PATH}")

# ---------------------------------------------------------------------------
# Step 9 — Print a quick summary so you can verify it looks right
# ---------------------------------------------------------------------------
print("\n--- Quick Summary ---")
print(f"Total households:      {len(household):,}")
print(f"Completed interviews:  {household['completed'].sum():,} ({household['completed'].mean()*100:.1f}%)")
print(f"Avg contact attempts:  {household['contact_attempts'].mean():.1f}")
print(f"Avg days in field:     {household['days_in_field'].mean():.1f}")
print()
print("HTC Segment Indicator Prevalence:")
for col, label in [
    ("htc_hard_to_interview", "Hard to Interview"),
    ("htc_hard_to_persuade",  "Hard to Persuade "),
    ("htc_hard_to_locate",    "Hard to Locate   "),
    ("htc_hard_to_contact",   "Hard to Contact  "),
]:
    n = household[col].sum()
    print(f"  {label}: {n:,} ({n/len(household)*100:.1f}%)")

print()
print("HTC Segment Count Distribution:")
for n, count in household["htc_segment_count"].value_counts().sort_index().items():
    print(f"  {n} segments: {count:,} ({count/len(household)*100:.1f}%)")
