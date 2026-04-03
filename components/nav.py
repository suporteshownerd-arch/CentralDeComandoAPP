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
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border-radius: 18px;
            padding: 24px 16px;
            text-align: center;
            margin-bottom: 16px;
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.35);
            position: relative;
            overflow: hidden;
        }
        .sidebar-logo::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            animation: shimmer 3s infinite;
        }
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        .logo-icon {
            font-size: 36px;
            margin-bottom: 8px;
            display: block;
        }
        .logo-title {
            font-size: 14px;
            font-weight: 700;
            color: white;
            letter-spacing: 1px;
            display: block;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        .logo-subtitle {
            font-size: 9px;
            color: rgba(255,255,255,0.75);
            font-family: 'Consolas', monospace;
            letter-spacing: 2px;
            display: block;
            margin-top: 4px;
        }
        
        /* Status */
        .status-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.25);
            border-radius: 20px;
            padding: 8px 14px;
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
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .status-text {
            font-size: 10px;
            font-weight: 600;
            color: #22c55e;
            letter-spacing: 1px;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Menu label */
        .menu-label {
            font-size: 10px;
            font-weight: 600;
            color: #555;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
            text-align: center;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Card de navegação - estilo Glassmorphism */
        .nav-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
            overflow: hidden;
        }
        .nav-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 3px;
            background: transparent;
            transition: all 0.3s ease;
            border-radius: 0 3px 3px 0;
        }
        .nav-card:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(139, 92, 246, 0.3);
            transform: translateX(4px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        .nav-card:hover::before {
            background: linear-gradient(180deg, #6366f1, #8b5cf6);
        }
        
        .nav-card.active {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
            border-color: rgba(139, 92, 246, 0.4);
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
        }
        .nav-card.active::before {
            background: linear-gradient(180deg, #818cf8, #a78bfa);
            width: 4px;
        }
        
        .nav-card-icon {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255,255,255,0.08);
            transition: all 0.3s ease;
        }
        .nav-card.active .nav-card-icon {
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255,255,255,0.2);
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
        }
        
        .nav-card-info {
            flex: 1;
            min-width: 0;
        }
        .nav-card-title {
            font-size: 13px;
            font-weight: 500;
            color: #d0d0d8;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            margin-bottom: 2px;
            transition: color 0.3s ease;
        }
        .nav-card:hover .nav-card-title {
            color: white;
        }
        .nav-card.active .nav-card-title {
            color: #c4b5fd;
            font-weight: 600;
        }
        .nav-card-desc {
            font-size: 10px;
            color: #5a5a6a;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            transition: color 0.3s ease;
        }
        .nav-card:hover .nav-card-desc {
            color: #7a7a8a;
        }
        .nav-card.active .nav-card-desc {
            color: #a5a5b8;
        }
        
        /* Usuário */
        .user-container {
            background: linear-gradient(180deg, rgba(30, 30, 40, 0.8) 0%, rgba(20, 20, 30, 0.9) 100%);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 20px 16px;
            text-align: center;
            margin-top: 24px;
        }
        .user-avatar {
            width: 56px;
            height: 56px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 12px;
            font-size: 28px;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
            border: 2px solid rgba(255,255,255,0.1);
        }
        .user-name {
            font-size: 14px;
            font-weight: 600;
            color: white;
            margin-bottom: 4px;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .user-role {
            font-size: 11px;
            color: #777;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .version {
            font-size: 9px;
            color: #444;
            text-align: center;
            margin-top: 16px;
            font-family: 'Consolas', monospace;
            letter-spacing: 1.5px;
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