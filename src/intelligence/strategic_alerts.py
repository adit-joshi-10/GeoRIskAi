from src.intelligence.country_profiles import (
    get_country_profile
)

# =====================================================
# STRATEGIC ALERT ENGINE
# =====================================================

def get_strategic_alert(country):

    profile = get_country_profile(country)

    alert_style = profile["alert_style"]

    strategic_theme = profile["strategic_theme"]

    investor_bias = profile["investor_bias"]

    sensitivities = profile["market_sensitivity"]

    # =================================================
    # COUNTRY-SPECIFIC LOGIC
    # =================================================

    if country == "Iran":

        return {

            "title":
                "STRAIT OF HORMUZ ESCALATION RISK",

            "message":
                "Naval instability near critical oil-shipping corridors "
                "is increasing energy-market volatility and raising "
                "global inflationary pressure risks.",

            "action":
                "Increase commodity hedges and monitor oil-sensitive sectors."
        }

    elif country == "Taiwan":

        return {

            "title":
                "SEMICONDUCTOR SUPPLY CHAIN FRAGILITY",

            "message":
                "Regional military pressure around Taiwan is elevating "
                "systemic semiconductor supply disruption probability "
                "across global AI and technology markets.",

            "action":
                "Reduce concentrated chip-supply exposure and increase defensive tech positioning."
        }

    elif country == "Russia":

        return {

            "title":
                "SANCTIONS ESCALATION PRESSURE",

            "message":
                "Expanded geopolitical fragmentation risks continue to "
                "pressure European energy stability and commodity-linked markets.",

            "action":
                "Favor defensive commodity exposure and monitor European industrial weakness."
        }

    elif country == "Israel":

        return {

            "title":
                "REGIONAL SPILLOVER RISK ELEVATED",

            "message":
                "Cross-border escalation dynamics are increasing the probability "
                "of wider regional instability affecting defense and energy markets.",

            "action":
                "Increase defense-sector monitoring and maintain geopolitical hedges."
        }

    elif country == "China":

        return {

            "title":
                "SUPPLY CHAIN FRAGMENTATION RISK",

            "message":
                "Trade restrictions and regional geopolitical tensions are "
                "increasing systemic export and manufacturing uncertainty.",

            "action":
                "Reduce exposure to export-sensitive sectors and monitor semiconductor supply chains."
        }

    elif country == "India":

        return {

            "title":
                "REGIONAL SECURITY MONITORING ELEVATED",

            "message":
                "Border-security sensitivity and commodity-price volatility "
                "remain key variables affecting regional market stability.",

            "action":
                "Favor infrastructure and domestic resilience sectors."
        }

    # =================================================
    # DEFAULT CONTEXTUAL ALERT
    # =================================================

    return {

        "title":
            alert_style.upper(),

        "message":
            strategic_theme,

        "action":
            investor_bias
    }