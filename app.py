"""
Central de Comando DPSP - Versão Ultra Estável v2.5
Sem imports dinâmicos - tudo inline
"""

import streamlit as st

# Configuração
st.set_page_config(page_title="Central de Comando - DPSP", page_icon="🛡️", layout="wide")

# CSS simples
st.markdown("""
<style>
    .stApp { background: #08090d; }
    h1, h2, h3 { color: #eaecf0; font-family: sans-serif; }
    .card { background: #0f1118; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 16px; margin: 8px 0; }
    .vd-badge { background: rgba(91,141,239,0.2); color: #5b8def; padding: 4px 8px; border-radius: 6px; font-family: monospace; }
    .status-open { color: #34d399; }
    .status-closed { color: #f87171; }
    section[data-testid="stSidebar"] { background: #0f1118; }
</style>
""", unsafe_allow_html=True)

# Session state
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []
if 'loja_selecionada' not in st.session_state:
    st.session_state.loja_selecionada = None

# Dados de exemplo
LOJAS = [
    {"vd": "318", "nome": "DSP SANTA BARBARA D'OESTE", "endereco": "AV DE CILLO,167", "cidade": "SANTA BARBARA D'OESTE", "estado": "SP", "status": "open"},
    {"vd": "322", "nome": "DSP SAO CARLOS", "endereco": "AV SAO CARLOS,2358", "cidade": "SAO CARLOS", "estado": "SP", "status": "open"},
    {"vd": "339", "nome": "DSP SHOPPING TAMBORE", "endereco": "AVENIDA PIRACEMA,669", "cidade": "BARUERI", "estado": "SP", "status": "open"},
    {"vd": "345", "nome": "DSP PORTUGAL II", "endereco": "AV PORTUGAL,602", "cidade": "SANTO ANDRE", "estado": "SP", "status": "open"},
    {"vd": "348", "nome": "DSP JARDIM MIRIAM", "endereco": "AV CUPECE,5400", "cidade": "SAO PAULO", "estado": "SP", "status": "open"},
]

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("### 🛡️ Central de Comando")
        st.markdown("**DPSP v2.5**")
        st.markdown("---")
        
        st.metric("Total Lojas", len(LOJAS))
        st.metric("Ativas", len([l for l in LOJAS if l['status'] == 'open']))
        
        st.markdown("---")
        menu = st.radio("Menu", [
            "🏪 Consulta de Lojas",
            "⚠️ Gestão de Crises", 
            "📋 Histórico",
            "📞 Abertura de Chamados",
            "📈 Dashboard"
        ])
    
    # Página
    if "Consulta" in menu:
        render_consulta()
    elif "Crises" in menu:
        render_crises()
    elif "Histórico" in menu:
        render_historico()
    elif "Chamados" in menu:
        render_chamados()
    elif "Dashboard" in menu:
        render_dashboard()


def render_consulta():
    st.markdown("## 🏪 Consulta de Lojas")
    st.markdown("*Busque informações completas de qualquer loja do parque DPSP*")
    
    st.metric("Total Lojas", len(LOJAS))
    st.markdown("---")
    
    termo = st.text_input("Buscar", placeholder="Digite VD ou nome...")
    
    resultados = LOJAS
    if termo:
        termo_lower = termo.lower()
        resultados = [l for l in LOJAS if termo_lower in str(l.get('vd','')).lower() or termo_lower in str(l.get('nome','')).lower()]
    
    st.markdown(f"**{len(resultados)} resultado(s)**")
    
    for i, loja in enumerate(resultados[:20]):
        with st.container():
            st.markdown(f"**VD {loja['vd']}** - {loja['nome']}")
            st.caption(f"📍 {loja['endereco']} - {loja['cidade']}/{loja['estado']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Status: {'🟢' if loja['status']=='open' else '🔴'}")
            with col2:
                if st.button(f"⭐", key=f"fav_{loja['vd']}_{i}"):
                    vd = str(loja['vd'])
                    if vd in st.session_state.favoritos:
                        st.session_state.favoritos.remove(vd)
                    else:
                        st.session_state.favoritos.append(vd)
            with col3:
                if st.button(f"📋", key=f"btn_{loja['vd']}_{i}"):
                    st.session_state.loja_selecionada = loja
            
            st.markdown("---")


def render_crises():
    st.markdown("## ⚠️ Gestão de Crises")
    st.info("Nenhum incidente ativo no momento")
    
    tab1, tab2, tab3 = st.tabs(["🔴 Alertas", "🚨 Crise", "⚡ Isolada"])
    with tab1:
        st.markdown("### Alertas Executivos")
        st.text_input("Escopo")
        st.text_input("Abrangência")
        st.text_area("Status")
        if st.button("Gerar"):
            st.success("Template gerado!")


def render_historico():
    st.markdown("## 📋 Histórico")
    st.info("Nenhum registro")


def render_chamados():
    st.markdown("## 📞 Abertura de Chamados")
    col1, col2 = st.columns(2)
    with col1:
        vd = st.text_input("VD")
        nome = st.text_input("Seu Nome")
    with col2:
        hora = st.time_input("Hora")
        op = st.selectbox("Operadora", ["Vivo", "Claro", "Ambas"])
    
    if st.button("Gerar"):
        st.success("Texto gerado!")


def render_dashboard():
    st.markdown("## 📈 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Lojas", len(LOJAS))
    with col2:
        st.metric("Ativas", len([l for l in LOJAS if l['status']=='open']))
    with col3:
        st.metric("Inativas", len([l for l in LOJAS if l['status']=='closed']))
    with col4:
        st.metric("Estados", len(set(l['estado'] for l in LOJAS)))
    
    st.markdown("### Lojas por Estado")
    estados = {}
    for l in LOJAS:
        e = l.get('estado', 'Outro')
        estados[e] = estados.get(e, 0) + 1
    for e, c in sorted(estados.items(), key=lambda x: x[1], reverse=True):
        st.write(f"{e}: {c}")


if __name__ == "__main__":
    main()