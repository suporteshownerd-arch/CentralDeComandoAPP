"""
Módulo de navegação e sidebar
Central de Comando DPSP - Bonito e Moderno
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
    
    # ═══════════════════════════════════════════════════════════════════════
    # HEADER
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        margin: -10px -1rem 20px -1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    ">
        <div style="font-size: 40px; margin-bottom: 8px;">🛡️</div>
        <div style="
            font-family: 'Arial', sans-serif;
            font-size: 22px;
            font-weight: bold;
            color: #fff;
            letter-spacing: 1px;
        ">Central de Comando</div>
        <div style="
            font-family: monospace;
            font-size: 11px;
            color: #888;
            margin-top: 4px;
        ">DPSP T.I. • Sistema de Gestão</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════
    # MENU COM BOTÕES BONITOS
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("### 📂 Páginas")
    
    cores = {
        "Consulta de Lojas": "#6366f1",
        "Gestão de Crises": "#ef4444", 
        "Abertura de Chamados": "#10b981",
        "Histórico": "#a855f7",
        "Dashboard": "#f59e0b",
        "Ajuda": "#6b7280",
    }
    
    for icon, nome in _MENU:
        cor = cores.get(nome, "#6366f1")
        ativo = pagina_atual == nome
        
        # Container customizado para cada botão
        if ativo:
            st.markdown(f"""
            <div style="
                background: linear-gradient(90deg, {cor}22 0%, {cor}11 100%);
                border-left: 4px solid {cor};
                border-radius: 10px;
                padding: 2px;
                margin: 4px 0;
            ">
            """, unsafe_allow_html=True)
        
        if st.button(f"  {icon}  {nome}", key=f"nav_{nome}", use_container_width=True):
            st.session_state.nav_page = nome
            st.rerun()
        
        if ativo:
            st.markdown("</div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════
    # ESTATÍSTICAS
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("### 📊 Estatísticas")
    
    total = len(lojas) if lojas else 0
    if total > 0:
        ativas = sum(1 for l in lojas if l.get("status") == "open")
        inativas = total - ativas
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ativas", ativas, f"{round(ativas/total*100)}%", delta_color="normal")
        with col2:
            st.metric("Inativas", inativas, f"{round(inativas/total*100)}%", delta_color="inverse")
    else:
        st.info("Nenhuma loja carregada")

    # ═══════════════════════════════════════════════════════════════════════
    # CONTATO
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("### 📞 Contato")
    
    st.markdown("""
    <div style="
        background: #1e1e2e;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #333;
    ">
        <div style="font-size: 24px; margin-bottom: 8px;">🎛️</div>
        <div style="font-weight: bold; color: #fff;">Central de Comando</div>
        <div style="color: #888; font-size: 13px;">(11) 3274-7527</div>
    </div>
    """, unsafe_allow_html=True)

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
