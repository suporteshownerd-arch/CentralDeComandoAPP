"""
Sidebar - Apenas para direcionar
"""

import streamlit as st


def render_sidebar(lojas, favoritos):
    st.markdown("""
    <style>
        .sidebar-logo {
            background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
            border-radius: 12px; padding: 16px;
            text-align: center; margin-bottom: 12px;
            box-shadow: 0 4px 16px var(--accent-glow);
        }
        .logo-icon { font-size: 28px; margin-bottom: 6px; display: block; }
        .logo-title {
            font-size: 12px; font-weight: 700; color: white; letter-spacing: 0.5px;
            display: block; font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .logo-subtitle {
            font-size: 7px; color: rgba(255,255,255,0.7);
            font-family: 'JetBrains Mono', monospace; letter-spacing: 2px;
            display: block; margin-top: 3px;
        }
        
        .status-container {
            display: flex; align-items: center; justify-content: center; gap: 6px;
            background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 16px; padding: 6px 10px; margin-bottom: 12px;
        }
        .status-dot {
            width: 6px; height: 6px; background: var(--green-light); border-radius: 50%;
            animation: pulse 2s infinite; box-shadow: 0 0 6px var(--green);
        }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .status-text {
            font-size: 9px; font-weight: 600; color: var(--green-light); letter-spacing: 0.5px;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        .menu-label {
            font-size: 9px; font-weight: 600; color: var(--text3);
            text-transform: uppercase; letter-spacing: 1px;
            margin-bottom: 10px; text-align: center;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .user-container {
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 12px; padding: 14px; text-align: center; margin-top: 16px;
        }
        .user-avatar {
            width: 40px; height: 40px;
            background: linear-gradient(135deg, var(--accent) 0%, var(--purple) 100%);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            margin: 0 auto 10px; font-size: 20px;
            box-shadow: 0 4px 12px var(--accent-glow);
        }
        .user-name {
            font-size: 12px; font-weight: 600; color: var(--text);
            margin-bottom: 2px; font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .user-role {
            font-size: 10px; color: var(--text3);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .version {
            font-size: 8px; color: var(--text3); text-align: center;
            margin-top: 10px; font-family: 'JetBrains Mono', monospace;
            letter-spacing: 1px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">🛡️</span>
        <span class="logo-title">CENTRAL DE COMANDO</span>
        <span class="logo-subtitle">DPSP • T.I. v5.0</span>
    </div>
    <div class="status-container">
        <span class="status-dot"></span>
        <span class="status-text">SISTEMA OPERACIONAL</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="menu-label">Navegação</div>', unsafe_allow_html=True)
    
    menu_itens = [
        ("🏠 Início", "🏠 Início"),
        ("📊 Feed", "📊 Feed"),
        ("📈 Dashboard", "📈 Dashboard"),
        ("🏪 Busca de Lojas", "🏪 Buscar uma loja"),
        ("🚨 Registro de Crises", "🚨 Registrar uma crise"),
        ("📞 Abertura de Chamados", "📞 Abrir chamado na Vivo/Claro"),
        ("📋 Histórico", "📋 Ver histórico de alertas"),
        ("❓ Ajuda", "❓ Ajuda e manual"),
    ]
    
    current_page = st.session_state.get("nav_page", "🏠 Início")
    
    for label, page_value in menu_itens:
        is_active = current_page == page_value
        
        if st.button(label, key=f"nav_{page_value}", use_container_width=True):
            st.session_state.nav_page = page_value
            st.rerun()
    
    st.markdown("""
    <div class="user-container">
        <div class="user-avatar">👤</div>
        <div class="user-name">Joao Carlos</div>
        <div class="user-role">Analista T.I.</div>
    </div>
    <div class="version">JARVIS v5.0 • T.I. DPSP</div>
    """, unsafe_allow_html=True)


def render_footer():
    st.caption("Central de Comando DPSP - v5.0")


def init_session_state():
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "🏠 Início"


def setup_page_config():
    st.set_page_config(page_title="Central de Comando", page_icon="🛡️", layout="wide")


def render_page_header(title, subtitle=None, icon=None):
    if icon: title = f"{icon} {title}"
    st.markdown(f"## {title}")
    if subtitle: st.markdown(f"*{subtitle}*")