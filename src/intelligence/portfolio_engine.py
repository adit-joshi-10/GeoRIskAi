# =====================================================
# PORTFOLIO RISK ENGINE
# =====================================================

PORTFOLIO_SIGNALS = {

    "Critical": {

        "safe": [

            "Gold",
            "USD",
            "Defense Stocks",
            "Oil",
        ],

        "risk": [

            "Airlines",
            "Emerging Markets",
            "Tourism",
            "Shipping",
        ]
    },

    "High": {

        "safe": [

            "Healthcare",
            "Utilities",
            "Cybersecurity",
        ],

        "risk": [

            "Growth Stocks",
            "Tech Supply Chains",
            "High Beta Assets",
        ]
    },

    "Medium": {

        "safe": [

            "Diversified ETFs",
            "Consumer Staples",
        ],

        "risk": [

            "Volatile Assets",
        ]
    },

    "Low": {

        "safe": [

            "Broad Markets",
            "Index Funds",
        ],

        "risk": [

            "Minimal Immediate Risk",
        ]
    }
}

# =====================================================
# GET PORTFOLIO SIGNALS
# =====================================================

def get_portfolio_signals(risk_level):

    return PORTFOLIO_SIGNALS.get(

        risk_level,

        PORTFOLIO_SIGNALS["Medium"]
    )