"""
app.py
------
HTC Population Dashboard. Built in Plotly Dash (chosen over Streamlit,
which is not installed in this environment) to stay in pure Python and
match the existing chart style in scripts/visualizations.py.

Organized around four tabs: Overview and Crosswalk, All Segments
(population-level patterns that are not specific to one characteristic),
By HTC Segment (a dropdown-driven view of each of the four characteristics
individually, including which data sources support it), and Data Quality.

Run:  python dashboard/app.py
      then open http://127.0.0.1:8050
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dash
from dash import dcc, html, dash_table, Input, Output

from data import load_data
import charts as C

# ---------------------------------------------------------------------------
# Load data once at process start
# ---------------------------------------------------------------------------
DATA = load_data()
mchi = DATA["mchi"]
fpar_household = DATA["fpar_household"]
fmli_household = DATA["fmli_household"]

N_MCHI = len(mchi)
N_FMLI = len(fmli_household)
FMLI_COMPLETION = fmli_household["completed"].mean() * 100
BASELINE_COMPLETION = mchi["completed"].mean() * 100

# Dash app instance is created before any @dash.callback below so callbacks
# bind to it, and suppress_callback_exceptions is required because graph or
# dropdown ids referenced in callbacks only exist once their tab has been
# rendered by the tabs callback further down (they are not in the initial
# layout tree).
app = dash.Dash(__name__)
app.title = "HTC Population Dashboard"
app.config.suppress_callback_exceptions = True

# ---------------------------------------------------------------------------
# Style tokens (dataviz skill reference palette, light mode column, for the
# content area). Values are pre-validated for contrast and CVD-safety in
# references/palette.md, not eyeballed; see dashboard/charts.py header.
#
# The top nav bar is the one deliberately dark exception (see NAV_BG below).
# It is UI chrome, not a data encoding, styled after an official .gov nav
# bar (dark navy bar, light page body) rather than pulled from the
# categorical/status palette, so it does not need to pass the six-check
# categorical validator. It only needs its own text to clear WCAG contrast,
# noted in the comments next to each value below.
# ---------------------------------------------------------------------------
PAGE = "#f9f9f7"          # light page plane
SURFACE = "#fcfcfb"       # light chart/card surface
RAISED = "#f0efec"        # one step up from SURFACE, for table headers etc.
INK = "#0b0b0b"           # light primary ink
INK_SECONDARY = "#52514e"  # light secondary ink
MUTED = "#898781"         # muted ink, mode-invariant
BORDER = "rgba(11,11,11,0.10)"
STATUS_GOOD = C.STATUS_GOOD
STATUS_CRITICAL = C.STATUS_CRITICAL
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', 'Fira Code', monospace"

# Nav bar chrome -- RL Blue directly (brand primary), with hover/active
# steps derived by lightening it in OKLCH. White text on NAV_BG clears
# 10.8:1; on NAV_BG_HOVER 7.6:1; on NAV_BG_ACTIVE 9.0:1.
NAV_BG = "#0B3390"        # RL Blue
NAV_BG_HOVER = "#244ead"
NAV_BG_ACTIVE = "#1942a0"
NAV_TEXT = "#ffffff"
NAV_TEXT_MUTED = "#a9b7cc"

# Per-tab and per-segment accent (drawn from the same fixed segment order,
# not new hues). Gives each section a distinct identity color without
# inventing a palette.
ACCENT_OVERVIEW = C.SEGMENT_COLORS["Hard to Contact"]     # RL Sky
ACCENT_MCHI = C.SEGMENT_COLORS["Hard to Contact"]         # RL Sky
ACCENT_FPAR = C.SEGMENT_COLORS["Hard to Persuade"]        # violet (non-brand exception)
ACCENT_FMLI = C.SEGMENT_COLORS["Hard to Interview"]       # aqua (non-brand exception)
ACCENT_QUALITY = STATUS_CRITICAL                          # red (status, non-brand)


def _hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


# Light background tints of the segment colors, for color-coding table rows
# and badges with dark text on top -- not the raw segment colors themselves.
# Two of the four (Hard to Interview's aqua, Hard to Locate's yellow) fall
# below 3:1 contrast on the light surface even as marks, per the dataviz
# skill's palette notes, and well below the 4.5:1 text needs if used as
# solid-fill-plus-white-text (a mistake this dashboard made once already;
# see the fix to the source badges further down). A light tint behind dark
# ink keeps contrast high regardless of which segment color is used.
SEGMENT_TINT = {name: _hex_to_rgba(hexval, 0.14) for name, hexval in C.SEGMENT_COLORS.items()}


def card_style(accent=None):
    style = {
        "backgroundColor": SURFACE,
        "border": f"1px solid {BORDER}",
        "borderRadius": "8px",
        "padding": "20px",
        "marginBottom": "20px",
    }
    if accent:
        style["borderLeft"] = f"3px solid {accent}"
    return style


CARD_STYLE = card_style()
SECTION_TITLE = {"color": INK, "fontSize": "20px", "fontWeight": 600, "marginBottom": "6px"}
EYEBROW_STYLE = {"color": ACCENT_OVERVIEW, "fontSize": "12px", "fontWeight": 700,
                  "letterSpacing": "0.12em", "textTransform": "uppercase",
                  "fontFamily": MONO, "marginBottom": "4px"}
CAVEAT_BANNER = {
    "backgroundColor": _hex_to_rgba(ACCENT_FPAR, 0.10),
    "border": f"1px solid {ACCENT_FPAR}",
    "borderRadius": "6px",
    "padding": "12px 16px",
    "color": INK_SECONDARY,
    "marginBottom": "20px",
    "fontSize": "14px",
}

# ---------------------------------------------------------------------------
# Glossary: project-specific terms shown as a definition on hover or
# keyboard focus. Implemented as a styled <span title="..."> rather than
# custom JavaScript, so the definition is exposed to screen readers and
# keyboard users (tabIndex makes it focusable; see assets/style.css for the
# focus-visible styling) as well as mouse users.
# ---------------------------------------------------------------------------
TERM_DEFS = {
    "CUID": "Household identifier. Used to join records across the MCHI, FPAR, and FMLI files.",
    "wave": "One interview attempt in the CE panel's rotating schedule of up to five waves per household.",
    "waves": "Interview attempts in the CE panel's rotating schedule of up to five waves per household.",
    "FNLOTCME": "Final outcome code recorded for a household's last contact attempt in MCHI.",
    "converted refusal": "A household that initially refused to participate and was later persuaded to complete an interview.",
    "contact attempt": "One logged interviewer visit or call, whether or not it resulted in contact.",
    "HOW_INTV": "FPAR field recording how the completed interview was actually conducted: personal visit, phone, or a mix of both.",
    "TELPV": "FPAR field recording the attempted collection mode on a wave that did not complete.",
    "NEWID": "Full CE record identifier, combining household and wave.",
    "QYEAR": "Year and quarter code for a survey record. For example, 20231 refers to 2023 Q1.",
    "HTC": "Hard to Count. The Census Bureau framework describing population characteristics that make accurate counting more difficult.",
    "completion rate": "The share of households whose final recorded outcome was a completed interview.",
    "reference person": "The household member the CE Interview identifies as primarily responsible for the household's finances. FMLI demographic variables such as age, sex, and education are recorded for this person specifically, not necessarily every household member.",
    "paradata": "Data about the process of collecting a survey, not the survey answers themselves -- how many contact attempts were made, how long they took, what mode was used, why an attempt failed. This dashboard is built entirely from paradata, not from what households reported.",
}

# Terms shown as a visible list on the Overview tab, in addition to the
# hover/keyboard-focus definitions available throughout the dashboard via
# gl(). A subset of TERM_DEFS, picked for the terms a first-time reader is
# most likely to need spelled out up front. Pairs of (TERM_DEFS key, display label).
KEY_TERMS = [
    ("HTC", "HTC"),
    ("paradata", "Paradata"),
    ("CUID", "CUID"),
    ("wave", "Wave"),
    ("completion rate", "Completion Rate"),
    ("converted refusal", "Converted Refusal"),
    ("contact attempt", "Contact Attempt"),
    ("reference person", "Reference Person"),
]


def gl(display, key=None):
    return html.Span(display, title=TERM_DEFS[key or display], tabIndex="0",
                      className="glossary-term")


# ---------------------------------------------------------------------------
# Crosswalk table content (verbatim from the manager-reviewed check-in deck
# and HTC_Dashboard_README.docx; this is her explicit request from check-in 1)
# ---------------------------------------------------------------------------
CROSSWALK_ROWS = [
    # Ordered to match the SEGMENT_INFO / By HTC Segment dropdown order
    # (Contact, Persuade, Interview, Locate), not alphabetically.
    ("Hard to Contact", "Contact not established", "NCTPER07", "Unable to reach the household due to a locked gate or buzzer-entry building"),
    ("Hard to Contact", "Contact not established", "NCTPER01", "No one home on personal visit"),
    ("Hard to Contact", "Contact not established", "NCTPER04", "Someone appeared to be home but did not answer the door"),
    ("Hard to Contact", "Contact not established", "NCTPER11", "Interviewer had to go through building management or doorman"),
    ("Hard to Contact", "Contact not established", "FNLOTCME=216", "Final outcome: no one home, unable to make any contact"),
    ("Hard to Persuade", "Privacy / participation concerns", "RSPDNT07", "Respondent cited privacy concerns"),
    ("Hard to Persuade", "Privacy / participation concerns", "RSPDNT08", "Respondent cited concerns about government data collection"),
    ("Hard to Persuade", "Privacy / participation concerns", "RSPDNT11", "Contact was ended abruptly by respondent"),
    ("Hard to Persuade", "Privacy / participation concerns", "RSPDNT12", "Respondent expressed strong objection to continued contact"),
    ("Hard to Persuade", "Privacy / participation concerns", "NONINTR3", "Respondent indicated hesitation to participate"),
    ("Hard to Persuade", "Scheduling / availability decline", "NONINTR2", "Respondent indicated the time was inconvenient (contact was established)"),
    ("Hard to Persuade", "Scheduling / availability decline", "RSPDNT02", "Respondent said they were too busy (contact was established)"),
    ("Hard to Persuade", "Scheduling / availability decline", "RSPDNT05", "Respondent cited scheduling difficulties (contact was established)"),
    ("Hard to Persuade", "Scheduling / availability decline", "FNLOTCME=321", "Final outcome: interview not completed due to respondent non-participation"),
    ("Hard to Persuade", "Scheduling / availability decline", "FNLOTCME=322", "Final outcome: interview not completed, respondent cited time-related reasons"),
    ("Hard to Interview", "Language barrier", "NONINTR4", "Language was the reason the interview could not be conducted"),
    ("Hard to Interview", "Language barrier", "LNGUAGE2", "No household member was able to translate"),
    ("Hard to Interview", "Language barrier", "LNGUAGE4", "Interviewer was unable to find a translator"),
    ("Hard to Interview", "Language barrier", "LNGUAGE5", "No time left to find a translator"),
    ("Hard to Interview", "Language barrier", "LANGLIST", "Language spoken by the household (coded list)"),
    ("Hard to Interview", "Language barrier", "FNLOTCME=323", "Final outcome: refused due to language problem"),
    ("Hard to Interview", "Health barrier", "NONINTR5", "Respondent or household had a health problem preventing the interview"),
    ("Hard to Locate", "Address instability", "NCTPER08", "Address does not exist or interviewer was unable to locate it"),
    ("Hard to Locate", "Address instability", "FNLOTCME=341", "Final outcome: household moved during survey period"),
]
CROSSWALK_DF = [
    {"HTC Segment": s, "Characteristic": c, "MCHI Variable": v, "Description": d}
    for s, c, v, d in CROSSWALK_ROWS
]

DATA_QUALITY_ITEMS = [
    ("Outcome code 314 (FPAR only)", ["Still undocumented. It occurs 6,434 times, is not listed in the CE-PUMD "
                                      "dictionary, and does not appear in MCHI's ", gl("FNLOTCME"), " field."]),
    ("Wave 5 absent", ["The CE panel runs to 5 ", gl("waves", "wave"), ", but no Wave 5 records appear in the "
                       "2023 to 2024 file."]),
    ("Q1 2023 is oversized", "11,302 households, about 31% of the data, compared with about 3,100 per other quarter. This likely reflects the panel enrollment baseline rather than an error."),
    ("872 households, 0 days in field", "Final outcome recorded on the same day as first contact. This may reflect same-day refusals or a recording artifact."),
    ("Extreme outlier", ["One household was contacted 108 times over 30 days and still did not complete "
                         "(3 ", gl("HTC"), " characteristics, Spanish-speaking, Wave 4)."]),
]

# APA 7th-edition source citations. Only sources with confirmed author,
# year, and publisher are listed; a source without confirmed details is
# not fabricated here.
APA_SOURCES = [
    "U.S. Census Bureau. (2019). Counting the hard to count in a census [Working paper]. https://www.census.gov/content/dam/Census/library/working-papers/2019/demo/Hard-to-Count-Populations-Brief.pdf",
    "U.S. Bureau of Labor Statistics. (n.d.). Consumer Expenditure Survey public use microdata. U.S. Department of Labor. https://www.bls.gov/cex/pumd_doc.htm",
]

# The specific CE-PUMD files this dashboard is built from, same descriptions
# as the README's Data Sources table -- listed separately from APA_SOURCES
# since these are files within that one BLS publication, not independent
# citations.
DATA_FILES_USED = [
    ("mchi2324.csv", "Mode and Contact History Interview paradata, 2023-2024. One row per contact attempt (~522K rows, ~36K households). Primary data source."),
    ("fpar2324.csv", "Final Paradata, 2023-2024. One row per household per wave (~102,733 rows, ~36,270 households, up to 4 waves each). Records final wave outcome, converted-refusal flag, interview mode, and interview timing/burden."),
    ("fmli2202.csv-fmli2501.csv", "Family/household characteristics and income files, 12 quarterly extracts (2022 Q2-2025 Q1), combined, deduplicated, and restricted to MCHI-matching households (20,396 households)."),
    ("ce-pumd-interview-diary-dictionary.xlsx", "Official data dictionary for all CE-PUMD variables and coded values."),
]


SOURCE_PERIOD = {"MCHI": "2023-2024", "FPAR": "2023-2024", "FMLI": "2022 Q2-2025 Q1"}


def data_period_line(sources):
    periods = {}
    for src in sources:
        periods.setdefault(SOURCE_PERIOD[src], []).append(src)
    if len(periods) == 1:
        return f"Data period: {next(iter(periods))}."
    parts = [f"{'/'.join(srcs)} {period}" for period, srcs in periods.items()]
    return "Data period: " + "; ".join(parts) + "."


# ---------------------------------------------------------------------------
# HTC segment metadata for the By HTC Segment tab: definition, which data
# sources contain evidence for it, and notes on what each source shows.
# ---------------------------------------------------------------------------
SEGMENT_INFO = {
    "Hard to Contact": {
        "col": "htc_hard_to_contact",
        "color": C.SEGMENT_COLORS["Hard to Contact"],
        "description": (
            "The household's location is known, but the interviewer was not able to reach "
            "anyone there. This includes no one home during a personal visit, a locked gate "
            "or buzzer-entry building, and no answer at the door."
        ),
        "sources": ["MCHI", "FMLI"],
        "source_notes": [
            ("MCHI", "Indicator flags NCTPER07, NCTPER01, NCTPER04, and NCTPER11, along with final outcome code 216. See the crosswalk table below."),
            ("FMLI", ["Age of ", gl("reference person"), " shows a relationship with this characteristic: "
                      "households with a reference person 34 or younger are flagged with Hard to Contact "
                      "at a higher rate than households with a reference person 65 or older. See the All "
                      "Segments tab for the full FMLI demographic breakdown."]),
        ],
    },
    "Hard to Persuade": {
        "col": "htc_hard_to_persuade",
        "color": C.SEGMENT_COLORS["Hard to Persuade"],
        "description": (
            "Contact with the household was established; however, the respondent declined "
            "to participate. Recorded reasons include privacy concerns, distrust of "
            "government data collection, and stated scheduling conflicts."
        ),
        "sources": ["MCHI", "FPAR"],
        "source_notes": [
            ("MCHI", "Indicator flags RSPDNT07, RSPDNT08, RSPDNT11, RSPDNT12, NONINTR2, NONINTR3, RSPDNT02, and RSPDNT05, along with final outcome codes 321 and 322. See the crosswalk table below."),
            ("FPAR", "The refusal conversion chart below is scoped to households flagged with this characteristic."),
        ],
    },
    "Hard to Interview": {
        "col": "htc_hard_to_interview",
        "color": C.SEGMENT_COLORS["Hard to Interview"],
        "description": (
            "Language, health, or technological factors made it difficult to conduct the "
            "interview itself, including no household member able to translate, no translator "
            "available, a health problem preventing the interview, or a lack of technology "
            "needed to complete it."
        ),
        "sources": ["MCHI"],
        "source_notes": [
            ("MCHI", "Indicator flags NONINTR4, LNGUAGE2, LNGUAGE4, LNGUAGE5, and NONINTR5, along with the language spoken by the household and final outcome code 323. See the crosswalk table and language chart below. MCHI has no indicator for technological barriers -- see Data Quality."),
        ],
    },
    "Hard to Locate": {
        "col": "htc_hard_to_locate",
        "color": C.SEGMENT_COLORS["Hard to Locate"],
        "description": (
            "The household's physical address could not be confirmed or found, or the "
            "household moved during the survey period."
        ),
        "sources": ["MCHI"],
        "source_notes": [
            ("MCHI", "Indicator flag NCTPER08 and final outcome code 341. See the crosswalk table below. Due to the amount of flagged households, this indicator does not currently have a dedicated FPAR or FMLI breakdown."),
        ],
    },
}


def stat_tile(value, label, color=INK):
    return html.Div([
        html.Div(value, style={"fontSize": "32px", "fontWeight": 700, "color": color}),
        html.Div(label, style={"fontSize": "13px", "color": MUTED, "marginTop": "2px"}),
    ], style={"flex": "1", "minWidth": "160px", "textAlign": "center", "padding": "10px"})


def graph_card(fig, id_=None, sources=None):
    kwargs = {"figure": fig, "config": {"displayModeBar": False}}
    if id_:
        kwargs["id"] = id_
    children = [dcc.Graph(**kwargs, style={"width": "100%"})]
    if sources:
        children.append(html.P(data_period_line(sources),
                                style={"color": MUTED, "fontSize": "11.5px",
                                       "margin": "4px 2px 0"}))
    return html.Div(children, style={"flex": "1", "minWidth": "340px", "backgroundColor": SURFACE,
              "border": f"1px solid {BORDER}", "borderRadius": "8px", "padding": "12px"})


# ---------------------------------------------------------------------------
# Tab 1 -- Overview and Crosswalk
# ---------------------------------------------------------------------------
def overview_tab():
    return html.Div([
        html.Div([
            html.Div("CE PARADATA // MCHI · FPAR · FMLI // BLS", style=EYEBROW_STYLE),
            html.H2("Hard-to-Count Population Dashboard", style=SECTION_TITLE),
            html.P("Data period: MCHI and FPAR cover 2023-2024. FMLI combines 12 quarters, "
                   "2022 Q2 through 2025 Q1.",
                   style={"color": MUTED, "fontSize": "12.5px", "marginTop": "2px", "marginBottom": "10px"}),
            html.Div([
                stat_tile(f"{N_MCHI:,}", "Total Households"),
                stat_tile(f"{BASELINE_COMPLETION:.1f}%", "Overall Completion Rate"),
            ], style={"display": "flex", "flexWrap": "wrap", "marginTop": "10px"}),
        ], style=card_style(ACCENT_OVERVIEW)),

        html.Div([
            html.H3("How to Use This Dashboard", style={"color": INK, "fontSize": "16px"}),
            html.Ul([
                html.Li([
                    "The tabs are organized as follows:",
                    html.Ul([
                        html.Li([html.B("Overview and Crosswalk: "), "introduces the project and the indicator-to-segment mapping."]),
                        html.Li([html.B("All Segments: "), "presents population-level patterns across MCHI, FPAR, and FMLI."]),
                        html.Li([html.B("By HTC Segment: "), "presents each of the four characteristics individually, including which data sources support it."]),
                        html.Li([html.B("Data Quality: "), "lists known data issues and sources."]),
                    ], style={"paddingLeft": "20px", "marginTop": "4px"}),
                ], style={"color": INK_SECONDARY, "marginBottom": "10px"}),
                html.Li("The All Segments and By HTC Segment tabs include interactive filters "
                        "that update the charts below them.",
                        style={"color": INK_SECONDARY, "marginBottom": "6px"}),
                html.Li("Color coding is consistent across all tabs: green indicates a completed "
                        "or converted outcome, and red indicates incomplete outcomes.",
                        style={"color": INK_SECONDARY}),
                html.Li(["Terms specific to this project, such as ", gl("CUID"), " or ", gl("wave"),
                         ", show a definition on mouse hover or keyboard focus."],
                        style={"color": INK_SECONDARY, "marginTop": "6px"}),
            ], style={"paddingLeft": "20px", "margin": 0, "fontSize": "14px"}),
        ], style=CARD_STYLE),

        html.Div([
            html.H3("Important Terminology Note", style={"color": INK, "fontSize": "16px"}),
            html.P(
                ["The Census ", gl("HTC"), " framework defines four conceptual segments. This "
                 "dashboard uses “characteristics” when describing HTC populations. MCHI "
                 "indicators are interviewer-recorded proxies for these framework segments, "
                 "not direct measures of HTC population membership."],
                style={"color": INK_SECONDARY, "fontSize": "14px"},
            ),
        ], style=CARD_STYLE),

        html.Div([
            html.H3("Key Terms", style={"color": INK, "fontSize": "16px"}),
            html.Div([
                html.Div([
                    html.Span(label, style={"color": INK, "fontWeight": 700, "fontSize": "13px",
                                             "display": "block"}),
                    html.Span(TERM_DEFS[key], style={"color": INK_SECONDARY, "fontSize": "13px"}),
                ], style={"padding": "10px 0", "borderBottom": f"1px solid {BORDER}"})
                for key, label in KEY_TERMS
            ]),
        ], style=CARD_STYLE),

        html.Div([
            html.H3("MCHI Indicator → HTC Segment Crosswalk", style={"color": INK, "fontSize": "16px"}),
            html.P(["Each MCHI code maps to one ", gl("HTC"), " segment."],
                   style={"color": MUTED, "fontSize": "13px"}),
            dash_table.DataTable(
                data=CROSSWALK_DF,
                columns=[{"name": c, "id": c} for c in ["HTC Segment", "Characteristic", "MCHI Variable", "Description"]],
                style_cell={"textAlign": "left", "padding": "8px", "fontSize": "13px",
                            "backgroundColor": SURFACE, "color": INK_SECONDARY,
                            "border": f"1px solid {BORDER}",
                            "whiteSpace": "normal", "height": "auto"},
                style_cell_conditional=[
                    {"if": {"column_id": "MCHI Variable"}, "fontFamily": MONO, "color": ACCENT_OVERVIEW},
                ],
                style_data_conditional=[
                    {"if": {"filter_query": f'{{HTC Segment}} = "{seg}"'},
                     "backgroundColor": SEGMENT_TINT[seg],
                     "borderLeft": f"3px solid {color}"}
                    for seg, color in C.SEGMENT_COLORS.items()
                ],
                style_header={"fontWeight": 600, "color": INK, "backgroundColor": RAISED,
                              "border": f"1px solid {BORDER}",
                              "whiteSpace": "normal", "height": "auto"},
                style_table={"overflowX": "auto"},
                page_size=len(CROSSWALK_DF),
            ),
        ], style=CARD_STYLE),
    ])


# ---------------------------------------------------------------------------
# Tab 2 -- All Segments (population-level views not specific to one
# characteristic; also houses FPAR and FMLI content that applies broadly).
# Split into four groups behind a dropdown, same pattern as the By HTC
# Segment tab, so the tab does not present all 13 charts at once.
# ---------------------------------------------------------------------------
ALL_SEGMENTS_GROUPS = [
    "Characteristics Overview",
    "Completion and Effort Patterns",
    "FPAR: Mode and Conversion Context",
    "FMLI: Demographics",
]
ALL_SEGMENTS_ACCENT = {
    "Characteristics Overview": ACCENT_MCHI,
    "Completion and Effort Patterns": ACCENT_MCHI,
    "FPAR: Mode and Conversion Context": ACCENT_FPAR,
    "FMLI: Demographics": ACCENT_FMLI,
}


def _group_characteristics_overview():
    return html.Div([
        html.Div("MCHI // 2023-2024", style={**EYEBROW_STYLE, "color": ACCENT_MCHI}),
        html.P(data_period_line(["MCHI"]),
               style={"color": MUTED, "fontSize": "12.5px", "margin": "2px 0 10px"}),
        html.Div([
            graph_card(C.fig_segment_prevalence(mchi), "fig-prevalence", sources=["MCHI"]),
            graph_card(C.fig_segment_clustering(mchi), sources=["MCHI"]),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        html.Div([
            graph_card(C.fig_cooccurrence_heatmap(mchi), sources=["MCHI"]),
        ], style={"display": "flex", "flexWrap": "wrap"}),
    ])


def _group_completion_effort():
    return html.Div([
        html.Div([
            html.Div("MCHI // 2023-2024", style={**EYEBROW_STYLE, "color": ACCENT_MCHI}),
            html.P(data_period_line(["MCHI"]),
                   style={"color": MUTED, "fontSize": "12.5px", "margin": "2px 0 8px"}),
            html.Label("Filter by Interview Wave", style={"color": INK_SECONDARY, "fontWeight": 600}),
            html.P(["Interact with the wave selection to see how the completion and effort charts "
                    "directly below change for that portion of the panel. The wave-pattern and "
                    "seasonality charts further down always reflect all ", gl("waves", "wave"), "."],
                   style={"color": MUTED, "fontSize": "12.5px", "margin": "4px 0 8px"}),
            dcc.Checklist(
                id="wave-filter",
                options=[{"label": f" Wave {w}", "value": w} for w in [1, 2, 3, 4]],
                value=[1, 2, 3, 4],
                inline=True,
                className="chip-checklist",
                inputStyle={"marginRight": "8px", "width": "16px", "height": "16px",
                            "verticalAlign": "middle"},
                labelStyle={"display": "inline-flex", "alignItems": "center",
                            "padding": "8px 16px", "marginRight": "10px", "marginTop": "6px",
                            "border": f"1.5px solid {ACCENT_MCHI}", "borderRadius": "20px",
                            "backgroundColor": SURFACE, "color": INK, "fontSize": "14px",
                            "fontWeight": 600, "cursor": "pointer"},
            ),
        ], style=card_style(ACCENT_MCHI)),

        html.Div([
            graph_card(C.fig_completion_by_segment_count(mchi), "fig-completion-count", sources=["MCHI"]),
            graph_card(C.fig_attempts_by_segment_count(mchi), "fig-attempts-count", sources=["MCHI"]),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        html.Div([
            graph_card(C.fig_wave_completion(mchi), sources=["MCHI"]),
            graph_card(C.fig_wave_attempts(mchi), sources=["MCHI"]),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        html.Div([
            graph_card(C.fig_seasonality(mchi), sources=["MCHI"]),
        ], style={"display": "flex", "flexWrap": "wrap"}),
    ])


def _group_fpar_mode():
    return html.Div([
        html.Div([
            html.Div("FPAR // 99.9% COVERAGE // 2023-2024", style={**EYEBROW_STYLE, "color": ACCENT_FPAR}),
            html.P(data_period_line(["FPAR"]),
                   style={"color": MUTED, "fontSize": "12.5px", "margin": "2px 0 8px"}),
            html.P("Covers 36,270 of 36,271 MCHI households, or 99.9%. Not subject to the FMLI "
                   "subset caveat on the FMLI: Demographics group.",
                   style={"color": INK_SECONDARY, "fontSize": "14px", "margin": 0}),
        ], style=card_style(ACCENT_FPAR)),

        html.Div([
            graph_card(C.fig_mode_segments(fpar_household), sources=["FPAR"]),
            graph_card(C.fig_mode_attempts(fpar_household), sources=["FPAR"]),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        html.Div([
            graph_card(C.fig_refusal_conversion(fpar_household), sources=["FPAR"]),
        ], style={"display": "flex", "flexWrap": "wrap"}),

        html.Div([
            html.P([
                "Interview mode above uses ", gl("HOW_INTV"), ", the mode of the wave that "
                "actually completed. It does not use ", gl("TELPV"), ", which records the "
                "attempted mode on waves that did not complete and is populated almost "
                "exclusively on failed waves, so comparing modes using TELPV would conflate "
                "mode with failure to complete.",
            ], style={"color": MUTED, "fontSize": "13px"}),
        ], style=CARD_STYLE),
    ])


def _group_fmli_demographics():
    summary = (
        fmli_household.groupby("tenure_label")
        .agg(households=("CUID", "count"), completion_rate=("completed", "mean"),
             avg_segments=("htc_segment_count", "mean"))
        .reset_index()
    )
    summary["completion_rate"] = (summary["completion_rate"] * 100).round(1)
    summary["avg_segments"] = summary["avg_segments"].round(2)
    summary["households"] = summary["households"].apply(lambda v: f"{v:,}")
    summary.columns = ["Tenure", "Number of Households", "Completion Rate (Percentage)",
                        "Average Number of HTC Characteristics"]

    return html.Div([
        html.Div([
            html.Div("FMLI // 56.2% COVERAGE, SKEWED SUBSET // 2022 Q2-2025 Q1",
                     style={**EYEBROW_STYLE, "color": ACCENT_FMLI}),
            html.P(data_period_line(["FMLI"]),
                   style={"color": MUTED, "fontSize": "12.5px", "margin": "2px 0 8px"}),
            html.P(
                f"Matched subset of n = {N_FMLI:,}, or 56.2% of the MCHI dataset.",
                style={"color": INK_SECONDARY, "margin": 0},
            ),
        ], style=CAVEAT_BANNER),

        html.Div([
            graph_card(C.fig_htc_prevalence_by_completion(fmli_household), sources=["FMLI"]),
            graph_card(C.fig_segment_count_by_completion(fmli_household), sources=["FMLI"]),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),

        html.Div([
            html.H3("Completion Rate and Average Number of HTC Characteristics by Housing Tenure, "
                    "Full FMLI-Matched Subset", style={"color": INK, "fontSize": "16px"}),
            dash_table.DataTable(
                data=summary.to_dict("records"),
                columns=[{"name": c, "id": c} for c in summary.columns],
                style_cell={"textAlign": "left", "padding": "8px", "fontSize": "13px",
                            "backgroundColor": SURFACE, "color": INK_SECONDARY,
                            "border": f"1px solid {BORDER}",
                            "whiteSpace": "normal", "height": "auto"},
                style_header={"fontWeight": 600, "color": INK, "backgroundColor": RAISED,
                              "border": f"1px solid {BORDER}",
                              "whiteSpace": "normal", "height": "auto"},
            ),
            html.P(data_period_line(["FMLI"]),
                   style={"color": MUTED, "fontSize": "11.5px", "marginTop": "6px", "marginBottom": 0}),
        ], style=card_style(ACCENT_FMLI)),

        html.Div([
            html.Label("Demographics of the HTC-Flagged and Completed Subgroup",
                       style={"color": INK_SECONDARY, "fontWeight": 600}),
            html.P("Select a dimension to see the composition of this specific group: "
                   "households that were both HTC-flagged and completed.",
                   style={"color": MUTED, "fontSize": "12.5px", "margin": "4px 0 8px"}),
            dcc.Dropdown(
                id="fmli-dimension",
                options=[{"label": k, "value": k} for k in C.DIMENSIONS],
                value="Tenure",
                clearable=False,
                style={"marginTop": "6px", "maxWidth": "320px"},
                className="htc-dropdown",
            ),
        ], style=card_style(ACCENT_FMLI)),

        html.Div([
            graph_card(C.fig_subgroup_composition(fmli_household, "Tenure"), "fig-subgroup", sources=["FMLI"]),
        ], style={"display": "flex", "flexWrap": "wrap"}),
    ])


ALL_SEGMENTS_BUILDERS = {
    "Characteristics Overview": _group_characteristics_overview,
    "Completion and Effort Patterns": _group_completion_effort,
    "FPAR: Mode and Conversion Context": _group_fpar_mode,
    "FMLI: Demographics": _group_fmli_demographics,
}


def build_all_segments_group(group_name):
    builder = ALL_SEGMENTS_BUILDERS.get(group_name, _group_characteristics_overview)
    return builder()


def all_segments_tab():
    return html.Div([
        html.Div([
            html.Div("ALL SEGMENTS // POPULATION-LEVEL VIEWS", style={**EYEBROW_STYLE, "color": ACCENT_MCHI}),
            html.Label("Select a Group of Charts", style={"color": INK_SECONDARY, "fontWeight": 600}),
            dcc.Dropdown(
                id="all-segments-group-select",
                options=[{"label": g, "value": g} for g in ALL_SEGMENTS_GROUPS],
                value="Characteristics Overview",
                clearable=False,
                style={"marginTop": "6px", "maxWidth": "420px"},
            ),
        ], style=CARD_STYLE),
        html.Div(id="all-segments-group-content",
                 children=build_all_segments_group("Characteristics Overview")),
    ])


@dash.callback(Output("all-segments-group-content", "children"),
               Input("all-segments-group-select", "value"))
def update_all_segments_group(group_name):
    return build_all_segments_group(group_name or "Characteristics Overview")


@dash.callback(
    Output("fig-completion-count", "figure"),
    Output("fig-attempts-count", "figure"),
    Input("wave-filter", "value"),
)
def update_wave_filter(waves):
    waves = waves or [1, 2, 3, 4]
    sub = mchi[mchi["max_wave"].isin(waves)]
    return C.fig_completion_by_segment_count(sub), C.fig_attempts_by_segment_count(sub)


@dash.callback(
    Output("fig-subgroup", "figure"),
    Input("fmli-dimension", "value"),
)
def update_fmli_dimension(dimension):
    return C.fig_subgroup_composition(fmli_household, dimension or "Tenure")


# ---------------------------------------------------------------------------
# Tab 3 -- By HTC Segment
# ---------------------------------------------------------------------------
def build_segment_detail(segment_name):
    info = SEGMENT_INFO[segment_name]
    col = info["col"]
    color = info["color"]
    n_flagged = int(mchi[col].sum())
    pct_flagged = n_flagged / len(mchi) * 100

    crosswalk_subset = [
        {"Characteristic": c, "MCHI Variable": v, "Description": d}
        for s, c, v, d in CROSSWALK_ROWS if s == segment_name
    ]

    # Tint background with dark text and a colored border, not solid color
    # with white text -- two of the four segment colors (aqua, yellow) fall
    # well below 4.5:1 contrast for white text at any reasonable size.
    source_badges = html.Div([
        html.Span(src, style={
            "display": "inline-block", "padding": "4px 12px", "marginRight": "8px",
            "borderRadius": "14px", "backgroundColor": SEGMENT_TINT[segment_name],
            "border": f"1.5px solid {color}", "color": INK,
            "fontSize": "12px", "fontWeight": 700, "fontFamily": MONO,
        }) for src in info["sources"]
    ], style={"marginTop": "6px"})

    children = [
        html.Div([
            html.Div(segment_name.upper(), style={**EYEBROW_STYLE, "color": color}),
            html.H2(segment_name, style=SECTION_TITLE),
            html.P(info["description"], style={"color": INK_SECONDARY}),
            html.P(data_period_line(info["sources"]),
                   style={"color": MUTED, "fontSize": "12.5px", "marginTop": "2px", "marginBottom": "8px"}),
            html.Div([
                html.Span("Data Sources: ", style={"color": INK_SECONDARY, "fontWeight": 600, "fontSize": "13px"}),
                source_badges,
            ]),
            html.Ul([
                html.Li([html.B(src + ": ")] + (note if isinstance(note, list) else [note]),
                        style={"color": INK_SECONDARY, "fontSize": "13px", "marginTop": "6px"})
                for src, note in info["source_notes"]
            ], style={"paddingLeft": "18px", "marginTop": "10px"}),
            html.Div([
                stat_tile(f"{pct_flagged:.1f}%", "Of Households Flagged"),
                stat_tile(f"{n_flagged:,}", "Households Flagged"),
            ], style={"display": "flex", "flexWrap": "wrap", "marginTop": "10px"}),
        ], style=card_style(color)),

        html.Div([
            graph_card(C.fig_segment_completion(mchi, col, color, segment_name), sources=["MCHI"]),
            graph_card(C.fig_segment_attempts(mchi, col, color, segment_name), sources=["MCHI"]),
        ], style={"display": "flex", "gap": "16px", "flexWrap": "wrap"}),
    ]

    if segment_name == "Hard to Interview":
        children.append(html.Div([
            graph_card(C.fig_language_breakdown(mchi), sources=["MCHI"]),
        ], style={"display": "flex", "flexWrap": "wrap"}))

    children.append(html.Div([
        html.H3("Crosswalk for This Characteristic", style={"color": INK, "fontSize": "16px"}),
        dash_table.DataTable(
            data=crosswalk_subset,
            columns=[{"name": c, "id": c} for c in ["Characteristic", "MCHI Variable", "Description"]],
            style_cell={"textAlign": "left", "padding": "8px", "fontSize": "13px",
                        "backgroundColor": SURFACE, "color": INK_SECONDARY,
                        "border": f"1px solid {BORDER}"},
            style_cell_conditional=[
                {"if": {"column_id": "MCHI Variable"}, "fontFamily": MONO, "color": color},
            ],
            style_header={"fontWeight": 600, "color": INK, "backgroundColor": RAISED,
                          "border": f"1px solid {BORDER}",
                          "whiteSpace": "normal", "height": "auto"},
            style_table={"overflowX": "auto"},
        ),
    ], style=CARD_STYLE))

    return html.Div(children)


def segment_tab():
    return html.Div([
        html.Div([
            html.Label("Select an HTC Characteristic", style={"color": INK_SECONDARY, "fontWeight": 600}),
            dcc.Dropdown(
                id="segment-select",
                options=[{"label": k, "value": k} for k in SEGMENT_INFO],
                value="Hard to Contact",
                clearable=False,
                style={"marginTop": "6px", "maxWidth": "360px"},
            ),
        ], style=CARD_STYLE),
        html.Div(id="segment-detail", children=build_segment_detail("Hard to Contact")),
    ])


@dash.callback(Output("segment-detail", "children"), Input("segment-select", "value"))
def update_segment_detail(segment_name):
    return build_segment_detail(segment_name or "Hard to Contact")


# ---------------------------------------------------------------------------
# Tab 4 -- Data Quality
# ---------------------------------------------------------------------------
def data_quality_tab():
    return html.Div([
        html.Div("SYSTEM // DATA QUALITY LOG", style={**EYEBROW_STYLE, "color": ACCENT_QUALITY}),
        html.Div([
            html.H3("Data Quality Notes", style={"color": INK, "fontSize": "16px"}),
            html.Ul([
                html.Li([html.B(title + ": ")] + (body if isinstance(body, list) else [body]),
                        style={"color": INK_SECONDARY, "marginBottom": "8px"})
                for title, body in DATA_QUALITY_ITEMS
            ]),
        ], style=card_style(ACCENT_QUALITY)),

        html.Div([
            html.H3("Sources", style={"color": INK, "fontSize": "16px"}),
            html.Div([
                html.P(src, style={"color": INK_SECONDARY, "fontSize": "13px",
                                    "paddingLeft": "24px", "textIndent": "-24px",
                                    "marginBottom": "10px"})
                for src in APA_SOURCES
            ]),
            html.H4("Data Files Used", style={"color": INK, "fontSize": "13px", "marginTop": "12px"}),
            html.Ul([
                html.Li([html.B(name + ": "), desc],
                        style={"color": INK_SECONDARY, "fontSize": "13px", "marginBottom": "8px"})
                for name, desc in DATA_FILES_USED
            ], style={"paddingLeft": "18px"}),
        ], style=card_style(ACCENT_QUALITY)),
    ])


# ---------------------------------------------------------------------------
# App shell: dark navy title bar and flat nav row, light content area below.
# Modeled on the structure of an official .gov site's nav chrome (dark bar,
# rectangular nav items) without reproducing its actual government-notice
# banner or copy; this is an internal tool, not a .gov page.
# ---------------------------------------------------------------------------
NAV_ACCENT = "#1E87E0"  # RL Sky -- pops against the RL Blue navy chrome

TAB_BAR_STYLE = {"backgroundColor": NAV_BG, "borderTop": "1px solid rgba(255,255,255,0.08)"}
TAB_STYLE = {"padding": "15px 20px", "color": NAV_TEXT_MUTED, "border": "none",
             "backgroundColor": NAV_BG, "fontSize": "14px", "fontWeight": 600,
             "textTransform": "uppercase", "letterSpacing": "0.03em"}
TAB_SELECTED_STYLE = {"padding": "15px 20px", "color": NAV_TEXT, "border": "none",
                       "backgroundColor": NAV_BG_ACTIVE, "fontSize": "14px", "fontWeight": 700,
                       "textTransform": "uppercase", "letterSpacing": "0.03em",
                       "borderBottom": f"3px solid {NAV_ACCENT}"}

# Reveal Labs mark, recreated as an inline SVG data URI + wordmark (no
# image asset was provided, only the brand slide) -- matches the
# white-on-dark horizontal variant from that slide, since the nav bar
# itself is already dark. dash.html has no Svg/Circle/Path element
# wrappers in this version, so the icon is built as a raw SVG string and
# embedded via a base64 data URI instead.
import base64

_EYE_SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
<path d="M2.5 12 C2.5 12 7 6.5 12 6.5 C17 6.5 21.5 12 21.5 12 C21.5 12 17 17.5 12 17.5 C7 17.5 2.5 12 2.5 12 Z"
      fill="none" stroke="{NAV_TEXT}" stroke-width="1.6"/>
<circle cx="12" cy="12" r="3" fill="{NAV_ACCENT}"/>
</svg>"""
_EYE_SVG_URI = "data:image/svg+xml;base64," + base64.b64encode(_EYE_SVG.encode()).decode()

REVEAL_LABS_LOGO = html.Div([
    html.Span("Reveal", style={"fontWeight": 700, "color": NAV_TEXT, "fontSize": "16px"}),
    html.Span("Labs", style={"fontWeight": 700, "color": NAV_TEXT, "fontSize": "16px", "marginLeft": "2px"}),
    html.Img(src=_EYE_SVG_URI, style={"width": "16px", "height": "16px",
                                       "marginLeft": "6px", "verticalAlign": "-3px"}),
], style={"textAlign": "right"})

NAVBAR = html.Div([
    html.Div([
        html.Span("●", style={"color": NAV_ACCENT, "marginRight": "10px", "fontSize": "20px"}),
        html.Span("HTC Dashboard", style={"fontFamily": MONO, "fontWeight": 700, "fontSize": "20px",
                                           "letterSpacing": "0.02em", "color": NAV_TEXT}),
    ]),
    html.Div([
        REVEAL_LABS_LOGO,
    ], style={"textAlign": "right"}),
], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center",
          "padding": "16px 24px", "backgroundColor": NAV_BG})

app.layout = html.Div([
    NAVBAR,
    dcc.Tabs(id="tabs", value="overview", parent_style=TAB_BAR_STYLE, children=[
        dcc.Tab(label="Overview and Crosswalk", value="overview", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
        dcc.Tab(label="All Segments", value="all-segments", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
        dcc.Tab(label="By HTC Segment", value="by-segment", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
        dcc.Tab(label="Data Quality", value="quality", style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE),
    ]),
    html.Div(id="tab-content", style={"padding": "20px", "maxWidth": "1200px", "margin": "0 auto"}),
], style={"backgroundColor": PAGE, "minHeight": "100vh",
          "fontFamily": "system-ui, -apple-system, 'Segoe UI', sans-serif"})


@dash.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_tab(tab):
    return {
        "overview": overview_tab,
        "all-segments": all_segments_tab,
        "by-segment": segment_tab,
        "quality": data_quality_tab,
    }[tab]()


if __name__ == "__main__":
    app.run(debug=True)
