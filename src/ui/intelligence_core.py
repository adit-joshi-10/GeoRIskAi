import streamlit as st
import streamlit.components.v1 as components


def render_intelligence_core(df):

    avg_score      = round(df["GeoRisk_Live_Score"].mean() * 100, 1)
    total          = len(df)
    critical_count = int((df["Dynamic_Risk_Level"] == "Critical").sum())

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600&display=swap');

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
        background: transparent;
        font-family: 'Rajdhani', sans-serif;
        color: #c8dde8;
    }}

    .modal {{
        background: linear-gradient(180deg, #040d14 0%, #020609 100%);
        border: 1px solid #0a2a40;
        border-top: 2px solid #00e5ff;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow:
            0 0 60px rgba(0,229,255,0.08),
            0 0 120px rgba(0,0,0,0.8);
        position: relative;
        overflow: hidden;
        animation: slideUp 0.35s cubic-bezier(0.16,1,0.3,1);
    }}

    @keyframes slideUp {{
        from {{ opacity:0; transform:translateY(20px); }}
        to   {{ opacity:1; transform:translateY(0); }}
    }}

    .modal::before {{
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
    }}

    @keyframes scanH {{
        0%,100% {{ opacity:0.3; }}
        50%      {{ opacity:1; }}
    }}

    .modal-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.4rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #0a2a40;
    }}

    .modal-title {{
        font-family: 'Orbitron', monospace;
        font-size: 1rem;
        font-weight: 700;
        color: #00e5ff;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        text-shadow: 0 0 15px rgba(0,229,255,0.4);
    }}

    .modal-subtitle {{
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.58rem;
        letter-spacing: 0.25em;
        color: #3a6070;
        text-transform: uppercase;
        margin-top: 4px;
    }}

    .sys-online {{
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.6rem;
        color: #00ff88;
        letter-spacing: 0.15em;
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    .dot {{
        width: 7px;
        height: 7px;
        border-radius: 50%;
        animation: pulseDot 2s ease-in-out infinite;
    }}

    .dot-green  {{ background: #00ff88; box-shadow: 0 0 8px rgba(0,255,136,0.7); }}
    .dot-cyan   {{ background: #00e5ff; box-shadow: 0 0 8px rgba(0,229,255,0.7); animation-delay: 0.5s; }}
    .dot-orange {{ background: #ff9500; box-shadow: 0 0 8px rgba(255,149,0,0.7); animation-delay: 1s; }}

    @keyframes pulseDot {{
        0%,100% {{ opacity:1; transform:scale(1); }}
        50%      {{ opacity:0.4; transform:scale(0.7); }}
    }}

    .stats-row {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 10px;
        margin-bottom: 1.4rem;
    }}

    .stat-box {{
        background: rgba(0,229,255,0.04);
        border: 1px solid #0a2a40;
        border-top: 2px solid #00e5ff;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }}

    .stat-value {{
        font-family: 'Orbitron', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: #00e5ff;
        text-shadow: 0 0 12px rgba(0,229,255,0.4);
    }}

    .stat-value.red {{
        color: #ff3b5c;
        text-shadow: 0 0 12px rgba(255,59,92,0.4);
    }}

    .stat-label {{
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.52rem;
        letter-spacing: 0.15em;
        color: #3a6070;
        text-transform: uppercase;
        margin-top: 4px;
    }}

    .section-title {{
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.6rem;
        letter-spacing: 0.25em;
        color: #3a6070;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .section-title::after {{
        content: '';
        flex: 1;
        height: 1px;
        background: #0a2a40;
    }}

    .status-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 1.4rem;
    }}

    .status-item {{
        background: rgba(0,229,255,0.03);
        border: 1px solid #0a2a40;
        border-radius: 8px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.08em;
        color: #7a9db0;
        text-transform: uppercase;
    }}

    .pipeline {{
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin-bottom: 1.4rem;
    }}

    .pipeline-step {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 9px 14px;
        background: rgba(0,229,255,0.03);
        border: 1px solid #0a2a40;
        border-left: 3px solid #00e5ff;
        border-radius: 6px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.68rem;
        color: #7a9db0;
        letter-spacing: 0.06em;
    }}

    .step-name {{ flex: 1; }}

    .step-badge {{
        font-size: 0.52rem;
        padding: 2px 8px;
        border-radius: 3px;
        background: rgba(0,229,255,0.1);
        border: 1px solid rgba(0,229,255,0.25);
        color: #00e5ff;
        letter-spacing: 0.1em;
    }}

    .formula-box {{
        background: #020d18;
        border: 1px solid #0a2a40;
        border-left: 3px solid #00e5ff;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.72rem;
        color: #7a9db0;
        line-height: 2.2;
        margin-bottom: 1.4rem;
    }}

    .formula-hl {{ color: #00e5ff; font-weight: bold; }}
    .formula-w  {{ color: #ff9500; }}

    .threat-tags {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 1.4rem;
    }}

    .threat-tag {{
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.58rem;
        letter-spacing: 0.1em;
        padding: 3px 10px;
        border-radius: 3px;
        background: rgba(255,59,92,0.08);
        border: 1px solid rgba(255,59,92,0.2);
        color: #ff6b85;
        text-transform: uppercase;
    }}

    .modal-footer {{
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #0a2a40;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.52rem;
        color: #1a3a50;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        display: flex;
        justify-content: space-between;
    }}

    @media (max-width: 480px) {{
        .stats-row   {{ grid-template-columns: 1fr 1fr; }}
        .status-grid {{ grid-template-columns: 1fr; }}
        .stat-value  {{ font-size: 1.2rem; }}
        .modal       {{ padding: 1.2rem; }}
    }}
</style>
</head>
<body>
<div class="modal">

    <!-- HEADER -->
    <div class="modal-header">
        <div>
            <div class="modal-title">⚡ Intelligence Core</div>
            <div class="modal-subtitle">GeoRiskAI — System Architecture v2.1</div>
        </div>
        <div class="sys-online">
            <div class="dot dot-green"></div>
            ALL SYSTEMS ONLINE
        </div>
    </div>

    <!-- STATS -->
    <div class="stats-row">
        <div class="stat-box">
            <div class="stat-value">{total}</div>
            <div class="stat-label">Countries Tracked</div>
        </div>
        <div class="stat-box">
            <div class="stat-value red">{critical_count}</div>
            <div class="stat-label">Critical Alerts</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{avg_score}%</div>
            <div class="stat-label">AI Confidence</div>
        </div>
    </div>

    <!-- ENGINE STATUS -->
    <div class="section-title">Engine Status</div>
    <div class="status-grid">
        <div class="status-item">
            <div class="dot dot-green"></div>
            ML Engine — Online
        </div>
        <div class="status-item">
            <div class="dot dot-cyan"></div>
            News Engine — Active
        </div>
        <div class="status-item">
            <div class="dot dot-cyan"></div>
            Fusion Engine — Active
        </div>
        <div class="status-item">
            <div class="dot dot-orange"></div>
            AI Analyst — Running
        </div>
    </div>

    <!-- PIPELINE -->
    <div class="section-title">Prediction Pipeline</div>
    <div class="pipeline">
        <div class="pipeline-step">
            <span>📡</span>
            <span class="step-name">GDELT / RSS News Feed</span>
            <span class="step-badge">LIVE</span>
        </div>
        <div class="pipeline-step">
            <span>🔍</span>
            <span class="step-name">Keyword Intelligence Filter</span>
            <span class="step-badge">ACTIVE</span>
        </div>
        <div class="pipeline-step">
            <span>🤖</span>
            <span class="step-name">Random Forest ML Model</span>
            <span class="step-badge">ONLINE</span>
        </div>
        <div class="pipeline-step">
            <span>⚡</span>
            <span class="step-name">Fusion Engine</span>
            <span class="step-badge">RUNNING</span>
        </div>
        <div class="pipeline-step">
            <span>📊</span>
            <span class="step-name">GeoRisk Live Score Output</span>
            <span class="step-badge">OUTPUT</span>
        </div>
        <div class="pipeline-step">
            <span>🧠</span>
            <span class="step-name">AI Briefing System</span>
            <span class="step-badge">ACTIVE</span>
        </div>
    </div>

    <!-- FORMULA -->
    <div class="section-title">Risk Formula</div>
    <div class="formula-box">
        <span class="formula-hl">GeoRisk Score</span> =<br>
        &nbsp;&nbsp;<span class="formula-w">0.45</span> × ML Conflict Score<br>
        &nbsp;&nbsp;<span class="formula-w">0.35</span> × News Risk Signal<br>
        &nbsp;&nbsp;<span class="formula-w">0.20</span> × Historical Conflict Probability
    </div>

    <!-- THREAT KEYWORDS -->
    <div class="section-title">Active Threat Keywords</div>
    <div class="threat-tags">
        <span class="threat-tag">WAR</span>
        <span class="threat-tag">MISSILE</span>
        <span class="threat-tag">SANCTIONS</span>
        <span class="threat-tag">MILITARY</span>
        <span class="threat-tag">TERRORISM</span>
        <span class="threat-tag">NUCLEAR</span>
        <span class="threat-tag">BORDER CONFLICT</span>
        <span class="threat-tag">AIRSTRIKE</span>
        <span class="threat-tag">INVASION</span>
        <span class="threat-tag">CEASEFIRE</span>
        <span class="threat-tag">INSURGENCY</span>
        <span class="threat-tag">CYBER ATTACK</span>
    </div>

    <!-- FOOTER -->
    <div class="modal-footer">
        <span>GeoRiskAI Intelligence Core v2.1</span>
        <span>UNCLASSIFIED — LIVE MONITORING</span>
    </div>

</div>
</body>
</html>
"""

    components.html(html_content, height=900, scrolling=True)

    # ── CLOSE BUTTON ────────────────────────────────
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(
            "✕  Close Intelligence Core",
            use_container_width=True,
            key="close_intel_core",
        ):
            st.session_state.intel_panel_open = False
            st.rerun()