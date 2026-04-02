"""
Página de Histórico
Central de Comando DPSP v2.0
"""

import streamlit as st


def render_page(sheets_manager):
    """Renderiza a página de Histórico"""
    st.markdown("## 📋 Histórico")
    st.markdown("*Registro de templates e comunicados*")
    
    try:
        historico = sheets_manager.get_historico()
        
        col1, col2, col3, col4 = st.columns(4)
        
        aexec = len([h for h in historico if 'AExec' in str(h)])
        gcrises = len([h for h in historico if 'GCrises' in str(h)])
        isoladas = len([h for h in historico if 'Isolada' in str(h)])
        
        with col1:
            st.metric("Alertas Executivos", aexec)
        with col2:
            st.metric("Gestão Crises", gcrises)
        with col3:
            st.metric("Lojas Isoladas", isoladas)
        with col4:
            st.metric("Total", len(historico))
        
        st.markdown("---")
        
        # Listar registros
        for reg in historico[:20]:
            icon = "🔴" if "AExec" in str(reg) else "🚨" if "GCrises" in str(reg) else "⚡"
            
            st.markdown(f"""
            <div class="template-box">
                <div class="template-header">
                    <span>{icon} {reg.get('tipo', 'N/A')}</span>
                    <span style="color:var(--text3)">{reg.get('data', '')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Opções
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                if st.button("📋 Copiar", key=f"copy_hist_{reg.get('id', '')}"):
                    st.toast("✅ Copiado!")
            with col_b2:
                if st.button("🗑️ Excluir", key=f"del_hist_{reg.get('id', '')}"):
                    st.toast("⚠️ Funcionalidade em desenvolvimento")
    
    except Exception as e:
        st.info("Nenhum registro encontrado.")
        st.error(f"Erro: {str(e)}")
    
    # Botão para limpar histórico
    st.markdown("---")
    if st.button("🗑️ Limpar Histórico"):
        try:
            sheets_manager.limpar_historico()
            st.success("✅ Histórico limpo!")
            st.rerun()
        except:
            st.error("❌ Erro ao limpar")