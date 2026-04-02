# Plano de Ação — Central de Comando DPSP
**Versão:** 1.0
**Data:** 2026-04-02
**Responsável:** Enzo Maranho — DPSP T.I.

---

## Visão Geral

```
FASE 0 — Correções Críticas     Semana 1       (Agora → 09/04)
FASE 1 — Fundação Estável       Semanas 2–3    (10/04 → 23/04)
FASE 2 — Funcionalidades Core   Semanas 4–6    (24/04 → 14/05)
FASE 3 — Experiência & UX       Semanas 7–8    (15/05 → 28/05)
FASE 4 — Enterprise             Maio–Junho     (Q2 2026)
```

---

## FASE 0 — Correções Críticas `Semana 1`
> Problemas que comprometem segurança ou funcionamento básico. Resolver antes de qualquer outra coisa.

### 0.1 Segurança — Remover MASTER_KEY hardcoded
**Prioridade:** P0 — Crítico
**Esforço:** 2h
**Arquivo:** `consulta lojas python/encryption.py`

- [ ] Substituir a chave hardcoded por `os.environ.get("MASTER_KEY")`
- [ ] Verificar se `relacaocheck.py` também tem a chave hardcoded e corrigir
- [ ] Garantir que `.env` está no `.gitignore`
- [ ] Criar `.env.example` com as chaves em branco (sem valores reais)
- [ ] Auditar todos os arquivos: `grep -r "D8razgzqFXW2"` para confirmar que não restou nenhuma ocorrência

**Critério de aceite:** Nenhuma chave secreta em nenhum arquivo versionado.

---

### 0.2 Integração Google Sheets — Validar e Ativar
**Prioridade:** P0 — Crítico
**Esforço:** 3h
**Arquivo:** `CentralDeComandoAPP/utils/sheets.py`

- [ ] Testar conexão com Service Account configurado
- [ ] Confirmar que `SHEETS_ID_AEXEC` e `SHEETS_ID_GCRISES` funcionam
- [ ] Verificar lógica de auto-rotação (max 99 registros)
- [ ] Testar o fallback SQLite quando Sheets estiver indisponível
- [ ] Logar erros de conexão com mensagem amigável na UI

**Critério de aceite:** Salvar um template no Sheets e verificar no painel Google.

---

### 0.3 Carregamento de Dados Reais — Remover Mock Data
**Prioridade:** P0 — Crítico
**Esforço:** 4h
**Arquivo:** `CentralDeComandoAPP/data/loader.py`

- [ ] Mapear onde o loader cai para dados de amostra (`sample_data`, `mock`)
- [ ] Corrigir path dos CSVs encriptados (`../consulta lojas python/csvs/`)
- [ ] Tratar `FileNotFoundError` com mensagem clara e sugestão de configuração
- [ ] Validar que todos os 6 arquivos `.enc` são carregados corretamente
- [ ] Testar merge entre `relacao.csv.enc` + `designacao.csv.enc` + `GGL.csv.enc` + `GR.csv.enc`

**Critério de aceite:** App mostra dados reais das lojas na Consulta.

---

## FASE 1 — Fundação Estável `Semanas 2–3`
> Tornar o que já existe confiável e bem testado antes de adicionar features.

### 1.1 Histórico — Implementação Completa
**Prioridade:** P1
**Esforço:** 1 dia
**Arquivo:** `CentralDeComandoAPP/pages/historico.py`

- [ ] Conectar página ao `GoogleSheetsManager.listar_templates()`
- [ ] Exibir cards com: timestamp, tipo, label, primeiras linhas do template
- [ ] Botão "Copiar" para reabrir template
- [ ] Botão "Excluir" com confirmação
- [ ] Filtro por tipo (AExec / GCrise / Isolada)
- [ ] Exibir mensagem quando histórico estiver vazio

**Critério de aceite:** Templates salvos aparecem na página Histórico.

---

### 1.2 Consulta de Lojas — Filtros Avançados
**Prioridade:** P1
**Esforço:** 1 dia
**Arquivo:** `CentralDeComandoAPP/pages/consulta_lojas.py`

- [ ] Adicionar filtro por **Estado** (dropdown multi-seleção)
- [ ] Adicionar filtro por **Região**
- [ ] Adicionar filtro por **Status** (Ativa / Inativa / Todos)
- [ ] Mostrar contador: "X lojas encontradas"
- [ ] Paginação real (botões Anterior/Próximo, não só limitar a 20)

**Critério de aceite:** Filtrar por Estado SP retorna só lojas paulistas.

---

### 1.3 Performance — Migrar Busca para Pandas
**Prioridade:** P1
**Esforço:** 1 dia
**Arquivo:** `CentralDeComandoAPP/data/loader.py` + `loader_pandas.py`

- [ ] Substituir busca O(n) com loop por `DataFrame.str.contains()`
- [ ] Usar `loader_pandas.py` como base para `loader.py`
- [ ] Adicionar índice por VD para lookup O(1) em chamados/crises
- [ ] Medir tempo de busca antes e depois (target: < 200ms)

**Critério de aceite:** Busca "farmacia sao paulo" retorna resultado em < 200ms.

---

### 1.4 Validação de Formulários
**Prioridade:** P1
**Esforço:** 4h
**Arquivos:** todas as `pages/`

- [ ] Validar VD: apenas numérico, 4–6 dígitos
- [ ] Validar campos obrigatórios nos formulários de crise (mostrar erro inline)
- [ ] Sanitizar inputs antes de gerar templates (evitar injeção de caracteres especiais)
- [ ] Desabilitar botão "Gerar" até todos os campos obrigatórios estarem preenchidos

**Critério de aceite:** VD "abc" mostra erro "VD deve conter apenas números".

---

### 1.5 Tratamento de Erros Global
**Prioridade:** P1
**Esforço:** 4h
**Arquivo:** `CentralDeComandoAPP/app.py` + `utils/sheets.py`

- [ ] Wrapper global para capturar exceções não tratadas
- [ ] Toast de erro amigável (nunca mostrar stack trace ao usuário)
- [ ] Log de erros em arquivo local (`logs/errors.log`)
- [ ] Mensagem de "modo offline" quando Google Sheets estiver inacessível

**Critério de aceite:** Desligar internet → app mostra aviso claro e continua funcionando (fallback SQLite).

---

## FASE 2 — Funcionalidades Core `Semanas 4–6`
> Features que aumentam diretamente a produtividade da equipe.

### 2.1 Abertura de Chamados — Auto-preenchimento Completo
**Prioridade:** P1
**Esforço:** 1 dia
**Arquivo:** `CentralDeComandoAPP/pages/abertura_chamados.py`

- [ ] Campo VD preenche automaticamente: nome, endereço, horário, MPLS, INN
- [ ] Detectar se loja tem MPLS, INN ou ambos e mostrar seção correta
- [ ] Formatar número de telefone no padrão das operadoras
- [ ] Botão "Abrir Portal Vivo" abre link direto no navegador
- [ ] Botão "Abrir Portal Claro" abre link direto no navegador
- [ ] Salvar chamado gerado no histórico automaticamente

**Critério de aceite:** Digitar VD → clicar "Gerar Vivo" → texto pronto para colar no portal.

---

### 2.2 Loja Isolada — Melhorias de UX
**Prioridade:** P1
**Esforço:** 4h
**Arquivo:** `CentralDeComandoAPP/pages/gestao_crises.py`

- [ ] Auto-preencher nome da loja ao digitar VD
- [ ] Gerar Abertura + Fechamento lado a lado (duas colunas)
- [ ] Contador de atualizações com incremento manual
- [ ] Adicionar campo "Observações" no template de fechamento

**Critério de aceite:** Digitar VD → nome aparece automaticamente → templates gerados em < 1s.

---

### 2.3 Dashboard — Gráficos Reais
**Prioridade:** P2
**Esforço:** 1 dia
**Arquivo:** `CentralDeComandoAPP/pages/dashboard.py`

- [ ] Gráfico de barras: distribuição de lojas por Estado (Plotly)
- [ ] Gráfico de pizza: Ativas vs Inativas
- [ ] Gráfico de barras: lojas por Região
- [ ] KPI cards: Total, Ativas, Inativas, Estados
- [ ] Tabela filtrada: lojas inativas recentes

**Critério de aceite:** Dashboard carrega com gráficos em < 3s.

---

### 2.4 Busca Fuzzy
**Prioridade:** P2
**Esforço:** 4h
**Arquivo:** `CentralDeComandoAPP/data/loader.py`

- [ ] Adicionar `fuzzywuzzy` ou `rapidfuzz` ao `requirements.txt`
- [ ] Modo de busca "Texto Livre" usa similaridade (threshold 70%)
- [ ] Ordenar resultados por relevância (score decrescente)
- [ ] Sugerir correção: "Você quis dizer: Farmácia São Paulo?"

**Critério de aceite:** Busca "farmcia sao pulo" (erro de digitação) ainda encontra lojas corretas.

---

### 2.5 Sistema de Favoritos Persistente
**Prioridade:** P2
**Esforço:** 4h
**Arquivo:** `CentralDeComandoAPP/pages/consulta_lojas.py`

- [ ] Favoritos salvos em `localStorage` via `st.session_state` + serialização JSON
- [ ] Ícone ⭐ no card alterna favorito
- [ ] Seção "Favoritos" no topo da Consulta
- [ ] Limite de 10 favoritos por sessão

**Critério de aceite:** Favoritar loja → recarregar app → loja ainda está nos favoritos.

---

## FASE 3 — Experiência & UX `Semanas 7–8`
> Polimento e usabilidade para reduzir fricção no uso diário.

### 3.1 Auto-complete na Busca
**Prioridade:** P2
**Esforço:** 4h

- [ ] `st.selectbox` com lista filtrada ao digitar
- [ ] Sugestões mostram VD + Nome + Cidade
- [ ] Debounce de 300ms para não travar na digitação
- [ ] Histórico das últimas 5 buscas (session_state)

---

### 3.2 Loading States
**Prioridade:** P2
**Esforço:** 3h

- [ ] Spinner durante carregamento de dados (`st.spinner`)
- [ ] Skeleton cards enquanto busca processa
- [ ] Mensagem de progresso no startup ("Carregando dados de lojas...")
- [ ] Progress bar no carregamento inicial

---

### 3.3 Atalhos de Teclado
**Prioridade:** P3
**Esforço:** 4h

- [ ] `Ctrl+K` → Focar campo de busca
- [ ] `Ctrl+C` → Copiar último template gerado
- [ ] `Esc` → Limpar busca
- [ ] Mostrar atalhos na página de Ajuda

---

### 3.4 Modo Claro/Escuro
**Prioridade:** P3
**Esforço:** 4h
**Arquivo:** `CentralDeComandoAPP/components/styles.py`

- [ ] Toggle no sidebar entre dark/light theme
- [ ] Paleta clara: bg #ffffff, text #1a1a2e, accent #2563eb
- [ ] Salvar preferência no `session_state`

---

### 3.5 Página de Ajuda — Implementar
**Prioridade:** P3
**Esforço:** 4h
**Arquivo:** `CentralDeComandoAPP/pages/ajuda.py`

- [ ] FAQ com as 10 perguntas mais comuns
- [ ] Guia: Como abrir chamado Vivo passo a passo
- [ ] Guia: Como usar templates de crise
- [ ] Contatos úteis: Central de Comando, TI, operadoras
- [ ] Glossário: VD, MPLS, INN, GGL, GR, CD

---

## FASE 4 — Enterprise `Q2–Q3 2026`
> Features de nível corporativo. Planejar em conjunto com TI e infra.

### 4.1 Autenticação SSO
**Prioridade:** P1 (bloqueante para uso amplo)
**Esforço:** 3–5 dias
**Decisão necessária:** Azure AD ou plugin Streamlit?

- [ ] Avaliar `streamlit-authenticator` vs Azure AD OIDC
- [ ] Definir roles: `viewer` (consulta) vs `operator` (crise) vs `admin`
- [ ] Implementar login screen com logo DPSP
- [ ] Audit log: quem gerou qual template, quando

---

### 4.2 Integração ServiceNow
**Prioridade:** P2
**Esforço:** 3 dias

- [ ] Mapear API ServiceNow disponível
- [ ] Botão "Criar Ticket ServiceNow" na página de chamados
- [ ] Auto-preencher campos do ticket com dados da loja
- [ ] Exibir número do ticket criado + link direto

---

### 4.3 Notificações Telegram
**Prioridade:** P2
**Esforço:** 2 dias

- [ ] Criar bot Telegram DPSP T.I.
- [ ] Webhook: alertas executivos publicados automaticamente no grupo
- [ ] Configuração do canal por tipo (Executivo, Crise, Isolada)

---

### 4.4 Sync Automático de Dados
**Prioridade:** P1
**Esforço:** 2 dias

- [ ] Substituir sync manual (`relacaocheck.py`) por job agendado
- [ ] Cron job: verificar XLSX na rede a cada 6h
- [ ] Notificar no app se dados estão desatualizados (> 7 dias)
- [ ] Migrar path hardcoded Windows para configurável via `.env`

---

### 4.5 Export PDF/Excel
**Prioridade:** P3
**Esforço:** 1 dia

- [ ] Exportar ficha completa da loja em PDF
- [ ] Exportar lista filtrada de lojas em Excel
- [ ] Template de relatório com logo DPSP

---

## Backlog — Itens Futuros (Sem Sprint Definido)

| Item | Categoria | Esforço estimado |
|------|-----------|-----------------|
| Mapa de lojas (Google Maps embed) | UX | 3 dias |
| App mobile (PWA offline) | Plataforma | 1 semana |
| Alertas proativos de loja offline | Automação | 1 semana |
| Multi-idioma PT/EN | UX | 3 dias |
| Integração com monitoramento de rede | Infra | 2 semanas |
| Relatório mensal automático | BI | 3 dias |

---

## Métricas de Sucesso

| Métrica | Atual | Meta Fase 1 | Meta Fase 2 |
|---------|-------|-------------|-------------|
| Tempo de busca | ~500ms | < 200ms | < 100ms |
| Geração de template | ~1s | < 500ms | < 300ms |
| Usuários mensais | ? | 20+ | 50+ |
| Templates gerados/mês | ? | 100+ | 300+ |
| Tempo de load inicial | ~5s | < 3s | < 2s |
| NPS da equipe | ? | > 60 | > 70 |

---

## Dependências e Riscos

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|--------------|-----------|
| CSVs desatualizados (sync manual) | Alto | Alta | Fase 4.4 (sync automático) |
| Google Sheets quota excedida | Médio | Baixa | Fallback SQLite já implementado |
| MASTER_KEY vazar em log/git | Alto | Média | **Fase 0.1 — urgente** |
| App sem auth acessível por qualquer um na rede | Alto | Alta | Fase 4.1 (SSO) |
| Path de CSVs quebrado após mover arquivos | Médio | Média | Configurar via `.env` |

---

## Convenções e Padrões de Código

- Módulos: `snake_case`
- Classes: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`
- Comentários em português (padrão do projeto)
- Commits: `[fase] tipo: descrição` — ex: `[F0] fix: remove MASTER_KEY hardcoded`
- Branches: `fase/0-seguranca`, `fase/1-historico`, etc.
- Testar localmente antes de commitar dados reais (usar `.env.local`)

---

## Checklist de Entrega por Fase

### Fase 0 — Done quando:
- [ ] Nenhuma chave secreta em arquivo versionado
- [ ] App carrega dados reais das lojas (não mock)
- [ ] Google Sheets salva e lê templates corretamente

### Fase 1 — Done quando:
- [ ] Histórico exibe templates salvos com filtros
- [ ] Busca retorna resultado em < 200ms
- [ ] Filtros por estado/região/status funcionam
- [ ] Formulários validam campos obrigatórios

### Fase 2 — Done quando:
- [ ] Chamados Vivo/Claro auto-preenchidos por VD
- [ ] Dashboard tem gráficos com dados reais
- [ ] Busca fuzzy encontra lojas com erros de digitação

### Fase 3 — Done quando:
- [ ] Loading states visíveis em todas as operações lentas
- [ ] Página de Ajuda completa e acessível
- [ ] Auto-complete no campo de busca

### Fase 4 — Done quando:
- [ ] Login obrigatório com SSO ou autenticação básica
- [ ] Sync automático de dados configurado e testado
