"""
Página Feed - Comunicados e imagens
"""

import streamlit as st
from datetime import datetime


def render_page(loader, lojas):
    st.markdown("## 📊 Feed")
    st.markdown("---")
    
    # Botão para adicionar imagem
    col_bt, col_cmp = st.columns([1, 4])
    with col_bt:
        if st.button("➕ Adicionar Imagem", key="btn_add_img"):
            st.session_state.show_add_img = True
    
    # Campo para adicionar (só mostra quando clica o botão)
    if st.session_state.get("show_add_img", False):
        with col_cmp:
            nova_url = st.text_input("Cole a URL da imagem:", key="input_url_img", placeholder="https://...")
            if nova_url:
                if st.button("Salvar", key="salvar_img"):
                    if "feed_imagens" not in st.session_state:
                        st.session_state.feed_imagens = []
                    st.session_state.feed_imagens.append(nova_url)
                    st.session_state.show_add_img = False
                    st.rerun()
            
            if st.button("Cancelar", key="cancelar_img"):
                st.session_state.show_add_img = False
                st.rerun()
    
    # Exibir imagens
    if "feed_imagens" in st.session_state and st.session_state.feed_imagens:
        st.markdown("---")
        
        cols = st.columns(3)
        for i, url in enumerate(st.session_state.feed_imagens):
            with cols[i % 3]:
                st.image(url, width=300)
                if st.button(f"🗑️", key=f"del_{i}"):
                    st.session_state.feed_imagens.pop(i)
                    st.rerun()
        
        st.caption(f"Total: {len(st.session_state.feed_imagens)} imagem(ns)")
    
    st.markdown("---")
    
    # Comunicados
    st.markdown("### 📢 Comunicados")
    
    st.markdown("""
    <style>
        .com-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin-bottom: 12px; }
        .com-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
        .com-icon { width: 32px; height: 32px; background: linear-gradient(135deg, var(--accent), var(--purple)); border-radius: 8px; display: flex; align-items: center; justify-content: center; }
        .com-title { font-weight: 600; color: var(--text); }
        .com-date { font-size: 11px; color: var(--text3); }
        .com-body { color: var(--text2); font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)
    
    for com in [
        {"icon": "🔧", "title": "Manutenção Programada", "date": datetime.now().strftime("%d/%m/%Y"), "body": "Manutenção preventiva neste sábado das 02h às 06h."},
        {"icon": "📱", "title": "Nova Versão Disponível", "date": datetime.now().strftime("%d/%m/%Y"), "body": "Versão 5.1 disponível com melhorias."},
    ]:
        st.markdown(f"""
        <div class="com-card">
            <div class="com-header">
                <div class="com-icon">{com['icon']}</div>
                <div><div class="com-title">{com['title']}</div><div class="com-date">{com['date']}</div></div>
            </div>
            <div class="com-body">{com['body']}</div>
        </div>
        """, unsafe_allow_html=True)