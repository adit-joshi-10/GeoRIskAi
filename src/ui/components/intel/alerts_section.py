import streamlit as st

from src.intelligence.strategic_alerts import (
    get_strategic_alert
)

# =====================================================
# HELPERS
# =====================================================

def _msec(title, icon):

    return f"""
<div style="
margin-top:18px;
margin-bottom:10px;
padding-bottom:8px;
border-bottom:1px solid rgba(0,255,255,0.08);
">

<div style="
font-size:10px;
letter-spacing:5px;
color:#3a6070;
text-transform:uppercase;
font-family:monospace;
">
{icon} {title}
</div>

</div>
"""

def _abox(title, body, border):

    return f"""
<div style="
padding:18px;
border-radius:16px;
background:
linear-gradient(
180deg,
rgba(25,0,0,0.45),
rgba(8,0,0,0.85)
);
border:1px solid {border};
margin-bottom:16px;
">

<div style="
font-size:10px;
letter-spacing:3px;
font-family:monospace;
margin-bottom:14px;
color:#ff4d6d;
text-transform:uppercase;
">
{title}
</div>

<div style="
font-size:15px;
line-height:1.8;
color:#d7f7ff;
">
{body}
</div>

</div>
"""

# =====================================================
# ALERTS SECTION
# =====================================================

def render_alerts_section(

    country

):

    alert = get_strategic_alert(
        country
    )

    # =================================================
    # STRATEGIC ALERT
    # =================================================

    st.markdown(
        _msec(
            "Strategic Escalation Alerts",
            "🚨"
        ),
        unsafe_allow_html=True
    )

    st.markdown(

        _abox(

            alert["title"],

            alert["message"],

            "rgba(255,60,90,0.18)"
        ),

        unsafe_allow_html=True
    )

    # =================================================
    # INVESTOR ACTION
    # =================================================

    st.markdown(
        _msec(
            "Institutional Response Guidance",
            "🧠"
        ),
        unsafe_allow_html=True
    )

    st.markdown(

        f"""
<div style="
padding:16px;
border-left:3px solid #00e5ff;
background:rgba(0,255,255,0.04);
border-radius:10px;
margin-bottom:18px;
font-size:14px;
line-height:1.8;
color:#d7f7ff;
">

<b style="color:white">
Suggested Institutional Action:
</b>

<br><br>

{alert["action"]}

</div>
""",

        unsafe_allow_html=True
    )

    # =================================================
    # ESCALATION PRESSURE
    # =================================================

    st.markdown(
        _msec(
            "Escalation Pressure",
            "📉"
        ),
        unsafe_allow_html=True
    )

    pressure_map = {

        "Iran": 91,
        "Taiwan": 84,
        "Russia": 87,
        "Israel": 82,
        "China": 73,
        "India": 51
    }

    pressure = pressure_map.get(
        country,
        55
    )

    st.progress(
        pressure / 100
    )

    st.markdown(

        f"""
<div style="
padding:14px;
margin-top:10px;
border-radius:10px;
background:rgba(255,60,90,0.04);
border:1px solid rgba(255,60,90,0.08);
font-size:14px;
line-height:1.7;
color:#ff9fb0;
">
Escalation pressure elevated to
<b style="color:white">{pressure}%</b>
across geopolitical conflict transmission channels.
</div>
""",

        unsafe_allow_html=True
    )

    # =================================================
    # REGIONAL CASCADE RISK
    # =================================================

    st.markdown(
        _msec(
            "Regional Cascade Exposure",
            "🌍"
        ),
        unsafe_allow_html=True
    )

    cascade_map = {

        "Iran": [
            "Middle East Oil Routes",
            "Global Inflation Channels",
            "Shipping Insurance Markets",
            "Commodity Volatility"
        ],

        "Taiwan": [
            "AI Infrastructure",
            "Global Semiconductor Supply",
            "Asian Manufacturing Chains",
            "Tech Export Stability"
        ],

        "Russia": [
            "European Energy Stability",
            "Commodity Markets",
            "NATO Supply Chains",
            "Industrial Production"
        ],

        "Israel": [
            "Regional Military Stability",
            "Oil Markets",
            "Defense Sector",
            "Cybersecurity Demand"
        ],

        "India": [
            "South Asian Stability",
            "Energy Imports",
            "Manufacturing Expansion",
            "Infrastructure Growth"
        ]
    }

    exposures = cascade_map.get(
        country,
        ["Regional Markets"]
    )

    html = ""

    for item in exposures:

        html += f"""
<div style="
padding:10px 0;
border-bottom:1px solid rgba(255,255,255,0.03);
font-size:15px;
color:#d7f7ff;
">
• {item}
</div>
"""

    st.markdown(

        _abox(

            "Cascade Risk Network",

            html,

            "rgba(255,60,90,0.12)"
        ),

        unsafe_allow_html=True
    )