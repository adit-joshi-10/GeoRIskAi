"""
src/intelligence/news_engine.py

Real-time geopolitical intelligence engine.
Uses GDELT — free, no API key, updates every 15 minutes.
"""

import pandas as pd
import requests
import os
import time
from datetime import datetime

from src.intelligence.news_filter import is_relevant_geopolitical

# =====================================================
# CONFIG
# =====================================================

GDELT_DOC_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

OUTPUT_PATH = os.path.join(
    "data",
    "processed",
    "live_news_risk.csv"
)

# =====================================================
# KEYWORD WEIGHTS
# =====================================================

KEYWORD_WEIGHTS = {
    "war":               10,
    "invasion":          10,
    "missile":            9,
    "airstrike":          9,
    "military":           8,
    "conflict":           8,
    "terrorism":          9,
    "nuclear":           10,
    "sanctions":          7,
    "rebels":             7,
    "attack":             8,
    "violence":           7,
    "protest":            5,
    "border":             5,
    "crisis":             6,
    "troops":             6,
    "cyberattack":        7,
    "inflation":          4,
    "economic collapse":  7,
    "market panic":       6,
}

# =====================================================
# COUNTRIES TO TRACK
# =====================================================

TRACKED_COUNTRIES = [
    "Russia",
    "Ukraine",
    "Iran",
    "Israel",
    "China",
    "Taiwan",
    "North Korea",
    "South Korea",
    "United States",
    "India",
    "Pakistan",
    "Syria",
    "Afghanistan",
    "Venezuela",
]


# =====================================================
# HELPER
# =====================================================

def safe_get(lst, i):
    return lst[i] if len(lst) > i else ""


def parse_gdelt_date(date_str):
    try:
        dt = datetime.strptime(date_str[:15], "%Y%m%dT%H%M%S")
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return date_str[:10]


# =====================================================
# FETCH NEWS FOR DASHBOARD (single country)
# =====================================================

def fetch_country_news(country, limit=5):
    """
    Fetch latest geopolitical news for one country from GDELT.
    Real-time — updates every 15 minutes. No API key needed.
    """
    try:
        query = (
            f'"{country}" '
            f'(war OR conflict OR military OR sanctions '
            f'OR terrorism OR missile OR nuclear OR border '
            f'OR troops OR crisis OR attack OR violence)'
        )

        params = {
            "query":      query,
            "mode":       "artlist",
            "maxrecords": 25,
            "format":     "json",
            "sort":       "DateDesc",
            "timespan":   "24h",
        }

        response = requests.get(
            GDELT_DOC_URL,
            params=params,
            timeout=15,
            headers={"User-Agent": "GeoRiskAI/1.0"},
        )

        if response.status_code != 200:
            print(f"GDELT error {response.status_code} for {country}")
            return []

        data = response.json()
        raw_articles = data.get("articles", [])

        articles = []
        for a in raw_articles:
            title  = a.get("title", "") or ""
            url    = a.get("url", "") or ""
            source = a.get("domain", "") or ""
            date   = a.get("seendate", "") or ""

            article_dict = {
                "title":       title,
                "description": "",
                "source":      {"name": source},
                "url":         url,
                "publishedAt": parse_gdelt_date(date),
            }

            if not is_relevant_geopolitical(article_dict):
                continue

            articles.append({
                "title":       title,
                "source":      source,
                "url":         url,
                "publishedAt": parse_gdelt_date(date),
                "description": "",
            })

            if len(articles) >= limit:
                break
         
        return articles

    except Exception as e:
        print(f"GDELT fetch failed for {country}: {e}")
        return []

def fetch_country_news(country, limit=5):

    print("\n" + "="*50)
    print(f"FETCHING NEWS FOR: {country}")
# =====================================================
# FETCH NEWS FOR PIPELINE
# =====================================================

def fetch_news(country):
    """
    Fetch and filter geopolitical articles for a country.
    Returns list of relevant articles.
    """
    try:
        query = (
            f'"{country}" '
            f'(war OR conflict OR military OR sanctions '
            f'OR terrorism OR missile OR nuclear OR border '
            f'OR troops OR crisis OR attack OR violence)'
        )

        params = {
            "query":      query,
            "mode":       "artlist",
            "maxrecords": 25,
            "format":     "json",
            "sort":       "DateDesc",
            "timespan":   "24h",
        }

        response = requests.get(
            GDELT_DOC_URL,
            params=params,
            timeout=15,
            headers={"User-Agent": "GeoRiskAI/1.0"},
        )

        if response.status_code != 200:
            return []

        data = response.json()
        raw_articles = data.get("articles", [])
        print(f"GDELT returned {len(raw_articles)} raw articles")

        filtered = []
        for a in raw_articles:
            title  = a.get("title", "") or ""
            source = a.get("domain", "") or ""
            url    = a.get("url", "") or ""
            date   = a.get("seendate", "") or ""

            article_dict = {
                "title":       title,
                "description": "",
                "source":      {"name": source},
                "url":         url,
                "publishedAt": parse_gdelt_date(date),
            }

            if is_relevant_geopolitical(article_dict):
                filtered.append(article_dict)

        return filtered

    except Exception as e:
        print(f"Error fetching {country}: {e}")
        return []


# =====================================================
# CALCULATE NEWS RISK SCORE
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


# =====================================================
# NORMALIZE SCORES
# =====================================================

def normalize_scores(df):
    max_score = df["Raw_Score"].max()
    if max_score == 0:
        df["News_Risk_Score"] = 0
    else:
        df["News_Risk_Score"] = df["Raw_Score"] / max_score
    return df


# =====================================================
# CLASSIFY RISK
# =====================================================

def classify_live_risk(score):
    if score >= 0.75:
        return "Critical"
    elif score >= 0.50:
        return "High"
    elif score >= 0.25:
        return "Medium"
    else:
        return "Low"


# =====================================================
# MAIN ENGINE
# =====================================================

def run_news_engine():
    print("\nStarting live geopolitical intelligence engine...\n")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    results = []

    for country in TRACKED_COUNTRIES:
        print(f"Analyzing {country}...")

        articles    = fetch_news(country)
        raw_score, keywords = calculate_risk_score(articles)

        top_titles  = []
        top_sources = []
        top_urls    = []
        top_dates   = []

        for article in articles[:5]:
            top_titles.append(article.get("title", ""))
            top_sources.append(
                article.get("source", {}).get("name", "")
            )
            top_urls.append(article.get("url", ""))
            top_dates.append(article.get("publishedAt", ""))

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

        time.sleep(0.5)

    df = pd.DataFrame(results)
    df = normalize_scores(df)
    df["Live_Risk_Level"] = df["News_Risk_Score"].apply(classify_live_risk)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nLive intelligence completed.\n")
    print(
        df[["Country", "Articles_Fetched", "Live_Risk_Level", "Last_Updated"]]
        .to_string(index=False)
    )
    print(f"\nSaved to: {OUTPUT_PATH}")

    return df


# =====================================================
# EXECUTE
# =====================================================

if __name__ == "__main__":
    run_news_engine()