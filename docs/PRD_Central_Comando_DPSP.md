# PRD — Central de Comando DPSP
**Product Requirements Document**
**Versão:** 3.0 — Análise Completa
**Data:** 2026-04-02
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
- **Plataforma:** Web app interna (Streamlit), acessível em rede local
- **Público:** Equipe de TI e Central de Comando DPSP

---

## 2. ESTRUTURA DE ARQUIVOS

```
/Jarvis/
├── CentralDeComandoAPP/              # Aplicação principal (v2.5 Stable)
│   ├── app.py                        # Entry point Streamlit
│   ├── requirements.txt              # Dependências Python
│   ├── README.md                     # Documentação de usuário
│   ├── data/
│   │   ├── loader.py                 # Carregamento CSV + Fernet + cache (TTL 300s)
│   │   └── loader_pandas.py          # Loader alternativo com Pandas
│   ├── pages/
│   │   ├── consulta_lojas.py         # Página de consulta de lojas
│   │   ├── gestao_crises.py          # Página de gestão de crises
│   │   ├── abertura_chamados.py      # Página de abertura de chamados
│   │   ├── historico.py              # Página de histórico/auditoria
│   │   ├── dashboard.py              # Dashboard com KPIs
│   │   └── ajuda.py                  # Ajuda/FAQ (placeholder)
│   ├── components/
│   │   ├── styles.py                 # Sistema de design e CSS global
│   │   ├── ui.py                     # Componentes reutilizáveis (cards, badges)
│   │   ├── nav.py                    # Navegação e sidebar
│   │   └── __init__.py               # Exports dos componentes
│   ├── templates/
│   │   └── __init__.py               # Funções de geração de templates
│   └── utils/
│       └── sheets.py                 # Integração Google Sheets API
│
├── consulta lojas python/            # App legado (predecessor) + sync de dados
│   ├── main.py                       # App Streamlit original
│   ├── encryption.py                 # Utilitário de encriptação Fernet
│   ├── relacaocheck.py               # Script de sync XLSX → CSV → .enc
│   ├── pages/crises.py               # Página de crises legada
│   └── csvs/                         # Arquivos de dados encriptados
│       ├── relacao.csv.enc           # Dados mestres das lojas (principal)
│       ├── designacao.csv.enc        # Designações de circuito MPLS/INN
│       ├── escalacao.csv.enc         # Contatos de escalação
│       ├── GGL.csv.enc               # Gerentes Gerais de Loja
│       ├── GR.csv.enc                # Gerentes Regionais
│       ├── links.csv.enc             # Links dos portais (Vivo, Claro)
│       └── CD.csv                    # Informações de CDs (não encriptado)
│
├── PRD_Central_Comando_DPSP.md       # Este documento
├── PRD_ARQUITETURA.md                # Arquitetura técnica (v2.0)
├── PRD_MELHORIAS_CONTINUAS.md        # Roadmap de melhorias
├── COMPARACAO_Doc_Implementacao.md   # Gap analysis doc vs código
├── DPSP_CentralDeComando_Documentacao.docx
└── central_comando.html              # Export HTML estático
```

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

---

## 4. MODELO DE DADOS

### 4.1 Entidade: Loja
```python
{
    "vd":       str,   # Virtual Depot ID (identificador principal)
    "nome":     str,   # Nome da loja
    "cnpj":     str,   # CNPJ
    "endereco": str,   # Endereço completo
    "cidade":   str,
    "estado":   str,
    "regiao":   str,
    "tel":      str,   # Telefone fixo
    "cel":      str,   # Celular/WhatsApp
    "email":    str,
    "horario":  str,   # Horário de funcionamento
    "ggl":      str,   # Nome do Gerente Geral de Loja
    "ggl_tel":  str,
    "gr":       str,   # Nome do Gerente Regional
    "gr_tel":   str,
    "mpls":     str,   # Designação de circuito MPLS
    "inn":      str,   # Designação de circuito INN
    "status":   str,   # "open" | "closed"
}
```

### 4.2 Fontes de Dados (CSVs Encriptados)

| Arquivo | Conteúdo | Campos-chave |
|---------|----------|-------------|
| `relacao.csv.enc` | Dados mestres das lojas | VD, nome, CNPJ, endereço, contatos |
| `designacao.csv.enc` | Designações de circuito | VD, MPLS, INN |
| `escalacao.csv.enc` | Escalonamento técnico | VD, nível, contato |
| `GGL.csv.enc` | Gerentes de loja | VD, nome, telefone |
| `GR.csv.enc` | Gerentes regionais | VD/Região, nome, telefone |
| `links.csv.enc` | Links de portais | Operadora, URL, credenciais |
| `CD.csv` | Centros de distribuição | Código, endereço, responsável |

---

## 5. ARQUITETURA E FLUXOS

### 5.1 Fluxo de Carregamento de Dados
```
Startup da App (app.py)
  │
  └→ DataLoader.__init__(master_key)
       │
       ├→ _init_fernet()          # Configura cipher com MASTER_KEY do .env
       │
       └→ get_lojas() [sob demanda]
            ├→ CacheManager.get("all_lojas")
            │     └─ [HIT] return cached data (TTL = 300s)
            │
            └─ [MISS] _load_from_csv()
                  ├→ Lê relacao.csv.enc
                  ├→ Fernet.decrypt(bytes) → CSV string
                  ├→ csv.DictReader → list[dict]
                  ├→ Merge com designacao.csv.enc (por VD)
                  ├→ Merge com GGL/GR.csv.enc
                  ├→ CacheManager.set("all_lojas", data, ttl=300)
                  └→ UsageLogger.log("load") [auditoria]
```

### 5.2 Fluxo de Sync de Dados (relacaocheck.py)
```
Arquivo XLSX na rede (\\dspsrv04\suporte relação lojas\)
  │
  ├→ pandas.read_excel() → DataFrame
  ├→ DataFrame.to_csv() → relacao.csv
  ├→ Fernet.encrypt(csv_bytes) → relacao.csv.enc
  └→ git commit + push (atualização mensal)
```

### 5.3 Fluxo de Consulta de Lojas
```
pages/consulta_lojas.py
  │
  ├→ st.text_input("Buscar loja")
  ├→ st.selectbox("Modo de busca")
  │     Modos: VD | Nome | Endereço | Texto livre
  │
  ├→ DataLoader.buscar_loja(termo, modo)
  │     └→ Filtragem O(n) na lista em memória
  │
  ├→ Paginação (max 20 resultados exibidos)
  │
  └→ components/ui.py → render_card(loja)
        Exibe: VD, nome, CNPJ, endereço, contatos,
               gerentes (GGL/GR), circuitos (MPLS/INN)
        Ações: ⭐ Favoritar | 📋 Detalhes | 📞 Gerar Chamado
```

### 5.4 Fluxo de Gestão de Crises
```
pages/gestao_crises.py
  │
  ├─ [Tab 1] Alertas Executivos
  │   ├→ Escopo: Internet MPLS | INN | Sistema PDV | ERP | VPN | DC | Energia
  │   ├→ Formulário: impacto, início, responsável
  │   ├→ templates.gerar_alerta_executivo(tipo, dados)
  │   │   └→ Retorna string formatada (WhatsApp-ready)
  │   │       🔴 Abertura | 🟡 Atualização | 🟢 Normalização
  │   └→ render_template_box(template) + botão copiar
  │
  ├─ [Tab 2] Gestão de Crise
  │   ├→ Formulário: número incidente, sala de crise, unidades afetadas,
  │   │             causa, responsável técnico, nível de crise
  │   ├→ templates.gerar_gestao_crise(dados)
  │   │   └→ Auto-calcula próxima atualização (+30min)
  │   └→ Contador de updates
  │
  └─ [Tab 3] Loja Isolada
      ├→ Tipo: Energia Elétrica | Internet/Conectividade
      ├→ VD da loja → lookup DataLoader.buscar_loja(vd)
      ├→ templates.gerar_loja_isolada(tipo, loja, dados)
      │   └→ Gera par: Abertura + Fechamento
      └→ Salvar em Google Sheets (opcional)
```

### 5.5 Fluxo de Abertura de Chamados
```
pages/abertura_chamados.py
  │
  ├→ Busca loja por VD (preenche campos automaticamente)
  │
  ├─ [Vivo MVE]
  │   Campos: Nome, Telefone, Email, Designação MPLS, VD, Início, Horário
  │   → Gera texto formatado para portal Vivo MVE
  │   → Link direto para o portal
  │
  └─ [Claro Empresas]
      Campos: Designação INN/MPLS, Unidade (VD + Nome), Endereço, Hora Incidente
      → Gera texto formatado para portal Claro Empresas
      → Link direto para o portal
```

### 5.6 Fluxo de Histórico
```
utils/sheets.py → GoogleSheetsManager
  │
  ├→ __init__(service_account_json, sheet_id)
  │   └→ gspread.authorize() com Service Account
  │
  ├→ salvar_template(tipo, subtipo, label, texto)
  │   ├→ sheets_api.append_row([timestamp, tipo, subtipo, label, texto])
  │   ├→ Auto-rotação: mantém max 99 registros por aba
  │   └─ [FALLBACK] SQLite: data/historico.db
  │
  └→ listar_templates(tipo)
      ├→ sheets_api.get_all_records()
      └→ Renderiza em pages/historico.py com cards
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
  ├─ Logo DPSP + Versão
  ├─ 🔍 Consulta de Lojas
  ├─ 🚨 Gestão de Crises
  ├─ 📋 Abertura de Chamados
  ├─ 📊 Dashboard
  ├─ 🕐 Histórico
  └─ ❓ Ajuda
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
| Vivo | MVE Portal (link em links.csv.enc) | MPLS |
| Claro | Claro Empresas (link em links.csv.enc) | INN / MPLS |

---

## 8. SEGURANÇA E ENCRIPTAÇÃO

### 8.1 Implementado
- Arquivos CSV encriptados com **Fernet** (simétrico, autenticado)
- Secrets em variáveis de ambiente (`.env`)
- Log de uso para auditoria (`UsageLogger`)

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
| MASTER_KEY hardcoded em `encryption.py` | Alta | Mover para `.env` exclusivamente |
| Sem autenticação de usuário | Alta | Implementar SSO (Azure AD) ou auth plugin |
| `secrets.toml` com chave em texto | Média | Usar apenas variáveis de ambiente |
| SQLite fallback sem encriptação | Média | Encriptar banco SQLite |
| Sem validação de inputs nos formulários | Baixa | Sanitizar todos os campos de crise |

---

## 9. DASHBOARD — KPIs

| Métrica | Fonte | Cálculo |
|---------|-------|---------|
| Total de Lojas | relacao.csv | `len(lojas)` |
| Lojas Ativas | relacao.csv | `status == "open"` |
| Lojas Inativas | relacao.csv | `status == "closed"` |
| Estados atendidos | relacao.csv | `len(set(l.estado))` |
| Distribuição por Estado | relacao.csv | `groupby(estado).count()` |
| Distribuição por Região | relacao.csv | `groupby(regiao).count()` |

---

## 10. PERFORMANCE

| Operação | Complexidade | Tempo Típico |
|---------|-------------|-------------|
| Carregamento inicial (CSV + decrypt) | O(n) | 2–5s |
| Busca de loja | O(n) linear scan | < 200ms |
| Salvar no Sheets | O(1) API call | ~500ms |
| Re-renderização UI | O(1) Streamlit | < 100ms |
| Cache hit | O(1) | < 1ms |

**Gargalos:**
- Decriptação CSV no primeiro load
- Latência Google Sheets API (~500ms/chamada)
- Sem índice de busca (busca linear em 2000+ registros)

**Melhorias sugeridas:**
- Índice invertido para busca por nome/endereço
- Pool de conexões Google Sheets
- Pre-warming do cache no startup

---

## 11. STATUS DE IMPLEMENTAÇÃO

### Completo
- Consulta de lojas (4 modos de busca)
- Geração de templates de crise (Alertas Executivos, Gestão de Crise, Loja Isolada)
- Geração de chamados Vivo/Claro
- Dashboard com KPIs
- Tema escuro responsivo
- Integração Google Sheets + fallback SQLite
- Encriptação Fernet dos dados
- Sistema de cache com TTL
- Biblioteca de componentes UI

### Parcial
- Histórico/Auditoria (leitura limitada das sheets)
- Carregamento de dados (fallback para dados de amostra se CSVs indisponíveis)
- Tratamento de erros em edge cases

### Não Implementado
- Autenticação/Autorização (SSO/Azure AD)
- Filtros avançados (estado, região, cluster)
- Sistema de favoritos persistente
- Export PDF/Excel dos dados de loja
- Webhooks para Telegram
- Integração ServiceNow
- Progressive Web App (modo offline)
- Atalhos de teclado
- Acessibilidade WCAG

---

## 12. ROADMAP

### Q2 2026 — Dados & Integração
- [ ] Sync em tempo real dos CSVs
- [ ] Filtros avançados (estado, região, status)
- [ ] Sistema de favoritos persistente
- [ ] Histórico local (localStorage)

### Q3 2026 — Automação
- [ ] Integração ServiceNow (auto-criação de tickets)
- [ ] Webhooks Telegram para notificações
- [ ] Export PDF/Excel dos detalhes de loja
- [ ] Modo wizard para novos usuários

### Q4 2026 — Enterprise
- [ ] SSO (Active Directory/Azure AD)
- [ ] Logs de auditoria completos
- [ ] Suporte multi-tenant
- [ ] Notificações em tempo real

---

## 13. INSTRUÇÕES DE EXECUÇÃO

```bash
# Clonar/navegar para o projeto
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
cd "consulta lojas python"
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
