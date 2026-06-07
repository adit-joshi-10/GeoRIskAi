import yfinance as yf
import pandas as pd
from datetime import datetime

from src.data.market.market_config import (
    ASSETS,
    DEFAULT_SIGNAL_ORDER
)

# =====================================================
# FETCH LIVE MARKET SIGNALS
# =====================================================

def fetch_live_market_signals():

    signals = []

    for asset_name in DEFAULT_SIGNAL_ORDER:

        config = ASSETS.get(asset_name)

        if not config:
            continue

        symbol = config["symbol"]

        try:

            ticker = yf.Ticker(symbol)

            hist = ticker.history(period="2d")

            if hist.empty or len(hist) < 2:
                continue

            latest_close = float(hist["Close"].iloc[-1])

            previous_close = float(hist["Close"].iloc[-2])

            change_pct = (
                (
                    latest_close
                    - previous_close
                )
                / previous_close
            ) * 100

            signals.append({

                "name": asset_name,

                "label": config["label"],

                "symbol": symbol,

                "value": round(latest_close, 2),

                "change_pct": round(change_pct, 2),

                "unit": config["unit"],

                "color": config["color"],

                "category": config["category"],

                "timestamp": datetime.utcnow().strftime(
                    "%Y-%m-%d %H:%M:%S UTC"
                )

            })

        except Exception as e:

            print(
                f"[MARKET FEED ERROR] "
                f"{asset_name}: {e}"
            )

    return pd.DataFrame(signals)