import streamlit as st

# =====================================================
# GEOINTELLIGENCE CORE
# =====================================================

def render_intelligence_core(df):

    st.markdown("""
    <div style="
        position:sticky;
        top:20px;
    ">
    """, unsafe_allow_html=True)

    st.markdown("""
    ## 🧠 GeoIntelligence Core
    """)

    st.markdown("---")

    # =============================================
    # ENGINE STATUS
    # =============================================

    st.markdown("### ⚡ Engine Status")

    st.success("ML Engine Online")

    st.success("News Engine Active")

    st.success("Fusion Engine Active")

    st.success("AI Analyst Running")

    st.markdown("---")

    # =============================================
    # MODEL FLOW
    # =============================================

    st.markdown("### 🔄 Prediction Flow")

    st.markdown("""

    NewsAPI  
    ↓  
    Keyword Intelligence  
    ↓  
    Random Forest Model  
    ↓  
    Fusion Engine  
    ↓  
    GeoRisk Live Score  
    ↓  
    AI Briefing System  

    """)

    st.markdown("---")

    # =============================================
    # RISK FORMULA
    # =============================================

    st.markdown("### 📐 Risk Formula")

    st.code("""

GeoRisk Score =

0.45 × ML Score
+ 0.35 × News Score
+ 0.20 × Conflict Probability

    """)

    # =============================================
    # LIVE THREAT SIGNALS
    # =============================================

    st.markdown("### 🚨 Threat Signals")

    st.markdown("""

- war
- missile
- sanctions
- military
- terrorism
- border conflict
- nuclear escalation

    """)

    st.markdown("---")

    # =============================================
    # AI CONFIDENCE
    # =============================================

    st.markdown("### 🧠 AI Confidence")

    avg_score = round(
        df["GeoRisk_Live_Score"]
        .mean() * 100,
        1
    )

    st.metric(
        "System Confidence",
        f"{avg_score}%"
    )

    # =============================================
    # LIVE MONITORING
    # =============================================

    st.markdown("### 🌍 Monitoring")

    st.metric(
        "Countries Tracked",
        len(df)
    )

    critical_count = int(

        (
            df[
                "Dynamic_Risk_Level"
            ] == "Critical"
        ).sum()
    )

    st.metric(
        "Critical Alerts",
        critical_count
    )

    st.markdown("---")

    st.caption(
        "GeoRiskAI Intelligence Core • "
        "Real-Time Geopolitical Monitoring"
    )

    st.markdown("</div>", unsafe_allow_html=True)