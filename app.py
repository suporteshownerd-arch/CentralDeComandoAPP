"""
Central de Comando DPSP — v5.0
Desenvolvido por Enzo Maranho - T.I. DPSP
"""

import os
import logging
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from components import (
    setup_page_config,
    render_styles,
    render_sidebar,
    init_session_state,
    render_footer,
)
from components.error_handler import ErrorHandler, handle_errors, render_error_page
from data.loader import DataLoader
from utils.sheets import GoogleSheetsManager
import pg.consulta_lojas as pg_consulta
import pg.gestao_crises as pg_crises
import pg.abertura_chamados as pg_chamados
import pg.historico as pg_historico
import pg.dashboard as pg_dashboard
import pg.ajuda as pg_ajuda

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_page_config():
    st.set_page_config(
        page_title="Central de Comando — DPSP",
        page_icon="🛡️",
        layout="wide",
    )


@st.cache_resource(show_spinner=False)
def get_data_loader() -> DataLoader:
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_dir = os.path.join(base_dir, "data")
        raw_key = os.environ.get("MASTER_KEY", "")
        master_key = raw_key.encode() if raw_key else None
        return DataLoader(data_dir=csv_dir, master_key=master_key)
    except Exception as e:
        logger.error(f"Erro ao criar DataLoader: {e}")
        return None


@st.cache_resource(show_spinner=False)
def get_sheets_manager() -> GoogleSheetsManager:
    try:
        return GoogleSheetsManager()
    except Exception as e:
        logger.error(f"Erro ao criar SheetsManager: {e}")
        return None


@handle_errors(title="Erro ao carregar dados", show_trace=False)
def load_lojas_data(loader: DataLoader):
    if loader is None:
        return []
    return loader.get_lojas()


def render_home_page(lojas):
    """Página inicial com logo, feed e menu"""
    
    # ═══════════════════════════════════════════════════════════════════════
    # HEADER COM LOGO
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        margin-bottom: 30px;
    ">
        <div style="font-size: 80px; margin-bottom: 20px;">🛡️</div>
        <div style="
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        ">Central de Comando</div>
        <div style="
            font-size: 16px;
            color: #888;
        ">DPSP T.I. • Sistema de Gestão de Lojas</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════
    # FEED / ESTATÍSTICAS
    # ═══════════════════════════════════════════════════════════════════════
    if lojas:
        total = len(lojas)
        ativas = sum(1 for l in lojas if l.get("status") == "open")
        inativas = total - ativas
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🏪 Total de Lojas", total)
        with col2:
            st.metric("✅ Lojas Ativas", ativas, f"{round(ativas/total*100)}%")
        with col3:
            st.metric("❌ Lojas Inativas", inativas, f"{round(inativas/total*100)}%")
        with col4:
            estados = len({l.get("estado") for l in lojas if l.get("estado")})
            st.metric("🗺️ Estados", estados)
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════════════
    # MENU DE PÁGINAS
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("### 📌 O que você quer fazer?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏪 Consulta de Lojas", use_container_width=True, type="primary"):
            st.session_state.nav_page = "🏪 Buscar uma loja"
            st.rerun()
        
        if st.button("🚨 Gestão de Crises", use_container_width=True):
            st.session_state.nav_page = "🚨 Registrar uma crise"
            st.rerun()
        
        if st.button("📞 Abertura de Chamados", use_container_width=True):
            st.session_state.nav_page = "📞 Abrir chamado na Vivo/Claro"
            st.rerun()
    
    with col2:
        if st.button("📋 Histórico", use_container_width=True):
            st.session_state.nav_page = "📋 Ver histórico de alertas"
            st.rerun()
        
        if st.button("📈 Dashboard", use_container_width=True):
            st.session_state.nav_page = "📈 Ver gráficos do parque"
            st.rerun()
        
        if st.button("❓ Ajuda", use_container_width=True):
            st.session_state.nav_page = "❓ Ajuda e manual"
            st.rerun()
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════════════
    # CONTATO
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown("### 📞 Precisa de ajuda?")
    st.info("📞 Ligue: (11) 3274-7527")


def main():
    setup_page_config()
    render_styles()
    init_session_state()
    
    # Carrega dados
    try:
        loader = get_data_loader()
        sheets = get_sheets_manager()
    except Exception as e:
        logger.error(f"Erro ao inicializar serviços: {e}")
        st.error("Erro ao carregar serviços")
        return

    if "lojas" not in st.session_state:
        try:
            with st.spinner("Carregando dados..."):
                st.session_state.lojas = load_lojas_data(loader)
        except Exception as e:
            logger.error(f"Erro ao carregar lojas: {e}")
            st.session_state.lojas = []
    
    lojas = st.session_state.get("lojas", [])
    
    # Renderiza página inicial
    render_home_page(lojas)
    
    # Processa navegação se mudou
    pagina = st.session_state.get("nav_page", "")
    
    try:
        if "🏪" in pagina:
            pg_consulta.render_page(loader, lojas)
        elif "🚨" in pagina:
            pg_crises.render_page(sheets, lojas)
        elif "📞" in pagina:
            pg_chamados.render_page(lojas)
        elif "📋" in pagina:
            pg_historico.render_page(sheets)
        elif "📈" in pagina:
            pg_dashboard.render_page(loader, lojas)
        elif "❓" in pagina:
            pg_ajuda.render_page()
    except Exception as e:
        logger.error(f"Erro ao renderizar página: {e}")
        render_error_page("generic")
    
    try:
        render_footer()
    except Exception as e:
        logger.error(f"Erro no footer: {e}")


if __name__ == "__main__":
    main()
