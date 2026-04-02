"""
Central de Comando DPSP - Aplicação Principal v2.0
Desenvolvido por Enzo Maranho - T.I. DPSP
Refatorado com arquitetura modular
"""

import streamlit as st

# Importar componentes
from components import (
    render_styles,
    init_session_state,
    setup_page_config
)
from data.loader import DataLoader
from utils.sheets import GoogleSheetsManager
from pages import (
    render_consulta_lojas,
    render_gestao_crises,
    render_historico,
    render_abertura_chamados,
    render_dashboard,
    render_ajuda
)
from components.nav import render_sidebar, render_footer


def main():
    """Função principal da aplicação"""
    
    # Configuração inicial
    setup_page_config()
    render_styles()
    init_session_state()
    
    # Inicializar serviços
    @st.cache_resource
    def get_data_loader():
        return DataLoader()
    
    @st.cache_resource
    def get_sheets_manager():
        return GoogleSheetsManager()
    
    data_loader = get_data_loader()
    sheets_manager = get_sheets_manager()
    lojas = data_loader.get_lojas()
    
    # Renderizar sidebar e obter menu
    menu_name = render_sidebar(
        lojas=lojas,
        favoritos=st.session_state.favoritos,
        kpi_data=st.session_state.kpi_data
    )
    
    # Renderizar página selecionada
    if menu_name == "Consulta de Lojas":
        render_consulta_lojas(data_loader, lojas)
    
    elif menu_name == "Gestão de Crises":
        render_gestao_crises(sheets_manager, lojas)
    
    elif menu_name == "Histórico":
        render_historico(sheets_manager)
    
    elif menu_name == "Abertura de Chamados":
        render_abertura_chamados(lojas)
    
    elif menu_name == "Dashboard":
        render_dashboard(data_loader, lojas)
    
    elif menu_name == "Ajuda":
        render_ajuda()
    
    # Renderizar rodapé
    render_footer()


if __name__ == "__main__":
    main()