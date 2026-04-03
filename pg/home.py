"""
Página Home - Início com logo
"""

import streamlit as st


def render_page():
    st.markdown("""
    <div style="
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        margin-bottom: 40px;
    ">
        <div style="font-size: 80px; margin-bottom: 20px;">🛡️</div>
        <div style="
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        ">Central de Comando</div>
        <div style="
            font-size: 16px;
            color: #888;
        ">DPSP T.I. • Sistema de Gestão de Lojas</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📌 Selecione uma opção no menu lateral")