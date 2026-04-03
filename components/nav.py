"""
Módulo de navegação e sidebar
Central de Comando DPSP v4.4
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


def _get_status_emoji(status: str) -> str:
    """Retorna emoji baseado no status"""
    if status == "open":
        return "🟢"
    elif status == "pending":
        return "🟡"
    return "🔴"


def _get_status_color(status: str) -> str:
    """Retorna cor baseada no status"""
    if status == "open":
        return "#10b981"
    elif status == "pending":
        return "#f59e0b"
    return "#ef4444"


def _calculate_metrics(lojas: List[dict]) -> Dict:
    """Calcula métricas detalhadas do parque"""
    if not lojas:
        return {}
    
    total = len(lojas)
    ativas = sum(1 for l in lojas if l.get("status") == "open")
    inativas = total - ativas
    pending = sum(1 for l in lojas if l.get("status") == "pending")
    
    bandeiras = {}
    for l in lojas:
        b = l.get("bandeira", "Outros")
        bandeiras[b] = bandeiras.get(b, 0) + 1
    
    com_mpls = sum(1 for l in lojas if l.get("mpls"))
    com_inn = sum(1 for l in lojas if l.get("inn"))
    
    regioes = {}
    for l in lojas:
        r = l.get("regiao", "Outros")
        regioes[r] = regioes.get(r, 0) + 1
    
    estados = {}
    for l in lojas:
        e = l.get("estado", "Outros")
        estados[e] = estados.get(e, 0) + 1
    
    return {
        "total": total,
        "ativas": ativas,
        "inativas": inativas,
        "pending": pending,
        "pct_ativas": round(ativas / total * 100) if total else 0,
        "bandeiras": bandeiras,
        "regioes": regioes,
        "estados": estados,
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

        # ═══════════════════════════════════════════════════════════════════════
        # 1. HEADER - Logo e Status
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown(
            """
            <div class="sb-header">
                <div class="sb-logo">
                    <div class="sb-logo-icon">🛡️</div>
                    <div>
                        <div class="sb-logo-title">Central de Comando</div>
                        <div class="sb-logo-sub">DPSP T.I. · v4.4</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Status com horário
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
        
        # ═══════════════════════════════════════════════════════════════════════
        # 2. VISÃO GERAL - KPIs
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sb-section-label'>📊 VISÃO GERAL</div>", unsafe_allow_html=True)
        
        # KPI Cards em linha
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"""<div class="sb-kpi-card green"><div class="sb-kpi-value">{ativas}</div><div class="sb-kpi-label">Ativas</div></div>""",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""<div class="sb-kpi-card red"><div class="sb-kpi-value">{inativas}</div><div class="sb-kpi-label">Inativas</div></div>""",
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f"""<div class="sb-kpi-card accent"><div class="sb-kpi-value">{total}</div><div class="sb-kpi-label">Total</div></div>""",
                unsafe_allow_html=True,
            )
        
        # Barra de progresso
        st.markdown(
            f"""
            <div class="sb-progress-container">
                <div class="sb-progress-bar">
                    <div class="sb-progress-fill" style="width:{pct}%"></div>
                </div>
                <div class="sb-progress-text">{pct}% das lojas ativas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # 3. DISTRIBUIÇÃO
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sb-section-label'>📈 DISTRIBUIÇÃO</div>", unsafe_allow_html=True)
        
        # Por Bandeira
        bandeiras = metrics.get("bandeiras", {})
        if bandeiras:
            st.markdown("<div class='sb-subsection-label'>Por Bandeira</div>", unsafe_allow_html=True)
            cores_bandeira = {"DSP": "#6366f1", "D1": "#10b981", "DPR": "#f59e0b", "P": "#a855f7"}
            
            for band, qtd in sorted(bandeiras.items(), key=lambda x: x[1], reverse=True)[:4]:
                pct_b = round(qtd/total*100) if total else 0
                cor = cores_bandeira.get(band, "#a0a0b0")
                st.markdown(
                    f'''
                    <div class="sb-dist-item">
                        <span class="sb-dist-dot" style="background:{cor}"></span>
                        <span class="sb-dist-name">{band}</span>
                        <div class="sb-dist-bar"><div class="sb-dist-fill" style="width:{pct_b}%;background:{cor}"></div></div>
                        <span class="sb-dist-pct">{pct_b}%</span>
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )
        
        # Por Estado (Top 5)
        estados = metrics.get("estados", {})
        if estados and len(estados) > 1:
            st.markdown("<div class='sb-subsection-label'>Por Estado (Top 5)</div>", unsafe_allow_html=True)
            
            top_estados = sorted(estados.items(), key=lambda x: x[1], reverse=True)[:5]
            for est, qtd in top_estados:
                pct_e = round(qtd/total*100) if total else 0
                st.markdown(
                    f'''
                    <div class="sb-dist-item">
                        <span class="sb-dist-icon">🗺️</span>
                        <span class="sb-dist-name">{est}</span>
                        <div class="sb-dist-bar"><div class="sb-dist-fill" style="width:{pct_e}%;background:var(--accent)"></div></div>
                        <span class="sb-dist-pct">{qtd}</span>
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )
        
        st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # 4. CONECTIVIDADE
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sb-section-label'>🌐 CONECTIVIDADE</div>", unsafe_allow_html=True)
        
        com_mpls = metrics.get("com_mpls", 0)
        com_inn = metrics.get("com_inn", 0)
        pct_mpls = round(com_mpls/total*100) if total else 0
        pct_inn = round(com_inn/total*100) if total else 0
        
        st.markdown(
            f'''
            <div class="sb-connect-grid">
                <div class="sb-connect-item">
                    <div class="sb-connect-icon">📡</div>
                    <div class="sb-connect-info">
                        <span class="sb-connect-label">MPLS</span>
                        <span class="sb-connect-value">{com_mpls} ({pct_mpls}%)</span>
                    </div>
                </div>
                <div class="sb-connect-item">
                    <div class="sb-connect-icon">🔗</div>
                    <div class="sb-connect-info">
                        <span class="sb-connect-label">INN</span>
                        <span class="sb-connect-value">{com_inn} ({pct_inn}%)</span>
                    </div>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        
        # Barra de conectividade total
        pct_conectado = round((com_mpls + com_inn)/total*100) if total else 0
        st.markdown(
            f'''
            <div class="sb-connect-bar">
                <span>Total conectados: {pct_conectado}%</span>
                <div class="sb-connect-progress"><div style="width:{pct_conectado}%"></div></div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        
        st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # 5. NAVEGAÇÃO
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sb-section-label'>📌 NAVEGAÇÃO</div>", unsafe_allow_html=True)

        for icon, nome, cor in _MENU:
            ativo = pagina_atual == nome
            if ativo:
                st.markdown('<div class="nav-active-marker"></div>', unsafe_allow_html=True)
            
            btn_key = f"navbtn_{nome}"
            if st.button(f"{icon}  {nome}", key=btn_key, use_container_width=True):
                st.session_state.nav_page = nome
                st.rerun()

        st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # 6. FAVORITOS
        # ═══════════════════════════════════════════════════════════════════════
        if favoritos:
            st.markdown("<div class='sb-section-label'>⭐ FAVORITOS</div>", unsafe_allow_html=True)
            idx = {l.get("vd"): l for l in lojas} if lojas else {}
            
            for vd in favoritos[:5]:
                loja = idx.get(vd)
                if loja:
                    nome_curto = loja.get("nome", "")[:20] + "…" if len(loja.get("nome", "")) > 20 else loja.get("nome", "")
                    status = loja.get("status", "closed")
                    status_cor = _get_status_color(status)
                    
                    st.markdown(
                        f'''
                        <div class="sb-fav-item">
                            <span class="sb-fav-vd">{vd}</span>
                            <span class="sb-fav-nome">{nome_curto}</span>
                            <span class="sb-fav-status" style="color:{status_cor}">●</span>
                        </div>
                        ''',
                        unsafe_allow_html=True,
                    )
            st.markdown("<div class='sb-divider'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # 7. CONTATOS
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sb-section-label'>📞 CONTATOS</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="sb-contacts">
                <a href="https://wa.me/551132747527" target="_blank" class="sb-contact-item">
                    <div class="sb-contact-icon">🎛️</div>
                    <div><div class="sb-contact-name">Central de Comando</div>
                    <div class="sb-contact-tel">(11) 3274-7527</div></div>
                </a>
                <a href="https://wa.me/551155296003" target="_blank" class="sb-contact-item">
                    <div class="sb-contact-icon">💻</div>
                    <div><div class="sb-contact-name">T.I. DPSP</div>
                    <div class="sb-contact-tel">(11) 5529-6003</div></div>
                </a>
                <a href="#" class="sb-contact-item">
                    <div class="sb-contact-icon">🚨</div>
                    <div><div class="sb-contact-name">Emergências</div>
                    <div class="sb-contact-tel">24 horas</div></div>
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
