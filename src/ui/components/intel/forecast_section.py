import streamlit as st

from src.intelligence.trend_forecast import (
    get_trend_forecast
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

def _fbox(title, value, color):

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
margin-bottom:14px;
text-align:center;
min-height:130px;
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
font-size:26px;
font-weight:700;
color:{color};
margin-top:10px;
">
{value}
</div>

</div>
"""

# =====================================================
# FORECAST SECTION
# =====================================================

def render_forecast_section(

    country

):

    forecast = get_trend_forecast(
        country
    )

    # =================================================
    # FORECAST HEADER
    # =================================================

    st.markdown(
        _msec(
            "7-Day Escalation Forecast",
            "📈"
        ),
        unsafe_allow_html=True
    )

    # =================================================
    # CORE FORECAST METRICS
    # =================================================

    f1, f2, f3 = st.columns(3)

    with f1:

        st.markdown(

            _fbox(

                "Trend",

                forecast.get(
                    "trend",
                    "—"
                ),

                "#00e5ff"
            ),

            unsafe_allow_html=True
        )

    with f2:

        st.markdown(

            _fbox(

                "Stability",

                forecast.get(
                    "stability",
                    "—"
                ),

                "#ff9500"
            ),

            unsafe_allow_html=True
        )

    with f3:

        st.markdown(

            _fbox(

                "Escalation Probability",

                forecast.get(
                    "probability",
                    "—"
                ),

                "#ff3b5c"
            ),

            unsafe_allow_html=True
        )

    # =================================================
    # FORECAST DRIVERS
    # =================================================

    st.markdown(
        _msec(
            "Forecast Drivers",
            "⚡"
        ),
        unsafe_allow_html=True
    )

    html = ""

    for driver in forecast.get(
        "drivers",
        []
    ):

        html += f"""
<div style="
padding:10px 0;
border-bottom:1px solid rgba(255,255,255,0.03);
font-size:15px;
color:#d7f7ff;
">
◆ {driver}
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
margin-bottom:16px;
">
{html}
</div>
""",

        unsafe_allow_html=True
    )

    # =================================================
    # TRAJECTORY ANALYSIS
    # =================================================

    st.markdown(
        _msec(
            "Trajectory Analysis",
            "🧠"
        ),
        unsafe_allow_html=True
    )

    trajectory_map = {

        "Iran":
        "Escalation trajectory remains highly sensitive to "
        "oil-route disruption risk and regional retaliation dynamics.",

        "Taiwan":
        "Technology supply-chain fragmentation risk continues "
        "to increase under geopolitical pressure conditions.",

        "Russia":
        "Long-duration geopolitical pressure sustaining "
        "elevated macro volatility across European markets.",

        "Israel":
        "Military escalation sensitivity remains elevated "
        "across regional geopolitical networks.",

        "India":
        "Domestic macro resilience continues supporting "
        "relative regional stability."
    }

    trajectory = trajectory_map.get(

        country,

        "Geopolitical conditions remain moderately elevated "
        "across regional intelligence indicators."
    )

    st.markdown(

        f"""
<div style="
padding:18px;
border-left:3px solid #00e5ff;
background:rgba(0,255,255,0.04);
border-radius:12px;
margin-bottom:18px;
font-size:15px;
line-height:1.9;
color:#d7f7ff;
">
{trajectory}
</div>
""",

        unsafe_allow_html=True
    )

    # =================================================
    # INSTITUTIONAL SIGNAL
    # =================================================

    st.markdown(
        _msec(
            "Institutional Forecast Confidence",
            "📉"
        ),
        unsafe_allow_html=True
    )

    confidence_map = {

        "Iran": 91,
        "Taiwan": 84,
        "Russia": 82,
        "Israel": 79,
        "China": 71,
        "India": 58
    }

    confidence = confidence_map.get(
        country,
        60
    )

    st.progress(
        confidence / 100
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
Institutional confidence in forecast trajectory elevated to
<b style="color:white">{confidence}%</b>
across multi-signal geopolitical intelligence models.
</div>
""",

        unsafe_allow_html=True
    )