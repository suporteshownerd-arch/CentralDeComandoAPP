"""
Sidebar - Simples e funcional
"""

import streamlit as st
from typing import List


_MENU = [
    ("🏪", "Consulta de Lojas"),
    ("🚨", "Gestão de Crises"),
    ("📞", "Abertura de Chamados"),
    ("📋", "Histórico"),
    ("📈", "Dashboard"),
    ("❓", "Ajuda"),
]

_PAGE_DEFAULT = "Consulta de Lojas"


def render_sidebar(lojas: List[dict], favoritos: List[str], **_) -> str:
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = _PAGE_DEFAULT

    pagina_atual = st.session_state.nav_page
    
    # ── Logo ─────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: -10px -1rem 20px -1rem;
            border-radius: 0 0 16px 16px;
        ">
            <span style="font-size: 32px;">🛡️</span>
            <div>
                <div style="font-size: 18px; font-weight: bold; color: white;">Central de Comando</div>
                <div style="font-size: 11px; color: rgba(255,255,255,0.7);">DPSP T.I.</div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # ── Menu de Navegação ────────────────────────────────────────────────────
    for nome in _MENU:
        icon = nome.split()[0]  # Pega o emoji
        
        # Botão para navegar
        if st.button(f"{icon} {nome}", key=f"nav_{nome}", use_container_width=True):
            st.session_state.nav_page = nome
            st.rerun()
    
    st.markdown("---")
    
    # ── Contato ─────────────────────────────────────────────────────────────
    st.markdown("**📞 Central de Comando**")
    st.caption("(11) 3274-7527")

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
