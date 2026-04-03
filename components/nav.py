"""
Sidebar - Super simples
"""

import streamlit as st


def render_sidebar(lojas, favoritos):
    # Título
    st.markdown("### 🛡️ Central de Comando")
    
    # Navegação com radio
    pagina = st.radio(
        "Páginas",
        [
            "🏪 Consulta de Lojas",
            "🚨 Gestão de Crises",
            "📞 Chamados",
            "📋 Histórico",
            "📈 Dashboard",
            "❓ Ajuda"
        ]
    )
    
    # Atualiza sessão
    st.session_state.nav_page = pagina
    
    st.markdown("---")
    
    # Contato
    st.caption("📞 (11) 3274-7527")
    
    return pagina


def render_footer():
    st.caption("Central de Comando DPSP")


def init_session_state():
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "🏪 Consulta de Lojas"


def setup_page_config():
    st.set_page_config(
        page_title="Central de Comando — DPSP",
        page_icon="🛡️",
        layout="wide",
    )


def render_page_header(title, subtitle=None, icon=None):
    if icon:
        title = f"{icon} {title}"
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")
