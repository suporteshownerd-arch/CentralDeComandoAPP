"""
Página Feed - Comunicados, imagens e informações
"""

import streamlit as st
from datetime import datetime


def render_page(loader, lojas):
    st.markdown("## 📊 Feed")
    st.markdown("---")
    
    # Inicializar session state
    if "feed_imagens" not in st.session_state:
        st.session_state.feed_imagens = []
    if "feed_uploaded_images" not in st.session_state:
        st.session_state.feed_uploaded_images = []
    if "feed_page" not in st.session_state:
        st.session_state.feed_page = 0
    
    # Botão sutil para adicionar imagem
    with st.popover("➕ Imagem"):
        uploaded_file = st.file_uploader("Do PC", type=['png', 'jpg', 'jpeg', 'gif', 'webp'], key="feed_upload")
        if uploaded_file:
            nome = st.text_input("Seu nome:", key="nome_up")
            if nome and st.button("Adicionar"):
                st.session_state.feed_uploaded_images.append({
                    "img": uploaded_file,
                    "user": nome,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M")
                })
                st.rerun()
        
        url = st.text_input("URL", key="url_in")
        if url:
            nome_url = st.text_input("Seu nome:", key="nome_url")
            if nome_url and st.button("Add URL"):
                st.session_state.feed_imagens.append({
                    "url": url,
                    "user": nome_url,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M")
                })
                st.rerun()
    
    st.markdown("---")
    
    # Exibir imagens do PC
    if st.session_state.feed_uploaded_images:
        total = len(st.session_state.feed_uploaded_images)
        pagina = st.session_state.get("feed_page", 0)
        items_por_pagina = 3
        ini = pagina * items_por_pagina
        fim = min(ini + items_por_pagina, total)
        imgs = st.session_state.feed_uploaded_images[ini:fim]
        
        for i, d in enumerate(imgs):
            st.image(d["img"], width=320)
            st.caption(f"📤 {d['user']} • {d['data']}")
            if st.button(f"🗑️", key=f"del_pc_{ini+i}"):
                st.session_state.feed_uploaded_images.pop(ini+i)
                st.rerun()
        
        total_pags = (total + items_por_pagina - 1) // items_por_pagina
        if total_pags > 1:
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("◀") and pagina > 0:
                    st.session_state.feed_page = pagina - 1
                    st.rerun()
            with c2:
                st.caption(f"{pagina+1}/{total_pags}")
            with c3:
                if st.button("▶") and pagina < total_pags - 1:
                    st.session_state.feed_page = pagina + 1
                    st.rerun()
    
    # Exibir imagens URL
    if st.session_state.feed_imagens:
        if st.session_state.feed_uploaded_images:
            st.markdown("---")
        
        total = len(st.session_state.feed_imagens)
        pagina = st.session_state.get("feed_url_page", 0)
        items_por_pagina = 3
        ini = pagina * items_por_pagina
        fim = min(ini + items_por_pagina, total)
        imgs = st.session_state.feed_imagens[ini:fim]
        
        for i, d in enumerate(imgs):
            st.image(d["url"], width=320)
            st.caption(f"📤 {d['user']} • {d['data']}")
            if st.button(f"🗑️", key=f"del_url_{ini+i}"):
                st.session_state.feed_imagens.pop(ini+i)
                st.rerun()
        
        total_pags = (total + items_por_pagina - 1) // items_por_pagina
        if total_pags > 1:
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("◀", key="prev") and pagina > 0:
                    st.session_state.feed_url_page = pagina - 1
                    st.rerun()
            with c2:
                st.caption(f"{pagina+1}/{total_pags}")
            with c3:
                if st.button("▶", key="next") and pagina < total_pags - 1:
                    st.session_state.feed_url_page = pagina + 1
                    st.rerun()
    
    st.markdown("---")
    
    # Comunicados
    st.markdown("### 📢 Comunicados")
    
    st.markdown("""
    <style>
        .card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px; margin-bottom: 16px; }
        .hdr { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
        .icn { width: 40px; height: 40px; background: linear-gradient(135deg, var(--accent), var(--purple)); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
        .ttl { font-size: 15px; font-weight: 600; color: var(--text); }
        .dta { font-size: 11px; color: var(--text3); font-family: 'JetBrains Mono', monospace; }
        .bod { font-size: 13px; color: var(--text2); line-height: 1.6; }
        .tag { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 10px; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; margin-top: 12px; }
        .aviso { background: rgba(245,158,11,0.15); color: var(--amber-light); }
        .info { background: rgba(59,130,246,0.15); color: var(--blue); }
    </style>
    """, unsafe_allow_html=True)
    
    for c in [
        {"icon": "🔧", "title": "Manutenção Programada", "date": datetime.now().strftime("%d/%m/%Y"), "body": "Manutenção preventiva neste sábado das 02h às 06h.", "tag": "aviso", "tag_text": "AVISO"},
        {"icon": "📱", "title": "Nova Versão Disponível", "date": datetime.now().strftime("%d/%m/%Y"), "body": "Versão 5.1 disponível com melhorias.", "tag": "info", "tag_text": "INFO"}
    ]:
        st.markdown(f'''<div class="card"><div class="hdr"><div class="icn">{c["icon"]}</div><div><div class="ttl">{c["title"]}</div><div class="dta">{c["date"]}</div></div></div><div class="bod">{c["body"]}</div><span class="tag {c["tag"]}">{c["tag_text"]}</span></div>''', unsafe_allow_html=True)