import streamlit as st

from src.data.market.market_feed import (
    fetch_live_market_signals
)

# =====================================================
# GLOBAL SIGNAL BAR
# =====================================================

def render_global_signal_bar():

    # =================================================
    # FETCH LIVE DATA
    # =================================================

    df = fetch_live_market_signals()

    if df.empty:

        st.warning(
            "Live market feed unavailable."
        )

        return

    # =================================================
    # BUILD SIGNAL CARDS
    # =================================================

    cards_html = ""

    for _, row in df.iterrows():

        move_color = (
            "#00ff88"
            if row["change_pct"] >= 0
            else "#ff3b5c"
        )

        arrow = (
            "▲"
            if row["change_pct"] >= 0
            else "▼"
        )

        cards_html += (

            f'<div style="'
            f'min-width:145px;'
            f'background:#06111c;'
            f'border:1px solid #0d3050;'
            f'border-top:2px solid {row["color"]};'
            f'padding:12px 14px;'
            f'border-radius:10px;' 
            f'box-shadow:0 0 12px rgba(0,0,0,.25);'
            f'transition:.2s ease;">'

            # =========================================
            # ASSET NAME
            # =========================================

            f'<div style="'
            f'font-size:10px;'
            f'letter-spacing:2px;'
            f'color:#3a6070;'
            f'font-family:monospace;'
            f'margin-bottom:8px;'
            f'text-transform:uppercase;">'

            f'{row["name"]}'

            f'</div>'

            # =========================================
            # LIVE PRICE
            # =========================================

            f'<div style="'
            f'font-size:21px;'
            f'font-weight:700;'
            f'color:#e2eef5;'
            f'font-family:monospace;'
            f'margin-bottom:4px;">'

            f'{row["value"]:,.2f}'

            f'</div>'

            # =========================================
            # UNIT
            # =========================================

            f'<div style="'
            f'font-size:10px;'
            f'color:#4d6b80;'
            f'font-family:monospace;'
            f'letter-spacing:1px;'
            f'margin-bottom:6px;">'

            f'{row["unit"]}'

            f'</div>'

            # =========================================
            # % CHANGE
            # =========================================

            f'<div style="'
            f'font-size:11px;'
            f'color:{move_color};'
            f'font-family:monospace;'
            f'font-weight:700;">'

            f'{arrow} {abs(row["change_pct"]):.2f}%'

            f'</div>'

            # =========================================
            # LAST UPDATED
            # =========================================

            f'<div style="'
            f'font-size:9px;'
            f'color:#355060;'
            f'font-family:monospace;'
            f'margin-top:7px;">'

            f'LIVE'

            f'</div>'

            f'</div>'
        )

    # =================================================
    # WRAPPER
    # =================================================

    wrapper = (

    '<div style="'
    'display:grid;'
    'grid-template-columns:repeat(auto-fit,minmax(145px,1fr));'
    'gap:12px;'
    'padding:4px 0 10px 0;'
    'margin:12px 0 18px 0;">'

    + cards_html +

    '</div>'
)

    # =================================================
    # RENDER
    # =================================================

    st.markdown(
        wrapper,
        unsafe_allow_html=True
    )