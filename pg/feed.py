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
    
    # Métricas em cards simples
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🏪 Total de Lojas", total)
    with col2:
        st.metric("✅ Ativas", ativas, f"{round(ativas/total*100)}%" if total > 0 else "0%")
    with col3:
        st.metric("❌ Inativas", inativas, f"-{round(inativas/total*100)}%" if total > 0 else "0%")
    
    st.markdown("---")
    
    # Lista de lojas
    st.markdown("### 🏪 Lojas")
    
    for loja in lojas:
        status = loja.get("status", "open")
        status_emoji = "✅" if status == "open" else "❌"
        
        col_info, col_status = st.columns([6, 1])
        
        with col_info:
            st.markdown(f"**{loja.get('nome', 'Loja')}** - {loja.get('cidade', '')}/{loja.get('estado', '')}")
        
        with col_status:
            st.markdown(status_emoji)