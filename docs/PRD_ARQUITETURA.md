# PRD — Arquitetura e Estrutura do Projeto
## Central de Comando DPSP v2.0

**Data:** 02/04/2026  
**Versão:** 2.0  
**Responsável:** Enzo Maranho — T.I. DPSP

---

## 1. Visão Geral da Arquitetura

### 1.1 Estrutura de Diretórios

```
CentralDeComandoAPP/
├── app.py                      # Ponto de entrada principal
├── requirements.txt            # Dependências
├── .env.example                # Variáveis de ambiente
├── README.md                   # Documentação
├── PRD_ARQUITETURA.md          # Este documento
│
├── components/                 # Componentes reutilizáveis
│   ├── __init__.py
│   ├── ui.py                   # Elementos de UI (cards, badges, etc)
│   ├── styles.py               # CSS e design system
│   └── nav.py                  # Navegação e menu
│
├── pages/                      # Páginas do sistema
│   ├── __init__.py
│   ├── consulta_lojas.py       # Consulta de lojas
│   ├── gestao_crises.py        # Gestão de crises
│   ├── historico.py            # Histórico
│   ├── abertura_chamados.py   # Abertura de chamados
│   ├── dashboard.py            # Dashboard KPIs
│   └── ajuda.py                # FAQ e ajuda
│
├── data/                       # Dados e carregamento
│   ├── __init__.py
│   ├── loader.py               # Carregamento de dados
│   ├── cache.py               # Gerenciador de cache
│   └── logs.py                # Sistema de logs
│
├── templates/                  # Templates de comunicação
│   ├── __init__.py
│   ├── alertas.py              # Alertas executivos
│   ├── crises.py               # Gestão de crise
│   ├── isolada.py              # Loja isolada
│   └── comunicados.py         # E-mails e chamados
│
└── utils/                      # Utilitários
    ├── __init__.py
    ├── sheets.py               # Google Sheets
    ├── export.py              # Exportação CSV/JSON
    └── validators.py          # Validações
```

---

## 2. Design System

### 2.1 Tipografia

| Uso | Família | Peso | Tamanho |
|-----|---------|------|----------|
| Títulos H1 | Syne | 800 | 32px |
| Títulos H2 | Syne | 700 | 24px |
| Títulos H3 | Syne | 600 | 20px |
| Corpo | DM Sans | 400 | 14px |
| Código/VD | DM Mono | 500 | 13px |
| Labels | DM Mono | 400 | 11px |

### 2.2 Cores

```css
:root {
    /* Fundo */
    --bg-primary: #08090d;
    --bg-secondary: #0f1118;
    --bg-tertiary: #161920;
    --bg-surface: #1c2029;
    --bg-surface2: #232a36;
    
    /* Bordas */
    --border: rgba(255,255,255,0.06);
    --border2: rgba(255,255,255,0.12);
    
    /* Texto */
    --text-primary: #eaecf0;
    --text-secondary: #9094a6;
    --text-tertiary: #5c6370;
    
    /* Accent */
    --accent: #5b8def;
    --accent-hover: #4a7de0;
    
    /* Estados */
    --success: #34d399;
    --error: #f87171;
    --warning: #fbbf24;
    --info: #22d3ee;
    --purple: #a78bfa;
}
```

### 2.3 Componentes UI

- **Cards**: borda arredondada 16px, hover com translateY(-4px)
- **Badges**: pills com border-radius 8px
- **Botões**: border-radius 10px, transition 0.2s
- **Inputs**: border-radius 12px, focus com accent
- **Toasts**: border-radius 10px, cores por tipo

---

## 3. Módulos e Responsabilidades

### 3.1 components/ui.py

```python
def render_card(title, content, footer=None):
    """Card premium com hover effect"""
    
def render_badge(text, type="default"):
    """Badge com cores: success, error, warning, info"""
    
def render_vd_badge(vd):
    """Badge do VD com estilo mono"""
    
def render_status_indicator(status):
    """Indicador de status (open/closed)"""
    
def render_info_section(title, rows):
    """Seção de informações com label"""
    
def render_template_box(template):
    """Box para templates de comunicação"""
    
def render_kpi_card(label, value, delta=None):
    """Card de KPI"""
```

### 3.2 components/styles.py

```python
def get_base_css():
    """CSS base com variáveis e reset"""
    
def get_responsive_css():
    """CSS responsivo para mobile/tablet"""
    
def get_animations_css():
    """Animações (pulse, shimmer, etc)"""
```

### 3.3 components/nav.py

```python
def render_sidebar(lojas, favoritos, kpi_data):
    """Sidebar completa com menu e KPIs"""
    
def render_menu():
    """Menu de navegação"""
    
def render_footer():
    """Rodapé do sistema"""
```

### 3.4 pages/*.py

Cada página é um módulo independente que:
- Recebe dados via parâmetros
- Renderiza sua própria lógica
- Usa componentes de `components/`

---

## 4. Fluxo de Dados

```
app.py (Main)
    ↓
components/styles → CSS Global
components/nav → Sidebar + Menu
    ↓
pages/consulta_lojas.py
    ↓
data/loader.py → get_lojas()
    ↓
templates/comunicados.py → gerar_chamado_vivo()
    ↓
utils/sheets.py → salvar no Sheets
```

---

## 5. Padrões de Código

### 5.1 Nomenclatura

- **Módulos**: snake_case (ex: `gestao_crises.py`)
- **Funções**: snake_case (ex: `render_card`)
- **Classes**: PascalCase (ex: `DataLoader`)
- **Constantes**: UPPER_SNAKE_CASE

### 5.2 Docstrings

```python
def funcao(param: type) -> return_type:
    """
    Descrição curta.
    
    Args:
        param: Descrição do parâmetro.
    
    Returns:
        Descrição do retorno.
    """
```

### 5.3 Imports

```python
# Stdlib
import os
import json
from datetime import datetime

# Third-party
import streamlit as st
from cryptography.fernet import Fernet

# Local
from components import render_card
from data.loader import DataLoader
```

---

## 6. Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `MASTER_KEY` | Chave Fernet | ✅ |
| `GCP_SERVICE_ACCOUNT` | JSON Service Account | ✅ (Sheets) |
| `SHEETS_ID_AEXEC` | ID Planilha AExec | ✅ |
| `SHEETS_ID_GCRISES` | ID Planilha GCrises | ✅ |

---

## 7. Checklist de Implementação

### v2.0 - Refatoração
- [x] PRD Arquitetura
- [ ] components/ui.py
- [ ] components/styles.py
- [ ] components/nav.py
- [ ] pages/consulta_lojas.py
- [ ] pages/gestao_crises.py
- [ ] pages/historico.py
- [ ] pages/abertura_chamados.py
- [ ] pages/dashboard.py
- [ ] pages/ajuda.py
- [ ] app.py refatorado
- [ ] Testes

---

## 8. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 01/04/2026 | Versão inicial |
| 1.4 | 02/04/2026 | Melhorias contínuas |
| 2.0 | 02/04/2026 | Refatoração modular |

---

*Documento criado para planejamento da arquitetura v2.0*