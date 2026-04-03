"""
Página Feed - Visão geral do sistema
"""

import streamlit as st


def render_page(loader, lojas):
    st.markdown("## 📊 Feed")
    st.markdown("---")
    
    if not lojas:
        st.warning("Nenhuma loja carregada")
        return
    
    total = len(lojas)
    ativas = sum(1 for l in lojas if l.get("status") == "open")
    inativas = total - ativas
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏪 Total de Lojas", total)
    with col2:
        st.metric("✅ Lojas Ativas", ativas, f"{round(ativas/total*100)}%")
    with col3:
        st.metric("❌ Lojas Inativas", inativas, f"{round(inativas/total*100)}%")
    with col4:
        estados = len({l.get("estado") for l in lojas if l.get("estado")})
        st.metric("🗺️ Estados", estados)
    
    st.markdown("---")
    
    # Alertas recentes
    st.markdown("### 🚨 Alertas Recentes")
    
    alertas = [l for l in lojas if l.get("status") != "open"]
    
    if alertas:
        for loja in alertas[:10]:
            st.warning(f"**{loja.get('nome', 'Loja')}** - {loja.get('status', 'Inativa')}")
    else:
        st.success("Nenhuma loja com problemas!")
    
    st.markdown("---")
    
    st.markdown("### 🏪 Lojas Recentes")
    
    for loja in lojas[:5]:
        status_emoji = "✅" if loja.get("status") == "open" else "❌"
        st.markdown(f"{status_emoji} **{loja.get('nome', 'Loja')}** - {loja.get('cidade', '')}/{loja.get('estado', '')}")