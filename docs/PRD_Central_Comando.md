# PRD — Central de Comando DPSP
## Plano de Melhorias Contínuas v1.0

**Data:** 02/04/2026  
**Versão do Sistema:** 1.0  
**Responsável:** Enzo Maranho — T.I. DPSP

---

## 1. Contexto e Visão do Produto

### 1.1 O Problema
A equipe de T.I. da DPSP necessita de uma ferramenta centralizada para:
- Consulta rápida de dados de lojas do parque
- Abertura padronizada de chamados junto às operadoras Vivo e Claro
- Geração de comunicados de crise para diferentes públicos

### 1.2 A Solução
Sistema web moderno (Python/Streamlit → HTML standalone) com interface profissional, tema claro/escuro e funcionalidades integradas.

### 1.3 Objetivos do PRD
- Documentar melhorias identificadas
- Priorizar funcionalidades
- Definir roadmap de evolução
- Estabelecer métricas de sucesso

---

## 2. Melhorias Identificadas

### 2.1 Melhorias de Interface (Alta Prioridade)

| # | Melhoria | Descrição | Impacto |
|---|----------|-----------|---------|
| I1 | Modo offline | Progressive Web App com Service Worker para funcionar offline | Alto |
| I2 | Atalhos de teclado | Ctrl+K para busca, Esc para fechar modais, Ctrl+1-5 para nav | Médio |
| I3 | Animações mais fluidas | Microinterações nos botões e transições de painéis | Baixo |
| I4 | Loading states | Spinners/skeletons durante carregamentos | Médio |
| I5 | Tooltips informativos | Hover em campos para ajudar o usuário | Baixo |

### 2.2 Melhorias de Funcionalidade (Alta Prioridade)

| # | Melhoria | Descrição | Impacto |
|---|----------|-----------|---------|
| F1 | Busca avançada com filtros | Filtro por estado, região, status (aberta/fechada) | Alto |
| F2 | Histórico persistente | Salvar templates gerados no localStorage | Alto |
| F3 | Favoritos | Marcar lojas frequentes para acesso rápido | Médio |
| F4 | Exportar dados | Exportar ficha da loja para PDF/Excel | Médio |
| F5 | Dashboard de métricas | Painel com KPIs de incidentes (MTTR, disponibilidade) | Alto |
| F6 | Notificações push | Alertas de incidentes críticos | Médio |

### 2.3 Melhorias de Integração (Média Prioridade)

| # | Melhoria | Descrição | Impacto |
|---|----------|-----------|---------|
| T1 | Integração Google Sheets | Ler/gravar templates diretamente | Alto |
| T2 | Integração API de lojas | Buscar dados reais dos CSVs criptografados | Alto |
| T3 | Webhooks para Telegram | Enviar comunicados direto para grupos | Médio |
| T4 | Integração com ServiceNow | Abrir chamados automaticamente | Médio |
| T5 | SSO corporativo | Login via Active Directory/Azure AD | Médio |

### 2.4 Melhorias de UX (Média Prioridade)

| # | Melhoria | Descrição | Impacto |
|---|----------|-----------|---------|
| U1 | Wizard de abertura de chamados | Passo a passo guiado para novatos | Médio |
| U2 | Templatescustomizáveis | Editar modelos antes de copiar | Médio |
| U3 | Busca por voz | Input por microfone | Baixo |
| U4 | Modo apresentação | Tela cheia para reuniões | Baixo |
| U5 | Accessibility (a11y) | Suporte completo a leitores de tela | Médio |

---

## 3. backlog de Funcionalidades

### 3.1 Próximo Sprint (2 semanas)

| ID | Feature | Esforço | Prioridade |
|----|---------|---------|------------|
| S1 | Filtros na busca de lojas | 2 dias | P0 |
| S2 | Favoritos (star) | 1 dia | P0 |
| S3 | localStorage para histórico | 2 dias | P0 |
| S4 | Dashboard com métricas reais | 3 dias | P1 |

### 3.2 Próximo Release (1 mês)

| ID | Feature | Esforço | Prioridade |
|----|---------|---------|------------|
| R1 | Integração Google Sheets API | 5 dias | P0 |
| R2 | PWA / modo offline | 3 dias | P1 |
| R3 | Atalhos de teclado | 1 dia | P1 |
| R4 | Export PDF da ficha | 2 dias | P2 |

### 3.3 Roadmap Trimestral

| Trimestre | Foco | Features |
|-----------|------|----------|
| Q2 2026 | Dados & Integração | API de lojas, Sheets, Webhooks |
| Q3 2026 | Automation | ServiceNow, Telegram, automações |
| Q4 2026 | Enterprise | SSO, audit logs, multi-tenant |

---

## 4. Arquitetura Proposta

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                          │
│  (HTML/CSS/JS - Single Page Application)            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐               │
│  │ Consult │ │ Crises  │ │ History │               │
│  └────┬────┘ └────┬────┘ └────┬────┘               │
│       └───────────┼───────────┘                     │
│                   ▼                                  │
│            ┌────────────┐                           │
│            │ Store JS   │ (State Management)        │
│            └─────┬──────┘                           │
└─────────────────┼───────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────┐
│                    BACKEND                           │
│  ┌─────────────┐  ┌─────────────┐                  │
│  │ Python API  │  │ Streamlit   │                  │
│  │ (FastAPI)   │  │ (Original)  │                  │
│  └──────┬──────┘  └──────┬──────┘                  │
│         └────────┬───────┘                          │
│                  ▼                                   │
│         ┌───────────────┐                           │
│         │ Data Layer    │                           │
│         │ (CSV Fernet)  │                           │
│         └───────────────┘                           │
└─────────────────────────────────────────────────────┘
```

---

## 5. Dados e Estrutura

### 5.1 Fontes de Dados (atuais)
- `relacao.csv` — Mapeamento VD ↔ Designação
- `designacao.csv` — Detalhes de circuitos
- `escalacao.csv` — Contatos de escalação
- `links.csv` — URLs de portais
- `GR.csv` — Gerentes Regionais
- `GGL.csv` — Gerentes de Loja

### 5.2 Dados Futuros
- Cache local com Dexie.js
- Sincronização com Google Sheets
- Logs de auditoria

---

## 6. Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `master_key` | Chave Fernet para descriptografia | ✅ |
| `gcp_service_account` | JSON da Service Account GCP | ✅ |
| `sheets_id_aexec` | ID da planilha Alertas Executivos | ✅ |
| `sheets_id_gcrises` | ID da planilha Gestão de Crises | ✅ |
| `api_url` | URL da API Python (opcional) | ❌ |
| `telegram_bot_token` | Token do bot Telegram (opcional) | ❌ |

---

## 7. Métricas de Sucesso

### 7.1 Métricas de Produto
| Métrica | Meta |
|---------|------|
| Tempo médio de busca de loja | < 3 segundos |
| Tempo de geração de template | < 1 segundo |
| Taxa de uso (DIU) | > 50 usuários únicos/mês |
| NPS | > 70 |

### 7.2 Métricas Operacionais
| Métrica | Meta |
|---------|------|
| Uptime | > 99.5% |
| MTTR (Mean Time to Resolve) | Redução de 20% |
| Chamados abertos via sistema | > 80% do total |

---

## 8. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|----------|
| Dados desatualizados | Alta | Alto | Automatizar sync diário |
| Falha na integração Sheets | Média | Alto | Fallback para localStorage |
| Usuários não adotam | Média | Alto | Treinamento + documentação |
| Segurança dos dados | Média | Alto | SSO + auditoria + encrypt at rest |

---

## 9. Próximos Passos

1. **Revisar PRD com stakeholders** — Validar prioridades
2. **Criar repositório Git** — Versionar código
3. **Setup ambiente de desenvolvimento** — Docker + Python
4. **Implementar Sprint 1** — Filtros + Favoritos + Histórico local
5. **Testar com usuários beta** — Coletar feedback
6. **Deploy em produção** — Behind VPN/internal

---

## 10. Referências

- Documento Técnico v1.0 (este arquivo)
- Repositório: `central-comando-dpsp`
- Contato: central.comando@dpsp.com.br
- Telefone: (11) 3274-7527

---

*Documento criado para planejamento de melhorias contínuas.*  
*Versão 1.0 — 02/04/2026*
