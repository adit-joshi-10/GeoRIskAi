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

try:
    from src.intelligence.news_filter import is_relevant_geopolitical
except Exception:
    def is_relevant_geopolitical(article):
        text = " ".join(
            [
                str(article.get("title", "")),
                str(article.get("description", "")),
            ]
        ).lower()
        keywords = [
            "war", "invasion", "missile", "airstrike", "military", "conflict",
            "terrorism", "nuclear", "sanctions", "rebels", "attack",
            "violence", "protest", "border", "crisis", "troops",
            "cyberattack", "inflation", "economic collapse", "market panic",
        ]
        return any(keyword in text for keyword in keywords)

# =====================================================
# CONFIG
# =====================================================

NEWSDATA_API_KEY = "pub_4059a784c6de403cbdbf08aad49a98cc"
NEWSDATA_URL = "https://newsdata.io/api/1/latest"

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
    if not date_str:
        return ""

    if not isinstance(date_str, str):
        date_str = str(date_str)

    date_str = date_str.strip()

    if len(date_str) >= 15 and date_str[:8].isdigit():
        try:
            dt = datetime.strptime(date_str[:15], "%Y%m%dT%H%M%S")
            return dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            pass

    if len(date_str) >= 10:
        return date_str[:10]

    return ""


# =====================================================
# FETCH NEWS FOR DASHBOARD (single country)
# =====================================================

# @st.cache_data(ttl=900)
def fetch_country_news(country, limit=5):
    """
    Fetch latest geopolitical news for one country from NewsData.
    Returns a list of relevant articles.
    """
    print("\n" + "=" * 50)
    print(f"FETCHING NEWS FOR: {country}")

    try:
        params = {
            "apikey": NEWSDATA_API_KEY,
            "q": country,
            "language": "en",
            "size": max(limit, 10),
        }

        response = requests.get(
            NEWSDATA_URL,
            params=params,
            timeout=20,
        )
        print(f"NewsData Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"NewsData error {response.status_code} for {country}")
            return []

        data = response.json()
        raw_articles = data.get("results", [])
        print(f"Raw Articles Found: {len(raw_articles)}")

        articles = []
        for a in raw_articles:
            title = (a.get("title") or "").strip()
            url = a.get("link") or a.get("url") or ""
            source_name = a.get("source_name") or a.get("domain") or ""
            date = a.get("pubDate") or a.get("created_at") or ""
            description = a.get("description") or ""

            article_dict = {
                "title": title,
                "description": description,
                "source": {"name": source_name},
                "url": url,
                "publishedAt": parse_gdelt_date(date),
            }
            relevant = is_relevant_geopolitical(article_dict)

            print(f"{title[:50]}... -> {'KEPT' if relevant else 'FILTERED'}")

            if not relevant:
                continue

            articles.append({
                "title": title,
                "source": {"name": source_name},
                "url": url,
                "publishedAt": parse_gdelt_date(date),
                "description": description,
            })

            if len(articles) >= limit:
                break

        if len(articles) == 0 and len(raw_articles) > 0:
            print(f"No relevant articles found for {country}")
            print(f"Using {min(limit, len(raw_articles))} fallback articles")

            for a in raw_articles[:limit]:
                articles.append({
                    "title": (a.get("title") or "").strip(),
                    "source": {"name": (a.get("source_name") or a.get("domain") or "")},
                    "url": a.get("url") or a.get("link") or "",
                    "publishedAt": parse_gdelt_date(
                        (a.get("pubDate") or a.get("created_at") or "")
                    ),
                    "description": (a.get("description") or ""),
                })

        print(f"Final Articles Returned: {len(articles)}")
        return articles

    except Exception as e:
        print(f"NewsData fetch failed for {country}: {e}")
        return []


# =====================================================
# FETCH NEWS FOR PIPELINE
# =====================================================

def fetch_news(country):
    """
    Fetch and filter geopolitical articles for a country.
    Returns list of relevant articles.
    """
    return fetch_country_news(country, limit=10)


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