"""
Sidebar - Claro e objective
"""

import streamlit as st
from datetime import datetime


def render_sidebar(lojas, favoritos):
    # Logo Melhorado
    st.markdown("""
    <style>
        .logo-container {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 16px;
        }
        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .logo-text {
            display: flex;
            flex-direction: column;
        }
        .logo-title {
            font-size: 16px;
            font-weight: bold;
            color: white;
            letter-spacing: 0.5px;
        }
        .logo-subtitle {
            font-size: 10px;
            color: rgba(255,255,255,0.5);
            font-family: monospace;
            letter-spacing: 1px;
        }
    </style>
    <div class="logo-container">
        <div class="logo-icon">🛡️</div>
        <div class="logo-text">
            <span class="logo-title">CENTRAL DE COMANDO</span>
            <span class="logo-subtitle">DPSP • T.I. v5.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status indicator
    st.markdown("""
    <style>
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            background: rgba(34, 197, 94, 0.15);
            border-radius: 20px;
            font-size: 11px;
            color: #22c55e;
            margin-bottom: 16px;
        }
        .status-dot {
            width: 6px;
            height: 6px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
    <div class="status-badge">
        <span class="status-dot"></span>
        SISTEMA OPERACIONAL
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Estatísticas com cards
    if lojas:
        total = len(lojas)
        ativas = sum(1 for l in lojas if l.get("status") == "open")
        st.markdown(f"""
        <style>
            .stat-row {
                display: flex;
                gap: 12px;
                margin-bottom: 16px;
            }
            .stat-box {
                flex: 1;
                background: rgba(255,255,255,0.05);
                border-radius: 8px;
                padding: 12px;
                text-align: center;
            }
            .stat-num {
                font-size: 24px;
                font-weight: bold;
                color: white;
            }
            .stat-label {
                font-size: 10px;
                color: rgba(255,255,255,0.5);
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        </style>
        <div class="stat-row">
            <div class="stat-box">
                <div class="stat-num">{total}</div>
                <div class="stat-label">Lojas</div>
            </div>
            <div class="stat-box">
                <div class="stat-num" style="color: #22c55e;">{ativas}</div>
                <div class="stat-label">Ativas</div>
            </div>
            <div class="stat-box">
                <div class="stat-num" style="color: #f59e0b;">{total - ativas}</div>
                <div class="stat-label">Inativas</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("Nenhuma loja carregada")
    
    st.markdown("---")
    
    # Contato
    st.markdown("**Precisa de ajuda?**")
    st.info("📞 Ligue: (11) 3274-7527")
    
    st.markdown("---")
    
    # Footer com usuário
    st.markdown(f"""
    <style>
        .user-footer {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .user-avatar {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }
        .user-info {
            flex: 1;
        }
        .user-name {
            font-size: 13px;
            font-weight: 600;
            color: white;
        }
        .user-role {
            font-size: 10px;
            color: rgba(255,255,255,0.5);
        }
        .logout-btn {
            background: rgba(239, 68, 68, 0.2);
            border: none;
            border-radius: 6px;
            padding: 6px;
            cursor: pointer;
            color: #ef4444;
            font-size: 14px;
        }
    </style>
    <div class="user-footer">
        <div class="user-avatar">👤</div>
        <div class="user-info">
            <div class="user-name">Enzo Maranho</div>
            <div class="user-role">Analista T.I.</div>
        </div>
        <button class="logout-btn" title="Sair">🚪</button>
    </div>
    <p style="text-align: center; font-size: 9px; color: rgba(255,255,255,0.3); margin-top: 8px; font-family: monospace;">
        Jarvis v5.0 • T.I. DPSP
    </p>
    """, unsafe_allow_html=True)
    
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
