# =====================================================
# MARKET IMPACT ENGINE
# =====================================================

MARKET_RULES = {

    "Iran": {

        "bullish": [

            "Oil & Energy",
            "Gold",
            "Defense Stocks",
            "USD Safe Haven",
        ],

        "bearish": [

            "Airlines",
            "Shipping",
            "Emerging Markets",
        ]
    },

    "Russia": {

        "bullish": [

            "Oil",
            "Natural Gas",
            "Defense",
            "Gold",
        ],

        "bearish": [

            "European Equities",
            "Supply Chains",
            "Emerging Europe",
        ]
    },

    "China": {

        "bullish": [

            "Defense",
            "Cybersecurity",
            "Safe Haven Assets",
        ],

        "bearish": [

            "Global Manufacturing",
            "Tech Supply Chains",
            "Asian Markets",
        ]
    },

    "Taiwan": {

        "bullish": [

            "Defense",
            "US Chip Manufacturing",
            "Safe Haven Assets",
        ],

        "bearish": [

            "Semiconductors",
            "Asian Tech",
            "Global Electronics",
        ]
    },

    "Israel": {

        "bullish": [

            "Defense",
            "Oil",
            "Gold",
        ],

        "bearish": [

            "Middle East Tourism",
            "Airlines",
            "Regional Markets",
        ]
    }
}

# =====================================================
# MARKET IMPACT FUNCTION
# =====================================================

def get_market_impact(country):

    return MARKET_RULES.get(

        country,

        {

            "bullish": [

                "Defensive Assets",
                "Gold",
            ],

            "bearish": [

                "Risk Assets",
                "Emerging Markets",
            ]
        }
    )