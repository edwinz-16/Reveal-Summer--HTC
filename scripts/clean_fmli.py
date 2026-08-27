"""
clean_fmli.py
-------------
Reads all available raw FMLI (Family/household characteristics and income)
quarterly extracts, selects the variables relevant to HTC analysis, decodes
coded values, and saves a clean CSV to data/processed/.

Each quarterly FMLI file only contains households interviewed in that
specific calendar quarter — a given household reappears in a later quarter's
file once it reaches its next wave. Combining all available quarters
substantially increases how many MCHI households have a demographic match
(12.9% -> 56.2% as of the 12 quarters currently on hand), since each quarter
picks up a different slice of the panel.

A household can appear in more than one quarterly file (once per wave). We
keep one row per household — the most recent wave on file — since that's
closest to a "current" demographic snapshot; income/expenditure fields will
differ slightly by wave but region/tenure/demographics are generally stable.

FMLI also includes CE panel households outside the MCHI/HTC study, so after
deduplicating we restrict the output to households that also appear in
mchi_clean.csv — this file exists specifically to support MCHI-based HTC
analysis, and keeping non-matching households in it would let downstream
stats silently include households outside that population.

Input:  data/raw/fmli2*.csv (all quarterly extracts present),
        data/processed/mchi_clean.csv (must be generated first, via clean_mchi.py)
Output: data/processed/fmli_clean.csv
"""

import pandas as pd
import glob
import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
RAW_PATHS = sorted(glob.glob(os.path.join("data", "raw", "fmli2*.csv")))
OUT_PATH = os.path.join("data", "processed", "fmli_clean.csv")

# ---------------------------------------------------------------------------
# Step 1 — Load and combine all quarterly raw files
# ---------------------------------------------------------------------------
print(f"Found {len(RAW_PATHS)} FMLI quarterly extract(s): {[os.path.basename(p) for p in RAW_PATHS]}")
frames = []
for path in RAW_PATHS:
    chunk = pd.read_csv(path, dtype=str, low_memory=False)
    frames.append(chunk)
    print(f"  Loaded {os.path.basename(path)}: {chunk.shape[0]:,} rows x {chunk.shape[1]} columns")

df = pd.concat(frames, ignore_index=True)
print(f"  Combined shape (all quarters, before dedup): {df.shape[0]:,} rows")

# ---------------------------------------------------------------------------
# Step 2 — Select only the columns we need
#
# FMLI has 500+ expenditure/weighting columns that are irrelevant to HTC
# analysis. We keep identifiers, geography, reference-person demographics,
# household structure, housing tenure, and income.
# ---------------------------------------------------------------------------
KEEP_COLS = [
    # --- Identifiers ---
    "CUID",         # Household ID — joins to mchi_clean.csv
    "NEWID",        # Full record ID
    "QINTRVYR",     # Year of interview
    "QINTRVMO",     # Month of interview

    # --- Geography (fills the "No geographic identifiers" gap in MCHI) ---
    "REGION",       # Census region: Northeast/Midwest/South/West
    "DIVISION",     # Census division (9 sub-regions)
    "STATE",        # State FIPS code — see data quality note below
    "BLS_URBN",     # Urban / Rural
    "URBAN",        # Urban / Rural (alternate coding)
    "SMSASTAT",     # In a metropolitan statistical area?
    "POPSIZE",      # Population size class of area
    "CBSAPRIN",     # CBSA principal-city status (codes undocumented in dictionary — kept raw)

    # --- Reference person demographics ---
    "AGE_REF",      # Age of reference person
    "SEX_REF",      # Sex of reference person
    "REF_RACE",     # Race of reference person
    "HISP_REF",     # Hispanic origin of reference person
    "EDUC_REF",     # Education of reference person
    "MARITAL1",     # Marital status of reference person

    # --- Household structure ---
    "FAM_SIZE",     # Number of members in household
    "FAM_TYPE",     # Family type/composition
    "NO_EARNR",     # Number of earners
    "PERSLT18",     # Number of members under 18
    "PERSOT64",     # Number of members over 64

    # --- Housing ---
    "CUTENURE",     # Housing tenure: own w/mortgage, own outright, rent, etc.

    # --- Income ---
    "FINCBTAX",     # Total income before taxes, past 12 months
    "INC_RANK",     # Income percentile rank (0-1)
    "INCLASS2",     # Income as fraction of poverty threshold, bucketed
]

df = df[KEEP_COLS].copy()
print(f"  After column selection: {df.shape[1]} columns kept")

# ---------------------------------------------------------------------------
# Step 3 — Convert numeric columns from string
# ---------------------------------------------------------------------------
NUMERIC_COLS = [
    "QINTRVYR", "QINTRVMO", "AGE_REF", "FAM_SIZE", "NO_EARNR",
    "PERSLT18", "PERSOT64", "FINCBTAX", "INC_RANK",
]
for col in NUMERIC_COLS:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------------------------------------------------------
# Step 3b — Collapse to one row per household
#
# A household can appear in multiple quarterly files (once per wave). Sort
# by interview year/month and keep the last (most recent) record per CUID.
# ---------------------------------------------------------------------------
before_dedup = len(df)
df = df.sort_values(["CUID", "QINTRVYR", "QINTRVMO"]).drop_duplicates(subset="CUID", keep="last")
print(f"  After collapsing to one row per household (most recent wave): "
      f"{len(df):,} households (dropped {before_dedup - len(df):,} earlier-wave duplicate rows)")

# ---------------------------------------------------------------------------
# Step 3c — Restrict to households that also appear in MCHI
#
# FMLI is a general CE extract — it includes households outside the HTC
# study (e.g. panel members whose MCHI wave falls outside the quarters we
# have). Keeping those in fmli_clean.csv would be misleading for this
# project, since every finding here is about the MCHI-derived HTC
# population: anyone computing stats straight off fmli_clean.csv without
# re-joining to MCHI would silently include households this analysis was
# never meant to cover.
# ---------------------------------------------------------------------------
mchi_path = os.path.join("data", "processed", "mchi_clean.csv")
mchi_cuids = set(pd.read_csv(mchi_path, dtype=str, usecols=["CUID"])["CUID"])
before_mchi_filter = len(df)
df = df[df["CUID"].isin(mchi_cuids)]
print(f"  After restricting to MCHI-matching households: "
      f"{len(df):,} households (dropped {before_mchi_filter - len(df):,} with no MCHI match)")

# ---------------------------------------------------------------------------
# Step 4 — Decode coded values into readable labels
# ---------------------------------------------------------------------------
REGION_LABELS = {"1": "Northeast", "2": "Midwest", "3": "South", "4": "West"}

DIVISION_LABELS = {
    "1": "New England", "2": "Middle Atlantic", "3": "East North Central",
    "4": "West North Central", "5": "South Atlantic", "6": "East South Central",
    "7": "West South Central", "8": "Mountain", "9": "Pacific",
}

URBN_LABELS = {"1": "Urban", "2": "Rural"}

SMSASTAT_LABELS = {"1": "In metro area", "2": "Not in metro area"}

POPSIZE_LABELS = {
    "1": "5 million+", "2": "1.2-4 million", "3": "0.33-1.19 million",
    "4": "125-329.9 thousand", "5": "Less than 125 thousand", "6": "Suppressed",
}

CUTENURE_LABELS = {
    "1": "Owned w/ mortgage", "2": "Owned w/o mortgage", "4": "Rented",
    "5": "Occupied w/o payment of cash rent", "6": "Student housing",
}

SEX_LABELS = {"1": "Male", "2": "Female"}

RACE_LABELS = {
    "1": "White", "2": "Black", "3": "Native American",
    "4": "Asian", "5": "Pacific Islander", "6": "Multi-race",
}

HISP_LABELS = {"1": "Hispanic", "2": "Non-Hispanic"}

# EDUC_REF uses the 2013+ coding scheme (values 00, 10-17)
EDUC_LABELS = {
    "00": "Never attended school",
    "10": "Elementary (grades 1-8)",
    "11": "High school, no diploma",
    "12": "High school graduate",
    "13": "Some college, no degree",
    "14": "Associate's degree",
    "15": "Bachelor's degree",
    "16": "Master's/professional/doctorate degree",
}

MARITAL_LABELS = {
    "1": "Married", "2": "Widowed", "3": "Divorced",
    "4": "Separated", "5": "Never married",
}

FAM_TYPE_LABELS = {
    "1": "Married couple only",
    "2": "Married couple + children, oldest < 6",
    "3": "Married couple + children, oldest 6-17",
    "4": "Married couple + children, oldest 18+",
    "5": "Other married couple family",
    "6": "Single parent (male), children < 18",
    "7": "Single parent (female), children < 18",
    "8": "Single consumer",
    "9": "Other family",
}

INCLASS2_LABELS = {
    "1": "< 16.67% of poverty threshold", "2": "16.67-33.33%",
    "3": "33.34-49.99%", "4": "50.00-66.66%", "5": "66.67-83.33%",
    "6": "83.34-100.00%", "7": "Incomplete reporting",
}

df["region_label"]    = df["REGION"].map(REGION_LABELS).fillna("Unknown")
df["division_label"]  = df["DIVISION"].map(DIVISION_LABELS).fillna("Unknown")
df["urban_label"]     = df["BLS_URBN"].map(URBN_LABELS).fillna("Unknown")
df["metro_label"]     = df["SMSASTAT"].map(SMSASTAT_LABELS).fillna("Unknown")
df["popsize_label"]   = df["POPSIZE"].map(POPSIZE_LABELS).fillna("Unknown")
df["tenure_label"]    = df["CUTENURE"].map(CUTENURE_LABELS).fillna("Unknown")
df["sex_ref_label"]   = df["SEX_REF"].map(SEX_LABELS).fillna("Unknown")
df["race_label"]      = df["REF_RACE"].map(RACE_LABELS).fillna("Unknown")
df["hispanic_label"]  = df["HISP_REF"].map(HISP_LABELS).fillna("Unknown")
df["education_label"] = df["EDUC_REF"].map(EDUC_LABELS).fillna("Unknown")
df["marital_label"]   = df["MARITAL1"].map(MARITAL_LABELS).fillna("Unknown")
df["fam_type_label"]  = df["FAM_TYPE"].map(FAM_TYPE_LABELS).fillna("Unknown")
df["poverty_label"]   = df["INCLASS2"].map(INCLASS2_LABELS).fillna("Unknown")

# ---------------------------------------------------------------------------
# Step 5 — Income quartile (derived, for easy grouping in analysis)
# ---------------------------------------------------------------------------
df["income_quartile"] = pd.qcut(
    df["FINCBTAX"], 4, labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"]
)

# ---------------------------------------------------------------------------
# Step 6 — Reorder columns for readability
# ---------------------------------------------------------------------------
ID_COLS = ["CUID", "NEWID", "QINTRVYR", "QINTRVMO"]
GEO_COLS = ["REGION", "region_label", "DIVISION", "division_label", "STATE",
            "BLS_URBN", "urban_label", "URBAN", "SMSASTAT", "metro_label",
            "POPSIZE", "popsize_label", "CBSAPRIN"]
DEMO_COLS = ["AGE_REF", "SEX_REF", "sex_ref_label", "REF_RACE", "race_label",
             "HISP_REF", "hispanic_label", "EDUC_REF", "education_label",
             "MARITAL1", "marital_label"]
HH_COLS = ["FAM_SIZE", "FAM_TYPE", "fam_type_label", "NO_EARNR",
           "PERSLT18", "PERSOT64", "CUTENURE", "tenure_label"]
INCOME_COLS = ["FINCBTAX", "income_quartile", "INC_RANK", "INCLASS2", "poverty_label"]

df = df[ID_COLS + GEO_COLS + DEMO_COLS + HH_COLS + INCOME_COLS]

# ---------------------------------------------------------------------------
# Step 7 — Save output
# ---------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
df.to_csv(OUT_PATH, index=False)
print(f"\nSaved clean file to: {OUT_PATH}")

# ---------------------------------------------------------------------------
# Step 8 — Print a quick summary so you can verify it looks right
# ---------------------------------------------------------------------------
print("\n--- Quick Summary ---")
print(f"Total households:     {len(df):,}")
print(f"Unique CUIDs:          {df['CUID'].nunique():,}")
earliest = df.sort_values(["QINTRVYR", "QINTRVMO"]).iloc[0]
latest = df.sort_values(["QINTRVYR", "QINTRVMO"]).iloc[-1]
print(f"Interview period:      {earliest['QINTRVYR']:.0f}-{earliest['QINTRVMO']:02.0f} to "
      f"{latest['QINTRVYR']:.0f}-{latest['QINTRVMO']:02.0f}")

print("\nRegion distribution:")
print(df["region_label"].value_counts())

print("\nUrban/Rural distribution:")
print(df["urban_label"].value_counts())

print("\nTenure distribution:")
print(df["tenure_label"].value_counts())

print("\nMedian household income (FINCBTAX): "
      f"${df['FINCBTAX'].median():,.0f}")
