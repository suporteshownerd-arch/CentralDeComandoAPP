"""
Módulo de estilos e design system
Central de Comando DPSP v2.0
"""


def get_base_css() -> str:
    """CSS base com variáveis, fontes e reset - Design System v4.0"""
    return """
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    :root {
        --bg: #0a0a0f;
        --bg2: #12121a;
        --bg3: #1a1a24;
        --surface: #222230;
        --surface2: #2a2a3a;
        --border: rgba(255,255,255,0.06);
        --border2: rgba(255,255,255,0.12);
        --border3: rgba(255,255,255,0.18);
        --text: #f0f0f5;
        --text2: #a0a0b0;
        --text3: #606070;
        --accent: #6366f1;
        --accent-light: #818cf8;
        --accent-hover: #5558e3;
        --accent-glow: rgba(99,102,241,0.25);
        --green: #10b981;
        --green-light: #34d399;
        --red: #ef4444;
        --red-light: #f87171;
        --amber: #f59e0b;
        --amber-light: #fbbf24;
        --purple: #a855f7;
        --purple-light: #c084fc;
        --cyan: #06b6d4;
        --blue: #3b82f6;
    }

    * { box-sizing: border-box; }
    
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg2); }
    ::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text3); }

    /* ── App background ── */
    .stApp { 
        background: var(--bg) !important;
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.15), transparent),
            radial-gradient(ellipse 60% 40% at 100% 0%, rgba(168,85,247,0.1), transparent) !important;
    }
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1280px; }
    
    /* ── Gradient text ── */
    .gradient-text {
        background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child {
        background: var(--bg2) !important;
    }
    section[data-testid="stSidebar"] {
        border-right: 1px solid var(--border) !important;
    }
    /* Remove padding extra do Streamlit dentro da sidebar */
    section[data-testid="stSidebar"] .block-container {
        padding: 0 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       SIDEBAR PREMIUM v4.5
       ═══════════════════════════════════════════════════════════════════════ */
    
    /* Header Premium */
    .sb-header-premium {
        background: linear-gradient(180deg, var(--bg2) 0%, var(--bg) 100%);
        padding: 20px;
        border-bottom: 1px solid var(--border);
    }
    .sb-logo-premium {
        display: flex; align-items: center; gap: 14px;
        margin-bottom: 16px;
    }
    .sb-logo-icon-premium {
        width: 52px; height: 52px;
        background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px;
        box-shadow: 0 6px 24px var(--accent-glow);
    }
    .sb-logo-text { flex: 1; }
    .sb-logo-title-premium {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 20px; font-weight: 700; color: var(--text);
    }
    .sb-logo-sub-premium {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; color: var(--text3);
        margin-top: 2px;
    }
    
    .sb-status-premium {
        display: flex; align-items: center; gap: 12px;
        padding: 12px 16px;
        background: linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(6,182,212,0.08) 100%);
        border: 1px solid rgba(16,185,129,0.3);
        border-radius: 12px;
    }
    .sb-status-dot-premium {
        width: 10px; height: 10px;
        background: var(--green-light);
        border-radius: 50%;
        box-shadow: 0 0 12px var(--green);
        animation: pulse-premium 2s infinite;
    }
    @keyframes pulse-premium { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.6;transform:scale(0.9)} }
    .sb-status-title-premium {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px; font-weight: 600; color: var(--green-light);
    }
    .sb-status-time-premium {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; color: var(--text3);
    }
    
    /* Dividers */
    .sb-divider-premium {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--border) 50%, transparent 100%);
        margin: 16px 0;
    }
    .sb-divider-premium-light {
        height: 1px;
        background: var(--border);
        margin: 12px 0;
        opacity: 0.5;
    }
    
    /* Hero KPI */
    .sb-hero-kpi {
        text-align: center;
        padding: 24px 20px;
        background: linear-gradient(135deg, var(--bg3) 0%, var(--surface) 100%);
        border: 1px solid var(--border);
        margin: 0 16px 16px 16px;
        border-radius: 16px;
    }
    .sb-hero-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; color: var(--accent-light);
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 8px;
    }
    .sb-hero-value {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 56px;
        font-weight: 700;
        background: linear-gradient(135deg, var(--accent-light) 0%, var(--purple-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    .sb-hero-sub {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px; color: var(--text2);
        margin-top: 4px;
    }
    .sb-hero-progress {
        margin-top: 16px;
    }
    .sb-hero-bar {
        height: 8px;
        background: var(--surface);
        border-radius: 8px;
        overflow: hidden;
    }
    .sb-hero-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--green) 0%, var(--accent) 100%);
        border-radius: 8px;
    }
    .sb-hero-percent {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px; color: var(--text2);
        margin-top: 8px;
    }
    
    /* Section Premium */
    .sb-section-premium {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: var(--text3);
        text-transform: uppercase;
        letter-spacing: 0.22em;
        padding: 12px 20px 8px 20px;
        font-weight: 600;
    }
    
    /* KPI Cards */
    .sb-card-kpi {
        text-align: center;
        padding: 16px 12px;
        margin: 4px 8px;
        border-radius: 14px;
        transition: all 0.2s ease;
    }
    .sb-card-kpi:hover { transform: translateY(-2px); }
    .sb-card-kpi.green {
        background: linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(16,185,129,0.05) 100%);
        border: 1px solid rgba(16,185,129,0.25);
    }
    .sb-card-kpi.red {
        background: linear-gradient(135deg, rgba(239,68,68,0.15) 0%, rgba(239,68,68,0.05) 100%);
        border: 1px solid rgba(239,68,68,0.25);
    }
    .sb-card-kpi-icon {
        font-size: 18px; margin-bottom: 6px;
    }
    .sb-card-kpi.green .sb-card-kpi-icon { color: var(--green-light); }
    .sb-card-kpi.red .sb-card-kpi-icon { color: var(--red-light); }
    .sb-card-kpi-value {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 28px; font-weight: 700;
    }
    .sb-card-kpi.green .sb-card-kpi-value { color: var(--green-light); }
    .sb-card-kpi.red .sb-card-kpi-value { color: var(--red-light); }
    .sb-card-kpi-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; color: var(--text3);
        text-transform: uppercase;
        margin-top: 4px;
    }
    
    /* Bar Items */
    .sb-bar-item {
        padding: 8px 20px;
    }
    .sb-bar-header {
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 6px;
    }
    .sb-bar-dot {
        width: 8px; height: 8px; border-radius: 50%;
    }
    .sb-bar-rank {
        width: 18px; height: 18px;
        background: var(--surface);
        border-radius: 50%;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: var(--text3);
        display: flex; align-items: center; justify-content: center;
    }
    .sb-bar-name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px; color: var(--text);
        flex: 1;
    }
    .sb-bar-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px; color: var(--text2);
    }
    .sb-bar-track {
        height: 6px;
        background: var(--surface);
        border-radius: 6px;
        overflow: hidden;
    }
    .sb-bar-fill {
        height: 100%;
        background: var(--accent);
        border-radius: 6px;
    }
    
    /* Connectivity Premium */
    .sb-connect-premium {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        padding: 8px 20px;
    }
    .sb-connect-card {
        display: flex; align-items: center; gap: 12px;
        padding: 14px;
        background: var(--bg3);
        border: 1px solid var(--border);
        border-radius: 12px;
    }
    .sb-connect-icon-premium {
        font-size: 22px;
    }
    .sb-connect-details {
        display: flex; flex-direction: column;
    }
    .sb-connect-name {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px; color: var(--text3);
        text-transform: uppercase;
    }
    .sb-connect-num {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 18px; font-weight: 700; color: var(--text);
    }
    .sb-connect-pct {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; color: var(--accent-light);
    }
    .sb-connect-total {
        padding: 8px 20px 16px 20px;
    }
    .sb-connect-total span {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 12px; color: var(--text2);
    }
    .sb-connect-bar {
        height: 6px;
        background: var(--surface);
        border-radius: 6px;
        margin-top: 8px;
        overflow: hidden;
    }
    .sb-connect-bar div {
        height: 100%;
        background: linear-gradient(90deg, var(--cyan) 0%, var(--accent) 100%);
        border-radius: 6px;
    }
    
    /* Favoritos Premium */
    .sb-fav-premium {
        display: flex; align-items: center; gap: 10px;
        padding: 10px 20px;
        margin: 4px 16px;
        background: var(--bg3);
        border-radius: 10px;
        transition: all 0.2s ease;
    }
    .sb-fav-premium:hover { background: var(--surface); }
    .sb-fav-vd-premium {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px; color: var(--accent-light);
        background: rgba(99,102,241,0.15);
        padding: 4px 8px; border-radius: 6px;
    }
    .sb-fav-name-premium {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px; color: var(--text2);
        flex: 1;
    }
    .sb-fav-status-premium {
        font-size: 14px;
    }
    
    /* Contacts Premium */
    .sb-contacts-premium {
        padding: 8px 16px;
    }
    .sb-contact-premium {
        display: flex; align-items: center; gap: 12px;
        padding: 12px;
        margin-bottom: 8px;
        background: var(--bg3);
        border: 1px solid var(--border);
        border-radius: 12px;
        text-decoration: none !important;
        transition: all 0.2s ease;
    }
    .sb-contact-premium:hover {
        background: var(--surface);
        border-color: var(--accent);
    }
    .sb-contact-icon-premium {
        font-size: 20px;
    }
    .sb-contact-name-premium {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px; font-weight: 600; color: var(--text);
    }
    .sb-contact-tel-premium {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; color: var(--text3);
    }
        padding: 8px 20px 6px 20px;
        font-weight: 500;
    }

    /* ── KPI Cards ── */
    .sb-kpi-card {
        text-align: center;
        padding: 12px 8px;
        border-radius: 12px;
        margin: 4px 8px;
        transition: all 0.2s ease;
    }
    .sb-kpi-card:hover { transform: translateY(-2px); }
    .sb-kpi-card.green { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); }
    .sb-kpi-card.red { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); }
    .sb-kpi-card.accent { background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.2); }
    .sb-kpi-card .sb-kpi-value {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 24px;
        font-weight: 700;
    }
    .sb-kpi-card.green .sb-kpi-value { color: var(--green-light); }
    .sb-kpi-card.red .sb-kpi-value { color: var(--red-light); }
    .sb-kpi-card.accent .sb-kpi-value { color: var(--accent-light); }
    .sb-kpi-card .sb-kpi-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: var(--text3);
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* ── Progress Bar ── */
    .sb-progress-container {
        padding: 8px 20px 16px 20px;
    }
    .sb-progress-bar {
        height: 8px;
        background: var(--surface);
        border-radius: 8px;
        overflow: hidden;
    }
    .sb-progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--green) 0%, var(--accent) 100%);
        border-radius: 8px;
        transition: width 0.5s ease;
    }
    .sb-progress-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: var(--text2);
        margin-top: 6px;
        text-align: center;
    }

    /* ── Distribution Items ── */
    .sb-dist-item {
        display: flex; align-items: center; gap: 10px;
        padding: 8px 20px;
    }
    .sb-dist-dot {
        width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
    }
    .sb-dist-icon {
        font-size: 14px; width: 20px; text-align: center;
    }
    .sb-dist-name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        color: var(--text);
        flex: 1;
        min-width: 50px;
    }
    .sb-dist-bar {
        flex: 2;
        height: 6px;
        background: var(--surface);
        border-radius: 6px;
        overflow: hidden;
    }
    .sb-dist-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 0.3s ease;
    }
    .sb-dist-pct {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: var(--text2);
        min-width: 40px;
        text-align: right;
    }

    /* ── Connectivity Grid ── */
    .sb-connect-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        padding: 8px 20px;
    }
    .sb-connect-item {
        display: flex; align-items: center; gap: 12px;
        padding: 14px;
        background: var(--bg3);
        border: 1px solid var(--border);
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    .sb-connect-item:hover {
        border-color: var(--accent);
        background: var(--surface);
    }
    .sb-connect-icon {
        font-size: 24px;
    }
    .sb-connect-info {
        display: flex; flex-direction: column;
    }
    .sb-connect-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: var(--text3);
        text-transform: uppercase;
    }
    .sb-connect-value {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: var(--text);
    }
    .sb-connect-bar {
        padding: 8px 20px 16px 20px;
    }
    .sb-connect-bar span {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: var(--text2);
    }
    .sb-connect-progress {
        height: 4px;
        background: var(--surface);
        border-radius: 4px;
        margin-top: 6px;
        overflow: hidden;
    }
    .sb-connect-progress div {
        height: 100%;
        background: linear-gradient(90deg, var(--green) 0%, var(--accent) 100%);
        border-radius: 4px;
    }

    /* ── Status ── */
    .sb-status {
        display: flex; align-items: center; gap: 12px;
        margin: 0 16px 0 16px;
        padding: 12px 16px;
        background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(6,182,212,0.05) 100%);
        border: 1px solid rgba(16,185,129,0.25);
        border-radius: 14px;
    }
    .sb-status-content {
        display: flex; flex-direction: column; gap: 2px;
    }
    .sb-status-title {
        font-size: 13px !important; color: var(--green-light) !important; font-weight: 600;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .sb-status-meta {
        font-size: 11px !important; color: var(--text3) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .sb-status-dot {
        width: 10px; height: 10px; background: var(--green-light); border-radius: 50%;
        animation: sb-pulse 2s infinite; flex-shrink: 0;
        box-shadow: 0 0 12px var(--green);
    }
    @keyframes sb-pulse { 0%,100%{opacity:1; transform: scale(1);} 50%{opacity:.6; transform: scale(0.85);} }

    /* ── KPI Principal ── */
    .sb-kpi-main {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, var(--bg3) 0%, var(--surface) 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        margin: 8px 16px;
    }
    .sb-kpi-main-value {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 42px;
        font-weight: 700;
        color: var(--accent-light);
        line-height: 1;
    }
    .sb-kpi-main-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: var(--text3);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 8px;
    }

    /* ── Divider Light ── */
    .sb-divider-light {
        height: 1px;
        background: var(--border);
        margin: 12px 16px;
        opacity: 0.5;
    }

    /* ── Stat Item (Bandeira) ── */
    .sb-stat-item {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 16px;
        margin: 4px 0;
        background: var(--bg3);
        border-radius: 10px;
        transition: all 0.2s ease;
    }
    .sb-stat-item:hover {
        background: var(--surface);
        transform: translateX(4px);
    }
    .sb-stat-header {
        display: flex; align-items: center; gap: 10px;
    }
    .sb-stat-dot {
        width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
    }
    .sb-stat-name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px;
        color: var(--text);
        font-weight: 500;
    }
    .sb-stat-values {
        display: flex; align-items: center; gap: 6px;
    }
    .sb-stat-qtd {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        color: var(--text);
        font-weight: 600;
    }
    .sb-stat-pct {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: var(--text3);
    }

    /* ── Circuit Stats ── */
    .sb-circuit-stats {
        display: flex; gap: 12px;
        padding: 0 16px;
        margin: 8px 0;
    }
    .sb-circuit-item {
        flex: 1;
        display: flex; align-items: center; gap: 10px;
        padding: 14px;
        background: var(--bg3);
        border: 1px solid var(--border);
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    .sb-circuit-item:hover {
        border-color: var(--accent);
        background: var(--surface);
    }
    .sb-circuit-icon {
        font-size: 20px;
    }
    .sb-circuit-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        color: var(--text2);
    }
    .sb-circuit-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 16px;
        color: var(--accent-light);
        font-weight: 600;
        margin-left: auto;
    }

    /* ── Dividers ── */
    .sb-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--border) 50%, transparent 100%);
        margin: 20px 0;
    }

    /* ── Quick Search ── */
    .sb-quick-search {
        padding: 0 16px;
        margin-bottom: 8px;
    }
    .sb-search-input {
        width: 100%;
        background: var(--surface);
        border: 1px solid var(--border2);
        border-radius: 12px;
        padding: 12px 16px;
        color: var(--text);
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        outline: none;
        transition: all 0.2s ease;
    }
    .sb-search-input::placeholder { color: var(--text3); }
    .sb-search-input:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 4px var(--accent-glow);
    }
    
    /* ── Stats by Bandeira ── */
    .sb-stats-box {
        background: var(--bg3);
        border: 1px solid var(--border);
        border-radius: 14px;
        margin: 8px 16px;
        padding: 12px;
    }
    .sb-stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid var(--border);
    }
    .sb-stat-row:last-child { border-bottom: none; }
    .sb-stat-label {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 13px;
        color: var(--text2);
        font-weight: 500;
    }
    .sb-stat-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: var(--text);
        font-weight: 600;
    }
    .sb-stat-pct {
        color: var(--text3);
        font-size: 11px;
    }
    
    /* ── Enhanced Favoritos ── */
    .sb-fav-item {
        display: flex; align-items: center; gap: 10px;
        padding: 10px 16px; margin: 0 8px 4px 8px;
        border-radius: 12px; cursor: default;
        background: var(--bg3);
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    .sb-fav-item:hover { 
        background: var(--surface); 
        border-color: var(--border2);
    }
    .sb-fav-vd {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px; color: var(--accent-light);
        background: rgba(99,102,241,0.15);
        padding: 4px 10px; border-radius: 8px;
        flex-shrink: 0;
    }
    .sb-fav-nome {
        font-size: 13px !important; color: var(--text2);
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        flex: 1;
    }
    .sb-fav-status {
        font-size: 12px;
        flex-shrink: 0;
    }

    /* ── Section labels ── */
    .sb-section-label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 10px !important; color: var(--text3) !important;
        text-transform: uppercase; letter-spacing: .18em;
        padding: 0 16px; margin-bottom: 8px; margin-top: 16px;
    }

    /* ── KPI row ── */
    .sb-kpi-row {
        display: flex; align-items: stretch;
        margin: 0 12px 10px 12px;
        background: var(--bg3);
        border: 1px solid var(--border);
        border-radius: 16px;
        overflow: hidden;
        padding: 4px;
    }
    .sb-kpi {
        flex: 1; text-align: center;
        padding: 16px 8px;
        border-radius: 12px;
        transition: background 0.2s;
    }
    .sb-kpi:hover { background: var(--surface); }
    .sb-kpi-value {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 28px !important; font-weight: 700; line-height: 1;
        letter-spacing: -0.02em;
    }
    .sb-kpi-value.accent { color: var(--accent-light); }
    .sb-kpi-value.green  { color: var(--green-light); }
    .sb-kpi-value.red    { color: var(--red-light); }
    .sb-kpi-label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 10px !important; color: var(--text3) !important;
        text-transform: uppercase; margin-top: 8px; letter-spacing: 0.05em;
    }
    .sb-kpi-sep {
        width: 1px;
        background: var(--border); flex-shrink: 0;
        align-self: stretch;
    }

    /* ── Progress bar ── */
    .sb-bar-wrap {
        margin: 0 12px 6px 12px;
        height: 6px; border-radius: 6px;
        background: var(--surface);
        overflow: hidden;
    }
    .sb-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--accent) 0%, var(--purple) 100%);
        border-radius: 6px;
        transition: width .6s ease;
        box-shadow: 0 0 12px var(--accent-glow);
    }
    .sb-bar-legend {
        display: flex; justify-content: space-between;
        padding: 4px 12px 12px 12px;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
    }
    .sb-bar-legend .green { color: var(--green-light); }
    .sb-bar-legend .red   { color: var(--red-light); }

    /* ── Navegação ── */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        border-radius: 12px !important;
        text-align: left !important;
        padding: 12px 16px 12px 18px !important;
        color: var(--text2) !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
        margin: 2px 8px !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: var(--surface) !important;
        color: var(--text) !important;
        transform: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button:focus:not(:active) {
        box-shadow: none !important; outline: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button p {
        font-size: 14px !important; color: inherit !important; text-align: left !important;
    }

    /* ── Nav active marker → ativo ── */
    .nav-icon-hint { display: none; height: 0; }
    .nav-active-marker { display: none; height: 0; margin: 0; padding: 0; }

    .nav-active-marker + div + div[data-testid="stButton"] > button,
    .nav-active-marker + div[data-testid="stButton"] > button,
    .nav-active-marker ~ div[data-testid="stButton"]:first-of-type > button {
        background: linear-gradient(135deg, rgba(99,102,241,0.2) 0%, rgba(168,85,247,0.15) 100%) !important;
        color: var(--accent-light) !important;
        font-weight: 600 !important;
        border-left: 3px solid var(--accent) !important;
        box-shadow: 0 0 20px var(--accent-glow) !important;
    }
    .nav-active-marker + div + div[data-testid="stButton"] > button:hover,
    .nav-active-marker + div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, rgba(99,102,241,0.25) 0%, rgba(168,85,247,0.2) 100%) !important;
    }

    /* ── Favorites ── */
    .sb-fav-item {
        display: flex; align-items: center; gap: 8px;
        padding: 5px 12px; margin: 0 4px 2px 4px;
        border-radius: 7px; cursor: default;
    }
    .sb-fav-item:hover { background: rgba(91,141,239,.07); }
    .sb-fav-vd {
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important; color: #5b8def;
        background: rgba(91,141,239,.14);
        padding: 1px 6px; border-radius: 4px; flex-shrink: 0;
    }
    .sb-fav-nome {
        font-size: 12px !important; color: #9094a6;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }

    /* ── Contacts ── */
    .sb-contacts {
        margin: 0 12px;
        background: var(--bg3);
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }
    .sb-contact-item {
        display: flex; align-items: center; gap: 10px;
        padding: 10px 12px;
        border-bottom: 1px solid rgba(255,255,255,.05);
        text-decoration: none !important;
        transition: background .15s;
    }
    .sb-contact-item:last-child { border-bottom: none; }
    .sb-contact-item:hover { background: rgba(91,141,239,.07) !important; }
    .sb-contact-icon { font-size: 16px; flex-shrink: 0; }
    .sb-contact-name {
        font-size: 12px !important; color: #eaecf0 !important;
        font-weight: 600; line-height: 1.2;
    }
    .sb-contact-tel {
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important; color: #5c6370;
    }

    /* ── Headings ── */
    h1 { font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; font-size: 32px !important; letter-spacing: -0.03em; color: var(--text) !important; }
    h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif !important; color: var(--text) !important; }
    h2 { font-size: 24px !important; font-weight: 600 !important; }
    h3 { font-size: 18px !important; font-weight: 600 !important; }

    /* ── Metrics ── */
    [data-testid="stMetric"] { 
        background: var(--bg2) !important; 
        border: 1px solid var(--border) !important; 
        border-radius: 16px !important; 
        padding: 20px 24px !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stMetric"]:hover {
        border-color: var(--border2) !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
    }
    [data-testid="stMetricLabel"] { 
        color: var(--text3) !important; 
        font-family: 'JetBrains Mono', monospace !important; 
        font-size: 11px !important; 
        text-transform: uppercase; 
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] { 
        color: var(--text) !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
        font-weight: 700 !important; 
        font-size: 32px !important; 
        letter-spacing: -0.02em;
    }
    [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input { 
        background: var(--surface) !important; 
        border: 1px solid var(--border2) !important; 
        border-radius: 12px !important; 
        color: var(--text) !important;
        padding: 12px 16px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14px !important;
    }
    .stTextInput > div > div > input::placeholder { color: var(--text3) !important; }
    .stTextInput > div > div > input:focus { 
        border-color: var(--accent) !important; 
        box-shadow: 0 0 0 4px var(--accent-glow) !important; 
    }
    .stSelectbox > div > div > div { 
        background: var(--surface) !important; 
        border: 1px solid var(--border2) !important; 
        border-radius: 12px !important;
        padding: 8px 12px !important;
    }
    .stSelectbox > div > div > div:hover { border-color: var(--border3) !important; }
    .stTextArea > div > div > textarea { 
        background: var(--surface) !important; 
        border: 1px solid var(--border2) !important; 
        border-radius: 12px !important; 
        color: var(--text) !important;
        padding: 12px 16px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .stTextArea > div > div > textarea:focus { 
        border-color: var(--accent) !important; 
        box-shadow: 0 0 0 4px var(--accent-glow) !important; 
    }

    /* ── Buttons ── */
    .stButton > button { 
        border-radius: 12px !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
        font-weight: 600 !important; 
        transition: all 0.2s ease !important; 
        border: 1px solid var(--border2) !important;
        padding: 10px 20px !important;
        font-size: 14px !important;
    }
    .stButton > button:hover { 
        transform: translateY(-2px) !important; 
        box-shadow: 0 8px 24px rgba(0,0,0,0.4) !important;
        border-color: var(--border3) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px; background: var(--bg2); padding: 6px;
        border-radius: 16px; border: 1px solid var(--border);
        margin-bottom: 16px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important; border-radius: 12px !important;
        padding: 10px 24px !important; font-weight: 500 !important;
        font-size: 14px !important; color: var(--text2) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        border: none !important; transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--surface) !important; color: var(--text) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%) !important; 
        color: white !important;
        font-weight: 600 !important; 
        box-shadow: 0 4px 16px var(--accent-glow) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-border"]    { display: none !important; }

    /* ── Code blocks ── */
    [data-testid="stCode"] {
        background: var(--bg3) !important;
        border: 1px solid var(--border2) !important;
        border-radius: 14px !important;
        overflow: hidden;
    }
    [data-testid="stCode"] pre {
        background: transparent !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px !important; color: #e0e0e8 !important;
        line-height: 1.7 !important; padding: 20px !important;
    }
    [data-testid="stCode"] .copy-button-container { display: none; }

    /* ── Primary button ── */
    .stButton > button[kind="primaryFormSubmit"],
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%) !important;
        border: none !important; 
        color: white !important;
        font-weight: 600 !important; 
        padding: 12px 28px !important;
        box-shadow: 0 4px 20px var(--accent-glow) !important;
        letter-spacing: .01em !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .stButton > button[kind="primaryFormSubmit"]:hover,
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 8px 32px var(--accent-glow) !important;
        transform: translateY(-2px) !important;
    }

    /* ── Alert / info / warning / error ── */
    [data-testid="stAlert"] {
        border-radius: 14px !important;
        font-size: 14px !important;
        border: 1px solid var(--border2) !important;
    }
    .stAlert { background: var(--bg2) !important; }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border) !important;
        border-radius: 16px !important; 
        overflow: hidden;
    }
    [data-testid="stDataFrame"] th { 
        background: var(--surface) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
    }
    [data-testid="stDataFrame"] td {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* ── Time / Number inputs ── */
    [data-testid="stTimeInput"] input,
    [data-testid="stNumberInput"] input {
        background: var(--surface) !important;
        border: 1px solid var(--border2) !important;
        border-radius: 10px !important; color: var(--text) !important;
    }

    /* ── Checkbox ── */
    [data-testid="stCheckbox"] {
        background: var(--surface);
        border: 1px solid var(--border2);
        border-radius: 10px;
        padding: 8px 14px !important;
    }
    [data-testid="stCheckbox"] span { color: var(--text2) !important; font-size: 13px !important; }
    [data-testid="stCheckbox"] svg  { fill: var(--accent) !important; }

    /* ── Step header component ── */
    .step-header {
        display: flex; align-items: center; gap: 12px;
        margin: 24px 0 14px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border);
    }
    .step-num {
        width: 28px; height: 28px; flex-shrink: 0;
        background: linear-gradient(135deg, var(--accent) 0%, #7c3aed 100%);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Syne', sans-serif;
        font-size: 12px; font-weight: 700; color: white;
        box-shadow: 0 2px 8px rgba(91,141,239,.35);
    }
    .step-title {
        font-family: 'Syne', sans-serif;
        font-size: 15px; font-weight: 700; color: var(--text);
    }
    .step-sub {
        font-size: 12px; color: var(--text3); margin-top: 1px;
    }

    /* ── Form section box ── */
    .form-section {
        background: var(--bg2);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
    .form-section-label {
        font-family: 'DM Mono', monospace;
        font-size: 9px; color: var(--text3);
        text-transform: uppercase; letter-spacing: .14em;
        margin-bottom: 12px;
    }

    /* ── Template output box ── */
    .tpl-box {
        background: var(--bg3);
        border: 1px solid var(--border2);
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 14px;
    }
    .tpl-box-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 10px 16px;
        border-bottom: 1px solid var(--border);
    }
    .tpl-box-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 12px; font-weight: 600; color: var(--text);
    }
    .tpl-badge-ab   { background: rgba(248,113,113,.15); color: #f87171; font-size:10px; padding:2px 8px; border-radius:20px; font-family:'DM Mono',monospace; }
    .tpl-badge-atu  { background: rgba(251,191,36,.15);  color: #fbbf24; font-size:10px; padding:2px 8px; border-radius:20px; font-family:'DM Mono',monospace; }
    .tpl-badge-norm { background: rgba(52,211,153,.15);  color: #34d399; font-size:10px; padding:2px 8px; border-radius:20px; font-family:'DM Mono',monospace; }

    /* ── History record left-border by type ── */
    .rec-aexec   [data-testid="stVerticalBlockBorderWrapper"] { border-left: 3px solid #f87171 !important; }
    .rec-gcrises [data-testid="stVerticalBlockBorderWrapper"] { border-left: 3px solid #fbbf24 !important; }
    .rec-isolada [data-testid="stVerticalBlockBorderWrapper"] { border-left: 3px solid #a78bfa !important; }

    /* ── Glossary grid ── */
    .gloss-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 10px; margin-top: 12px;
    }
    .gloss-item {
        background: var(--bg2);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 12px 14px;
    }
    .gloss-term {
        font-family: 'DM Mono', monospace;
        font-size: 12px; font-weight: 600; color: var(--accent);
        margin-bottom: 4px;
    }
    .gloss-def {
        font-size: 12px; color: var(--text2); line-height: 1.4;
    }

    /* ── Contact card ── */
    .contact-pill {
        display: flex; align-items: center; gap: 14px;
        background: var(--bg2); border: 1px solid var(--border);
        border-radius: 12px; padding: 14px 16px; margin-bottom: 8px;
        text-decoration: none !important;
        transition: border-color .15s, background .15s;
    }
    .contact-pill:hover { border-color: rgba(91,141,239,.3) !important; background: var(--surface) !important; }
    .contact-pill-icon { font-size: 22px; flex-shrink: 0; }
    .contact-pill-name { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: var(--text); }
    .contact-pill-tel  { font-family: 'DM Mono', monospace; font-size: 12px; color: var(--text3); margin-top: 2px; }

    /* ── Portal link card ── */
    .portal-card {
        background: var(--bg2); border: 1px solid var(--border);
        border-radius: 12px; padding: 16px;
    }
    .portal-card a { color: var(--accent) !important; text-decoration: none !important; font-weight: 600; }
    .portal-card a:hover { text-decoration: underline !important; }

    /* ── Footer ── */
    .footer { text-align: center; color: var(--text3); font-size: 12px; padding: 24px; border-top: 1px solid var(--border); margin-top: 48px; }

    /* ── Page header ── */
    .page-header {
        display: flex; align-items: center; gap: 16px;
        margin-bottom: 32px;
        padding: 24px;
        background: linear-gradient(135deg, var(--bg2) 0%, var(--bg3) 100%);
        border: 1px solid var(--border);
        border-radius: 20px;
    }
    .page-header-icon {
        width: 56px; height: 56px; flex-shrink: 0;
        background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px;
        box-shadow: 0 4px 20px var(--accent-glow);
    }
    .page-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 26px !important; font-weight: 700 !important;
        color: var(--text) !important; margin: 0 !important; line-height: 1.2;
        letter-spacing: -0.02em;
    }
    .page-sub {
        font-size: 14px !important; color: var(--text2) !important;
        margin: 6px 0 0 0 !important;
    }

    /* ── Card containers (st.container border=True) ── */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--bg2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        margin-bottom: 12px !important;
        transition: all 0.25s ease !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: var(--accent) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px var(--accent-glow) !important;
        transform: translateY(-2px);
    }

    /* ── Card elements ── */
    .card-header {
        display: flex; align-items: center; gap: 12px;
        flex-wrap: wrap; padding: 4px 0;
    }
    .card-vd {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px; font-weight: 600;
        color: var(--accent-light);
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.3);
        padding: 4px 12px; border-radius: 8px;
        flex-shrink: 0;
    }
    .card-nome {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 17px; font-weight: 600; color: var(--text);
        letter-spacing: -0.01em;
    }
    .card-bandeira {
        font-size: 11px; color: var(--text3);
        background: var(--surface);
        padding: 4px 10px; border-radius: 6px;
        font-weight: 500;
    }
    .card-meta {
        font-size: 13px; color: var(--text2);
        margin: 6px 0 8px 0 !important;
        line-height: 1.6;
    }
    .card-row {
        display: flex; flex-wrap: wrap;
        align-items: center; gap: 8px;
        margin: 6px 0 8px 0;
    }

    /* ── Circuit chips ── */
    .chip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px; padding: 5px 12px;
        border-radius: 24px; white-space: nowrap;
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    .chip:hover { transform: scale(1.02); }
    .chip-green  { background: rgba(16,185,129,0.12); color: var(--green-light); border-color: rgba(16,185,129,0.25); }
    .chip-purple { background: rgba(168,85,247,0.12); color: var(--purple-light); border-color: rgba(168,85,247,0.25); }
    .chip-cyan   { background: rgba(6,182,212,0.1); color: var(--cyan); border-color: rgba(6,182,212,0.2); }

    /* ── Quick contacts ── */
    .quick-contact {
        font-size: 13px; padding: 6px 14px;
        border-radius: 24px; text-decoration: none !important;
        white-space: nowrap;
        transition: all 0.2s ease;
    }
    .quick-contact:hover { transform: scale(1.03); }
    .quick-contact.green  { color: var(--green-light); background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); }
    .quick-contact.accent { color: var(--accent-light); background: rgba(99,102,241,0.1);  border: 1px solid rgba(99,102,241,0.2); }
    .quick-contact.muted  { color: var(--text2); background: var(--surface); border: 1px solid var(--border); }

    /* ── Section / result labels ── */
    .section-label {
        font-family: 'DM Mono', monospace !important;
        font-size: 10px !important; color: #5c6370 !important;
        text-transform: uppercase; letter-spacing: .12em;
        margin: 16px 0 8px 0 !important;
    }
    .result-count {
        font-size: 13px; color: #5c6370;
        margin: 8px 0 12px 0 !important;
    }
    .result-count b { color: #eaecf0; }

    /* ── Radio como pills (modo de busca) ── */
    [data-testid="stRadio"] > div {
        display: flex; flex-wrap: wrap; gap: 8px !important;
        margin-top: 12px !important;
    }
    [data-testid="stRadio"] label {
        background: var(--surface) !important;
        border: 1px solid var(--border2) !important;
        border-radius: 24px !important;
        padding: 8px 18px !important;
        font-size: 13px !important; font-weight: 500 !important;
        color: var(--text2) !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    [data-testid="stRadio"] label:hover {
        border-color: var(--accent) !important;
        color: var(--text) !important;
        background: var(--surface2) !important;
    }
    [data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(99,102,241,0.2) 0%, rgba(168,85,247,0.15) 100%) !important;
        border-color: var(--accent) !important;
        color: var(--accent-light) !important;
        font-weight: 600 !important;
        box-shadow: 0 0 16px var(--accent-glow) !important;
    }
    [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        display: none !important;
    }
    [data-testid="stRadio"] > div > div:first-child {
        display: none !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
    }
    [data-testid="stExpander"] summary {
        font-size: 14px !important;
        color: var(--text2) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 12px 16px !important;
    }
    [data-testid="stExpander"][open] summary {
        border-bottom: 1px solid var(--border);
    }
"""


def get_responsive_css() -> str:
    """CSS responsivo para diferentes tamanhos de tela - v4.0"""
    return """
    @media (max-width: 768px) {
        .stApp { padding: 0 !important; }
        .stColumn { padding: 6px !important; }
        .card { padding: 20px !important; margin-bottom: 16px !important; }
        .info-grid { grid-template-columns: 1fr !important; }
        .sidebar-logo { padding: 16px !important; }
        h1 { font-size: 26px !important; }
        h2 { font-size: 20px !important; }
        .stColumns { flex-direction: column !important; }
        [data-testid="stMetric"] { padding: 16px !important; }
        [data-testid="stMetricValue"] { font-size: 24px !important; }
        .template-box { padding: 20px !important; }
        .page-header { padding: 16px !important; flex-direction: column; align-items: flex-start; }
        .page-header-icon { width: 48px !important; height: 48px !important; }
        .page-title { font-size: 22px !important; }
    }
    
    @media (max-width: 480px) {
        .sidebar-logo-icon { width: 36px !important; height: 36px !important; }
        .sidebar-logo-text { font-size: 16px !important; }
        .kpi-card { padding: 16px !important; }
        .kpi-value { font-size: 28px !important; }
        .sb-kpi-value { font-size: 22px !important; }
    }
"""


def get_animations_css() -> str:
    """CSS para animações e transições - v4.0"""
    return """
    .card { 
        background: var(--bg2); 
        border: 1px solid var(--border); 
        border-radius: 20px; 
        padding: 24px; 
        margin-bottom: 20px; 
        transition: all 0.3s ease;
    }
    .card:hover { 
        border-color: var(--accent); 
        transform: translateY(-4px); 
        box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 30px var(--accent-glow); 
    }
    
    .status-indicator { 
        display: flex; align-items: center; gap: 10px; 
        padding: 12px 20px; 
        background: rgba(16,185,129,0.1); 
        border-radius: 14px; 
        border: 1px solid rgba(16,185,129,0.2); 
    }
    .status-dot { 
        width: 10px; height: 10px; 
        background: var(--green); 
        border-radius: 50%; 
        animation: pulse 2s infinite; 
        box-shadow: 0 0 10px var(--green);
    }
    
    @keyframes pulse { 
        0%, 100% { opacity: 1; transform: scale(1); } 
        50% { opacity: 0.5; transform: scale(0.95); } 
    }
    
    .skeleton { 
        background: linear-gradient(90deg, var(--surface) 25%, var(--surface2) 50%, var(--surface) 75%); 
        background-size: 200% 100%; 
        animation: shimmer 1.5s infinite; 
        border-radius: 12px; 
    }
    @keyframes shimmer { 
        0% { background-position: 200% 0; } 
        100% { background-position: -200% 0; } 
    }
    .skeleton-card { height: 200px; margin-bottom: 16px; }
    .skeleton-text { height: 20px; margin-bottom: 8px; }
    .skeleton-text-short { height: 20px; width: 60%; }
    
    .fade-in { animation: fadeIn 0.4s ease-out; }
    @keyframes fadeIn { 
        from { opacity: 0; transform: translateY(10px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    
    .slide-up { animation: slideUp 0.3s ease-out; }
    @keyframes slideUp { 
        from { transform: translateY(20px); opacity: 0; } 
        to { transform: translateY(0); opacity: 1; } 
    }

    /* Glow effects */
    .glow-accent {
        box-shadow: 0 0 20px var(--accent-glow), 0 4px 16px rgba(0,0,0,0.3);
    }
    .glow-green {
        box-shadow: 0 0 20px rgba(16,185,129,0.3), 0 4px 16px rgba(0,0,0,0.3);
    }
    
    /* Gradient borders */
    .gradient-border {
        position: relative;
        background: var(--bg2);
        border-radius: 18px;
    }
    .gradient-border::before {
        content: '';
        position: absolute;
        inset: 0;
        padding: 1px;
        border-radius: 18px;
        background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }
"""


def get_component_css() -> str:
    """CSS específico para componentes de UI - v4.0"""
    return """
    .vd-badge { 
        background: rgba(99,102,241,0.2); 
        color: var(--accent-light); 
        padding: 8px 16px; 
        border-radius: 10px; 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 14px; 
        font-weight: 600;
    }
    
    .status-open { 
        background: rgba(16,185,129,0.15); 
        color: var(--green-light); 
        padding: 6px 16px; 
        border-radius: 24px; 
        font-size: 12px;
        font-weight: 500;
    }
    .status-closed { 
        background: rgba(239,68,68,0.15); 
        color: var(--red-light); 
        padding: 6px 16px; 
        border-radius: 24px; 
        font-size: 12px;
        font-weight: 500;
    }
    .status-pending { 
        background: rgba(245,158,11,0.15); 
        color: var(--amber-light); 
        padding: 6px 16px; 
        border-radius: 24px; 
        font-size: 12px;
        font-weight: 500;
    }
    
    .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
    @media (max-width: 768px) { .info-grid { grid-template-columns: 1fr; } }
    
    .info-section { 
        background: var(--surface); 
        border-radius: 16px; 
        padding: 20px; 
        border: 1px solid var(--border); 
    }
    .info-section h4 { 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 11px; 
        color: var(--text3); 
        text-transform: uppercase; 
        letter-spacing: 0.15em; 
        margin-bottom: 16px; 
    }
    .info-row { font-size: 14px; color: var(--text2); margin-bottom: 10px; }
    .info-row a { color: var(--accent-light); text-decoration: none; }
    .info-row a:hover { text-decoration: underline; }
    
    .desig-pill { 
        display: inline-flex; 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 12px; 
        padding: 6px 14px; 
        border-radius: 8px; 
        margin: 4px 8px 4px 0; 
    }
    .desig-mpls { 
        background: rgba(16,185,129,0.12); 
        color: var(--green-light); 
        border: 1px solid rgba(16,185,129,0.25); 
    }
    .desig-inn { 
        background: rgba(99,102,241,0.12); 
        color: var(--accent-light); 
        border: 1px solid rgba(99,102,241,0.25); 
    }
    
    .template-box { 
        background: var(--bg3); 
        border: 1px solid var(--border); 
        border-radius: 20px; 
        padding: 24px; 
        margin-bottom: 20px; 
    }
    .template-header { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        margin-bottom: 20px; 
        padding-bottom: 16px; 
        border-bottom: 1px solid var(--border); 
    }
    .template-type { 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 12px; 
        padding: 6px 14px; 
        border-radius: 8px; 
    }
    .template-abertura { 
        background: rgba(239,68,68,0.15); 
        color: var(--red-light); 
    }
    .template-atualizacao { 
        background: rgba(245,158,11,0.15); 
        color: var(--amber-light); 
    }
    .template-normalizacao { 
        background: rgba(16,185,129,0.15); 
        color: var(--green-light); 
    }
    .template-content { 
        background: var(--surface); 
        border-radius: 14px; 
        padding: 24px; 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 13px; 
        line-height: 1.8; 
        white-space: pre-wrap; 
    }
    
    .suggestions-box { 
        background: var(--surface); 
        border: 1px solid var(--border2); 
        border-radius: 16px; 
        max-height: 240px; 
        overflow-y: auto; 
        margin-top: 8px; 
    }
    .suggestion-item { 
        padding: 14px 20px; 
        cursor: pointer; 
        border-bottom: 1px solid var(--border); 
        transition: background 0.2s; 
    }
    .suggestion-item:hover { background: var(--surface2); }
    .suggestion-item:last-child { border-bottom: none; }
    .suggestion-vd { 
        font-family: 'JetBrains Mono', monospace; 
        color: var(--accent-light); 
        font-size: 13px; 
    }
    .suggestion-nome { color: var(--text); font-size: 15px; font-weight: 500; }
    .suggestion-endereco { color: var(--text3); font-size: 13px; }
    
    .kpi-card { 
        background: var(--bg2); 
        border: 1px solid var(--border); 
        border-radius: 20px; 
        padding: 24px; 
        text-align: center; 
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        border-color: var(--accent);
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.4);
    }
    .kpi-value { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        font-size: 40px; 
        font-weight: 700; 
    }
    .kpi-label { 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 12px; 
        color: var(--text3); 
        text-transform: uppercase; 
        margin-top: 12px; 
        letter-spacing: 0.1em;
    }
    
    .sidebar-logo { 
        display: flex; 
        align-items: center; 
        gap: 14px; 
        padding: 24px 20px; 
        background: linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(168,85,247,0.08) 100%);
    }
    .sidebar-logo-icon { 
        width: 48px; height: 48px; 
        background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%); 
        border-radius: 14px; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
    }
    .sidebar-logo-text { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        font-weight: 700; 
        font-size: 18px; 
    }
    .sidebar-logo-sub { 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 11px; 
        color: var(--text3); 
    }
    
    .contact-card { 
        background: var(--surface); 
        border-radius: 16px; 
        padding: 20px; 
        border: 1px solid var(--border); 
    }
    .contact-item { 
        display: flex; 
        align-items: center; 
        gap: 12px; 
        font-size: 14px; 
        color: var(--text2); 
    }
    
    .toast-success { 
        background: rgba(16,185,129,0.15); 
        border: 1px solid rgba(16,185,129,0.3); 
        color: var(--green-light); 
        padding: 14px 24px; 
        border-radius: 14px; 
        margin: 10px 0; 
    }
    .toast-error { 
        background: rgba(239,68,68,0.15); 
        border: 1px solid rgba(239,68,68,0.3); 
        color: var(--red-light); 
        padding: 14px 24px; 
        border-radius: 14px; 
        margin: 10px 0; 
    }
    .toast-info { 
        background: rgba(99,102,241,0.15); 
        border: 1px solid rgba(99,102,241,0.3); 
        color: var(--accent-light); 
        padding: 14px 24px; 
        border-radius: 14px; 
        margin: 10px 0; 
    }
    
    .alert-banner { 
        background: rgba(239,68,68,0.1); 
        border: 1px solid rgba(239,68,68,0.3); 
        border-radius: 16px; 
        padding: 20px; 
        margin-bottom: 20px; 
    }
    .alert-banner h4 { color: var(--red-light); margin: 0 0 10px 0; }
    .alert-banner p { color: var(--text2); font-size: 14px; margin: 0; }
    
    .faq-item { 
        background: var(--surface); 
        border: 1px solid var(--border); 
        border-radius: 16px; 
        padding: 20px; 
        margin-bottom: 16px; 
    }
    .faq-question { font-weight: 600; color: var(--text); margin-bottom: 10px; font-size: 15px; }
    .faq-answer { color: var(--text2); font-size: 14px; line-height: 1.6; }
    
    /* Step component */
    .step-header {
        display: flex; align-items: center; gap: 16px;
        margin: 28px 0 18px 0;
        padding-bottom: 14px;
        border-bottom: 1px solid var(--border);
    }
    .step-num {
        width: 36px; height: 36px; flex-shrink: 0;
        background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 14px; font-weight: 700; color: white;
        box-shadow: 0 4px 16px var(--accent-glow);
    }
    .step-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 18px; font-weight: 600; color: var(--text);
    }
    .step-sub {
        font-size: 13px; color: var(--text3); margin-top: 3px;
    }

    /* Portal card */
    .portal-card {
        background: var(--bg2); 
        border: 1px solid var(--border);
        border-radius: 16px; 
        padding: 20px;
        transition: all 0.2s ease;
    }
    .portal-card:hover {
        border-color: var(--accent);
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .portal-card a { 
        color: var(--accent-light) !important; 
        text-decoration: none !important; 
        font-weight: 600; 
    }
    .portal-card a:hover { text-decoration: underline !important; }
    
    /* Footer */
    .footer { 
        text-align: center; 
        color: var(--text3); 
        font-size: 12px; 
        padding: 32px; 
        border-top: 1px solid var(--border); 
        margin-top: 64px; 
        background: linear-gradient(180deg, transparent 0%, var(--bg2) 100%);
    }
    .footer-logo {
        font-size: 24px;
        margin-bottom: 8px;
    }
    .footer-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        font-weight: 600;
        color: var(--text2);
        margin-bottom: 4px;
    }
    .footer-version {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: var(--accent-light);
        background: rgba(99,102,241,0.15);
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 12px;
    }
    .footer-dev {
        font-size: 12px;
        color: var(--text3);
        margin-bottom: 8px;
    }
    .footer-copy {
        font-size: 10px;
        color: var(--text3);
        opacity: 0.7;
    }

    /* ── Error Page ── */
    .error-page {
        text-align: center;
        padding: 60px 40px;
        background: var(--bg2);
        border: 1px solid var(--border);
        border-radius: 24px;
        margin: 40px 0;
    }
    .error-icon {
        font-size: 64px;
        margin-bottom: 20px;
    }
    .error-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 24px;
        color: var(--text);
        margin-bottom: 12px;
    }
    .error-message {
        color: var(--text2);
        font-size: 15px;
        margin-bottom: 8px;
    }
    .error-suggestion {
        color: var(--text3);
        font-size: 13px;
        margin-bottom: 24px;
    }
    .error-button {
        background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .error-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px var(--accent-glow);
    }

    /* ── Empty State ── */
    .empty-state {
        text-align: center;
        padding: 48px 32px;
        background: var(--bg2);
        border: 1px solid var(--border);
        border-radius: 20px;
        margin: 24px 0;
    }
    .empty-icon {
        font-size: 48px;
        margin-bottom: 16px;
        opacity: 0.7;
    }
    .empty-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 18px;
        color: var(--text);
        margin-bottom: 8px;
    }
    .empty-message {
        color: var(--text2);
        font-size: 14px;
    }

    /* ── Error Banner ── */
    .error-banner {
        padding: 16px 20px;
        border-radius: 12px;
        margin: 16px 0;
        font-size: 14px;
        color: var(--text);
    }

    /* ── Loading Animation ── */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px;
    }
    .loading-spinner {
        width: 48px;
        height: 48px;
        border: 3px solid var(--surface);
        border-top-color: var(--accent);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    .loading-text {
        margin-top: 16px;
        color: var(--text2);
        font-size: 14px;
    }

    /* ── Skeleton Loading ── */
    .skeleton {
        background: linear-gradient(90deg, var(--surface) 25%, var(--surface2) 50%, var(--surface) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: 8px;
    }
    .skeleton-card {
        height: 180px;
        margin-bottom: 16px;
        border-radius: 16px;
    }
    .skeleton-text {
        height: 16px;
        margin-bottom: 8px;
    }
    .skeleton-text-short {
        height: 16px;
        width: 60%;
    }
"""


def get_full_css() -> str:
    """Retorna todo o CSS combinado"""
    return get_base_css() + get_responsive_css() + get_animations_css() + get_component_css()


def render_styles():
    """Renderiza o CSS completo no Streamlit"""
    import streamlit as st
    st.markdown(f"<style>{get_full_css()}</style>", unsafe_allow_html=True)


# Constantes de design system
class Colors:
    """Cores do design system v4.0"""
    BG_PRIMARY = "#0a0a0f"
    BG_SECONDARY = "#12121a"
    BG_TERTIARY = "#1a1a24"
    SURFACE = "#222230"
    SURFACE2 = "#2a2a3a"
    TEXT_PRIMARY = "#f0f0f5"
    TEXT_SECONDARY = "#a0a0b0"
    TEXT_TERTIARY = "#606070"
    ACCENT = "#6366f1"
    ACCENT_LIGHT = "#818cf8"
    ACCENT_HOVER = "#5558e3"
    ACCENT_GLOW = "rgba(99,102,241,0.25)"
    SUCCESS = "#10b981"
    SUCCESS_LIGHT = "#34d399"
    ERROR = "#ef4444"
    ERROR_LIGHT = "#f87171"
    WARNING = "#f59e0b"
    WARNING_LIGHT = "#fbbf24"
    INFO = "#06b6d4"
    PURPLE = "#a855f7"
    PURPLE_LIGHT = "#c084fc"
    BLUE = "#3b82f6"


class Fonts:
    """Fontes do design system"""
    HEADING = "Plus Jakarta Sans, sans-serif"
    BODY = "Plus Jakarta Sans, sans-serif"
    MONO = "JetBrains Mono, monospace"


class Spacing:
    """Espaçamentos do design system"""
    XS = "4px"
    SM = "8px"
    MD = "16px"
    LG = "24px"
    XL = "32px"
    XXL = "48px"


class BorderRadius:
    """Border radius do design system"""
    SM = "8px"
    MD = "12px"
    LG = "16px"
    XL = "20px"
    ROUND = "24px"