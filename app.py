import streamlit as st
    
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time
import streamlit as st
from streamlit_option_menu import option_menu

if "mobile_mode" not in st.session_state:
    st.session_state.mobile_mode = False
from src.intelligence.news_engine import fetch_country_news

from src.ui.intelligence_core import (
    render_intelligence_core
)
from src.ui.layout_engine import (

    initialize_layout,

    create_layout,

    render_panel_toggle
)
from src.intelligence.market_impact import (
    get_market_impact
)
from src.intelligence.investor_actions import (
    get_investor_actions
)
from src.intelligence.trend_forecast import (
    get_trend_forecast
)
from src.intelligence.portfolio_engine import (
    get_portfolio_signals
)
from src.intelligence.market_reactions import (
    get_market_reactions
)
from src.intelligence.capital_flows import (
    get_capital_flows
)
from src.intelligence.strategic_alerts import (
    get_strategic_alert
)
from src.intelligence.macro_themes import (
    get_macro_themes
)
from src.intelligence.conviction_engine import (
    get_conviction_score
)
from src.ui.tabs.tab_global import (
    render_global_tab
)
from src.ui.tabs.tab_ai import (
    render_ai_tab
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="GeoRiskAI — Geopolitical Intelligence",
    page_icon="🛰",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

/* ===== TAB CONTAINER ===== */

.stTabs [data-baseweb="tab-list"] {

    gap: 10px;
    overflow-x: auto;
    scrollbar-width: none;
    padding-bottom: 10px;
}

.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {

    display: none;
}

/* ===== INDIVIDUAL TAB ===== */

.stTabs [data-baseweb="tab"] {

    height: 55px;

    white-space: nowrap;

    border-radius: 15px;

    background:
        rgba(0, 15, 30, 0.85);

    border:
        1px solid rgba(0,255,255,0.15);

    color:
        #d7f7ff;

    font-weight:
        600;

    padding:
        12px 20px;

    transition:
        all 0.3s ease;
}

/* ===== HOVER EFFECT ===== */

.stTabs [data-baseweb="tab"]:hover {

    border:
        1px solid rgba(0,255,255,0.5);

    box-shadow:
        0 0 15px rgba(0,255,255,0.25);

    transform:
        translateY(-2px);
}

/* ===== ACTIVE TAB ===== */

.stTabs [aria-selected="true"] {

    background:
        linear-gradient(
            135deg,
            rgba(0,80,120,0.95),
            rgba(0,140,180,0.95)
        ) !important;

    color:
        white !important;

    border:
        1px solid rgba(0,255,255,0.8);

    box-shadow:
        0 0 20px rgba(0,255,255,0.35);
}

/* ===== MOBILE ===== */

@media (max-width: 768px) {

    .stTabs [data-baseweb="tab"] {

        min-width: 170px;

        font-size: 12px;

        padding: 10px 16px;
    }

}

</style>
""", unsafe_allow_html=True)
initialize_layout()

# =====================================================
# CSS — MILITARY TERMINAL AESTHETIC
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;500;600;700&family=Orbitron:wght@400;700;900&display=swap');

/* ── ROOT ── */
:root {
    --bg:        #020609;
    --bg2:       #040d14;
    --bg3:       #071420;
    --panel:     #080f1a;
    --border:    #0a2a40;
    --border2:   #0d3a55;
    --cyan:      #00e5ff;
    --cyan2:     #00b8d4;
    --cyan-dim:  rgba(0,229,255,0.08);
    --cyan-glow: rgba(0,229,255,0.25);
    --red:       #ff3b5c;
    --red-dim:   rgba(255,59,92,0.12);
    --orange:    #ff9500;
    --orange-dim:rgba(255,149,0,0.12);
    --green:     #00ff88;
    --green-dim: rgba(0,255,136,0.10);
    --yellow:    #ffe600;
    --muted:     #3a6070;
    --text:      #c8dde8;
    --text2:     #7a9db0;
    --text3:     #3a6070;
    --mono:      'Share Tech Mono', monospace;
    --head:      'Orbitron', monospace;
    --body:      'Rajdhani', sans-serif;
}

html, body, .stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--body) !important;
}
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 100% !important; }

/* scanline */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,229,255,0.012) 2px, rgba(0,229,255,0.012) 4px);
    pointer-events: none;
    z-index: 9999;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] { background: var(--bg2) !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] * { font-family: var(--body) !important; color: var(--text) !important; }

/* ── HEADER ── */
.geo-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 1.5rem; margin: -1.5rem -2rem 2rem -2rem;
    background: linear-gradient(90deg, var(--bg2) 0%, var(--bg3) 50%, var(--bg2) 100%);
    border-bottom: 1px solid var(--border); position: relative; overflow: hidden;
}
.geo-header::before {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent 0%, var(--cyan) 30%, var(--cyan) 70%, transparent 100%);
    animation: scanH 4s ease-in-out infinite;
}
@keyframes scanH { 0%,100% { opacity:0.3; } 50% { opacity:1; } }
.geo-logo {
    font-family: var(--head) !important; font-size: 1.6rem; font-weight: 900;
    letter-spacing: 0.15em; color: var(--cyan) !important;
    text-shadow: 0 0 20px var(--cyan-glow), 0 0 40px rgba(0,229,255,0.1);
}
.geo-logo span { color: var(--text2); font-weight: 400; font-size: 0.65em; letter-spacing: 0.3em; display: block; margin-top: -4px; }
.geo-status { display: flex; gap: 1.5rem; align-items: center; }
.status-pill { font-family: var(--mono); font-size: 0.65rem; letter-spacing: 0.1em; padding: 3px 10px; border-radius: 2px; border: 1px solid; text-transform: uppercase; }
.status-live { color: var(--green); border-color: var(--green); background: var(--green-dim); animation: pulse-green 2s ease-in-out infinite; }
@keyframes pulse-green { 0%,100% { box-shadow: 0 0 4px rgba(0,255,136,0.2); } 50% { box-shadow: 0 0 12px rgba(0,255,136,0.5); } }
.status-classified { color: var(--red); border-color: var(--red); background: var(--red-dim); }

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: var(--panel) !important; border: 1px solid var(--border) !important;
    border-top: 2px solid var(--cyan) !important; border-radius: 0 !important;
    padding: 1.2rem 1.4rem !important; position: relative;
    clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 0 100%);
}
[data-testid="metric-container"] label { font-family: var(--mono) !important; font-size: 0.62rem !important; letter-spacing: 0.15em !important; color: var(--muted) !important; text-transform: uppercase !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { font-family: var(--head) !important; font-size: 2rem !important; font-weight: 700 !important; color: var(--cyan) !important; text-shadow: 0 0 15px var(--cyan-glow) !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid var(--border) !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; border: none !important; border-bottom: 2px solid transparent !important; border-radius: 0 !important; padding: 0.6rem 1.4rem !important; font-family: var(--mono) !important; font-size: 0.72rem !important; letter-spacing: 0.12em !important; text-transform: uppercase !important; color: var(--text3) !important; transition: all 0.2s !important; }
.stTabs [data-baseweb="tab"]:hover { color: var(--text) !important; background: var(--cyan-dim) !important; }
.stTabs [aria-selected="true"] { color: var(--cyan) !important; border-bottom-color: var(--cyan) !important; background: var(--cyan-dim) !important; text-shadow: 0 0 8px var(--cyan-glow) !important; }

/* ── SECTION HEADERS ── */
.section-label { font-family: var(--mono); font-size: 0.65rem; letter-spacing: 0.25em; color: var(--muted); text-transform: uppercase; margin-bottom: 0.4rem; }
.section-title { font-family: var(--head); font-size: 1.1rem; font-weight: 700; color: var(--text); letter-spacing: 0.08em; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.6rem; }
.section-title::before { content: ''; width: 3px; height: 1.1em; background: var(--cyan); box-shadow: 0 0 8px var(--cyan-glow); display: inline-block; border-radius: 1px; }

/* ── ALERT CARDS ── */
.alert-card { background: var(--panel); border: 1px solid var(--border); border-left: 3px solid var(--red); padding: 1rem 1.2rem; margin-bottom: 0.6rem; clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 0 100%); }
.alert-card.critical { border-left-color: var(--red); }
.alert-card.high     { border-left-color: var(--orange); }
.alert-card.medium   { border-left-color: var(--yellow); }
.alert-card.low      { border-left-color: var(--green); }
.alert-country { font-family: var(--head); font-size: 0.9rem; font-weight: 700; letter-spacing: 0.1em; color: var(--text); }
.alert-score { font-family: var(--mono); font-size: 1.4rem; font-weight: 400; color: var(--cyan); }
.alert-level { font-family: var(--mono); font-size: 0.6rem; letter-spacing: 0.2em; text-transform: uppercase; padding: 2px 8px; border-radius: 2px; }
.badge-critical { color: var(--red);    background: var(--red-dim);    border: 1px solid var(--red); }
.badge-high     { color: var(--orange); background: var(--orange-dim); border: 1px solid var(--orange); }
.badge-medium   { color: var(--yellow); background: rgba(255,230,0,.1); border: 1px solid var(--yellow); }
.badge-low      { color: var(--green);  background: var(--green-dim);  border: 1px solid var(--green); }

/* ── TICKER ── */
.ticker-wrap { background: var(--bg2); border: 1px solid var(--border); padding: 6px 16px; font-family: var(--mono); font-size: 0.68rem; letter-spacing: 0.08em; color: var(--text2); margin-bottom: 1.5rem; overflow: hidden; white-space: nowrap; }
.ticker-inner { display: inline-block; animation: ticker 30s linear infinite; }
@keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
.ticker-item { margin-right: 3rem; }
.ticker-hi { color: var(--red); }
.ticker-ok { color: var(--green); }

/* ── SIDEBAR ── */
.sidebar-logo { font-family: var(--head); font-size: 1.1rem; font-weight: 900; color: var(--cyan); letter-spacing: 0.2em; text-align: center; padding: 1rem 0 0.5rem; text-shadow: 0 0 12px var(--cyan-glow); }
.sidebar-sub { font-family: var(--mono); font-size: 0.55rem; letter-spacing: 0.3em; color: var(--muted); text-align: center; text-transform: uppercase; margin-bottom: 1.5rem; }
.sidebar-divider { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }

/* ── WARNING BOX ── */
.geo-warning { background: var(--red-dim); border: 1px solid var(--red); border-left: 4px solid var(--red); padding: 1rem 1.4rem; font-family: var(--mono); font-size: 0.75rem; color: var(--red); letter-spacing: 0.05em; margin: 1rem 0; }

/* ── INTEL TABLE ── */
.intel-table { width: 100%; border-collapse: collapse; font-family: var(--mono); font-size: 0.75rem; }
.intel-table thead tr { background: #040d14; border-bottom: 2px solid var(--cyan); }
.intel-table thead th { padding: 0.7rem 1rem; text-align: left; letter-spacing: 0.15em; color: var(--muted); font-size: 0.6rem; text-transform: uppercase; white-space: nowrap; }
.intel-table tbody tr { border-bottom: 1px solid var(--border); transition: background 0.15s; }
.intel-table tbody tr:hover { background: var(--cyan-dim); }
.intel-table tbody td { padding: 0.65rem 1rem; color: var(--text); vertical-align: middle; }
.intel-table .country-cell { font-family: var(--head); font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; color: var(--text); }
.intel-table .rank-cell { font-family: var(--mono); font-size: 0.6rem; color: var(--muted); }
.score-bar-wrap { display: flex; align-items: center; gap: 8px; }
.score-bar-bg { flex: 1; height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; min-width: 60px; }
.score-bar-fill { height: 100%; border-radius: 2px; transition: width 0.5s; }
.score-val { font-family: var(--mono); font-size: 0.75rem; min-width: 40px; text-align: right; }

/* ── SIGNAL CARDS ── */
.signal-card {
    background: var(--panel); border: 1px solid var(--border);
    padding: 1.1rem 1.3rem; margin-bottom: 0.7rem;
    clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 0 100%);
    position: relative;
}
.signal-card::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; }
.signal-card.crit::before { background: var(--red); box-shadow: 0 0 8px rgba(255,59,92,0.5); }
.signal-card.high::before { background: var(--orange); box-shadow: 0 0 8px rgba(255,149,0,0.5); }
.signal-card.med::before  { background: var(--yellow); }
.signal-card.low-s::before { background: var(--green); }
.sig-country { font-family: var(--head); font-size: 0.82rem; font-weight: 700; letter-spacing: 0.1em; color: var(--text); }
.sig-score-big { font-family: var(--mono); font-size: 1.6rem; color: var(--cyan); text-shadow: 0 0 10px var(--cyan-glow); }
.sig-label { font-family: var(--mono); font-size: 0.58rem; letter-spacing: 0.18em; color: var(--muted); text-transform: uppercase; margin-bottom: 2px; }
.news-pill { display: inline-block; font-family: var(--mono); font-size: 0.6rem; letter-spacing: 0.1em; padding: 2px 7px; border-radius: 2px; margin-right: 4px; border: 1px solid; }
.sig-bar-row { display: flex; align-items: center; gap: 8px; margin-top: 6px; }
.sig-bar-label { font-family: var(--mono); font-size: 0.58rem; color: var(--muted); min-width: 100px; letter-spacing: 0.08em; }
.sig-bar-bg { flex: 1; height: 3px; background: var(--border); border-radius: 2px; }
.sig-bar-fill { height: 100%; border-radius: 2px; }
.sig-bar-val { font-family: var(--mono); font-size: 0.62rem; color: var(--text2); min-width: 38px; text-align: right; }

/* ── AI BRIEFING CARDS ── */
.ai-card {
    background: #050d18;
    border: 1px solid #0d3050;
    border-top: 2px solid var(--cyan);
    padding: 1.4rem;
    margin-bottom: 1rem;
    position: relative;
    clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
}
.ai-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; }
.ai-card-country { font-family: var(--head); font-size: 0.95rem; font-weight: 700; letter-spacing: 0.12em; color: var(--text); }
.ai-card-risk { font-family: var(--mono); font-size: 0.62rem; letter-spacing: 0.15em; padding: 3px 10px; border-radius: 2px; text-transform: uppercase; }
.ai-confidence { font-family: var(--mono); font-size: 0.65rem; color: var(--cyan); letter-spacing: 0.1em; margin-bottom: 0.8rem; }
.ai-confidence-bar { height: 2px; background: var(--border); border-radius: 1px; margin-bottom: 1rem; overflow: hidden; }
.ai-confidence-fill { height: 100%; background: linear-gradient(90deg, var(--cyan2), var(--cyan)); border-radius: 1px; }
.ai-analysis { font-family: var(--body); font-size: 0.9rem; color: var(--text2); line-height: 1.7; margin-bottom: 1rem; }
.ai-factors-label { font-family: var(--mono); font-size: 0.58rem; letter-spacing: 0.2em; color: var(--muted); text-transform: uppercase; margin-bottom: 0.5rem; }
.ai-factor { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; font-family: var(--body); font-size: 0.82rem; color: var(--text2); }
.ai-factor::before { content: '▸'; color: var(--cyan); font-size: 0.7rem; }
.ai-sources { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 0.8rem; }
.source-tag { font-family: var(--mono); font-size: 0.58rem; letter-spacing: 0.1em; padding: 2px 8px; background: var(--cyan-dim); border: 1px solid var(--border2); color: var(--cyan2); border-radius: 2px; text-transform: uppercase; }
.ai-divider { border: none; border-top: 1px solid var(--border); margin: 0.8rem 0; }

/* ── CHAT ── */
.user-msg { background: var(--cyan-dim); border: 1px solid var(--border2); border-right: 3px solid var(--cyan); padding: .8rem 1rem; font-family: var(--body); font-size: 0.9rem; color: var(--text); margin: .5rem 0; border-radius: 2px; }
.ai-msg { background: var(--panel); border: 1px solid var(--border); border-left: 3px solid var(--green); padding: .8rem 1rem; font-family: var(--body); font-size: 0.9rem; color: var(--text); margin: .5rem 0; border-radius: 2px; }
.ai-tag { font-family: var(--mono); font-size: 0.6rem; letter-spacing: 0.15em; color: var(--green); text-transform: uppercase; margin-bottom: 4px; }

/* ── FOOTER ── */
.geo-footer { font-family: var(--mono); font-size: 0.6rem; letter-spacing: 0.15em; color: var(--text3); text-align: center; padding: 2rem 0 1rem; text-transform: uppercase; border-top: 1px solid var(--border); margin-top: 3rem; }

[data-baseweb="select"] > div { background: var(--panel) !important; border-color: var(--border2) !important; font-family: var(--mono) !important; font-size: 0.8rem !important; }
/* ── RESPONSIVE BREAKPOINTS ── */

/* Tablet — 768px to 1024px */
@media (max-width: 1024px) {
    .block-container {
        padding: 1rem 1rem 2rem !important;
    }
    .geo-header {
        padding: 0.8rem 1rem;
        margin: -1rem -1rem 1.5rem -1rem;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .geo-logo {
        font-size: 1.2rem !important;
    }
    .geo-status {
        gap: 0.8rem;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    .ticker-wrap {
        font-size: 0.6rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 0.8rem !important;
        font-size: 0.65rem !important;
    }
    .signal-card {
        padding: 0.8rem 1rem;
    }
    .sig-score-big {
        font-size: 1.2rem;
    }
    .ai-card {
        padding: 1rem;
    }
}

/* Mobile — below 768px */
@media (max-width: 768px) {
    .block-container {
        padding: 0.5rem 0.5rem 2rem !important;
    }
    .geo-header {
        padding: 0.6rem 0.8rem;
        margin: -0.5rem -0.5rem 1rem -0.5rem;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.6rem;
    }
    .geo-logo {
        font-size: 1rem !important;
        letter-spacing: 0.08em !important;
    }
    .geo-logo span {
        font-size: 0.55em !important;
    }
    .geo-status {
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .status-pill {
        font-size: 0.55rem;
        padding: 2px 7px;
    }
    [data-testid="metric-container"] {
        padding: 0.8rem !important;
        clip-path: none !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 1.2rem !important;
    }
    [data-testid="metric-container"] label {
        font-size: 0.55rem !important;
    }
    .ticker-wrap {
        font-size: 0.55rem;
        padding: 4px 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.4rem 0.6rem !important;
        font-size: 0.58rem !important;
        letter-spacing: 0.06em !important;
    }
    .section-title {
        font-size: 0.9rem;
    }
    .section-label {
        font-size: 0.58rem;
    }
    .signal-card {
        padding: 0.7rem 0.8rem;
        clip-path: none !important;
    }
    .sig-country {
        font-size: 0.72rem;
    }
    .sig-score-big {
        font-size: 1rem;
    }
    .sig-bar-label {
        font-size: 0.52rem;
        min-width: 80px;
    }
    .alert-card {
        clip-path: none !important;
        padding: 0.7rem 0.9rem;
    }
    .alert-score {
        font-size: 1.1rem;
    }
    .ai-card {
        padding: 0.8rem;
        clip-path: none !important;
    }
    .ai-card-country {
        font-size: 0.8rem;
    }
    .intel-table {
        font-size: 0.65rem;
    }
    .intel-table thead th {
        padding: 0.5rem 0.6rem;
        font-size: 0.52rem;
    }
    .intel-table tbody td {
        padding: 0.5rem 0.6rem;
    }
    .geo-footer {
        font-size: 0.52rem;
        margin-top: 2rem;
        padding: 1rem 0;
    }
    .sidebar-logo {
        font-size: 0.9rem;
    }
    .user-msg, .ai-msg {
        font-size: 0.82rem;
        padding: 0.6rem 0.8rem;
    }
}

/* Small mobile — below 480px */
@media (max-width: 480px) {
    .geo-logo {
        font-size: 0.85rem !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 1rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.3rem 0.4rem !important;
        font-size: 0.52rem !important;
        letter-spacing: 0.04em !important;
    }
    .sig-bar-label {
        display: none;
    }
    .signal-card {
        padding: 0.6rem 0.7rem;
    }
}
            /* ── MOBILE TAB SCROLL FIX ── */
.stTabs [data-baseweb="tab-list"] {
    overflow-x: auto !important;
    overflow-y: hidden !important;
    flex-wrap: nowrap !important;
    -webkit-overflow-scrolling: touch !important;
    scrollbar-width: none !important;
    padding-bottom: 2px !important;
}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
    display: none !important;
}
.stTabs [data-baseweb="tab"] {
    white-space: nowrap !important;
    flex-shrink: 0 !important;
}

@media (max-width: 768px) {
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 0.7rem !important;
        font-size: 0.6rem !important;
        letter-spacing: 0.05em !important;
    }
}
 </style>
""", unsafe_allow_html=True)

# =====================================================
# PLOTLY THEME
# =====================================================

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="#020609",
    plot_bgcolor="#040d14",
    font=dict(family="Share Tech Mono, monospace", color="#c8dde8", size=11),
    margin=dict(l=40, r=20, t=40, b=40),
    colorway=["#00e5ff","#ff3b5c","#ff9500","#00ff88","#ffe600","#7b61ff"],
    xaxis=dict(gridcolor="#0a2a40", linecolor="#0a2a40", zerolinecolor="#0a2a40"),
    yaxis=dict(gridcolor="#0a2a40", linecolor="#0a2a40", zerolinecolor="#0a2a40"),
)

def apply_theme(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig

def safe_load(path):
    try:
        if os.path.exists(path):
            return pd.read_csv(path)
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# =====================================================
# LOAD DATA
# =====================================================

df           = safe_load("data/processed/final_georisk.csv")
history_df   = safe_load("data/processed/predictions.csv")
ai_df        = safe_load("data/processed/ai_briefings.csv")
investor_df  = safe_load("data/processed/investor_intelligence.csv")

required_cols = {
    "Country":             "Unknown",
    "GeoRisk_Live_Score":  0.0,
    "Dynamic_Risk_Level":  "Low",
    "Conflict_Probability":0.0,
    "News_Risk_Score":     0.0,
}
if not df.empty:
    for col, default in required_cols.items():
        if col not in df.columns:
            df[col] = default

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="geo-header">
  <div>
    <div class="geo-logo">GEORISK<span style="color:#00e5ff">AI</span><span>GEOPOLITICAL INTELLIGENCE PLATFORM</span></div>
  </div>
  <div class="geo-status">
    <span class="status-pill status-live">● LIVE FEED</span>
    <span class="status-pill status-classified">⬡ INTELLIGENCE ACTIVE</span>
    <span style="font-family:'Share Tech Mono',monospace;font-size:.65rem;color:#3a6070;letter-spacing:.1em">SYS:ONLINE</span>
  </div>
</div>
""", unsafe_allow_html=True)
render_panel_toggle()
if st.session_state.get("intel_panel_open", False):
    render_intelligence_core(df)
    st.stop()
st.markdown("""
<script>
function updateScreenWidth() {
    var width = window.innerWidth;
    sessionStorage.setItem('screen_width', width);
}
updateScreenWidth();
window.addEventListener('resize', updateScreenWidth);
</script>
""", unsafe_allow_html=True)

if df.empty:
    st.markdown('<div class="geo-warning">⚠ SYSTEM WARNING — No intelligence data loaded.<br>Run the pipeline first: <code>python src/pipeline.py</code></div>', unsafe_allow_html=True)
    st.stop()

# =====================================================
# TICKER
# =====================================================

top5 = df.nlargest(5, "GeoRisk_Live_Score")[["Country","GeoRisk_Live_Score","Dynamic_Risk_Level"]]
ticker_items = ""
for _, r in top5.iterrows():
    cls = "ticker-hi" if r["Dynamic_Risk_Level"] in ["Critical","High"] else "ticker-ok"
    ticker_items += f'<span class="ticker-item"><span class="{cls}">▲ {r["Country"].upper()}</span> — GEORISK {r["GeoRisk_Live_Score"]:.3f} [{r["Dynamic_Risk_Level"].upper()}]</span>'
ticker_double = ticker_items * 2
st.markdown(f'<div class="ticker-wrap"><div class="ticker-inner">{ticker_double}</div></div>', unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown('<div class="sidebar-logo">GEORISK<span style="color:#3a6070">AI</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Intelligence Console v2.1</div>', unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:.65rem;letter-spacing:.15em;color:#3a6070;text-transform:uppercase;margin-bottom:.4rem">Filter by risk level</div>', unsafe_allow_html=True)
    levels = sorted(df["Dynamic_Risk_Level"].unique())
    selected = st.multiselect("", levels, default=levels, label_visibility="collapsed")
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    total      = len(df)
    critical_n = (df["Dynamic_Risk_Level"] == "Critical").sum()
    avg_risk   = df["GeoRisk_Live_Score"].mean()
    st.markdown(f"""
    <div style="font-family:'Share Tech Mono',monospace;font-size:.7rem;line-height:2;color:#7a9db0">
    COUNTRIES MONITORED <span style="color:#00e5ff;float:right">{total}</span><br>
    CRITICAL ALERTS     <span style="color:#ff3b5c;float:right">{critical_n}</span><br>
    AVG GEORISK SCORE   <span style="color:#00e5ff;float:right">{avg_risk:.3f}</span><br>
    DATA INTEGRITY      <span style="color:#00ff88;float:right">100%</span><br>
    PIPELINE STATUS     <span style="color:#00ff88;float:right">ONLINE</span>
    </div>""", unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:.55rem;color:#1a3a50;text-align:center;letter-spacing:.1em">GEORISKAI © 2026 — UNCLASSIFIED</div>', unsafe_allow_html=True)

filtered_df = df[df["Dynamic_Risk_Level"].isin(selected)] if selected else df

# =====================================================
# METRICS ROW
# =====================================================

screen = st.session_state.get("screen_width", 1200)
is_mobile = screen < 768
if screen < 768:
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)
else:
    c1, c2, c3, c4 = st.columns(4)
c1.metric("Countries Monitored", f"{len(filtered_df):,}")
c2.metric("Critical Alerts",     int((filtered_df["Dynamic_Risk_Level"] == "Critical").sum()))
c3.metric("Avg GeoRisk Score",   f"{filtered_df['GeoRisk_Live_Score'].mean():.3f}")
c4.metric("Live Signals",        f"{len(filtered_df):,}")
st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

# =====================================================
# TABS
# =====================================================

# =====================================================
# COMMAND CENTER NAVIGATION
# =====================================================

st.markdown("""
<style>

/* ── NAV CONTAINER ── */
.nav-container {
    background: linear-gradient(180deg, #040d14 0%, #020609 100%);
    border: 1px solid #0a2a40;
    border-radius: 12px;
    padding: 6px 8px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.nav-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        #00e5ff 30%,
        #00e5ff 70%,
        transparent 100%
    );
    animation: scanH 4s ease-in-out infinite;
}

/* ── NAV ITEMS ── */
.nav-link {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #3a6070 !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 10px 16px !important;
    transition: all 0.25s ease !important;
    white-space: nowrap !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

.nav-link:hover {
    color: #00e5ff !important;
    border-color: rgba(0,229,255,0.2) !important;
    background: rgba(0,229,255,0.05) !important;
    text-shadow: 0 0 8px rgba(0,229,255,0.4) !important;
}

.nav-link-selected {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #00e5ff !important;
    background: linear-gradient(135deg,
        rgba(0,80,120,0.9),
        rgba(0,40,70,0.9)
    ) !important;
    border: 1px solid rgba(0,229,255,0.4) !important;
    border-radius: 8px !important;
    padding: 10px 16px !important;
    box-shadow:
        0 0 15px rgba(0,229,255,0.15),
        inset 0 1px 0 rgba(0,229,255,0.1) !important;
    text-shadow: 0 0 10px rgba(0,229,255,0.6) !important;
    white-space: nowrap !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

/* ── ICON ── */
.nav-link i, .nav-link-selected i {
    font-size: 1rem !important;
}

/* ── MENU CONTAINER ── */
#MainMenu { visibility: hidden; }
.css-1rs6os { overflow-x: auto; }

/* ── MOBILE NAV ── */
@media (max-width: 768px) {
    .nav-container {
        padding: 4px 4px;
        border-radius: 8px;
    }
    .nav-link, .nav-link-selected {
        font-size: 0.58rem !important;
        padding: 8px 10px !important;
        letter-spacing: 0.06em !important;
    }
    /* Hide text on very small screens, show only icons */
    @media (max-width: 420px) {
        .nav-link span:last-child,
        .nav-link-selected span:last-child {
            display: none !important;
        }
        .nav-link, .nav-link-selected {
            padding: 10px 12px !important;
            justify-content: center !important;
        }
    }
}

/* ── STATUS BAR ABOVE NAV ── */
.nav-status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 8px;
    margin-bottom: 6px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.12em;
    color: #1a3a50;
    text-transform: uppercase;
}

.nav-status-dot {
    display: inline-block;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #00ff88;
    box-shadow: 0 0 6px rgba(0,255,136,0.6);
    animation: pulse-dot 2s ease-in-out infinite;
    margin-right: 5px;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ── CORNER DECORATION ── */
.nav-corner {
    position: absolute;
    width: 8px;
    height: 8px;
    border-color: #00e5ff;
    border-style: solid;
    opacity: 0.4;
}
.nav-corner-tl { top: 4px; left: 4px; border-width: 1px 0 0 1px; }
.nav-corner-tr { top: 4px; right: 4px; border-width: 1px 1px 0 0; }
.nav-corner-bl { bottom: 4px; left: 4px; border-width: 0 0 1px 1px; }
.nav-corner-br { bottom: 4px; right: 4px; border-width: 0 1px 1px 0; }
</style>
""", unsafe_allow_html=True)

# Status bar above nav
st.markdown(f"""
<div class="nav-status-bar">
    <span><span class="nav-status-dot"></span>GEORISKAI COMMAND CENTER — INTELLIGENCE ACTIVE</span>
    <span>NODES: {len(filtered_df)} MONITORED</span>
</div>
""", unsafe_allow_html=True)

# Navigation
with st.container():
    selected_tab = option_menu(
        menu_title=None,
        options=[
            "Global Overview",
            "Country Intel",
            "Live Signals",
            "Investor Brief",
            "AI Analyst",
        ],
        icons=[
            "globe",
            "broadcast",
            "lightning-charge",
            "graph-up-arrow",
            "robot",
        ],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding":          "0",
                "background-color": "transparent",
                "border":           "none",
                "gap":              "4px",
            },
            "icon": {
                "color":     "#3a6070",
                "font-size": "14px",
            },
            "nav-link": {
                "font-family":    "'Share Tech Mono', monospace",
                "font-size":      "0.68rem",
                "letter-spacing": "0.1em",
                "text-transform": "uppercase",
                "color":          "#3a6070",
                "background":     "transparent",
                "border":         "1px solid transparent",
                "border-radius":  "8px",
                "padding":        "10px 14px",
                "transition":     "all 0.2s",
                "white-space":    "nowrap",
            },
            "nav-link-selected": {
                "font-family":    "'Share Tech Mono', monospace",
                "font-size":      "0.68rem",
                "letter-spacing": "0.1em",
                "text-transform": "uppercase",
                "color":          "#00e5ff",
                "background":     "linear-gradient(135deg, rgba(0,80,120,0.9), rgba(0,40,70,0.9))",
                "border":         "1px solid rgba(0,229,255,0.4)",
                "border-radius":  "8px",
                "box-shadow":     "0 0 15px rgba(0,229,255,0.15)",
                "text-shadow":    "0 0 8px rgba(0,229,255,0.5)",
            },
        },
        key="main_nav",
    )

# =====================================================
# RENDER SELECTED TAB
# =====================================================

if selected_tab == "Global Overview":
    render_global_tab(filtered_df, PLOTLY_LAYOUT)

elif selected_tab == "Country Intel":
    st.markdown(
        '<div class="section-label">Deep Analysis</div>'
        '<div class="section-title">Country Intelligence Profile</div>',
        unsafe_allow_html=True,
    )
    if not history_df.empty:
        countries  = sorted(history_df["Country"].dropna().unique())
        screen     = st.session_state.get("screen_width", 1200)
        if screen < 768:
            country = st.selectbox("SELECT COUNTRY", countries)
            col_info  = st.container()
            col_spark = st.container()
        else:
            col_sel, col_info_outer = st.columns([1, 3])
            with col_sel:
                country = st.selectbox("SELECT COUNTRY", countries)
            col_info  = col_info_outer
            col_spark = None

        country_df = history_df[history_df["Country"] == country]

        if "Year" in country_df.columns and "Conflict_Probability" in country_df.columns:
            trend_fig = px.area(
                country_df, x="Year", y="Conflict_Probability",
                title=f"CONFLICT PROBABILITY TREND — {country.upper()}",
                markers=True,
            )
            trend_fig.update_traces(
                line_color="#00e5ff",
                fillcolor="rgba(0,229,255,0.08)",
                marker=dict(size=5, color="#00e5ff"),
            )
            trend_fig.update_layout(
                **PLOTLY_LAYOUT,
                height=320,
                title_font=dict(family="Share Tech Mono", size=11, color="#3a6070"),
            )
            st.plotly_chart(trend_fig, use_container_width=True)

            latest = country_df.sort_values("Year").iloc[-1] if not country_df.empty else None
            if latest is not None:
                prob = latest.get("Conflict_Probability", 0)
                st.markdown(f"""
<div style="background:#040d14;border:1px solid #0a2a40;
            padding:1.2rem;margin-top:.5rem;border-radius:8px;
            display:inline-block;min-width:160px;">
  <div style="font-family:'Share Tech Mono',monospace;font-size:.6rem;
              letter-spacing:.2em;color:#3a6070;text-transform:uppercase;
              margin-bottom:.5rem">LATEST READING</div>
  <div style="font-family:'Orbitron',monospace;font-size:2rem;
              font-weight:700;color:#00e5ff;
              text-shadow:0 0 15px rgba(0,229,255,.4)">{prob:.3f}</div>
  <div style="font-family:'Share Tech Mono',monospace;font-size:.65rem;
              color:#7a9db0;margin-top:.3rem">CONFLICT PROBABILITY</div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="geo-warning">⚠ No historical data. Run pipeline.py first.</div>',
            unsafe_allow_html=True,
        )

elif selected_tab == "Live Signals":
    st.markdown(
        '<div class="section-label">Real-Time Intelligence</div>'
        '<div class="section-title">Signal Analysis Matrix</div>',
        unsafe_allow_html=True,
    )
    screen    = st.session_state.get("screen_width", 1200)
    is_mobile = screen < 768

    if is_mobile:
        col_scatter = st.container()
        col_dist    = st.container()
    else:
        col_scatter, col_dist = st.columns([3, 2])

    with col_scatter:
        live_fig = px.scatter(
            filtered_df,
            x="Conflict_Probability",
            y="News_Risk_Score",
            size="GeoRisk_Live_Score",
            color="Dynamic_Risk_Level",
            hover_name="Country",
            color_discrete_map={
                "Critical": "#ff3b5c",
                "High":     "#ff9500",
                "Medium":   "#ffe600",
                "Low":      "#00ff88",
            },
            title="ML PROBABILITY vs NEWS RISK SIGNAL",
            size_max=28,
            custom_data=["GeoRisk_Live_Score", "Dynamic_Risk_Level"],
        )
        live_fig.update_traces(
            marker=dict(line=dict(width=0.5, color="#0a2a40")),
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Conflict Prob: <b>%{x:.4f}</b><br>"
                "News Risk: <b>%{y:.4f}</b><br>"
                "GeoRisk: <b>%{customdata[0]:.4f}</b><br>"
                "Level: <b>%{customdata[1]}</b><extra></extra>"
            ),
        )
        live_fig.update_layout(
            **PLOTLY_LAYOUT,
            height=300 if is_mobile else 380,
            legend=dict(
                orientation="h" if is_mobile else "v",
                yanchor="bottom",
                y=1.02 if is_mobile else 0,
                xanchor="right",
                x=1,
                font=dict(size=9),
            ),
            title_font=dict(family="Share Tech Mono", size=11, color="#3a6070"),
        )
        st.plotly_chart(live_fig, use_container_width=True)

    with col_dist:
        dist_fig = px.histogram(
            filtered_df, x="GeoRisk_Live_Score",
            nbins=20,
            title="GEORISK SCORE DISTRIBUTION",
            color_discrete_sequence=["#00e5ff"],
        )
        dist_fig.update_traces(marker_line_width=0, opacity=0.8)
        dist_fig.update_layout(
            **PLOTLY_LAYOUT,
            height=250 if is_mobile else 380,
            title_font=dict(family="Share Tech Mono", size=11, color="#3a6070"),
        )
        st.plotly_chart(dist_fig, use_container_width=True)

    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-label">News Signal Breakdown</div>'
        '<div class="section-title">Live Signal Cards — Top Threat Countries</div>',
        unsafe_allow_html=True,
    )

    if is_mobile:
        sig_cols = st.columns(1)
    elif screen < 1024:
        sig_cols = st.columns(2)
    else:
        sig_cols = st.columns(3)

    top_signals    = filtered_df.nlargest(9, "GeoRisk_Live_Score")
    sig_level_css  = {"Critical":"crit","High":"high","Medium":"med","Low":"low-s"}
    sig_news_color = {"Critical":"#ff3b5c","High":"#ff9500","Medium":"#ffe600","Low":"#00ff88"}

    for i, (_, row) in enumerate(top_signals.iterrows()):
        lvl    = row.get("Dynamic_Risk_Level", "Low")
        score  = row.get("GeoRisk_Live_Score", 0)
        cprob  = row.get("Conflict_Probability", 0)
        news   = row.get("News_Risk_Score", 0)
        cntry  = row.get("Country", "Unknown")
        sc_css = sig_level_css.get(lvl, "low-s")
        nc     = sig_news_color.get(lvl, "#00ff88")
        ml_pct   = int(cprob * 100)
        news_pct = int(news * 100)
        geo_pct  = int(score * 100)

        if news >= 0.7:
            news_label = "HIGH INTENSITY"
            news_bc    = f"color:{nc};background:rgba(255,59,92,.12);border:1px solid {nc}"
        elif news >= 0.4:
            news_label = "MODERATE"
            news_bc    = "color:#ff9500;background:rgba(255,149,0,.12);border:1px solid #ff9500"
        else:
            news_label = "LOW"
            news_bc    = "color:#00ff88;background:rgba(0,255,136,.10);border:1px solid #00ff88"

        with sig_cols[i % len(sig_cols)]:
            st.markdown(f"""
<div class="signal-card {sc_css}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.6rem">
    <span class="sig-country">{cntry.upper()}</span>
    <span class="sig-score-big">{score:.3f}</span>
  </div>
  <div style="display:flex;gap:6px;margin-bottom:.8rem;flex-wrap:wrap">
    <span class="news-pill" style="{news_bc}">{news_label}</span>
    <span class="news-pill badge-{lvl.lower()}">{lvl.upper()}</span>
  </div>
  <div class="sig-label">SIGNAL COMPONENTS</div>
  <div class="sig-bar-row">
    <span class="sig-bar-label">▸ ML PROB</span>
    <div class="sig-bar-bg"><div class="sig-bar-fill" style="width:{ml_pct}%;background:#ff9500"></div></div>
    <span class="sig-bar-val">{cprob:.3f}</span>
  </div>
  <div class="sig-bar-row">
    <span class="sig-bar-label">▸ NEWS RISK</span>
    <div class="sig-bar-bg"><div class="sig-bar-fill" style="width:{news_pct}%;background:#ff3b5c"></div></div>
    <span class="sig-bar-val">{news:.3f}</span>
  </div>
  <div class="sig-bar-row">
    <span class="sig-bar-label">▸ COMPOSITE</span>
    <div class="sig-bar-bg"><div class="sig-bar-fill" style="width:{geo_pct}%;background:#00e5ff"></div></div>
    <span class="sig-bar-val">{score:.3f}</span>
  </div>
  <div style="margin-top:.7rem;padding-top:.6rem;border-top:1px solid #0a2a40;
              font-family:'Share Tech Mono',monospace;font-size:.58rem;color:#3a6070;
              display:flex;justify-content:space-between">
    <span>SRC: ML + NEWS FUSION</span>
    <span style="color:#1a3a50">LIVE</span>
  </div>
</div>""", unsafe_allow_html=True)

elif selected_tab == "Investor Brief":
    st.markdown(
        '<div class="section-label">Market Intelligence</div>'
        '<div class="section-title">Investor Intelligence Terminal</div>',
        unsafe_allow_html=True,
    )

    def investor_action(risk):
        return {"Critical":"AVOID","High":"HEDGE","Medium":"MONITOR"}.get(risk,"STABLE")

    sector_map = {
        "Iran":     ("Energy",          "Oil export volatility"),
        "Russia":   ("Energy",          "Global energy disruption"),
        "Ukraine":  ("Agriculture",     "Grain supply instability"),
        "China":    ("Manufacturing",   "Supply chain disruption"),
        "Taiwan":   ("Semiconductors",  "Chip production risk"),
        "Israel":   ("Defense",         "Regional escalation"),
        "Pakistan": ("Infrastructure",  "Political instability"),
        "Syria":    ("Logistics",       "Conflict-driven disruption"),
    }

    screen    = st.session_state.get("screen_width", 1200)
    is_mobile = screen < 768

    if is_mobile:
        m1, m2 = st.columns(2)
        m3, m4 = st.columns(2)
    else:
        m1, m2, m3, m4 = st.columns(4)

    m1.metric("🚨 Critical", int((filtered_df["Dynamic_Risk_Level"]=="Critical").sum()))
    m2.metric("⚠ High",     int((filtered_df["Dynamic_Risk_Level"]=="High").sum()))
    m3.metric("🌍 Avg Risk", round(filtered_df["GeoRisk_Live_Score"].mean(), 3))
    m4.metric("📡 Signals",  len(filtered_df))

    st.markdown("---")

    s1, s2 = st.columns([2, 1])
    with s1:
        search_country = st.text_input("🔍 Search Country")
    with s2:
        sort_option = st.selectbox("Sort By", ["Highest GeoRisk","Highest News Risk","Alphabetical"])

    investor_view = filtered_df.copy()
    if search_country:
        investor_view = investor_view[investor_view["Country"].str.contains(search_country, case=False, na=False)]
    if sort_option == "Highest GeoRisk":
        investor_view = investor_view.sort_values("GeoRisk_Live_Score", ascending=False)
    elif sort_option == "Highest News Risk":
        investor_view = investor_view.sort_values("News_Risk_Score", ascending=False)
    else:
        investor_view = investor_view.sort_values("Country")

    if is_mobile:
        cols = st.columns(1)
    elif screen < 1024:
        cols = st.columns(2)
    else:
        cols = st.columns(3)

    risk_emoji = {"Critical":"🔴","High":"🟠","Medium":"🟡"}

    for i, (_, row) in enumerate(investor_view.iterrows()):
        country = row["Country"]
        risk    = row["Dynamic_Risk_Level"]
        score   = float(row["GeoRisk_Live_Score"])
        news    = float(row["News_Risk_Score"])
        action  = investor_action(risk)
        sector, impact = sector_map.get(country, ("Regional Markets","General geopolitical volatility"))
        emoji   = risk_emoji.get(risk, "🟢")

        with cols[i % len(cols)]:
            with st.container(border=True):
                t1, t2 = st.columns([3, 1])
                with t1:
                    st.markdown(f"### 🌍 {country}")
                with t2:
                    st.markdown(f"## {emoji}")
                c1, c2 = st.columns(2)
                c1.metric("GeoRisk", f"{score:.3f}")
                c2.metric("News",    f"{news:.3f}")
                st.metric("Action",  action)
                st.markdown(f"**🏭 Sector:** {sector}")
                st.markdown(f"**📉 Impact:** {impact}")
                if risk == "Critical":
                    st.error("High geopolitical exposure. Avoid aggressive positioning.")
                elif risk == "High":
                    st.warning("Elevated instability. Hedging advised.")
                elif risk == "Medium":
                    st.info("Moderate volatility. Monitor closely.")
                else:
                    st.success("Stable environment.")

elif selected_tab == "AI Analyst":
    render_ai_tab(ai_df, df)