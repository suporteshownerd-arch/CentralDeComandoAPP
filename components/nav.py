"""
Sidebar - Apenas para direcionar
"""

import streamlit as st


def render_sidebar(lojas, favoritos):
    # CSS global para o sidebar
    st.markdown("""
    <style>
        /* Logo */
        .sidebar-logo {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 28px 16px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.35);
        }
        .logo-icon {
            font-size: 40px;
            margin-bottom: 10px;
            display: block;
        }
        .logo-title {
            font-size: 15px;
            font-weight: 700;
            color: white;
            letter-spacing: 1px;
            display: block;
            margin-bottom: 4px;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        .logo-subtitle {
            font-size: 9px;
            color: rgba(255,255,255,0.75);
            font-family: 'Consolas', 'Monaco', monospace;
            letter-spacing: 2px;
            display: block;
        }
        
        /* Status */
        .status-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.25);
            border-radius: 24px;
            padding: 10px 16px;
            margin-bottom: 24px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
            box-shadow: 0 0 10px #22c55e;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(0.9); }
        }
        .status-text {
            font-size: 10px;
            font-weight: 600;
            color: #22c55e;
            letter-spacing: 1px;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        
        /* Menu */
        .menu-label {
            font-size: 10px;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 14px;
            text-align: center;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        
        /* Item ativo */
        .nav-active {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.2) 100%);
            border: 1px solid rgba(102, 126, 234, 0.4);
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 6px;
            color: #a5b4fc !important;
            font-weight: 600;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Segoe UI', system-ui, sans-serif;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        
        /* Usuário */
        .user-container {
            background: linear-gradient(145deg, #1a1a2e 0%, #0f0f1a 100%);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 24px 16px;
            text-align: center;
            margin-top: 24px;
        }
        .user-avatar {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 14px;
            font-size: 32px;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
        }
        .user-name {
            font-size: 14px;
            font-weight: 600;
            color: white;
            margin-bottom: 4px;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        .user-role {
            font-size: 11px;
            color: #888;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        .version {
            font-size: 9px;
            color: #444;
            text-align: center;
            margin-top: 18px;
            font-family: 'Consolas', 'Monaco', monospace;
            letter-spacing: 1px;
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
        full_label = f"{icon}  {label}"
        
        if is_active:
            st.markdown(f'<div class="nav-active">{icon}  {label}</div>', unsafe_allow_html=True)
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