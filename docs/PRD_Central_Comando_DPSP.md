# PRD — Central de Comando DPSP
**Product Requirements Document**
**Versão:** 3.1 — Atualizado
**Data:** 2026-04-03
**Desenvolvedor:** Enzo Maranho — DPSP T.I.

---

## 1. VISÃO GERAL

### 1.1 Objetivo
A **Central de Comando DPSP** é uma aplicação web interna para a equipe de TI da DPSP (Drogarias Super Pharmacie), focada em:

- Consultar informações de 2000+ lojas (farmácias) por VD, nome, endereço ou texto livre
- Gerar templates padronizados para alertas executivos e gestão de crises
- Automatizar a abertura de chamados com operadoras de telecom (Vivo e Claro)
- Registrar histórico de comunicações em Google Sheets
- Exibir dashboard com KPIs operacionais

### 1.2 Contexto Operacional
- **Contato Central:** central.comando@dpsp.com.br | (11) 3274-7527
- **TI DPSP:** (11) 5529-6003
- **Plataforma:** Streamlit — Streamlit Cloud (público) + local
- **Público:** Equipe de TI e Central de Comando DPSP

---

## 2. ESTRUTURA DE ARQUIVOS

```
CentralDeComandoAPP/
├── app.py                        # Entry point Streamlit
├── requirements.txt              # Dependências Python
├── README.md                     # Documentação de usuário
├── .streamlit/
│   └── config.toml               # Tema dark + configurações (commitado no git)
├── data/
│   ├── loader.py                 # Carregamento CSV + Fernet + cache (TTL 300s)
│   ├── loader_pandas.py          # Loader alternativo com Pandas
│   ├── relacao.csv(.enc)         # Dados mestres das lojas (~2055 lojas)
│   ├── designacao.csv(.enc)      # Designações de circuito MPLS/INN
│   ├── GGL.csv(.enc)             # Gerentes Gerais de Loja
│   └── GR.csv(.enc)              # Gerentes Regionais
├── pg/                           # Páginas do sistema (ATENÇÃO: pg/, não pages/)
│   ├── consulta_lojas.py         # Consulta de lojas
│   ├── gestao_crises.py          # Gestão de crises
│   ├── abertura_chamados.py      # Abertura de chamados
│   ├── historico.py              # Histórico/auditoria
│   ├── dashboard.py              # Dashboard com KPIs
│   ├── ajuda.py                  # Ajuda/FAQ
│   └── __init__.py
├── components/
│   ├── styles.py                 # Sistema de design e CSS global
│   ├── ui.py                     # Componentes reutilizáveis (cards, badges)
│   ├── nav.py                    # Navegação e sidebar (botões, não radio)
│   └── __init__.py
├── templates/
│   └── __init__.py               # Funções de geração de templates
└── utils/
    └── sheets.py                 # Integração Google Sheets API
```

> **Nota importante:** O diretório de páginas é `pg/` (não `pages/`). O nome `pages/` foi
> evitado intencionalmente — o Streamlit auto-descobre esse diretório e cria rotas separadas,
> quebrando a navegação via session_state.

---

## 3. STACK TECNOLÓGICO

| Camada | Tecnologia | Versão mínima |
|--------|-----------|--------------|
| Frontend/Framework | Streamlit | >= 1.28.0 |
| Linguagem | Python | >= 3.9 |
| Encriptação | cryptography (Fernet) | >= 41.0.0 |
| Dados | pandas | >= 2.0.0 |
| Gráficos | plotly | >= 5.18.0 |
| Google Sheets | gspread | >= 5.12.0 |
| Auth Google | google-auth | >= 2.23.0 |
| Env vars | python-dotenv | >= 1.0.0 |
| Fuzzy search | rapidfuzz | >= 3.0.0 (opcional) |

---

## 4. MODELO DE DADOS

### 4.1 Entidade: Loja (campos completos)
```python
{
    # Identificação
    "vd":        str,   # Virtual Depot ID (identificador principal, ex: "2015")
    "nome":      str,   # Nome da loja (ex: "DSP VILLA LOBOS (MATRIZ)")
    "bandeira":  str,   # Bandeira da loja (ex: "DSP", "RD")
    "cnpj":      str,   # CNPJ

    # Endereço
    "endereco":  str,
    "bairro":    str,
    "cidade":    str,
    "estado":    str,
    "cep":       str,

    # Região
    "regiao":    str,   # Região GGL (ex: "SP AMERICANA")
    "regiao_gr": str,   # Região GR  (ex: "SP INTERIOR")
    "regiao_div":str,   # Região DIV (ex: "SP")

    # Contatos
    "tel":       str,   # Telefone 1
    "tel2":      str,   # Telefone 2
    "cel":       str,   # Celular
    "email":     str,

    # Operação
    "horario":   str,   # "Seg-Sex HH:MM | Sáb HH:MM | Dom HH:MM"
    "status":    str,   # "open" | "closed"
    "cluster":   str,   # ex: "AR_G"
    "tipo_loja": str,   # ex: "Meio de Quadra"
    "cd":        str,   # CD Supridor (ex: "VD910")

    # Gestores
    "ggl":       str,   # Nome do Gerente Geral de Loja
    "ggl_tel":   str,
    "gr":        str,   # Nome do Gerente Regional
    "gr_tel":    str,

    # Circuitos de telecom
    "mpls":      str,   # Designação do circuito MPLS (Tipo de acesso = "VPN IP MPLS")
    "inn":       str,   # Designação do circuito INN  (Tipo de acesso = "INN")
    "circuitos": list,  # Lista completa: [{"op": str, "tipo": str, "des": str}]
}
```

### 4.2 Fontes de Dados (CSVs Encriptados)

| Arquivo | Conteúdo | Campo-chave | Campos relevantes |
|---------|----------|-------------|-------------------|
| `relacao.csv(.enc)` | Dados mestres das lojas | `CODIGO` (= VD) | LOJAS, STATUS, REGIAO GGL, NOME GGL/GR, ENDEREÇO, BAIRRO, CIDADE, ESTADO, CEP, CNPJ, TELEFONE1/2, CELULAR, E-MAIL, 2ª a 6ª, SAB, DOM, BANDEIRA, CLUSTER, TIPO LOJA, CD SUPRIDOR |
| `designacao.csv(.enc)` | Circuitos MPLS/INN | `People` (= VD) | Operadora, Número (Designação), **Tipo de acesso**, Status |
| `GGL.csv(.enc)` | Gerentes Gerais de Loja | `NOME GGL` | CELULAR |
| `GR.csv(.enc)` | Gerentes Regionais | `NOME GR` | CELULAR.1 |

> **Nota sobre designacao.csv:** A classificação de circuito usa o campo **`Tipo de acesso`**,
> não o campo `Operadora`. Valores: `"VPN IP MPLS"` → circuito principal (mpls),
> `"INN"` → circuito backup (inn). Linhas com `Status = "INATIVO"` são ignoradas.

---

## 5. ARQUITETURA E FLUXOS

### 5.1 Fluxo de Carregamento de Dados
```
Startup da App (app.py)
  │
  └→ DataLoader.__init__(master_key)
       │
       ├→ _init_fernet()          # Configura cipher com MASTER_KEY do .env/.streamlit/secrets.toml
       │
       └→ get_lojas() [sob demanda, via @st.cache_resource]
            ├→ CacheManager.get("all_lojas")
            │     └─ [HIT] return cached data (TTL = 300s)
            │
            └─ [MISS] _load_from_csv()
                  ├→ Lê relacao.csv(.enc)  ← prefere .enc se cipher disponível
                  ├→ Fernet.decrypt(bytes) → CSV string
                  ├→ csv.DictReader → list[dict]
                  ├→ Merge com designacao.csv(.enc) via People=VD
                  ├→ Merge com GGL.csv(.enc) via NOME GGL
                  ├→ Merge com GR.csv(.enc)  via NOME GR
                  ├→ CacheManager.set("all_lojas", data, ttl=300)
                  └→ [FALLBACK] _get_sample_data() se CSVs indisponíveis
```

### 5.2 Fluxo de Consulta de Lojas
```
pg/consulta_lojas.py
  │
  ├→ st.text_input("Buscar loja")
  ├→ st.selectbox("Modo de busca")
  │     Modos: "VD / Designação" | "Nome de Loja" | "Endereço" | "Outra Informação"
  │
  ├→ DataLoader.buscar_loja(termo, modo)
  │     ├─ VD / Designação:
  │     │   ├─ termo ≤ 4 dígitos → match EXATO por VD
  │     │   └─ termo longo/alfanumérico → busca em mpls, inn, circuitos
  │     ├─ Nome de Loja:  substring no nome
  │     ├─ Endereço:      substring em endereço/cidade/bairro/cep
  │     └─ Outra Informação: substring em blob (nome, ggl, gr, email, tel, cnpj, cd, cidade, estado)
  │         + fuzzy fallback via rapidfuzz (se instalado)
  │
  └→ components/ui.py → render_card(loja)
        Exibe: VD, nome, CNPJ, endereço, contatos,
               gerentes (GGL/GR), circuitos (MPLS/INN)
        Ações: ⭐ Favoritar | 📋 Detalhes | 📞 Gerar Chamado
```

### 5.3 Fluxo de Gestão de Crises
```
pg/gestao_crises.py
  │
  ├─ [Tab 1] Alertas Executivos
  │   ├→ Escopo: Internet MPLS | INN | Sistema PDV | ERP | VPN | DC | Energia
  │   ├→ templates.gerar_alerta_executivo(tipo, dados)
  │   │   └→ 🔴 Abertura | 🟡 Atualização | 🟢 Normalização
  │   └→ render_template_box(template) + botão copiar
  │
  ├─ [Tab 2] Gestão de Crise
  │   ├→ número incidente, sala de crise, unidades afetadas,
  │   │   causa, responsável técnico, nível de crise
  │   └→ Auto-calcula próxima atualização (+30min)
  │
  └─ [Tab 3] Loja Isolada
      ├→ Tipo: Energia Elétrica | Internet/Conectividade
      ├→ VD da loja → lookup DataLoader
      └→ Gera par: Abertura + Fechamento
```

### 5.4 Fluxo de Abertura de Chamados
```
pg/abertura_chamados.py
  │
  ├→ Busca loja por VD (preenche campos automaticamente)
  │
  ├─ [Vivo MVE]
  │   Campos: Nome, Telefone, Email, Designação MPLS, VD, Início, Horário
  │   → Gera texto formatado para portal Vivo MVE
  │
  └─ [Claro Empresas]
      Campos: Designação INN/MPLS, Unidade (VD + Nome), Endereço, Hora Incidente
      → Gera texto formatado para portal Claro Empresas
```

### 5.5 Fluxo de Histórico
```
utils/sheets.py → GoogleSheetsManager
  │
  ├→ salvar_template(tipo, subtipo, label, texto)
  │   ├→ sheets_api.append_row([timestamp, tipo, subtipo, label, texto])
  │   ├→ Auto-rotação: mantém max 99 registros por aba
  │   └─ [FALLBACK] SQLite: data/historico.db
  │
  └→ listar_templates(tipo)
      └→ Renderiza em pg/historico.py com cards
```

### 5.6 Navegação (session_state)
```
components/nav.py
  │
  ├→ st.button() por item do menu (NÃO st.radio)
  ├→ Tecnica CSS: .nav-active-marker + div[stButton] > button
  └→ st.session_state.nav_page → routing em app.py
```

---

## 6. COMPONENTES DE UI

### 6.1 Sistema de Design (components/styles.py)

**Paleta de Cores:**
```css
--bg:      #08090d   /* Background principal */
--bg2:     #0f1118   /* Background cards */
--bg3:     #161920   /* Background terciário */
--surface: #1c2029   /* Inputs e superfícies */
--text:    #eaecf0   /* Texto primário */
--text2:   #9094a6   /* Texto secundário */
--text3:   #5c6370   /* Texto terciário */
--accent:  #5b8def   /* Azul — ação principal */
--green:   #34d399   /* Sucesso */
--red:     #f87171   /* Erro */
--amber:   #fbbf24   /* Alerta */
--purple:  #a78bfa   /* Acento extra */
--cyan:    #22d3ee   /* Info */
```

**Tipografia:**
- **Syne** (600–800): H1, H2, H3
- **DM Sans** (300–600): Corpo e botões
- **DM Mono** (400–500): VD, código, dados técnicos

**Tema Streamlit** (`.streamlit/config.toml`):
```toml
[theme]
primaryColor = "#5b8def"
backgroundColor = "#08090d"
secondaryBackgroundColor = "#0f1118"
textColor = "#eaecf0"
```

### 6.2 Componentes Principais (components/ui.py)

| Componente | Função |
|-----------|--------|
| `render_card(loja)` | Card completo da loja com todos os dados |
| `render_vd_badge(vd)` | Badge monospace com VD |
| `render_status_badge(status)` | Badge verde/vermelho de status |
| `render_template_box(texto)` | Caixa copiável para templates |
| `render_toast(msg, tipo)` | Notificação pop-up |
| `render_metric_card(label, valor)` | Card de KPI para dashboard |

### 6.3 Navegação (components/nav.py)
```
Sidebar
  ├─ Logo + versão
  ├─ KPIs: Total / Ativas / Inativas (barra de progresso)
  ├─ Botões de navegação (st.button, active via CSS marker)
  │     🏪 Consulta de Lojas
  │     🚨 Gestão de Crises
  │     📞 Abertura de Chamados
  │     📋 Histórico
  │     📈 Dashboard
  │     ❓ Ajuda
  ├─ ⭐ Favoritos (últimos 5)
  └─ Contatos fixos (Central + TI DPSP)
```

---

## 7. INTEGRAÇÕES EXTERNAS

### 7.1 Google Sheets API
- **Biblioteca:** gspread + google-auth
- **Auth:** Service Account (JSON via env var `GCP_SERVICE_ACCOUNT`)
- **Planilhas:**
  - `SHEETS_ID_AEXEC` → Alertas Executivos (aba "AExec")
  - `SHEETS_ID_GCRISES` → Gestão de Crises (aba "GCrises")
- **Limite:** 99 registros por aba com auto-rotação (deleta mais antigo)
- **Fallback:** SQLite `data/historico.db`

### 7.2 Portais de Telecom
| Operadora | Portal | Circuito |
|-----------|--------|---------|
| Vivo | MVE Portal | MPLS (Tipo de acesso = "VPN IP MPLS") |
| Claro | Claro Empresas | INN (Tipo de acesso = "INN") |

---

## 8. SEGURANÇA E ENCRIPTAÇÃO

### 8.1 Implementado
- Arquivos CSV encriptados com **Fernet** (simétrico, autenticado)
- Secrets em variáveis de ambiente (`.env` local / Streamlit Cloud secrets)
- Log de uso para auditoria (`UsageLogger` em `data/loader.py`)
- `.streamlit/secrets.toml` no `.gitignore` (nunca commitado)

### 8.2 Variáveis de Ambiente Necessárias
```bash
MASTER_KEY="<base64_32bytes>"          # Chave Fernet para decriptar CSVs
GCP_SERVICE_ACCOUNT='{"type":"service_account",...}'  # SA Google Cloud
SHEETS_ID_AEXEC="<spreadsheet_id>"    # ID da planilha de alertas executivos
SHEETS_ID_GCRISES="<spreadsheet_id>"  # ID da planilha de crises
```

### 8.3 Riscos Identificados
| Risco | Severidade | Mitigação Recomendada |
|-------|-----------|----------------------|
| Sem autenticação de usuário | Alta | Implementar SSO (Azure AD) ou auth plugin |
| SQLite fallback sem encriptação | Média | Encriptar banco SQLite |
| Sem validação de inputs nos formulários | Baixa | Sanitizar campos de crise |

---

## 9. DASHBOARD — KPIs

| Métrica | Fonte | Cálculo |
|---------|-------|---------|
| Total de Lojas | relacao.csv | `len(lojas)` |
| Lojas Ativas | relacao.csv | `status == "open"` |
| Lojas Inativas | relacao.csv | `status == "closed"` |
| Estados atendidos | relacao.csv | `len(set(l["estado"]))` |
| Distribuição por Estado | relacao.csv | `groupby(estado).count()` |
| Distribuição por Região | relacao.csv | `groupby(regiao).count()` |

---

## 10. PERFORMANCE

| Operação | Complexidade | Tempo Típico |
|---------|-------------|-------------|
| Carregamento inicial (CSV + decrypt) | O(n) | 2–5s |
| Busca de loja | O(n) linear scan | < 200ms |
| Salvar no Sheets | O(1) API call | ~500ms |
| Cache hit | O(1) | < 1ms |

**Gargalos:**
- Decriptação CSV no primeiro load (mitigado por `@st.cache_resource`)
- Busca linear em ~2055 registros (aceitável, sem índice invertido)
- Latência Google Sheets API (~500ms/chamada)

---

## 11. STATUS DE IMPLEMENTAÇÃO

### Completo ✅
- Carregamento de dados reais (~2055 lojas via CSV Fernet)
- Consulta de lojas — 4 modos de busca (VD/Designação, Nome, Endereço, Outra Info)
- Busca VD: exact match ≤ 4 dígitos; busca designação para entradas longas/alfanuméricas
- Detecção de circuito MPLS/INN via campo `Tipo de acesso` (não Operadora)
- Geração de templates de crise (Alertas Executivos, Gestão de Crise, Loja Isolada)
- Geração de chamados Vivo/Claro
- Dashboard com KPIs
- Tema escuro via `.streamlit/config.toml` (commitado)
- Sidebar com navegação por botões (não radio) + CSS active state
- Integração Google Sheets + fallback SQLite
- Encriptação Fernet dos dados
- Cache em memória com TTL 300s
- Biblioteca de componentes UI

### Parcial ⚠️
- Histórico/Auditoria (leitura limitada das sheets)
- Tratamento de erros em edge cases

### Não Implementado ❌
- Autenticação/Autorização (SSO/Azure AD)
- Filtros avançados na UI (estado, região, cluster)
- Sistema de favoritos persistente (apenas session_state)
- Export PDF/Excel dos dados de loja
- Webhooks para Telegram
- Integração ServiceNow
- Progressive Web App (modo offline)
- Atalhos de teclado
- Acessibilidade WCAG

---

## 12. ROADMAP

### Q2 2026 — Dados & Integração
- [ ] Filtros avançados na UI (estado, região, status, bandeira)
- [ ] Sistema de favoritos persistente (localStorage ou Sheets)
- [ ] Auto-complete na busca
- [ ] Sync automático dos CSVs

### Q3 2026 — Automação
- [ ] Integração ServiceNow (auto-criação de tickets)
- [ ] Webhooks Telegram para notificações
- [ ] Export PDF/Excel dos detalhes de loja
- [ ] Modo wizard para novos usuários

### Q4 2026 — Enterprise
- [ ] SSO (Active Directory/Azure AD)
- [ ] Logs de auditoria completos
- [ ] Notificações em tempo real

---

## 13. INSTRUÇÕES DE EXECUÇÃO

```bash
# Navegar para o projeto
cd /home/pop-os-jonh/Documentos/Jarvis/CentralDeComandoAPP

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com as chaves corretas

# Executar
streamlit run app.py
```

**Acesso:** http://localhost:8501

**Para atualizar dados (sync XLSX → CSV enc):**
```bash
cd "../consulta lojas python"
python relacaocheck.py
```

---

## 14. CONTATOS

| Papel | Contato |
|-------|---------|
| Desenvolvedor | Enzo Maranho — DPSP T.I. |
| Central de Comando | central.comando@dpsp.com.br |
| Telefone Central | (11) 3274-7527 |
| TI DPSP | (11) 5529-6003 |
