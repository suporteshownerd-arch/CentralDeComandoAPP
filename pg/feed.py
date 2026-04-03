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
        if uploaded_file and uploaded_file not in st.session_state.feed_uploaded_images:
            st.session_state.feed_uploaded_images.append(uploaded_file)
            st.rerun()
        
        nova_url = st.text_input("URL", placeholder="https://...", key="feed_url")
        if st.button("Adicionar") and nova_url:
            st.session_state.feed_imagens.append(nova_url)
            st.rerun()
    
    st.markdown("---")
    
    QTD_POR_PAGINA = 3
    
    # Exibir imagens do PC (3 por vez)
    if st.session_state.feed_uploaded_images:
        total = len(st.session_state.feed_uploaded_images)
        pagina = st.session_state.get("feed_page", 0)
        inicio = pagina * QTD_POR_PAGINA
        fim = min(inicio + QTD_POR_PAGINA, total)
        imagens_pagina = st.session_state.feed_uploaded_images[inicio:fim]
        
        if len(imagens_pagina) == 1:
            st.image(imagens_pagina[0], width=320)
            if st.button("🗑️ Excluir", key=f"excluir_pc_{inicio}"):
                st.session_state.feed_uploaded_images.pop(inicio)
                st.rerun()
        else:
            cols = st.columns(3)
            for i, img in enumerate(imagens_pagina):
                with cols[i]:
                    st.image(img, width=320)
                    if st.button(f"🗑️", key=f"excluir_pc_{inicio + i}"):
                        st.session_state.feed_uploaded_images.pop(inicio + i)
                        st.rerun()
        
        # Navegação
        total_paginas = (total + QTD_POR_PAGINA - 1) // QTD_POR_PAGINA
        if total_paginas > 1:
            col_nav = st.columns([1, 2, 1])
            with col_nav[0]:
                if st.button("◀ Anterior") and pagina > 0:
                    st.session_state.feed_page = pagina - 1
                    st.rerun()
            with col_nav[1]:
                st.caption(f"Página {pagina + 1} de {total_paginas} ({total} imagens)")
            with col_nav[2]:
                if st.button("Próxima ▶") and pagina < total_paginas - 1:
                    st.session_state.feed_page = pagina + 1
                    st.rerun()
    
    # Exibir imagens URL (3 por vez)
    if st.session_state.feed_imagens:
        if st.session_state.feed_uploaded_images: st.markdown("---")
        
        total = len(st.session_state.feed_imagens)
        pagina = st.session_state.get("feed_url_page", 0)
        inicio = pagina * QTD_POR_PAGINA
        fim = min(inicio + QTD_POR_PAGINA, total)
        imagens_pagina = st.session_state.feed_imagens[inicio:fim]
        
        if len(imagens_pagina) == 1:
            st.image(imagens_pagina[0], width=320)
            if st.button("🗑️ Excluir", key=f"excluir_url_{inicio}"):
                st.session_state.feed_imagens.pop(inicio)
                st.rerun()
        else:
            cols = st.columns(3)
            for i, img in enumerate(imagens_pagina):
                with cols[i]:
                    st.image(img, width=320)
                    if st.button(f"🗑️", key=f"excluir_url_{inicio + i}"):
                        st.session_state.feed_imagens.pop(inicio + i)
                        st.rerun()
        
        total_paginas = (total + QTD_POR_PAGINA - 1) // QTD_POR_PAGINA
        if total_paginas > 1:
            col_nav = st.columns([1, 2, 1])
            with col_nav[0]:
                if st.button("◀ Anterior", key="prev_url") and pagina > 0:
                    st.session_state.feed_url_page = pagina - 1
                    st.rerun()
            with col_nav[1]:
                st.caption(f"Página {pagina + 1} de {total_paginas} ({total} imagens)")
            with col_nav[2]:
                if st.button("Próxima ▶", key="next_url") and pagina < total_paginas - 1:
                    st.session_state.feed_url_page = pagina + 1
                    st.rerun()
    
    st.markdown("---")
    
    # Comunicados
    st.markdown("### 📢 Comunicados")
    
    st.markdown("""
    <style>
        .comunicado-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 20px; margin-bottom: 16px; }
        .comunicado-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
        .comunicado-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--accent), var(--purple)); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
        .comunicado-title { font-size: 15px; font-weight: 600; color: var(--text); }
        .comunicado-date { font-size: 11px; color: var(--text3); font-family: 'JetBrains Mono', monospace; }
        .comunicado-body { font-size: 13px; color: var(--text2); line-height: 1.6; }
        .comunicado-tag { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 10px; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; margin-top: 12px; }
        .tag-aviso { background: rgba(245,158,11,0.15); color: var(--amber-light); }
        .tag-info { background: rgba(59,130,246,0.15); color: var(--blue); }
    </style>
    """, unsafe_allow_html=True)
    
    for com in [
        {"icon": "🔧", "title": "Manutenção Programada", "date": datetime.now().strftime("%d/%m/%Y"), "body": "Manutenção preventiva neste sábado das 02h às 06h.", "tag": "aviso", "tag_text": "AVISO"},
        {"icon": "📱", "title": "Nova Versão Disponível", "date": datetime.now().strftime("%d/%m/%Y"), "body": "Versão 5.1 disponível com melhorias.", "tag": "info", "tag_text": "INFO"}
    ]:
        st.markdown(f'''<div class="comunicado-card"><div class="comunicado-header"><div class="comunicado-icon">{com["icon"]}</div><div><div class="comunicado-title">{com["title"]}</div><div class="comunicado-date">{com["date"]}</div></div></div><div class="comunicado-body">{com["body"]}</div><span class="comunicado-tag tag-{com["tag"]}">{com["tag_text"]}</span></div>''', unsafe_allow_html=True)