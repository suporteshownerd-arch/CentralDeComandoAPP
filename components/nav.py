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
        
        /* Menu label */
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
        
        /* Card de navegação */
        .nav-card {
            background: linear-gradient(145deg, #1e1e28 0%, #16161e 100%);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .nav-card:hover {
            background: linear-gradient(145deg, #25252f 0%, #1e1e28 100%);
            border-color: rgba(139, 92, 246, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }
        .nav-card:hover .nav-card-icon {
            transform: scale(1.1);
        }
        
        .nav-card.active {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.35) 0%, rgba(139, 92, 246, 0.3) 100%);
            border: 1px solid rgba(139, 92, 246, 0.6);
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35), inset 0 1px 0 rgba(255,255,255,0.1);
        }
        .nav-card.active:hover {
            border-color: rgba(139, 92, 246, 0.8);
        }
        
        .nav-card-icon {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
            transition: transform 0.25s ease;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
        }
        .nav-card.active .nav-card-icon {
            background: rgba(255,255,255,0.15);
            border-color: rgba(255,255,255,0.2);
        }
        
        .nav-card-info {
            flex: 1;
            min-width: 0;
        }
        .nav-card-title {
            font-size: 14px;
            font-weight: 600;
            color: #e0e0e8;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin-bottom: 3px;
        }
        .nav-card.active .nav-card-title {
            color: #c4b5fd;
            font-weight: 700;
        }
        .nav-card-desc {
            font-size: 11px;
            color: #6b6b7a;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .nav-card.active .nav-card-desc {
            color: #a5a5b8;
        }
        
        /* Usuário */
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
    
    # Menu de navegação com cards
    menu_itens = [
        ("🏠", "Início", "Página inicial", "🏠 Início"),
        ("📊", "Feed", "Visão geral", "📊 Feed"),
        ("📈", "Dashboard", "Gráficos e métricas", "📈 Dashboard"),
        ("🏪", "Busca de Lojas", "Consultar lojas", "🏪 Buscar uma loja"),
        ("🚨", "Registro de Crises", "Cadastrar crise", "🚨 Registrar uma crise"),
        ("📞", "Abertura de Chamados", "Abrir chamado", "📞 Abrir chamado na Vivo/Claro"),
        ("📋", "Histórico", "Ver registros", "📋 Ver histórico de alertas"),
        ("❓", "Ajuda", "Manual e suporte", "❓ Ajuda e manual"),
    ]
    
    current_page = st.session_state.get("nav_page", "🏠 Início")
    
    for icon, title, desc, page_value in menu_itens:
        is_active = current_page == page_value
        
        if is_active:
            st.markdown(f'''
            <div class="nav-card active">
                <div class="nav-card-icon">{icon}</div>
                <div class="nav-card-info">
                    <div class="nav-card-title">{title}</div>
                    <div class="nav-card-desc">{desc}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            if st.button(f"{icon}  {title}", key=f"nav_{page_value}", use_container_width=True):
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