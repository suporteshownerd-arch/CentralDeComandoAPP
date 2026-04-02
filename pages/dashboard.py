"""
Página de Dashboard - Versão Estável v2.3
"""

import streamlit as st


def render_page(data_loader, lojas):
    """Renderiza a página de Dashboard"""
    
    st.markdown("## 📈 Dashboard")
    st.markdown("*Visão geral das operações*")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Lojas", len(lojas) if lojas else 0)
    with col2:
        ativas = len([l for l in lojas if l.get('status') == 'open']) if lojas else 0
        st.metric("Lojas Ativas", ativas)
    with col3:
        inativas = len([l for l in lojas if l.get('status') == 'closed']) if lojas else 0
        st.metric("Lojas Inativas", inativas)
    with col4:
        estados = set(l.get('estado') for l in lojas if l.get('estado'))
        st.metric("Estados", len(estados))
    
    st.markdown("---")
    
    # Lojas por estado
    st.markdown("### Lojas por Estado")
    
    estados_dict = {}
    for loja in (lojas or []):
        est = loja.get('estado', 'Outro')
        estados_dict[est] = estados_dict.get(est, 0) + 1
    
    for estado, count in sorted(estados_dict.items(), key=lambda x: x[1], reverse=True):
        st.write(f"{estado}: {count}")