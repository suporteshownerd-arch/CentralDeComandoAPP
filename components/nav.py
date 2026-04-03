"""
Sidebar de Navegação - Super Simples
"""

import streamlit as st
from typing import List


_PAGINAS = [
    "🏪 Consulta de Lojas",
    "🚨 Gestão de Crises", 
    "📞 Abertura de Chamados",
    "📋 Histórico",
    "📈 Dashboard",
    "❓ Ajuda",
]

_DEFAULT = "🏪 Consulta de Lojas"


def render_sidebar(lojas: List[dict], favoritos: List[str], **_) -> str:
    # Pegar ou criar página atual
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = _DEFAULT

    # ═══════════════════════════════════════════════════════════════════════
    # TÍTULO DO APP
    # ═══════════════════════════════════════════════════════════════════════
    st.title("🛡️ Central de Comando")
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════
    # SELETOR DE PÁGINA (st.selectbox)
    # ═══════════════════════════════════════════════════════════════════════
    st.header("Navegação")
    
    # Selectbox para mudar de página
    pagina_selecionada = st.selectbox(
        "Escolha uma página:",
        _PAGINAS,
        index=_PAGINAS.index(st.session_state.nav_page) if st.session_state.nav_page in _PAGINAS else 0,
        label_visibility="collapsed"
    )
    
    # Se mudou, atualizar
    if pagina_selecionada != st.session_state.nav_page:
        st.session_state.nav_page = pagina_selecionada
        st.rerun()
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════
    # INFO DO PARQUE
    # ═══════════════════════════════════════════════════════════════════════
    if lojas:
        total = len(lojas)
        ativas = sum(1 for l in lojas if l.get("status") == "open")
        st.metric("Total de Lojas", total)
        st.metric("Lojas Ativas", ativas)
    else:
        st.info("Nenhuma loja carregada")
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════
    # CONTATO
    # ═══════════════════════════════════════════════════════════════════════
    st.caption("📞 Central: (11) 3274-7527")

    return st.session_state.nav_page


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
