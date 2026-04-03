"""
Página Feed - Comunicados e imagens
"""

import streamlit as st
from datetime import datetime


def render_page(loader, lojas):
    st.markdown("## 📊 Feed")
    st.markdown("---")
    
    # Session states
    if "feed_imagens" not in st.session_state:
        st.session_state.feed_imagens = []
    if "feed_page" not in st.session_state:
        st.session_state.feed_page = 0
    
    # Adicionar imagem
    with st.expander("➕ Adicionar Imagem"):
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded = st.file_uploader("Do computador", type=['png', 'jpg', 'jpeg', 'gif', 'webp'])
            if uploaded:
                nome = st.text_input("Seu nome", key="nome_pc")
                if nome and st.button("Enviar do PC"):
                    st.session_state.feed_imagens.append({
                        "tipo": "upload",
                        "dados": uploaded,
                        "usuario": nome,
                        "data": datetime.now().strftime("%d/%m %H:%M")
                    })
                    st.rerun()
        
        with col2:
            url_img = st.text_input("URL da imagem", key="url_img")
            if url_img:
                nome_url = st.text_input("Seu nome", key="nome_url")
                if nome_url and st.button("Enviar URL"):
                    st.session_state.feed_imagens.append({
                        "tipo": "url",
                        "dados": url_img,
                        "usuario": nome_url,
                        "data": datetime.now().strftime("%d/%m %H:%M")
                    })
                    st.rerun()
    
    st.markdown("---")
    
    # Exibir imagens (carousel de 3 em 3)
    if st.session_state.feed_imagens:
        total = len(st.session_state.feed_imagens)
        por_pagina = 3
        total_paginas = (total + por_pagina - 1) // por_pagina
        
        # Navegação
        col_ant, col_pag, col_prox = st.columns([1, 2, 1])
        with col_ant:
            if st.button("◀") and st.session_state.feed_page > 0:
                st.session_state.feed_page -= 1
                st.rerun()
        with col_pag:
            st.markdown(f"**Página {st.session_state.feed_page + 1} / {total_paginas}**")
        with col_prox:
            if st.button("▶") and st.session_state.feed_page < total_paginas - 1:
                st.session_state.feed_page += 1
                st.rerun()
        
        # Imagens da página atual
        ini = st.session_state.feed_page * por_pagina
        fim = min(ini + por_pagina, total)
        imgs_pag = st.session_state.feed_imagens[ini:fim]
        
        cols = st.columns(len(imgs_pag))
        for i, img in enumerate(imgs_pag):
            with cols[i]:
                try:
                    if img["tipo"] == "upload":
                        st.image(img["dados"], width=300)
                    else:
                        st.image(img["dados"], width=300)
                except:
                    st.error("Erro ao carregar imagem")
                st.caption(f"📤 {img['usuario']} • {img['data']}")
                if st.button(f"🗑️ Excluir", key=f"del_{ini+i}"):
                    st.session_state.feed_imagens.pop(ini+i)
                    if st.session_state.feed_page > 0:
                        st.session_state.feed_page -= 1
                    st.rerun()
        
        # Pontos de navegação
        pontos = "".join([f"•" if p != st.session_state.feed_page else "●" for p in range(total_paginas)])
        st.markdown(f"<div style='text-align: center; color: #888;'>{pontos}</div>", unsafe_allow_html=True)
    
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