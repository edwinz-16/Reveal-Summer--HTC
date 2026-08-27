"""
clean_fpar.py
-------------
Reads the raw FPAR (Final Paradata) 2023-2024 file, selects HTC-relevant
variables, decodes coded values, and saves a clean CSV to data/processed/.

FPAR is one row per household PER WAVE (~102K rows, ~36K households, up to
4 waves each) — finer-grained than mchi_clean.csv, which collapses all waves
into one row per household. We keep that wave-level granularity here rather
than aggregating it away, since wave-to-wave change (e.g. a converted
refusal) is itself information MCHI cannot provide.

Input:  data/raw/fpar2324.csv
Output: data/processed/fpar_clean.csv
"""

import pandas as pd
import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
RAW_PATH = os.path.join("data", "raw", "fpar2324.csv")
OUT_PATH = os.path.join("data", "processed", "fpar_clean.csv")

# ---------------------------------------------------------------------------
# Step 1 — Load raw data
# ---------------------------------------------------------------------------
print("Loading raw FPAR data...")
df = pd.read_csv(RAW_PATH, dtype=str, low_memory=False)
print(f"  Raw shape: {df.shape[0]:,} rows x {df.shape[1]} columns")

# ---------------------------------------------------------------------------
# Step 2 — Select only the columns we need
#
# We drop the granular per-section/per-record indicator columns (TYPEREC1-9,
# TELSCT01-10) — too fine-grained for current analysis scope — and keep
# identifiers, outcome, interview mode, respondent engagement signals, and
# interview timing.
# ---------------------------------------------------------------------------
KEEP_COLS = [
    # --- Identifiers ---
    "CUID",         # Household ID — joins to mchi_clean.csv / fmli_clean.csv
    "NEWID",        # Full record ID (household + wave)
    "QYEAR",        # Year + quarter of this wave's interview

    # --- Outcome ---
    "OUTCOME",      # Final interview status for this wave
    "CONVREF",      # Was this a converted refusal? (initially refused, later completed)

    # --- Interview mode ---
    "HOW_INTV",     # Personal visit vs phone split across the interview
    "TELPV",        # Primary collection method: personal visit or phone
    "TEL_RESN",     # Main reason data was collected by phone

    # --- Housing / location context ---
    "HSG_UNIT",     # Type of housing unit (house, apt, mobile home, dorm, rooming house...)

    # --- Language ---
    "LANGUAGE",     # Language the interview was conducted in

    # --- Respondent engagement signals ---
    "RESPON",       # Line number of respondent (95 = proxy respondent)
    "RECORDS",      # How often respondent used records/bills to answer
    "SNGL_INT",     # Records used: single-person vs household records
    "GENINTRO",     # Did respondent confirm receiving the advance letter?
    "INFOBOOK",     # How often the information booklet was used
    "NUMDK",        # Number of "Don't Know" responses in this interview
    "NUMRF",        # Number of "Refused" responses in this interview
    "NUMEXPN",      # Number of expenditures reported (unedited)
    "EXPNSUM",      # Total value of expenditures reported (unedited)

    # --- Interview burden / timing (seconds) ---
    "SECTNO",       # Last section number completed (how far the interview got)
    "TOT_TIME",     # Total interview time
    "FRONT",        # Time on front-section (household roster/screening)
    "BACK",         # Time on back-section (recap/wrap-up)
    "COVERAGE",     # Time on coverage section
    "CONTROL",      # Time on control section
]

df = df[KEEP_COLS].copy()
print(f"  After column selection: {df.shape[1]} columns kept")

# ---------------------------------------------------------------------------
# Step 3 — Convert numeric columns from string
# ---------------------------------------------------------------------------
NUMERIC_COLS = [
    "QYEAR", "RESPON", "NUMDK", "NUMRF", "NUMEXPN", "EXPNSUM",
    "SECTNO", "TOT_TIME", "FRONT", "BACK", "COVERAGE", "CONTROL",
]
for col in NUMERIC_COLS:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------------------------------------------------------
# Step 4 — Decode coded values into readable labels
# ---------------------------------------------------------------------------

# Same final-outcome scheme as MCHI's FNLOTCME, plus a few FPAR-only codes.
# Code 314 is NOT in the CE-PUMD data dictionary — same undocumented-code
# issue already flagged for MCHI (see README Data Quality Notes). It is
# labeled explicitly here rather than silently bucketed. Code 313 was
# previously undocumented but has since been confirmed as "Stop Work
# (Type A Noninterview)".
OUTCOME_LABELS = {
    "201": "Completed",
    "203": "Transmit - no more follow-up possible",
    "215": "Insufficient partial",
    "216": "No one home - unable to contact",
    "217": "Temporarily absent",
    "219": "Other non-interview",
    "313": "Stop Work (Type A Noninterview)",
    "314": "Other/Unknown (undocumented code 314)",
    "321": "Refused - hostile respondent",
    "322": "Refused - time related",
    "323": "Refused - language problem",
    "324": "Refused - other",
    "341": "Household moved",
    "342": "Household merged with another CU at same address",
}

HOW_INTV_LABELS = {
    "1": "Personal visit for all sections",
    "2": "Personal visit, phone follow-up for some questions",
    "3": "Personal visit for most sections, rest by phone",
    "4": "Evenly split personal visit / phone",
    "5": "Phone for most sections, rest by personal visit",
    "6": "Phone for all sections",
}

TELPV_LABELS = {"1": "Personal visit", "2": "Phone"}

CONVREF_LABELS = {"1": "Yes - converted refusal", "2": "No"}

LANGUAGE_LABELS = {"1": "English", "2": "Spanish", "3": "Other"}

HSG_UNIT_LABELS = {
    "01": "House, apartment, or flat",
    "02": "HU in nontransient hotel/motel",
    "03": "HU, permanent in transient hotel/motel",
    "04": "HU in rooming house",
    "05": "Mobile home/trailer, no permanent room added",
    "06": "Mobile home/trailer, permanent room(s) added",
    "07": "HU not specified above",
    "08": "Quarters not HU, in rooming/boarding house",
    "09": "Student quarters in college dormitory",
    "10": "Group quarters, unit not specified",
}

RECORDS_LABELS = {
    "1": "Always/almost always (90%+)",
    "2": "Most of the time (50-89%)",
    "3": "Occasionally (10-49%)",
    "4": "Never/almost never (<10%)",
}

GENINTRO_LABELS = {"1": "Yes", "2": "No", "3": "Non-interview"}

INFOBOOK_LABELS = {
    "1": "Almost always (90%+)",
    "2": "Most of the time (50-89%)",
    "3": "Occasionally (10-49%)",
    "4": "Never/almost never (<10%)",
    "5": "No access to information booklet",
}

TEL_RESN_LABELS = {
    "1": "Barriers reaching the sample unit",
    "2": "Collecting data from additional respondent(s)",
    "3": "Distance to sample unit",
    "4": "Respondent called field rep to do interview",
    "5": "Respondent only available by phone",
    "6": "Respondent refused personal visit",
    "7": "Respondent requested telephone interview",
    "8": "Other",
}

SNGL_INT_LABELS = {"1": "Yes", "2": "No"}

df["outcome_label"]  = df["OUTCOME"].map(OUTCOME_LABELS).fillna("Other/Unknown")
df["how_intv_label"] = df["HOW_INTV"].map(HOW_INTV_LABELS).fillna("Unknown")
df["telpv_label"]    = df["TELPV"].map(TELPV_LABELS).fillna("Unknown")
df["convref_label"]  = df["CONVREF"].map(CONVREF_LABELS).fillna("Not applicable")
df["language_label"] = df["LANGUAGE"].map(LANGUAGE_LABELS).fillna("Unknown")
df["hsg_unit_label"] = df["HSG_UNIT"].map(HSG_UNIT_LABELS).fillna("Unknown")
df["records_label"]  = df["RECORDS"].map(RECORDS_LABELS).fillna("Unknown")
df["genintro_label"] = df["GENINTRO"].map(GENINTRO_LABELS).fillna("Unknown")
df["infobook_label"] = df["INFOBOOK"].map(INFOBOOK_LABELS).fillna("Unknown")
df["tel_resn_label"] = df["TEL_RESN"].map(TEL_RESN_LABELS).fillna("Not applicable")
df["sngl_int_label"] = df["SNGL_INT"].map(SNGL_INT_LABELS).fillna("Unknown")

# Completed flag, consistent with mchi_clean.py's household-level "completed" column
df["completed"] = (df["OUTCOME"] == "201").astype(int)

# ---------------------------------------------------------------------------
# Step 5 — Reorder columns for readability
# ---------------------------------------------------------------------------
ID_COLS = ["CUID", "NEWID", "QYEAR"]
OUTCOME_COLS = ["OUTCOME", "outcome_label", "completed", "CONVREF", "convref_label"]
MODE_COLS = ["HOW_INTV", "how_intv_label", "TELPV", "telpv_label",
             "TEL_RESN", "tel_resn_label", "HSG_UNIT", "hsg_unit_label",
             "LANGUAGE", "language_label"]
ENGAGEMENT_COLS = ["RESPON", "RECORDS", "records_label", "SNGL_INT", "sngl_int_label",
                    "GENINTRO", "genintro_label", "INFOBOOK", "infobook_label",
                    "NUMDK", "NUMRF", "NUMEXPN", "EXPNSUM"]
TIMING_COLS = ["SECTNO", "TOT_TIME", "FRONT", "BACK", "COVERAGE", "CONTROL"]

df = df[ID_COLS + OUTCOME_COLS + MODE_COLS + ENGAGEMENT_COLS + TIMING_COLS]

# ---------------------------------------------------------------------------
# Step 6 — Save output
# ---------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
df.to_csv(OUT_PATH, index=False)
print(f"\nSaved clean file to: {OUT_PATH}")

# ---------------------------------------------------------------------------
# Step 7 — Print a quick summary so you can verify it looks right
# ---------------------------------------------------------------------------
print("\n--- Quick Summary ---")
print(f"Total household-wave rows: {len(df):,}")
print(f"Unique households (CUID):  {df['CUID'].nunique():,}")
print(f"Waves per household:")
print(df.groupby("CUID").size().value_counts().sort_index())

print("\nOutcome distribution (per wave, not per household):")
print(df["outcome_label"].value_counts())

print("\nConverted refusals:")
print(df["convref_label"].value_counts())

print("\nInterview mode (TELPV):")
print(df["telpv_label"].value_counts())

print(f"\nMedian total interview time: {df['TOT_TIME'].median():.0f} seconds "
      f"({df['TOT_TIME'].median()/60:.1f} minutes)")
