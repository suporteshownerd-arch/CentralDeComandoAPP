"""
Página de Dashboard
Central de Comando DPSP v2.1
Com Gráficos Plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components import render_kpi_card


def render_page(data_loader, lojas):
    """Renderiza a página de Dashboard"""
    st.markdown("## 📈 Dashboard")
    st.markdown("*Visão geral das operações*")
    
    # Obter DataFrame
    df = data_loader.get_df()
    
    # Estatísticas de uso
    stats = data_loader.usage_logger.get_stats()
    kpi = st.session_state.kpi_data
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Lojas",
            len(df) if not df.empty else kpi.get('buscas_hoje', 0)
        )
    with col2:
        ativas = len(df[df['status'] == 'open']) if not df.empty and 'status' in df.columns else kpi.get('chamados_hoje', 0)
        st.metric("Lojas Ativas", ativas)
    with col3:
        inativas = len(df[df['status'] == 'closed']) if not df.empty and 'status' in df.columns else kpi.get('crises_ativas', 0)
        st.metric("Lojas Inativas", inativas)
    with col4:
        if 'estado' in df.columns:
            st.metric("Estados", df['estado'].nunique())
        else:
            st.metric("MTTR Médio", kpi.get('mttr_medio', 'N/A'))
    
    st.markdown("---")
    
    # Gráficos
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        if not df.empty and 'estado' in df.columns:
            render_grafico_estado(df)
        else:
            st.info("Dados de estado não disponíveis")
    
    with col_g2:
        if not df.empty and 'status' in df.columns:
            render_grafico_status(df)
        else:
            render_grafico_status_fallback(kpi)
    
    st.markdown("---")
    
    # Mais gráficos
    col_g3, col_g4 = st.columns(2)
    
    with col_g3:
        if not df.empty and 'cidade' in df.columns:
            render_grafico_cidades(df)
    
    with col_g4:
        if not df.empty:
            render_grafico_tipo_loja(df)
    
    st.markdown("---")
    
    # Tabela de lojas por região
    if not df.empty:
        render_tabela_regioes(df)
    
    # Histórico de uso
    render_historico_uso(stats)


def render_grafico_estado(df: pd.DataFrame):
    """Renderiza gráfico de lojas por estado"""
    st.markdown("### 🏪 Lojas por Estado")
    
    if 'estado' not in df.columns:
        st.warning("Coluna Estado não encontrada")
        return
    
    estado_counts = df['estado'].value_counts().reset_index()
    estado_counts.columns = ['Estado', 'Quantidade']
    
    fig = px.bar(
        estado_counts,
        x='Estado',
        y='Quantidade',
        title="Lojas por Estado",
        color='Quantidade',
        color_continuous_scale='Blues',
        text='Quantidade'
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#eaecf0',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_grafico_status(df: pd.DataFrame):
    """Renderiza gráfico de status das lojas"""
    st.markdown("### 📊 Status das Lojas")
    
    if 'status' not in df.columns:
        st.warning("Coluna Status não encontrada")
        return
    
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Quantidade']
    
    status_labels = {'open': 'Ativas', 'closed': 'Inativas'}
    status_counts['Status'] = status_counts['Status'].map(status_labels).fillna(status_counts['Status'])
    
    colors = {'Ativas': '#34d399', 'Inativas': '#f87171'}
    
    fig = px.pie(
        status_counts,
        names='Status',
        values='Quantidade',
        title="Lojas Ativas vs Inativas",
        color='Status',
        color_discrete_map=colors,
        hole=0.4
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#eaecf0'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_grafico_status_fallback(kpi: dict):
    """Renderiza gráfico de status com dados fallback"""
    st.markdown("### 📊 Status das Lojas")
    
    labels = ['Ativas', 'Inativas']
    valores = [kpi.get('lojas_online', 100), kpi.get('lojas_total', 162) - kpi.get('lojas_online', 100)]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.4,
        marker=dict(colors=['#34d399', '#f87171'])
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#eaecf0'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_grafico_cidades(df: pd.DataFrame):
    """Renderiza gráfico das principais cidades"""
    st.markdown("### 🏙️ Top Cidades")
    
    if 'cidade' not in df.columns:
        st.warning("Coluna Cidade não encontrada")
        return
    
    cidade_counts = df['cidade'].value_counts().head(10).reset_index()
    cidade_counts.columns = ['Cidade', 'Quantidade']
    
    fig = px.bar(
        cidade_counts,
        x='Quantidade',
        y='Cidade',
        orientation='h',
        title="Top 10 Cidades",
        color='Quantidade',
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#eaecf0',
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_grafico_tipo_loja(df: pd.DataFrame):
    """Renderiza gráfico de tipo de loja"""
    st.markdown("### 🏪 Tipos de Loja")
    
    tipo_col = 'tipo_loja' if 'tipo_loja' in df.columns else 'TIPO LOJA'
    
    if tipo_col not in df.columns:
        st.warning("Coluna Tipo de Loja não encontrada")
        return
    
    tipo_counts = df[tipo_col].value_counts().head(8).reset_index()
    tipo_counts.columns = ['Tipo', 'Quantidade']
    
    fig = px.pie(
        tipo_counts,
        names='Tipo',
        values='Quantidade',
        title="Tipos de Loja"
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#eaecf0'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_tabela_regioes(df: pd.DataFrame):
    """Renderiza tabela de lojas por região/estado"""
    st.markdown("### 📋 Lojas por Região")
    
    if 'estado' not in df.columns:
        return
    
    regiao_df = df.groupby('estado').agg({
        'vd': 'count',
        'nome': 'first'
    }).reset_index()
    
    regiao_df.columns = ['Estado', 'Total Lojas', 'Exemplo']
    
    col_vis1, col_vis2 = st.columns([3, 1])
    
    with col_vis1:
        st.dataframe(
            regiao_df.sort_values('Total Lojas', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    
    with col_vis2:
        st.metric("Média por Estado", f"{regiao_df['Total Lojas'].mean():.0f}")


def render_historico_uso(stats: dict):
    """Renderiza histórico de uso"""
    st.markdown("### 📈 Histórico de Uso (7 dias)")
    
    col_h1, col_h2, col_h3 = st.columns(3)
    
    with col_h1:
        st.metric("Total Buscas", stats.get("buscas", 0))
    with col_h2:
        st.metric("Total Chamados", stats.get("chamados", 0))
    with col_h3:
        st.metric("Usuários Únicos", stats.get("usuarios", 0))