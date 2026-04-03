"""
Página Feed - Comunicados, imagens e informações
"""

import streamlit as st
from datetime import datetime


def render_page(loader, lojas):
    st.markdown("## 📊 Feed")
    st.markdown("---")
    
    # Inicializar session state para imagens
    if "feed_imagens" not in st.session_state:
        st.session_state.feed_imagens = []
    
    # Seção de Imagens
    st.markdown("### 🖼️ Imagens")
    
    # Botão para adicionar imagem
    col_botao, col_limpar = st.columns([4, 1])
    
    with col_botao:
        nova_url = st.text_input("Adicionar URL da imagem:", placeholder="https://...")
    
    with col_limpar:
        if st.button("➕ Add", key="add_imagem") and nova_url:
            st.session_state.feed_imagens.append(nova_url)
            st.rerun()
    
    # Exibir imagens
    if st.session_state.feed_imagens:
        # Se só 1 imagem, mostra normal
        if len(st.session_state.feed_imagens) == 1:
            st.image(st.session_state.feed_imagens[0], use_container_width=True)
            
            # Botão de excluir
            if st.button("🗑️ Excluir", key="excluir_img_0"):
                st.session_state.feed_imagens.pop(0)
                st.rerun()
        
        # Se mais de 1, carousel
        else:
            col_prev, col_img, col_next = st.columns([1, 6, 1])
            
            with col_prev:
                if st.button("◀"):
                    st.session_state.feed_idx = (st.session_state.get("feed_idx", 0) - 1) % len(st.session_state.feed_imagens)
                    st.rerun()
            
            with col_img:
                idx = st.session_state.get("feed_idx", 0)
                st.image(st.session_state.feed_imagens[idx], use_container_width=True)
                st.caption(f"{idx + 1} / {len(st.session_state.feed_imagens)}")
                
                if st.button("🗑️ Excluir esta", key=f"excluir_img_{idx}"):
                    st.session_state.feed_imagens.pop(idx)
                    if st.session_state.feed_imagens:
                        st.session_state.feed_idx = 0
                    st.rerun()
            
            with col_next:
                if st.button("▶"):
                    st.session_state.feed_idx = (st.session_state.get("feed_idx", 0) + 1) % len(st.session_state.feed_imagens)
                    st.rerun()
    
    st.markdown("---")
    
    # Seção de Comunicados
    st.markdown("### 📢 Comunicados")
    
    st.markdown("""
    <style>
        .comunicado-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
        }
        .comunicado-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }
        .comunicado-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent), var(--purple));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .comunicado-title {
            font-size: 15px;
            font-weight: 600;
            color: var(--text);
        }
        .comunicado-date {
            font-size: 11px;
            color: var(--text3);
            font-family: 'JetBrains Mono', monospace;
        }
        .comunicado-body {
            font-size: 13px;
            color: var(--text2);
            line-height: 1.6;
        }
        .comunicado-tag {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 10px;
            font-family: 'JetBrains Mono', monospace;
            text-transform: uppercase;
            margin-top: 12px;
        }
        .tag-aviso { background: rgba(245,158,11,0.15); color: var(--amber-light); }
        .tag-info { background: rgba(59,130,246,0.15); color: var(--blue); }
        .tag-alerta { background: rgba(239,68,68,0.15); color: var(--red-light); }
    </style>
    """, unsafe_allow_html=True)
    
    comunicados = [
        {
            "icon": "🔧",
            "title": "Manutenção Programada",
            "date": datetime.now().strftime("%d/%m/%Y"),
            "body": "Atenção! Manutenção preventiva programada para o banco de dados neste sábado das 02h às 06h.",
            "tag": "aviso",
            "tag_text": "AVISO"
        },
        {
            "icon": "📱",
            "title": "Nova Versão Disponível",
            "date": datetime.now().strftime("%d/%m/%Y"),
            "body": "A versão 5.1 do sistema está disponível com melhorias na consulta de lojas.",
            "tag": "info",
            "tag_text": "INFO"
        }
    ]
    
    for com in comunicados:
        st.markdown(f"""
        <div class="comunicado-card">
            <div class="comunicado-header">
                <div class="comunicado-icon">{com['icon']}</div>
                <div>
                    <div class="comunicado-title">{com['title']}</div>
                    <div class="comunicado-date">{com['date']}</div>
                </div>
            </div>
            <div class="comunicado-body">{com['body']}</div>
            <span class="comunicado-tag tag-{com['tag']}">{com['tag_text']}</span>
        </div>
        """, unsafe_allow_html=True)