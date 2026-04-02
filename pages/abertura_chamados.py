"""
Página de Abertura de Chamados
Central de Comando DPSP v2.0
"""

import streamlit as st
from datetime import datetime


def render_page(lojas):
    """Renderiza a página de Abertura de Chamados"""
    st.markdown("## 📞 Abertura de Chamados")
    st.markdown("*Gere textos para abertura de chamado nas operadoras*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        vd_ch = st.text_input("VD", placeholder="2015")
        desig_ch = st.text_input("Designação")
        nome_ch = st.text_input("Seu Nome")
    
    with col2:
        hora_ch = st.time_input("Hora Início")
        horario_ch = st.text_input("Horário Funcionamento")
        op = st.selectbox("Operadora", ["Vivo + Claro", "Apenas Vivo", "Apenas Claro"])
    
    if st.button("🔄 Gerar", type="primary"):
        if vd_ch and desig_ch:
            hora_str = hora_ch.strftime("%H:%M") if hora_ch else "--:--"
            
            # Buscar loja
            loja = None
            for l in lojas:
                if l.get('vd') == vd_ch:
                    loja = l
                    break
            
            from templates import gerar_chamado_vivo, gerar_chamado_claro
            
            if loja:
                vivo_txt = gerar_chamado_vivo(loja, nome_ch or "Atendente", hora_str)
                claro_txt = gerar_chamado_claro(loja, hora_str)
            else:
                vivo_txt = f"VD: {vd_ch} - Designação: {desig_ch}"
                claro_txt = f"VD: {vd_ch} - Designação: {desig_ch}"
            
            if op in ["Vivo + Claro", "Apenas Vivo"]:
                st.markdown("### 📱 VIVO")
                st.code(vivo_txt)
                if st.button("📋 Copiar Vivo", key="copy_ch_vivo"):
                    st.toast("✅ Copiado!")
            
            if op in ["Vivo + Claro", "Apenas Claro"]:
                st.markdown("### 🔵 CLARO")
                st.code(claro_txt)
                if st.button("📋 Copiar Claro", key="copy_ch_claro"):
                    st.toast("✅ Copiado!")
        else:
            st.warning("Preencha VD e Designação!")
    
    # Links úteis
    st.markdown("---")
    st.markdown("### 🔗 Portais das Operadoras")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown("""
        **📱 Vivo MVE**
        [Acessar portal](https://mve.vivo.com.br)
        """)
    with col_l2:
        st.markdown("""
        **🔵 Claro Empresas**
        [Acessar portal](https://webebt01.embratel.com.br/claroempresasonline/index)
        """)