"""
Sidebar - Claro e objective
"""

import streamlit as st


def render_sidebar(lojas, favoritos):
    # Logo
    st.markdown("**🛡️ CENTRAL DE COMANDO**")
    st.caption("DPSP • T.I. v5.0")
    
    st.markdown("---")
    
    # Feed
    st.markdown("**📊 Feed**")
    if lojas:
        total = len(lojas)
        ativas = sum(1 for l in lojas if l.get("status") == "open")
        st.metric("Total Lojas", total)
        st.metric("Ativas", ativas)
    
    st.markdown("---")
    
    # Menu
    st.markdown("**📌 Menu**")
    
    menu_itens = [
        ("📈 Dashboard", "📈 Dashboard"),
        ("🏪 Busca de Lojas", "🏪 Buscar uma loja"),
        ("🚨 Registro de Crises", "🚨 Registrar uma crise"),
        ("📞 Abertura de Chamados", "📞 Abrir chamado na Vivo/Claro"),
        ("📋 Histórico", "📋 Ver histórico de alertas"),
        ("❓ Ajuda", "❓ Ajuda e manual"),
    ]
    
    current_page = st.session_state.get("nav_page", "🏪 Buscar uma loja")
    
    for emoji_label, page_value in menu_itens:
        if st.button(emoji_label, key=f"nav_{page_value}", use_container_width=True):
            st.session_state.nav_page = page_value
            st.rerun()
    
    st.markdown("---")
    
    # Footer usuário
    st.markdown("**👤 Usuário**")
    st.caption("Enzo Maranho")
    st.caption("Analista T.I.")


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