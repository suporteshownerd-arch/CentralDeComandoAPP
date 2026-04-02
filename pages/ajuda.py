"""
Página de Ajuda
Central de Comando DPSP v3.0
"""

import streamlit as st


_FAQ = [
    ("Como buscar uma loja?",
     "Vá em **Consulta de Lojas**, digite o VD (número), nome ou endereço e escolha o modo de busca. "
     "Use os filtros avançados para restringir por Estado, Região ou Status."),

    ("O que é VD?",
     "VD (Virtual Depot) é o identificador único de cada loja no sistema DPSP. "
     "É um número de até 6 dígitos (ex: 2015, 318)."),

    ("O que é MPLS e INN?",
     "São as designações dos circuitos de internet de cada loja:\n"
     "- **MPLS** → Circuito principal Vivo (usado para abrir chamado Vivo MVE)\n"
     "- **INN** → Circuito Claro Empresas (usado para abrir chamado Claro)"),

    ("Como abrir chamado na Vivo?",
     "1. Vá em **Abertura de Chamados**\n"
     "2. Digite o VD da loja — os campos são preenchidos automaticamente\n"
     "3. Informe seu nome e a hora do incidente\n"
     "4. Selecione **Apenas Vivo** e clique em Gerar\n"
     "5. Copie o texto gerado e cole no portal Vivo MVE"),

    ("Como abrir chamado na Claro?",
     "1. Vá em **Abertura de Chamados**\n"
     "2. Digite o VD → campos preenchidos automaticamente\n"
     "3. Informe hora do incidente\n"
     "4. Selecione **Apenas Claro** e clique em Gerar\n"
     "5. Copie o texto e cole no portal Claro Empresas"),

    ("Como gerar um Alerta Executivo?",
     "1. Vá em **Gestão de Crises** → aba **Alertas Executivos**\n"
     "2. Escolha o Escopo (Internet MPLS, POS, ERP, etc.)\n"
     "3. Preencha os campos: abrangência, equipes, status\n"
     "4. Marque quais templates gerar (Abertura / Atualização / Normalização)\n"
     "5. Clique **Gerar** → copie o texto e envie no grupo executivo"),

    ("Como registrar uma Loja Isolada?",
     "1. Vá em **Gestão de Crises** → aba **Loja Isolada**\n"
     "2. Digite o VD da loja\n"
     "3. Selecione o tipo: **Energia Elétrica** ou **Internet**\n"
     "4. Informe horário de início e previsão de retorno\n"
     "5. Clique **Gerar** → dois templates são criados: Abertura e Fechamento"),

    ("Como favoritar uma loja?",
     "Na **Consulta de Lojas**, abra os detalhes de qualquer loja e clique em **☆ Favoritar**. "
     "Lojas favoritadas aparecem no topo da consulta e na sidebar. Limite de 10 favoritos."),

    ("O histórico não está aparecendo, o que fazer?",
     "O histórico requer conexão com o Google Sheets ou banco local SQLite. Verifique:\n"
     "- Se as variáveis `GCP_SERVICE_ACCOUNT`, `SHEETS_ID_AEXEC` e `SHEETS_ID_GCRISES` estão no `.env`\n"
     "- Se há templates já salvos (clique em **💾 Salvar** após gerar um template)\n"
     "- Clique em 🔄 **Atualizar** na página de Histórico"),

    ("Os dados das lojas estão desatualizados, o que fazer?",
     "Os dados vêm de arquivos CSV encriptados sincronizados pelo script `relacaocheck.py`. "
     "Para atualizar:\n"
     "1. Execute `python relacaocheck.py` no diretório `consulta lojas python/`\n"
     "2. Certifique-se de que a variável `MASTER_KEY` está no `.env`\n"
     "3. O script lê a planilha Excel da rede e gera novos `.csv.enc`"),
]

_GLOSSARIO = {
    "VD":           "Virtual Depot — identificador único da loja",
    "MPLS":         "Circuito internet principal (Vivo MVE)",
    "INN":          "Circuito internet secundário (Claro Empresas)",
    "GGL":          "Gerente Geral de Loja",
    "GR":           "Gerente Regional",
    "CD":           "Centro de Distribuição",
    "PDV":          "Ponto de Venda — sistema de caixa da loja",
    "ERP":          "Enterprise Resource Planning — sistema de gestão",
    "NOC":          "Network Operations Center — centro de operações de rede",
    "Loja Isolada": "Loja sem internet ou energia elétrica",
    "Fernet":       "Algoritmo de encriptação simétrica usado nos arquivos CSV",
    "TTL":          "Time To Live — tempo de vida do cache (padrão: 300s)",
}

_CONTATOS = [
    ("🎛️ Central de Comando", "(11) 3274-7527", "central.comando@dpsp.com.br"),
    ("💻 T.I. DPSP",           "(11) 5529-6003", ""),
]


def render_page():
    st.markdown("## ❓ Ajuda")
    st.markdown("*Guias rápidos, FAQ e contatos úteis*")

    tab_faq, tab_guia, tab_gloss, tab_cont = st.tabs([
        "🙋 FAQ", "📖 Guias Rápidos", "📚 Glossário", "📞 Contatos"
    ])

    # ── FAQ ───────────────────────────────────────────────────────────────────
    with tab_faq:
        st.markdown("### Perguntas Frequentes")
        for pergunta, resposta in _FAQ:
            with st.expander(pergunta):
                st.markdown(resposta)

    # ── Guias Rápidos ─────────────────────────────────────────────────────────
    with tab_guia:
        st.markdown("### Fluxo de Atendimento — Loja sem Internet")
        st.markdown("""
1. **Identificar a loja** — Consulta de Lojas → digitar VD
2. **Verificar circuitos** — confirmar designação MPLS e INN nos detalhes
3. **Registrar isolamento** — Gestão de Crises → Loja Isolada → gerar templates
4. **Abrir chamados** — Abertura de Chamados → gerar textos Vivo + Claro
5. **Comunicar gestão** — enviar template Loja Isolada no grupo WhatsApp
6. **Acompanhar** — quando normalizar, usar template de **Fechamento**
        """)

        st.markdown("---")
        st.markdown("### Fluxo de Crise Geral")
        st.markdown("""
1. **Identificar escopo** — qual sistema/rede está impactado?
2. **Gerar Alerta Executivo de Abertura** 🔴 — enviar para grupo executivo
3. **Abrir sala de crise** — criar link e registrar em Gestão de Crise
4. **Atualizar a cada 30min** — gerar template 🟡 Atualização com novo status
5. **Normalização** — quando resolver, gerar template 🟢 Normalização
6. **Salvar no histórico** — clique **💾 Salvar** após gerar o template
        """)

        st.markdown("---")
        st.markdown("### Como configurar o ambiente")
        st.code("""# 1. Copiar o arquivo de exemplo
cp .env.example .env

# 2. Editar o .env com os valores reais
MASTER_KEY=<chave_fernet_base64>
GCP_SERVICE_ACCOUNT={"type":"service_account",...}
SHEETS_ID_AEXEC=<id_planilha_alertas>
SHEETS_ID_GCRISES=<id_planilha_crises>

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar o app
streamlit run app.py""", language="bash")

    # ── Glossário ─────────────────────────────────────────────────────────────
    with tab_gloss:
        st.markdown("### Glossário de Termos")
        for termo, definicao in sorted(_GLOSSARIO.items()):
            st.markdown(f"**`{termo}`** — {definicao}")

    # ── Contatos ──────────────────────────────────────────────────────────────
    with tab_cont:
        st.markdown("### Contatos Úteis")
        for nome, tel, email in _CONTATOS:
            with st.container(border=True):
                st.markdown(f"**{nome}**")
                st.caption(f"📞 {tel}")
                if email:
                    st.caption(f"✉️ {email}")

        st.markdown("---")
        st.markdown("### Links dos Portais")
        st.markdown("- [Vivo MVE](https://mve.vivo.com.br)")
        st.markdown("- [Claro Empresas](https://webebt01.embratel.com.br/claroempresasonline/index)")

        st.markdown("---")
        st.caption("Central de Comando DPSP v3.0 · Desenvolvido por Enzo Maranho — T.I. DPSP · Uso Interno")
