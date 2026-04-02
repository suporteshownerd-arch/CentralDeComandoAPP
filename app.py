"""
Central de Comando DPSP — v3.0
Desenvolvido por Enzo Maranho - T.I. DPSP
"""

import os
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
from data.loader import DataLoader
from utils.sheets import GoogleSheetsManager
import pg.consulta_lojas as pg_consulta
import pg.gestao_crises as pg_crises
import pg.abertura_chamados as pg_chamados
import pg.historico as pg_historico
import pg.dashboard as pg_dashboard
import pg.ajuda as pg_ajuda

setup_page_config()
render_styles()
init_session_state()


@st.cache_resource(show_spinner=False)
def get_data_loader() -> DataLoader:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir  = os.path.join(base_dir, "data")

    raw_key = os.environ.get("MASTER_KEY", "")
    master_key = raw_key.encode() if raw_key else None

    return DataLoader(data_dir=csv_dir, master_key=master_key)


@st.cache_resource(show_spinner=False)
def get_sheets_manager() -> GoogleSheetsManager:
    return GoogleSheetsManager()


def main():
    loader = get_data_loader()
    sheets = get_sheets_manager()

    if "lojas" not in st.session_state:
        with st.spinner("Carregando dados das lojas..."):
            st.session_state.lojas = loader.get_lojas()

    lojas = st.session_state.lojas

    with st.sidebar:
        pagina = render_sidebar(
            lojas=lojas,
            favoritos=st.session_state.get("favoritos", []),
        )

    if "Consulta" in pagina:
        pg_consulta.render_page(loader, lojas)
    elif "Crises" in pagina or "Gestão" in pagina:
        pg_crises.render_page(sheets, lojas)
    elif "Chamados" in pagina:
        pg_chamados.render_page(lojas)
    elif "Histórico" in pagina or "Historico" in pagina:
        pg_historico.render_page(sheets)
    elif "Dashboard" in pagina:
        pg_dashboard.render_page(loader, lojas)
    elif "Ajuda" in pagina:
        pg_ajuda.render_page()
    else:
        pg_consulta.render_page(loader, lojas)

    render_footer()


if __name__ == "__main__":
    main()
