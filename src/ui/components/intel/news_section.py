import streamlit as st
import requests

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


def _news_card(title, source, published, tag, color, url):
    return f"""
<div style="
padding:18px;
border-radius:16px;
background:linear-gradient(180deg,rgba(0,18,35,0.55),rgba(0,5,15,0.92));
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
style="color:#d7f7ff;text-decoration:none;">
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
# GDELT DIRECT FETCH (fallback)
# =====================================================

def fetch_gdelt_direct(country, timespan="7d"):
    """
    Direct GDELT fetch with wider timespan as fallback.
    """
    try:
        params = {
            "query":      f"{country} war OR conflict OR military OR attack OR crisis",
            "mode":       "artlist",
            "maxrecords": 10,
            "format":     "json",
            "sort":       "DateDesc",
            "timespan":   timespan,
        }

        response = requests.get(
            "https://api.gdeltproject.org/api/v2/doc/doc",
            params=params,
            timeout=15,
            headers={"User-Agent": "GeoRiskAI/1.0"},
        )

        if response.status_code != 200:
            return []

        data = response.json()
        raw = data.get("articles", [])

        articles = []
        for a in raw:
            title  = a.get("title", "") or ""
            source = a.get("domain", "") or ""
            url    = a.get("url", "") or ""
            date   = a.get("seendate", "") or ""

            # Parse date
            try:
                from datetime import datetime
                dt = datetime.strptime(date[:15], "%Y%m%dT%H%M%S")
                readable = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                readable = date[:10]

            if not title:
                continue

            articles.append({
                "title":       title,
                "source":      source,
                "url":         url,
                "publishedAt": readable,
            })

        return articles

    except Exception as e:
        print(f"GDELT direct fetch failed: {e}")
        return []


# =====================================================
# RSS FALLBACK
# =====================================================

def fetch_rss_fallback(country):
    """
    Fetch news from RSS feeds as last resort.
    BBC, Reuters, Al Jazeera — always live, no limits.
    """
    try:
        import feedparser

        feeds = [
            "http://feeds.bbci.co.uk/news/world/rss.xml",
            "https://feeds.reuters.com/reuters/worldNews",
            "https://www.aljazeera.com/xml/rss/all.xml",
        ]

        articles = []
        for feed_url in feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title   = entry.get("title", "") or ""
                summary = entry.get("summary", "") or ""
                link    = entry.get("link", "") or ""
                date    = entry.get("published", "") or ""

                combined = (title + " " + summary).lower()

                if country.lower() in combined:
                    articles.append({
                        "title":       title,
                        "source":      feed.feed.get("title", "RSS"),
                        "url":         link,
                        "publishedAt": date[:16],
                    })

            if len(articles) >= 5:
                break

        return articles[:5]

    except Exception as e:
        print(f"RSS fallback failed: {e}")
        return []


# =====================================================
# LIVE NEWS SECTION
# =====================================================

def render_news_section(country):

    st.markdown(
        _msec(f"Live Intelligence Feed — {country}", "📰"),
        unsafe_allow_html=True
    )

    try:
        # ── Layer 1: news_engine fetch (24h timespan) ──
        articles = fetch_country_news(country)
        print(f"render_news_section called for {country}")

        # ── Layer 2: GDELT direct with 7d timespan ──
        if not articles:
            print(f"Layer 1 empty for {country}, trying 7d GDELT...")
            articles = fetch_gdelt_direct(country, timespan="7d")

        # ── Layer 3: GDELT with 30d timespan ──
        if not articles:
            print(f"Layer 2 empty for {country}, trying 30d GDELT...")
            articles = fetch_gdelt_direct(country, timespan="30d")

        # ── Layer 4: RSS feeds ──
        if not articles:
            print(f"Layer 3 empty for {country}, trying RSS...")
            articles = fetch_rss_fallback(country)

        # ── Nothing found ──
        if not articles:
            st.markdown(
                f"""
<div style="
padding:18px;
border-radius:16px;
background:rgba(0,18,35,0.45);
border:1px solid rgba(0,255,255,0.08);
font-size:15px;
color:#7a9db0;
">
No live geopolitical intelligence detected for {country}.<br>
<span style="font-size:12px;color:#3a6070;">
All sources checked — GDELT 24h, GDELT 7d, GDELT 30d, RSS feeds.
</span>
</div>
""",
                unsafe_allow_html=True
            )
            return

        # ── Render articles ──
        for article in articles:

            title = str(
                article.get("title", "No Title")
            ).replace("<", "").replace(">", "")

            source    = article.get("source", "Unknown")
            url       = article.get("url", "#")
            published = article.get("publishedAt", "")

            lower = title.lower()

            if any(x in lower for x in [
                "war", "attack", "missile",
                "explosion", "military", "conflict"
            ]):
                tag   = "HIGH RISK"
                color = "#ff3b5c"

            elif any(x in lower for x in [
                "sanctions", "oil", "inflation",
                "market", "trade"
            ]):
                tag   = "MACRO"
                color = "#ff9500"

            elif any(x in lower for x in [
                "technology", "ai",
                "semiconductor", "cyber"
            ]):
                tag   = "TECH"
                color = "#00c2ff"

            else:
                tag   = "LIVE"
                color = "#00c896"

            st.markdown(
                _news_card(
                    title, source, published,
                    tag, color, url
                ),
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Live intelligence feed error: {e}")