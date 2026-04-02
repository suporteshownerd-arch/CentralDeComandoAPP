"""
Central de Comando DPSP - Aplicação Principal v2.3
Simplificado e estável
"""

import streamlit as st

# Componentes
from components import render_styles, init_session_state, setup_page_config
from components.nav import render_sidebar, render_footer

# Data
from data.loader_pandas import DataLoaderPandas, get_sample_data_legacy


def main():
    """Função principal da aplicação"""
    
    # Configuração inicial
    setup_page_config()
    render_styles()
    init_session_state()
    
    # Carregar dados
    lojas = get_sample_data_legacy()
    df = None
    
    try:
        @st.cache_resource
        def get_data_loader():
            return DataLoaderPandas()
        
        loader = get_data_loader()
        lojas = loader.get_lojas_list()
        df = loader.get_df()
    except Exception as e:
        st.warning(f"Usando dados de exemplo: {e}")
    
    # Sidebar
    try:
        menu_name = render_sidebar(lojas, st.session_state.favoritos, st.session_state.kpi_data)
    except:
        menu_name = "Consulta de Lojas"
    
    # Páginas
    if menu_name == "Consulta de Lojas":
        from pages.consulta_lojas import render_page
        render_page(None, lojas)
    elif menu_name == "Gestão de Crises":
        from pages.gestao_crises import render_page
        render_page(None, lojas)
    elif menu_name == "Histórico":
        from pages.historico import render_page
        render_page(None)
    elif menu_name == "Abertura de Chamados":
        from pages.abertura_chamados import render_page
        render_page(lojas)
    elif menu_name == "Dashboard":
        from pages.dashboard import render_page
        render_page(None, lojas)
    elif menu_name == "Ajuda":
        from pages.ajuda import render_page
        render_page()
    
    try:
        render_footer()
    except:
        pass


if __name__ == "__main__":
    main()