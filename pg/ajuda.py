"""
Página de Ajuda
Central de Comando DPSP v3.1
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
     "O histórico requer conexão com o Google Sheets. Verifique:\n"
     "- Se as variáveis `GCP_SERVICE_ACCOUNT`, `SHEETS_ID_AEXEC` e `SHEETS_ID_GCRISES` estão no `.env`\n"
     "- Se há templates já salvos (clique em **💾 Salvar** após gerar um template)\n"
     "- Clique em 🔄 **Atualizar** na página de Histórico"),

    ("Os dados das lojas estão desatualizados, o que fazer?",
     "Os dados vêm de arquivos CSV encriptados. Para atualizar:\n"
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
    "CD":           "Centro de Distribuição Supridor",
    "PDV":          "Ponto de Venda — sistema de caixa da loja",
    "ERP":          "Enterprise Resource Planning — sistema de gestão",
    "NOC":          "Network Operations Center — centro de operações de rede",
    "Loja Isolada": "Loja sem internet ou energia elétrica",
    "Fernet":       "Algoritmo de encriptação simétrica usado nos CSVs",
    "TTL":          "Time To Live — tempo de vida do cache (padrão: 300s)",
}

_CONTATOS = [
    ("🎛️", "Central de Comando", "(11) 3274-7527", "551132747527", "central.comando@dpsp.com.br"),
    ("💻", "T.I. DPSP",          "(11) 5529-6003", "551155296003", ""),
]


def render_page():
    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="page-header">
            <div class="page-header-icon">❓</div>
            <div>
                <h2 class="page-title">Ajuda</h2>
                <p class="page-sub">Guias rápidos, FAQ e contatos úteis</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_faq, tab_guia, tab_gloss, tab_cont = st.tabs([
        "🙋  FAQ",
        "📖  Guias Rápidos",
        "📚  Glossário",
        "📞  Contatos",
    ])

    # ── FAQ ───────────────────────────────────────────────────────────────────
    with tab_faq:
        st.markdown(
            "<div style='font-family:DM Mono,monospace;font-size:9px;color:#5c6370;"
            "text-transform:uppercase;letter-spacing:.14em;margin-bottom:14px'>"
            f"{len(_FAQ)} perguntas frequentes</div>",
            unsafe_allow_html=True,
        )
        for pergunta, resposta in _FAQ:
            with st.expander(pergunta):
                st.markdown(resposta)

    # ── Guias Rápidos ─────────────────────────────────────────────────────────
    with tab_guia:
        with st.container(border=True):
            st.markdown(
                "<div style='font-family:Syne,sans-serif;font-weight:700;font-size:15px;"
                "color:#eaecf0;margin-bottom:12px'>🌐 Loja sem Internet</div>",
                unsafe_allow_html=True,
            )
            st.markdown("""
1. **Identificar a loja** — Consulta de Lojas → digitar VD
2. **Verificar circuitos** — confirmar designação MPLS e INN nos detalhes
3. **Registrar isolamento** — Gestão de Crises → Loja Isolada → gerar templates
4. **Abrir chamados** — Abertura de Chamados → gerar textos Vivo + Claro
5. **Comunicar gestão** — enviar template Loja Isolada no grupo WhatsApp
6. **Acompanhar** — quando normalizar, usar template de **Fechamento**
            """)

        with st.container(border=True):
            st.markdown(
                "<div style='font-family:Syne,sans-serif;font-weight:700;font-size:15px;"
                "color:#eaecf0;margin-bottom:12px'>🚨 Crise Geral</div>",
                unsafe_allow_html=True,
            )
            st.markdown("""
1. **Identificar escopo** — qual sistema/rede está impactado?
2. **Gerar Alerta Executivo de Abertura** 🔴 — enviar para grupo executivo
3. **Abrir sala de crise** — criar link e registrar em Gestão de Crise
4. **Atualizar a cada 30min** — gerar template 🟡 Atualização com novo status
5. **Normalização** — quando resolver, gerar template 🟢 Normalização
6. **Salvar no histórico** — clique **💾 Salvar** após gerar o template
            """)

        with st.container(border=True):
            st.markdown(
                "<div style='font-family:Syne,sans-serif;font-weight:700;font-size:15px;"
                "color:#eaecf0;margin-bottom:12px'>⚙️ Configurar o Ambiente</div>",
                unsafe_allow_html=True,
            )
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
        items_html = "".join(
            f"<div class='gloss-item'>"
            f"<div class='gloss-term'>{termo}</div>"
            f"<div class='gloss-def'>{definicao}</div>"
            f"</div>"
            for termo, definicao in sorted(_GLOSSARIO.items())
        )
        st.markdown(
            f"<div class='gloss-grid'>{items_html}</div>",
            unsafe_allow_html=True,
        )

    # ── Contatos ──────────────────────────────────────────────────────────────
    with tab_cont:
        st.markdown(
            "<div style='font-family:DM Mono,monospace;font-size:9px;color:#5c6370;"
            "text-transform:uppercase;letter-spacing:.14em;margin-bottom:12px'>Contatos Rápidos</div>",
            unsafe_allow_html=True,
        )
        for icon, nome, tel, wa_num, email in _CONTATOS:
            href = f"https://wa.me/{wa_num}" if wa_num else "#"
            email_html = (
                f"<div style='font-size:11px;color:#5c6370;margin-top:2px'>✉️ {email}</div>"
                if email else ""
            )
            st.markdown(
                f"<a href='{href}' target='_blank' class='contact-pill'>"
                f"<div class='contact-pill-icon'>{icon}</div>"
                f"<div>"
                f"<div class='contact-pill-name'>{nome}</div>"
                f"<div class='contact-pill-tel'>📞 {tel}</div>"
                f"{email_html}"
                f"</div>"
                f"</a>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='font-family:DM Mono,monospace;font-size:9px;color:#5c6370;"
            "text-transform:uppercase;letter-spacing:.14em;margin:20px 0 12px 0'>Portais</div>",
            unsafe_allow_html=True,
        )
        lc1, lc2 = st.columns(2)
        with lc1:
            st.markdown(
                "<div class='portal-card'>"
                "<div style='font-weight:700;font-size:13px;color:#eaecf0;margin-bottom:8px'>📱 Vivo MVE</div>"
                "<a href='https://mve.vivo.com.br' target='_blank'>→ Acessar portal</a>"
                "</div>",
                unsafe_allow_html=True,
            )
        with lc2:
            st.markdown(
                "<div class='portal-card'>"
                "<div style='font-weight:700;font-size:13px;color:#eaecf0;margin-bottom:8px'>🔵 Claro Empresas</div>"
                "<a href='https://webebt01.embratel.com.br/claroempresasonline/index' target='_blank'>→ Acessar portal</a>"
                "</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='margin-top:20px;text-align:center;font-size:11px;color:#5c6370'>"
            "Central de Comando DPSP v3.1 · Desenvolvido por Enzo Maranho — T.I. DPSP · Uso Interno"
            "</div>",
            unsafe_allow_html=True,
        )
