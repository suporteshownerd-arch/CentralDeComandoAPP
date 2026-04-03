"""
Página Feed - Consulta rápida de lojas
"""

import streamlit as st


def render_page(loader, lojas):
    st.markdown("## 📊 Feed")
    st.markdown("---")
    
    if not lojas:
        st.warning("Nenhuma loja carregada")
        return
    
    # Consulta rápida
    st.markdown("### 🔍 Consultar Loja")
    
    busca = st.text_input("Digite o nome ou código da loja:", placeholder="Buscar...", key="feed_busca")
    
    if busca:
        resultados = [l for l in lojas if busca.lower() in str(l.get('nome', '')).lower() or busca.lower() in str(l.get('codigo', '')).lower()]
    else:
        resultados = lojas[:10]
    
    st.markdown("---")
    
    # Resultados
    st.markdown(f"### 📋 Resultados ({len(resultados)})")
    
    if not resultados:
        st.info("Nenhuma loja encontrada")
        return
    
    for loja in resultados:
        status = loja.get("status", "open")
        status_emoji = "✅" if status == "open" else "❌"
        
        with st.container():
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"**{loja.get('nome', 'Loja')}**")
                st.caption(f"{loja.get('cidade', '')}/{loja.get('estado', '')}")
            with col2:
                st.markdown(status_emoji)
            st.divider()