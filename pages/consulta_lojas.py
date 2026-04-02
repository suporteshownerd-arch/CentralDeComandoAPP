"""
Página de Consulta de Lojas - Ultra Minimalista
"""

import streamlit as st


def render_page(data_loader, lojas):
    """Renderiza a página de Consulta de Lojas"""
    
    st.markdown("## 🏪 Consulta de Lojas")
    st.markdown("*Busque informações completas de qualquer loja do parque DPSP*")
    
    st.metric("Total Lojas", len(lojas) if lojas else 0)
    st.markdown("---")
    
    # Busca
    termo = st.text_input("Buscar", placeholder="Digite VD ou nome...")
    
    # Resultados
    resultados = lojas or []
    if termo:
        termo_lower = termo.lower()
        resultados = [
            l for l in lojas 
            if termo_lower in str(l.get('vd', '')).lower() 
            or termo_lower in str(l.get('nome', '')).lower()
        ]
        
    st.markdown(f"**{len(resultados)} resultado(s)**")
    
    # Mostrar resultados
    for i, loja in enumerate(resultados[:20]):
        vd = str(loja.get('vd', 'N/A'))
        nome = loja.get('nome', 'N/A')
        endereco = loja.get('endereco', 'N/A')
        cidade = loja.get('cidade', 'N/A')
        estado = loja.get('estado', 'N/A')
        
        st.markdown(f"**VD {vd}** - {nome}")
        st.caption(f"📍 {endereco} - {cidade}/{estado}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"⭐", key=f"fav_{vd}_{i}"):
                pass
        with col2:
            if st.button(f"📋", key=f"det_{vd}_{i}"):
                st.session_state.loja_selecionada = loja
        
        st.markdown("---")