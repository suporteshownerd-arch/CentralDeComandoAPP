"""
Sidebar - Apenas para direcionar
"""

import streamlit as st


def render_sidebar(lojas, favoritos):
    # CSS global para o sidebar
    st.markdown("""
    <style>
        /* Logo - mais elegante */
        .sidebar-logo {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            border-radius: 20px;
            padding: 32px 20px;
            text-align: center;
            margin-bottom: 24px;
            box-shadow: 0 12px 40px rgba(99, 102, 241, 0.4), inset 0 1px 0 rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.15);
        }
        .logo-icon {
            font-size: 48px;
            margin-bottom: 12px;
            display: block;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
        }
        .logo-title {
            font-size: 17px;
            font-weight: 800;
            color: white;
            letter-spacing: 1.5px;
            display: block;
            margin-bottom: 6px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .logo-subtitle {
            font-size: 10px;
            color: rgba(255,255,255,0.8);
            font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
            letter-spacing: 3px;
            display: block;
            font-weight: 500;
        }
        
        /* Status - mais destacado */
        .status-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(16, 185, 129, 0.1) 100%);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 30px;
            padding: 12px 20px;
            margin-bottom: 28px;
        }
        .status-dot {
            width: 10px;
            height: 10px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
            box-shadow: 0 0 16px #22c55e, 0 0 32px rgba(34, 197, 94, 0.4);
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(0.85); }
        }
        .status-text {
            font-size: 11px;
            font-weight: 700;
            color: #22c55e;
            letter-spacing: 1.5px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Menu */
        .menu-label {
            font-size: 11px;
            font-weight: 600;
            color: #555;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 16px;
            text-align: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Item ativo - mais impactante */
        .nav-active {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.25) 100%);
            border: 1px solid rgba(139, 92, 246, 0.5);
            border-radius: 14px;
            padding: 16px 18px;
            margin-bottom: 8px;
            color: #c4b5fd !important;
            font-weight: 700;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 14px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3), inset 0 1px 0 rgba(255,255,255,0.1);
        }
        
        /* Usuário - mais sofisticado */
        .user-container {
            background: linear-gradient(180deg, #12121a 0%, #0a0a0f 100%);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 20px;
            padding: 28px 20px;
            text-align: center;
            margin-top: 28px;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
        }
        .user-avatar {
            width: 72px;
            height: 72px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px;
            font-size: 36px;
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4), inset 0 2px 0 rgba(255,255,255,0.15);
            border: 3px solid rgba(255,255,255,0.1);
        }
        .user-name {
            font-size: 15px;
            font-weight: 700;
            color: white;
            margin-bottom: 6px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .user-role {
            font-size: 12px;
            color: #666;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-weight: 500;
        }
        .version {
            font-size: 10px;
            color: #333;
            text-align: center;
            margin-top: 20px;
            font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
            letter-spacing: 2px;
            font-weight: 600;
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
        full_label = f"{icon}   {label}"
        
        if is_active:
            st.markdown(f'<div class="nav-active">{icon}   {label}</div>', unsafe_allow_html=True)
        else:
            if st.button(full_label, key=f"nav_{page_value}", use_container_width=True):
                st.session_state.nav_page = page_value
                st.rerun()
    
    # Footer usuário
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