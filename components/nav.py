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
            border-radius: 16px;
            padding: 20px 16px;
            text-align: center;
            margin-bottom: 16px;
            box-shadow: 0 6px 24px rgba(99, 102, 241, 0.35);
        }
        .logo-icon { font-size: 32px; margin-bottom: 8px; display: block; }
        .logo-title {
            font-size: 13px; font-weight: 700; color: white; letter-spacing: 1px;
            display: block; font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .logo-subtitle {
            font-size: 8px; color: rgba(255,255,255,0.75);
            font-family: 'Consolas', monospace; letter-spacing: 2px;
            display: block; margin-top: 4px;
        }
        
        /* Status */
        .status-container {
            display: flex; align-items: center; justify-content: center; gap: 8px;
            background: rgba(34, 197, 94, 0.12); border: 1px solid rgba(34, 197, 94, 0.25);
            border-radius: 20px; padding: 8px 14px; margin-bottom: 16px;
        }
        .status-dot {
            width: 8px; height: 8px; background: #22c55e; border-radius: 50%;
            animation: pulse 2s infinite; box-shadow: 0 0 8px #22c55e;
        }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .status-text {
            font-size: 10px; font-weight: 600; color: #22c55e; letter-spacing: 1px;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Menu label */
        .menu-label {
            font-size: 10px; font-weight: 600; color: #555;
            text-transform: uppercase; letter-spacing: 1.5px;
            margin-bottom: 12px; text-align: center;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Card navegação - todos os estados bonitaos */
        .nav-item {
            display: flex; align-items: center; gap: 12px;
            padding: 14px 16px; margin-bottom: 10px;
            border-radius: 14px; cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative; overflow: hidden;
        }
        
        /* Estado inativo - visual bonito */
        .nav-item {
            background: linear-gradient(135deg, #3d3d52 0%, #2d2d40 100%);
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        .nav-item:hover {
            background: linear-gradient(135deg, #4a4a65 0%, #3a3a52 100%);
            border-color: rgba(139, 92, 246, 0.5);
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 24px rgba(0,0,0,0.35), 0 0 20px rgba(139, 92, 246, 0.15);
        }
        
        /* Estado ativo - ainda mais bonito */
        .nav-item.active {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            border-color: rgba(255,255,255,0.25);
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.5), 0 0 40px rgba(139, 92, 246, 0.3);
            transform: scale(1.02);
        }
        .nav-item.active:hover {
            transform: scale(1.03);
        }
        
        /* Ícone */
        .nav-icon {
            width: 40px; height: 40px;
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; flex-shrink: 0;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }
        .nav-item:hover .nav-icon {
            background: rgba(139, 92, 246, 0.3);
            transform: rotate(5deg) scale(1.1);
        }
        .nav-item.active .nav-icon {
            background: rgba(255,255,255,0.25);
            border-color: rgba(255,255,255,0.3);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* Texto */
        .nav-text { flex: 1; min-width: 0; }
        .nav-title {
            font-size: 14px; font-weight: 600; color: #e0e0e8;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            margin-bottom: 3px; transition: color 0.3s;
        }
        .nav-item:hover .nav-title { color: white; }
        .nav-item.active .nav-title { color: white; font-weight: 700; }
        
        .nav-desc {
            font-size: 11px; color: #8a8a9a;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .nav-item:hover .nav-desc { color: #aaaabc; }
        .nav-item.active .nav-desc { color: rgba(255,255,255,0.8); }
        
        /* Usuário */
        .user-container {
            background: linear-gradient(180deg, #2d2d40 0%, #1e1e28 100%);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px; padding: 18px; text-align: center; margin-top: 24px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.25);
        }
        .user-avatar {
            width: 52px; height: 52px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            margin: 0 auto 12px; font-size: 26px;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
            border: 2px solid rgba(255,255,255,0.15);
        }
        .user-name {
            font-size: 14px; font-weight: 600; color: white;
            margin-bottom: 3px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .user-role {
            font-size: 11px; color: #888;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .version {
            font-size: 9px; color: #555; text-align: center;
            margin-top: 14px; font-family: 'Consolas', monospace;
            letter-spacing: 1.5px; font-weight: 600;
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
    
    # Menu
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
            <div class="nav-item active">
                <div class="nav-icon">{icon}</div>
                <div class="nav-text">
                    <div class="nav-title">{title}</div>
                    <div class="nav-desc">{desc}</div>
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
    st.set_page_config(page_title="Central de Comando", page_icon="🛡️", layout="wide")


def render_page_header(title, subtitle=None, icon=None):
    if icon: title = f"{icon} {title}"
    st.markdown(f"## {title}")
    if subtitle: st.markdown(f"*{subtitle}*")