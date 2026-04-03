"""
Módulo de navegação e sidebar
Central de Comando DPSP v4.3
"""

import streamlit as st
from typing import List, Dict
from datetime import datetime


_MENU = [
    ("🏪", "Consulta de Lojas",     "#6366f1"),
    ("🚨", "Gestão de Crises",      "#ef4444"),
    ("📞", "Abertura de Chamados",  "#10b981"),
    ("📋", "Histórico",             "#a855f7"),
    ("📈", "Dashboard",             "#f59e0b"),
    ("❓", "Ajuda",                 "#a0a0b0"),
]

_PAGE_DEFAULT = "Consulta de Lojas"


def _format_number(num: int) -> str:
    """Formata número com sufixos"""
    if num >= 1000:
        return f"{num/1000:.1f}k"
    return str(num)


def _get_status_emoji(status: str) -> str:
    """Retorna emoji basedo no status"""
    if status == "open":
        return "🟢"
    elif status == "pending":
        return "🟡"
    return "🔴"


def _calculate_metrics(lojas: List[dict]) -> Dict:
    """Calcula métricas detalhadas do parque"""
    if not lojas:
        return {}
    
    total = len(lojas)
    ativas = sum(1 for l in lojas if l.get("status") == "open")
    inativas = total - ativas
    pending = sum(1 for l in lojas if l.get("status") == "pending")
    
    # Por estado
    estados = {}
    for l in lojas:
        e = l.get("estado", "Outros")
        estados[e] = estados.get(e, 0) + 1
    
    # Por bandeira
    bandeiras = {}
    for l in lojas:
        b = l.get("bandeira", "Outros")
        bandeiras[b] = bandeiras.get(b, 0) + 1
    
    # Com circuitos
    com_mpls = sum(1 for l in lojas if l.get("mpls"))
    com_inn = sum(1 for l in lojas if l.get("inn"))
    
    # Por região
    regioes = {}
    for l in lojas:
        r = l.get("regiao", "Outros")
        regioes[r] = regioes.get(r, 0) + 1
    
    return {
        "total": total,
        "ativas": ativas,
        "inativas": inativas,
        "pending": pending,
        "pct_ativas": round(ativas / total * 100) if total else 0,
        "estados": estados,
        "bandeiras": bandeiras,
        "regioes": regioes,
        "com_mpls": com_mpls,
        "com_inn": com_inn,
    }


def render_sidebar(lojas: List[dict], favoritos: List[str], **_) -> str:
    try:
        if "nav_page" not in st.session_state:
            st.session_state.nav_page = _PAGE_DEFAULT

        pagina_atual = st.session_state.nav_page
        
        metrics = _calculate_metrics(lojas)
        total = metrics.get("total", 0)
        ativas = metrics.get("ativas", 0)
        inativas = metrics.get("inativas", 0)
        pct = metrics.get("pct_ativas", 0)

        # ── Logo com versão ─────────────────────────────────────────────────────────
        st.markdown(
            """
            <div class="sb-logo">
                <div class="sb-logo-icon">🛡️</div>
                <div>
                    <div class="sb-logo-title">Central de Comando</div>
                    <div class="sb-logo-sub">DPSP T.I. · v4.3</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Status Indicator ─────────────────────────────────────────────────────────
        now = datetime.now()
        hora_atual = now.strftime("%H:%M")
        dia_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"][now.weekday()]
        
        st.markdown(
            f'''
            <div class="sb-status">
                <div class="sb-status-dot"></div>
                <div class="sb-status-content">
                    <span class="sb-status-title">Sistema Operacional</span>
                    <span class="sb-status-meta">{hora_atual} · {dia_semana}</span>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

        # ── KPIs Principal ───────────────────────────────────────────────────────────
        st.markdown("<div class='sb-section-label'>📊 Visão Geral</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="sb-kpi-main">
                <div class="sb-kpi-main-value">{total:,}</div>
                <div class="sb-kpi-main-label">Total de Lojas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Barras de progresso
        st.markdown(
            f"""
            <div class="sb-bar-wrap">
                <div class="sb-bar-fill" style="width:{pct}%"></div>
            </div>
            <div class="sb-bar-legend">
                <span class="green">● Ativas: {ativas} ({pct}%)</span>
                <span class="red">● Inativas: {inativas}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='sb-divider-light'></div>", unsafe_allow_html=True)

        # ── Estatísticas por Bandeira ───────────────────────────────────────────────
        bandeiras = metrics.get("bandeiras", {})
        if bandeiras:
            st.markdown("<div class='sb-section-label'>🏷️ Por Bandeira</div>", unsafe_allow_html=True)
            
            cores_bandeira = {
                "DSP": "#6366f1",
                "D1": "#10b981", 
                "DPR": "#f59e0b",
                "P": "#a855f7",
            }
            
            for band, qtd in sorted(bandeiras.items(), key=lambda x: x[1], reverse=True)[:4]:
                pct_b = round(qtd/total*100) if total else 0
                cor = cores_bandeira.get(band, "#a0a0b0")
                st.markdown(
                    f'''
                    <div class="sb-stat-item">
                        <div class="sb-stat-header">
                            <span class="sb-stat-dot" style="background:{cor}"></span>
                            <span class="sb-stat-name">{band}</span>
                        </div>
                        <div class="sb-stat-values">
                            <span class="sb-stat-qtd">{qtd}</span>
                            <span class="sb-stat-pct">({pct_b}%)</span>
                        </div>
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )
        
        st.markdown("<div class='sb-divider-light'></div>", unsafe_allow_html=True)

        # ── Circuitos ───────────────────────────────────────────────────────────────
        com_mpls = metrics.get("com_mpls", 0)
        com_inn = metrics.get("com_inn", 0)
        
        st.markdown("<div class='sb-section-label'>🌐 Circuitos</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="sb-circuit-stats">
                <div class="sb-circuit-item">
                    <span class="sb-circuit-icon">📡</span>
                    <span class="sb-circuit-label">MPLS</span>
                    <span class="sb-circuit-value">{com_mpls}</span>
                </div>
                <div class="sb-circuit-item">
                    <span class="sb-circuit-icon">🔗</span>
                    <span class="sb-circuit-label">INN</span>
                    <span class="sb-circuit-value">{com_inn}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='sb-divider-light'></div>", unsafe_allow_html=True)

        # ── Navegação ───────────────────────────────────────────────────────────────
        st.markdown("<div class='sb-section-label'>📌 Menu</div>", unsafe_allow_html=True)

        for icon, nome, cor in _MENU:
            ativo = pagina_atual == nome
            if ativo:
                st.markdown('<div class="nav-active-marker"></div>', unsafe_allow_html=True)
            
            btn_key = f"navbtn_{nome}"
            if st.button(f"{icon}  {nome}", key=btn_key, use_container_width=True):
                st.session_state.nav_page = nome
                st.rerun()

        st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

        # ── Favoritos ────────────────────────────────────────────────────────────────
        if favoritos:
            st.markdown("<div class='sb-section-label'>⭐ Favoritos</div>", unsafe_allow_html=True)
            idx = {l.get("vd"): l for l in lojas} if lojas else {}
            
            for vd in favoritos[:5]:
                loja = idx.get(vd)
                if loja:
                    nome_curto = loja.get("nome", "")[:18] + "…" if len(loja.get("nome", "")) > 18 else loja.get("nome", "")
                    status = loja.get("status", "closed")
                    
                    st.markdown(
                        f'''
                        <div class="sb-fav-item">
                            <span class="sb-fav-vd">{vd}</span>
                            <span class="sb-fav-nome">{nome_curto}</span>
                            <span class="sb-fav-status">{_get_status_emoji(status)}</span>
                        </div>
                        ''',
                        unsafe_allow_html=True,
                    )
            st.markdown("<div class='sb-divider-light'></div>", unsafe_allow_html=True)

        # ── Contatos Rápidos ───────────────────────────────────────────────────────
        st.markdown("<div class='sb-section-label'>📞 Contatos</div>", unsafe_allow_html=True)
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
                <a href="#" class="sb-contact-item">
                    <div class="sb-contact-icon">🚨</div>
                    <div>
                        <div class="sb-contact-name">Emergências</div>
                        <div class="sb-contact-tel">24 horas</div>
                    </div>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return pagina_atual
        
    except Exception as e:
        st.error(f"⚠️ Erro na sidebar: {str(e)}")
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
