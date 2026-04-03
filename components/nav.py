"""
Módulo de navegação e sidebar
Central de Comando DPSP v4.5 - Premium
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


def _calculate_metrics(lojas: List[dict]) -> Dict:
    """Calcula métricas detalhadas do parque"""
    if not lojas:
        return {}
    
    total = len(lojas)
    ativas = sum(1 for l in lojas if l.get("status") == "open")
    inativas = total - ativas
    
    bandeiras = {}
    for l in lojas:
        b = l.get("bandeira", "Outros")
        bandeiras[b] = bandeiras.get(b, 0) + 1
    
    com_mpls = sum(1 for l in lojas if l.get("mpls"))
    com_inn = sum(1 for l in lojas if l.get("inn"))
    
    estados = {}
    for l in lojas:
        e = l.get("estado", "Outros")
        estados[e] = estados.get(e, 0) + 1
    
    regioes = {}
    for l in lojas:
        r = l.get("regiao", "Outros")
        regioes[r] = regioes.get(r, 0) + 1
    
    return {
        "total": total,
        "ativas": ativas,
        "inativas": inativas,
        "pct_ativas": round(ativas / total * 100) if total else 0,
        "bandeiras": bandeiras,
        "estados": estados,
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

        # ═══════════════════════════════════════════════════════════════════════
        # HEADER PREMIUM
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="sb-header-premium">
            <div class="sb-logo-premium">
                <div class="sb-logo-icon-premium">🛡️</div>
                <div class="sb-logo-text">
                    <div class="sb-logo-title-premium">Central de Comando</div>
                    <div class="sb-logo-sub-premium">DPSP T.I. · v4.5</div>
                </div>
            </div>
            <div class="sb-status-premium">
                <div class="sb-status-dot-premium"></div>
                <div>
                    <div class="sb-status-title-premium">Sistema Operacional</div>
                    <div class="sb-status-time-premium">""" + datetime.now().strftime("%H:%M") + """ · """ + ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"][datetime.now().weekday()] + """</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='sb-divider-premium'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # HERO KPI - Total de Lojas
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown(f"""
        <div class="sb-hero-kpi">
            <div class="sb-hero-label">PARQUE TOTAL</div>
            <div class="sb-hero-value">{total:,}</div>
            <div class="sb-hero-sub">lojas cadastradas</div>
            <div class="sb-hero-progress">
                <div class="sb-hero-bar"><div class="sb-hero-fill" style="width:{pct}%"></div></div>
                <div class="sb-hero-percent">{pct}% online</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # STATUS CARDS
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sb-section-premium'>📊 STATUS</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="sb-card-kpi green">
                <div class="sb-card-kpi-icon">✓</div>
                <div class="sb-card-kpi-value">{ativas}</div>
                <div class="sb-card-kpi-label">Ativas</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="sb-card-kpi red">
                <div class="sb-card-kpi-icon">✕</div>
                <div class="sb-card-kpi-value">{inativas}</div>
                <div class="sb-card-kpi-label">Inativas</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='sb-divider-premium-light'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # BANDHEIRAS COM BARRAS
        # ═══════════════════════════════════════════════════════════════════════
        bandeiras = metrics.get("bandeiras", {})
        if bandeiras:
            st.markdown("<div class='sb-section-premium'>🏷️ BANDHEIRAS</div>", unsafe_allow_html=True)
            
            cores = {"DSP": "#6366f1", "D1": "#10b981", "DPR": "#f59e0b", "P": "#a855f7", "D2": "#ec4899"}
            
            for band, qtd in sorted(bandeiras.items(), key=lambda x: x[1], reverse=True)[:5]:
                pct_b = round(qtd/total*100) if total else 0
                cor = cores.get(band, "#a0a0b0")
                st.markdown(f"""
                <div class="sb-bar-item">
                    <div class="sb-bar-header">
                        <span class="sb-bar-dot" style="background:{cor}"></span>
                        <span class="sb-bar-name">{band}</span>
                        <span class="sb-bar-value">{qtd}</span>
                    </div>
                    <div class="sb-bar-track"><div class="sb-bar-fill" style="width:{pct_b}%;background:{cor}"></div></div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<div class='sb-divider-premium-light'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # TOP ESTADOS
        # ═══════════════════════════════════════════════════════════════════════
        estados = metrics.get("estados", {})
        if estados and len(estados) > 1:
            st.markdown("<div class='sb-section-premium'>🗺️ TOP ESTADOS</div>", unsafe_allow_html=True)
            
            top = sorted(estados.items(), key=lambda x: x[1], reverse=True)[:5]
            for i, (est, qtd) in enumerate(top):
                pct_e = round(qtd/total*100) if total else 0
                st.markdown(f"""
                <div class="sb-bar-item">
                    <div class="sb-bar-header">
                        <span class="sb-bar-rank">{i+1}</span>
                        <span class="sb-bar-name">{est}</span>
                        <span class="sb-bar-value">{qtd}</span>
                    </div>
                    <div class="sb-bar-track"><div class="sb-bar-fill" style="width:{pct_e}%"></div></div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<div class='sb-divider-premium-light'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # CONECTIVIDADE
        # ═══════════════════════════════════════════════════════════════════════
        com_mpls = metrics.get("com_mpls", 0)
        com_inn = metrics.get("com_inn", 0)
        pct_mpls = round(com_mpls/total*100) if total else 0
        pct_inn = round(com_inn/total*100) if total else 0
        pct_conectado = round((com_mpls + com_inn)/total*100) if total else 0
        
        st.markdown("<div class='sb-section-premium'>🌐 CONECTIVIDADE</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="sb-connect-premium">
            <div class="sb-connect-card">
                <div class="sb-connect-icon-premium">📡</div>
                <div class="sb-connect-details">
                    <span class="sb-connect-name">MPLS</span>
                    <span class="sb-connect-num">{com_mpls}</span>
                    <span class="sb-connect-pct">{pct_mpls}%</span>
                </div>
            </div>
            <div class="sb-connect-card">
                <div class="sb-connect-icon-premium">🔗</div>
                <div class="sb-connect-details">
                    <span class="sb-connect-name">INN</span>
                    <span class="sb-connect-num">{com_inn}</span>
                    <span class="sb-connect-pct">{pct_inn}%</span>
                </div>
            </div>
        </div>
        <div class="sb-connect-total">
            <span>🔵 Total Conectado: {pct_conectado}%</span>
            <div class="sb-connect-bar"><div style="width:{pct_conectado}%"></div></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='sb-divider-premium'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # NAVEGAÇÃO
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sb-section-premium'>📌 MENU</div>", unsafe_allow_html=True)

        for icon, nome, cor in _MENU:
            ativo = pagina_atual == nome
            if ativo:
                st.markdown('<div class="nav-active-marker"></div>', unsafe_allow_html=True)
            
            btn_key = f"navbtn_{nome}"
            if st.button(f"{icon}  {nome}", key=btn_key, use_container_width=True):
                st.session_state.nav_page = nome
                st.rerun()

        st.markdown("<div class='sb-divider-premium'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # FAVORITOS
        # ═══════════════════════════════════════════════════════════════════════
        if favoritos:
            st.markdown("<div class='sb-section-premium'>⭐ FAVORITOS</div>", unsafe_allow_html=True)
            idx = {l.get("vd"): l for l in lojas} if lojas else {}
            
            for vd in favoritos[:4]:
                loja = idx.get(vd)
                if loja:
                    nome = loja.get("nome", "")[:18] + "…" if len(loja.get("nome", "")) > 18 else loja.get("nome", "")
                    status = "open"
                    cor = "#10b981" if loja.get("status") == "open" else "#ef4444"
                    
                    st.markdown(f'''
                    <div class="sb-fav-premium">
                        <span class="sb-fav-vd-premium">{vd}</span>
                        <span class="sb-fav-name-premium">{nome}</span>
                        <span class="sb-fav-status-premium" style="color:{cor}">●</span>
                    </div>
                    ''', unsafe_allow_html=True)
            st.markdown("<div class='sb-divider-premium-light'></div>", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════════
        # CONTATOS
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sb-section-premium'>📞 CONTATOS</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="sb-contacts-premium">
            <a href="https://wa.me/551132747527" target="_blank" class="sb-contact-premium">
                <span class="sb-contact-icon-premium">🎛️</span>
                <div><div class="sb-contact-name-premium">Central de Comando</div>
                <div class="sb-contact-tel-premium">(11) 3274-7527</div></div>
            </a>
            <a href="https://wa.me/551155296003" target="_blank" class="sb-contact-premium">
                <span class="sb-contact-icon-premium">💻</span>
                <div><div class="sb-contact-name-premium">T.I. DPSP</div>
                <div class="sb-contact-tel-premium">(11) 5529-6003</div></div>
            </a>
            <a href="#" class="sb-contact-premium">
                <span class="sb-contact-icon-premium">🚨</span>
                <div><div class="sb-contact-name-premium">Emergências 24h</div>
                <div class="sb-contact-tel-premium">Clique para info</div></div>
            </a>
        </div>
        """, unsafe_allow_html=True)

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
