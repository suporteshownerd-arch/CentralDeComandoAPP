"""
Página de Dashboard
Central de Comando DPSP v2.0
"""

import streamlit as st
from components import render_kpi_card


def render_page(data_loader, lojas):
    """Renderiza a página de Dashboard"""
    st.markdown("## 📈 Dashboard")
    st.markdown("*Visão geral das operações*")
    
    # Estatísticas de uso
    stats = data_loader.usage_logger.get_stats()
    kpi = st.session_state.kpi_data
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Buscas Hoje",
            stats.get("buscas", kpi['buscas_hoje']),
            "+12%",
            delta_color="normal"
        )
    with col2:
        st.metric(
            "Chamados Hoje",
            stats.get("chamados", kpi['chamados_hoje']),
            "+3%",
            delta_color="normal"
        )
    with col3:
        st.metric(
            "Crises Ativas",
            kpi['crises_ativas'],
            "-1",
            delta_color="normal"
        )
    with col4:
        st.metric(
            "MTTR Médio",
            kpi['mttr_medio'],
            "-5min",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Gráficos
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        render_lojas_por_estado(lojas)
    
    with col_d2:
        render_status_lojas(lojas)
    
    st.markdown("---")
    
    # Histórico de uso
    render_historico_uso(stats)


def render_lojas_por_estado(lojas):
    """Renderiza gráfico de lojas por estado"""
    st.markdown("### 🏪 Lojas por Estado")
    
    estados = {}
    for l in lojas:
        e = l.get('estado', 'Outro')
        estados[e] = estados.get(e, 0) + 1
    
    for estado, count in sorted(estados.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(lojas)) * 100
        st.progress(pct/100, f"{estado}: {count} ({pct:.1f}%)")


def render_status_lojas(lojas):
    """Renderiza status das lojas"""
    st.markdown("### 📊 Status das Lojas")
    
    abertas = len([l for l in lojas if l.get('status') == 'open'])
    fechadas = len([l for l in lojas if l.get('status') == 'closed'])
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Abertas", abertas)
    with col_s2:
        st.metric("Fechadas", fechadas)
    
    pct_online = (abertas / len(lojas) * 100) if len(lojas) > 0 else 0
    st.progress(pct_online/100, f"Uptime: {pct_online:.1f}%")


def render_historico_uso(stats):
    """Renderiza histórico de uso"""
    st.markdown("### 📈 Histórico de Uso (7 dias)")
    
    col_h1, col_h2, col_h3 = st.columns(3)
    
    with col_h1:
        st.metric("Total Buscas", stats.get("buscas", 0))
    with col_h2:
        st.metric("Total Chamados", stats.get("chamados", 0))
    with col_h3:
        st.metric("Usuários Únicos", stats.get("usuarios", 0))