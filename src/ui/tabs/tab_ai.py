import streamlit as st
import time

from src.intelligence.market_impact import get_market_impact
from src.intelligence.investor_actions import get_investor_actions
from src.intelligence.trend_forecast import get_trend_forecast
from src.intelligence.portfolio_engine import get_portfolio_signals
from src.intelligence.strategic_alerts import get_strategic_alert
from src.intelligence.macro_themes import get_macro_themes
from src.intelligence.conviction_engine import get_conviction_score
from src.ui.components.intel.market_section import render_market_section
from src.ui.components.intel.macro_section import render_macro_section
from src.ui.components.intel.forecast_section import render_forecast_section
from src.ui.components.intel.positioning_section import render_positioning_section
from src.ui.components.intel.news_section import render_news_section
from src.ui.components.intel.global_signal_bar import (
    render_global_signal_bar
)

CARD_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@400;700;900&display=swap');
:root{--bg:#020609;--bg2:#040d14;--panel:#080f1a;--border:#0a2a40;--border2:#0d3a55;--cyan:#00e5ff;--cyan2:#00b8d4;--cyan-dim:rgba(0,229,255,0.08);--cyan-glow:rgba(0,229,255,0.25);--red:#ff3b5c;--red-dim:rgba(255,59,92,0.14);--orange:#ff9500;--orange-dim:rgba(255,149,0,0.14);--green:#00ff88;--green-dim:rgba(0,255,136,0.12);--yellow:#ffe600;--muted:#3a6070;--text:#e2eef5;--text2:#9bbccc;--text3:#3a6070;--mono:'Share Tech Mono',monospace;--head:'Orbitron',monospace;--body:'Rajdhani',sans-serif;}
div[data-testid="stDialogContainer"]{backdrop-filter:blur(14px) saturate(0.4)!important;-webkit-backdrop-filter:blur(14px) saturate(0.4)!important;background:rgba(2,6,9,0.82)!important;}
div[data-testid="stDialogContent"],div[role="dialog"]{background:#04101e!important;border:1px solid #0d3050!important;border-top:2px solid var(--cyan)!important;border-radius:2px!important;box-shadow:0 0 80px rgba(0,229,255,0.10),0 30px 120px rgba(0,0,0,0.9)!important;max-width:860px!important;}
[data-testid="stDialogContent"] p,[data-testid="stDialogContent"] span,[data-testid="stDialogContent"] div,[data-testid="stDialogContent"] label{color:#c8dde8;}
[data-testid="stDialogContent"] .stMarkdown{color:#c8dde8!important;}
.geo-card{background:#050d18;border:1px solid #0d2a40;padding:0;position:relative;overflow:hidden;margin-bottom:4px;}
.geo-card-top-bar{height:3px;width:100%;}
.geo-card-inner{padding:1rem 1.1rem 0.8rem;}
.geo-card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;}
.geo-card-country{font-family:'Orbitron',monospace;font-size:0.82rem;font-weight:700;letter-spacing:0.12em;color:#e2eef5;}
.risk-badge{font-family:'Share Tech Mono',monospace;font-size:0.58rem;letter-spacing:0.18em;padding:2px 9px;border-radius:2px;text-transform:uppercase;border:1px solid;font-weight:400;}
.rb-critical{color:#ff3b5c;background:rgba(255,59,92,0.14);border-color:#ff3b5c;}
.rb-high{color:#ff9500;background:rgba(255,149,0,0.14);border-color:#ff9500;}
.rb-medium{color:#ffe600;background:rgba(255,230,0,0.10);border-color:#ffe600;}
.rb-low{color:#00ff88;background:rgba(0,255,136,0.12);border-color:#00ff88;}
.geo-card-metrics{display:grid;grid-template-columns:1fr 1fr 1fr;gap:0;margin-bottom:0.75rem;border:1px solid #0a2030;background:#030b14;}
.card-metric{padding:0.5rem 0.6rem;border-right:1px solid #0a2030;}
.card-metric:last-child{border-right:none;}
.card-metric-label{font-family:'Share Tech Mono',monospace;font-size:0.5rem;letter-spacing:0.15em;color:#3a6070;text-transform:uppercase;margin-bottom:3px;}
.card-metric-val{font-family:'Orbitron',monospace;font-size:0.9rem;font-weight:700;line-height:1.1;}
.geo-card-analysis{font-family:'Rajdhani',sans-serif;font-size:0.82rem;color:#7a9db0;line-height:1.5;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:0.75rem;min-height:56px;}
.mbar{display:flex;align-items:center;gap:8px;margin-bottom:5px;}
.mbar-lbl{font-family:'Share Tech Mono',monospace;font-size:0.5rem;color:#3a6070;text-transform:uppercase;letter-spacing:.08em;min-width:82px;}
.mbar-track{flex:1;height:3px;background:#0a2030;border-radius:2px;overflow:hidden;}
.mbar-fill{height:100%;border-radius:2px;}
.mbar-val{font-family:'Share Tech Mono',monospace;font-size:0.58rem;color:#7a9db0;min-width:36px;text-align:right;}
div[data-testid="column"] .stButton>button[kind="secondary"]{width:100%!important;background:transparent!important;border:1px solid #0d3050!important;border-radius:0!important;color:#00e5ff!important;font-family:'Share Tech Mono',monospace!important;font-size:0.6rem!important;letter-spacing:0.22em!important;text-transform:uppercase!important;padding:0.55rem 1rem!important;margin-top:2px;transition:all 0.18s!important;}
div[data-testid="column"] .stButton>button[kind="secondary"]:hover{background:rgba(0,229,255,0.06)!important;border-color:#00e5ff!important;box-shadow:0 0 14px rgba(0,229,255,0.12)!important;}
[data-testid="stDialogContent"] .stTabs [data-baseweb="tab-list"]{background:#030b14!important;border-bottom:1px solid #0a2a40!important;gap:0!important;}
[data-testid="stDialogContent"] .stTabs [data-baseweb="tab"]{font-family:'Share Tech Mono',monospace!important;font-size:0.6rem!important;letter-spacing:0.12em!important;text-transform:uppercase!important;color:#3a6070!important;background:transparent!important;border:none!important;border-bottom:2px solid transparent!important;border-radius:0!important;padding:0.5rem 1.1rem!important;}
[data-testid="stDialogContent"] .stTabs [aria-selected="true"]{color:#00e5ff!important;border-bottom-color:#00e5ff!important;background:rgba(0,229,255,0.06)!important;}
[data-testid="stDialogContent"] [data-testid="metric-container"]{background:#050d18!important;border:1px solid #0a2a40!important;border-top:2px solid #0d3a55!important;border-radius:0!important;padding:0.7rem 0.9rem!important;}
[data-testid="stDialogContent"] [data-testid="metric-container"] label{font-family:'Share Tech Mono',monospace!important;font-size:0.52rem!important;letter-spacing:0.15em!important;color:#3a6070!important;text-transform:uppercase!important;}
[data-testid="stDialogContent"] [data-testid="metric-container"] [data-testid="stMetricValue"]{font-family:'Orbitron',monospace!important;font-size:1.1rem!important;font-weight:700!important;color:#00e5ff!important;}
.msec{font-family:'Share Tech Mono',monospace;font-size:0.58rem;letter-spacing:0.25em;color:#3a6070;text-transform:uppercase;padding:0.8rem 0 0.4rem;border-bottom:1px solid #0a2a40;margin-bottom:0.7rem;display:flex;align-items:center;gap:7px;}
.msec::before{content:'';width:2px;height:0.75em;background:#00e5ff;box-shadow:0 0 6px rgba(0,229,255,0.4);display:inline-block;flex-shrink:0;}
.irow{display:flex;align-items:flex-start;gap:8px;padding:5px 0;font-family:'Rajdhani',sans-serif;font-size:0.87rem;color:#9bbccc;border-bottom:1px solid #070f18;line-height:1.4;}
.irow-up{color:#00ff88;font-size:0.65rem;margin-top:3px;flex-shrink:0;}
.irow-down{color:#ff3b5c;font-size:0.65rem;margin-top:3px;flex-shrink:0;}
.icol-label{font-family:'Share Tech Mono',monospace;font-size:0.55rem;letter-spacing:0.15em;text-transform:uppercase;padding:3px 10px;margin-bottom:7px;display:inline-block;border-radius:2px;}
.icol-bull{color:#00ff88;background:rgba(0,255,136,0.10);border:1px solid #00ff88;}
.icol-bear{color:#ff3b5c;background:rgba(255,59,92,0.12);border:1px solid #ff3b5c;}
.conv-track{height:5px;background:#0a2030;border-radius:2px;margin:5px 0 6px;overflow:hidden;}
.conv-fill{height:100%;background:linear-gradient(90deg,#00b8d4,#00e5ff);border-radius:2px;}
.conv-label{font-family:'Orbitron',monospace;font-size:0.72rem;font-weight:700;color:#e2eef5;letter-spacing:0.08em;}
.conv-desc{font-family:'Rajdhani',sans-serif;font-size:0.82rem;color:#7a9db0;margin-top:3px;line-height:1.5;}
.alert-box{background:rgba(255,59,92,0.10);border:1px solid #6a0020;border-left:3px solid #ff3b5c;padding:0.8rem 1rem;font-family:'Share Tech Mono',monospace;font-size:0.68rem;color:#ff8099;letter-spacing:0.06em;margin-bottom:0.7rem;line-height:1.5;}
.alert-message{font-family:'Rajdhani',sans-serif;font-size:0.9rem;color:#9bbccc;line-height:1.65;padding:0.5rem 0 0.7rem;}
.alert-action{background:rgba(0,229,255,0.06);border:1px solid #0d3050;border-left:3px solid #00e5ff;padding:0.6rem 1rem;font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#00b8d4;letter-spacing:0.06em;line-height:1.5;}
.macro-card{background:#040c18;border:1px solid #0a2a40;border-left:2px solid #ff9500;padding:0.7rem 1rem;margin-bottom:5px;}
.macro-title{font-family:'Orbitron',monospace;font-size:0.7rem;font-weight:700;color:#e2eef5;letter-spacing:0.06em;margin-bottom:4px;}
.macro-desc{font-family:'Rajdhani',sans-serif;font-size:0.85rem;color:#9bbccc;line-height:1.55;}
.drow{display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid #070f18;font-family:'Rajdhani',sans-serif;font-size:0.87rem;color:#9bbccc;line-height:1.4;}
.drow-arrow{color:#00e5ff;font-size:0.6rem;margin-top:4px;flex-shrink:0;}
.prow{display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid #070f18;font-family:'Rajdhani',sans-serif;font-size:0.87rem;color:#9bbccc;line-height:1.4;}
.prow-dot{color:#00e5ff;font-size:0.6rem;margin-top:4px;flex-shrink:0;}
.mhero{background:linear-gradient(90deg,#030c18,#06172a,#030c18);border-bottom:1px solid #0a2a40;padding:1.1rem 1.4rem;margin:-1rem -1rem 1rem -1rem;display:flex;justify-content:space-between;align-items:center;}
.mhero-name{font-family:'Orbitron',monospace;font-size:1.1rem;font-weight:900;letter-spacing:0.15em;color:#00e5ff;text-shadow:0 0 18px rgba(0,229,255,0.3);}
.mhero-sub{font-family:'Share Tech Mono',monospace;font-size:0.55rem;letter-spacing:0.28em;color:#3a6070;text-transform:uppercase;margin-top:3px;}
.mhero-score{font-family:'Orbitron',monospace;font-size:1.8rem;font-weight:700;line-height:1;text-shadow:0 0 18px rgba(0,229,255,0.3);}
.mhero-score-label{font-family:'Share Tech Mono',monospace;font-size:0.5rem;letter-spacing:0.22em;color:#3a6070;text-transform:uppercase;text-align:right;margin-top:3px;}
.analysis-text{font-family:'Rajdhani',sans-serif;font-size:0.93rem;color:#9bbccc;line-height:1.75;padding:0.5rem 0 0.2rem;}
.fdriver{font-family:'Rajdhani',sans-serif;font-size:0.82rem;color:#5a7a8a;padding:3px 0;border-bottom:1px solid #06141e;}
.src-tag{font-family:'Share Tech Mono',monospace;font-size:0.55rem;letter-spacing:0.1em;padding:2px 8px;background:rgba(0,229,255,0.06);border:1px solid #0d3050;color:#00b8d4;border-radius:2px;text-transform:uppercase;display:inline-block;margin-right:5px;margin-bottom:4px;}
</style>"""

# ── helpers ───────────────────────────────────────────────────────────────────

_BADGE_CLS = {"Critical":"rb-critical","High":"rb-high","Medium":"rb-medium","Low":"rb-low"}
_SCORE_CLR = {"Critical":"#ff3b5c","High":"#ff9500","Medium":"#ffe600","Low":"#00ff88"}
_TOP_CLR   = {"Critical":"#ff3b5c","High":"#ff9500","Medium":"#ffe600","Low":"#00ff88"}


def _pct(v):
    return min(float(v) * 100, 100)


def _msec(label, icon=""):
    return f'<div class="msec">{icon+"&nbsp;" if icon else ""}{label}</div>'


def _irows_up(items):
    return "".join(f'<div class="irow"><span class="irow-up">▲</span>{i}</div>' for i in items)


def _irows_down(items):
    return "".join(f'<div class="irow"><span class="irow-down">▼</span>{i}</div>' for i in items)


# ── modal body ────────────────────────────────────────────────────────────────

def _render_modal_body(country, analysis, score, news, risk, conflict_prob, match):
    bd_cls = _BADGE_CLS.get(risk, "rb-low")
    sc_clr = _SCORE_CLR.get(risk, "#00ff88")

    st.markdown(f"""
    <div class="mhero">
      <div>
        <div class="mhero-name">&#127758;&nbsp; {country.upper()}</div>
        <div class="mhero-sub">GEOPOLITICAL INTELLIGENCE BRIEF &nbsp;&#8212;&nbsp; LIVE</div>
      </div>
      <div style="text-align:right">
        <div style="margin-bottom:5px"><span class="risk-badge {bd_cls}">{risk.upper()}</span></div>
        <div class="mhero-score" style="color:{sc_clr}">{score:.4f}</div>
        <div class="mhero-score-label">GEORISK INDEX</div>
      </div>
    </div>""", unsafe_allow_html=True)

    conviction = get_conviction_score(score, news, conflict_prob)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("GeoRisk Score", f"{score:.4f}")
    m2.metric("Conflict Prob", f"{conflict_prob:.4f}")
    m3.metric("News Risk",     f"{news:.4f}")
    m4.metric("AI Conviction", f"{conviction['score']}%")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    render_global_signal_bar()

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "📋  ANALYSIS", "💹  MARKETS", "🧠  PORTFOLIO",
        "🚨  ALERTS",   "🌐  MACRO",   "📰  LIVE FEED",
    ])

    with t1:
        st.markdown(_msec("AI Intelligence Analysis", "🤖"), unsafe_allow_html=True)
        st.markdown(f'<div class="analysis-text">{analysis}</div>', unsafe_allow_html=True)

        st.markdown(_msec("Key Risk Drivers", "⚡"), unsafe_allow_html=True)
        drivers = []
        if conflict_prob > 0.90: drivers.append("Near-maximum conflict probability — imminent hostilities likely")
        if conflict_prob > 0.75: drivers.append("ML model flags high-probability conflict escalation trajectory")
        if news > 0.70:          drivers.append("Elevated news risk signal — high-frequency conflict reporting")
        elif news > 0.45:        drivers.append("Moderate media escalation signal detected across news sources")
        if score > 0.80:         drivers.append("Composite GeoRisk index exceeds critical threshold (>0.80)")
        if score < 0.35:         drivers.append("Stable regional outlook — low composite risk index")
        if not drivers:          drivers.append("Baseline geopolitical indicators elevated above global average")
        st.markdown("".join(f'<div class="drow"><span class="drow-arrow">&#9658;</span>{d}</div>' for d in drivers), unsafe_allow_html=True)

        st.markdown(_msec("AI Conviction Engine", "🧠"), unsafe_allow_html=True)
        cp = conviction["score"]
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px">
          <span class="conv-label">{conviction['level']}</span>
          <span style="font-family:'Share Tech Mono',monospace;font-size:0.82rem;color:#00e5ff">{cp}%</span>
        </div>
        <div class="conv-track"><div class="conv-fill" style="width:{cp}%"></div></div>
        <div class="conv-desc">{conviction['description']}</div>
        """, unsafe_allow_html=True)

        render_forecast_section(country)

    with t2:
        st.markdown(_msec("Market Impact Forecast", "💹"), unsafe_allow_html=True)
        impact = get_market_impact(country)
        ci1, ci2 = st.columns(2)
        with ci1:
            st.markdown('<div class="icol-label icol-bull">&#9650; BULLISH IMPACT</div>' + _irows_up(impact.get("bullish", [])), unsafe_allow_html=True)
        with ci2:
            st.markdown('<div class="icol-label icol-bear">&#9660; BEARISH IMPACT</div>' + _irows_down(impact.get("bearish", [])), unsafe_allow_html=True)
        render_market_section(country, risk)
        st.markdown(_msec("Dominant Macro Themes", "🌐"), unsafe_allow_html=True)
        for idx, theme in enumerate(get_macro_themes(country), 1):
            st.markdown(f'<div class="macro-card"><div class="macro-title">{idx}.&nbsp;{theme.get("theme","—")}</div><div class="macro-desc">{theme.get("description","—")}</div></div>', unsafe_allow_html=True)

    with t3:
        render_positioning_section(country, risk)

    with t4:
        st.markdown(_msec("Strategic Alert Engine", "🚨"), unsafe_allow_html=True)
        alert = get_strategic_alert(country)
        st.markdown(f"""
        <div class="alert-box">&#9650; {alert.get('title','—')}</div>
        <div class="alert-message">{alert.get('message','—')}</div>
        <div class="alert-action">&#9658; SUGGESTED ACTION:&nbsp; {alert.get('action','—')}</div>
        """, unsafe_allow_html=True)
        st.markdown(_msec("Intelligence Sources", "📎"), unsafe_allow_html=True)
        st.markdown("".join(f'<span class="src-tag">{s}</span>' for s in ["RANDOM FOREST ML","NEWS RISK ENGINE","GEORISK COMPOSITE","GEMINI AI"]), unsafe_allow_html=True)

    with t5:
        render_macro_section(country)

    with t6:
        render_news_section(country)


# ── card html ─────────────────────────────────────────────────────────────────

def _card_html(country, score, news, conflict_prob, risk, analysis_preview):
    bd_cls = _BADGE_CLS.get(risk, "rb-low")
    sc_clr = _SCORE_CLR.get(risk, "#00ff88")
    tc     = _TOP_CLR.get(risk, "#00ff88")
    short  = (analysis_preview[:155] + "…") if len(analysis_preview) > 155 else analysis_preview
    return f"""
<div class="geo-card">
  <div class="geo-card-top-bar" style="background:{tc}"></div>
  <div class="geo-card-inner">
    <div class="geo-card-header">
      <div class="geo-card-country">&#127758; {country.upper()}</div>
      <span class="risk-badge {bd_cls}">{risk.upper()}</span>
    </div>
    <div class="geo-card-metrics">
      <div class="card-metric"><div class="card-metric-label">GeoRisk</div><div class="card-metric-val" style="color:{sc_clr}">{score:.3f}</div></div>
      <div class="card-metric"><div class="card-metric-label">Conflict</div><div class="card-metric-val" style="color:#ff9500">{conflict_prob:.3f}</div></div>
      <div class="card-metric"><div class="card-metric-label">News</div><div class="card-metric-val" style="color:#ff3b5c">{news:.3f}</div></div>
    </div>
    <div class="geo-card-analysis">{short}</div>
    <div class="mbar"><span class="mbar-lbl">CONFLICT</span><div class="mbar-track"><div class="mbar-fill" style="width:{_pct(conflict_prob):.1f}%;background:#ff9500"></div></div><span class="mbar-val">{conflict_prob:.3f}</span></div>
    <div class="mbar"><span class="mbar-lbl">NEWS RISK</span><div class="mbar-track"><div class="mbar-fill" style="width:{_pct(news):.1f}%;background:#ff3b5c"></div></div><span class="mbar-val">{news:.3f}</span></div>
    <div class="mbar"><span class="mbar-lbl">GEORISK IDX</span><div class="mbar-track"><div class="mbar-fill" style="width:{_pct(score):.1f}%;background:{sc_clr}"></div></div><span class="mbar-val">{score:.3f}</span></div>
  </div>
</div>"""


# ── main render ───────────────────────────────────────────────────────────────

def render_ai_tab(ai_df, df):

    st.markdown(CARD_CSS, unsafe_allow_html=True)

    # auto-refresh every 45 s
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()
    if (time.time() - st.session_state.last_refresh) > 45:
        st.session_state.last_refresh = time.time()
        st.rerun()

    # LIVE SIGNAL HEADER — exactly once, fully inside st.markdown
        render_global_signal_bar()
    st.markdown("""
    <div style="background:#040d14;border:1px solid #0a2a40;border-left:3px solid #00ff88;
                padding:.75rem 1.2rem;margin-bottom:1.2rem;border-radius:10px;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-family:'Share Tech Mono',monospace;font-size:.58rem;color:#3a6070;letter-spacing:.1em">
          &#9658; SOURCES:&nbsp;
          <span style="color:#00e5ff">ML MODEL</span>&nbsp;+&nbsp;
          <span style="color:#ff9500">NEWS ENGINE</span>&nbsp;+&nbsp;
          <span style="color:#ff3b5c">WORLD BANK</span>&nbsp;+&nbsp;
          <span style="color:#00ff88">GEMINI AI</span>
        </span>
        <div style="padding:6px 14px;border-radius:999px;background:#00ff88;color:#020609;
                    font-size:.58rem;font-family:'Share Tech Mono',monospace;
                    letter-spacing:.18em;font-weight:700;">&#9679; LIVE</div>
      </div>
      <div style="margin-top:10px;font-family:'Share Tech Mono',monospace;font-size:.58rem;
                  color:#1a3a50;letter-spacing:.08em;">
        CLICK &#8220;OPEN INTEL&#8221; ON ANY CARD FOR FULL STRATEGIC BRIEFING
      </div>
    </div>
    """, unsafe_allow_html=True)

    if ai_df.empty:
        st.markdown(
            '<div style="background:rgba(255,59,92,.1);border:1px solid #ff3b5c;'
            'border-left:4px solid #ff3b5c;padding:1rem 1.4rem;'
            'font-family:\'Share Tech Mono\',monospace;font-size:.72rem;color:#ff8099;">'
            '&#9651; AI BRIEFING FILE MISSING — RUN PIPELINE FIRST</div>',
            unsafe_allow_html=True,
        )
        return

    chunks = [ai_df.head(6).iloc[i:i+3] for i in range(0, min(6, len(ai_df)), 3)]

    for chunk in chunks:
        cols = st.columns(3)
        for col_idx, (_, row) in enumerate(chunk.iterrows()):
            country  = str(row.get("Country", "Unknown"))
            analysis = (
                str(row.get("AI_Analysis", "No analysis available."))
                .replace("<", "").replace(">", "").replace("```", "")
            )
            match = df[df["Country"] == country]
            if not match.empty:
                score         = float(match["GeoRisk_Live_Score"].values[0])
                news          = float(match["News_Risk_Score"].values[0])
                risk          = str(match["Dynamic_Risk_Level"].values[0])
                conflict_prob = float(match["Conflict_Probability"].values[0])
            else:
                score = news = conflict_prob = 0.0
                risk  = "Low"

            with cols[col_idx]:
                st.markdown(_card_html(country, score, news, conflict_prob, risk, analysis), unsafe_allow_html=True)
                if st.button(f"&#9651;  OPEN INTEL  —  {country.upper()}", key=f"btn_{country}_{col_idx}", use_container_width=True):
                    _c, _a, _s, _n, _r, _cp, _m = country, analysis, score, news, risk, conflict_prob, match

                    @st.dialog(f"INTEL — {_c.upper()}", width="large")
                    def _modal():
                        _render_modal_body(_c, _a, _s, _n, _r, _cp, _m)

                    _modal()

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)