"""
Central de Comando DPSP - Aplicação Principal v2.2
Desenvolvido por Enzo Maranho - T.I. DPSP
Com tratamento de erros robusto
"""

import streamlit as st

# Importar componentes
from components import (
    render_styles,
    init_session_state,
    setup_page_config
)

# Importar data loader
from data.loader_pandas import DataLoaderPandas, get_sample_data_legacy
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
    
    # Inicializar serviços com tratamento de erros
    data_loader = None
    lojas = []
    df = None
    
    try:
        @st.cache_resource
        def get_data_loader():
            return DataLoaderPandas()
        
        data_loader = get_data_loader()
        lojas = data_loader.get_lojas_list()
        
        try:
            df = data_loader.get_df()
            stats = data_loader.get_estatisticas()
            if stats.get('total', 0) > 0:
                st.session_state.kpi_data['lojas_online'] = stats.get('ativas', 0)
                st.session_state.kpi_data['lojas_total'] = stats.get('total', 0)
        except Exception:
            pass
            
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        # Usar dados de exemplo
        lojas = get_sample_data_legacy()
    
    sheets_manager = None
    try:
        @st.cache_resource
        def get_sheets_manager():
            return GoogleSheetsManager()
        sheets_manager = get_sheets_manager()
    except Exception:
        pass
    
    # Renderizar sidebar e obter menu
    try:
        menu_name = render_sidebar(
            lojas=lojas,
            favoritos=st.session_state.favoritos,
            kpi_data=st.session_state.kpi_data
        )
    except Exception as e:
        st.error(f"Erro na sidebar: {e}")
        menu_name = "Consulta de Lojas"
    
    # Renderizar página selecionada
    try:
        if menu_name == "Consulta de Lojas":
            render_consulta_lojas(data_loader, lojas)
        
        elif menu_name == "Gestão de Crises":
            if sheets_manager:
                render_gestao_crises(sheets_manager, lojas)
            else:
                render_gestao_crises(None, lojas)
        
        elif menu_name == "Histórico":
            if sheets_manager:
                render_historico(sheets_manager)
            else:
                st.error("Google Sheets não disponível")
        
        elif menu_name == "Abertura de Chamados":
            render_abertura_chamados(lojas)
        
        elif menu_name == "Dashboard":
            render_dashboard(data_loader, lojas)
        
        elif menu_name == "Ajuda":
            render_ajuda()
    except Exception as e:
        st.error(f"Erro ao renderizar página: {e}")
    
    # Renderizar rodapé
    try:
        render_footer()
    except Exception:
        pass


if __name__ == "__main__":
    main()