import streamlit as st

from src.intelligence.market_reactions import (
    get_market_reactions
)

from src.intelligence.capital_flows import (
    get_capital_flows
)

# =====================================================
# SMALL HELPERS
# =====================================================

def _msec(title, icon):

    return (
        f"""
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
    )

def _ibox(title, body, border):

    return f"""
<div style="
padding:14px 16px;
border-radius:16px;
background:
linear-gradient(
180deg,
rgba(0,18,35,0.55),
rgba(0,5,15,0.85)
);
border:1px solid {border};
min-height:210px;
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

    for asset, move in items:

        html += f"""
<div style="
display:flex;
justify-content:space-between;
padding:10px 0;
border-bottom:1px solid rgba(255,255,255,0.03);
font-size:15px;
">

<div style="color:{color}">
{arrow} {asset}
</div>

<div style="color:#6f8fa0">
{move}
</div>

</div>
"""

    return html

# =====================================================
# MARKET SECTION
# =====================================================

def render_market_section(

    country,

    risk

):

    # =================================================
    # MARKET IMPACT FORECAST
    # =================================================

    impact_map = {

        "Iran": {

            "bullish": [
                ("Oil & Energy", ""),
                ("Gold", ""),
                ("Defense Stocks", ""),
                ("USD Safe Haven", "")
            ],

            "bearish": [
                ("Airlines", ""),
                ("Shipping", ""),
                ("Emerging Markets", "")
            ]
        },

        "Taiwan": {

            "bullish": [
                ("Cybersecurity", ""),
                ("Defense Tech", ""),
                ("US Chip Alternatives", "")
            ],

            "bearish": [
                ("Semiconductors", ""),
                ("AI Hardware", ""),
                ("Consumer Electronics", "")
            ]
        },

        "India": {

            "bullish": [
                ("Infrastructure", ""),
                ("Manufacturing", ""),
                ("Domestic Growth", "")
            ],

            "bearish": [
                ("Oil Importers", ""),
                ("Export Sensitives", "")
            ]
        }
    }

    impacts = impact_map.get(

        country,

        {

            "bullish": [
                ("Gold", ""),
                ("Utilities", "")
            ],

            "bearish": [
                ("Growth Stocks", ""),
                ("Travel", "")
            ]
        }
    )

    st.markdown(
        _msec(
            "Market Impact Forecast",
            "📊"
        ),
        unsafe_allow_html=True
    )

    i1, i2 = st.columns(2)

    with i1:

        st.markdown(

            _ibox(

                "Bullish Impact",

                _rows(
                    impacts["bullish"],
                    True
                ),

                "rgba(0,255,180,0.14)"
            ),

            unsafe_allow_html=True
        )

    with i2:

        st.markdown(

            _ibox(

                "Bearish Impact",

                _rows(
                    impacts["bearish"],
                    False
                ),

                "rgba(255,60,90,0.14)"
            ),

            unsafe_allow_html=True
        )

    # =================================================
    # MARKET REACTIONS
    # =================================================

    reactions = get_market_reactions(
        country
    )

    st.markdown(
        _msec(
            "Market Reaction Monitor",
            "📈"
        ),
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(

            _ibox(

                "Positive Momentum",

                _rows(
                    reactions.get(
                        "positive",
                        []
                    ),
                    True
                ),

                "rgba(0,255,180,0.14)"
            ),

            unsafe_allow_html=True
        )

    with c2:

        st.markdown(

            _ibox(

                "Negative Momentum",

                _rows(
                    reactions.get(
                        "negative",
                        []
                    ),
                    False
                ),

                "rgba(255,60,90,0.14)"
            ),

            unsafe_allow_html=True
        )

    # =================================================
    # CAPITAL FLOWS
    # =================================================

    flows = get_capital_flows(
        country
    )

    st.markdown(
        _msec(
            "Capital Flow Sentiment",
            "📡"
        ),
        unsafe_allow_html=True
    )

    st.markdown(

        f"""
<div style="
padding:14px 16px;
border-left:3px solid #ff9500;
background:rgba(255,149,0,0.05);
border-radius:10px;
margin-bottom:18px;
font-size:14px;
line-height:1.7;
color:#ffd27a;
">
{flows.get("sentiment","—")}
</div>
""",

        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    inflows = [

        (x, "")
        for x in flows.get(
            "inflows",
            []
        )
    ]

    outflows = [

        (x, "")
        for x in flows.get(
            "outflows",
            []
        )
    ]

    with c1:

        st.markdown(

            _ibox(

                "Capital Inflows",

                _rows(
                    inflows,
                    True
                ),

                "rgba(0,255,180,0.14)"
            ),

            unsafe_allow_html=True
        )

    with c2:

        st.markdown(

            _ibox(

                "Capital Outflows",

                _rows(
                    outflows,
                    False
                ),

                "rgba(255,60,90,0.14)"
            ),

            unsafe_allow_html=True
        )

    # =====================================================
    # CROSS-ASSET SHOCK SIMULATION
    # =====================================================

    st.markdown(
        _msec(
            "Cross-Asset Shock Simulation",
            "⚡"
        ),
        unsafe_allow_html=True
    )

    shock_map = {

        "Iran": {

            "positive": [
                ("Crude Oil", "+5.8%"),
                ("Gold", "+2.4%"),
                ("Defense", "+3.1%"),
                ("Volatility Index", "+8.2%")
            ],

            "negative": [
                ("Airlines", "-4.2%"),
                ("Shipping", "-3.9%"),
                ("Tourism", "-2.8%"),
                ("Emerging Markets", "-1.9%")
            ]
        },

        "Taiwan": {

            "positive": [
                ("Cybersecurity", "+4.1%"),
                ("Defense Tech", "+3.4%"),
                ("US Chip Alternatives", "+2.7%")
            ],

            "negative": [
                ("Semiconductors", "-6.1%"),
                ("AI Hardware", "-4.3%"),
                ("Consumer Electronics", "-3.2%")
            ]
        },

        "Russia": {

            "positive": [
                ("Energy", "+4.8%"),
                ("Gold", "+2.1%"),
                ("Defense", "+2.9%")
            ],

            "negative": [
                ("European Industrials", "-3.7%"),
                ("Banks", "-2.8%"),
                ("Imports", "-2.1%")
            ]
        },

        "Israel": {

            "positive": [
                ("Cybersecurity", "+5.0%"),
                ("Defense", "+4.4%"),
                ("Oil", "+2.2%")
            ],

            "negative": [
                ("Regional Airlines", "-3.2%"),
                ("Tourism", "-4.1%"),
                ("Hospitality", "-2.7%")
            ]
        },

        "India": {

            "positive": [
                ("Infrastructure", "+3.3%"),
                ("Domestic Consumption", "+2.6%"),
                ("Manufacturing", "+2.4%")
            ],

            "negative": [
                ("Oil Importers", "-2.4%"),
                ("Export Sensitives", "-1.8%")
            ]
        }
    }

    shocks = shock_map.get(

        country,

        {

            "positive": [
                ("Gold", "+1.8%"),
                ("Utilities", "+1.4%")
            ],

            "negative": [
                ("Growth Stocks", "-2.1%"),
                ("Travel", "-1.9%")
            ]
        }
    )

    sh1, sh2 = st.columns(2)

    with sh1:

        st.markdown(

            _ibox(

                "Safe Haven Rotation",

                _rows(
                    shocks["positive"],
                    True
                ),

                "rgba(0,255,180,0.14)"
            ),

            unsafe_allow_html=True
        )

    with sh2:

        st.markdown(

            _ibox(

                "Contagion Pressure",

                _rows(
                    shocks["negative"],
                    False
                ),

                "rgba(255,60,90,0.14)"
            ),

            unsafe_allow_html=True
        )

    # =====================================================
    # VOLATILITY PRESSURE
    # =====================================================

    st.markdown(
        _msec(
            "Institutional Volatility Pressure",
            "📉"
        ),
        unsafe_allow_html=True
    )

    volatility_map = {

        "Iran": 88,
        "Taiwan": 82,
        "Russia": 79,
        "Israel": 76,
        "China": 72,
        "India": 48
    }

    vol_score = volatility_map.get(
        country,
        55
    )

    st.progress(
        vol_score / 100
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
Institutional volatility pressure elevated to
<b style="color:white">{vol_score}%</b>
across correlated geopolitical macro channels.
</div>
""",

        unsafe_allow_html=True
    )

    # =====================================================
    # REGIONAL SPILLOVER ENGINE
    # =====================================================

    st.markdown(
        _msec(
            "Regional Spillover Simulation",
            "🌍"
        ),
        unsafe_allow_html=True
    )

    spillovers = {

        "Iran": [
            "Saudi Arabia",
            "UAE",
            "Global Oil Markets",
            "Shipping Routes"
        ],

        "Taiwan": [
            "China",
            "South Korea",
            "Japan",
            "AI Infrastructure"
        ],

        "Russia": [
            "Europe",
            "Energy Markets",
            "NATO Supply Chains"
        ],

        "Israel": [
            "Middle East",
            "Oil Markets",
            "Defense Sector"
        ],

        "India": [
            "South Asia",
            "Manufacturing Chains",
            "Energy Imports"
        ]
    }

    affected = spillovers.get(
        country,
        ["Regional Markets"]
    )

    html = ""

    for item in affected:

        html += f"""
<div style="
padding:8px 0;
border-bottom:1px solid rgba(255,255,255,0.03);
font-size:15px;
color:#d7f7ff;
">
• {item}
</div>
"""

    st.markdown(

        _ibox(
            "Cascade Exposure Network",
            html,
            "rgba(0,255,255,0.08)"
        ),

        unsafe_allow_html=True
    )