"""
Módulo de navegação e sidebar
Central de Comando DPSP v3.0
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


def render_sidebar(lojas: List[dict], favoritos: List[str], **_) -> str:
    total  = len(lojas) if lojas else 0
    ativas = sum(1 for l in lojas if l.get("status") == "open") if lojas else 0
    inativas = total - ativas
    pct_ativas = round(ativas / total * 100) if total else 0

    # ── Logo / cabeçalho ─────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="sb-logo">
            <div class="sb-logo-icon">🛡️</div>
            <div>
                <div class="sb-logo-title">Central de Comando</div>
                <div class="sb-logo-sub">DPSP T.I. · v3.0</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Status online ─────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="sb-status">
            <div class="sb-status-dot"></div>
            <span>Sistema Operacional</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Parque de Lojas ───────────────────────────────────────────────────────
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
            <div class="sb-bar-fill" style="width:{pct_ativas}%"></div>
        </div>
        <div class="sb-bar-legend">
            <span class="green">● {pct_ativas}% ativas</span>
            <span class="red">● {100-pct_ativas}% inativas</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Navegação ─────────────────────────────────────────────────────────────
    st.markdown("<div class='sb-section-label'>Navegação</div>", unsafe_allow_html=True)

    menu_labels = [f"{icon}  {nome}" for icon, nome in _MENU]
    escolha = st.radio("nav", menu_labels, label_visibility="collapsed")
    pagina = escolha.split("  ", 1)[1] if "  " in escolha else escolha

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Favoritos ─────────────────────────────────────────────────────────────
    if favoritos:
        st.markdown("<div class='sb-section-label'>⭐ Favoritos</div>", unsafe_allow_html=True)
        idx = {l.get("vd"): l.get("nome", "") for l in lojas} if lojas else {}
        items_html = ""
        for vd in favoritos[:5]:
            nome = idx.get(vd, f"VD {vd}")
            nome_curto = nome[:20] + "…" if len(nome) > 20 else nome
            items_html += f"""
            <div class="sb-fav-item">
                <span class="sb-fav-vd">{vd}</span>
                <span class="sb-fav-nome">{nome_curto}</span>
            </div>
            """
        st.markdown(items_html, unsafe_allow_html=True)
        st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Contatos rápidos ──────────────────────────────────────────────────────
    st.markdown("<div class='sb-section-label'>Contatos</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sb-contacts">
            <div class="sb-contact-item">
                <span>🎛️</span>
                <div>
                    <div class="sb-contact-name">Central</div>
                    <div class="sb-contact-tel">(11) 3274-7527</div>
                </div>
            </div>
            <div class="sb-contact-item">
                <span>💻</span>
                <div>
                    <div class="sb-contact-name">T.I. DPSP</div>
                    <div class="sb-contact-tel">(11) 5529-6003</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return pagina


def render_page_header(title: str, subtitle: str = None, icon: str = None):
    if icon:
        title = f"{icon} {title}"
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")


def render_footer():
    st.markdown(
        """<div class="footer">
            <b>🛡️ Central de Comando DPSP v3.0</b><br>
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
