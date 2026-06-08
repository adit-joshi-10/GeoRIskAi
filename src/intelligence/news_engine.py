"""
src/intelligence/news_engine.py

Real-time geopolitical intelligence engine.
Uses NewsAPI to compute live geopolitical risk signals.
"""

import pandas as pd
import requests
import os
import time

from src.intelligence.news_filter import (
    is_relevant_geopolitical
)

# =====================================================
# LOAD ENV VARIABLES
# =====================================================

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    print("DOTENV ERROR:", e)

import streamlit as st

try:
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
except:
    NEWS_API_KEY = ""

print("NEWS API KEY LOADED:", NEWS_API_KEY is not None)

# =====================================================
# CONFIG
# =====================================================

NEWS_URL = "https://newsapi.org/v2/everything"

OUTPUT_PATH = os.path.join(
    "data",
    "processed",
    "live_news_risk.csv"
)

# =====================================================
# GEOPOLITICAL KEYWORDS
# =====================================================

KEYWORD_WEIGHTS = {

    # HIGH RISK
    "war": 10,
    "invasion": 10,
    "missile": 9,
    "airstrike": 9,
    "military": 8,
    "conflict": 8,
    "terrorism": 9,
    "nuclear": 10,
    "sanctions": 7,
    "rebels": 7,
    "attack": 8,
    "violence": 7,

    # MEDIUM RISK
    "protest": 5,
    "border": 5,
    "crisis": 6,
    "troops": 6,
    "political tension": 6,
    "cyberattack": 7,

    # ECONOMIC / INSTABILITY
    "inflation": 4,
    "oil shock": 5,
    "economic collapse": 7,
    "market panic": 6,
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
# LIVE COUNTRY NEWS FETCHER
# =====================================================

def fetch_country_news(country, limit=5):

    try:

        # =============================================
        # IMPROVED QUERY
        # =============================================

        query = (
            f'"{country}" AND '
            f'(geopolitics OR war OR conflict OR military '
            f'OR sanctions OR terrorism OR defense '
            f'OR border OR missile OR nuclear)'
        )

        params = {

            "q": query,

            "language": "en",

            "sortBy": "publishedAt",

            "pageSize": 20,

            "apiKey": NEWS_API_KEY,
        }

        response = requests.get(
            NEWS_URL,
            params=params,
            timeout=15
        )

        data = response.json()

        articles = []

        if "articles" not in data:

            return []

        # =============================================
        # FILTER ARTICLES
        # =============================================

        for article in data["articles"]:

            # Skip irrelevant news
            if not is_relevant_geopolitical(
                article
            ):

                continue

            articles.append({

                "title":
                article.get("title", ""),

                "source":
                article.get("source", {})
                .get("name", ""),

                "url":
                article.get("url", ""),

                "publishedAt":
                article.get(
                    "publishedAt",
                    ""
                ),

                "description":
                article.get(
                    "description",
                    ""
                )
            })

        # =============================================
        # LIMIT FINAL RESULTS
        # =============================================

        return articles[:limit]

    except Exception as e:

        print(
            f"News fetch failed for {country}: {e}"
        )

        return []

# =====================================================
# FETCH NEWS FOR PIPELINE
# =====================================================

def fetch_news(country):

    query = (
        f'"{country}" AND '
        f'(geopolitics OR war OR conflict OR military '
        f'OR sanctions OR terrorism OR missile '
        f'OR border OR nuclear)'
    )

    params = {

        "q": query,

        "language": "en",

        "sortBy": "publishedAt",

        "pageSize": 25,

        "apiKey": NEWS_API_KEY,
    }

    try:

        response = requests.get(
            NEWS_URL,
            params=params,
            timeout=15
        )

        data = response.json()

        if data.get("status") != "ok":

            print(f"API error for {country}")

            return []

        filtered_articles = []

        for article in data.get(
            "articles",
            []
        ):

            if is_relevant_geopolitical(
                article
            ):

                filtered_articles.append(
                    article
                )

        return filtered_articles

    except Exception as e:

        print(
            f"Error fetching {country}: {e}"
        )

        return []

# =====================================================
# CALCULATE NEWS RISK SCORE
# =====================================================

def calculate_risk_score(articles):

    total_score = 0

    matched_keywords = {}

    for article in articles:

        text = (

            str(article.get("title", ""))

            + " " +

            str(article.get(
                "description",
                ""
            ))
        ).lower()

        for keyword, weight in (
            KEYWORD_WEIGHTS.items()
        ):

            if keyword in text:

                total_score += weight

                matched_keywords[keyword] = (

                    matched_keywords.get(
                        keyword,
                        0
                    ) + 1
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

        df["News_Risk_Score"] = (

            df["Raw_Score"]

            / max_score
        )

    return df

# =====================================================
# MAIN ENGINE
# =====================================================

def run_news_engine():

    print(
        "\nStarting live geopolitical intelligence engine...\n"
    )

    results = []

    for country in TRACKED_COUNTRIES:

        print(f"Analyzing {country}...")

        articles = fetch_news(country)

        raw_score, keywords = (
            calculate_risk_score(
                articles
            )
        )

        # =============================================
        # EXTRACT TOP ARTICLES
        # =============================================

        top_titles = []
        top_sources = []
        top_urls = []

        for article in articles[:5]:

            top_titles.append(

                article.get(
                    "title",
                    ""
                )
            )

            top_sources.append(

                article.get(
                    "source",
                    {}
                ).get(
                    "name",
                    ""
                )
            )

            top_urls.append(

                article.get(
                    "url",
                    ""
                )
            )

        # =============================================
        # SAVE RESULTS
        # =============================================

        results.append({

            "Country": country,

            "Articles_Fetched":
            len(articles),

            "Raw_Score":
            raw_score,

            "Matched_Keywords":
            str(keywords),

            # =========================================
            # ARTICLE DATA
            # =========================================

            "Top_Article_1":
            top_titles[0]
            if len(top_titles) > 0
            else "",

            "Top_Article_2":
            top_titles[1]
            if len(top_titles) > 1
            else "",

            "Top_Article_3":
            top_titles[2]
            if len(top_titles) > 2
            else "",

            "Top_Article_4":
            top_titles[3]
            if len(top_titles) > 3
            else "",

            "Top_Article_5":
            top_titles[4]
            if len(top_titles) > 4
            else "",

            "Source_1":
            top_sources[0]
            if len(top_sources) > 0
            else "",

            "Source_2":
            top_sources[1]
            if len(top_sources) > 1
            else "",

            "Source_3":
            top_sources[2]
            if len(top_sources) > 2
            else "",

            "URL_1":
            top_urls[0]
            if len(top_urls) > 0
            else "",

            "URL_2":
            top_urls[1]
            if len(top_urls) > 1
            else "",

            "URL_3":
            top_urls[2]
            if len(top_urls) > 2
            else "",
        })

        # Avoid rate limit
        time.sleep(1)

    # =================================================
    # DATAFRAME
    # =================================================

    df = pd.DataFrame(results)

    df = normalize_scores(df)

    # =================================================
    # CLASSIFY LIVE RISK
    # =================================================

    def classify_live_risk(score):

        if score >= 0.75:

            return "Critical"

        elif score >= 0.50:

            return "High"

        elif score >= 0.25:

            return "Medium"

        else:

            return "Low"

    df["Live_Risk_Level"] = (

        df["News_Risk_Score"]

        .apply(classify_live_risk)
    )

    # =================================================
    # SAVE
    # =================================================

    os.makedirs(

        os.path.dirname(
            OUTPUT_PATH
        ),

        exist_ok=True
    )

    df.to_csv(

        OUTPUT_PATH,

        index=False
    )

    print(
        "\nLive intelligence completed.\n"
    )

    print(
        df.to_string(index=False)
    )

    print(
        f"\nSaved to: {OUTPUT_PATH}"
    )

    return df

# =====================================================
# EXECUTE
# =====================================================

if __name__ == "__main__":

    run_news_engine()