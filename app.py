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
    
    # Sidebar
    with st.sidebar:
        try:
            pagina = render_sidebar(
                lojas=lojas,
                favoritos=st.session_state.get("favoritos", []),
            )
        except Exception as e:
            logger.error(f"Erro na sidebar: {e}")
            pagina = "🏪 Buscar uma loja"
    
    # Processa navegação se mudou
    if not pagina:
        pagina = st.session_state.get("nav_page", "")
    
    # Se nenhuma página definida, mostra home
    if not pagina:
        render_home_page(lojas)
    else:
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
            else:
                render_home_page(lojas)
        except Exception as e:
            logger.error(f"Erro ao renderizar página: {e}")
            render_error_page("generic")
    
    try:
        render_footer()
    except Exception as e:
        logger.error(f"Erro no footer: {e}")


if __name__ == "__main__":
    main()
