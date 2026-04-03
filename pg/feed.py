"""
Página Feed - Visão geral do sistema
"""

import streamlit as st


def render_page(loader, lojas):
    st.markdown("## 📊 Feed")
    st.markdown("---")
    
    if not lojas:
        st.warning("Nenhuma loja carregada")
        return
    
    total = len(lojas)
    ativas = sum(1 for l in lojas if l.get("status") == "open")
    inativas = total - ativas
    estados = len({l.get("estado") for l in lojas if l.get("estado")})
    
    # Cards de métricas
    st.markdown("""
    <style>
        .metric-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px 16px;
            text-align: center;
            transition: all 0.2s ease;
        }
        .metric-card:hover {
            border-color: var(--border2);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }
        .metric-value {
            font-size: 36px;
            font-weight: 700;
            color: var(--text);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .metric-label {
            font-size: 12px;
            color: var(--text3);
            margin-top: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-family: 'JetBrains Mono', monospace;
        }
        .metric-delta {
            font-size: 11px;
            margin-top: 4px;
            font-family: 'JetBrains Mono', monospace;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">🏪 {total}</div>
            <div class="metric-label">Total de Lojas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pct_ativas = round(ativas/total*100) if total > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: var(--green-light);">✅ {ativas}</div>
            <div class="metric-label">Lojas Ativas</div>
            <div class="metric-delta" style="color: var(--green-light);">{pct_ativas}% do total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pct_inativas = round(inativas/total*100) if total > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: var(--red-light);">❌ {inativas}</div>
            <div class="metric-label">Lojas Inativas</div>
            <div class="metric-delta" style="color: var(--red-light);">{pct_inativas}% do total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">🗺️ {estados}</div>
            <div class="metric-label">Estados</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Alertas e Lojas em colunas
    col_alertas, col_lojas = st.columns(2)
    
    with col_alertas:
        st.markdown("### 🚨 Alertas Recentes")
        
        alertas = [l for l in lojas if l.get("status") != "open"]
        
        if alertas:
            for loja in alertas[:8]:
                st.markdown(f"""
                <div style="
                    background: var(--surface);
                    border: 1px solid rgba(239,68,68,0.2);
                    border-left: 4px solid var(--red-light);
                    padding: 14px;
                    border-radius: 10px;
                    margin-bottom: 8px;
                    transition: all 0.2s ease;
                ">
                    <div style="font-weight: 600; color: var(--text); font-family: 'Plus Jakarta Sans', sans-serif;">{loja.get('nome', 'Loja')}</div>
                    <small style="color: var(--text2); font-family: 'Plus Jakarta Sans', sans-serif;">{loja.get('cidade', '')}/{loja.get('estado', '')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                background: rgba(16,185,129,0.1);
                border: 1px solid rgba(16,185,129,0.2);
                border-left: 4px solid var(--green-light);
                padding: 16px;
                border-radius: 10px;
                color: var(--green-light);
                font-family: 'Plus Jakarta Sans', sans-serif;
            ">
                ✅ Nenhuma loja com problemas!
            </div>
            """, unsafe_allow_html=True)
    
    with col_lojas:
        st.markdown("### 🏪 Lojas Recentes")
        
        for i, loja in enumerate(lojas[:8]):
            status = loja.get("status", "open")
            status_color = "var(--green-light)" if status == "open" else "var(--red-light)"
            status_emoji = "✅" if status == "open" else "❌"
            
            st.markdown(f"""
            <div style="
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 10px;
                padding: 14px;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 12px;
                transition: all 0.2s ease;
            ">
                <span style="font-size: 18px;">{status_emoji}</span>
                <div>
                    <div style="font-weight: 600; color: var(--text); font-family: 'Plus Jakarta Sans', sans-serif;">{loja.get('nome', 'Loja')}</div>
                    <small style="color: var(--text2); font-family: 'Plus Jakarta Sans', sans-serif;">{loja.get('cidade', '')}/{loja.get('estado', '')}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)