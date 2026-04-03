"""
Sidebar de Navegação
"""

import streamlit as st
from typing import List


_MENU = [
    "🏪 Consulta de Lojas",
    "🚨 Gestão de Crises",
    "📞 Abertura de Chamados",
    "📋 Histórico",
    "📈 Dashboard",
    "❓ Ajuda",
]

_PAGE_DEFAULT = "Consulta de Lojas"


def render_sidebar(lojas: List[dict], favoritos: List[str], **_) -> str:
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = _PAGE_DEFAULT

    pagina_atual = st.session_state.nav_page
    
    # ═══════════════════════════════════════════════════════════════════════
    # TÍTULO
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("### 🛡️ Central de Comando")
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════════════
    # NAVEGAÇÃO COM RADIO (mais bonito que botão)
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("**Navegação**")
    
    # Usar radio para seleção de página
    opcao = st.radio(
        "Selecione uma página:",
        _MENU,
        index=_MENU.index(pagina_atual) if pagina_atual in _MENU else 0,
        label_visibility="collapsed",
        key="nav_radio"
    )
    
    if opcao != pagina_atual:
        st.session_state.nav_page = opcao
        st.rerun()
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════════════
    # ESTATÍSTICAS
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("**Estatísticas**")
    total = len(lojas) if lojas else 0
    if total > 0:
        ativas = sum(1 for l in lojas if l.get("status") == "open")
        st.metric("Total de Lojas", total)
        st.metric("Lojas Ativas", ativas)
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════════════
    # CONTATO
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("**Contato**")
    st.info("📞 Central: (11) 3274-7527")

    return pagina_atual


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
