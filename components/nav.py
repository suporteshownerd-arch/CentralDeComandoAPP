"""
Sidebar - Claro e objective
"""

import streamlit as st
from datetime import datetime


def render_sidebar(lojas, favoritos):
    # Logo Melhorado
    st.markdown("""
    <style>
        .logo-container {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 16px;
        }
        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .logo-text {
            display: flex;
            flex-direction: column;
        }
        .logo-title {
            font-size: 16px;
            font-weight: bold;
            color: white;
            letter-spacing: 0.5px;
        }
        .logo-subtitle {
            font-size: 10px;
            color: rgba(255,255,255,0.5);
            font-family: monospace;
            letter-spacing: 1px;
        }
    </style>
    <div class="logo-container">
        <div class="logo-icon">🛡️</div>
        <div class="logo-text">
            <span class="logo-title">CENTRAL DE COMANDO</span>
            <span class="logo-subtitle">DPSP • T.I. v5.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status indicator
    st.markdown("""
    <style>
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            background: rgba(34, 197, 94, 0.15);
            border-radius: 20px;
            font-size: 11px;
            color: #22c55e;
            margin-bottom: 16px;
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
    <div class="status-badge">
        <span class="status-dot"></span>
        SISTEMA OPERACIONAL
    </div>
    """, unsafe_allow_html=True)
    
    # Feed / Estatísticas
    st.markdown("**📊 Feed**")
    if lojas:
        total = len(lojas)
        ativas = sum(1 for l in lojas if l.get("status") == "open")
        inativas = total - ativas
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏪 Total", total)
        with col2:
            st.metric("✅ Ativas", ativas)
        
        col3, col4 = st.columns(2)
        with col3:
            st.metric("❌ Inativas", inativas)
        with col4:
            estados = len({l.get("estado") for l in lojas if l.get("estado")})
            st.metric("🗺️ Estados", estados)
    
    st.markdown("---")
    
    # Menu de Navegação
    st.markdown("**📌 Menu**")
    
    menu_itens = [
        ("📈 Dashboard", "📈 Dashboard"),
        ("🏪 Busca de Lojas", "🏪 Buscar uma loja"),
        ("🚨 Registro de Crises", "🚨 Registrar uma crise"),
        ("📞 Abertura de Chamados", "📞 Abrir chamado na Vivo/Claro"),
        ("📋 Histórico", "📋 Ver histórico de alertas"),
        ("❓ Ajuda", "❓ Ajuda e manual"),
    ]
    
    # Get current page
    current_page = st.session_state.get("nav_page", "🏪 Buscar uma loja")
    
    # Render menu buttons
    for emoji_label, page_value in menu_itens:
        is_active = current_page == page_value
        
        # Custom button styling
        button_style = """
        <style>
            .nav-btn {
                width: 100%;
                padding: 10px 12px;
                margin-bottom: 4px;
                border: none;
                border-radius: 8px;
                background: rgba(255,255,255,0.05);
                color: rgba(255,255,255,0.7);
                font-size: 13px;
                font-weight: 500;
                text-align: left;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .nav-btn:hover {
                background: rgba(255,255,255,0.1);
                color: white;
            }
            .nav-btn.active {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
        </style>
        """
        
        if is_active:
            st.markdown(button_style, unsafe_allow_html=True)
            st.markdown(f'<button class="nav-btn active">{emoji_label}</button>', unsafe_allow_html=True)
        else:
            if st.button(emoji_label, key=f"nav_{page_value}", use_container_width=True):
                st.session_state.nav_page = page_value
                st.rerun()
    
    st.markdown("---")
    
    # Contato
    st.markdown("**Precisa de ajuda?**")
    st.info("📞 Ligue: (11) 3274-7527")
    
    st.markdown("---")
    
    # Footer com usuário
    st.markdown(f"""
    <style>
        .user-footer {{
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .user-avatar {{
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }}
        .user-info {{
            flex: 1;
        }}
        .user-name {{
            font-size: 13px;
            font-weight: 600;
            color: white;
        }}
        .user-role {{
            font-size: 10px;
            color: rgba(255,255,255,0.5);
        }}
    </style>
    <div class="user-footer">
        <div class="user-avatar">👤</div>
        <div class="user-info">
            <div class="user-name">Enzo Maranho</div>
            <div class="user-role">Analista T.I.</div>
        </div>
    </div>
    <p style="text-align: center; font-size: 9px; color: rgba(255,255,255,0.3); margin-top: 8px; font-family: monospace;">
        Jarvis v5.0 • T.I. DPSP
    </p>
    """, unsafe_allow_html=True)
    
    return st.session_state.get("nav_page", "🏪 Buscar uma loja")


def render_footer():
    st.caption("Central de Comando DPSP - v5.0")


def init_session_state():
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "🏪 Buscar uma loja"


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