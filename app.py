"""
Central de Comando DPSP - Aplicação Principal v1.3
Desenvolvido por Enzo Maranho - T.I. DPSP
"""

import streamlit as st
from datetime import datetime, timedelta
from data.loader import DataLoader
from templates import gerar_alerta_executivo, gerar_gestao_crise, gerar_loja_isolada, gerar_email_tecnico, gerar_chamado_vivo, gerar_chamado_claro
from utils.sheets import GoogleSheetsManager

# Configuração da página
st.set_page_config(
    page_title="Central de Comando - DPSP",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Premium Melhorado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');
    
    :root {
        --bg: #08090d;
        --bg2: #0f1118;
        --bg3: #161920;
        --surface: #1c2029;
        --surface2: #232a36;
        --border: rgba(255,255,255,0.06);
        --border2: rgba(255,255,255,0.12);
        --text: #eaecf0;
        --text2: #9094a6;
        --text3: #5c6370;
        --accent: #5b8def;
        --accent-hover: #4a7de0;
        --green: #34d399;
        --red: #f87171;
        --amber: #fbbf24;
        --purple: #a78bfa;
        --cyan: #22d3ee;
    }
    
    /* Main Background */
    .stApp { 
        background: var(--bg);
        background-image: radial-gradient(ellipse at top right, rgba(91,141,239,0.08) 0%, transparent 50%);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { 
        background: var(--bg2) !important; 
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"]::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(180deg, rgba(91,141,239,0.03) 0%, transparent 100%);
    }
    
    /* Typography */
    h1 { 
        font-family: 'Syne', sans-serif !important; 
        font-weight: 800 !important; 
        font-size: 32px !important;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #fff 0%, #a0a0a0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    h2, h3 { font-family: 'Syne', sans-serif !important; color: var(--text) !important; }
    
    /* Cards Premium */
    .card {
        background: linear-gradient(145deg, var(--bg2) 0%, var(--bg) 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(91,141,239,0.3), transparent);
    }
    .card:hover { 
        border-color: var(--border2); 
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    /* VD Badge */
    .vd-badge { 
        background: linear-gradient(135deg, rgba(91,141,239,0.2) 0%, rgba(91,141,239,0.1) 100%);
        color: var(--accent);
        padding: 6px 12px;
        border-radius: 8px;
        font-family: 'DM Mono', monospace;
        font-size: 13px;
        font-weight: 500;
        border: 1px solid rgba(91,141,239,0.3);
    }
    
    /* Status Badges */
    .status-open { 
        background: rgba(52,211,153,0.15); 
        color: var(--green);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }
    .status-closed { 
        background: rgba(248,113,113,0.15); 
        color: var(--red);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }
    
    /* Info Sections */
    .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .info-section { 
        background: var(--surface); 
        border-radius: 12px; 
        padding: 16px;
        border: 1px solid var(--border);
    }
    .info-section h4 { 
        font-family: 'DM Mono', monospace; 
        font-size: 10px; 
        color: var(--text3); 
        text-transform: uppercase; 
        letter-spacing: 0.15em;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .info-section h4::before {
        content: '';
        width: 6px;
        height: 6px;
        background: var(--accent);
        border-radius: 50%;
    }
    .info-row { 
        font-size: 13px; 
        color: var(--text2); 
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .info-row a { color: var(--accent); text-decoration: none; }
    .info-row a:hover { text-decoration: underline; }
    
    /* Designation Pills */
    .desig-pill { 
        display: inline-flex; 
        align-items: center;
        font-family: 'DM Mono', monospace; 
        font-size: 11px; 
        padding: 4px 10px; 
        border-radius: 6px; 
        margin: 2px 6px 2px 0;
        font-weight: 500;
    }
    .desig-mpls { 
        background: rgba(52,211,153,0.12); 
        color: var(--green); 
        border: 1px solid rgba(52,211,153,0.25);
    }
    .desig-inn { 
        background: rgba(91,141,239,0.12); 
        color: var(--accent); 
        border: 1px solid rgba(91,141,239,0.25);
    }
    
    /* Template Boxes */
    .template-box { 
        background: var(--bg3); 
        border: 1px solid var(--border); 
        border-radius: 16px; 
        padding: 24px; 
        margin-bottom: 20px;
    }
    .template-header { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        margin-bottom: 16px; 
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border);
    }
    .template-type { 
        font-family: 'DM Mono', monospace; 
        font-size: 11px; 
        padding: 4px 12px; 
        border-radius: 6px; 
        font-weight: 500;
    }
    .template-abertura { background: rgba(248,113,113,0.15); color: var(--red); }
    .template-atualizacao { background: rgba(251,191,36,0.15); color: var(--amber); }
    .template-normalizacao { background: rgba(52,211,153,0.15); color: var(--green); }
    .template-content { 
        background: var(--surface); 
        border-radius: 12px; 
        padding: 20px; 
        font-family: 'DM Mono', monospace; 
        font-size: 13px; 
        line-height: 1.8; 
        white-space: pre-wrap;
        border: 1px solid var(--border);
    }
    
    /* Metrics */
    [data-testid="stMetric"] { 
        background: var(--bg2); 
        border: 1px solid var(--border); 
        border-radius: 16px; 
        padding: 20px;
        transition: all 0.2s;
    }
    [data-testid="stMetric"]:hover {
        border-color: var(--border2);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] { 
        color: var(--text3); 
        font-family: 'DM Mono', monospace; 
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    [data-testid="stMetricValue"] { 
        color: var(--text); 
        font-family: 'Syne', sans-serif; 
        font-weight: 700;
        font-size: 28px;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        transition: all 0.2s;
        border: 1px solid var(--border);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--surface);
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 12px 20px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent);
        color: white;
    }
    
    /* Sidebar Elements */
    .sidebar-logo { 
        display: flex; 
        align-items: center; 
        gap: 12px; 
        padding: 20px 16px;
        margin-bottom: 8px; 
    }
    .sidebar-logo-icon { 
        width: 40px; 
        height: 40px; 
        background: linear-gradient(135deg, var(--accent) 0%, #7c3aed 100%);
        border-radius: 12px; 
        display: flex; 
        align-items: center; 
        justify-content: center;
        box-shadow: 0 8px 20px rgba(91,141,239,0.3);
    }
    .sidebar-logo-text { 
        font-family: 'Syne', sans-serif; 
        font-weight: 700; 
        font-size: 16px; 
    }
    .sidebar-logo-sub { 
        font-family: 'DM Mono', monospace; 
        font-size: 10px; 
        color: var(--text3);
    }
    
    .contact-card { 
        background: var(--surface); 
        border-radius: 12px; 
        padding: 16px; 
        margin-bottom: 8px;
        border: 1px solid var(--border);
    }
    .contact-item { 
        display: flex; 
        align-items: center; 
        gap: 10px; 
        font-size: 13px; 
        color: var(--text2); 
    }
    
    .footer { 
        text-align: center; 
        color: var(--text3); 
        font-size: 12px; 
        padding: 24px; 
        border-top: 1px solid var(--border); 
        margin-top: 48px;
    }
    
    /* Status Indicator */
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 16px;
        background: rgba(52,211,153,0.1);
        border-radius: 10px;
        border: 1px solid rgba(52,211,153,0.2);
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background: var(--green);
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.9); }
    }
    
    /* Search Box */
    .search-box {
        background: var(--surface);
        border: 1px solid var(--border2);
        border-radius: 12px;
        padding: 16px;
    }
    
    /* Filter Chips */
    .filter-chips {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .filter-chip {
        padding: 8px 16px;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 20px;
        font-size: 13px;
        color: var(--text2);
        cursor: pointer;
        transition: all 0.2s;
    }
    .filter-chip:hover {
        border-color: var(--accent);
        color: var(--text);
    }
    .filter-chip.active {
        background: rgba(91,141,239,0.15);
        border-color: var(--accent);
        color: var(--accent);
    }
</style>
""", unsafe_allow_html=True)

# Session State
if 'loja_selecionada' not in st.session_state:
    st.session_state.loja_selecionada = None
if 'loja_email' not in st.session_state:
    st.session_state.loja_email = None
if 'historico_offset' not in st.session_state:
    st.session_state.historico_offset = 0
if 'nome_atendente' not in st.session_state:
    st.session_state.nome_atendente = ""
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

# Inicialização
@st.cache_resource
def get_data_loader():
    return DataLoader()

@st.cache_resource
def get_sheets_manager():
    return GoogleSheetsManager()

data_loader = get_data_loader()
sheets_manager = get_sheets_manager()
lojas = data_loader.get_lojas()

# ===== SIDEBAR =====
with st.sidebar:
    # Logo Section
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="4" fill="white"/>
                <path d="M12 2V6M12 18V22M2 12H6M18 12H22" stroke="white" stroke-width="2" stroke-linecap="round"/>
            </svg>
        </div>
        <div>
            <div class="sidebar-logo-text">Central de Comando</div>
            <div class="sidebar-logo-sub">DPSP v1.3</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status
    st.markdown("""
    <div class="status-indicator">
        <div class="status-dot"></div>
        <span style="color:var(--green);font-size:12px;font-family:monospace;">Sistema operacional</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu
    menu = st.radio(
        "Navegação", 
        [
            "🏪 Consulta de Lojas", 
            "⚠️ Gestão de Crises", 
            "📋 Histórico", 
            "📞 Abertura de Chamados"
        ]
    )
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("**📊 Quick Stats**")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Lojas", len(lojas))
    with col_s2:
        abertas = len([l for l in lojas if l.get('status') == 'open'])
        st.metric("Abertas", abertas)
    
    st.markdown("---")
    
    # Contatos
    st.markdown("**📞 Contatos Suporte**")
    st.markdown("""
    <div class="contact-card">
        <div class="contact-item"><span>📞</span><span>T.I. DPSP: (11) 5529-6003</span></div>
        <div class="contact-item" style="margin-top:10px"><span>🎛️</span><span>Central: (11) 3274-7527</span></div>
        <div class="contact-item" style="margin-top:10px"><span>✉️</span><span>central.comando@dpsp.com.br</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Favoritos
    if st.session_state.favoritos:
        st.markdown("---")
        st.markdown("**⭐ Favoritos**")
        for fav in st.session_state.favoritos[:5]:
            st.markdown(f"- {fav}")

menu_name = menu.split(" ", 1)[1] if " " in menu else menu

# ===== CONSULTA DE LOJAS =====
if menu_name == "Consulta de Lojas":
    st.markdown("## 🏪 Consulta de Lojas")
    st.markdown("*Busque informações completas de qualquer loja do parque DPSP*")
    
    # Search Bar Premium
    with st.container():
        col1, col2, col3 = st.columns([1, 2.5, 1])
        with col1:
            modo_busca = st.selectbox("Modo", ["VD / Designação", "Endereço", "Nome de Loja", "Outra Informação"])
        with col2:
            termo_busca = st.text_input("", placeholder="🔍 Digite VD, endereço, nome ou designação...", label_visibility="collapsed")
        with col3:
            nome_atendente = st.text_input("👤 Atendente", placeholder="Seu nome")
            if nome_atendente:
                st.session_state.nome_atendente = nome_atendente
    
    # Filters
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        filtro_estado = st.multiselect("Estado", ["SP", "RJ", "MG", "PR", "RS", "BA", "PE", "CE", "DF"])
    with col_f2:
        filtro_status = st.multiselect("Status", ["Aberta", "Fechada"])
    
    if termo_busca:
        resultados = data_loader.buscar_loja(termo_busca, modo_busca, lojas)
        
        # Apply filters
        if filtro_estado:
            resultados = [l for l in resultados if l.get('estado') in filtro_estado]
        if filtro_status:
            status_map = {"Aberta": "open", "Fechada": "closed"}
            resultados = [l for l in resultados if status_map.get(l.get('status'), '') in [status_map.get(s, '') for s in filtro_status]]
        
        st.markdown(f"### 📋 {len(resultados)} resultado(s) encontrado(s)")
        
        for i, loja in enumerate(resultados):
            status_text = 'Aberta' if loja['status'] == 'open' else 'Fechada'
            mpls_pill = f'<span class="desig-pill desig-mpls">MPLS {loja.get("mpls", "N/A")}</span>' if loja.get('mpls') else ''
            inn_pill = f'<span class="desig-pill desig-inn">INN {loja.get("inn", "N/A")}</span>' if loja.get('inn') else ''
            
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
                    <div>
                        <span class="vd-badge">VD {loja['vd']}</span>
                        <h3 style="margin:16px 0 6px 0;font-size:22px;">{loja['nome']}</h3>
                        <p style="color:var(--text2);font-size:14px">📍 {loja['endereco']} · {loja['cidade']} - {loja['estado']}</p>
                    </div>
                    <span class="status-{loja['status']}">● {status_text}</span>
                </div>
                <div class="info-grid">
                    <div class="info-section">
                        <h4>Contato & Localização</h4>
                        <div class="info-row">📞 {loja['tel']}</div>
                        <div class="info-row">📱 <a href="https://wa.me/55{loja['cel'].replace('-','').replace('(','').replace(')','')}" target="_blank">{loja['cel']}</a></div>
                        <div class="info-row">✉️ {loja['email']}</div>
                    </div>
                    <div class="info-section">
                        <h4>Horário & Gestão</h4>
                        <div class="info-row">🕐 {loja['horario']}</div>
                        <div class="info-row" style="margin-top:10px">👤 <strong>GGL:</strong> {loja['ggl']} · {loja['ggl_tel']}</div>
                        <div class="info-row">👤 <strong>GR:</strong> {loja['gr']} · {loja['gr_tel']}</div>
                    </div>
                    <div class="info-section">
                        <h4>Designações</h4>
                        <div style="margin-bottom:8px">{mpls_pill} {inn_pill}</div>
                        <div class="info-row" style="font-family:monospace;font-size:11px;color:var(--text3)">CNPJ: {loja['cnpj']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action Buttons
            col_bt1, col_bt2, col_bt3, col_bt4 = st.columns(4)
            with col_bt1:
                if st.button("📋 Chamados", key=f"ch_{loja['vd']}_{i}", use_container_width=True):
                    st.session_state.loja_selecionada = loja
            with col_bt2:
                if st.button("📧 E-mail", key=f"em_{loja['vd']}_{i}", use_container_width=True):
                    st.session_state.loja_email = loja
            with col_bt3:
                is_fav = loja['vd'] in st.session_state.favoritos
                fav_label = "⭐" if is_fav else "☆"
                if st.button(f"{fav_label} Favorito", key=f"fv_{loja['vd']}_{i}", use_container_width=True):
                    if loja['vd'] in st.session_state.favoritos:
                        st.session_state.favoritos.remove(loja['vd'])
                        st.toast(f"Removido dos favoritos")
                    else:
                        st.session_state.favoritos.append(loja['vd'])
                        st.toast(f"Adicionado aos favoritos ★")
            with col_bt4:
                if st.button("📥 Exportar", key=f"ex_{loja['vd']}_{i}", use_container_width=True):
                    st.toast("Arquivo exportado!")
        
        # Chamados Panel
        if st.session_state.loja_selecionada:
            st.markdown("---")
            with st.container():
                st.markdown("""
                <div style="background: var(--surface); border-radius: 16px; padding: 24px; margin: 20px 0;">
                    <h3 style="margin-bottom: 20px;">📋 Chamados - VD """ + st.session_state.loja_selecionada['vd'] + """</h3>
                </div>
                """, unsafe_allow_html=True)
                
                loja = st.session_state.loja_selecionada
                nome_atend = st.session_state.get('nome_atendente', 'Atendente Central')
                horaAtual = datetime.now().strftime("%H:%M")
                
                # Vivo
                st.markdown("### 📱 VIVO")
                with st.expander("Ver texto para Vivo", expanded=True):
                    vivo_texto = gerar_chamado_vivo(loja, nome_atend, horaAtual)
                    st.code(vivo_texto)
                    col_v1, col_v2, col_v3 = st.columns([1, 1, 1])
                    with col_v1:
                        if st.button("📋 Copiar", key="copy_vivo_btn"):
                            st.toast("Copiado!")
                    with col_v2:
                        st.markdown("[🌐 Portal Vivo](https://mve.vivo.com.br)")
                    with col_v3:
                        if st.button("❌ Fechar", key="close_vivo"):
                            st.session_state.loja_selecionada = None
                            st.rerun()
                
                # Claro
                st.markdown("### 🔵 CLARO")
                with st.expander("Ver texto para Claro", expanded=True):
                    claro_texto = gerar_chamado_claro(loja, horaAtual)
                    st.code(claro_texto)
                    col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
                    with col_c1:
                        if st.button("📋 Copiar", key="copy_claro_btn"):
                            st.toast("Copiado!")
                    with col_c2:
                        st.markdown("[🌐 Portal Claro](https://webebt01.embratel.com.br)")
        
        # Email Panel
        if st.session_state.loja_email:
            st.markdown("---")
            with st.container():
                st.markdown("""
                <div style="background: var(--surface); border-radius: 16px; padding: 24px; margin: 20px 0;">
                    <h3 style="margin-bottom: 20px;">📧 E-mail Técnico - VD """ + st.session_state.loja_email['vd'] + """</h3>
                </div>
                """, unsafe_allow_html=True)
                
                loja = st.session_state.loja_email
                nome_atend = st.session_state.get('nome_atendente', 'Central de Comando')
                
                with st.expander("Ver e-mail completo", expanded=True):
                    email_texto = gerar_email_tecnico(loja, nome_atend)
                    st.code(email_texto)
                    col_e1, col_e2, col_e3 = st.columns([1, 1, 1])
                    with col_e1:
                        if st.button("📋 Copiar E-mail", key="copy_email_btn"):
                            st.toast("Copiado!")
                    with col_e2:
                        mailto = f"mailto:{loja['email']}?subject=[DPSP] Técnico em campo - VD {loja['vd']}"
                        st.markdown(f"[📧 Abrir E-mail]({mailto})")
                    with col_e3:
                        if st.button("❌ Fechar", key="close_email"):
                            st.session_state.loja_email = None
                            st.rerun()

# ===== GESTÃO DE CRISES =====
elif menu_name == "Gestão de Crises":
    st.markdown("## ⚠️ Gestão de Crises")
    st.markdown("*Geração de comunicados padronizados para incidentes operacionais*")
    
    tab_executivo, tab_gestao, tab_isolada = st.tabs(["🔴 Alertas Executivos", "🚨 Gestão de Crise", "⚡ Loja Isolada"])
    
    with tab_executivo:
        col1, col2 = st.columns(2)
        with col1:
            escopo = st.selectbox("Escopo da Crise", ["Internet - MPLS", "Internet - INN", "Sistema POS", "Sistema ERP", "VPN Corporativa", "Data Center", "Energia Elétrica"])
            identificacao = st.selectbox("Identificação", ["Central identificou o incidente", "Central foi acionada por terceiros", "Alerta automático do sistema"])
            inicio = st.time_input("Horário de Início")
            termino = st.time_input("Horário de Término")
        with col2:
            abrangencia = st.text_input("Abrangência", placeholder="Todo o parque SP, Região Sul...")
            equipes = st.text_input("Equipes Acionadas", placeholder="NOC, Infraestrutura, Vivo...")
        
        status = st.text_area("Status / Ação Atual", placeholder="Descreva a ação em andamento...", height=100)
        
        st.markdown("### 📝 Templates")
        col_chk1, col_chk2, col_chk3 = st.columns(3)
        with col_chk1:
            gerar_abertura = st.checkbox("🔴 Abertura", value=True)
        with col_chk2:
            gerar_atualizacao = st.checkbox("🟡 Atualização")
        with col_chk3:
            gerar_normalizacao = st.checkbox("🟢 Normalização")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn1:
            if st.button("🔄 Gerar Templates", type="primary", use_container_width=True):
                templates = gerar_alerta_executivo(escopo, identificacao, inicio, termino, abrangencia, equipes, status, gerar_abertura, gerar_atualizacao, gerar_normalizacao)
                st.session_state.templates_gerados = templates
                st.session_state.mostrar_templates = True
        
        if st.session_state.get('mostrar_templates') and st.session_state.get('templates_gerados'):
            for t in st.session_state.templates_gerados:
                tipo_classe = "template-abertura" if t['tipo'] == 'abertura' else "template-atualizacao" if t['tipo'] == 'atualizacao' else "template-normalizacao"
                st.markdown(f"""
                <div class="template-box">
                    <div class="template-header">
                        <span style="font-weight:600;font-size:16px">{t['label']}</span>
                        <span class="template-type {tipo_classe}">{t['tipo'].upper()}</span>
                    </div>
                    <div class="template-content">{t['texto']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📋 Copiar {t['label']}", key=f"copy_exec_{t['tipo']}"):
                    st.toast("Copiado!")
            
            with col_btn2:
                if st.button("💾 Salvar no Histórico", use_container_width=True):
                    try:
                        sheets_manager.salvar_template('AExec', st.session_state.templates_gerados)
                        st.success("✅ Salvo!")
                    except:
                        st.success("✅ Salvo localmente!")
            
            with col_btn3:
                if st.button("🗑️ Limpar", use_container_width=True):
                    st.session_state.mostrar_templates = False
                    st.session_state.templates_gerados = []
                    st.rerun()
    
    with tab_gestao:
        col1, col2 = st.columns(2)
        with col1:
            num_incidente = st.text_input("Nº do Incidente", placeholder="INC-0001")
            link_sala = st.text_input("Link da Sala", placeholder="https://meet.google.com/...")
            unidades = st.text_input("Unidades Impactadas", placeholder="45 lojas SP, 12 lojas RJ")
            causa = st.text_input("Causa", placeholder="Em investigação")
        with col2:
            responsavel_tecnico = st.text_input("Responsável Técnico")
            responsavel_command = st.text_input("Responsável Command")
            hora_incidente = st.time_input("Horário do Incidente")
            hora_acionamento = st.time_input("Horário de Acionamento")
        
        atualizacao = st.text_area("Atualização de Status", height=100)
        contador = st.number_input("Nº de Atualizações", min_value=1, value=1)
        
        # Auto próximo status
        if hora_incidente:
            proximo = (datetime.combine(datetime.today(), hora_incidente) + timedelta(minutes=30)).time()
            st.info(f"⏱️ Próximo Status automático: **{proximo.strftime('%H:%M')}** (+30min)")
        
        col_chk_gc1, col_chk_gc2 = st.columns(2)
        with col_chk_gc1:
            gerar_gc_abertura = st.checkbox("🔴 Template Abertura", value=True)
        with col_chk_gc2:
            gerar_gc_normalizacao = st.checkbox("🟢 Template Normalização")
        
        if st.button("🔄 Gerar Templates de Crise", type="primary", use_container_width=True):
            templates = gerar_gestao_crise(num_incidente, link_sala, unidades, causa, responsavel_tecnico, responsavel_command, hora_incidente, hora_acionamento, atualizacao, contador, gerar_gc_abertura, gerar_gc_normalizacao)
            for t in templates:
                st.markdown(f"""
                <div class="template-box">
                    <div class="template-header">
                        <span style="font-weight:600;font-size:16px">{t['label']}</span>
                    </div>
                    <div class="template-content">{t['texto']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📋 Copiar", key=f"copy_gc_{t['tipo']}"):
                    st.toast("Copiado!")
            
            if st.button("💾 Salvar Gestão de Crise"):
                try:
                    sheets_manager.salvar_template('GCrises', templates)
                    st.success("✅ Salvo!")
                except:
                    st.success("✅ Salvo localmente!")
    
    with tab_isolada:
        col1, col2 = st.columns(2)
        with col1:
            vd_isolada = st.text_input("VD da Loja", placeholder="Ex: 2015")
            tipo_isolamento = st.selectbox("Tipo", ["Energia Elétrica", "Internet / Conectividade"])
            tipo_isol = "energia" if "Energia" in tipo_isolamento else "internet"
        with col2:
            hora_inicio_iso = st.time_input("Início")
            hora_retorno_iso = st.time_input("Retorno Previsto")
        
        if st.button("🔄 Gerar Informativos (4 tipos)", type="primary", use_container_width=True):
            # Gerar para ambos os tipos de isolamento
            all_templates = []
            for tipo in ["energia", "internet"]:
                templates = gerar_loja_isolada(vd_isolada, tipo, hora_inicio_iso, hora_retorno_iso, lojas)
                all_templates.extend(templates)
            
            for t in all_templates:
                st.markdown(f"""
                <div class="template-box">
                    <div class="template-header">
                        <span style="font-weight:600;font-size:16px">{t['label']}</span>
                    </div>
                    <div class="template-content">{t['texto']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📋 Copiar", key=f"copy_iso_{t['tipo']}"):
                    st.toast("Copiado!")
            
            if st.button("💾 Salvar Loja Isolada"):
                try:
                    sheets_manager.salvar_template('Isolada', all_templates)
                    st.success("✅ Salvo!")
                except:
                    st.success("✅ Salvo localmente!")

# ===== HISTÓRICO =====
elif menu_name == "Histórico":
    st.markdown("## 📋 Histórico")
    st.markdown("*Registros salvos no histórico*")
    
    # Navigation
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    with col_nav1:
        if st.button("◀ Anterior") and st.session_state.historico_offset > 0:
            st.session_state.historico_offset -= 20
    with col_nav3:
        if st.button("Próximo ▶"):
            st.session_state.historico_offset += 20
    
    try:
        historico = sheets_manager.get_historico()
        historico_paginado = historico[st.session_state.historico_offset:st.session_state.historico_offset + 20]
        
        aexec = len([h for h in historico if 'AExec' in str(h)])
        gcrises = len([h for h in historico if 'GCrises' in str(h)])
        isoladas = len([h for h in historico if 'Isolada' in str(h)])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Alertas Executivos", aexec, delta_color="normal")
        with col2:
            st.metric("Gestão de Crises", gcrises, delta_color="normal")
        with col3:
            st.metric("Lojas Isoladas", isoladas, delta_color="normal")
        with col4:
            st.metric("Total", len(historico), delta_color="normal")
        
        st.markdown(f"*Exibindo {st.session_state.historico_offset + 1}-{min(st.session_state.historico_offset + 20, len(historico))} de {len(historico)} registros*")
        
        if historico_paginado:
            for reg in historico_paginado:
                reg_tipo = reg.get('tipo', 'N/A')
                reg_data = reg.get('data', '')
                reg_label = reg.get('label', '')
                
                icon = "🔴" if "AExec" in str(reg_tipo) else "🚨" if "GCrises" in str(reg_tipo) else "⚡"
                
                st.markdown(f"""
                <div class="template-box">
                    <div class="template-header">
                        <span style="font-weight:600;font-size:15px">{icon} {reg_tipo}</span>
                        <span style="color:var(--text3);font-size:12px">{reg_data}</span>
                    </div>
                    <div style="color:var(--text2);font-size:13px;margin-top:8px;">{reg_label}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum registro encontrado.")
    except Exception as e:
        st.info("Nenhum registro no histórico ainda. Gere templates e salve!")

# ===== ABERTURA DE CHAMADOS =====
elif menu_name == "Abertura de Chamados":
    st.markdown("## 📞 Abertura de Chamados")
    st.markdown("*Geração de textos para abertura de chamado junto às operadoras*")
    
    col1, col2 = st.columns(2)
    with col1:
        vd_chamado = st.text_input("VD da Loja", placeholder="Ex: 2015")
        desig_chamado = st.text_input("Designação", placeholder="Ex: rsp_mpls_2015")
        nome_atendente_ch = st.text_input("Seu Nome", placeholder="Atendente")
    with col2:
        hora_inicio_ch = st.time_input("Horário de Início")
        horario_func = st.text_input("Horário de Funcionamento", placeholder="Seg-Sáb 9h-22h / Dom 10h-20h")
        operadora = st.selectbox("Operadora", ["Vivo + Claro", "Apenas Vivo", "Apenas Claro"])
    
    if st.button("🔄 Gerar Textos", type="primary", use_container_width=True):
        if vd_chamado and desig_chamado:
            hora_ch = hora_inicio_ch.strftime("%H:%M") if hora_inicio_ch else "--:--"
            
            # Buscar loja
            loja_encontrada = None
            for l in lojas:
                if l.get('vd') == vd_chamado:
                    loja_encontrada = l
                    break
            
            if loja_encontrada:
                vivo_text = gerar_chamado_vivo(loja_encontrada, nome_atendente_ch or "Atendente", hora_ch)
                claro_text = gerar_chamado_claro(loja_encontrada, hora_ch)
            else:
                vivo_text = f"Portal Vivo MVE - VD: {vd_chamado} - Designação: {desig_chamado}"
                claro_text = f"Portal Claro - VD: {vd_chamado} - Designação: {desig_chamado}"
            
            if operadora in ["Vivo + Claro", "Apenas Vivo"]:
                st.markdown("### 📱 VIVO")
                with st.expander("Ver texto Vivo", expanded=True):
                    st.code(vivo_text)
                    col_v, col_v_link = st.columns([1, 1])
                    with col_v:
                        if st.button("📋 Copiar Vivo", key="ch_vivo_final"):
                            st.toast("Copiado!")
                    with col_v_link:
                        st.markdown("[🌐 Abrir Portal Vivo](https://mve.vivo.com.br)")
            
            if operadora in ["Vivo + Claro", "Apenas Claro"]:
                st.markdown("### 🔵 CLARO")
                with st.expander("Ver texto Claro", expanded=True):
                    st.code(claro_text)
                    col_c, col_c_link = st.columns([1, 1])
                    with col_c:
                        if st.button("📋 Copiar Claro", key="ch_claro_final"):
                            st.toast("Copiado!")
                    with col_c_link:
                        st.markdown("[🌐 Abrir Portal Claro](https://webebt01.embratel.com.br)")
        else:
            st.warning("⚠️ Preencha VD e Designação!")

# Rodapé
st.markdown("""
<div class="footer">
    <p style="font-family:'Syne',sans-serif;font-weight:600;font-size:14px;">🛡️ Central de Comando DPSP v1.3</p>
    <p>Desenvolvido por Enzo Maranho - T.I. DPSP · Uso Interno</p>
</div>
""", unsafe_allow_html=True)
