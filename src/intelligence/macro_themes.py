from src.intelligence.country_profiles import (
    get_country_profile
)

# =====================================================
# MACRO THEMES ENGINE
# =====================================================

def get_macro_themes(country):

    profile = get_country_profile(country)

    focus = profile["macro_focus"]

    strategic_theme = profile["strategic_theme"]

    sensitivities = profile["market_sensitivity"]

    themes = []

    # =================================================
    # PRIMARY STRATEGIC THEME
    # =================================================

    themes.append({

        "theme":
            "Primary Strategic Narrative",

        "description":
            strategic_theme
    })

    # =================================================
    # CONTEXTUAL THEMES
    # =================================================

    if "Oil" in focus:

        themes.append({

            "theme":
                "Global Energy Shock Risk",

            "description":
                "Commodity volatility and shipping instability "
                "continue to pressure inflation-sensitive markets."
        })

    if "Semiconductors" in focus:

        themes.append({

            "theme":
                "AI Infrastructure Dependency",

            "description":
                "Concentrated semiconductor manufacturing exposure "
                "is increasing systemic technology-market fragility."
        })

    if "Defense" in focus:

        themes.append({

            "theme":
                "Defense Expansion Cycle",

            "description":
                "Persistent geopolitical fragmentation is accelerating "
                "global military and cybersecurity investment."
        })

    if "Infrastructure" in focus:

        themes.append({

            "theme":
                "Emerging Market Industrial Rotation",

            "description":
                "Global manufacturing diversification trends are "
                "supporting infrastructure-heavy emerging economies."
        })

    # =================================================
    # MARKET SENSITIVITY THEMES
    # =================================================

    for sensitivity in sensitivities:

        themes.append({

            "theme":
                sensitivity,

            "description":
                f"Markets remain highly sensitive to developments related to {sensitivity.lower()}."
        })

    # =================================================
    # REMOVE DUPLICATES
    # =================================================

    unique = []

    seen = set()

    for theme in themes:

        key = theme["theme"]

        if key not in seen:

            unique.append(theme)

            seen.add(key)

    # =================================================
    # RETURN
    # =================================================

    return unique