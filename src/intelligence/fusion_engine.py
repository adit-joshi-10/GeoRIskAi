"""
src/intelligence/fusion_engine.py

Combines:
- Historical ML forecasting
- Live geopolitical news intelligence

Produces final dynamic geopolitical risk scores.
"""

import pandas as pd
import os


# =====================================================
# FILE PATHS
# =====================================================

PREDICTIONS_PATH = os.path.join(
    "data",
    "processed",
    "predictions.csv"
)

NEWS_PATH = os.path.join(
    "data",
    "processed",
    "live_news_risk.csv"
)

OUTPUT_PATH = os.path.join(
    "data",
    "processed",
    "final_georisk.csv"
)


# =====================================================
# LOAD DATA
# =====================================================

def load_data():

    predictions_df = pd.read_csv(
        PREDICTIONS_PATH
    )

    news_df = pd.read_csv(
        NEWS_PATH
    )

    return predictions_df, news_df


# =====================================================
# GET LATEST YEAR ONLY
# =====================================================

def latest_predictions(df):

    latest_year = df["Year"].max()

    latest_df = df[
        df["Year"] == latest_year
    ].copy()

    return latest_df


# =====================================================
# FUSION LOGIC
# =====================================================

def fuse_scores(predictions_df, news_df):

    predictions_df = latest_predictions(
        predictions_df
    )

    merged = pd.merge(
        predictions_df,
        news_df,
        on="Country",
        how="left"
    )

    # Fill missing news scores
    merged["News_Risk_Score"] = (
        merged["News_Risk_Score"]
        .fillna(0)
    )

    # =================================================
    # FINAL LIVE SCORE
    # =================================================

    merged["GeoRisk_Live_Score"] = (
        0.7 * merged["Conflict_Probability"]
        +
        0.3 * merged["News_Risk_Score"]
    )

    # =================================================
    # DYNAMIC RISK CLASSIFICATION
    # =================================================

    def classify(score):

        if score >= 0.75:
            return "Critical"

        elif score >= 0.50:
            return "High"

        elif score >= 0.25:
            return "Medium"

        else:
            return "Low"

    merged["Dynamic_Risk_Level"] = (
        merged["GeoRisk_Live_Score"]
        .apply(classify)
    )

    return merged


# =====================================================
# EMERGING THREAT DETECTION
# =====================================================

def detect_emerging_threats(df):

    conditions = (
        (df["News_Risk_Score"] >= 0.60)
        &
        (df["Conflict_Probability"] < 0.50)
    )

    df["Emerging_Threat"] = (
        conditions
    )

    return df


# =====================================================
# SAVE RESULTS
# =====================================================

def save_results(df):

    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nSaved final intelligence to:"
    )

    print(OUTPUT_PATH)


# =====================================================
# MAIN ENGINE
# =====================================================

def run_fusion_engine():

    print(
        "\nStarting GeoRiskAI Fusion Engine...\n"
    )

    predictions_df, news_df = load_data()

    final_df = fuse_scores(
        predictions_df,
        news_df
    )

    final_df = detect_emerging_threats(
        final_df
    )

    # =================================================
    # SORT BY LIVE RISK
    # =================================================

    final_df = (
        final_df.sort_values(
            "GeoRisk_Live_Score",
            ascending=False
        )
    )

    # =================================================
    # DISPLAY
    # =================================================

    display_cols = [
        "Country",
        "Conflict_Probability",
        "News_Risk_Score",
        "GeoRisk_Live_Score",
        "Dynamic_Risk_Level",
        "Emerging_Threat",
    ]

    print(
        final_df[
            display_cols
        ].head(20).to_string(index=False)
    )

    save_results(final_df)

    return final_df


# =====================================================
# EXECUTE
# =====================================================

if __name__ == "__main__":

    run_fusion_engine()