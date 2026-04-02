"""
Página de Ajuda e FAQ
Central de Comando DPSP v2.0
"""

import streamlit as st
from components import render_faq_item


FAQS = [
    {
        "pergunta": "🔍 Como buscar uma loja?",
        "resposta": """
1. Selecione o modo de busca (VD/Designação, Endereço, Nome ou Livre)
2. Digite o termo de busca no campo de pesquisa
3. O sistema irá mostrar sugestões automaticamente
4. Clique na loja desejada para ver todos os detalhes
        """
    },
    {
        "pergunta": "📋 Como abrir um chamado?",
        "resposta": """
1. Busque a loja pelo VD
2. Clique no botão "Chamados" no card da loja
3. Selecione a operadora (Vivo ou Claro)
4. Copie o texto gerado e cole no portal da operadora
        """
    },
    {
        "pergunta": "⚠️ Como criar um alerta de crise?",
        "resposta": """
1. Acesse "Gestão de Crises" no menu
2. Escolha o tipo: Alertas Executivos, Gestão de Crise ou Loja Isolada
3. Preencha os campos necessários
4. Clique em "Gerar" para criar o template
5. Copie ou salve o informativo
        """
    },
    {
        "pergunta": "⭐ Como usar favoritos?",
        "resposta": """
1. Ao buscar uma loja, clique no botão de estrela (☆)
2. A loja será adicionada aos favoritos na sidebar
3. Você pode acessar rapidamente suas lojas favoritadas
        """
    },
    {
        "pergunta": "⌨️ Quais são os atalhos de teclado?",
        "resposta": """
• **Ctrl+K**: Abrir busca rápida
• **1-4**: Navegar entre as abas do menu
• **Esc**: Fechar modais
        """
    },
    {
        "pergunta": "📥 Como exportar dados das lojas?",
        "resposta": """
1. Vá para "Consulta de Lojas"
2. Clique em "Exportar" no canto superior esquerdo
3. Escolha entre CSV ou JSON
4. Clique em "Download" para salvar o arquivo
        """
    },
    {
        "pergunta": "💾 Como salvar templates?",
        "resposta": """
1.Após gerar um template (crise, alerta, etc), clique em "Salvar"
2. O sistema tentará salvar no Google Sheets
3. Se não houver configuração, salvará localmente no SQLite
        """
    },
    {
        "pergunta": "📊 Onde vejo as estatísticas de uso?",
        "resposta": """
Acesse a página "Dashboard" no menu para ver:
• Número de buscas e chamados do dia
• Status das lojas (abertas/fechadas)
• Distribuição por estado
• Histórico de uso dos últimos 7 dias
        """
    }
]


def render_page():
    """Renderiza a página de Ajuda e FAQ"""
    st.markdown("## ❓ Ajuda e FAQ")
    st.markdown("*Perguntas frequentes e instruções de uso*")
    
    # FAQ com expanders
    for faq in FAQS:
        with st.expander(faq["pergunta"], expanded=True):
            st.markdown(faq["resposta"])
    
    st.markdown("---")
    
    # Contatos de suporte
    st.markdown("### 📞 Contato de Suporte")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        st.markdown("""
        **T.I. DPSP**
        📞 (11) 5529-6003
        """)
    
    with col_c2:
        st.markdown("""
        **Central de Comando**
        📞 (11) 3274-7527
        """)
    
    with col_c3:
        st.markdown("""
        **E-mail**
        📧 central.comando@dpsp.com.br
        """)
    
    st.markdown("---")
    
    # Links úteis
    st.markdown("### 🔗 Links Úteis")
    
    col_l1, col_l2 = st.columns(2)
    
    with col_l1:
        st.markdown("""
        - [Portal Vivo MVE](https://mve.vivo.com.br)
        - [Claro Empresas](https://webebt01.embratel.com.br/claroempresasonline/index)
        """)
    
    with col_l2:
        st.markdown("""
        - [GitHub do Projeto](https://github.com/suporteshownerd-arch/CentralDeComandoAPP)
        - [Documentação PRD](./PRD_MELHORIAS_CONTINUAS.md)
        """)