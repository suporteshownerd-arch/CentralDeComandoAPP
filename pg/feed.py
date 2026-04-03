"""
Página Feed - Comunicados e informações
"""

import streamlit as st
from datetime import datetime


def render_page(loader, lojas):
    st.markdown("## 📊 Feed")
    st.markdown("---")
    
    st.markdown("### 📢 Comunicados")
    
    # Card de comunicado exemplo
    st.markdown("""
    <style>
        .comunicado-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            transition: all 0.2s ease;
        }
        .comunicado-card:hover {
            border-color: var(--border2);
            transform: translateY(-2px);
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
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .comunicado-date {
            font-size: 11px;
            color: var(--text3);
            font-family: 'JetBrains Mono', monospace;
        }
        .comunicado-body {
            font-size: 13px;
            color: var(--text2);
            font-family: 'Plus Jakarta Sans', sans-serif;
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
    
    # Comunicados fixos (exemplo)
    comunicados = [
        {
            "icon": "🔧",
            "title": "Manutenção Programada",
            "date": datetime.now().strftime("%d/%m/%Y"),
            "body": "Atenção! Manutenção preventiva programada para o banco de dados neste sábado (05/04) das 02h às 06h. Pode haver instabilidade.",
            "tag": "aviso",
            "tag_text": "AVISO"
        },
        {
            "icon": "📱",
            "title": "Nova Versão Disponível",
            "date": datetime.now().strftime("%d/%m/%Y"),
            "body": "A versão 5.1 do sistema está disponível com melhorias na consulta de lojas e correção de bugs.",
            "tag": "info",
            "tag_text": "INFO"
        },
        {
            "icon": "⚠️",
            "title": "Alerta de Segurança",
            "date": datetime.now().strftime("%d/%m/%Y"),
            "body": "Recomendamos que todos alterem suas senhas periodicamente. Não compartilhe credenciais.",
            "tag": "alerta",
            "tag_text": "ALERTA"
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
    
    st.markdown("---")
    
    # Estátisticas rápidas
    if lojas:
        total = len(lojas)
        ativas = sum(1 for l in lojas if l.get("status") == "open")
        inativas = total - ativas
        
        st.markdown("### 📈 Resumo")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏪 Total", total)
        with col2:
            st.metric("✅ Ativas", ativas)
        with col3:
            st.metric("❌ Inativas", inativas)