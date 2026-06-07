"""
src/features/feature_engineering.py

Creates ML-ready geopolitical forecasting features
from the country-year dataset.
"""

import pandas as pd
import os


# =========================
# FILE PATHS
# =========================

INPUT_PATH = os.path.join(
    "data",
    "processed",
    "country_year.csv"
)

OUTPUT_PATH = os.path.join(
    "data",
    "processed",
    "features.csv"
)


# =========================
# LOAD DATA
# =========================

def load_data() -> pd.DataFrame:

    print("\nLoading processed dataset...")

    df = pd.read_csv(INPUT_PATH)

    print(
        f"Dataset loaded: "
        f"{df.shape[0]:,} rows"
    )

    return df


# =========================
# FEATURE ENGINEERING
# =========================

def build_features(df: pd.DataFrame) -> pd.DataFrame:

    print("\nBuilding geopolitical forecasting features...")

    # Sort properly
    df = df.sort_values(
        ["Country", "Year"]
    )

    # =====================================
    # PREVIOUS YEAR CONFLICT
    # =====================================

    df["prev_conflict"] = (
        df.groupby("Country")["Conflict"]
        .shift(1)
        .fillna(0)
    )

    # =====================================
    # PREVIOUS YEAR DEATHS
    # =====================================

    df["prev_year_deaths"] = (
        df.groupby("Country")["total_deaths"]
        .shift(1)
        .fillna(0)
    )

    # =====================================
    # ROLLING CONFLICT AVERAGE
    # =====================================

    df["rolling_conflict_3yr"] = (
        df.groupby("Country")["Conflict"]
        .transform(
            lambda x:
            x.shift(1)
             .rolling(3, min_periods=1)
             .mean()
        )
        .fillna(0)
    )

    # =====================================
    # ROLLING DEATHS AVERAGE
    # =====================================

    df["rolling_deaths_3yr"] = (
        df.groupby("Country")["total_deaths"]
        .transform(
            lambda x:
            x.shift(1)
             .rolling(3, min_periods=1)
             .mean()
        )
        .fillna(0)
    )

    # =====================================
    # EVENT CHANGE
    # =====================================

    df["event_change"] = (
        df.groupby("Country")["conflict_events"]
        .diff()
        .fillna(0)
    )

    # =====================================
    # CONFLICT STREAK
    # =====================================

    streaks = []

    current_country = None
    streak = 0

    for _, row in df.iterrows():

        country = row["Country"]

        if country != current_country:
            streak = 0
            current_country = country

        if row["Conflict"] == 1:
            streak += 1
        else:
            streak = 0

        streaks.append(streak)

    df["conflict_streak"] = streaks

    # =====================================
    # FUTURE CONFLICT TARGET
    # =====================================

    df["Future_Conflict"] = (
        df.groupby("Country")["Conflict"]
        .shift(-1)
    )

    # Remove rows without future target
    df = df.dropna(
        subset=["Future_Conflict"]
    )

    df["Future_Conflict"] = (
        df["Future_Conflict"]
        .astype(int)
    )

    print("\nFeatures created successfully.")

    return df


# =========================
# SAVE FEATURES
# =========================

def save_features(df: pd.DataFrame):

    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nFeatures saved to:"
    )

    print(OUTPUT_PATH)


# =========================
# MAIN PIPELINE
# =========================

def run():

    df = load_data()

    df = build_features(df)

    save_features(df)

    return df


# =========================
# EXECUTE
# =========================

if __name__ == "__main__":

    df = run()

    print("\nFeature sample:\n")

    print(
        df.head(20).to_string(index=False)
    )