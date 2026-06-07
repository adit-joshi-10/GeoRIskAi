import streamlit as st

from src.intelligence.news_engine import (
    fetch_country_news
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

def _news_card(

    title,

    source,

    published,

    tag,

    color,

    url

):

    return f"""
<div style="
padding:18px;
border-radius:16px;
background:
linear-gradient(
180deg,
rgba(0,18,35,0.55),
rgba(0,5,15,0.92)
);
border:1px solid rgba(0,255,255,0.08);
margin-bottom:16px;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:14px;
">

<div style="
font-size:10px;
letter-spacing:3px;
font-family:monospace;
color:#3a6070;
text-transform:uppercase;
">
LIVE INTELLIGENCE SIGNAL
</div>

<div style="
padding:4px 10px;
border-radius:999px;
font-size:10px;
font-family:monospace;
letter-spacing:2px;
background:{color};
color:white;
">
{tag}
</div>

</div>

<div style="
font-size:18px;
line-height:1.7;
font-weight:600;
margin-bottom:14px;
">

<a href="{url}"
target="_blank"
style="
color:#d7f7ff;
text-decoration:none;
">
{title}
</a>

</div>

<div style="
display:flex;
justify-content:space-between;
font-size:12px;
color:#6f8fa0;
font-family:monospace;
">

<div>{source}</div>

<div>{published}</div>

</div>

</div>
"""

# =====================================================
# LIVE NEWS SECTION
# =====================================================

def render_news_section(

    country

):

    st.markdown(
        _msec(
            f"Live Intelligence Feed — {country}",
            "📰"
        ),
        unsafe_allow_html=True
    )

    try:

        articles = fetch_country_news(
            country
        )

        if not articles:

            st.markdown(
                """
<div style="
padding:18px;
border-radius:16px;
background:rgba(0,18,35,0.45);
border:1px solid rgba(0,255,255,0.08);
font-size:15px;
color:#7a9db0;
">
No live geopolitical intelligence detected.
</div>
""",
                unsafe_allow_html=True
            )

            return

        # =============================================
        # ARTICLE RENDERING
        # =============================================

        for article in articles:

            title = str(
                article.get(
                    "title",
                    "No Title"
                )
            ).replace("<", "").replace(">", "")

            source = article.get(
                "source",
                "Unknown"
            )

            url = article.get(
                "url",
                "#"
            )

            published = article.get(
                "publishedAt",
                ""
            )

            # =========================================
            # THREAT CLASSIFICATION
            # =========================================

            lower = title.lower()

            if any(x in lower for x in [

                "war",
                "attack",
                "missile",
                "explosion",
                "military",
                "conflict"

            ]):

                tag = "HIGH RISK"
                color = "#ff3b5c"

            elif any(x in lower for x in [

                "sanctions",
                "oil",
                "inflation",
                "market",
                "trade"

            ]):

                tag = "MACRO"
                color = "#ff9500"

            elif any(x in lower for x in [

                "technology",
                "ai",
                "semiconductor",
                "cyber"

            ]):

                tag = "TECH"
                color = "#00c2ff"

            else:

                tag = "LIVE"
                color = "#00c896"

            st.markdown(

                _news_card(

                    title,

                    source,

                    published,

                    tag,

                    color,

                    url
                ),

                unsafe_allow_html=True
            )

    except Exception as e:

        st.error(
            f"Live intelligence feed error: {e}"
        )