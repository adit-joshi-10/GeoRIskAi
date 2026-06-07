from src.intelligence.country_profiles import (
    get_country_profile
)

# =====================================================
# MARKET REACTION ENGINE
# =====================================================

def get_market_reactions(country):

    profile = get_country_profile(country)

    focus = profile["macro_focus"]

    safe_assets = profile["safe_assets"]

    risk_assets = profile["risk_assets"]

    # =================================================
    # POSITIVE MARKET MOVES
    # =================================================

    positive = []

    for asset in safe_assets:

        positive.append(

            (
                asset,

                f"+{round(1.5 + len(asset) * 0.1, 1)}%"
            )
        )

    # =================================================
    # NEGATIVE MARKET MOVES
    # =================================================

    negative = []

    for asset in risk_assets:

        negative.append(

            (
                asset,

                f"-{round(2.0 + len(asset) * 0.12, 1)}%"
            )
        )

    # =================================================
    # CONTEXTUAL ADDITIONS
    # =================================================

    if "Oil" in focus:

        positive.append(
            ("Crude Oil", "+4.2%")
        )

        negative.append(
            ("Airlines", "-3.8%")
        )

    if "Semiconductors" in focus:

        negative.append(
            ("Chip Manufacturing", "-5.1%")
        )

        positive.append(
            ("Cybersecurity", "+2.9%")
        )

    if "Defense" in focus:

        positive.append(
            ("Defense Contractors", "+3.7%")
        )

    # =================================================
    # RETURN
    # =================================================

    return {

        "positive": positive,

        "negative": negative
    }