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
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .metric-value {
            font-size: 42px;
            font-weight: bold;
            color: white;
        }
        .metric-label {
            font-size: 14px;
            color: #888;
            margin-top: 8px;
        }
        .metric-delta {
            font-size: 12px;
            margin-top: 4px;
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
            <div class="metric-value" style="color: #22c55e;">✅ {ativas}</div>
            <div class="metric-label">Lojas Ativas</div>
            <div class="metric-delta" style="color: #22c55e;">{pct_ativas}% do total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pct_inativas = round(inativas/total*100) if total > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #ef4444;">❌ {inativas}</div>
            <div class="metric-label">Lojas Inativas</div>
            <div class="metric-delta" style="color: #ef4444;">{pct_inativas}% do total</div>
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
                    background: rgba(239, 68, 68, 0.1);
                    border-left: 4px solid #ef4444;
                    padding: 12px;
                    border-radius: 8px;
                    margin-bottom: 8px;
                ">
                    <strong>{loja.get('nome', 'Loja')}</strong><br>
                    <small style="color: #888;">{loja.get('cidade', '')}/{loja.get('estado', '')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                background: rgba(34, 197, 94, 0.1);
                border-left: 4px solid #22c55e;
                padding: 16px;
                border-radius: 8px;
            ">
                ✅ Nenhuma loja com problemas!
            </div>
            """, unsafe_allow_html=True)
    
    with col_lojas:
        st.markdown("### 🏪 Lojas Recentes")
        
        for i, loja in enumerate(lojas[:8]):
            status = loja.get("status", "open")
            status_color = "#22c55e" if status == "open" else "#ef4444"
            status_emoji = "✅" if status == "open" else "❌"
            
            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.03);
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 10px;
            ">
                <span style="color: {status_color}; font-size: 18px;">{status_emoji}</span>
                <div>
                    <strong>{loja.get('nome', 'Loja')}</strong><br>
                    <small style="color: #888;">{loja.get('cidade', '')}/{loja.get('estado', '')}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)