import streamlit as st

from src.intelligence.conviction_engine import (
    get_conviction_score
)

# =====================================================
# CONVICTION INTELLIGENCE SECTION
# =====================================================

def render_conviction_section(

    country,

    score,

    news,

    conflict_prob

):

    st.markdown(
        "## 🧠 AI Conviction Intelligence"
    )

    # =================================================
    # CONVICTION ENGINE
    # =================================================

    conviction = get_conviction_score(

        score,

        news,

        conflict_prob,

        country
    )

    # =================================================
    # MAIN SCORE
    # =================================================

    c1, c2 = st.columns([1, 2])

    with c1:

        st.metric(

            conviction["level"],

            f"{conviction['score']}%"
        )

    with c2:

        st.progress(
            conviction["score"] / 100
        )

        st.caption(
            conviction["description"]
        )

    st.markdown("---")

    # =================================================
    # BREAKDOWN
    # =================================================

    st.markdown(
        "### 📊 Signal Breakdown"
    )

    breakdown = conviction.get(
        "breakdown",
        {}
    )

    for key, value in breakdown.items():

        st.markdown(
            f"**{key}** — {value}"
        )