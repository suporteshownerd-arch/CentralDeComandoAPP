"""
Página de Dashboard
Central de Comando DPSP v2.2
Robusta com tratamento de erros
"""

import streamlit as st
import pandas as pd


def render_page(data_loader, lojas):
    """Renderiza a página de Dashboard"""
    
    st.markdown("## 📈 Dashboard")
    st.markdown("*Visão geral das operações*")
    
    # Obter DataFrame com segurança
    try:
        df = data_loader.get_df()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        df = pd.DataFrame()
    
    # KPIs principais
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        if df is not None and not df.empty:
            with col1:
                st.metric("Total Lojas", len(df))
            with col2:
                ativas = len(df[df['status'] == 'open']) if 'status' in df.columns else len(df)
                st.metric("Lojas Ativas", ativas)
            with col3:
                inativas = len(df[df['status'] == 'closed']) if 'status' in df.columns else 0
                st.metric("Lojas Inativas", inativas)
            with col4:
                if 'estado' in df.columns:
                    st.metric("Estados", df['estado'].nunique())
                else:
                    st.metric("MTTR Médio", "N/A")
        else:
            with col1:
                st.metric("Total Lojas", len(lojas) if lojas else 0)
            with col2:
                st.metric("Lojas Ativas", 0)
            with col3:
                st.metric("Lojas Inativas", 0)
            with col4:
                st.metric("MTTR Médio", "N/A")
    except Exception as e:
        st.error(f"Erro ao carregar KPIs: {e}")
    
    st.markdown("---")
    
    # Gráficos
    try:
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            if df is not None and not df.empty and 'estado' in df.columns:
                render_grafico_estado(df)
            else:
                st.info("Dados de estado não disponíveis")
        
        with col_g2:
            if df is not None and not df.empty and 'status' in df.columns:
                render_grafico_status(df)
            else:
                st.info("Dados de status não disponíveis")
    except Exception as e:
        st.error(f"Erro ao renderizar gráficos: {e}")
    
    st.markdown("---")
    
    # Histórico de uso
    try:
        stats = data_loader.usage_logger.get_stats() if hasattr(data_loader, 'usage_logger') else {}
        
        st.markdown("### 📈 Histórico de Uso (7 dias)")
        
        col_h1, col_h2, col_h3 = st.columns(3)
        with col_h1:
            st.metric("Total Buscas", stats.get("buscas", 0))
        with col_h2:
            st.metric("Total Chamados", stats.get("chamados", 0))
        with col_h3:
            st.metric("Usuários Únicos", stats.get("usuarios", 0))
    except Exception:
        pass


def render_grafico_estado(df: pd.DataFrame):
    """Renderiza gráfico de lojas por estado"""
    st.markdown("### 🏪 Lojas por Estado")
    
    try:
        if 'estado' not in df.columns:
            st.warning("Coluna Estado não encontrada")
            return
        
        estado_counts = df['estado'].value_counts().head(10).reset_index()
        estado_counts.columns = ['Estado', 'Quantidade']
        
        st.bar_chart(estado_counts.set_index('Estado')['Quantidade'])
        
    except Exception as e:
        st.error(f"Erro no gráfico: {e}")


def render_grafico_status(df: pd.DataFrame):
    """Renderiza gráfico de status das lojas"""
    st.markdown("### 📊 Status das Lojas")
    
    try:
        if 'status' not in df.columns:
            st.warning("Coluna Status não encontrada")
            return
        
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Quantidade']
        
        status_labels = {'open': 'Ativas', 'closed': 'Inativas'}
        status_counts['Status'] = status_counts['Status'].map(status_labels).fillna(status_counts['Status'])
        
        st.bar_chart(status_counts.set_index('Status')['Quantidade'])
        
    except Exception as e:
        st.error(f"Erro no gráfico: {e}")