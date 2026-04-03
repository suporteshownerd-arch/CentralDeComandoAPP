"""
Página Home - Início com logo
"""

import streamlit as st


def render_page():
    st.markdown("""
    <style>
        .home-logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 70vh;
            text-align: center;
        }
        .home-logo {
            font-size: 120px;
            margin-bottom: 24px;
            display: block;
            filter: drop-shadow(0 8px 32px rgba(99, 102, 241, 0.4));
        }
        .home-title {
            font-size: 36px;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 8px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            letter-spacing: 2px;
        }
        .home-subtitle {
            font-size: 14px;
            color: var(--text2);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="home-logo-container">
        <span class="home-logo">🛡️</span>
        <h1 class="home-title">CENTRAL DE COMANDO</h1>
        <p class="home-subtitle">DPSP T.I. • Sistema de Gestão de Lojas</p>
    </div>
    """, unsafe_allow_html=True)