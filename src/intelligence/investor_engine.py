"""
src/intelligence/investor_engine.py

Investor intelligence engine for GeoRiskAI.
Maps geopolitical instability to sector exposure.
"""

import pandas as pd
import os


# =====================================================
# FILE PATHS
# =====================================================

INPUT_PATH = os.path.join(
    "data",
    "processed",
    "final_georisk.csv"
)

OUTPUT_PATH = os.path.join(
    "data",
    "processed",
    "investor_intelligence.csv"
)


# =====================================================
# COUNTRY → SECTOR IMPACT MAPPING
# =====================================================

SECTOR_EXPOSURE = {

    "Taiwan": [
        "Semiconductors",
        "Electronics",
        "AI Hardware"
    ],

    "China": [
        "Manufacturing",
        "Supply Chains",
        "Technology"
    ],

    "Iran": [
        "Oil",
        "Energy",
        "Shipping"
    ],

    "Russia": [
        "Energy",
        "Natural Gas",
        "Oil"
    ],

    "Ukraine": [
        "Agriculture",
        "Food Supply",
        "Grain Exports"
    ],

    "Israel": [
        "Cybersecurity",
        "Defense Technology"
    ],

    "North Korea": [
        "Defense",
        "Regional Security"
    ],

    "United States": [
        "Global Markets",
        "Technology",
        "Defense"
    ],

    "India": [
        "IT Services",
        "Manufacturing",
        "Energy"
    ]
}


# =====================================================
# GENERATE INVESTOR IMPACT
# =====================================================

def generate_investor_signals(df):

    insights = []

    for _, row in df.iterrows():

        country = row["Country"]

        risk = row["Dynamic_Risk_Level"]

        score = row["GeoRisk_Live_Score"]

        sectors = SECTOR_EXPOSURE.get(
            country,
            ["Regional Markets"]
        )

        # =============================================
        # MARKET IMPACT LEVEL
        # =============================================

        if score >= 0.75:

            impact = "Severe"

        elif score >= 0.50:

            impact = "High"

        elif score >= 0.25:

            impact = "Moderate"

        else:

            impact = "Low"

        # =============================================
        # BUILD INVESTOR MESSAGE
        # =============================================

        message = (
            f"{country} shows {risk} geopolitical risk. "
            f"Potential exposure detected in: "
            f"{', '.join(sectors)}."
        )

        insights.append({

            "Country": country,

            "GeoRisk_Live_Score": round(
                score,
                3
            ),

            "Dynamic_Risk_Level": risk,

            "Affected_Sectors": ", ".join(
                sectors
            ),

            "Market_Impact": impact,

            "Investor_Alert": message
        })

    return pd.DataFrame(insights)


# =====================================================
# SAVE
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
        f"\nSaved investor intelligence to:"
    )

    print(OUTPUT_PATH)


# =====================================================
# MAIN ENGINE
# =====================================================

def run_investor_engine():

    print(
        "\nStarting Investor Intelligence Engine...\n"
    )

    df = pd.read_csv(INPUT_PATH)

    investor_df = generate_investor_signals(df)

    investor_df = (
        investor_df.sort_values(
            "GeoRisk_Live_Score",
            ascending=False
        )
    )

    print(
        investor_df.head(20).to_string(index=False)
    )

    save_results(investor_df)

    return investor_df


# =====================================================
# EXECUTE
# =====================================================

if __name__ == "__main__":

    run_investor_engine()