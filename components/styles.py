"""
Módulo de estilos e design system
Central de Comando DPSP v2.0
"""


def get_base_css() -> str:
    """CSS base com variáveis, fontes e reset"""
    return """
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --bg: #08090d;
        --bg2: #0f1118;
        --bg3: #161920;
        --surface: #1c2029;
        --surface2: #232a36;
        --border: rgba(255,255,255,0.07);
        --border2: rgba(255,255,255,0.14);
        --text: #eaecf0;
        --text2: #9094a6;
        --text3: #5c6370;
        --accent: #5b8def;
        --accent-hover: #4a7de0;
        --green: #34d399;
        --red: #f87171;
        --amber: #fbbf24;
        --purple: #a78bfa;
        --cyan: #22d3ee;
    }

    /* ── App background ── */
    .stApp { background: var(--bg) !important; }
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: var(--bg2) !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] > div { padding: 0 !important; }
    section[data-testid="stSidebar"] .block-container { padding: 0 !important; }

    /* ── Sidebar logo ── */
    .sb-logo {
        display: flex; align-items: center; gap: 12px;
        padding: 20px 16px 16px 16px;
    }
    .sb-logo-icon {
        width: 38px; height: 38px; flex-shrink: 0;
        background: linear-gradient(135deg,#5b8def 0%,#7c3aed 100%);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 18px;
    }
    .sb-logo-title {
        font-family: 'Syne', sans-serif !important;
        font-weight: 700; font-size: 14px; color: #eaecf0; line-height: 1.2;
    }
    .sb-logo-sub {
        font-family: 'DM Mono', monospace !important;
        font-size: 10px; color: #5c6370; letter-spacing: .06em; margin-top: 2px;
    }

    /* ── Sidebar status badge ── */
    .sb-status {
        display: flex; align-items: center; gap: 8px;
        margin: 0 12px 4px 12px;
        padding: 7px 12px;
        background: rgba(52,211,153,.08);
        border: 1px solid rgba(52,211,153,.2);
        border-radius: 8px;
    }
    .sb-status span {
        font-size: 11px !important; color: #34d399 !important; font-weight: 600;
        font-family: 'DM Sans', sans-serif !important;
    }
    .sb-status-dot {
        width: 7px; height: 7px; background: #34d399; border-radius: 50%;
        animation: sb-pulse 2s infinite; flex-shrink: 0;
    }
    @keyframes sb-pulse { 0%,100%{opacity:1} 50%{opacity:.4} }

    /* ── Dividers ── */
    .sb-divider {
        border-top: 1px solid rgba(255,255,255,.06);
        margin: 12px 0;
    }

    /* ── Section labels ── */
    .sb-section-label {
        font-family: 'DM Mono', monospace !important;
        font-size: 9px !important; color: #5c6370 !important;
        text-transform: uppercase; letter-spacing: .14em;
        padding: 0 16px; margin-bottom: 8px;
    }

    /* ── KPI row ── */
    .sb-kpi-row {
        display: flex; align-items: center;
        margin: 0 12px 10px 12px;
        background: var(--bg3);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 10px 0;
    }
    .sb-kpi { flex: 1; text-align: center; }
    .sb-kpi-value {
        font-family: 'Syne', sans-serif !important;
        font-size: 20px !important; font-weight: 700; line-height: 1;
    }
    .sb-kpi-value.accent { color: #5b8def; }
    .sb-kpi-value.green  { color: #34d399; }
    .sb-kpi-value.red    { color: #f87171; }
    .sb-kpi-label {
        font-family: 'DM Mono', monospace !important;
        font-size: 9px !important; color: #5c6370 !important;
        text-transform: uppercase; margin-top: 3px;
    }
    .sb-kpi-sep {
        width: 1px; height: 28px;
        background: rgba(255,255,255,.07); flex-shrink: 0;
    }

    /* ── Progress bar ── */
    .sb-bar-wrap {
        margin: 0 12px 4px 12px;
        height: 5px; border-radius: 4px;
        background: rgba(248,113,113,.2);
        overflow: hidden;
    }
    .sb-bar-fill {
        height: 100%; background: #34d399; border-radius: 4px;
        transition: width .5s ease;
    }
    .sb-bar-legend {
        display: flex; justify-content: space-between;
        padding: 0 12px;
        font-family: 'DM Mono', monospace !important;
        font-size: 10px !important;
    }
    .sb-bar-legend .green { color: #34d399; }
    .sb-bar-legend .red   { color: #f87171; }

    /* ── Favorites ── */
    .sb-fav-item {
        display: flex; align-items: center; gap: 8px;
        padding: 5px 12px;
        margin: 0 4px 2px 4px;
        border-radius: 7px;
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
        padding: 9px 12px;
        border-bottom: 1px solid rgba(255,255,255,.05);
    }
    .sb-contact-item:last-child { border-bottom: none; }
    .sb-contact-name {
        font-size: 12px !important; color: #eaecf0 !important;
        font-weight: 600; line-height: 1.2;
    }
    .sb-contact-tel {
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important; color: #5c6370;
    }

    /* ── Radio nav (inside sidebar) ── */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        font-size: 13px !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        margin-bottom: 2px !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] > div {
        background: transparent !important;
        border: none !important;
        gap: 2px !important;
        padding: 0 8px !important;
    }

    /* ── Headings ── */
    h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; font-size: 30px !important; letter-spacing: -.03em; color: var(--text) !important; }
    h2, h3 { font-family: 'Syne', sans-serif !important; color: var(--text) !important; }

    /* ── Metrics ── */
    [data-testid="stMetric"] { background: var(--bg2) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 16px !important; }
    [data-testid="stMetricLabel"] { color: var(--text3) !important; font-family: 'DM Mono', monospace !important; font-size: 10px !important; text-transform: uppercase; }
    [data-testid="stMetricValue"] { color: var(--text) !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; font-size: 26px !important; }

    /* ── Inputs ── */
    .stTextInput > div > div > input { background: var(--surface) !important; border: 1px solid var(--border2) !important; border-radius: 10px !important; color: var(--text) !important; }
    .stTextInput > div > div > input:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(91,141,239,.15) !important; }
    .stSelectbox > div > div > div { background: var(--surface) !important; border: 1px solid var(--border2) !important; border-radius: 10px !important; }
    .stTextArea > div > div > textarea { background: var(--surface) !important; border: 1px solid var(--border2) !important; border-radius: 10px !important; color: var(--text) !important; }

    /* ── Buttons ── */
    .stButton > button { border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; transition: all .18s !important; border: 1px solid var(--border2) !important; }
    .stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 16px rgba(0,0,0,.3) !important; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; background: var(--surface); padding: 6px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { background: transparent; border-radius: 7px; padding: 10px 18px; font-weight: 500; }
    .stTabs [aria-selected="true"] { background: var(--accent) !important; color: white !important; }

    /* ── Footer ── */
    .footer { text-align: center; color: var(--text3); font-size: 12px; padding: 24px; border-top: 1px solid var(--border); margin-top: 48px; }
"""


def get_responsive_css() -> str:
    """CSS responsivo para diferentes tamanhos de tela"""
    return """
    @media (max-width: 768px) {
        .stApp { padding: 0 !important; }
        .stColumn { padding: 4px !important; }
        .card { padding: 16px !important; margin-bottom: 12px !important; }
        .info-grid { grid-template-columns: 1fr !important; }
        .sidebar-logo { padding: 12px !important; }
        h1 { font-size: 24px !important; }
        h2 { font-size: 20px !important; }
        .stColumns { flex-direction: column !important; }
        [data-testid="stMetric"] { padding: 12px !important; }
        .template-box { padding: 16px !important; }
    }
    
    @media (max-width: 480px) {
        .sidebar-logo-icon { width: 32px !important; height: 32px !important; }
        .sidebar-logo-text { font-size: 14px !important; }
        .kpi-card { padding: 12px !important; }
        .kpi-value { font-size: 24px !important; }
    }
"""


def get_animations_css() -> str:
    """CSS para animações e transições"""
    return """
    .card { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 24px; margin-bottom: 20px; transition: all 0.3s; }
    .card:hover { border-color: var(--border2); transform: translateY(-4px); box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
    
    .status-indicator { display: flex; align-items: center; gap: 8px; padding: 10px 16px; background: rgba(52,211,153,0.1); border-radius: 10px; border: 1px solid rgba(52,211,153,0.2); }
    .status-dot { width: 8px; height: 8px; background: var(--green); border-radius: 50%; animation: pulse 2s infinite; }
    
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    
    .skeleton { background: linear-gradient(90deg, var(--surface) 25%, var(--surface2) 50%, var(--surface) 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 8px; }
    @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
    .skeleton-card { height: 200px; margin-bottom: 16px; }
    .skeleton-text { height: 20px; margin-bottom: 8px; }
    .skeleton-text-short { height: 20px; width: 60%; }
    
    .fade-in { animation: fadeIn 0.3s ease-in; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    
    .slide-up { animation: slideUp 0.3s ease-out; }
    @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
"""


def get_component_css() -> str:
    """CSS específico para componentes de UI"""
    return """
    .vd-badge { background: rgba(91,141,239,0.2); color: var(--accent); padding: 6px 12px; border-radius: 8px; font-family: 'DM Mono', monospace; font-size: 13px; }
    
    .status-open { background: rgba(52,211,153,0.15); color: var(--green); padding: 6px 14px; border-radius: 20px; font-size: 12px; }
    .status-closed { background: rgba(248,113,113,0.15); color: var(--red); padding: 6px 14px; border-radius: 20px; font-size: 12px; }
    
    .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    @media (max-width: 768px) { .info-grid { grid-template-columns: 1fr; } }
    
    .info-section { background: var(--surface); border-radius: 12px; padding: 16px; border: 1px solid var(--border); }
    .info-section h4 { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--text3); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 12px; }
    .info-row { font-size: 13px; color: var(--text2); margin-bottom: 8px; }
    .info-row a { color: var(--accent); text-decoration: none; }
    
    .desig-pill { display: inline-flex; font-family: 'DM Mono', monospace; font-size: 11px; padding: 4px 10px; border-radius: 6px; margin: 2px 6px 2px 0; }
    .desig-mpls { background: rgba(52,211,153,0.12); color: var(--green); border: 1px solid rgba(52,211,153,0.25); }
    .desig-inn { background: rgba(91,141,239,0.12); color: var(--accent); border: 1px solid rgba(91,141,239,0.25); }
    
    .template-box { background: var(--bg3); border: 1px solid var(--border); border-radius: 16px; padding: 24px; margin-bottom: 20px; }
    .template-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
    .template-type { font-family: 'DM Mono', monospace; font-size: 11px; padding: 4px 12px; border-radius: 6px; }
    .template-abertura { background: rgba(248,113,113,0.15); color: var(--red); }
    .template-atualizacao { background: rgba(251,191,36,0.15); color: var(--amber); }
    .template-normalizacao { background: rgba(52,211,153,0.15); color: var(--green); }
    .template-content { background: var(--surface); border-radius: 12px; padding: 20px; font-family: 'DM Mono', monospace; font-size: 13px; line-height: 1.8; white-space: pre-wrap; }
    
    .suggestions-box { background: var(--surface); border: 1px solid var(--border2); border-radius: 12px; max-height: 200px; overflow-y: auto; margin-top: 4px; }
    .suggestion-item { padding: 10px 16px; cursor: pointer; border-bottom: 1px solid var(--border); transition: background 0.15s; }
    .suggestion-item:hover { background: var(--surface2); }
    .suggestion-item:last-child { border-bottom: none; }
    .suggestion-vd { font-family: 'DM Mono', monospace; color: var(--accent); font-size: 12px; }
    .suggestion-nome { color: var(--text); font-size: 14px; }
    .suggestion-endereco { color: var(--text3); font-size: 12px; }
    
    .kpi-card { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 20px; text-align: center; }
    .kpi-value { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 700; }
    .kpi-label { font-family: 'DM Mono', monospace; font-size: 11px; color: var(--text3); text-transform: uppercase; margin-top: 8px; }
    
    .sidebar-logo { display: flex; align-items: center; gap: 12px; padding: 20px 16px; }
    .sidebar-logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--accent) 0%, #7c3aed 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; }
    .sidebar-logo-text { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 16px; }
    .sidebar-logo-sub { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--text3); }
    
    .contact-card { background: var(--surface); border-radius: 12px; padding: 16px; border: 1px solid var(--border); }
    .contact-item { display: flex; align-items: center; gap: 10px; font-size: 13px; color: var(--text2); }
    
    .toast-success { background: rgba(52,211,153,0.15); border: 1px solid rgba(52,211,153,0.3); color: var(--green); padding: 12px 20px; border-radius: 10px; margin: 8px 0; }
    .toast-error { background: rgba(248,113,113,0.15); border: 1px solid rgba(248,113,113,0.3); color: var(--red); padding: 12px 20px; border-radius: 10px; margin: 8px 0; }
    .toast-info { background: rgba(91,141,239,0.15); border: 1px solid rgba(91,141,239,0.3); color: var(--accent); padding: 12px 20px; border-radius: 10px; margin: 8px 0; }
    
    .alert-banner { background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.3); border-radius: 12px; padding: 16px; margin-bottom: 20px; }
    .alert-banner h4 { color: var(--red); margin: 0 0 8px 0; }
    .alert-banner p { color: var(--text2); font-size: 13px; margin: 0; }
    
    .faq-item { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin-bottom: 12px; }
    .faq-question { font-weight: 600; color: var(--text); margin-bottom: 8px; }
    .faq-answer { color: var(--text2); font-size: 13px; }
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
    """Cores do design system"""
    BG_PRIMARY = "#08090d"
    BG_SECONDARY = "#0f1118"
    BG_TERTIARY = "#161920"
    SURFACE = "#1c2029"
    SURFACE2 = "#232a36"
    TEXT_PRIMARY = "#eaecf0"
    TEXT_SECONDARY = "#9094a6"
    TEXT_TERTIARY = "#5c6370"
    ACCENT = "#5b8def"
    ACCENT_HOVER = "#4a7de0"
    SUCCESS = "#34d399"
    ERROR = "#f87171"
    WARNING = "#fbbf24"
    INFO = "#22d3ee"
    PURPLE = "#a78bfa"


class Fonts:
    """Fontes do design system"""
    HEADING = "Syne, sans-serif"
    BODY = "DM Sans, sans-serif"
    MONO = "DM Mono, monospace"


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
    SM = "6px"
    MD = "8px"
    LG = "12px"
    XL = "16px"
    ROUND = "20px"