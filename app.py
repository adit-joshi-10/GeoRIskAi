import streamlit as st
    
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time
import streamlit as st

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

c1, c2, c3, c4 = st.columns(4)
c1.metric("Countries Monitored", f"{len(filtered_df):,}")
c2.metric("Critical Alerts",     int((filtered_df["Dynamic_Risk_Level"] == "Critical").sum()))
c3.metric("Avg GeoRisk Score",   f"{filtered_df['GeoRisk_Live_Score'].mean():.3f}")
c4.metric("Live Signals",        f"{len(filtered_df):,}")
st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

# =====================================================
# TABS
# =====================================================

layout = create_layout()

with layout[0]:

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌍  GLOBAL OVERVIEW",
    "📡  COUNTRY INTEL",
    "⚡  LIVE SIGNALS",
    "💹  INVESTOR BRIEF",
    "🤖  AI ANALYST",
])
# =====================================================
# MAIN LAYOUT
# =====================================================

main_col, side_col = st.columns([4, 1])

# =====================================================
# TAB 1 — GLOBAL OVERVIEW
# =====================================================

with tab1:

    render_global_tab(
        filtered_df,
        PLOTLY_LAYOUT
    )
# =====================================================
# TAB 2 — COUNTRY INTEL
# =====================================================

with tab2:
    st.markdown('<div class="section-label">Deep Analysis</div><div class="section-title">Country Intelligence Profile</div>', unsafe_allow_html=True)

    if not history_df.empty:
        countries = sorted(history_df["Country"].dropna().unique())
        col_sel, col_info = st.columns([1, 3])
        with col_sel:
            country = st.selectbox("SELECT COUNTRY", countries, label_visibility="visible")

        country_df = history_df[history_df["Country"] == country]

        if "Year" in country_df.columns and "Conflict_Probability" in country_df.columns:
            col_info, col_spark = st.columns([3, 1])

            with col_info:
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
                trend_fig.update_layout(**PLOTLY_LAYOUT, height=320,
                                        title_font=dict(family="Share Tech Mono", size=11, color="#3a6070"))
                st.plotly_chart(trend_fig, use_container_width=True)

            with col_spark:
                latest = country_df.sort_values("Year").iloc[-1] if not country_df.empty else None
                if latest is not None:
                    prob = latest.get("Conflict_Probability",0)
                    st.markdown(f"""
                    <div style="background:#040d14;border:1px solid #0a2a40;padding:1.2rem;margin-top:.5rem">
                      <div style="font-family:'Share Tech Mono',monospace;font-size:.6rem;letter-spacing:.2em;color:#3a6070;text-transform:uppercase;margin-bottom:.5rem">LATEST READING</div>
                      <div style="font-family:'Orbitron',monospace;font-size:2rem;font-weight:700;color:#00e5ff;text-shadow:0 0 15px rgba(0,229,255,.4)">{prob:.3f}</div>
                      <div style="font-family:'Share Tech Mono',monospace;font-size:.65rem;color:#7a9db0;margin-top:.3rem">CONFLICT PROBABILITY</div>
                    </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="geo-warning">⚠ No historical prediction data found. Run pipeline.py first.</div>', unsafe_allow_html=True)

# =====================================================
# TAB 3 — LIVE SIGNALS  (UPGRADED)
# =====================================================

with tab3:
    st.markdown('<div class="section-label">Real-Time Intelligence</div><div class="section-title">Signal Analysis Matrix</div>', unsafe_allow_html=True)

    col_scatter, col_dist = st.columns([3, 2])

    with col_scatter:
        live_fig = px.scatter(
            filtered_df,
            x="Conflict_Probability",
            y="News_Risk_Score",
            size="GeoRisk_Live_Score",
            color="Dynamic_Risk_Level",
            hover_name="Country",
            color_discrete_map={"Critical":"#ff3b5c","High":"#ff9500","Medium":"#ffe600","Low":"#00ff88"},
            title="ML PROBABILITY vs NEWS RISK SIGNAL",
            size_max=28,
            custom_data=["GeoRisk_Live_Score","Dynamic_Risk_Level"],
        )
        live_fig.update_traces(
            marker=dict(line=dict(width=0.5, color="#0a2a40")),
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Conflict Prob: <b style='color:#ff9500'>%{x:.4f}</b><br>"
                "News Risk: <b style='color:#ff3b5c'>%{y:.4f}</b><br>"
                "GeoRisk Score: <b style='color:#00e5ff'>%{customdata[0]:.4f}</b><br>"
                "Level: <b>%{customdata[1]}</b><extra></extra>"
            ),
        )
        live_fig.update_layout(**PLOTLY_LAYOUT, height=380,
                               title_font=dict(family="Share Tech Mono", size=11, color="#3a6070"))
        st.plotly_chart(live_fig, use_container_width=True)

    with col_dist:
        dist_fig = px.histogram(
            filtered_df, x="GeoRisk_Live_Score",
            nbins=20,
            title="GEORISK SCORE DISTRIBUTION",
            color_discrete_sequence=["#00e5ff"],
        )
        dist_fig.update_traces(marker_line_width=0, opacity=0.8)
        dist_fig.update_layout(**PLOTLY_LAYOUT, height=380,
                               title_font=dict(family="Share Tech Mono", size=11, color="#3a6070"))
        st.plotly_chart(dist_fig, use_container_width=True)

    # ── NEWS SCORE BREAKDOWN SECTION ─────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">News Signal Breakdown</div><div class="section-title">Live Signal Cards — Top Threat Countries</div>', unsafe_allow_html=True)

    sig_cols = st.columns(3)
    top_signals = filtered_df.nlargest(9, "GeoRisk_Live_Score")

    sig_level_css = {"Critical":"crit","High":"high","Medium":"med","Low":"low-s"}
    sig_news_color = {"Critical":"#ff3b5c","High":"#ff9500","Medium":"#ffe600","Low":"#00ff88"}

    for i, (_, row) in enumerate(top_signals.iterrows()):
        lvl    = row.get("Dynamic_Risk_Level","Low")
        score  = row.get("GeoRisk_Live_Score",0)
        cprob  = row.get("Conflict_Probability",0)
        news   = row.get("News_Risk_Score",0)
        cntry  = row.get("Country","Unknown")
        sc_css = sig_level_css.get(lvl,"low-s")
        nc     = sig_news_color.get(lvl,"#00ff88")

        # Derive signal breakdown heuristics
        ml_pct   = int(cprob * 100)
        news_pct = int(news * 100)
        geo_pct  = int(score * 100)

        # News intensity label
        if news >= 0.7:   news_label, news_bc = "HIGH INTENSITY", f"color:{nc};background:rgba(255,59,92,.12);border:1px solid {nc}"
        elif news >= 0.4: news_label, news_bc = "MODERATE",       f"color:#ff9500;background:rgba(255,149,0,.12);border:1px solid #ff9500"
        else:             news_label, news_bc = "LOW",             "color:#00ff88;background:rgba(0,255,136,.10);border:1px solid #00ff88"

        with sig_cols[i % 3]:
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
                <span class="sig-bar-label">▸ ML CONFLICT PROB</span>
                <div class="sig-bar-bg"><div class="sig-bar-fill" style="width:{ml_pct}%;background:#ff9500"></div></div>
                <span class="sig-bar-val">{cprob:.3f}</span>
              </div>
              <div class="sig-bar-row">
                <span class="sig-bar-label">▸ NEWS RISK SCORE</span>
                <div class="sig-bar-bg"><div class="sig-bar-fill" style="width:{news_pct}%;background:#ff3b5c"></div></div>
                <span class="sig-bar-val">{news:.3f}</span>
              </div>
              <div class="sig-bar-row">
                <span class="sig-bar-label">▸ COMPOSITE INDEX</span>
                <div class="sig-bar-bg"><div class="sig-bar-fill" style="width:{geo_pct}%;background:#00e5ff"></div></div>
                <span class="sig-bar-val">{score:.3f}</span>
              </div>

              <div style="margin-top:.7rem;padding-top:.6rem;border-top:1px solid #0a2a40;
                          font-family:'Share Tech Mono',monospace;font-size:.58rem;color:#3a6070;
                          display:flex;justify-content:space-between">
                <span>SRC: ML + NEWS FUSION</span>
                <span style="color:#1a3a50">LIVE FEED</span>
              </div>
            </div>""", unsafe_allow_html=True)

# =====================================================
# TAB 4 — INVESTOR BRIEF
# =====================================================
with tab4:

    st.subheader("💹 Investor Intelligence Terminal")

    # =================================================
    # ACTION ENGINE
    # =================================================

    def investor_action(risk):

        if risk == "Critical":
            return "AVOID"

        elif risk == "High":
            return "HEDGE"

        elif risk == "Medium":
            return "MONITOR"

        return "STABLE"

    # =================================================
    # SECTOR MAP
    # =================================================

    sector_map = {

        "Iran":
        ("Energy", "Oil export volatility"),

        "Russia":
        ("Energy", "Global energy disruption"),

        "Ukraine":
        ("Agriculture", "Grain supply instability"),

        "China":
        ("Manufacturing", "Supply chain disruption"),

        "Taiwan":
        ("Semiconductors", "Chip production risk"),

        "Israel":
        ("Defense", "Regional escalation"),

        "Pakistan":
        ("Infrastructure", "Political instability"),

        "Syria":
        ("Logistics", "Conflict-driven disruption")
    }

    # =================================================
    # METRICS
    # =================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "🚨 Critical Markets",

        int(
            (
                filtered_df[
                    "Dynamic_Risk_Level"
                ] == "Critical"
            ).sum()
        )
    )

    c2.metric(

        "⚠ High Exposure",

        int(
            (
                filtered_df[
                    "Dynamic_Risk_Level"
                ] == "High"
            ).sum()
        )
    )

    c3.metric(

        "🌍 Avg GeoRisk",

        round(
            filtered_df[
                "GeoRisk_Live_Score"
            ].mean(),
            3
        )
    )

    c4.metric(

        "📡 Market Signals",

        len(filtered_df)
    )

    st.markdown("---")

    # =================================================
    # SEARCH + SORT
    # =================================================

    s1, s2 = st.columns([2,1])

    with s1:

        search_country = st.text_input(
            "🔍 Search Country"
        )

    with s2:

        sort_option = st.selectbox(

            "Sort By",

            [

                "Highest GeoRisk",

                "Highest News Risk",

                "Alphabetical"
            ]
        )

    # =================================================
    # DATA
    # =================================================

    investor_view = filtered_df.copy()

    # =================================================
    # SEARCH FILTER
    # =================================================

    if search_country:

        investor_view = investor_view[

            investor_view["Country"]

            .str.contains(
                search_country,
                case=False,
                na=False
            )
        ]

    # =================================================
    # SORTING
    # =================================================

    if sort_option == "Highest GeoRisk":

        investor_view = investor_view.sort_values(

            "GeoRisk_Live_Score",

            ascending=False
        )

    elif sort_option == "Highest News Risk":

        investor_view = investor_view.sort_values(

            "News_Risk_Score",

            ascending=False
        )

    else:

        investor_view = investor_view.sort_values(
            "Country"
        )

    # =================================================
    # RESPONSIVE GRID
    # =================================================

    cols = st.columns(3)

    # =================================================
    # LOOP
    # =================================================

    for i, (_, row) in enumerate(
        investor_view.iterrows()
    ):

        country = row["Country"]

        risk = row["Dynamic_Risk_Level"]

        score = float(
            row["GeoRisk_Live_Score"]
        )

        news = float(
            row["News_Risk_Score"]
        )

        action = investor_action(risk)

        sector, impact = sector_map.get(

            country,

            (
                "Regional Markets",
                "General geopolitical volatility"
            )
        )

        # =============================================
        # RISK COLORS
        # =============================================

        if risk == "Critical":

            emoji = "🔴"

        elif risk == "High":

            emoji = "🟠"

        elif risk == "Medium":

            emoji = "🟡"

        else:

            emoji = "🟢"

        # =============================================
        # CARD
        # =============================================

        with cols[i % 3]:

            with st.container(border=True):

                top1, top2 = st.columns([3,1])

                with top1:

                    st.markdown(
                        f"### 🌍 {country}"
                    )

                with top2:

                    st.markdown(
                        f"## {emoji}"
                    )

                # =====================================
                # METRICS
                # =====================================

                m1, m2 = st.columns(2)

                m1.metric(
                    "GeoRisk",
                    f"{score:.3f}"
                )

                m2.metric(
                    "News",
                    f"{news:.3f}"
                )

                st.metric(
                    "Investor Action",
                    action
                )

                st.markdown("#### 🏭 Affected Sector")

                st.write(sector)

                st.markdown("#### 📉 Market Impact")

                st.write(impact)

                st.markdown("#### 🧠 Investor Insight")

                if risk == "Critical":

                    st.error(
                        "High geopolitical exposure detected. "
                        "Aggressive positioning not recommended."
                    )

                elif risk == "High":

                    st.warning(
                        "Elevated instability signals detected. "
                        "Hedging strategies advised."
                    )

                elif risk == "Medium":

                    st.info(
                        "Moderate volatility environment. "
                        "Close monitoring recommended."
                    )

                else:

                    st.success(
                        "Stable geopolitical environment."
                    )

                st.markdown("---")



with tab5:

    render_ai_tab(

        ai_df,

        df
    )