"""
Módulo de navegação e sidebar
Central de Comando DPSP v4.1
"""

import streamlit as st
from typing import List


_MENU = [
    ("🏪", "Consulta de Lojas",     "#6366f1"),
    ("🚨", "Gestão de Crises",      "#ef4444"),
    ("📞", "Abertura de Chamados",  "#10b981"),
    ("📋", "Histórico",             "#a855f7"),
    ("📈", "Dashboard",             "#f59e0b"),
    ("❓", "Ajuda",                 "#a0a0b0"),
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

    # ── Logo com animação ────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="sb-logo">
            <div class="sb-logo-icon">🛡️</div>
            <div>
                <div class="sb-logo-title">Central de Comando</div>
                <div class="sb-logo-sub">DPSP T.I. · v4.1</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Status com animação glow ────────────────────────────────────────────────
    st.markdown(
        '<div class="sb-status">'
        '<div class="sb-status-dot"></div>'
        '<span>Sistema Operacional</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Busca rápida na sidebar ────────────────────────────────────────────────
    st.markdown("<div class='sb-section-label'>🔍 Busca Rápida</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sb-quick-search">
            <input type="text" placeholder="Digite VD ou nome..." class="sb-search-input">
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── KPIs melhorados ─────────────────────────────────────────────────────────
    st.markdown("<div class='sb-section-label'>📊 Parque de Lojas</div>", unsafe_allow_html=True)
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
    
    # ── Estatísticas por bandeira ───────────────────────────────────────────────
    if lojas:
        bandeiras = {}
        for l in lojas:
            b = l.get("bandeira", "Outros")
            bandeiras[b] = bandeiras.get(b, 0) + 1
        
        if len(bandeiras) > 1:
            st.markdown("<div class='sb-section-label'>🏷️ Por Bandeira</div>", unsafe_allow_html=True)
            band_html = ""
            for b, qtd in sorted(bandeiras.items(), key=lambda x: x[1], reverse=True)[:4]:
                pct_b = round(qtd/total*100)
                band_html += f"""
                <div class="sb-stat-row">
                    <span class="sb-stat-label">{b}</span>
                    <span class="sb-stat-value">{qtd} <span class="sb-stat-pct">({pct_b}%)</span></span>
                </div>
                """
            st.markdown(f'<div class="sb-stats-box">{band_html}</div>', unsafe_allow_html=True)
    
    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Navegação com ícones coloridos ───────────────────────────────────────────
    st.markdown("<div class='sb-section-label'>📌 Menu Principal</div>", unsafe_allow_html=True)

    for icon, nome, cor in _MENU:
        ativo = pagina_atual == nome
        if ativo:
            st.markdown('<div class="nav-active-marker"></div>', unsafe_allow_html=True)
        
        btn_key = f"navbtn_{nome}"
        if st.button(f"{icon}  {nome}", key=btn_key, use_container_width=True):
            st.session_state.nav_page = nome
            st.rerun()

    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Favoritos com mais detalhes ─────────────────────────────────────────────
    if favoritos:
        st.markdown("<div class='sb-section-label'>⭐ Favoritos</div>", unsafe_allow_html=True)
        idx = {l.get("vd"): l for l in lojas} if lojas else {}
        
        for vd in favoritos[:5]:
            loja = idx.get(vd)
            if loja:
                nome_curto = loja.get("nome", "")[:20] + "…" if len(loja.get("nome", "")) > 20 else loja.get("nome", "")
                cidade = loja.get("cidade", "")
                status = loja.get("status", "closed")
                status_icon = "🟢" if status == "open" else "🔴"
                
                st.markdown(
                    f'<div class="sb-fav-item">'
                    f'<span class="sb-fav-vd">{vd}</span>'
                    f'<span class="sb-fav-nome">{nome_curto}</span>'
                    f'<span class="sb-fav-status">{status_icon}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="sb-fav-item">'
                    f'<span class="sb-fav-vd">{vd}</span>'
                    f'<span class="sb-fav-nome">VD não encontrado</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

    # ── Contatos rápidos com ícones atualizados ────────────────────────────────
    st.markdown("<div class='sb-section-label'>📞 Contatos Rápidos</div>", unsafe_allow_html=True)
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
            <a href="https://wa.me/5511999999999" target="_blank" class="sb-contact-item">
                <div class="sb-contact-icon">🚨</div>
                <div>
                    <div class="sb-contact-name">Emergências 24h</div>
                    <div class="sb-contact-tel">(11) 99999-9999</div>
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # ── Atalhos rápido ─────────────────────────────────────────────────────────
    st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sb-section-label'>⚡ Atalhos</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📈 Dashboard", use_container_width=True, key="short_dash"):
            st.session_state.nav_page = "Dashboard"
            st.rerun()
    with col2:
        if st.button("🏪 Lojas", use_container_width=True, key="short_lojas"):
            st.session_state.nav_page = "Consulta de Lojas"
            st.rerun()

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
