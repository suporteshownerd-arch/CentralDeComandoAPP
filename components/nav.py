"""
Sidebar - Apenas para direcionar
"""

import streamlit as st


def render_sidebar(lojas, favoritos):
    # CSS global para o sidebar
    st.markdown("""
    <style>
        /* Wrapper principal */
        .sidebar-content {
            padding: 12px;
        }
        
        /* Logo */
        .sidebar-logo {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 24px 16px;
            text-align: center;
            margin-bottom: 16px;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        }
        .logo-icon {
            font-size: 36px;
            margin-bottom: 8px;
            display: block;
        }
        .logo-title {
            font-size: 16px;
            font-weight: 700;
            color: white;
            letter-spacing: 0.5px;
            display: block;
            margin-bottom: 4px;
        }
        .logo-subtitle {
            font-size: 10px;
            color: rgba(255,255,255,0.7);
            font-family: monospace;
            letter-spacing: 1px;
            display: block;
        }
        
        /* Status */
        .status-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.2);
            border-radius: 24px;
            padding: 10px 16px;
            margin-bottom: 20px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
            box-shadow: 0 0 8px #22c55e;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(0.9); }
        }
        .status-text {
            font-size: 11px;
            font-weight: 600;
            color: #22c55e;
            letter-spacing: 0.5px;
        }
        
        /* Menu */
        .menu-label {
            font-size: 11px;
            font-weight: 600;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
            padding-left: 4px;
        }
        
        /* Item ativo */
        .nav-active {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.15) 100%);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 6px;
            color: #818cf8 !important;
            font-weight: 600;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Usuário */
        .user-container {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            margin-top: 16px;
        }
        .user-avatar {
            width: 56px;
            height: 56px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px;
            font-size: 28px;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        }
        .user-name {
            font-size: 14px;
            font-weight: 600;
            color: white;
            margin-bottom: 4px;
        }
        .user-role {
            font-size: 12px;
            color: #888;
        }
        .version {
            font-size: 10px;
            color: #555;
            text-align: center;
            margin-top: 16px;
            font-family: monospace;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Logo
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">🛡️</span>
        <span class="logo-title">CENTRAL DE COMANDO</span>
        <span class="logo-subtitle">DPSP • T.I. v5.0</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Status
    st.markdown("""
    <div class="status-container">
        <span class="status-dot"></span>
        <span class="status-text">SISTEMA OPERACIONAL</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="menu-label">Navegação</div>', unsafe_allow_html=True)
    
    # Menu de navegação
    menu_itens = [
        ("🏠", "Início", "🏠 Início"),
        ("📊", "Feed", "📊 Feed"),
        ("📈", "Dashboard", "📈 Dashboard"),
        ("🏪", "Busca de Lojas", "🏪 Buscar uma loja"),
        ("🚨", "Registro de Crises", "🚨 Registrar uma crise"),
        ("📞", "Abertura de Chamados", "📞 Abrir chamado na Vivo/Claro"),
        ("📋", "Histórico", "📋 Ver histórico de alertas"),
        ("❓", "Ajuda", "❓ Ajuda e manual"),
    ]
    
    current_page = st.session_state.get("nav_page", "🏠 Início")
    
    for icon, label, page_value in menu_itens:
        is_active = current_page == page_value
        full_label = f"{icon} {label}"
        
        if is_active:
            st.markdown(f'<div class="nav-active">{icon} {label}</div>', unsafe_allow_html=True)
        else:
            if st.button(full_label, key=f"nav_{page_value}", use_container_width=True):
                st.session_state.nav_page = page_value
                st.rerun()
    
    # Footer usuário
    st.markdown("""
    <div class="user-container">
        <div class="user-avatar">👤</div>
        <div class="user-name">Enzo Maranho</div>
        <div class="user-role">Analista T.I.</div>
    </div>
    <div class="version">Jarvis v5.0 • T.I. DPSP</div>
    """, unsafe_allow_html=True)


def render_footer():
    st.caption("Central de Comando DPSP - v5.0")


def init_session_state():
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "🏠 Início"


def setup_page_config():
    st.set_page_config(
        page_title="Central de Comando",
        page_icon="🛡️",
        layout="wide",
    )


def render_page_header(title, subtitle=None, icon=None):
    if icon:
        title = f"{icon} {title}"
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")