# =====================================================
# GEOPOLITICAL NEWS FILTER ENGINE
# =====================================================

# =====================================================
# REQUIRED KEYWORDS
# =====================================================

GEO_KEYWORDS = [

    "war",
    "conflict",
    "military",
    "missile",
    "army",
    "border",
    "terror",
    "terrorism",
    "sanctions",
    "geopolitical",
    "security",
    "nuclear",
    "government",
    "rebels",
    "violence",
    "airstrike",
    "defense",
    "troops",
    "crisis",
    "civil war",
    "diplomatic",
    "foreign policy",
    "militant",
    "weapon",
    "attack",
    "ceasefire",
    "insurgency",
    "hostage",
    "navy",
    "explosion",
]

# =====================================================
# BLACKLIST KEYWORDS
# =====================================================

BLACKLIST = [

    "cricket",
    "football",
    "soccer",
    "basketball",
    "tennis",
    "match",
    "t20",
    "ipl",
    "olympics",
    "movie",
    "film",
    "actor",
    "actress",
    "celebrity",
    "music",
    "song",
    "festival",
    "fashion",
    "crypto",
    "bitcoin",
    "iphone",
    "android",
    "gaming",
    "esports",
    "stock market",
    "startup",
    "AI transformation",
    "commonwealth games",
]

# =====================================================
# FILTER ENGINE
# =====================================================

def is_relevant_geopolitical(article):

    title = article.get(
        "title",
        ""
    ).lower()

    description = article.get(
        "description",
        ""
    ).lower()

    text = f"{title} {description}"

    # =============================================
    # BLACKLIST CHECK
    # =============================================

    for bad in BLACKLIST:

        if bad in text:

            return False

    # =============================================
    # GEO SCORE
    # =============================================

    score = 0

    for kw in GEO_KEYWORDS:

        if kw in text:

            score += 1

    # =============================================
    # MINIMUM THRESHOLD
    # =============================================

    return score >= 1