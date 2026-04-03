# PRD — Central de Comando DPSP
## Plano de Melhorias Contínuas v1.5

**Data:** 03/04/2026  
**Versão Atual:** 1.5  
**Responsável:** Enzo Maranho — T.I. DPSP

---

## 1. Visão Geral do Produto

### 1.1 O que é
Sistema web interno para consulta de lojas, gestão de crises, abertura de chamados e feed de comunicados/imagens da DPSP.

### 1.2 Objetivos do PRD
- Documentar melhorias identificadas
- Priorizar funcionalidades
- Definir roadmap de evolução
- Estabelecer métricas de sucesso

---

## 2. Feed de Comunicados e Imagens

### 2.1 Overview da Página Feed
A página Feed (📊) é uma das principais páginas do sistema, responsável por:
- Exibir comunicados e notícias importantes
- Compartilhar imagens (prints, alertas, comunicados visuais)
- Manter equipe informada sobre manutenções e mudanças

### 2.2 Estado Atual (v1.5)

| Feature | Status | Observações |
|---------|--------|------------|
| Carrossel de 3 imagens por página | ✅ Implementado | Navegação com ◀ ▶ |
| Redimensionamento 540x720 (3:4) | ✅ Implementado | PIL resize |
| Bordas coloridas | ✅ Implementado | Roxo/Azul |
| Upload de imagens (PC) | ✅ Implementado | Via popover |
| Adicionar por URL | ✅ Implementado | Via popover |
| Exibir usuário e data | ✅ Implementado | Metadata simples |
| Excluir imagens | ✅ Implementado | Botão lixeira |
| Comunicados (cards) | ✅ Implementado | Estáticos |
| Zoom no hover | ⚠️ CSS não funciona | Streamlit limita |
| Animações CSS | ⚠️ Limitado | Streamlit limita |
| Exibir 3+ por página | ✅ Implementado | Paginação |
| Imagens de exemplo (mock) | ✅ Implementado | picsum.photos |
| Limpar cache imagens | ⚠️ Pendente | Não implementado |

### 2.3 Melhorias Propostas para Feed

| ID | Melhoria | Descrição | Prioridade | Status |
|----|---------|-----------|------------|--------|--------|
| F1 | **Slide Automático** | Carrossel avança automaticamente (5-10s) | Alta | Pendente |
| F2 | **Thumbnails** | Miniaturas clicáveis para navegar | Alta | Pendente |
| F3 | **Lightbox** | Clique na imagem abre em tela cheia | Média | Pendente |
| F4 | **Comunicados Dinâmicos** | Buscar comunicados do Sheets | Alta | Pendente |
| F5 | **Tipos de Comunicado** | Categorias: Manutenção, Alerta, Info, Novidade | Média | Pendente |
| F6 | **Ordenar Imagens** | Arrastar para reordenar | Baixa | Pendente |
| F7 | **Compartilhar** | Copiar link da imagem | Baixa | Pendente |
| F8 | **Download** | Baixar imagem original | Baixa | Pendente |
| F9 | **Galeria Grid** | Visualização em grid (opcional) | Média | Pendente |
| F10 | **Filtros** | Filtrar por usuário, data, tipo | Baixa | Pendente |
| F11 | **Animações Reais** | Usar biblioteca JS externa | Alta | Pendente |
| F12 | **Upload Múltiplo** | Selecionar várias imagens | Alta | Pendente |

### 2.4 Especificações Técnicas do Feed Atual

```
Dimensão Imagem: 540x720 pixels (proporção 3:4 - Instagram/Feed)
Bordas: 6px Roxo (#6366f1) + 4px Azul (#1e1e2e)
Imagens por página: 3
Navegação: ◀ Anterior | Próxima ▶
Cache: session_state (memória)
Dados: st.file_uploader + URL
```

### 2.5 Backlog Feed

| ID | Feature | Esforço | Prioridade |
|----|---------|---------|------------|
| F1 | Slide Automático | 1 dia | P1 |
| F2 | Thumbnails | 1 dia | P1 |
| F3 | Lightbox | 1 dia | P2 |
| F4 | Comunicados Sheets | 2 dias | P0 |
| F5 | Categorias | 1 dia | P2 |
| F7 | Download | 0.5 dia | P2 |
| F12 | Upload Múltiplo | 1 dia | P1 |

---

## 3. Análise SWOT

| **Forças** | **Fraquezas** |
|------------|---------------|
| Interface moderna e intuitiva | Dados de exemplo (mock) |
| Tema escuro premium | Integração Sheets não configurada |
| Múltiplos modos de busca | Sem autenticação |
| Templates automáticos | Sem backup automático |
| Feed com imagens | Cache em memória |

| **Oportunidades** | **Ameaças** |
|-------------------|--------------|
| Integração com API real | Dados desatualizados |
| Mobile responsive | Falta de training |
| Notificações push | Segurança |

---

## 3. Melhorias por Categoria

## 4. Melhorias por Categoria

### 4.1 Lógica & Dados

| # | Melhoria | Descrição | Prioridade | Status |
|---|----------|-----------|------------|--------|
| L1 | **Dados Reais** | Integrar com CSVs criptografados (Fernet) | Alta | ✅ Implementado |
| L2 | **Busca Avançada** | Filtros por região, GGL, GR, status | Alta | ✅ Implementado |
| L3 | **Auto-complete** | Suggestion ao digitar na busca | Média | Pendente |
| L4 | **Validação VD** | Validar se VD existe antes de buscar | Média | Pendente |
| L5 | **Cache Inteligente** | Cachear dados por tempo configurável | Média | Pendente |
| L6 | **Logs de Uso** | Registrar quem buscou o que | Baixa | Pendente |

### 4.2 Informações & Conteúdo

| # | Melhoria | Descrição | Prioridade | Status |
|---|----------|-----------|------------|--------|
| I1 | **Dashboard KPI** | Métricas: MTTR, uptime, chamados/dia | Alta | ✅ Parcial |
| I2 | **Alertas Ativos** | Notificações de incidentes em andamento | Alta | Pendente |
| I3 | **Mapa de Lojas** | Visualização geográfica das lojas | Média | Pendente |
| I4 | **Relatórios** | Exportar histórico em PDF/Excel | Média | Pendente |
| I5 | **FAQ/Help** | Tutorial integrado ao sistema | Baixa | Pendente |
| I6 | **Contatos Úteis** | Lista completa de emergências | Baixa | ✅ Sidebar |

### 4.3 Layout & UX

| # | Melhoria | Descrição | Prioridade | Status |
|---|----------|-----------|------------|--------|
| U1 | **Mobile First** | Layout responsivo para celular | Alta | ✅ Parcial |
| U2 | **Dark/Light Toggle** | Alternar entre temas | Alta | ✅ Streamlit config.toml |
| U3 | **Atalhos Teclado** | Ctrl+K busca, 1-4 navegação | Alta | Pendente |
| U4 | **Loading States** | Skeletons durante carregamento | Média | Pendente |
| U5 | **Toasts Melhorados** | Feedback visual mais claro | Média | ✅ Parcial |
| U6 | **Drag & Drop** | Reordenar favoritos | Baixa | Pendente |

---

## 5. Backlog de Funcionalidades

### 4.1 Sprint Atual (1-2 semanas)

| ID | Feature | Esforço | Prioridade |
|----|---------|---------|------------|
| ~~S1~~ | ~~Dados reais via CSV Fernet~~ | — | ✅ Concluído |
| S2 | Auto-complete na busca | 2 dias | P1 |
| S3 | Filtros avançados (estado, região, status) | 2 dias | P0 |
| S4 | Dashboard KPIs reais (plotly/altair) | 2 dias | P1 |

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

## 6. Arquitetura Técnica

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

## 7. Variáveis de Ambiente

| Variável | Descrição | Obrigatório | Atual |
|----------|-----------|-------------|-------|
| `MASTER_KEY` | Chave Fernet | ✅ | ❌ |
| `GCP_SERVICE_ACCOUNT` | JSON Service Account | ✅ (Sheets) | ❌ |
| `SHEETS_ID_AEXEC` | ID Planilha AExec | ✅ | ❌ |
| `SHEETS_ID_GCRISES` | ID Planilha GCrises | ✅ | ❌ |
| `DATABASE_URL` | PostgreSQL connection | ❌ | Futuro |
| `REDIS_URL` | Redis connection | ❌ | Futuro |

---

## 8. Métricas de Sucesso

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

## 9. Riscos e Mitigações

| Risco | Prob. | Impacto | Mitigação |
|-------|-------|---------|------------|
| Dados desatualizados | Alta | Alto | Sync diário automatizado |
| Sheets fora | Média | Alto | Fallback SQLite local |
| Usuários não adotam | Média | Alto | Treinamento + docs |
| Segurança | Média | Alto | SSO + auditoria |

---

## 10. Checklist de Implementação

### ✅ Concluído (v1.5)
- [x] Layout Premium com CSS customizado
- [x] Tema escuro via .streamlit/config.toml (Streamlit Cloud)
- [x] Dados reais — ~2055 lojas via CSV Fernet (relacao, designacao, GGL, GR)
- [x] Busca VD: match exato ≤ 4 dígitos; busca designação para entradas longas
- [x] Detecção MPLS/INN via campo "Tipo de acesso" (não Operadora)
- [x] Sidebar navegação por botões com CSS active state
- [x] KPIs dinâmicos na sidebar (total/ativas/inativas)
- [x] Chamados Vivo/Claro funcionais
- [x] Templates Crises (Abertura/Atualização/Normalização)
- [x] Templates Loja Isolada
- [x] Histórico com navegação
- [x] Salvar em Sheets/SQLite
- [x] Feed: Carrossel 3 imagens/página (540x720)
- [x] Feed: Upload (PC) e URL
- [x] Feed: Bordas coloridas (PIL)
- [x] Feed: Comunicados cards

### 🔄 Em Andamento
- [ ] Configuração Google Sheets (variáveis de ambiente no Streamlit Cloud)

### ⏳ Pendente
- [ ] Autenticação SSO
- [ ] Filtros avançados na UI (estado, região, cluster)
- [ ] Dashboard KPIs reais (plotly/altair)
- [ ] Mapa de lojas
- [ ] Notificações push
- [ ] Logs de auditoria persistentes
- [ ] Favoritos persistentes (além de session_state)

---

## 11. Próximos Passos

1. ✅ **Revisar PRD** com stakeholders
2. ⏳ **Configurar variáveis** no Streamlit Cloud
3. ⏳ **Testar integração** Sheets
4. ⏳ **Coletar feedback** dos usuários
5. ⏳ **Implementar dados reais**

---

## 12. Referências

- **Repositório:** https://github.com/suporteshownerd-arch/CentralDeComandoAPP
- **Documento Original:** `DPSP_CentralDeComando_Documentacao.docx`
- **Contato:** central.comando@dpsp.com.br
- **Telefone:** (11) 3274-7527

---

*Documento criado para planejamento de melhorias contínuas.*  
*Versão 1.5 — 03/04/2026*
