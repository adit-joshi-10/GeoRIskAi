import streamlit as st

from src.intelligence.investor_actions import (
    get_investor_actions
)

from src.intelligence.portfolio_engine import (
    get_portfolio_signals
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

def _ibox(title, body, border):

    return f"""
<div style="
padding:16px;
border-radius:16px;
background:
linear-gradient(
180deg,
rgba(0,18,35,0.55),
rgba(0,5,15,0.88)
);
border:1px solid {border};
min-height:220px;
">

<div style="
font-size:10px;
letter-spacing:3px;
font-family:monospace;
margin-bottom:18px;
color:#00e5ff;
text-transform:uppercase;
">
{title}
</div>

{body}

</div>
"""

def _rows(items, positive=True):

    html = ""

    arrow = "▲" if positive else "▼"

    color = "#00ffae" if positive else "#ff4d6d"

    for item in items:

        html += f"""
<div style="
padding:10px 0;
border-bottom:1px solid rgba(255,255,255,0.03);
font-size:15px;
color:{color};
">
{arrow} {item}
</div>
"""

    return html

# =====================================================
# POSITIONING SECTION
# =====================================================

def render_positioning_section(

    country,

    risk

):

    # =================================================
    # PORTFOLIO ENGINE
    # =================================================

    portfolio = get_portfolio_signals(
        risk
    )

    st.markdown(
        _msec(
            "Portfolio Risk Allocation",
            "🧠"
        ),
        unsafe_allow_html=True
    )

    p1, p2 = st.columns(2)

    with p1:

        st.markdown(

            _ibox(

                "Safe Haven Assets",

                _rows(
                    portfolio.get(
                        "safe",
                        []
                    ),
                    True
                ),

                "rgba(0,255,180,0.14)"
            ),

            unsafe_allow_html=True
        )

    with p2:

        st.markdown(

            _ibox(

                "High Risk Exposure",

                _rows(
                    portfolio.get(
                        "risk",
                        []
                    ),
                    False
                ),

                "rgba(255,60,90,0.14)"
            ),

            unsafe_allow_html=True
        )

    # =================================================
    # INVESTOR POSITIONING
    # =================================================

    actions = get_investor_actions(
        country
    )

    st.markdown(
        _msec(
            "Institutional Positioning",
            "🔮"
        ),
        unsafe_allow_html=True
    )

    html = ""

    for action in actions:

        html += f"""
<div style="
padding:12px 0;
border-bottom:1px solid rgba(255,255,255,0.03);
font-size:15px;
line-height:1.8;
color:#d7f7ff;
">
◆ {action}
</div>
"""

    st.markdown(

        f"""
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
margin-bottom:18px;
">
{html}
</div>
""",

        unsafe_allow_html=True
    )

    # =================================================
    # ROTATION ENGINE
    # =================================================

    st.markdown(
        _msec(
            "Capital Rotation Dynamics",
            "📡"
        ),
        unsafe_allow_html=True
    )

    rotation_map = {

        "Iran": [
            "Rotation toward energy and commodity-linked assets.",
            "Defensive capital positioning accelerating globally.",
            "Emerging-market sensitivity increasing."
        ],

        "Taiwan": [
            "AI infrastructure hedging activity intensifying.",
            "Semiconductor diversification positioning increasing.",
            "Cybersecurity allocations strengthening."
        ],

        "Russia": [
            "Commodity-linked allocation bias remaining elevated.",
            "European industrial exposure weakening.",
            "Defensive macro positioning continuing."
        ],

        "Israel": [
            "Defense-sector accumulation accelerating.",
            "Cybersecurity exposure increasing globally.",
            "Regional risk hedging flows strengthening."
        ],

        "India": [
            "Infrastructure and manufacturing flows improving.",
            "Domestic growth positioning remaining resilient.",
            "Emerging-market diversification strengthening."
        ]
    }

    rotations = rotation_map.get(

        country,

        [
            "Institutional positioning remains moderately defensive."
        ]
    )

    html = ""

    for item in rotations:

        html += f"""
<div style="
padding:10px 0;
border-bottom:1px solid rgba(255,255,255,0.03);
font-size:15px;
color:#d7f7ff;
line-height:1.8;
">
• {item}
</div>
"""

    st.markdown(

        f"""
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
margin-bottom:18px;
">
{html}
</div>
""",

        unsafe_allow_html=True
    )

    # =================================================
    # POSITIONING PRESSURE
    # =================================================

    st.markdown(
        _msec(
            "Institutional Positioning Pressure",
            "📉"
        ),
        unsafe_allow_html=True
    )

    pressure_map = {

        "Iran": 92,
        "Taiwan": 85,
        "Russia": 81,
        "Israel": 78,
        "China": 73,
        "India": 56
    }

    pressure = pressure_map.get(
        country,
        60
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
background:rgba(0,255,255,0.03);
border:1px solid rgba(0,255,255,0.05);
font-size:14px;
line-height:1.7;
color:#7a9db0;
">
Institutional positioning pressure elevated to
<b style="color:white">{pressure}%</b>
across cross-asset allocation models.
</div>
""",

        unsafe_allow_html=True
    )