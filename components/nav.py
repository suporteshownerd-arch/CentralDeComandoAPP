"""
Módulo de navegação e sidebar
Central de Comando DPSP v5.0 - Minimalista
"""

import streamlit as st
from typing import List
from datetime import datetime


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
    try:
        if "nav_page" not in st.session_state:
            st.session_state.nav_page = _PAGE_DEFAULT

        pagina_atual = st.session_state.nav_page
        total = len(lojas) if lojas else 0

        # ═══════════════════════════════════════════════════════════════════════
        # HEADER SIMPLES
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="sb-simple-header">
            <div class="sb-simple-logo">🛡️</div>
            <div class="sb-simple-title">Central de Comando</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='sb-simple-divider'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # NAVEGAÇÃO PRINCIPAL
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sb-simple-label'>PÁGINAS</div>", unsafe_allow_html=True)

        for icon, nome in _MENU:
            ativo = pagina_atual == nome
            
            btn_key = f"navbtn_{nome}"
            
            # Botão com estilo diferente se ativo
            if st.button(
                f"{icon}  {nome}", 
                key=btn_key, 
                use_container_width=True,
                type="primary" if ativo else "secondary"
            ):
                st.session_state.nav_page = nome
                st.rerun()

        st.markdown("<div class='sb-simple-divider'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # RESUMO RÁPIDO (apenas número total)
        # ═══════════════════════════════════════════════════════════════════════
        if total > 0:
            ativas = sum(1 for l in lojas if l.get("status") == "open")
            pct = round(ativas / total * 100)
            
            st.markdown(f"""
            <div class="sb-simple-stats">
                <span class="sb-simple-stat-label">Total de lojas</span>
                <span class="sb-simple-stat-value">{total}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='sb-simple-divider'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # FAVORITOS (apenas se existirem)
        # ═══════════════════════════════════════════════════════════════════════
        if favoritos:
            st.markdown("<div class='sb-simple-label'>⭐ FAVORITOS</div>", unsafe_allow_html=True)
            
            idx = {l.get("vd"): l.get("nome", "") for l in lojas} if lojas else {}
            
            for vd in favoritos:
                nome = idx.get(vd, f"VD {vd}")
                nome_curto = nome[:20] + "..." if len(nome) > 20 else nome
                
                st.markdown(
                    f'<div class="sb-simple-fav">🏷️ {vd} - {nome_curto}</div>',
                    unsafe_allow_html=True,
                )
            
            st.markdown("<div class='sb-simple-divider'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # CONTATO ÚNICO
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sb-simple-label'>📞 AJUDA</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="sb-simple-contact">
            <span>🎛️ Central: (11) 3274-7527</span>
        </div>
        """, unsafe_allow_html=True)

        return pagina_atual
        
    except Exception as e:
        st.error(f"Erro: {str(e)}")
        return _PAGE_DEFAULT


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
