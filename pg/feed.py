"""
Página Feed - Comunicados e imagens
"""

import streamlit as st
from datetime import datetime


def render_page(loader, lojas):
    st.markdown("## 📊 Feed")
    st.markdown("---")
    
    # Imagens
    st.markdown("### 🖼️ Imagens")
    
    # Campo para adicionar URL
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        nova_url = st.text_input("Adicionar URL da imagem:", placeholder="https://...", key="feed_url")
    with col_btn:
        if nova_url and st.button("➕", key="add_img_btn"):
            if "feed_imagens" not in st.session_state:
                st.session_state.feed_imagens = []
            st.session_state.feed_imagens.append(nova_url)
            st.rerun()
    
    # Exibir imagens
    if "feed_imagens" in st.session_state and st.session_state.feed_imagens:
        st.markdown("---")
        
        num_imgs = len(st.session_state.feed_imagens)
        cols = st.columns(min(num_imgs, 3))
        
        for i, url in enumerate(st.session_state.feed_imagens):
            with cols[i % 3]:
                st.image(url, width=250)
                if st.button(f"🗑️ Excluir", key=f"del_img_{i}"):
                    st.session_state.feed_imagens.pop(i)
                    st.rerun()
        
        if num_imgs > 3:
            st.caption(f"Total: {num_imgs} imagens")
    
    st.markdown("---")
    
    # Comunicados
    st.markdown("### 📢 Comunicados")
    
    st.markdown("""
    <style>
        .com-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
        }
        .com-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }
        .com-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--accent), var(--purple));
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .com-title {
            font-weight: 600;
            color: var(--text);
        }
        .com-date {
            font-size: 11px;
            color: var(--text3);
        }
        .com-body {
            color: var(--text2);
            font-size: 13px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    comunicados = [
        {"icon": "🔧", "title": "Manutenção Programada", "date": datetime.now().strftime("%d/%m/%Y"), "body": "Manutenção preventiva neste sábado das 02h às 06h. Podem ocorrer instabilidades."},
        {"icon": "📱", "title": "Nova Versão Disponível", "date": datetime.now().strftime("%d/%m/%Y"), "body": "A versão 5.1 do sistema já está disponível com melhorias e correções."},
    ]
    
    for com in comunicados:
        st.markdown(f"""
        <div class="com-card">
            <div class="com-header">
                <div class="com-icon">{com['icon']}</div>
                <div>
                    <div class="com-title">{com['title']}</div>
                    <div class="com-date">{com['date']}</div>
                </div>
            </div>
            <div class="com-body">{com['body']}</div>
        </div>
        """, unsafe_allow_html=True)