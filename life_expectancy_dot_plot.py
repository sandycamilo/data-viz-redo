"""
Interactive ranked dot plot: life expectancy in U.S. states vs. other countries.
Redesign of the NYT chart "Life Expectancy in U.S. States and Select Countries" (Kristof, 2023).

Requirements:  pip install pandas plotly
Run:           python life_expectancy_dot_plot.py
Output:        life_expectancy_dot_plot.html  (open in a browser and hover over any line or dot)
"""
import pandas as pd
import plotly.graph_objects as go

# ---- 1. Load the data (CSV must be in the same folder as this script) ----
df = pd.read_csv("life_expectancy_states_countries.csv")

GROUPS = ["Wealthy country", "U.S. state", "Other country"]
COLORS = {"Wealthy country": "#2A78D6", "U.S. state": "#D85A30", "Other country": "#A8A69E"}
AXIS_START = 70

# Publication-style fonts: serif headline, clean sans-serif for everything else.
# (Loaded from Google Fonts in the HTML; the fallbacks are used if they can't load.)
SERIF = "'Source Serif 4', Georgia, 'Times New Roman', serif"
SANS = "'Source Sans 3', 'Helvetica Neue', Arial, sans-serif"
INK, MUTED, FAINT = "#1F1F1F", "#5F5E5A", "#8A8983"
WEALTHY_AVG = df.loc[df.group == "Wealthy country", "life_expectancy_est"].mean()
LOWEST_WEALTHY = df.loc[df.group == "Wealthy country", "life_expectancy_est"].min()

# Overall rank (1 = longest life expectancy) for the hover text
df["rank"] = df["life_expectancy_est"].rank(ascending=False, method="min").astype(int)

# ---- 2. Rank every place from highest (top) to lowest (bottom) in one list ----
df = df.sort_values("life_expectancy_est", ascending=True).reset_index(drop=True)
df["y"] = range(1, len(df) + 1)

# ---- 3. Build the chart: one trace of stems + one trace of dots per group (colors = legend) ----
fig = go.Figure()
for g in GROUPS:
    sub = df[df.group == g]
    hover = [
        f"<b>{r['name']}</b><br>"
        f"{r['group']}<br>"
        f"Life expectancy: <b>{r['life_expectancy_est']:.1f} years</b><br>"
        f"{r['years_vs_wealthy_avg']:+.1f} years vs. wealthy-country avg ({WEALTHY_AVG:.1f})<br>"
        f"Rank: {r['rank']} of {len(df)}<br>"
        f"Birth year of data: {r['birth_year']}"
        for _, r in sub.iterrows()
    ]

    # Stems (the "lollipop" lines) - drawn as one trace with gaps (None) between lines
    xs, ys, hs = [], [], []
    for (_, r), h in zip(sub.iterrows(), hover):
        xs += [AXIS_START, r["life_expectancy_est"], None]
        ys += [r["y"], r["y"], None]
        hs += [h, h, None]
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="lines", line=dict(color=COLORS[g], width=2), opacity=0.35,
        hovertext=hs, hoverinfo="text", showlegend=False))

    # Dots
    fig.add_trace(go.Scatter(
        x=sub["life_expectancy_est"], y=sub["y"], mode="markers", name=g,
        marker=dict(color=COLORS[g], size=9), hovertext=hover, hoverinfo="text",
        showlegend=True))

# Shaded band showing the range of wealthy countries (lowest = Germany, highest = Japan)
HIGHEST_WEALTHY = df.loc[df.group == "Wealthy country", "life_expectancy_est"].max()
fig.add_vrect(x0=LOWEST_WEALTHY, x1=HIGHEST_WEALTHY, fillcolor=COLORS["Wealthy country"],
              opacity=0.08, line_width=0, layer="below")
fig.add_vline(x=LOWEST_WEALTHY, line=dict(color=COLORS["Wealthy country"], dash="dot", width=1.5))
fig.add_annotation(x=(LOWEST_WEALTHY + HIGHEST_WEALTHY) / 2, y=df["y"].max() + 1.2, yanchor="bottom",
                   text=f"<b>Wealthy-country range</b><br>{LOWEST_WEALTHY}–{HIGHEST_WEALTHY} years",
                   showarrow=False, xanchor="center", align="center",
                   font=dict(size=13, color=COLORS["Wealthy country"]))
# Callout right beside Hawaii (the top U.S. state), extending down into the empty part of the band
HAWAII = df.loc[df.name == "Hawaii"].iloc[0]
fig.add_annotation(x=LOWEST_WEALTHY, y=HAWAII["y"] + 0.45, xanchor="left", yanchor="top", xshift=14,
                   text=(f"\u2190 <b>Hawaii</b>, the top U.S. state ({HAWAII['life_expectancy_est']}),<br>"
                         "only ties the lowest wealthy country.<br>The other 49 states fall below it."),
                   showarrow=False, align="left", font=dict(size=13, color=COLORS["U.S. state"]))

# ---- 4. Layout ----
# Equal left/right margins keep the plot centered under the centered title.
# TOP is the space reserved above the chart for the title and subtitle; increase it if they ever overlap.
SIDE, TOP, HEIGHT = 150, 200, 1850
fig.update_layout(
    font=dict(family=SANS, color=INK),
    title=dict(
        text="<b>Despite being one of the richest countries in the world, almost every<br>"
             "U.S. state has a lower life expectancy than its wealthy peers</b>",
        font=dict(family=SERIF, size=26, color=INK),
        subtitle=dict(
            text="Life expectancy at birth, in years. The shaded band shows the range of wealthy countries. "
                 "Most U.S. states<br>rank alongside middle-income countries like Thailand, Poland, and Turkey. "
                 "Hover over any line for details.",
            font=dict(family=SANS, size=15, color=MUTED)),
        x=0.5, xanchor="center", xref="container",
        y=1 - 36 / HEIGHT, yanchor="top", yref="container"),
    height=HEIGHT, width=1000,
    margin=dict(l=SIDE, r=SIDE, t=TOP, b=120),
    plot_bgcolor="white", paper_bgcolor="white",
    hoverlabel=dict(bgcolor="white", font=dict(family=SANS, size=14), bordercolor="#CCC"),
    legend=dict(x=1.02, y=1, xanchor="left", yanchor="top", bgcolor="white",   # in the right margin, top
                bordercolor="#DDD", borderwidth=1, font=dict(size=14),
                title=dict(text="<b>Color key</b>", font=dict(size=14))),
    xaxis=dict(range=[AXIS_START, 86], dtick=2, showgrid=False, zeroline=False,
               title=None, side="top", tickfont=dict(size=13, color=MUTED),
               ticks="outside", tickcolor="#BBB", linecolor="#BBB", showline=True),
    yaxis=dict(tickmode="array", tickvals=df["y"], ticktext=df["name"],
               tickfont=dict(size=13, color="#3D3D3A"), showgrid=False, zeroline=False,
               range=[0, df["y"].max() + 4], ticklabelstandoff=8),
)
fig.add_annotation(
    text=("Sources: National Center for Health Statistics; United Nations. U.S. data are for people born in 2020, "
          "international data for 2021.<br>Values estimated from N. Kristof, \"How Do We Fix the Scandal That Is "
          "American Health Care?\" The New York Times, Aug. 16, 2023."),
    xref="paper", yref="paper", x=0.5, y=0, xanchor="center", yanchor="top", yshift=-30,
    showarrow=False, align="center", font=dict(size=12, color=FAINT))

# ---- 5. Save ----
fig.write_html("life_expectancy_dot_plot.html", include_plotlyjs="cdn",
               config={"modeBarButtons": [["toImage"]],   # only the camera (download PNG) button
                       "displaylogo": False,
                       "toImageButtonOptions": {"format": "png", "scale": 2,
                                                "filename": "life_expectancy_dot_plot"}})

# Load the web fonts and center the chart on the page
FONT_HEAD = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600'
    '&family=Source+Serif+4:wght@600;700&display=swap" rel="stylesheet">'
    '<meta name="viewport" content="width=device-width, initial-scale=1">'
    '<title>U.S. life expectancy vs. the world</title>'
    '<style>body{margin:0;padding:24px 0;background:#fff;display:flex;justify-content:center;}</style>'
)
with open("life_expectancy_dot_plot.html", encoding="utf-8") as f:
    html = f.read()
html = html.replace("<head>", "<head>" + FONT_HEAD, 1)
with open("life_expectancy_dot_plot.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Saved life_expectancy_dot_plot.html - open it in a browser.")