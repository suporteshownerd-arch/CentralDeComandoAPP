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
    
    # Adicionar
    col_add, col_list = st.columns([1, 4])
    with col_add:
        nova_img = st.text_input("URL imagem:", key="img_url")
    with col_list:
        if nova_img and st.button("+ Add"):
            if "feed_imgs" not in st.session_state:
                st.session_state.feed_imgs = []
            st.session_state.feed_imgs.append({"url": nova_img, "user": "User", "date": datetime.now().strftime("%d/%m")})
            st.rerun()
    
    # Listar
    if "feed_imgs" in st.session_state and st.session_state.feed_imgs:
        cols = st.columns(len(st.session_state.feed_imgs))
        for i, img in enumerate(st.session_state.feed_imgs):
            with cols[i]:
                try:
                    st.image(img["url"], width=300)
                except:
                    st.error("Erro")
                if st.button(f"X", key=f"del_{i}"):
                    st.session_state.feed_imgs.pop(i)
                    st.rerun()
    
    st.markdown("---")
    
    # Comunicados
    st.markdown("### 📢 Comunicados")
    
    for c in [
        {"icon": "🔧", "title": "Manutenção", "date": datetime.now().strftime("%d/%m/%Y"), "body": "Manutenção sábado 02h-06h"},
        {"icon": "📱", "title": "Nova Versão", "date": datetime.now().strftime("%d/%m/%Y"), "body": "Versão 5.1 disponível"}
    ]:
        st.markdown(f"**{c['icon']} {c['title']}** - {c['date']}")
        st.markdown(c['body'])
        st.divider()