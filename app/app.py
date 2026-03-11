import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="lessthannothing",
    page_icon="▮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styling ───────────────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Unbounded:wght@300;400;700;900&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0a0a0a;
    color: #e8e4dc;
  }

  .block-container {
    padding: 4rem 6rem 4rem 6rem;
    max-width: 1400px;
  }

  h1, h2, h3 {
    font-family: 'Unbounded', sans-serif;
    letter-spacing: -0.03em;
  }

  .header-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c8f000;
    margin-bottom: 0.5rem;
  }

  .main-title {
    font-family: 'Unbounded', sans-serif;
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 900;
    line-height: 0.95;
    letter-spacing: -0.04em;
    color: #e8e4dc;
    margin-bottom: 1.5rem;
  }

  .subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    color: #888;
    line-height: 1.7;
    max-width: 560px;
    margin-bottom: 3rem;
  }

  .divider {
    border: none;
    border-top: 1px solid #222;
    margin: 3rem 0;
  }

  .stat-block {
    border-left: 2px solid #c8f000;
    padding-left: 1.2rem;
    margin-bottom: 2rem;
  }

  .stat-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 0.25rem;
  }

  .stat-value {
    font-family: 'Unbounded', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: #e8e4dc;
    line-height: 1;
  }

  .stat-sub {
    font-size: 0.7rem;
    color: #555;
    margin-top: 0.25rem;
  }

  .section-label {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 1rem;
  }

  .footnote {
    font-size: 0.65rem;
    color: #444;
    margin-top: 1rem;
    line-height: 1.6;
  }

  /* Hide streamlit branding */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────

@st.cache_data
def load_gini():
    return pd.read_parquet("data/core/fact_gini.parquet")

df = load_gini()

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown('<div class="header-eyebrow">Deutschland — Vermögensungleichheit</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">less than<br>nothing</div>', unsafe_allow_html=True)
st.markdown("""
<div class="subtitle">
  Germany presents itself as a social market economy — fair, stable, and middle-class.
  The data tells a different story. This is what the structure looks like.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Key stats row ─────────────────────────────────────────────────────────────

latest_year = df["year"].max()
latest_value = df[df["year"] == latest_year]["value"].values[0]
earliest_year = df["year"].min()
earliest_value = df[df["year"] == earliest_year]["value"].values[0]
delta = latest_value - earliest_value
delta_str = f"+{delta:.1f}" if delta > 0 else f"{delta:.1f}"

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-block">
      <div class="stat-label">Gini — {latest_year}</div>
      <div class="stat-value">{latest_value:.1f}</div>
      <div class="stat-sub">coefficient of income inequality</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-block">
      <div class="stat-label">Change since {earliest_year}</div>
      <div class="stat-value">{delta_str}</div>
      <div class="stat-sub">points over {latest_year - earliest_year} years</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-block">
      <div class="stat-label">Scale</div>
      <div class="stat-value">0 — 100</div>
      <div class="stat-sub">0 = perfect equality / 100 = one person owns everything</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Chart ─────────────────────────────────────────────────────────────────────

st.markdown('<div class="section-label">01 — Gini coefficient over time</div>', unsafe_allow_html=True)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["year"],
    y=df["value"],
    mode="lines+markers",
    line=dict(color="#c8f000", width=2),
    marker=dict(color="#c8f000", size=5),
    hovertemplate="<b>%{x}</b><br>Gini: %{y:.1f}<extra></extra>",
))

fig.update_layout(
    paper_bgcolor="#0a0a0a",
    plot_bgcolor="#0a0a0a",
    font=dict(family="DM Mono, monospace", color="#888", size=11),
    margin=dict(l=0, r=0, t=20, b=0),
    height=380,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickcolor="#333",
        linecolor="#222",
        tickfont=dict(color="#555"),
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#1a1a1a",
        zeroline=False,
        tickcolor="#333",
        linecolor="#222",
        tickfont=dict(color="#555"),
        range=[
            df["value"].min() - 1,
            df["value"].max() + 1
        ],
    ),
    hoverlabel=dict(
        bgcolor="#111",
        bordercolor="#333",
        font=dict(family="DM Mono, monospace", color="#e8e4dc"),
    ),
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="footnote">
  Source: Eurostat, ilc_di12 — Gini coefficient of equivalised disposable income (after taxes and transfers).
  Measured at household level. A higher number means greater inequality.
</div>
""", unsafe_allow_html=True)