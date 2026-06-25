"""
visualizations.py
-----------------
Generates all key charts from the MCHI household-level findings.
Charts are saved as HTML files (interactive) in a visuals/ folder.

Input:  data/processed/mchi_clean.csv
Output: visuals/*.html
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
df = pd.read_csv("data/processed/mchi_clean.csv", low_memory=False)

NUMERIC = ["contact_attempts", "days_in_field", "completed", "barrier_count",
           "htc_language", "htc_distrust", "htc_hard_locate", "htc_scheduling",
           "max_wave"]
for col in NUMERIC:
    df[col] = pd.to_numeric(df[col], errors="coerce")

os.makedirs("visuals", exist_ok=True)

# Color palette — consistent across all charts
COLORS = {
    "scheduling":  "#4C72B0",
    "distrust":    "#DD8452",
    "hard_locate": "#55A868",
    "language":    "#C44E52",
    "neutral":     "#8172B2",
    "completed":   "#2ecc71",
    "incomplete":  "#e74c3c",
}

print("Generating charts...")

# ---------------------------------------------------------------------------
# Chart 1 — Barrier Prevalence
# How common is each HTC barrier across all households
# ---------------------------------------------------------------------------
barriers = ["htc_scheduling", "htc_distrust", "htc_hard_locate", "htc_language"]
labels   = ["Scheduling /\nTime Constraints", "Government\nDistrust", "Hard to\nLocate", "Language\nBarrier"]
colors   = [COLORS["scheduling"], COLORS["distrust"], COLORS["hard_locate"], COLORS["language"]]
counts   = [df[b].sum() for b in barriers]
pcts     = [c / len(df) * 100 for c in counts]

fig1 = go.Figure(go.Bar(
    x=labels,
    y=pcts,
    marker_color=colors,
    text=[f"{p:.1f}%<br>({c:,} households)" for p, c in zip(pcts, counts)],
    textposition="outside",
    hovertemplate="%{x}<br>%{y:.1f}% of households<extra></extra>",
))
fig1.update_layout(
    title=dict(text="HTC Barrier Prevalence Across All Households", font_size=18),
    xaxis_title="HTC Barrier Type",
    yaxis_title="% of Households Flagged",
    yaxis_range=[0, 85],
    plot_bgcolor="white",
    showlegend=False,
    height=500,
)
fig1.update_xaxes(showgrid=False)
fig1.update_yaxes(showgrid=True, gridcolor="#eeeeee")
fig1.write_html("visuals/1_barrier_prevalence.html")
print("  Chart 1 saved — Barrier Prevalence")

# ---------------------------------------------------------------------------
# Chart 2 — Barrier Clustering
# How many barriers does each household face?
# ---------------------------------------------------------------------------
cluster = df["barrier_count"].value_counts().sort_index()
cluster_labels = ["0 barriers\n(no flags)", "1 barrier", "2 barriers",
                  "3 barriers", "4 barriers"]
cluster_colors = ["#95a5a6", "#3498db", "#e67e22", "#e74c3c", "#8e44ad"]

fig2 = go.Figure(go.Bar(
    x=cluster_labels[:len(cluster)],
    y=cluster.values,
    marker_color=cluster_colors[:len(cluster)],
    text=[f"{v:,}<br>({v/len(df)*100:.1f}%)" for v in cluster.values],
    textposition="outside",
    hovertemplate="%{x}: %{y:,} households<extra></extra>",
))
fig2.update_layout(
    title=dict(text="How Many HTC Barriers Does Each Household Face?", font_size=18),
    xaxis_title="Number of Barriers",
    yaxis_title="Number of Households",
    yaxis_range=[0, max(cluster.values) * 1.15],
    plot_bgcolor="white",
    showlegend=False,
    height=500,
)
fig2.update_xaxes(showgrid=False)
fig2.update_yaxes(showgrid=True, gridcolor="#eeeeee")
fig2.write_html("visuals/2_barrier_clustering.html")
print("  Chart 2 saved — Barrier Clustering")

# ---------------------------------------------------------------------------
# Chart 3 — The Compounding Effect (dual axis)
# As barriers increase: completion drops, attempts climb
# ---------------------------------------------------------------------------
barrier_groups = df.groupby("barrier_count").agg(
    avg_attempts=("contact_attempts", "mean"),
    completion_rate=("completed", "mean"),
    count=("completed", "count"),
).reset_index()
barrier_groups = barrier_groups[barrier_groups["barrier_count"] <= 4]
barrier_groups["completion_pct"] = barrier_groups["completion_rate"] * 100

fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(
    x=barrier_groups["barrier_count"].astype(str),
    y=barrier_groups["completion_pct"],
    name="Completion Rate (%)",
    marker_color=COLORS["completed"],
    opacity=0.85,
    hovertemplate="Barriers: %{x}<br>Completion: %{y:.1f}%<extra></extra>",
), secondary_y=False)

fig3.add_trace(go.Scatter(
    x=barrier_groups["barrier_count"].astype(str),
    y=barrier_groups["avg_attempts"],
    name="Avg Contact Attempts",
    mode="lines+markers",
    marker=dict(size=10, color=COLORS["incomplete"]),
    line=dict(color=COLORS["incomplete"], width=3),
    hovertemplate="Barriers: %{x}<br>Avg Attempts: %{y:.1f}<extra></extra>",
), secondary_y=True)

fig3.update_layout(
    title=dict(text="The Compounding Effect: More Barriers = Harder to Reach", font_size=18),
    xaxis_title="Number of HTC Barriers Per Household",
    plot_bgcolor="white",
    legend=dict(x=0.5, y=1.1, orientation="h", xanchor="center"),
    height=500,
)
fig3.update_yaxes(title_text="Completion Rate (%)", secondary_y=False,
                  range=[0, 65], showgrid=True, gridcolor="#eeeeee")
fig3.update_yaxes(title_text="Avg Contact Attempts", secondary_y=True,
                  range=[0, 30], showgrid=False)
fig3.write_html("visuals/3_compounding_effect.html")
print("  Chart 3 saved — Compounding Effect")

# ---------------------------------------------------------------------------
# Chart 4 — Severity by Barrier Type
# Completion rate WITH vs WITHOUT each barrier
# ---------------------------------------------------------------------------
barrier_names = {
    "htc_hard_locate": "Hard to Locate",
    "htc_distrust":    "Govt Distrust",
    "htc_language":    "Language Barrier",
    "htc_scheduling":  "Scheduling",
}

with_rates    = []
without_rates = []
attempt_with  = []
names         = []

for col, label in barrier_names.items():
    names.append(label)
    with_rates.append(df[df[col] == 1]["completed"].mean() * 100)
    without_rates.append(df[df[col] == 0]["completed"].mean() * 100)
    attempt_with.append(df[df[col] == 1]["contact_attempts"].mean())

fig4 = go.Figure()
fig4.add_trace(go.Bar(
    name="With Barrier",
    x=names,
    y=with_rates,
    marker_color=COLORS["incomplete"],
    text=[f"{r:.1f}%" for r in with_rates],
    textposition="outside",
))
fig4.add_trace(go.Bar(
    name="Without Barrier",
    x=names,
    y=without_rates,
    marker_color=COLORS["completed"],
    text=[f"{r:.1f}%" for r in without_rates],
    textposition="outside",
))
fig4.update_layout(
    title=dict(text="Completion Rate: With vs. Without Each Barrier", font_size=18),
    xaxis_title="HTC Barrier",
    yaxis_title="Completion Rate (%)",
    yaxis_range=[0, 65],
    barmode="group",
    plot_bgcolor="white",
    legend=dict(x=0.5, y=1.1, orientation="h", xanchor="center"),
    height=500,
)
fig4.update_xaxes(showgrid=False)
fig4.update_yaxes(showgrid=True, gridcolor="#eeeeee")
fig4.write_html("visuals/4_severity_by_barrier.html")
print("  Chart 4 saved — Severity by Barrier Type")

# ---------------------------------------------------------------------------
# Chart 5 — Co-occurring Barrier Pairs (heatmap)
# ---------------------------------------------------------------------------
barrier_cols  = ["htc_language", "htc_distrust", "htc_hard_locate", "htc_scheduling"]
barrier_short = ["Language", "Distrust", "Hard to Locate", "Scheduling"]
total = len(df)

matrix = []
for b1 in barrier_cols:
    row = []
    for b2 in barrier_cols:
        if b1 == b2:
            row.append(None)
        else:
            count = ((df[b1] == 1) & (df[b2] == 1)).sum()
            row.append(round(count / total * 100, 1))
    matrix.append(row)

fig5 = go.Figure(go.Heatmap(
    z=matrix,
    x=barrier_short,
    y=barrier_short,
    colorscale="Oranges",
    text=[[f"{v}%" if v is not None else "" for v in row] for row in matrix],
    texttemplate="%{text}",
    textfont=dict(size=14),
    hovertemplate="%{y} + %{x}<br>Co-occur in %{z}% of households<extra></extra>",
    showscale=True,
))
fig5.update_layout(
    title=dict(text="Barrier Co-occurrence: % of Households With Both Barriers", font_size=18),
    height=480,
    plot_bgcolor="white",
)
fig5.write_html("visuals/5_cooccurrence_heatmap.html")
print("  Chart 5 saved — Co-occurrence Heatmap")

# ---------------------------------------------------------------------------
# Chart 6 — Language Breakdown
# Which languages are most common among flagged households
# ---------------------------------------------------------------------------
lang_df = df[df["language"] != "None recorded"]["language"].value_counts().reset_index()
lang_df.columns = ["language", "count"]
lang_df = lang_df[lang_df["language"] != "Other"].head(10)  # top 10, exclude vague "other"

fig6 = go.Figure(go.Bar(
    x=lang_df["count"],
    y=lang_df["language"],
    orientation="h",
    marker_color=COLORS["language"],
    text=[f"{c:,}" for c in lang_df["count"]],
    textposition="outside",
    hovertemplate="%{y}: %{x} households<extra></extra>",
))
fig6.update_layout(
    title=dict(text="Language Barriers: Most Common Languages Among Flagged Households", font_size=18),
    xaxis_title="Number of Households",
    yaxis=dict(autorange="reversed"),
    plot_bgcolor="white",
    showlegend=False,
    height=480,
)
fig6.update_xaxes(showgrid=True, gridcolor="#eeeeee")
fig6.update_yaxes(showgrid=False)
fig6.write_html("visuals/6_language_breakdown.html")
print("  Chart 6 saved — Language Breakdown")

# ---------------------------------------------------------------------------
# Chart 7 — Interview Wave Patterns
# How effort and completion change across the 5-wave panel
# ---------------------------------------------------------------------------
wave_df = df.groupby("max_wave").agg(
    avg_attempts=("contact_attempts", "mean"),
    completion_rate=("completed", "mean"),
    count=("completed", "count"),
).reset_index()
wave_df = wave_df[wave_df["max_wave"].between(1, 5)]
wave_df["completion_pct"] = wave_df["completion_rate"] * 100

fig7 = make_subplots(specs=[[{"secondary_y": True}]])

fig7.add_trace(go.Bar(
    x=wave_df["max_wave"].astype(int).astype(str),
    y=wave_df["avg_attempts"],
    name="Avg Contact Attempts",
    marker_color="#4C72B0",
    opacity=0.8,
    hovertemplate="Wave %{x}<br>Avg Attempts: %{y:.1f}<extra></extra>",
), secondary_y=False)

fig7.add_trace(go.Scatter(
    x=wave_df["max_wave"].astype(int).astype(str),
    y=wave_df["completion_pct"],
    name="Completion Rate (%)",
    mode="lines+markers",
    marker=dict(size=10, color=COLORS["completed"]),
    line=dict(color=COLORS["completed"], width=3),
    hovertemplate="Wave %{x}<br>Completion: %{y:.1f}%<extra></extra>",
), secondary_y=True)

fig7.update_layout(
    title=dict(text="Contact Effort and Completion Rate Across Interview Waves", font_size=18),
    xaxis_title="Interview Wave",
    plot_bgcolor="white",
    legend=dict(x=0.5, y=1.1, orientation="h", xanchor="center"),
    height=500,
)
fig7.update_yaxes(title_text="Avg Contact Attempts", secondary_y=False,
                  range=[0, 25], showgrid=True, gridcolor="#eeeeee")
fig7.update_yaxes(title_text="Completion Rate (%)", secondary_y=True,
                  range=[0, 60], showgrid=False)
fig7.write_html("visuals/7_wave_patterns.html")
print("  Chart 7 saved — Wave Patterns")

# ---------------------------------------------------------------------------
# Chart 8 — Final Outcome Breakdown
# Where do non-completions end up?
# ---------------------------------------------------------------------------
outcome_df = df["final_outcome"].value_counts().reset_index()
outcome_df.columns = ["outcome", "count"]
outcome_df = outcome_df[outcome_df["outcome"] != "Other/Unknown"].head(8)
outcome_df["pct"] = outcome_df["count"] / len(df) * 100

outcome_colors = [
    COLORS["completed"] if o == "Completed" else "#e74c3c"
    if "Refused" in o else "#95a5a6"
    for o in outcome_df["outcome"]
]

fig8 = go.Figure(go.Bar(
    x=outcome_df["count"],
    y=outcome_df["outcome"],
    orientation="h",
    marker_color=outcome_colors,
    text=[f"{c:,} ({p:.1f}%)" for c, p in zip(outcome_df["count"], outcome_df["pct"])],
    textposition="outside",
    hovertemplate="%{y}<br>%{x:,} households<extra></extra>",
))
fig8.update_layout(
    title=dict(text="Final Interview Outcomes Across All Households", font_size=18),
    xaxis_title="Number of Households",
    xaxis_range=[0, 18000],
    yaxis=dict(autorange="reversed"),
    plot_bgcolor="white",
    showlegend=False,
    height=500,
)
fig8.update_xaxes(showgrid=True, gridcolor="#eeeeee")
fig8.update_yaxes(showgrid=False)
fig8.write_html("visuals/8_final_outcomes.html")
print("  Chart 8 saved — Final Outcomes")

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
print(f"\nAll charts saved to visuals/ folder.")
print("Open any .html file in your browser to view the interactive chart.")
