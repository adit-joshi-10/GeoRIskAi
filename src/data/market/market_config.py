# =====================================================
# MARKET CONFIGURATION
# =====================================================

# Central asset registry for GeoRiskAI
# All live market feeds reference this file


ASSETS = {

    # =================================================
    # ENERGY
    # =================================================

    "OIL": {

        "symbol": "BZ=F",
        "label": "Brent Crude",
        "unit": "USD/bbl",
        "color": "#ff9500",
        "category": "Energy"

    },

    "NATGAS": {

        "symbol": "NG=F",
        "label": "Natural Gas",
        "unit": "USD/MMBtu",
        "color": "#ff6a00",
        "category": "Energy"

    },

    # =================================================
    # SAFE HAVENS
    # =================================================

    "GOLD": {

        "symbol": "GC=F",
        "label": "Gold Spot",
        "unit": "USD/oz",
        "color": "#ffe600",
        "category": "Safe Haven"

    },

    "SILVER": {

        "symbol": "SI=F",
        "label": "Silver",
        "unit": "USD/oz",
        "color": "#c0c0c0",
        "category": "Safe Haven"

    },

    # =================================================
    # VOLATILITY
    # =================================================

    "VIX": {

        "symbol": "^VIX",
        "label": "Volatility Index",
        "unit": "INDEX",
        "color": "#ff3b5c",
        "category": "Volatility"

    },

    # =================================================
    # FX / DOLLAR
    # =================================================

    "DXY": {

        "symbol": "DX-Y.NYB",
        "label": "US Dollar Index",
        "unit": "INDEX",
        "color": "#00e5ff",
        "category": "Forex"

    },

    # =================================================
    # CRYPTO
    # =================================================

    "BTC": {

        "symbol": "BTC-USD",
        "label": "Bitcoin",
        "unit": "USD",
        "color": "#00ff88",
        "category": "Crypto"

    },

    "ETH": {

        "symbol": "ETH-USD",
        "label": "Ethereum",
        "unit": "USD",
        "color": "#8b5cf6",
        "category": "Crypto"

    },

    # =================================================
    # EQUITIES
    # =================================================

    "S&P": {

        "symbol": "ES=F",
        "label": "S&P Futures",
        "unit": "FUTURES",
        "color": "#00b8d4",
        "category": "Equities"

    },

    "NASDAQ": {

        "symbol": "NQ=F",
        "label": "Nasdaq Futures",
        "unit": "FUTURES",
        "color": "#0078ff",
        "category": "Equities"

    }

}


# =====================================================
# REFRESH SETTINGS
# =====================================================

REFRESH_INTERVAL_SECONDS = 30

CACHE_TIMEOUT_SECONDS = 25


# =====================================================
# DEFAULT DISPLAY ORDER
# =====================================================

DEFAULT_SIGNAL_ORDER = [

    "OIL",
    "GOLD",
    "VIX",
    "DXY",
    "BTC",
    "S&P"

]