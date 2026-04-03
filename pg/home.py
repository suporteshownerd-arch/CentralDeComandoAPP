"""
Página Home - Início com logo
"""

import streamlit as st
from datetime import datetime


def render_page():
    # Header com logo
    st.markdown("""
    <style>
        .home-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 24px;
            padding: 60px 40px;
            text-align: center;
            margin-bottom: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            position: relative;
            overflow: hidden;
        }
        .home-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 50% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        }
        .home-logo {
            font-size: 100px;
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }
        .home-title {
            font-size: 48px;
            font-weight: bold;
            color: white;
            margin-bottom: 12px;
            position: relative;
            z-index: 1;
            letter-spacing: 2px;
        }
        .home-subtitle {
            font-size: 18px;
            color: #888;
            position: relative;
            z-index: 1;
        }
        .home-version {
            display: inline-block;
            background: rgba(102, 126, 234, 0.2);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px;
            color: #667eea;
            margin-top: 16px;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(34, 197, 94, 0.15);
            padding: 8px 16px;
            border-radius: 20px;
            color: #22c55e;
            font-size: 13px;
            margin-top: 20px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.9); }
        }
    </style>
    <div class="home-header">
        <div class="home-logo">🛡️</div>
        <div class="home-title">CENTRAL DE COMANDO</div>
        <div class="home-subtitle">DPSP T.I. • Sistema de Gestão de Lojas</div>
        <div class="status-badge">
            <span class="status-dot"></span>
            SISTEMA OPERACIONAL
        </div>
        <div class="home-version">v5.0 • Jarvis</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data e hora
    now = datetime.now()
    st.markdown(f"""
    <div style="text-align: center; color: #666; margin-bottom: 30px;">
        {now.strftime('%d/%m/%Y')} • {now.strftime('%H:%M')}
    </div>
    """, unsafe_allow_html=True)
    
    # Instrução
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        margin-bottom: 20px;
    ">
        <div style="font-size: 40px; margin-bottom: 16px;">👈</div>
        <div style="font-size: 18px; color: white; margin-bottom: 8px;">Selecione uma opção no menu lateral</div>
        <div style="font-size: 14px; color: #888;">Navegue pelas opções para acessar as funcionalidades do sistema</div>
    </div>
    """, unsafe_allow_html=True)