"""
Central de Comando DPSP — v3.0
Desenvolvido por Enzo Maranho - T.I. DPSP
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env (se existir)
load_dotenv()

# Importações dos módulos locais
from components import (
    setup_page_config,
    render_styles,
    render_sidebar,
    init_session_state,
    render_footer,
)
from data.loader import DataLoader
from utils.sheets import GoogleSheetsManager
import pages.consulta_lojas as pg_consulta
import pages.gestao_crises as pg_crises
import pages.abertura_chamados as pg_chamados
import pages.historico as pg_historico
import pages.dashboard as pg_dashboard
import pages.ajuda as pg_ajuda


# ── Configuração da página ─────────────────────────────────────────────────
setup_page_config()
render_styles()
init_session_state()


# ── Inicialização do DataLoader ────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_data_loader() -> DataLoader:
    """Cria e devolve um DataLoader singleton com o path correto dos CSVs."""
    # Tenta encontrar o diretório de CSVs relativo ao app ou ao projeto
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidatos = [
        os.path.join(base_dir, "..", "consulta lojas python", "csvs"),
        os.path.join(base_dir, "data"),
    ]
    csv_dir = next((p for p in candidatos if os.path.isdir(p)), os.path.join(base_dir, "data"))

    master_key = os.environ.get("MASTER_KEY", "")
    if master_key and isinstance(master_key, str):
        master_key = master_key.encode()

    return DataLoader(data_dir=csv_dir, master_key=master_key or None)


@st.cache_resource(show_spinner=False)
def get_sheets_manager() -> GoogleSheetsManager:
    """Cria e devolve um GoogleSheetsManager singleton."""
    return GoogleSheetsManager()


# ── Carregamento de dados ──────────────────────────────────────────────────
def load_lojas(loader: DataLoader):
    """Carrega lojas com spinner de feedback."""
    with st.spinner("Carregando dados das lojas..."):
        return loader.get_lojas()


# ── Roteamento de páginas ──────────────────────────────────────────────────
def main():
    loader = get_data_loader()
    sheets = get_sheets_manager()

    # Carrega lojas uma vez por sessão
    if "lojas" not in st.session_state:
        st.session_state.lojas = load_lojas(loader)

    lojas = st.session_state.lojas

    # KPI data para a sidebar
    kpi_data = {
        "buscas_hoje": st.session_state.get("buscas_hoje", 0),
        "chamados_hoje": st.session_state.get("chamados_hoje", 0),
        "crises_ativas": st.session_state.get("crises_ativas", 0),
        "lojas_online": len([l for l in lojas if l.get("status") == "open"]),
        "lojas_total": len(lojas),
    }

    # Sidebar — retorna nome da página selecionada
    with st.sidebar:
        pagina = render_sidebar(
            lojas=lojas,
            favoritos=st.session_state.get("favoritos", []),
            kpi_data=kpi_data,
        )

    # Roteamento
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
