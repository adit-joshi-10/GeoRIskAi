import streamlit as st

from src.intelligence.macro_themes import (
    get_macro_themes
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

def _macrobox(title, body):

    return f"""
<div style="
padding:18px;
border-radius:16px;
background:
linear-gradient(
180deg,
rgba(0,18,35,0.50),
rgba(0,5,15,0.90)
);
border:1px solid rgba(0,255,255,0.08);
margin-bottom:16px;
">

<div style="
font-size:10px;
letter-spacing:3px;
font-family:monospace;
margin-bottom:14px;
color:#00e5ff;
text-transform:uppercase;
">
{title}
</div>

<div style="
font-size:15px;
line-height:1.9;
color:#d7f7ff;
">
{body}
</div>

</div>
"""

# =====================================================
# MACRO SECTION
# =====================================================

def render_macro_section(

    country

):

    themes = get_macro_themes(
        country
    )

    # =================================================
    # STRATEGIC THEMES
    # =================================================

    st.markdown(
        _msec(
            "Strategic Macro Themes",
            "🌐"
        ),
        unsafe_allow_html=True
    )

    for idx, theme in enumerate(

        themes,

        start=1

    ):

        st.markdown(

            _macrobox(

                f"{idx}. {theme['theme']}",

                theme["description"]
            ),

            unsafe_allow_html=True
        )

    # =================================================
    # SYSTEMIC TRANSMISSION
    # =================================================

    st.markdown(
        _msec(
            "Systemic Economic Transmission",
            "📡"
        ),
        unsafe_allow_html=True
    )

    transmission_map = {

        "Iran": [
            "Global inflation acceleration through oil volatility.",
            "Commodity-sensitive economies exposed to pricing shocks.",
            "Shipping and insurance markets pricing geopolitical risk."
        ],

        "Taiwan": [
            "AI infrastructure dependency pressure intensifying.",
            "Global semiconductor concentration risk elevated.",
            "Technology supply-chain fragmentation expanding."
        ],

        "Russia": [
            "European energy restructuring pressures increasing.",
            "Commodity dependency reshaping industrial pricing.",
            "Long-term sanctions altering capital allocation patterns."
        ],

        "Israel": [
            "Defense and cybersecurity investment accelerating.",
            "Regional military tensions influencing oil markets.",
            "Cross-border geopolitical sensitivity increasing."
        ],

        "India": [
            "Emerging-market manufacturing rotation strengthening.",
            "Infrastructure-led domestic growth remaining resilient.",
            "Global diversification trends supporting industrial expansion."
        ]
    }

    transmissions = transmission_map.get(

        country,

        [
            "Regional geopolitical sensitivity affecting capital markets."
        ]
    )

    html = ""

    for item in transmissions:

        html += f"""
<div style="
padding:10px 0;
border-bottom:1px solid rgba(255,255,255,0.03);
font-size:15px;
line-height:1.8;
color:#d7f7ff;
">
• {item}
</div>
"""

    st.markdown(

        _macrobox(

            "Macro Transmission Channels",

            html
        ),

        unsafe_allow_html=True
    )

    # =================================================
    # MARKET SENSITIVITY
    # =================================================

    st.markdown(
        _msec(
            "Market Sensitivity Matrix",
            "📉"
        ),
        unsafe_allow_html=True
    )

    sensitivity_map = {

        "Iran": 89,
        "Taiwan": 86,
        "Russia": 81,
        "Israel": 77,
        "China": 73,
        "India": 52
    }

    sensitivity = sensitivity_map.get(
        country,
        55
    )

    st.progress(
        sensitivity / 100
    )

    st.markdown(

        f"""
<div style="
padding:14px;
margin-top:10px;
border-radius:10px;
background:rgba(0,255,255,0.03);
border:1px solid rgba(0,255,255,0.05);
font-size:14px;
line-height:1.7;
color:#7a9db0;
">
Institutional market sensitivity elevated to
<b style="color:white">{sensitivity}%</b>
across macroeconomic transmission networks.
</div>
""",

        unsafe_allow_html=True
    )

    # =================================================
    # STRATEGIC DEPENDENCIES
    # =================================================

    st.markdown(
        _msec(
            "Strategic Dependency Network",
            "🔗"
        ),
        unsafe_allow_html=True
    )

    dependency_map = {

        "Iran": [
            "Oil Supply Chains",
            "Hormuz Shipping Corridor",
            "Commodity Inflation",
            "Energy Imports"
        ],

        "Taiwan": [
            "AI Chips",
            "Semiconductor Manufacturing",
            "Cloud Infrastructure",
            "Global Hardware Supply"
        ],

        "Russia": [
            "Natural Gas",
            "European Energy",
            "Commodity Exports",
            "Industrial Fuel Pricing"
        ],

        "Israel": [
            "Cybersecurity",
            "Defense Technology",
            "Military Infrastructure",
            "Regional Stability"
        ],

        "India": [
            "Infrastructure Growth",
            "Industrial Manufacturing",
            "Energy Imports",
            "Domestic Expansion"
        ]
    }

    dependencies = dependency_map.get(
        country,
        ["Regional Economic Stability"]
    )

    html = ""

    for item in dependencies:

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

        _macrobox(

            "Dependency Exposure Matrix",

            html
        ),

        unsafe_allow_html=True
    )