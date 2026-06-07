from src.intelligence.country_profiles import (
    get_country_profile
)

# =====================================================
# CAPITAL FLOW ENGINE
# =====================================================

def get_capital_flows(country):

    profile = get_country_profile(country)

    safe_assets = profile["safe_assets"]

    risk_assets = profile["risk_assets"]

    capital_behavior = profile["capital_behavior"]

    focus = profile["macro_focus"]

    # =================================================
    # BASE FLOWS
    # =================================================

    inflows = []

    outflows = []

    # =================================================
    # SAFE ASSET INFLOWS
    # =================================================

    for asset in safe_assets:

        inflows.append(asset)

    # =================================================
    # RISK ASSET OUTFLOWS
    # =================================================

    for asset in risk_assets:

        outflows.append(asset)

    # =================================================
    # CONTEXTUAL COUNTRY LOGIC
    # =================================================

    if "Oil" in focus:

        inflows.extend([
            "Energy ETFs",
            "Commodity Futures",
            "Oil Producers"
        ])

        outflows.extend([
            "Airlines",
            "Travel Equities"
        ])

    if "Semiconductors" in focus:

        inflows.extend([
            "Cybersecurity",
            "US Chip Alternatives"
        ])

        outflows.extend([
            "Global Hardware Supply Chains"
        ])

    if "Defense" in focus:

        inflows.extend([
            "Defense Contractors",
            "Military Technology"
        ])

    if "Infrastructure" in focus:

        inflows.extend([
            "Domestic Infrastructure",
            "Construction"
        ])

    # =================================================
    # REMOVE DUPLICATES
    # =================================================

    inflows = list(dict.fromkeys(inflows))

    outflows = list(dict.fromkeys(outflows))

    # =================================================
    # RETURN
    # =================================================

    return {

        "sentiment": capital_behavior,

        "inflows": inflows,

        "outflows": outflows
    }