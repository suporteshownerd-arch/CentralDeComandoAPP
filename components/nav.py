"""
Sidebar - Claro e objective
"""

import streamlit as st


def render_sidebar(lojas, favoritos):
    # Logo/Título
    st.markdown("**🛡️ CENTRAL DE COMANDO**")
    
    st.markdown("---")
    
    # Navegação com LABELS CLAROS
    st.markdown("**O que você quer fazer?**")
    
    opcoes = {
        "Buscar uma loja": "🏪",
        "Registrar uma crise": "🚨",
        "Abrir chamado na Vivo/Claro": "📞",
        "Ver histórico de alertas": "📋",
        "Ver gráficos do parque": "📈",
        "Ajuda e manual": "❓"
    }
    
    # Lista de opções com emoji
    lista = [f"{emoji} {nome}" for nome, emoji in opcoes.items()]
    
    # Selectbox para navegar
    escolha = st.selectbox(
        "Selecione:",
        lista,
        label_visibility="collapsed"
    )
    
    # Atualiza sessão
    st.session_state.nav_page = escolha
    
    st.markdown("---")
    
    # Estatísticas
    if lojas:
        total = len(lojas)
        ativas = sum(1 for l in lojas if l.get("status") == "open")
        st.markdown(f"📊 **{total}** lojas no total")
        st.markdown(f"✅ **{ativas}** lojas ativas")
    else:
        st.markdown("Nenhuma loja carregada")
    
    st.markdown("---")
    
    # Contato
    st.markdown("**Precisa de ajuda?**")
    st.info("📞 Ligue: (11) 3274-7527")
    
    return escolha


def render_footer():
    st.caption("Central de Comando DPSP - v5.0")


def init_session_state():
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "🏪 Buscar uma loja"


def setup_page_config():
    st.set_page_config(
        page_title="Central de Comando",
        page_icon="🛡️",
        layout="wide",
    )


def render_page_header(title, subtitle=None, icon=None):
    if icon:
        title = f"{icon} {title}"
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")
