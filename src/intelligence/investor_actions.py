from src.intelligence.country_profiles import (
    get_country_profile
)

# =====================================================
# INVESTOR POSITIONING ENGINE
# =====================================================

def get_investor_actions(country):

    profile = get_country_profile(country)

    focus = profile["macro_focus"]

    investor_bias = profile["investor_bias"]

    safe_assets = profile["safe_assets"]

    risk_assets = profile["risk_assets"]

    actions = []

    # =================================================
    # PRIMARY POSITIONING
    # =================================================

    actions.append(
        investor_bias
    )

    # =================================================
    # SAFE ASSET POSITIONING
    # =================================================

    for asset in safe_assets:

        actions.append(
            f"Increase exposure to {asset.lower()} sectors."
        )

    # =================================================
    # RISK REDUCTION
    # =================================================

    for asset in risk_assets[:2]:

        actions.append(
            f"Reduce concentration in {asset.lower()} assets."
        )

    # =================================================
    # CONTEXTUAL LOGIC
    # =================================================

    if "Oil" in focus:

        actions.extend([

            "Increase inflation-hedge positioning.",

            "Monitor commodity-linked currencies.",

            "Favor energy-sector resilience."
        ])

    if "Semiconductors" in focus:

        actions.extend([

            "Diversify semiconductor supply-chain exposure.",

            "Increase cybersecurity allocation.",

            "Reduce single-region chip dependency."
        ])

    if "Defense" in focus:

        actions.extend([

            "Increase defense-contractor monitoring.",

            "Favor geopolitical hedge allocations."
        ])

    if "Infrastructure" in focus:

        actions.extend([

            "Favor domestic infrastructure growth.",

            "Increase industrial manufacturing exposure."
        ])

    # =================================================
    # REMOVE DUPLICATES
    # =================================================

    actions = list(dict.fromkeys(actions))

    # =================================================
    # RETURN
    # =================================================

    return actions