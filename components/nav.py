"""
Módulo de navegação e sidebar
Central de Comando DPSP v3.1
"""

import streamlit as st
from typing import List


_MENU = [
    ("🏪", "Consulta de Lojas",     "#5b8def"),
    ("🚨", "Gestão de Crises",      "#f87171"),
    ("📞", "Abertura de Chamados",  "#34d399"),
    ("📋", "Histórico",             "#a78bfa"),
    ("📈", "Dashboard",             "#fbbf24"),
    ("❓", "Ajuda",                 "#9094a6"),
]

_PAGE_DEFAULT = "Consulta de Lojas"


def render_sidebar(lojas: List[dict], favoritos: List[str], **_) -> str:
    total    = len(lojas) if lojas else 0
    ativas   = sum(1 for l in lojas if l.get("status") == "open")   if lojas else 0
    inativas = sum(1 for l in lojas if l.get("status") == "closed") if lojas else 0
    pct      = round(ativas / total * 100) if total else 0

    if "nav_page" not in st.session_state:
        st.session_state.nav_page = _PAGE_DEFAULT

    pagina_atual = st.session_state.nav_page

    # ── Logo ─────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="sb-logo">
            <div class="sb-logo-icon">🛡️</div>
            <div>
                <div class="sb-logo-title">Central de Comando</div>
                <div class="sb-logo-sub">DPSP T.I. · v4.0</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Status ────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="sb-status">'
        '<div class="sb-status-dot"></div>'
        '<span>Sistema Operacional</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── KPIs ──────────────────────────────────────────────────────────────────
    st.markdown("<div class='sb-section-label'>Parque de Lojas</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="sb-kpi-row">
            <div class="sb-kpi">
                <div class="sb-kpi-value accent">{total:,}</div>
                <div class="sb-kpi-label">Total</div>
            </div>
            <div class="sb-kpi-sep"></div>
            <div class="sb-kpi">
                <div class="sb-kpi-value green">{ativas:,}</div>
                <div class="sb-kpi-label">Ativas</div>
            </div>
            <div class="sb-kpi-sep"></div>
            <div class="sb-kpi">
                <div class="sb-kpi-value red">{inativas:,}</div>
                <div class="sb-kpi-label">Inativas</div>
            </div>
        </div>
        <div class="sb-bar-wrap">
            <div class="sb-bar-fill" style="width:{pct}%"></div>
        </div>
        <div class="sb-bar-legend">
            <span class="green">● {pct}% ativas</span>
            <span class="red">● {100-pct}% inativas</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Navegação ─────────────────────────────────────────────────────────────
    st.markdown("<div class='sb-section-label'>Menu</div>", unsafe_allow_html=True)

    for icon, nome, cor in _MENU:
        ativo = pagina_atual == nome
        if ativo:
            st.markdown('<div class="nav-active-marker"></div>', unsafe_allow_html=True)
        # Ícone colorido inline antes do texto
        st.markdown(
            f"<div class='nav-icon-hint' style='--nav-cor:{cor}'></div>",
            unsafe_allow_html=True,
        )
        if st.button(f"{icon}  {nome}", key=f"navbtn_{nome}", use_container_width=True):
            st.session_state.nav_page = nome
            st.rerun()

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Favoritos ─────────────────────────────────────────────────────────────
    if favoritos:
        st.markdown("<div class='sb-section-label'>⭐ Favoritos</div>", unsafe_allow_html=True)
        idx = {l.get("vd"): l.get("nome", "") for l in lojas} if lojas else {}
        items = ""
        for vd in favoritos[:5]:
            nome_loja = idx.get(vd, f"VD {vd}")
            curto = nome_loja[:22] + "…" if len(nome_loja) > 22 else nome_loja
            items += (
                f'<div class="sb-fav-item">'
                f'<span class="sb-fav-vd">{vd}</span>'
                f'<span class="sb-fav-nome">{curto}</span>'
                f'</div>'
            )
        st.markdown(items, unsafe_allow_html=True)
        st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Contatos ──────────────────────────────────────────────────────────────
    st.markdown("<div class='sb-section-label'>Contatos Rápidos</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sb-contacts">
            <a href="https://wa.me/551132747527" target="_blank" class="sb-contact-item">
                <div class="sb-contact-icon">🎛️</div>
                <div>
                    <div class="sb-contact-name">Central de Comando</div>
                    <div class="sb-contact-tel">(11) 3274-7527</div>
                </div>
            </a>
            <a href="https://wa.me/551155296003" target="_blank" class="sb-contact-item">
                <div class="sb-contact-icon">💻</div>
                <div>
                    <div class="sb-contact-name">T.I. DPSP</div>
                    <div class="sb-contact-tel">(11) 5529-6003</div>
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return pagina_atual


def render_footer():
    st.markdown(
        """<div class="footer">
            <b>🛡️ Central de Comando DPSP v4.0</b><br>
            Desenvolvido por Enzo Maranho — T.I. DPSP · Uso Interno
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
