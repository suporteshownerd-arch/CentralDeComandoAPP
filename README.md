# Central de Comando DPSP

Aplicação web interna para a equipe de T.I. da DPSP. Centraliza consulta de lojas, gestão de crises e abertura de chamados.

## 🚀 Quick Start

```bash
# 1. Clone o repositório
git clone https://github.com/suporteshownerd-arch/CentralDeComandoAPP.git
cd CentralDeComandoAPP

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# 5. Execute a aplicação
streamlit run app.py
```

## 📋 Módulos

- **Consulta de Lojas**: Busca por VD, endereço, nome ou informação livre
- **Gestão de Crises**: Alertas Executivos, Gestão de Crise, Loja Isolada
- **Histórico**: Registros salvos no Google Sheets
- **Abertura de Chamados**: Textos para Vivo e Claro

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `MASTER_KEY` | Chave Fernet para descriptografia | ✅ |
| `GCP_SERVICE_ACCOUNT` | JSON da Service Account | ✅ (para Sheets) |
| `SHEETS_ID_AEXEC` | ID planilha Alertas Executivos | ✅ |
| `SHEETS_ID_GCRISES` | ID planilha Gestão de Crises | ✅ |

## 📁 Estrutura

```
CentralDeComandoAPP/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências Python
├── .env.example         # Modelo de variáveis de ambiente
├── data/
│   └── loader.py        # Carregador de dados
├── templates/
│   └── __init__.py      # Templates de comunicados
├── utils/
│   └── sheets.py        # Integração Google Sheets
└── .streamlit/
    └── config.toml      # Configurações Streamlit
```

## 📞 Contatos

- **Central de Comando**: (11) 3274-7527
- **T.I. DPSP**: (11) 5529-6003
- **E-mail**: central.comando@dpsp.com.br

---

**Desenvolvido por Enzo Maranho - T.I. DPSP**
