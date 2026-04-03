"""
Sidebar - Apenas para direcionar
"""

import streamlit as st


def render_sidebar(lojas, favoritos):
    # Logo
    st.markdown("""
    <style>
        .sidebar-logo {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            margin-bottom: 8px;
            border: 1px solid rgba(102, 126, 234, 0.2);
        }
        .logo-icon {
            font-size: 40px;
            margin-bottom: 8px;
        }
        .logo-title {
            font-size: 18px;
            font-weight: bold;
            color: white;
            letter-spacing: 1px;
        }
        .logo-subtitle {
            font-size: 10px;
            color: #666;
            font-family: monospace;
            letter-spacing: 2px;
        }
        .status-badge {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.2);
            border-radius: 20px;
            padding: 8px 12px;
            margin-bottom: 16px;
            font-size: 11px;
            color: #22c55e;
        }
        .status-dot {
            width: 6px;
            height: 6px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
    <div class="sidebar-logo">
        <div class="logo-icon">🛡️</div>
        <div class="logo-title">CENTRAL DE COMANDO</div>
        <div class="logo-subtitle">DPSP • T.I. v5.0</div>
    </div>
    <div class="status-badge">
        <span class="status-dot"></span>
        SISTEMA OPERACIONAL
    </div>
    """, unsafe_allow_html=True)
    
    # Menu de navegação
    st.markdown("**📌 Menu**")
    
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
    
    for emoji_label, page_value in menu_itens:
        is_active = current_page == page_value
        
        if is_active:
            st.markdown(f"""
            <style>
                .nav-btn-active {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white !important;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 16px;
                    font-weight: 600;
                    text-align: left;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                    margin-bottom: 4px;
                }}
            </style>
            <div class="nav-btn-active">{emoji_label}</div>
            """, unsafe_allow_html=True)
        else:
            if st.button(emoji_label, key=f"nav_{page_value}", use_container_width=True):
                st.session_state.nav_page = page_value
                st.rerun()
    
    st.markdown("---")
    
    # Footer usuário
    st.markdown("""
    <style>
        .user-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }
        .user-avatar {
            font-size: 32px;
            margin-bottom: 8px;
        }
        .user-name {
            font-size: 14px;
            font-weight: 600;
            color: white;
        }
        .user-role {
            font-size: 11px;
            color: #666;
        }
        .version {
            font-size: 9px;
            color: #444;
            text-align: center;
            margin-top: 12px;
            font-family: monospace;
        }
    </style>
    <div class="user-card">
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