from src.intelligence.country_profiles import (
    get_country_profile
)

# =====================================================
# TREND FORECAST ENGINE
# =====================================================

def get_trend_forecast(country):

    profile = get_country_profile(country)

    focus = profile["macro_focus"]

    sensitivities = profile["market_sensitivity"]

    strategic_theme = profile["strategic_theme"]

    # =================================================
    # DEFAULT VALUES
    # =================================================

    trend = "Moderate Escalation Risk"

    stability = "Volatile"

    probability = "58%"

    drivers = []

    # =================================================
    # CONTEXTUAL FORECASTING
    # =================================================

    if "Oil" in focus:

        trend = "Energy Market Escalation"

        stability = "Highly Volatile"

        probability = "81%"

        drivers.extend([

            "Oil corridor instability increasing.",

            "Commodity inflation pressures rising.",

            "Shipping-risk premiums expanding."
        ])

    if "Semiconductors" in focus:

        trend = "Technology Supply Chain Stress"

        stability = "Fragile"

        probability = "76%"

        drivers.extend([

            "AI infrastructure dependency increasing.",

            "Chip-supply concentration risk elevated.",

            "Regional military sensitivity expanding."
        ])

    if "Defense" in focus:

        trend = "Regional Security Escalation"

        stability = "Unstable"

        probability = "72%"

        drivers.extend([

            "Defense-sector expansion accelerating.",

            "Cross-border geopolitical pressure increasing.",

            "Cybersecurity demand strengthening."
        ])

    if "Infrastructure" in focus:

        trend = "Emerging Market Resilience"

        stability = "Moderately Stable"

        probability = "49%"

        drivers.extend([

            "Industrial diversification trends improving.",

            "Domestic infrastructure momentum strengthening.",

            "Regional growth outlook remains resilient."
        ])

    # =================================================
    # MARKET SENSITIVITY DRIVERS
    # =================================================

    for sensitivity in sensitivities:

        drivers.append(
            f"Markets remain reactive to {sensitivity.lower()} developments."
        )

    # =================================================
    # STRATEGIC OVERLAY
    # =================================================

    drivers.append(
        strategic_theme
    )

    # =================================================
    # REMOVE DUPLICATES
    # =================================================

    drivers = list(dict.fromkeys(drivers))

    # =================================================
    # RETURN
    # =================================================

    return {

        "trend": trend,

        "stability": stability,

        "probability": probability,

        "drivers": drivers
    }