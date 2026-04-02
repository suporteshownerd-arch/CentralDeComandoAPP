# Análise Comparativa: Documento vs Implementação

## Resumo Executivo

| Módulo | Documento | Implementado | Status |
|--------|-----------|--------------|--------|
| Consulta de Lojas | ✅ Completo | ✅ ~90% | 🟡 Pendente |
| Gestão de Crises | ✅ Completo | ✅ ~80% | 🟡 Pendente |
| Histórico | ✅ Completo | ✅ ~70% | 🟡 Pendente |
| Abertura de Chamados | ✅ Completo | ✅ ~60% | 🟡 Pendente |

---

## 2.1 Consulta de Lojas

| Funcionalidade | Documento | App.py | Pendente |
|----------------|-----------|--------|----------|
| Modo VD/Designação | ✅ | ✅ | - |
| Modo Endereço | ✅ | ✅ | - |
| Modo Nome de Loja | ✅ | ✅ | - |
| Modo Informação Livre | ✅ | ✅ | - |
| VD, Nome, CNPJ | ✅ | ✅ | - |
| Endereço, Cidade, Estado | ✅ | ✅ | - |
| Telefones, WhatsApp, Email | ✅ | ✅ | - |
| Horário de funcionamento | ✅ | ✅ | - |
| GGL e GR com telefones | ✅ | ✅ | - |
| Designações MPLS/INN | ✅ | ✅ | - |
| **E-mail pré-formatado** | ✅ | ❌ | Implementar |
| Abertura Vivo | ✅ | ❌ | Implementar |
| Abertura Claro | ✅ | ❌ | Implementar |
| **Filtros (Estado/Região)** | ❌ | ❌ | 🆕 Adicionar |

---

## 2.2 Gestão de Crises

### Tipo 1 - Alertas Executivos

| Campo | Documento | App.py | Pendente |
|-------|-----------|--------|----------|
| Escopo da Crise | ✅ | ✅ | - |
| Identificação | ✅ | ✅ | - |
| Horário de Início | ✅ | ✅ | - |
| Horário de Término | ✅ | ✅ | - |
| Abrangência | ✅ | ✅ | - |
| Equipes Acionadas | ✅ | ✅ | - |
| Ação / Status | ✅ | ✅ | - |
| Templates Abertura/Atualização/Normalização | ✅ | ✅ | - |
| **Custom Escopo** | ✅ | ❌ | Implementar |

### Tipo 2 - Gestão de Crise

| Campo | Documento | App.py | Pendente |
|-------|-----------|--------|----------|
| Nº do Incidente | ✅ | ✅ | - |
| Link da Sala | ✅ | ✅ | - |
| Unidades Impactadas | ✅ | ✅ | - |
| Causa | ✅ | ✅ | - |
| Responsável Técnico | ✅ | ✅ | - |
| Responsável Command | ✅ | ✅ | - |
| Horários | ✅ | ✅ | - |
| **Histórico de Atualizações** | ✅ | ❌ | Implementar |
| **Próximo Status (+30min)** | ✅ | ❌ | Implementar |
| Template Abertura/Normalização | ✅ | ✅ | - |

### Tipo 3 - Loja Isolada

| Campo | Documento | App.py | Pendente |
|-------|-----------|--------|----------|
| VD da Loja | ✅ | ✅ | - |
| Tipo (Energia/Internet) | ✅ | ✅ | - |
| Horário Início | ✅ | ✅ | - |
| Horário Retorno | ✅ | ✅ | - |
| **4 templates automáticos** | ✅ | ❌ | 2 templates vs 4 |

---

## 2.3 Histórico e Persistência

| Funcionalidade | Documento | App.py | Pendente |
|----------------|-----------|--------|----------|
| Salvar no Google Sheets | ✅ | ❌ | Configurar API |
| Ler do Google Sheets | ✅ | ❌ | Configurar API |
| Limite 99 registros | ✅ | ❌ | Implementar |
| Rotação automática | ✅ | ❌ | Implementar |
| Navegação (próximo/anterior) | ✅ | ❌ | Implementar |
| Ver Histórico na interface | ✅ | ⚠️ | Parcial |

---

## 3. Arquitetura e Dados

| Componente | Documento | App.py | Status |
|------------|-----------|--------|--------|
| CSVs Fernet criptografados | ✅ | ❌ | Pendente |
| 6 arquivos de dados | ✅ | ❌ | Pendente |
| Google Sheets API v4 | ✅ | ⚠️ | Estrutura pronta |
| Integração WhatsApp wa.me | ✅ | ✅ | OK |
| Portal Vivo MVE link | ✅ | ✅ | OK |
| Portal Claro link | ✅ | ✅ | OK |

---

## 3.3 Configurações Necessárias

| Variável | Documento | .env.example | Status |
|----------|-----------|--------------|--------|
| master_key | ✅ | ✅ | OK |
| gcp_service_account | ✅ | ✅ | OK |
| sheets-id-aexec | ✅ | ✅ | OK |
| sheets-id-gcrises | ✅ | ✅ | OK |

---

## 4. Guias Rápidos

| Guia | Documento | App.py | Status |
|------|-----------|--------|--------|
| Consulta por VD | ✅ | ✅ | OK |
| Gerar Alerta Executivo | ✅ | ⚠️ | Parcial |
| Gerar Alerta Gestão de Crise | ✅ | ⚠️ | Parcial |
| Informativo Loja Isolada | ✅ | ⚠️ | Parcial |
| Consultar Histórico | ✅ | ❌ | Implementar |

---

## 📌 Prioridades de Implementação

### 🔴 Alta Prioridade
1. **E-mail pré-formatado** - Botão funcional
2. **Chamados Vivo/Claro** - Textos completos
3. **4 templates Loja Isolada** - Energia + Internet abertura/fechamento
4. **Google Sheets** - Configurar API

### 🟡 Média Prioridade
5. **Custom Escopo** - Campo adicional
6. **Histórico de Atualizações** - Lista dinâmica
7. **Próximo Status** - Cálculo automático +30min
8. **Ver Histórico** - Botão na interface

### 🟢 Baixa Prioridade
9. **CSVs Fernet** - Backend com arquivos reais
10. **Navegação Histórico** - Botões anterior/próximo
11. **Filtros por Estado/Região** -melhoria UX

---

## Conclusão

O frontend Streamlit está ~70% completo conforme especificação. As principais lacunas são:
- Funcionalidade dos botões (e-mail, chamados)
- Templates completos (4 tipos Loja Isolada)
- Integração Google Sheets (API configurada mas não conectada)
- Histórico de atualizações dinâmico

**Próximo passo recomendado:** Implementar funcionalidades de botões e configurar variáveis de ambiente no Streamlit Cloud.
