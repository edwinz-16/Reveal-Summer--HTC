"""
charts.py
---------
Figure-building functions for the HTC dashboard. Each function takes a
dataframe (so callbacks can pass filtered subsets) and returns a plotly
Figure.

Color values are built from the Reveal Labs brand palette (RL Blue
#0B3390, RL Sky #1E87E0, RL Light Blue #D3ECF7, RGC Lime #B6C93E, RL
Yellow #FFC600), adapted for use as data marks rather than applied as
flat swatches. Checked with WCAG contrast, OKLCH lightness/chroma, and
Machado-Oliveira-Fernandes 2009 CVD-simulated distance (script used for
the check: scratchpad/validate_brand.py from the session that did this):

- RL Blue is reserved for nav chrome only (see app.py) -- it does not
  double as a segment color, so no HTC characteristic looks like the
  dashboard's own chrome.
- RL Light Blue, RGC Lime, and RL Yellow do not pass as data marks on
  their own: all three fall below the 3:1 mark-contrast floor on this
  light surface (1.20:1 / 1.79:1 / 1.53:1), and Lime vs. Yellow are close
  enough to be nearly indistinguishable under simulated colorblindness
  (CVD delta as low as 0.9, floor is 6). Yellow is kept but re-stepped to
  a usable lightness/chroma (#B07D00, same hue angle, 3.54:1 contrast);
  Lime is dropped rather than shipped broken.
- The brand kit only really offers two well-separated hue families
  (blue and yellow-green), which isn't enough for 4 categorical segment
  identities that read as genuinely different colors, especially once
  blue and red were both ruled out as segment colors entirely (blue
  because RL Blue is the nav chrome and any blue segment reads as
  matching the dashboard's own frame; red because it's reserved for
  status-critical). Orange (~25-55 deg) does not work either: every
  lightness/chroma variant tested reads as a shade of status-critical
  red or collapses into the current Yellow under simulated
  colorblindness. That leaves only ~200 deg of the wheel usable at all
  (roughly 72-222 deg and 288-335 deg), which isn't enough hue budget
  for 4 segments that each read as a genuinely different color family
  to a non-expert, not just 4 colors that clear the numeric floors.
  Rather than force two segments into the same narrow violet/magenta
  wedge (an earlier version did exactly this -- rose #C668B2 and
  violet #6C4AB3 were only 41 deg apart and read as "the same purple"
  even though their raw OKLab distance technically passed), one segment
  (Hard to Locate) is now a deep, deliberately dark and desaturated
  teal-blue instead -- a scoped, explicit exception to "no blue," not
  an oversight. It's the one pairing in this palette that doesn't clear
  the ideal 15-point floor against nav-blue specifically (13.4), but at
  L=0.46/C=0.08 vs. nav-blue's vivid L=0.36/C=0.16 the two read as
  "slate/petrol" vs. "vivid navy" -- distinguishable in practice even
  though close in hue. Every other pairing in the palette -- all 6
  segment-to-segment comparisons, and every segment against both status
  colors and both nav colors -- clears the full normal-vision (>=15)
  and CVD (>=8 target, >=6 floor) checks. Only Yellow is a literal
  brand color; teal, deep teal-blue, and violet are flagged non-brand
  exceptions, each re-checked against the other three and against both
  status colors and both nav colors whenever one was added or changed.
  Status colors (completed/not-completed) stay on the existing
  accessible green/red rather than being forced into brand hues that
  don't carry that meaning.

The dashboard's content area is light (dark chrome lives only in the top
nav bar in app.py); this file only ever renders on the light surface.

Deliberately avoids dual-axis charts (two y-scales on one figure): where
scripts/visualizations.py paired a rate with a count on one plot, this
module renders them as two separate single-axis figures instead.

Bar labels use textposition="outside", so they render against the light
plot surface (not on top of each bar's own fill) -- a single dark-ink text
color is safe everywhere. The co-occurrence heatmap is the exception: its
labels sit *inside* colored cells, so its colorscale is deliberately capped
at a light-to-medium band (never the ramp's darkest steps) so dark-ink
text clears 4.5:1 against every cell, not just some.
"""

import textwrap

import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Palette -- brand-derived, see module docstring for how each value was
# checked and why RGC Lime doesn't appear anywhere in this file.
# ---------------------------------------------------------------------------
SURFACE = "#fcfcfb"       # light chart surface
GRID = "#e1e0d9"          # light gridline
AXIS = "#c3c2b7"          # light baseline/axis
INK = "#0b0b0b"           # light primary ink
INK_SECONDARY = "#52514e"  # light secondary ink

# Fixed categorical order -- one identity per HTC segment, reused everywhere
# that segment appears (e.g. the language chart drills into Hard to
# Interview, so it keeps Hard to Interview's aqua).
SEGMENT_COLORS = {
    "Hard to Contact": "#B07D00",    # RL Yellow, re-stepped for mark contrast
    "Hard to Persuade": "#763ebd",   # violet -- non-brand exception, see module docstring
    "Hard to Interview": "#00a49c",  # teal -- non-brand exception, see module docstring
    "Hard to Locate": "#1B5E7D",     # deep teal-blue -- non-brand exception, see module docstring
}
SEGMENT_COLS = ["htc_hard_to_contact", "htc_hard_to_persuade",
                "htc_hard_to_interview", "htc_hard_to_locate"]
SEGMENT_LABELS = ["Hard to Contact", "Hard to Persuade", "Hard to Interview", "Hard to Locate"]

# Completion is a genuine good/bad outcome -- status colors, not identity.
# Kept on the existing accessible green/red rather than forced into brand
# hues; the brand kit has no red or green, and this meaning (completed vs.
# not) recurs on every tab, so it gets a color no other element uses.
STATUS_GOOD = "#0ca30c"      # completed
STATUS_CRITICAL = "#d03b3b"  # not completed

# Ordinal one-hue ramp (RL Blue family, light->dark) for the 0-4 HTC
# segment count, where order carries meaning (more segments = more
# severe). Interpolated in OKLCH between RL Sky and RL Blue.
ORDINAL_BLUE = ["#8edaff", "#68b2ff", "#3a82e2", "#0c5ab5", "#00378f"]

# Single nominal-categorical hue for "one series across many groups" bars
# (demographic breakdowns) -- per the color formula, one series needs no
# legend and takes slot 1.
NOMINAL_BLUE = "#1E87E0"


def _wrap_title(text, width=42):
    """Plotly does not auto-wrap titles to the container width -- long ones
    just get clipped. Break at word boundaries and let the title span
    multiple lines instead."""
    return "<br>".join(textwrap.wrap(text, width=width))


def _style(fig, title, xaxis_title=None, yaxis_title=None, yrange=None, height=420):
    wrapped = _wrap_title(title)
    top_margin = 60 + wrapped.count("<br>") * 22  # extra room per wrapped line
    fig.update_layout(
        title=dict(text=wrapped, font_size=17, font_color=INK, x=0.5, xanchor="center"),
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        plot_bgcolor=SURFACE,
        paper_bgcolor=SURFACE,
        font=dict(color=INK_SECONDARY),
        showlegend=False,
        height=height + (top_margin - 60),
        margin=dict(t=top_margin, b=40, l=50, r=20),
    )
    fig.update_traces(selector=dict(type="bar"), textfont_color=INK)
    fig.update_xaxes(showgrid=False, linecolor=AXIS)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, linecolor=AXIS,
                      range=yrange, zeroline=False)
    return fig


# ---------------------------------------------------------------------------
# MCHI Segments tab
# ---------------------------------------------------------------------------
def fig_segment_prevalence(mchi):
    counts = [mchi[c].sum() for c in SEGMENT_COLS]
    pcts = [c / len(mchi) * 100 for c in counts]
    fig = go.Figure(go.Bar(
        x=SEGMENT_LABELS, y=pcts,
        marker_color=[SEGMENT_COLORS[l] for l in SEGMENT_LABELS],
        text=[f"{p:.1f}%" for p in pcts],
        textposition="outside",
        customdata=counts,
        hovertemplate="%{x}<br>%{y:.1f}%% of households<br>%{customdata:,} households<extra></extra>",
    ))
    return _style(fig, "Percentage of All Households Flagged With Each HTC Characteristic",
                  xaxis_title="HTC Characteristic",
                  yaxis_title="Percentage of Households", yrange=[0, 90])


def fig_segment_clustering(mchi):
    dist = mchi["htc_segment_count"].value_counts().sort_index()
    dist = dist[dist.index <= 4]
    fig = go.Figure(go.Bar(
        x=[str(i) for i in dist.index], y=dist.values,
        marker_color=[ORDINAL_BLUE[int(i)] for i in dist.index],
        text=[f"{v:,}<br>({v / len(mchi) * 100:.1f}%)" for v in dist.values],
        textposition="outside",
        hovertemplate="%{x} characteristics: %{y:,} households<extra></extra>",
    ))
    return _style(fig, "Number of HTC Characteristics Flagged Per Household, All Households",
                  xaxis_title="Number of Characteristics Flagged", yaxis_title="Number of Households")


def fig_completion_by_segment_count(df):
    g = df.groupby("htc_segment_count")["completed"].mean()
    g = g[g.index <= 4]
    fig = go.Figure(go.Bar(
        x=[str(i) for i in g.index], y=g.values * 100,
        marker_color=[ORDINAL_BLUE[int(i)] for i in g.index],
        text=[f"{v * 100:.1f}%" for v in g.values], textposition="outside",
        hovertemplate="%{x} characteristics: %{y:.1f}%% completion<extra></extra>",
    ))
    return _style(fig, "Completion Rate by Number of HTC Characteristics Flagged, All Households",
                  xaxis_title="Number of Characteristics Flagged",
                  yaxis_title="Completion Rate (Percentage)", yrange=[0, 100])


def fig_attempts_by_segment_count(df):
    g = df.groupby("htc_segment_count")["contact_attempts"].mean()
    g = g[g.index <= 4]
    fig = go.Figure(go.Bar(
        x=[str(i) for i in g.index], y=g.values,
        marker_color=[ORDINAL_BLUE[int(i)] for i in g.index],
        text=[f"{v:.1f}" for v in g.values], textposition="outside",
        hovertemplate="%{x} characteristics: %{y:.1f} average attempts<extra></extra>",
    ))
    return _style(fig, "Average Contact Attempts by Number of HTC Characteristics Flagged, All Households",
                  xaxis_title="Number of Characteristics Flagged",
                  yaxis_title="Average Number of Contact Attempts")


def fig_cooccurrence_heatmap(mchi):
    total = len(mchi)
    matrix = []
    for a in SEGMENT_COLS:
        row = []
        for b in SEGMENT_COLS:
            row.append(None if a == b else round(((mchi[a] == 1) & (mchi[b] == 1)).sum() / total * 100, 1))
        matrix.append(row)
    fig = go.Figure(go.Heatmap(
        # Capped at step 350 (never the ramp's darkest steps) rather than
        # the full ramp -- cell labels render *inside* the fill, so every
        # cell needs to stay light enough for dark-ink text to clear 4.5:1.
        z=matrix, x=SEGMENT_LABELS, y=SEGMENT_LABELS,
        colorscale=[[0, "#8edaff"], [0.5, "#68b2ff"], [1, "#3a82e2"]],
        text=[[f"{v}%" if v is not None else "" for v in row] for row in matrix],
        texttemplate="%{text}", textfont=dict(size=13, color=INK),
        hovertemplate="%{y} + %{x}: %{z}%% of households<extra></extra>",
        showscale=True,
        colorbar=dict(tickfont=dict(color=INK_SECONDARY), outlinecolor=AXIS),
    ))
    heatmap_title = _wrap_title("Percentage of Households Flagged With Each Pair of HTC Characteristics")
    top_margin = 60 + heatmap_title.count("<br>") * 22
    fig.update_layout(title=dict(text=heatmap_title, font_size=17, font_color=INK, x=0.5, xanchor="center"),
                       plot_bgcolor=SURFACE, paper_bgcolor=SURFACE,
                       height=440 + (top_margin - 60),
                       font=dict(color=INK_SECONDARY),
                       margin=dict(t=top_margin, b=40, l=90, r=20))
    return fig


def fig_language_breakdown(mchi):
    # Top 5, not top 10 -- the tail past Korean (Arabic, Portuguese, Polish,
    # Japanese, Tagalog, French, Italian, Urdu) is thin (1-25 households
    # each) and added length without much signal.
    lang = mchi[mchi["language"] != "None recorded"]["language"].value_counts()
    lang = lang[lang.index != "Other"].head(5)
    fig = go.Figure(go.Bar(
        x=lang.values, y=lang.index, orientation="h",
        marker_color=SEGMENT_COLORS["Hard to Interview"],
        text=[f"{v:,}" for v in lang.values], textposition="outside",
        hovertemplate="%{y}: %{x:,} households<extra></extra>",
    ))
    fig.update_yaxes(autorange="reversed")
    return _style(fig, "Most Common Languages Among Language-Flagged Hard to Interview Households",
                  xaxis_title="Number of Households", height=440)


def fig_wave_completion(mchi):
    g = mchi.groupby("max_wave")["completed"].mean()
    g = g[g.index.isin([1, 2, 3, 4])]
    fig = go.Figure(go.Bar(
        x=[f"Wave {int(i)}" for i in g.index], y=g.values * 100,
        marker_color=[ORDINAL_BLUE[int(i) - 1] for i in g.index],
        text=[f"{v * 100:.1f}%" for v in g.values], textposition="outside",
    ))
    return _style(fig, "Completion Rate by Interview Wave, All Households",
                  xaxis_title="Interview Wave",
                  yaxis_title="Completion Rate (Percentage)", yrange=[0, 60])


def fig_wave_attempts(mchi):
    g = mchi.groupby("max_wave")["contact_attempts"].mean()
    g = g[g.index.isin([1, 2, 3, 4])]
    fig = go.Figure(go.Bar(
        x=[f"Wave {int(i)}" for i in g.index], y=g.values,
        marker_color=[ORDINAL_BLUE[int(i) - 1] for i in g.index],
        text=[f"{v:.1f}" for v in g.values], textposition="outside",
    ))
    return _style(fig, "Average Contact Attempts by Interview Wave, All Households",
                  xaxis_title="Interview Wave",
                  yaxis_title="Average Number of Contact Attempts")


def fig_seasonality(mchi):
    g = mchi.groupby("qyear")["completed"].mean().sort_index()
    labels = [f"{str(int(q))[:4]} Q{str(int(q))[4]}" for q in g.index]
    # Flat single hue, deliberately -- completion barely moves quarter to
    # quarter (37.6-41.9%), and an ordinal gradient here would visually
    # imply a trend/severity order that the data doesn't actually show.
    fig = go.Figure(go.Bar(
        x=labels, y=g.values * 100, marker_color=NOMINAL_BLUE,
        text=[f"{v * 100:.1f}%" for v in g.values], textposition="outside",
        hovertemplate="%{x}: %{y:.1f}%% completion<extra></extra>",
    ))
    return _style(fig, "Completion Rate by Calendar Quarter, All Households", xaxis_title="Calendar Quarter",
                  yaxis_title="Completion Rate (Percentage)", yrange=[0, 55])


# ---------------------------------------------------------------------------
# Per-segment detail (By HTC Segment tab)
# ---------------------------------------------------------------------------
NEUTRAL_GRAY = "#c3c2b7"  # "without this characteristic" comparison bar


def fig_segment_completion(mchi, segment_col, segment_color, segment_name):
    with_rate = mchi[mchi[segment_col] == 1]["completed"].mean() * 100
    without_rate = mchi[mchi[segment_col] == 0]["completed"].mean() * 100
    with_n = int((mchi[segment_col] == 1).sum())
    without_n = int((mchi[segment_col] == 0).sum())
    # The household count is placed in the x-axis category label, under the
    # bar, rather than combined with the percentage in the same data label.
    # Combining "41.8%" and "n = 28,720" in one label reads as though the
    # percentage is a share of that count, when the count is actually the
    # denominator the percentage was already computed from.
    fig = go.Figure(go.Bar(
        x=[f"Flagged<br>(n = {with_n:,} households)",
           f"Not Flagged<br>(n = {without_n:,} households)"],
        y=[with_rate, without_rate],
        marker_color=[segment_color, NEUTRAL_GRAY],
        text=[f"{with_rate:.1f}%", f"{without_rate:.1f}%"],
        textposition="outside",
    ))
    return _style(fig, f"Completion Rate for Households With and Without the {segment_name} Characteristic",
                  yaxis_title="Completion Rate (Percentage)", yrange=[0, 90])


def fig_segment_attempts(mchi, segment_col, segment_color, segment_name):
    with_avg = mchi[mchi[segment_col] == 1]["contact_attempts"].mean()
    without_avg = mchi[mchi[segment_col] == 0]["contact_attempts"].mean()
    with_n = int((mchi[segment_col] == 1).sum())
    without_n = int((mchi[segment_col] == 0).sum())
    fig = go.Figure(go.Bar(
        x=[f"Flagged<br>(n = {with_n:,} households)",
           f"Not Flagged<br>(n = {without_n:,} households)"],
        y=[with_avg, without_avg],
        marker_color=[segment_color, NEUTRAL_GRAY],
        text=[f"{with_avg:.1f}", f"{without_avg:.1f}"], textposition="outside",
    ))
    return _style(fig, f"Average Contact Attempts for Households With and Without the {segment_name} Characteristic",
                  yaxis_title="Average Number of Contact Attempts")


# ---------------------------------------------------------------------------
# FPAR tab
# ---------------------------------------------------------------------------
def fig_refusal_conversion(fpar_household):
    hp = fpar_household[fpar_household["htc_hard_to_persuade"] == 1]
    g = hp.groupby("ever_converted")["completed"].agg(["mean", "count"])
    vals = [g.loc[False, "mean"] * 100, g.loc[True, "mean"] * 100]
    counts = [int(g.loc[False, "count"]), int(g.loc[True, "count"])]
    labels = [f"Never Converted<br>(n = {counts[0]:,} households)",
              f"Ever Converted<br>(n = {counts[1]:,} households)"]
    fig = go.Figure(go.Bar(
        x=labels, y=vals, marker_color=[STATUS_CRITICAL, STATUS_GOOD],
        text=[f"{v:.1f}%" for v in vals], textposition="outside",
    ))
    return _style(fig, "Completion Rate by Refusal Conversion Status, Hard to Persuade Households",
                  yaxis_title="Completion Rate (Percentage)", yrange=[0, 90])


def fig_mode_segments(fpar_household):
    g = fpar_household[fpar_household["mode_group"].isin(
        ["Personal visit", "Phone"])]
    agg = g.groupby("mode_group")["htc_segment_count"].mean()
    colors = [SEGMENT_COLORS["Hard to Contact"] if "Personal" in l else SEGMENT_COLORS["Hard to Persuade"]
              for l in agg.index]
    fig = go.Figure(go.Bar(
        x=list(agg.index), y=agg.values, marker_color=colors,
        text=[f"{v:.2f}" for v in agg.values], textposition="outside",
    ))
    return _style(fig, "Average Number of HTC Characteristics by Completed Interview Mode",
                  xaxis_title="Interview Mode",
                  yaxis_title="Average Number of Characteristics", height=380)


def fig_mode_attempts(fpar_household):
    g = fpar_household[fpar_household["mode_group"].isin(
        ["Personal visit", "Phone"])]
    agg = g.groupby("mode_group")["contact_attempts"].mean()
    colors = [SEGMENT_COLORS["Hard to Contact"] if "Personal" in l else SEGMENT_COLORS["Hard to Persuade"]
              for l in agg.index]
    fig = go.Figure(go.Bar(
        x=list(agg.index), y=agg.values, marker_color=colors,
        text=[f"{v:.1f}" for v in agg.values], textposition="outside",
    ))
    return _style(fig, "Average Contact Attempts by Completed Interview Mode",
                  xaxis_title="Interview Mode",
                  yaxis_title="Average Number of Contact Attempts", height=380)


# ---------------------------------------------------------------------------
# FMLI tab
# ---------------------------------------------------------------------------
def fig_htc_prevalence_by_completion(fmli_household):
    g = fmli_household.groupby("completed")["at_least_one_htc"].agg(["mean", "count"])
    vals = [g.loc[0, "mean"] * 100, g.loc[1, "mean"] * 100]
    counts = [int(g.loc[0, "count"]), int(g.loc[1, "count"])]
    labels = [f"Not Completed<br>(n = {counts[0]:,} households)",
              f"Completed<br>(n = {counts[1]:,} households)"]
    fig = go.Figure(go.Bar(
        x=labels, y=vals, marker_color=[STATUS_CRITICAL, STATUS_GOOD],
        text=[f"{v:.1f}%" for v in vals], textposition="outside",
    ))
    return _style(fig, "Percentage of Households With At Least One HTC Characteristic, by Completion Status",
                  yaxis_title="Percentage With At Least One Characteristic", yrange=[0, 110], height=380)


def fig_segment_count_by_completion(fmli_household):
    g = fmli_household.groupby(["htc_segment_count", "completed"]).size().unstack(fill_value=0)
    g = g[g.index <= 4]
    pct = g.div(g.sum(axis=0), axis=1) * 100
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Not Completed", x=[str(i) for i in pct.index], y=pct[0],
                          marker_color=STATUS_CRITICAL,
                          text=[f"{v:.1f}%" for v in pct[0]], textposition="outside"))
    fig.add_trace(go.Bar(name="Completed", x=[str(i) for i in pct.index], y=pct[1],
                          marker_color=STATUS_GOOD,
                          text=[f"{v:.1f}%" for v in pct[1]], textposition="outside"))
    fig.update_layout(barmode="group", showlegend=True,
                       legend=dict(x=0.5, y=1.12, orientation="h", xanchor="center"))
    return _style(fig, "Distribution of Number of HTC Characteristics Flagged, by Completion Status",
                  xaxis_title="Number of Characteristics Flagged",
                  yaxis_title="Percentage Within Group", yrange=[0, 85], height=420)


DIMENSIONS = {
    "Tenure": "tenure_label",
    "Age of reference person": "age_band",
    "Region": "region_label",
    "Urban / Rural": "urban_label",
}


def fig_subgroup_composition(fmli_household, dimension_label):
    col = DIMENSIONS[dimension_label]
    sub = fmli_household[(fmli_household["at_least_one_htc"] == 1) & (fmli_household["completed"] == 1)]
    vc = (sub[col].value_counts(normalize=True) * 100).sort_values(ascending=False)
    fig = go.Figure(go.Bar(
        x=[str(v) for v in vc.index], y=vc.values, marker_color=NOMINAL_BLUE,
        text=[f"{v:.1f}%" for v in vc.values], textposition="outside",
    ))
    return _style(fig, f"Distribution of HTC-Flagged and Completed Households by {dimension_label}",
                  xaxis_title=dimension_label,
                  yaxis_title="Percentage of This Subgroup (n = {:,})".format(len(sub)), height=420)
