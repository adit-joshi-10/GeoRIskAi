"""
src/intelligence/news_engine.py
Real-time news via MediaStack API — 500 free requests/month
"""

import pandas as pd
import requests
import os
import time
import feedparser
from datetime import datetime

from src.intelligence.news_filter import is_relevant_geopolitical

# =====================================================
# CONFIG
# =====================================================

MEDIASTACK_KEY = "2a72c99f10e891b1000dc305e8024fba"
MEDIASTACK_URL = "http://api.mediastack.com/v1/news"

GDELT_DOC_URL  = "https://api.gdeltproject.org/api/v2/doc/doc"

RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.reuters.com/reuters/worldNews",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://rss.dw.com/rdf/rss-en-world",
    "https://feeds.skynews.com/feeds/rss/world.xml",
]

KEYWORD_WEIGHTS = {
    "war": 10, "invasion": 10, "missile": 9,
    "airstrike": 9, "military": 8, "conflict": 8,
    "terrorism": 9, "nuclear": 10, "sanctions": 7,
    "rebels": 7, "attack": 8, "violence": 7,
    "protest": 5, "border": 5, "crisis": 6,
    "troops": 6, "cyberattack": 7, "killed": 8,
    "bombing": 9, "ceasefire": 6, "offensive": 7,
}

TRACKED_COUNTRIES = [
    "Russia", "Ukraine", "Iran", "Israel", "China",
    "Taiwan", "North Korea", "South Korea", "United States",
    "India", "Pakistan", "Syria", "Afghanistan", "Venezuela",
]

OUTPUT_PATH = os.path.join("data", "processed", "live_news_risk.csv")


# =====================================================
# LAYER 1 — MEDIASTACK
# =====================================================

def fetch_via_mediastack(country, limit=8):
    try:
        params = {
            "access_key": MEDIASTACK_KEY,
            "keywords":   f"{country} conflict war military attack",
            "languages":  "en",
            "sort":       "published_desc",
            "limit":      25,
        }
        response = requests.get(
            MEDIASTACK_URL,
            params=params,
            timeout=15,
        )
        if response.status_code != 200:
            return []

        data     = response.json()
        articles = data.get("data", [])

        results = []
        for a in articles:
            title  = a.get("title", "") or ""
            url    = a.get("url", "") or ""
            source = a.get("source", "") or ""
            date   = a.get("published_at", "") or ""

            if not title or title == "[Removed]":
                continue

            article_dict = {
                "title":       title,
                "description": a.get("description", "") or "",
                "source":      {"name": source},
                "url":         url,
                "publishedAt": date[:10],
            }

            if is_relevant_geopolitical(article_dict):
                results.append({
                    "title":       title,
                    "source":      source,
                    "url":         url,
                    "publishedAt": date[:10],
                    "description": a.get("description", "") or "",
                })

            if len(results) >= limit:
                break

        return results

    except Exception as e:
        print(f"MediaStack failed for {country}: {e}")
        return []


# =====================================================
# LAYER 2 — GDELT
# =====================================================

def fetch_via_gdelt(country, timespan="7d"):
    try:
        params = {
            "query":      f"{country} conflict OR war OR military OR attack",
            "mode":       "artlist",
            "maxrecords": 25,
            "format":     "json",
            "sort":       "DateDesc",
            "timespan":   timespan,
        }
        response = requests.get(
            GDELT_DOC_URL,
            params=params,
            timeout=15,
            headers={"User-Agent": "GeoRiskAI/1.0"},
        )
        if response.status_code != 200:
            return []

        data        = response.json()
        raw_articles = data.get("articles", [])

        results = []
        for a in raw_articles:
            title  = a.get("title", "") or ""
            url    = a.get("url", "") or ""
            source = a.get("domain", "") or ""
            date   = a.get("seendate", "") or ""

            try:
                dt       = datetime.strptime(date[:15], "%Y%m%dT%H%M%S")
                readable = dt.strftime("%Y-%m-%d")
            except Exception:
                readable = date[:10]

            if not title:
                continue

            article_dict = {
                "title":       title,
                "description": "",
                "source":      {"name": source},
                "url":         url,
                "publishedAt": readable,
            }

            if is_relevant_geopolitical(article_dict):
                results.append({
                    "title":       title,
                    "source":      source,
                    "url":         url,
                    "publishedAt": readable,
                    "description": "",
                })

        return results

    except Exception as e:
        print(f"GDELT failed for {country}: {e}")
        return []


# =====================================================
# LAYER 3 — RSS FEEDS
# =====================================================

def fetch_via_rss(country, limit=8):
    try:
        results = []
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    title   = entry.get("title", "") or ""
                    summary = entry.get("summary", "") or ""
                    link    = entry.get("link", "") or ""
                    date    = entry.get("published", "") or ""
                    combined = (title + " " + summary).lower()

                    if country.lower() not in combined:
                        continue

                    article_dict = {
                        "title":       title,
                        "description": summary,
                        "source":      {"name": feed.feed.get("title", "")},
                        "url":         link,
                        "publishedAt": date[:10],
                    }

                    if is_relevant_geopolitical(article_dict):
                        results.append({
                            "title":       title,
                            "source":      feed.feed.get("title", "RSS"),
                            "url":         link,
                            "publishedAt": date[:10],
                            "description": summary,
                        })

                    if len(results) >= limit:
                        break

            except Exception:
                continue

            if len(results) >= limit:
                break

        return results

    except Exception as e:
        print(f"RSS failed for {country}: {e}")
        return []


# =====================================================
# LAYER 4 — RSS ANY MENTION (last resort)
# =====================================================

def fetch_rss_any_mention(country, limit=5):
    try:
        results = []
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    title   = entry.get("title", "") or ""
                    summary = entry.get("summary", "") or ""
                    link    = entry.get("link", "") or ""
                    date    = entry.get("published", "") or ""
                    combined = (title + " " + summary).lower()

                    if country.lower() in combined:
                        results.append({
                            "title":       title,
                            "source":      feed.feed.get("title", "RSS"),
                            "url":         link,
                            "publishedAt": date[:10],
                            "description": summary,
                        })

                    if len(results) >= limit:
                        break

            except Exception:
                continue

            if len(results) >= limit:
                break

        return results

    except Exception as e:
        return []


# =====================================================
# MAIN FETCH — 4 LAYER FALLBACK
# =====================================================

def fetch_country_news(country, limit=8):
    """
    4-layer fallback:
    1. MediaStack API (most reliable)
    2. GDELT 7d
    3. GDELT 30d
    4. RSS geopolitical filtered
    5. RSS any mention
    """
    # Layer 1 — MediaStack
    articles = fetch_via_mediastack(country, limit)
    if articles:
        print(f"MediaStack OK for {country}: {len(articles)} articles")
        return articles

    # Layer 2 — GDELT 7d
    articles = fetch_via_gdelt(country, timespan="7d")
    if articles:
        print(f"GDELT 7d OK for {country}: {len(articles)} articles")
        return articles[:limit]

    # Layer 3 — GDELT 30d
    articles = fetch_via_gdelt(country, timespan="30d")
    if articles:
        print(f"GDELT 30d OK for {country}: {len(articles)} articles")
        return articles[:limit]

    # Layer 4 — RSS filtered
    articles = fetch_via_rss(country, limit)
    if articles:
        print(f"RSS OK for {country}: {len(articles)} articles")
        return articles

    # Layer 5 — RSS any mention
    articles = fetch_rss_any_mention(country, limit)
    if articles:
        print(f"RSS any OK for {country}: {len(articles)} articles")
        return articles

    print(f"All layers failed for {country}")
    return []


# =====================================================
# FETCH NEWS (pipeline use)
# =====================================================

def fetch_news(country):
    return fetch_country_news(country, limit=10)


# =====================================================
# RISK SCORING
# =====================================================

def calculate_risk_score(articles):
    total_score      = 0
    matched_keywords = {}

    for article in articles:
        text = (
            str(article.get("title", ""))
            + " " +
            str(article.get("description", ""))
        ).lower()

        for keyword, weight in KEYWORD_WEIGHTS.items():
            if keyword in text:
                total_score += weight
                matched_keywords[keyword] = (
                    matched_keywords.get(keyword, 0) + 1
                )

    return total_score, matched_keywords


def normalize_scores(df):
    max_score = df["Raw_Score"].max()
    if max_score == 0:
        df["News_Risk_Score"] = 0
    else:
        df["News_Risk_Score"] = df["Raw_Score"] / max_score
    return df


def classify_live_risk(score):
    if score >= 0.75:   return "Critical"
    elif score >= 0.50: return "High"
    elif score >= 0.25: return "Medium"
    else:               return "Low"


def safe_get(lst, i):
    return lst[i] if len(lst) > i else ""


# =====================================================
# MAIN ENGINE
# =====================================================

def run_news_engine():
    print(f"\nStarting engine — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    results = []

    for country in TRACKED_COUNTRIES:
        print(f"Analyzing {country}...")
        articles              = fetch_news(country)
        raw_score, keywords   = calculate_risk_score(articles)

        top_titles  = [a.get("title", "")                          for a in articles[:5]]
        top_sources = [a.get("source", "")                         for a in articles[:5]]
        top_urls    = [a.get("url", "")                            for a in articles[:5]]
        top_dates   = [a.get("publishedAt", "")                    for a in articles[:5]]

        results.append({
            "Country":          country,
            "Articles_Fetched": len(articles),
            "Raw_Score":        raw_score,
            "Matched_Keywords": str(keywords),
            "Last_Updated":     datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Top_Article_1":    safe_get(top_titles, 0),
            "Top_Article_2":    safe_get(top_titles, 1),
            "Top_Article_3":    safe_get(top_titles, 2),
            "Top_Article_4":    safe_get(top_titles, 3),
            "Top_Article_5":    safe_get(top_titles, 4),
            "Source_1":         safe_get(top_sources, 0),
            "Source_2":         safe_get(top_sources, 1),
            "Source_3":         safe_get(top_sources, 2),
            "URL_1":            safe_get(top_urls, 0),
            "URL_2":            safe_get(top_urls, 1),
            "URL_3":            safe_get(top_urls, 2),
            "Date_1":           safe_get(top_dates, 0),
            "Date_2":           safe_get(top_dates, 1),
            "Date_3":           safe_get(top_dates, 2),
        })

        time.sleep(0.3)

    df = pd.DataFrame(results)
    df = normalize_scores(df)
    df["Live_Risk_Level"] = df["News_Risk_Score"].apply(classify_live_risk)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nEngine complete.")
    print(df[["Country", "Articles_Fetched", "Live_Risk_Level"]].to_string(index=False))
    return df


if __name__ == "__main__":
    run_news_engine()