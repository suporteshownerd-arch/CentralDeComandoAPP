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
        st.session_state.feed_imagens = []  # URLs externas
    if "feed_uploaded_images" not in st.session_state:
        st.session_state.feed_uploaded_images = []  # Arquivos do PC
    
    # Seção de Imagens
    st.markdown("### 🖼️ Imagens")
    
    # Upload de arquivo do PC
    uploaded_file = st.file_uploader("Enviar imagem do PC", type=['png', 'jpg', 'jpeg', 'gif', 'webp'], key="feed_upload")
    
    if uploaded_file is not None:
        if uploaded_file not in st.session_state.feed_uploaded_images:
            st.session_state.feed_uploaded_images.append(uploaded_file)
            st.rerun()
    
    # Campo para adicionar URL
    nova_url = st.text_input("Ou adicionar URL:", placeholder="https://...", key="feed_url")
    
    if st.button("➕ Adicionar") and nova_url:
        st.session_state.feed_imagens.append(nova_url)
        st.rerun()
    
    st.markdown("---")
    
    # Exibir imagens do PC (prioridade)
    if st.session_state.feed_uploaded_images:
        st.markdown("#### 📁 Imagens do PC")
        
        if len(st.session_state.feed_uploaded_images) == 1:
            st.image(st.session_state.feed_uploaded_images[0], use_container_width=True)
            if st.button("🗑️ Excluir", key="excluir_pc_0"):
                st.session_state.feed_uploaded_images.pop(0)
                st.rerun()
        else:
            col_prev, col_img, col_next = st.columns([1, 6, 1])
            idx = st.session_state.get("feed_idx", 0)
            
            with col_prev:
                if st.button("◀"):
                    st.session_state.feed_idx = (idx - 1) % len(st.session_state.feed_uploaded_images)
                    st.rerun()
            
            with col_img:
                st.image(st.session_state.feed_uploaded_images[idx], use_container_width=True)
                st.caption(f"{idx + 1} / {len(st.session_state.feed_uploaded_images)}")
                if st.button("🗑️ Excluir", key=f"excluir_pc_{idx}"):
                    st.session_state.feed_uploaded_images.pop(idx)
                    if st.session_state.feed_uploaded_images:
                        st.session_state.feed_idx = 0
                    st.rerun()
            
            with col_next:
                if st.button("▶"):
                    st.session_state.feed_idx = (idx + 1) % len(st.session_state.feed_uploaded_images)
                    st.rerun()
    
    # Exibir imagens de URL
    if st.session_state.feed_imagens:
        if st.session_state.feed_uploaded_images:
            st.markdown("---")
        st.markdown("#### 🔗 Imagens URL")
        
        if len(st.session_state.feed_imagens) == 1:
            st.image(st.session_state.feed_imagens[0], use_container_width=True)
            if st.button("🗑️ Excluir", key="excluir_url_0"):
                st.session_state.feed_imagens.pop(0)
                st.rerun()
        else:
            col_prev, col_img, col_next = st.columns([1, 6, 1])
            idx = st.session_state.get("feed_url_idx", 0)
            
            with col_prev:
                if st.button("◀", key="prev_url"):
                    st.session_state.feed_url_idx = (idx - 1) % len(st.session_state.feed_imagens)
                    st.rerun()
            
            with col_img:
                st.image(st.session_state.feed_imagens[idx], use_container_width=True)
                st.caption(f"{idx + 1} / {len(st.session_state.feed_imagens)}")
                if st.button("🗑️ Excluir", key=f"excluir_url_{idx}"):
                    st.session_state.feed_imagens.pop(idx)
                    if st.session_state.feed_imagens:
                        st.session_state.feed_url_idx = 0
                    st.rerun()
            
            with col_next:
                if st.button("▶", key="next_url"):
                    st.session_state.feed_url_idx = (idx + 1) % len(st.session_state.feed_imagens)
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