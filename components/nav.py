"""
Sidebar - Apenas o necessário
"""

import streamlit as st


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
    
    # Pega página atual ou默认值
    atual = st.session_state.get("nav_page", opcoes[0])
    
    # Menu de seleção
    pagina = st.selectbox("Ir para:", opcoes, index=opcoes.index(atual))
    
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
    st.markdown(
        """<div class="footer">
            <div class="footer-logo">🛡️</div>
            <div class="footer-title">Central de Comando DPSP</div>
            <div class="footer-version">v4.1</div>
            <div class="footer-dev">Desenvolvido por Enzo Maranho — T.I. DPSP</div>
            <div class="footer-copy">Uso Interno · Todos os direitos reservados</div>
        </div>""",
        unsafe_allow_html=True,
    )


def init_session_state():
    defaults = {
        "loja_selecionada": None,
        "nome_atendente": "",
        "favoritos": [],
        "consulta_pagina": 1,
        "nav_page": _PAGE_DEFAULT,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


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
