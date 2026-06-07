"""
src/data_loader.py

Loads and cleans the geopolitical event dataset.
Builds a clean country-year dataset for ML training.
"""

import pandas as pd
import os


# =========================
# FILE PATHS
# =========================

RAW_PATH = os.path.join(
    "data",
    "raw",
    "GEDEvent_v25_1.csv"
)

PROCESSED_PATH = os.path.join(
    "data",
    "processed",
    "country_year.csv"
)


# =========================
# LOAD RAW DATA
# =========================

def load_events() -> pd.DataFrame:

    print("\nLoading raw dataset...")

    df = pd.read_csv(
        RAW_PATH,
        low_memory=False
    )

    print(
        f"Raw data loaded: "
        f"{df.shape[0]:,} rows x "
        f"{df.shape[1]} columns"
    )

    return df


# =========================
# BUILD COUNTRY-YEAR TABLE
# =========================

def make_country_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw event-level data into one row per country per year.

    Features:
    - total_deaths
    - conflict_events
    - Conflict (binary target)
    """

    print("\nBuilding country-year conflict table...")

    # Keep only required columns
    df = df[[
        "country",
        "year",
        "best"
    ]].copy()

    # Remove missing values
    df = df.dropna()

    # Ensure numeric
    df["best"] = pd.to_numeric(
        df["best"],
        errors="coerce"
    ).fillna(0)

    # =========================
    # GROUP BY COUNTRY + YEAR
    # =========================

    cy = (
        df.groupby(["country", "year"])
        .agg(
            total_deaths=("best", "sum"),
            conflict_events=("best", "count"),
        )
        .reset_index()
    )

    # =========================
    # CREATE TARGET LABEL
    # =========================

    # Conflict = 1 if deaths >= 25
    # Removes tiny/noisy events

    cy["Conflict"] = (
        cy["total_deaths"] >= 25
    ).astype(int)

    # =========================
    # CLEAN COLUMN NAMES
    # =========================

    cy = cy.rename(
        columns={
            "country": "Country",
            "year": "Year"
        }
    )

    # =========================
    # CREATE FULL COUNTRY-YEAR GRID
    # =========================

    all_countries = cy["Country"].unique()

    all_years = range(
        int(cy["Year"].min()),
        int(cy["Year"].max()) + 1
    )

    full_index = pd.MultiIndex.from_product(
        [all_countries, all_years],
        names=["Country", "Year"]
    )

    cy = (
        cy.set_index(["Country", "Year"])
        .reindex(full_index, fill_value=0)
        .reset_index()
    )

    # =========================
    # FINAL INFO
    # =========================

    print(
        f"\nCountry-year table created:"
    )

    print(
        f"Rows: {cy.shape[0]:,}"
    )

    print(
        f"Countries: {cy['Country'].nunique()}"
    )

    print(
        f"Years: "
        f"{cy['Year'].min()} - "
        f"{cy['Year'].max()}"
    )

    print(
        f"Conflict rate: "
        f"{cy['Conflict'].mean():.2%}"
    )

    return cy


# =========================
# SAVE DATASET
# =========================

def save_processed_data(df: pd.DataFrame):

    os.makedirs(
        os.path.dirname(PROCESSED_PATH),
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_PATH,
        index=False
    )

    print(
        f"\nProcessed dataset saved to:"
    )

    print(PROCESSED_PATH)


# =========================
# MAIN PIPELINE
# =========================

def run() -> pd.DataFrame:

    raw = load_events()

    cy = make_country_year(raw)

    save_processed_data(cy)

    return cy


# =========================
# EXECUTE
# =========================

if __name__ == "__main__":

    df = run()

    print("\nSample rows:\n")

    print(
        df.head(10).to_string(index=False)
    )

    print("\nCountries with conflict:\n")

    print(
        df[df["Conflict"] == 1]
        .head(10)
        .to_string(index=False)
    )