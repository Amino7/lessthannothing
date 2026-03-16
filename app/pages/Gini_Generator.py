import streamlit as st
import plotly.graph_objects as go
import numpy as np

def gini_to_distribution(gini: float, n: int = 10) -> np.ndarray:
    """
    Generate a randomised wealth distribution approximating the target Gini.
    Different each call — same structure, different specific numbers.
    Guarantees all shares > 0.
    """
    g = gini / 100.0

    if g < 0.01:
        shares = np.ones(n) + np.random.uniform(-0.05, 0.05, n)
    else:
        exponent = 1 + (g ** 2) * 15
        base = np.array([(i / n) ** exponent for i in range(1, n + 1)])
        noise = np.random.uniform(0.7, 1.3, n)
        raw = base * noise
        shares = raw / raw.sum()

    # Ensure strictly positive and renormalise
    eps = 1e-6
    shares = np.clip(shares, eps, None)
    shares = shares / shares.sum()

    return np.sort(shares)


def render_gini_explainer():
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">03 — Was bedeutet ein Gini-Wert?</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="subtitle" style="margin-bottom: 1.5rem;">
        Stell dir 10 Menschen vor, die zusammen €1.000.000 besitzen.
        Wie verteilt sich das Vermögen — abhängig vom Gini-Koeffizienten?
    </div>
    """, unsafe_allow_html=True)

    # ── Slider ────────────────────────────────────────────────────────────────

    gini_value = st.slider(
        label="Gini-Koeffizient",
        min_value=0,
        max_value=100,
        value=73,
        step=1,
        help="0 = vollständige Gleichheit / 100 = eine Person besitzt alles"
    )


    col_btn, _ = st.columns([1, 4])
    with col_btn:
        st.button("↻ neu würfeln", key="randomize")

    # ── Compute distribution ──────────────────────────────────────────────────

    total_wealth = 1_000_000
    shares = gini_to_distribution(gini_value)

    # Scale to integers
    wealth = (shares * total_wealth).astype(int)

    # Ensure everyone has at least 1
    zeros = wealth == 0
    extra_needed = int(zeros.sum())

    if extra_needed > 0:
        wealth[zeros] = 1
        # take the extra from the richest person
        wealth[-1] -= extra_needed

    # Final fix so it sums exactly to total_wealth
    wealth[-1] += total_wealth - wealth.sum()

    persons = [f"Person {i+1}" for i in range(10)]
    colors = ["#c8f000" if i == 9 else "#2a2a2a" for i in range(10)]
    border_colors = ["#c8f000" if i == 9 else "#444" for i in range(10)]

    # ── Key stats ─────────────────────────────────────────────────────────────

    top1_share = wealth[-1] / total_wealth * 100
    bottom5_share = wealth[:5].sum() / total_wealth * 100
    richest = wealth[-1]
    poorest = wealth[0]
    ratio = f"{richest / poorest:.0f}x" if poorest > 0 else "∞"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-block">
          <div class="stat-label">Reichste Person</div>
          <div class="stat-value" style="font-size:1.8rem">€{richest:,.0f}</div>
          <div class="stat-sub">{top1_share:.1f}% des Gesamtvermögens</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-block">
          <div class="stat-label">Untere 5 Personen (untere 50%)</div>
          <div class="stat-value" style="font-size:1.8rem">{bottom5_share:.1f}%</div>
          <div class="stat-sub">€{wealth[:5].sum():,.0f} zusammen</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-block">
          <div class="stat-label">Verhältnis Reich / Arm</div>
          <div class="stat-value" style="font-size:1.8rem">{ratio}</div>
          <div class="stat-sub">Reichste zu ärmster Person</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Bar chart ─────────────────────────────────────────────────────────────

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=persons,
        y=wealth,
        marker=dict(
            color=colors,
            line=dict(color=border_colors, width=1),
        ),
        hovertemplate="<b>%{x}</b><br>Vermögen: €%{y:,.0f}<extra></extra>",
        text=[f"€{w:,.0f}" for w in wealth],
        textposition="outside",
        textfont=dict(color="#666", size=10, family="DM Mono, monospace"),
    ))

    fig.update_layout(
        paper_bgcolor="#0a0a0a",
        plot_bgcolor="#0a0a0a",
        font=dict(family="DM Mono, monospace", color="#888", size=11),
        margin=dict(l=0, r=0, t=20, b=0),
        height=340,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="#555"),
            linecolor="#222",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1a1a1a",
            zeroline=False,
            tickfont=dict(color="#555"),
            tickprefix="€",
            tickformat=",.0f",
        ),
        hoverlabel=dict(
            bgcolor="#111",
            bordercolor="#333",
            font=dict(family="DM Mono, monospace", color="#e8e4dc"),
        ),
        bargap=0.3,
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Contextual annotation ─────────────────────────────────────────────────

    if gini_value <= 15:
        note = "Eine weitgehend gleiche Gesellschaft. Existiert nirgendwo in der realen Welt."
    elif gini_value <= 30:
        note = "Skandinavisches Modell. Hohe Umverteilung, starker Sozialstaat."
    elif gini_value <= 40:
        note = "Deutschlands offizieller Gini für Einkommensungleichheit nach Umverteilung (~31)."
    elif gini_value <= 55:
        note = "Ungefähr Deutschlands Einkommens-Gini vor Steuern und Transfers — was der Markt produziert, bevor der Staat eingreift."
    elif gini_value <= 70:
        note = "Annäherung an Deutschlands Vermögens-Gini wenn Pensionsansprüche eingerechnet werden (~58)."
    else:
        note = f"Deutschlands realer Vermögens-Gini liegt bei ~73. Du siehst gerade die Struktur."

    st.markdown(f"""
    <div class="footnote" style="color: #c8f000; border-left: 2px solid #c8f000; padding-left: 1rem; margin-top: 0.5rem;">
        {note}
    </div>
    """, unsafe_allow_html=True)

render_gini_explainer()