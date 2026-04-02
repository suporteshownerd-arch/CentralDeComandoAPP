# PRD — Central de Comando DPSP
## Plano de Melhorias Contínuas v1.3

**Data:** 02/04/2026  
**Versão Atual:** 1.3  
**Responsável:** Enzo Maranho — T.I. DPSP

---

## 1. Visão Geral do Produto

### 1.1 O que é
Sistema web interno para consulta de lojas, gestão de crises e abertura de chamados da DPSP.

### 1.2 Objetivos do PRD
- Documentar melhorias identificadas
- Priorizar funcionalidades
- Definir roadmap de evolução
- Estabelecer métricas de sucesso

---

## 2. Análise SWOT

| **Forças** | **Fraquezas** |
|------------|---------------|
| Interface moderna e intuitiva | Dados de exemplo (mock) |
| Tema escuro premium | Integração Sheets não configurada |
| Múltiplos modos de busca | Sem autenticação |
| Templates automáticos | Sem backup automático |

| **Oportunidades** | **Ameaças** |
|-------------------|--------------|
| Integração com API real | Dados desatualizados |
| Mobile responsive | Falta de training |
| Notificações push | Segurança |

---

## 3. Melhorias por Categoria

### 3.1 Lógica & Dados

| # | Melhoria | Descrição | Prioridade | Status |
|---|----------|-----------|------------|--------|
| L1 | **Dados Reais** | Integrar com CSVs criptografados (Fernet) | Alta | Pendente |
| L2 | **Busca Avançada** | Filtros por região, GGL, GR, status | Alta | ✅ Implementado |
| L3 | **Auto-complete** | Suggestion ao digitar na busca | Média | Pendente |
| L4 | **Validação VD** | Validar se VD existe antes de buscar | Média | Pendente |
| L5 | **Cache Inteligente** | Cachear dados por tempo configurável | Média | Pendente |
| L6 | **Logs de Uso** | Registrar quem buscou o que | Baixa | Pendente |

### 3.2 Informações & Conteúdo

| # | Melhoria | Descrição | Prioridade | Status |
|---|----------|-----------|------------|--------|
| I1 | **Dashboard KPI** | Métricas: MTTR, uptime, chamados/dia | Alta | ✅ Parcial |
| I2 | **Alertas Ativos** | Notificações de incidentes em andamento | Alta | Pendente |
| I3 | **Mapa de Lojas** | Visualização geográfica das lojas | Média | Pendente |
| I4 | **Relatórios** | Exportar histórico em PDF/Excel | Média | Pendente |
| I5 | **FAQ/Help** | Tutorial integrado ao sistema | Baixa | Pendente |
| I6 | **Contatos Úteis** | Lista completa de emergências | Baixa | ✅ Sidebar |

### 3.3 Layout & UX

| # | Melhoria | Descrição | Prioridade | Status |
|---|----------|-----------|------------|--------|
| U1 | **Mobile First** | Layout responsivo para celular | Alta | ✅ Parcial |
| U2 | **Dark/Light Toggle** | Alternar entre temas | Alta | ✅ HTML only |
| U3 | **Atalhos Teclado** | Ctrl+K busca, 1-4 navegação | Alta | ✅ HTML only |
| U4 | **Loading States** | Skeletons durante carregamento | Média | Pendente |
| U5 | **Toasts Melhorados** | Feedback visual mais claro | Média | ✅ Parcial |
| U6 | **Drag & Drop** | Reordenar favoritos | Baixa | Pendente |

---

## 4. Backlog de Funcionalidades

### 4.1 Sprint Atual (1-2 semanas)

| ID | Feature | Esforço | Prioridade |
|----|---------|---------|------------|
| S1 | Dados reais via CSV Fernet | 3 dias | P0 |
| S2 | Auto-complete na busca | 2 dias | P1 |
| S3 | Layout mobile responsivo | 2 dias | P1 |
| S4 | Dashboard KPIs reais | 2 dias | P2 |

### 4.2 Próximo Release (1 mês)

| ID | Feature | Esforço | Prioridade |
|----|---------|---------|------------|
| R1 | Integração Google Sheets | 3 dias | P0 |
| R2 | Autenticação (SSO/Azure AD) | 5 dias | P0 |
| R3 | Notificações push | 2 dias | P1 |
| R4 | Mapa de lojas | 3 dias | P2 |
| R5 | Exportar relatórios | 2 dias | P2 |

### 4.3 Roadmap Trimestral

| Trimestre | Foco | Features |
|-----------|------|----------|
| Q2 2026 | Dados & Integração | CSVs, Sheets, API |
| Q3 2026 | Mobile & UX | Responsivo, PWA, Offline |
| Q4 2026 | Enterprise | SSO, Logs, Backup |

---

## 5. Arquitetura Técnica

### 5.1 Stack Atual
```
Frontend:  Streamlit (Python)
Dados:    JSON/CSV (mock)
Estilização: CSS Customizado
```

### 5.2 Stack Proposto
```
Frontend:  Streamlit + React (futuro)
Backend:   FastAPI + PostgreSQL
Cache:    Redis
Dados:    CSV Fernet + Sheets
Auth:     Azure AD / SSO
Deploy:   Docker + K8s
```

### 5.3 Estrutura de Dados

```python
# Modelo Loja
{
    "vd": "2015",
    "nome": "Drogasil Paulista",
    "cnpj": "12.345.678/0001-99",
    "endereco": "Av. Paulista, 1500",
    "cidade": "São Paulo",
    "estado": "SP",
    "regiao": "Sudeste",
    "tel": "(11) 3001-2015",
    "cel": "(11) 91234-5678",
    "email": "paulista@dpsp.com.br",
    "horario": "Seg-Sex 07h-22h",
    "ggl": "Marcos Silva",
    "ggl_tel": "(11) 99876-5432",
    "gr": "Ana Paula Torres",
    "gr_tel": "(11) 98765-4321",
    "mpls": "rsp_mpls_2015",
    "inn": "rsp_inn_2015",
    "status": "open",
    "favorito": false
}
```

---

## 6. Variáveis de Ambiente

| Variável | Descrição | Obrigatório | Atual |
|----------|-----------|-------------|-------|
| `MASTER_KEY` | Chave Fernet | ✅ | ❌ |
| `GCP_SERVICE_ACCOUNT` | JSON Service Account | ✅ (Sheets) | ❌ |
| `SHEETS_ID_AEXEC` | ID Planilha AExec | ✅ | ❌ |
| `SHEETS_ID_GCRISES` | ID Planilha GCrises | ✅ | ❌ |
| `DATABASE_URL` | PostgreSQL connection | ❌ | Futuro |
| `REDIS_URL` | Redis connection | ❌ | Futuro |

---

## 7. Métricas de Sucesso

### 7.1 Produto
| Métrica | Meta |
|---------|------|
| Tempo médio de busca | < 3 segundos |
| Tempo de geração template | < 1 segundo |
| Usuários únicos/mês | > 50 |
| NPS | > 70 |

### 7.2 Operacionais
| Métrica | Meta |
|---------|------|
| Uptime | > 99.5% |
| MTTR | Redução 20% |
| Chamados via sistema | > 80% |

---

## 8. Riscos e Mitigações

| Risco | Prob. | Impacto | Mitigação |
|-------|-------|---------|------------|
| Dados desatualizados | Alta | Alto | Sync diário automatizado |
| Sheets fora | Média | Alto | Fallback SQLite local |
| Usuários não adotam | Média | Alto | Treinamento + docs |
| Segurança | Média | Alto | SSO + auditoria |

---

## 9. Checklist de Implementação

### ✅ Concluído (v1.3)
- [x] Layout Premium com CSS customizado
- [x] Tema escuro elegante
- [x] Busca por VD/Designação/Endereço/Nome/Livre
- [x] Filtros por Estado e Status
- [x] Favoritos na sidebar
- [x] Quick Stats na sidebar
- [x] E-mail técnico funcional
- [x] Chamados Vivo/Claro funcionais
- [x] Templates Crises (Abertura/Atualização/Normalização)
- [x] Templates Loja Isolada (4 tipos)
- [x] Histórico com navegação
- [x] Salvar em Sheets/SQLite

### 🔄 Em Andamento
- [ ] Dados reais via CSV Fernet
- [ ] Configuração Google Sheets

### ⏳ Pendente
- [ ] Autenticação SSO
- [ ] Layout mobile
- [ ] Dashboard KPIs reais
- [ ] Mapa de lojas
- [ ] Notificações push
- [ ] Logs de auditoria

---

## 10. Próximos Passos

1. ✅ **Revisar PRD** com stakeholders
2. ⏳ **Configurar variáveis** no Streamlit Cloud
3. ⏳ **Testar integração** Sheets
4. ⏳ **Coletar feedback** dos usuários
5. ⏳ **Implementar dados reais**

---

## 11. Referências

- **Repositório:** https://github.com/suporteshownerd-arch/CentralDeComandoAPP
- **Documento Original:** `DPSP_CentralDeComando_Documentacao.docx`
- **Contato:** central.comando@dpsp.com.br
- **Telefone:** (11) 3274-7527

---

*Documento criado para planejamento de melhorias contínuas.*  
*Versão 1.3 — 02/04/2026*
