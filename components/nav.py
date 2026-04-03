"""
Sidebar - Apenas o necessário
"""

import streamlit as st


_PAGINA_INICIAL = "🏪 Consulta de Lojas"


def render_sidebar(lojas, favoritos):
    st.markdown("### 🛡️ Central de Comando")
    
    # Lista de páginas
    opcoes = [
        "🏪 Consulta de Lojas",
        "🚨 Gestão de Crises", 
        "📞 Abertura de Chamados",
        "📋 Histórico",
        "📈 Dashboard",
        "❓ Ajuda"
    ]
    
    # Pega página atual
    atual = st.session_state.get("nav_page", _PAGINA_INICIAL)
    
    # Menu de seleção
    pagina = st.selectbox("Ir para:", opcoes, index=opcoes.index(atual) if atual in opcoes else 0)
    
    # Atualiza se mudou
    if pagina != atual:
        st.session_state.nav_page = pagina
        st.rerun()
    
    st.markdown("---")
    
    # Stats simples
    if lojas:
        st.metric("Total", len(lojas))
    
    st.markdown("---")
    st.caption("📞 (11) 3274-7527")
    
    return pagina


def render_footer():
    st.markdown("---")
    st.caption("🛡️ Central de Comando DPSP - Uso Interno")


def init_session_state():
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = _PAGINA_INICIAL


def setup_page_config():
    st.set_page_config(
        page_title="Central de Comando — DPSP",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_page_header(title: str, subtitle: str = None, icon: str = None):
    if icon:
        title = f"{icon} {title}"
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")
