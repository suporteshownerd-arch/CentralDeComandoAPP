"""
Página de Consulta de Lojas - Versão Estável v2.3
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
    if termo and lojas:
        termo_lower = termo.lower()
        resultados = [
            l for l in lojas 
            if termo_lower in str(l.get('vd', '')).lower() 
            or termo_lower in str(l.get('nome', '')).lower()
        ]
        
        st.markdown(f"**{len(resultados)} resultado(s)**")
        
        for i, loja in enumerate(resultados[:20]):
            render_loja_card(loja, i)
    elif lojas:
        st.markdown("### Lojas do Parque")
        for i, loja in enumerate(lojas[:10]):
            render_loja_card(loja, i)


def render_loja_card(loja, index):
    """Renderiza card de loja"""
    from components import render_vd_badge, render_status_badge, render_desig_pill, render_info_section
    
    vd = str(loja.get('vd', 'N/A'))
    nome = loja.get('nome', 'N/A')
    endereco = loja.get('endereco', 'N/A')
    cidade = loja.get('cidade', 'N/A')
    estado = loja.get('estado', 'N/A')
    status = loja.get('status', 'open')
    
    st.markdown(f"""
    <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
                {render_vd_badge(vd)}
                <h3 style="margin:12px 0 6px 0;">{nome}</h3>
                <p style="color:var(--text2)">📍 {endereco} · {cidade} - {estado}</p>
            </div>
            {render_status_badge(status)}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botões
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⭐ Favorito", key=f"fav_{vd}_{index}"):
            vd_str = str(vd)
            if vd_str in st.session_state.favoritos:
                st.session_state.favoritos.remove(vd_str)
            else:
                st.session_state.favoritos.append(vd_str)
            st.rerun()
    with col2:
        if st.button("📋 Detalhes", key=f"det_{vd}_{index}"):
            st.session_state.loja_selecionada = loja