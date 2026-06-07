"""
AI Analyst Engine
CLEAN TEXT VERSION
"""

import pandas as pd


# =====================================================
# PATHS
# =====================================================

FINAL_PATH = "data/processed/final_georisk.csv"

OUTPUT_PATH = "data/processed/ai_briefings.csv"


# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(FINAL_PATH)


# =====================================================
# CLEAN ANALYSIS GENERATOR
# =====================================================

def generate_analysis(row):

    country = row["Country"]

    risk = row["Dynamic_Risk_Level"]

    score = row["GeoRisk_Live_Score"]

    # =================================================
    # COUNTRY SPECIALIZATION
    # =================================================

    sector_focus = {

        "Iran":
        "oil exports and sanctions",

        "Ukraine":
        "infrastructure and regional security",

        "Russia":
        "energy exports and global trade",

        "China":
        "manufacturing and supply chains",

        "Taiwan":
        "semiconductor production",

        "Pakistan":
        "political stability and debt exposure",

        "Israel":
        "regional conflict escalation",

        "Syria":
        "civil conflict and reconstruction"
    }

    focus = sector_focus.get(
        country,
        "regional market stability"
    )

    # =================================================
    # RISK LOGIC
    # =================================================

    if risk == "Critical":

        return (
            f"{country} is currently experiencing "
            f"severe geopolitical instability with "
            f"elevated escalation indicators.\n\n"

            f"The GeoRisk score of {score:.2f} "
            f"suggests substantial investor exposure "
            f"and high regional volatility.\n\n"

            f"Current intelligence signals indicate "
            f"possible disruption risks in "
            f"{focus}.\n\n"

            f"Investors should avoid aggressive "
            f"exposure and closely monitor "
            f"real-time developments."
        )

    elif risk == "High":

        return (
            f"{country} currently demonstrates "
            f"elevated geopolitical tension.\n\n"

            f"The GeoRisk score of {score:.2f} "
            f"indicates increased uncertainty "
            f"for investors.\n\n"

            f"Potential pressure may emerge in "
            f"{focus}.\n\n"

            f"Cautious monitoring is advised."
        )

    elif risk == "Medium":

        return (
            f"{country} currently shows moderate "
            f"geopolitical volatility.\n\n"

            f"The GeoRisk score of {score:.2f} "
            f"indicates manageable investor risk.\n\n"

            f"Some fluctuations may occur in "
            f"{focus}, though overall conditions "
            f"remain relatively stable."
        )

    return (

        f"{country} currently maintains "
        f"stable geopolitical conditions.\n\n"

        f"The GeoRisk score of {score:.2f} "
        f"reflects relatively low escalation risk.\n\n"

        f"Investor exposure appears manageable "
        f"under current forecasting conditions."
    )


# =====================================================
# GENERATE OUTPUT
# =====================================================

analyses = []

for _, row in df.iterrows():

    analyses.append({

        "Country": row["Country"],

        "AI_Analysis":
        generate_analysis(row)
    })


# =====================================================
# SAVE
# =====================================================

output_df = pd.DataFrame(analyses)

output_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nAI briefings generated successfully.")

print(
    f"\nSaved to: {OUTPUT_PATH}"
)