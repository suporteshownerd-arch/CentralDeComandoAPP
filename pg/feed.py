"""
Página Feed - Comunicados e imagens
"""

import streamlit as st
from datetime import datetime
from io import BytesIO
from PIL import Image
import requests


def render_page(loader, lojas):
    st.markdown("## 📊 Feed")
    st.markdown("---")
    
    # Session states
    if "feed_imagens" not in st.session_state:
        st.session_state.feed_imagens = [
            {"tipo": "url", "dados": "https://picsum.photos/600/400?random=1", "usuario": "João", "data": "03/04 10:00"},
            {"tipo": "url", "dados": "https://picsum.photos/600/400?random=2", "usuario": "Maria", "data": "03/04 11:00"},
        ]
    if "feed_idx" not in st.session_state:
        st.session_state.feed_idx = 0
    if "feed_page" not in st.session_state:
        st.session_state.feed_page = 0
    
    # Botão discreto para adicionar
    with st.popover("➕ Imagem"):
        st.markdown("**Adicionar imagem**")
        
        uploaded = st.file_uploader("Do computador", type=['png', 'jpg', 'jpeg', 'gif', 'webp'], key="upl_feed")
        nome = st.text_input("Seu nome", key="nome_upl")
        if uploaded and nome:
            if st.button("Enviar"):
                st.session_state.feed_imagens.append({
                    "tipo": "upload",
                    "dados": uploaded,
                    "usuario": nome,
                    "data": datetime.now().strftime("%d/%m %H:%M")
                })
                st.rerun()
        
        st.markdown("---")
        
        url_img = st.text_input("URL da imagem", key="url_feed")
        nome_url = st.text_input("Seu nome", key="nome_url_feed")
        if url_img and nome_url:
            if st.button("Adicionar URL"):
                st.session_state.feed_imagens.append({
                    "tipo": "url",
                    "dados": url_img,
                    "usuario": nome_url,
                    "data": datetime.now().strftime("%d/%m %H:%M")
                })
                st.rerun()
    
    st.markdown("---")
    
# Carousel de imagens - 3 por página
    if not st.session_state.feed_imagens:
        st.info("📷 Adicione imagens usando o botão ➕ acima")
    else:
        total = len(st.session_state.feed_imagens)
        imgs_por_pagina = 3
        total_paginas = (total + imgs_por_pagina - 1) // imgs_por_pagina
        
        idx_inicio = st.session_state.feed_page * imgs_por_pagina
        idx_fim = min(idx_inicio + imgs_por_pagina, total)
        imagens_pagina = st.session_state.feed_imagens[idx_inicio:idx_fim]
        
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.button("◀ Página anterior"):
                st.session_state.feed_page = (st.session_state.feed_page - 1) % total_paginas
                st.rerun()
        with col_next:
            if st.button("Próxima página ▶"):
                st.session_state.feed_page = (st.session_state.feed_page + 1) % total_paginas
                st.rerun()
        
        cols = st.columns(len(imagens_pagina))
        for i, img in enumerate(imagens_pagina):
            idx = idx_inicio + i
            with cols[i]:
                try:
                    if img["tipo"] == "upload":
                        img_data = Image.open(img["dados"])
                    else:
                        img_data = Image.open(BytesIO(requests.get(img["dados"]).content))
                    img_data = img_data.resize((540, 720), Image.Resampling.LANCZOS)
                    
                    from PIL import ImageOps
                    bordered = ImageOps.expand(img_data, border=6, fill='#6366f1')
                    bordered = ImageOps.expand(bordered, border=4, fill='#1e1e2e')
                    
                    buf = BytesIO()
                    bordered.save(buf, format="PNG")
                    st.image(buf.getvalue(), width=560)
                except:
                    st.image(img["dados"], width=540)
                st.markdown(f"📤 **{img['usuario']}** • {img['data']}")
                if st.button("🗑️", key="del_" + str(idx)):
                    st.session_state.feed_imagens.pop(idx)
                    st.rerun()
        
        st.markdown(f"<div style='text-align: center; color: #888; margin-top: 10px;'>Página {st.session_state.feed_page + 1} de {total_paginas}</div>", unsafe_allow_html=True)
    
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