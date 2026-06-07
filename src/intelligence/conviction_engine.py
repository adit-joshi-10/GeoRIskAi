from src.intelligence.country_profiles import (
    get_country_profile
)

# =====================================================
# AI CONVICTION ENGINE
# =====================================================

def get_conviction_score(

    georisk_score,

    news_score,

    conflict_probability,

    country="Global"
):

    profile = get_country_profile(country)

    focus = profile["macro_focus"]

    # =================================================
    # BASE SIGNALS
    # =================================================

    georisk_weight = georisk_score * 35

    news_weight = news_score * 25

    conflict_weight = conflict_probability * 40

    # =================================================
    # SIGNAL ALIGNMENT
    # =================================================

    alignment_bonus = 0

    if georisk_score > 0.7 and news_score > 0.7:

        alignment_bonus += 8

    if conflict_probability > 0.8:

        alignment_bonus += 10

    # =================================================
    # COUNTRY CONTEXT BONUS
    # =================================================

    context_bonus = 0

    if "Oil" in focus:

        context_bonus += 5

    if "Semiconductors" in focus:

        context_bonus += 4

    if "Defense" in focus:

        context_bonus += 4

    # =================================================
    # FINAL SCORE
    # =================================================

    raw_score = (

        georisk_weight +

        news_weight +

        conflict_weight +

        alignment_bonus +

        context_bonus
    )

    score = round(min(raw_score, 100))

    # =================================================
    # CONVICTION LEVELS
    # =================================================

    if score >= 90:

        level = "EXTREME CONVICTION"

        description = (
            "Multi-signal geopolitical alignment indicates "
            "very high escalation confidence across intelligence layers."
        )

    elif score >= 75:

        level = "HIGH CONVICTION"

        description = (
            "Strong cross-signal alignment detected between "
            "news activity, market stress, and escalation indicators."
        )

    elif score >= 55:

        level = "MODERATE CONVICTION"

        description = (
            "Geopolitical indicators remain elevated but "
            "signal consistency is partially fragmented."
        )

    else:

        level = "LOW CONVICTION"

        description = (
            "Insufficient escalation alignment detected "
            "across intelligence systems."
        )

    # =================================================
    # SIGNAL BREAKDOWN
    # =================================================

    breakdown = {

        "GeoRisk Alignment":
            round(georisk_weight),

        "News Confidence":
            round(news_weight),

        "Conflict Escalation":
            round(conflict_weight),

        "Macro Context":
            round(context_bonus + alignment_bonus)
    }

    # =================================================
    # RETURN
    # =================================================

    return {

        "score": score,

        "level": level,

        "description": description,

        "breakdown": breakdown
    }