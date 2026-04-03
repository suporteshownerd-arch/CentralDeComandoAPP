"""
Página Home - Início com logo
"""

import streamlit as st
from datetime import datetime


def render_page():
    st.markdown("""
    <style>
        :root {
            --bg: #0a0a0f;
            --bg2: #12121a;
            --bg3: #1a1a24;
            --surface: #222230;
            --surface2: #2a2a3a;
            --border: rgba(255,255,255,0.06);
            --border2: rgba(255,255,255,0.12);
            --text: #f0f0f5;
            --text2: #a0a0b0;
            --text3: #606070;
            --accent: #6366f1;
            --accent-light: #818cf8;
            --accent-glow: rgba(99,102,241,0.25);
            --green: #10b981;
            --green-light: #34d399;
            --purple: #a855f7;
        }
        
        .home-header {
            background: linear-gradient(135deg, var(--bg2) 0%, var(--bg3) 100%);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 48px 32px;
            text-align: center;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
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
            background: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99,102,241,0.15), transparent);
            pointer-events: none;
        }
        .home-logo {
            font-size: 72px;
            margin-bottom: 16px;
            position: relative;
            z-index: 1;
            display: block;
        }
        .home-title {
            font-size: 32px;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 8px;
            position: relative;
            z-index: 1;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .home-subtitle {
            font-size: 14px;
            color: var(--text2);
            position: relative;
            z-index: 1;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            color: var(--green-light);
            font-size: 12px;
            margin-top: 20px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 500;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--green-light);
            border-radius: 50%;
            animation: pulse 2s infinite;
            box-shadow: 0 0 8px var(--green);
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .home-version {
            display: inline-block;
            background: rgba(99,102,241,0.1);
            border: 1px solid rgba(99,102,241,0.2);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            color: var(--accent-light);
            margin-top: 16px;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .datetime-box {
            text-align: center;
            color: var(--text3);
            font-size: 13px;
            margin-bottom: 24px;
            font-family: 'JetBrains Mono', monospace;
        }
        
        .instruction-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 32px 24px;
            text-align: center;
            margin-bottom: 20px;
        }
        .instruction-icon {
            font-size: 36px;
            margin-bottom: 16px;
            display: block;
        }
        .instruction-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 8px;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .instruction-desc {
            font-size: 13px;
            color: var(--text2);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="home-header">
        <span class="home-logo">🛡️</span>
        <h1 class="home-title">CENTRAL DE COMANDO</h1>
        <p class="home-subtitle">DPSP T.I. • Sistema de Gestão de Lojas</p>
        <div class="status-badge">
            <span class="status-dot"></span>
            SISTEMA OPERACIONAL
        </div>
        <div class="home-version">v5.0 • Jarvis</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Data e hora
    now = datetime.now()
    st.markdown(f"""
    <div class="datetime-box">
        {now.strftime('%d/%m/%Y')} • {now.strftime('%H:%M')}
    </div>
    """, unsafe_allow_html=True)
    
    # Instrução
    st.markdown("""
    <div class="instruction-box">
        <span class="instruction-icon">👈</span>
        <div class="instruction-title">Selecione uma opção no menu lateral</div>
        <div class="instruction-desc">Navegue pelas opções para acessar as funcionalidades do sistema</div>
    </div>
    """, unsafe_allow_html=True)