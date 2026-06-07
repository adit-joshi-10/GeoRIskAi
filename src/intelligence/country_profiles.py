# =====================================================
# COUNTRY PERSONALITY ENGINE
# =====================================================

COUNTRY_PROFILES = {

    "China": {

        "type": "Manufacturing Superpower",

        "macro_focus": [
            "Semiconductors",
            "Exports",
            "AI Infrastructure",
            "Supply Chains"
        ],

        "safe_assets": [
            "Gold",
            "State-Owned Banks",
            "Defense"
        ],

        "risk_assets": [
            "Tech Exports",
            "Consumer Electronics",
            "Shipping"
        ],

        "market_sensitivity": [
            "Taiwan Conflict",
            "US Sanctions",
            "Trade Restrictions"
        ],

        "capital_behavior": "Regional capital rotation into defensive Asian assets.",

        "strategic_theme":
            "Global semiconductor dependency increases systemic market vulnerability.",

        "alert_style":
            "Supply-chain fragmentation risk escalating.",

        "investor_bias":
            "Defensive positioning in export-sensitive sectors."
    },

    "Iran": {

        "type": "Energy Chokepoint",

        "macro_focus": [
            "Oil",
            "Shipping",
            "Middle-East Security"
        ],

        "safe_assets": [
            "Oil Producers",
            "Gold",
            "Defense Stocks"
        ],

        "risk_assets": [
            "Airlines",
            "Shipping",
            "Tourism"
        ],

        "market_sensitivity": [
            "Strait of Hormuz",
            "Oil Shock",
            "Military Escalation"
        ],

        "capital_behavior":
            "Flight toward commodities and defensive energy exposure.",

        "strategic_theme":
            "Energy corridor instability threatening global inflation stability.",

        "alert_style":
            "Oil supply disruption probability rising.",

        "investor_bias":
            "Increase commodity hedge exposure."
    },

    "Russia": {

        "type": "Sanctioned Energy Power",

        "macro_focus": [
            "Energy",
            "Sanctions",
            "European Markets"
        ],

        "safe_assets": [
            "Energy",
            "Gold",
            "Defense"
        ],

        "risk_assets": [
            "European Industrials",
            "Banks",
            "Imports"
        ],

        "market_sensitivity": [
            "Sanctions",
            "NATO Escalation",
            "Energy Exports"
        ],

        "capital_behavior":
            "European capital rotating toward defensive commodity sectors.",

        "strategic_theme":
            "Long-term fragmentation of European energy dependency.",

        "alert_style":
            "Sanctions escalation pressure increasing.",

        "investor_bias":
            "Favor commodity resilience and defense sectors."
    },

    "Taiwan": {

        "type": "Semiconductor Epicenter",

        "macro_focus": [
            "Semiconductors",
            "AI Chips",
            "Global Tech Supply"
        ],

        "safe_assets": [
            "Defense",
            "Cybersecurity",
            "Gold"
        ],

        "risk_assets": [
            "Chip Manufacturing",
            "Global Tech",
            "Exports"
        ],

        "market_sensitivity": [
            "China Tensions",
            "Naval Activity",
            "Supply Chains"
        ],

        "capital_behavior":
            "Capital seeking semiconductor alternatives and US tech resilience.",

        "strategic_theme":
            "Chip concentration risk becoming systemic to AI economies.",

        "alert_style":
            "Semiconductor disruption risk rising.",

        "investor_bias":
            "Reduce concentrated chip supply exposure."
    },

    "Israel": {

        "type": "Regional Military Flashpoint",

        "macro_focus": [
            "Defense",
            "Cybersecurity",
            "Regional Stability"
        ],

        "safe_assets": [
            "Defense",
            "Cybersecurity",
            "Oil"
        ],

        "risk_assets": [
            "Tourism",
            "Regional Equities",
            "Airlines"
        ],

        "market_sensitivity": [
            "Regional Spillover",
            "Military Escalation",
            "Iran Proxy Activity"
        ],

        "capital_behavior":
            "Defensive capital migration toward military and cybersecurity sectors.",

        "strategic_theme":
            "Regional instability driving persistent defense-sector expansion.",

        "alert_style":
            "Cross-border escalation risk increasing.",

        "investor_bias":
            "Increase defense and cybersecurity exposure."
    },

    "India": {

        "type": "Emerging Economic Power",

        "macro_focus": [
            "Manufacturing",
            "Technology",
            "Infrastructure"
        ],

        "safe_assets": [
            "Infrastructure",
            "Domestic Consumption",
            "Energy"
        ],

        "risk_assets": [
            "Exports",
            "Border Regions",
            "Currency-sensitive sectors"
        ],

        "market_sensitivity": [
            "Border Tensions",
            "Oil Prices",
            "Regional Stability"
        ],

        "capital_behavior":
            "Emerging market inflows remain resilient amid regional volatility.",

        "strategic_theme":
            "India emerging as alternative manufacturing destination.",

        "alert_style":
            "Regional security monitoring elevated.",

        "investor_bias":
            "Favor infrastructure and domestic growth sectors."
    }
}

# =====================================================
# DEFAULT PROFILE
# =====================================================

DEFAULT_PROFILE = {

    "type": "General Economy",

    "macro_focus": [
        "Regional Stability",
        "Trade",
        "Inflation"
    ],

    "safe_assets": [
        "Gold",
        "Utilities",
        "Defense"
    ],

    "risk_assets": [
        "Growth Stocks",
        "Travel",
        "Exports"
    ],

    "market_sensitivity": [
        "Political Instability",
        "Commodity Prices"
    ],

    "capital_behavior":
        "Defensive capital positioning increasing.",

    "strategic_theme":
        "Macroeconomic uncertainty affecting investor confidence.",

    "alert_style":
        "Geopolitical volatility elevated.",

    "investor_bias":
        "Maintain diversified defensive exposure."
}

# =====================================================
# GET PROFILE
# =====================================================

def get_country_profile(country):

    return COUNTRY_PROFILES.get(

        country,

        DEFAULT_PROFILE
    )