"""
Módulo de navegação e layout
Central de Comando DPSP v2.0
"""

import streamlit as st
from typing import List, Dict
from .ui import (
    render_sidebar_logo,
    render_status_indicator,
    render_kpi_card,
    render_contact_card
)


def render_sidebar(
    lojas: List[dict],
    favoritos: List[str],
    kpi_data: Dict = None,
    menu_itens: List[str] = None
) -> str:
    """
    Renderiza a sidebar completa
    
    Args:
        lojas: Lista de lojas
        favoritos: Lista de VDs favoritos
        kpi_data: Dados dos KPIs
        menu_itens: Itens do menu
    
    Returns:
        Nome do item selecionado
    """
    if menu_itens is None:
        menu_itens = [
            "🏪 Consulta de Lojas",
            "⚠️ Gestão de Crises",
            "📋 Histórico",
            "📞 Abertura de Chamados",
            "📈 Dashboard",
            "❓ Ajuda"
        ]
    
    st.markdown(render_sidebar_logo(), unsafe_allow_html=True)
    st.markdown(render_status_indicator("Sistema operacional"), unsafe_allow_html=True)
    st.markdown("---")

    # KPIs reais das lojas
    total_lojas  = len(lojas)
    lojas_ativas = sum(1 for l in lojas if l.get("status") == "open")
    pct = round(lojas_ativas / total_lojas * 100) if total_lojas else 0
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.markdown(render_kpi_card("Total", str(total_lojas), color="var(--accent)"), unsafe_allow_html=True)
    with col_k2:
        st.markdown(render_kpi_card("Ativas", f"{lojas_ativas} ({pct}%)", color="var(--green)"), unsafe_allow_html=True)

    st.markdown("---")
    
    menu = st.radio("Navegação", menu_itens)
    
    st.markdown("---")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Total Lojas", len(lojas))
    with col_s2:
        abertas = len([l for l in lojas if l.get('status') == 'open'])
        st.metric("Abertas", abertas)
    
    st.markdown("---")
    
    st.markdown("**📞 Contatos**")
    st.markdown(render_contact_card([
        {"icon": "📞", "label": "T.I. DPSP", "value": "(11) 5529-6003"},
        {"icon": "🎛️", "label": "Central", "value": "(11) 3274-7527"}
    ]), unsafe_allow_html=True)
    
    if favoritos:
        st.markdown("---")
        st.markdown("**⭐ Favoritos**")
        for fav in favoritos[:5]:
            st.markdown(f"- VD {fav}")
    
    return menu.split(" ", 1)[1] if " " in menu else menu


def render_page_header(title: str, subtitle: str = None, icon: str = None):
    """Renderiza cabeçalho de página"""
    if icon:
        title = f"{icon} {title}"
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")


def render_footer():
    """Renderiza rodapé do sistema"""
    st.markdown("""
    <div class="footer">
        <p><b>🛡️ Central de Comando DPSP v2.0</b></p>
        <p>Desenvolvido por Enzo Maranho - T.I. DPSP · Uso Interno</p>
    </div>
    """, unsafe_allow_html=True)


def init_session_state():
    """Inicializa states da sessão"""
    defaults = {
        'loja_selecionada': None,
        'loja_email': None,
        'historico_offset': 0,
        'nome_atendente': "",
        'favoritos': [],
        'loading': False,
        'suggestions': [],
        'kpi_data': {
            'buscas_hoje': 47,
            'chamados_hoje': 12,
            'crises_ativas': 2,
            'mttr_medio': '32min',
            'lojas_online': 156,
            'lojas_total': 162
        },
        'busca_validada': None,
        'termo_selecionado': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def setup_page_config():
    """Configura a página do Streamlit"""
    st.set_page_config(
        page_title="Central de Comando - DPSP",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )