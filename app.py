"""
Central de Comando DPSP - Aplicação Principal v1.4
Desenvolvido por Enzo Maranho - T.I. DPSP
"""

import streamlit as st
from datetime import datetime, timedelta
import time
from data.loader import DataLoader, CacheManager, UsageLogger
from templates import gerar_alerta_executivo, gerar_gestao_crise, gerar_loja_isolada, gerar_email_tecnico, gerar_chamado_vivo, gerar_chamado_claro
from utils.sheets import GoogleSheetsManager

# Configuração da página
st.set_page_config(
    page_title="Central de Comando - DPSP",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Premium Melhorado com Mobile
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
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .stApp { padding: 0 !important; }
        .stColumn { padding: 4px !important; }
        .card { padding: 16px !important; margin-bottom: 12px !important; }
        .info-grid { grid-template-columns: 1fr !important; }
        .sidebar-logo { padding: 12px !important; }
        h1 { font-size: 24px !important; }
    }
    
    .stApp { background: var(--bg); }
    section[data-testid="stSidebar"] { background: var(--bg2) !important; border-right: 1px solid var(--border); }
    
    h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; font-size: 32px !important; letter-spacing: -0.03em; }
    h2, h3 { font-family: 'Syne', sans-serif !important; color: var(--text) !important; }
    
    .card { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 24px; margin-bottom: 20px; transition: all 0.3s; }
    .card:hover { border-color: var(--border2); transform: translateY(-4px); box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
    
    .vd-badge { background: rgba(91,141,239,0.2); color: var(--accent); padding: 6px 12px; border-radius: 8px; font-family: 'DM Mono', monospace; font-size: 13px; }
    .status-open { background: rgba(52,211,153,0.15); color: var(--green); padding: 6px 14px; border-radius: 20px; font-size: 12px; }
    .status-closed { background: rgba(248,113,113,0.15); color: var(--red); padding: 6px 14px; border-radius: 20px; font-size: 12px; }
    
    .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    @media (max-width: 768px) { .info-grid { grid-template-columns: 1fr; } }
    
    .info-section { background: var(--surface); border-radius: 12px; padding: 16px; border: 1px solid var(--border); }
    .info-section h4 { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--text3); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 12px; }
    .info-row { font-size: 13px; color: var(--text2); margin-bottom: 8px; }
    .info-row a { color: var(--accent); text-decoration: none; }
    
    .desig-pill { display: inline-flex; font-family: 'DM Mono', monospace; font-size: 11px; padding: 4px 10px; border-radius: 6px; margin: 2px 6px 2px 0; }
    .desig-mpls { background: rgba(52,211,153,0.12); color: var(--green); border: 1px solid rgba(52,211,153,0.25); }
    .desig-inn { background: rgba(91,141,239,0.12); color: var(--accent); border: 1px solid rgba(91,141,239,0.25); }
    
    .template-box { background: var(--bg3); border: 1px solid var(--border); border-radius: 16px; padding: 24px; margin-bottom: 20px; }
    .template-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
    .template-type { font-family: 'DM Mono', monospace; font-size: 11px; padding: 4px 12px; border-radius: 6px; }
    .template-abertura { background: rgba(248,113,113,0.15); color: var(--red); }
    .template-atualizacao { background: rgba(251,191,36,0.15); color: var(--amber); }
    .template-normalizacao { background: rgba(52,211,153,0.15); color: var(--green); }
    .template-content { background: var(--surface); border-radius: 12px; padding: 20px; font-family: 'DM Mono', monospace; font-size: 13px; line-height: 1.8; white-space: pre-wrap; }
    
    [data-testid="stMetric"] { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 20px; }
    [data-testid="stMetricLabel"] { color: var(--text3); font-family: 'DM Mono', monospace; font-size: 11px; text-transform: uppercase; }
    [data-testid="stMetricValue"] { color: var(--text); font-family: 'Syne', sans-serif; font-weight: 700; font-size: 28px; }
    
    .stButton > button { border-radius: 10px; font-family: 'DM Sans', sans-serif; font-weight: 600; transition: all 0.2s; border: 1px solid var(--border); }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.3); }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: var(--surface); padding: 8px; border-radius: 12px; }
    .stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px; padding: 12px 20px; font-weight: 500; }
    .stTabs [aria-selected="true"] { background: var(--accent); color: white; }
    
    .sidebar-logo { display: flex; align-items: center; gap: 12px; padding: 20px 16px; }
    .sidebar-logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--accent) 0%, #7c3aed 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; }
    .sidebar-logo-text { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 16px; }
    .sidebar-logo-sub { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--text3); }
    
    .contact-card { background: var(--surface); border-radius: 12px; padding: 16px; border: 1px solid var(--border); }
    .contact-item { display: flex; align-items: center; gap: 10px; font-size: 13px; color: var(--text2); }
    
    .footer { text-align: center; color: var(--text3); font-size: 12px; padding: 24px; border-top: 1px solid var(--border); margin-top: 48px; }
    
    .status-indicator { display: flex; align-items: center; gap: 8px; padding: 10px 16px; background: rgba(52,211,153,0.1); border-radius: 10px; border: 1px solid rgba(52,211,153,0.2); }
    .status-dot { width: 8px; height: 8px; background: var(--green); border-radius: 50%; animation: pulse 2s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    
    /* Suggestions Dropdown */
    .suggestions-box { background: var(--surface); border: 1px solid var(--border2); border-radius: 12px; max-height: 200px; overflow-y: auto; margin-top: 4px; }
    .suggestion-item { padding: 10px 16px; cursor: pointer; border-bottom: 1px solid var(--border); transition: background 0.15s; }
    .suggestion-item:hover { background: var(--surface2); }
    .suggestion-item:last-child { border-bottom: none; }
    .suggestion-vd { font-family: 'DM Mono', monospace; color: var(--accent); font-size: 12px; }
    .suggestion-nome { color: var(--text); font-size: 14px; }
    .suggestion-endereco { color: var(--text3); font-size: 12px; }
    
    /* Loading Skeleton */
    .skeleton { background: linear-gradient(90deg, var(--surface) 25%, var(--surface2) 50%, var(--surface) 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 8px; }
    @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
    .skeleton-card { height: 200px; margin-bottom: 16px; }
    .skeleton-text { height: 20px; margin-bottom: 8px; }
    .skeleton-text-short { height: 20px; width: 60%; }
    
    /* KPI Cards */
    .kpi-card { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 20px; text-align: center; }
    .kpi-value { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 700; }
    .kpi-label { font-family: 'DM Mono', monospace; font-size: 11px; color: var(--text3); text-transform: uppercase; margin-top: 8px; }
    .kpi-delta { font-size: 12px; margin-top: 4px; }
    .kpi-delta.positive { color: var(--green); }
    .kpi-delta.negative { color: var(--red); }
    
    /* Better Toasts */
    .toast-success { background: rgba(52,211,153,0.15); border: 1px solid rgba(52,211,153,0.3); color: var(--green); padding: 12px 20px; border-radius: 10px; margin: 8px 0; }
    .toast-error { background: rgba(248,113,113,0.15); border: 1px solid rgba(248,113,113,0.3); color: var(--red); padding: 12px 20px; border-radius: 10px; margin: 8px 0; }
    .toast-info { background: rgba(91,141,239,0.15); border: 1px solid rgba(91,141,239,0.3); color: var(--accent); padding: 12px 20px; border-radius: 10px; margin: 8px 0; }
    
    /* Export Button */
    .export-btn { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 8px 16px; cursor: pointer; transition: all 0.2s; }
    .export-btn:hover { background: var(--surface2); border-color: var(--accent); }
    
    /* FAQ Cards */
    .faq-item { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin-bottom: 12px; }
    .faq-question { font-weight: 600; color: var(--text); margin-bottom: 8px; }
    .faq-answer { color: var(--text2); font-size: 13px; }
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
if 'loading' not in st.session_state:
    st.session_state.loading = False
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []
if 'kpi_data' not in st.session_state:
    st.session_state.kpi_data = {
        'buscas_hoje': 47,
        'chamados_hoje': 12,
        'crises_ativas': 2,
        'mttr_medio': '32min',
        'lojas_online': 156,
        'lojas_total': 162
    }
if 'busca_validada' not in st.session_state:
    st.session_state.busca_validada = None

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

# Funções de suggestions
def get_suggestions(termo, modo):
    """Retorna sugestões baseadas no termo de busca"""
    if not termo or len(termo) < 2:
        return []
    
    termo = termo.lower()
    sugestoes = []
    
    for loja in lojas:
        if modo == "VD / Designação":
            if termo in str(loja.get('vd', '')):
                sugestoes.append(loja)
            elif termo in str(loja.get('mpls', '')).lower():
                sugestoes.append(loja)
            elif termo in str(loja.get('inn', '')).lower():
                sugestoes.append(loja)
        elif modo == "Endereço":
            if termo in str(loja.get('endereco', '')).lower():
                sugestoes.append(loja)
        elif modo == "Nome de Loja":
            if termo in str(loja.get('nome', '')).lower():
                sugestoes.append(loja)
        elif modo == "Outra Informação":
            dados = str(loja).lower()
            if termo in dados:
                sugestoes.append(loja)
    
    return sugestoes[:8]

# ===== SIDEBAR =====
with st.sidebar:
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
            <div class="sidebar-logo-sub">DPSP v1.4</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="status-indicator">
        <div class="status-dot"></div>
        <span style="color:var(--green);font-size:12px;font-family:monospace;">Sistema operacional</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # KPIs na Sidebar
    st.markdown("**📊 KPIs em Tempo Real**")
    
    kpi = st.session_state.kpi_data
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color:var(--accent)">{kpi['buscas_hoje']}</div>
            <div class="kpi-label">Buscas Hoje</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color:var(--green)">{kpi['chamados_hoje']}</div>
            <div class="kpi-label">Chamados</div>
        </div>
        """, unsafe_allow_html=True)
    
    col_k3, col_k4 = st.columns(2)
    with col_k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color:var(--red)">{kpi['crises_ativas']}</div>
            <div class="kpi-label">Crises Ativas</div>
        </div>
        """, unsafe_allow_html=True)
    with col_k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="color:var(--green)">{kpi['lojas_online']}/{kpi['lojas_total']}</div>
            <div class="kpi-label">Lojas Online</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu
    menu = st.radio("Navegação", ["🏪 Consulta de Lojas", "⚠️ Gestão de Crises", "📋 Histórico", "📞 Abertura de Chamados", "📈 Dashboard", "❓ Ajuda"])
    
    st.markdown("---")
    
    # Quick Stats
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Total Lojas", len(lojas))
    with col_s2:
        abertas = len([l for l in lojas if l.get('status') == 'open'])
        st.metric("Abertas", abertas)
    
    st.markdown("---")
    
    # Contatos
    st.markdown("**📞 Contatos**")
    st.markdown("""
    <div class="contact-card">
        <div class="contact-item">📞 T.I. DPSP: (11) 5529-6003</div>
        <div class="contact-item" style="margin-top:8px">🎛️ Central: (11) 3274-7527</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Favoritos
    if st.session_state.favoritos:
        st.markdown("---")
        st.markdown("**⭐ Favoritos**")
        for fav in st.session_state.favoritos[:5]:
            st.markdown(f"- VD {fav}")

menu_name = menu.split(" ", 1)[1] if " " in menu else menu

# ===== CONSULTA DE LOJAS =====
if menu_name == "Consulta de Lojas":
    st.markdown("## 🏪 Consulta de Lojas")
    st.markdown("*Busque informações completas de qualquer loja do parque DPSP*")
    
    col_exp, col_busca = st.columns([1, 4])
    with col_exp:
        with st.expander("📥 Exportar"):
            if st.button("📄 Exportar CSV"):
                import csv
                import io
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=lojas[0].keys() if lojas else [])
                writer.writeheader()
                writer.writerows(lojas)
                st.download_button("⬇️ Download CSV", output.getvalue(), "lojas_dpsp.csv", "text/csv")
            if st.button("📊 Exportar JSON"):
                import json
                st.download_button("⬇️ Download JSON", json.dumps(lojas, indent=2), "lojas_dpsp.json", "application/json")
    
    # Search com Auto-complete
    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col1:
        modo_busca = st.selectbox("Modo", ["VD / Designação", "Endereço", "Nome de Loja", "Outra Informação"])
    with col2:
        termo_busca = st.text_input("", placeholder="🔍 Digite para buscar...", label_visibility="collapsed", key="busca_input")
        
        # Auto-complete
        if termo_busca and len(termo_busca) >= 2:
            sugestoes = get_suggestions(termo_busca, modo_busca)
            if sugestoes:
                st.markdown('<div class="suggestions-box">', unsafe_allow_html=True)
                for s in sugestoes:
                    if st.button(f"**VD {s['vd']}** - {s['nome']}\n\n📍 {s['endereco']}", key=f"sug_{s['vd']}"):
                        st.session_state.termo_selecionado = s['vd']
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Validação de VD
        if termo_busca and modo_busca == "VD / Designação" and termo_busca.isdigit():
            validacao = data_loader.validar_vd(termo_busca)
            if validacao["valido"]:
                st.success(f"✅ VD {termo_busca} válido - {validacao['loja']['nome']}")
            else:
                st.warning(f"⚠️ {validacao['mensagem']}")
            data_loader.usage_logger.log("busca_vd", st.session_state.get("nome_atendente", "anonymous"), {"vd": termo_busca, "valido": validacao["valido"]})
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
    
    # Loading
    if st.session_state.loading:
        st.markdown("""
        <div class="skeleton skeleton-card"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text-short"></div>
        """, unsafe_allow_html=True)
    elif termo_busca or st.session_state.get('termo_selecionado'):
        search_term = st.session_state.get('termo_selecionado') or termo_busca
        resultados = data_loader.buscar_loja(search_term, modo_busca, lojas)
        
        # Apply filters
        if filtro_estado:
            resultados = [l for l in resultados if l.get('estado') in filtro_estado]
        if filtro_status:
            status_map = {"Aberta": "open", "Fechada": "closed"}
            resultados = [l for l in resultados if status_map.get(l.get('status'), '') in [status_map.get(s, '') for s in filtro_status]]
        
        st.markdown(f"### 📋 {len(resultados)} resultado(s)")
        
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
                        <h4>Contato</h4>
                        <div class="info-row">📞 {loja['tel']}</div>
                        <div class="info-row">📱 <a href="https://wa.me/55{loja['cel'].replace('-','').replace('(','').replace(')','')}" target="_blank">{loja['cel']}</a></div>
                        <div class="info-row">✉️ {loja['email']}</div>
                    </div>
                    <div class="info-section">
                        <h4>Horário & Gestão</h4>
                        <div class="info-row">🕐 {loja['horario']}</div>
                        <div class="info-row">👤 GGL: {loja['ggl']}</div>
                        <div class="info-row">👤 GR: {loja['gr']}</div>
                    </div>
                    <div class="info-section">
                        <h4>Designações</h4>
                        <div>{mpls_pill} {inn_pill}</div>
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
                if st.button(f"{'⭐' if is_fav else '☆'}", key=f"fv_{loja['vd']}_{i}", use_container_width=True):
                    if is_fav:
                        st.session_state.favoritos.remove(loja['vd'])
                    else:
                        st.session_state.favoritos.append(loja['vd'])
                    st.rerun()
            with col_bt4:
                if st.button("📥 Exportar", key=f"ex_{loja['vd']}_{i}", use_container_width=True):
                    st.toast("Arquivo exportado!")
        
        # Panels
        if st.session_state.loja_selecionada:
            st.markdown("---")
            loja = st.session_state.loja_selecionada
            nome_atend = st.session_state.get('nome_atendente', 'Atendente')
            horaAtual = datetime.now().strftime("%H:%M")
            
            with st.expander(f"📋 Chamados - VD {loja['vd']}", expanded=True):
                st.markdown("### 📱 VIVO")
                vivo_texto = gerar_chamado_vivo(loja, nome_atend, horaAtual)
                st.code(vivo_texto)
                col_v1, col_v2 = st.columns(2)
                with col_v1:
                    if st.button("📋 Copiar Vivo"): st.toast("Copiado!")
                with col_v2:
                    st.markdown("[Portal Vivo](https://mve.vivo.com.br)")
                
                st.markdown("### 🔵 CLARO")
                claro_texto = gerar_chamado_claro(loja, horaAtual)
                st.code(claro_texto)
                if st.button("📋 Copiar Claro"): st.toast("Copiado!")
        
        if st.session_state.loja_email:
            st.markdown("---")
            loja = st.session_state.loja_email
            with st.expander(f"📧 E-mail - VD {loja['vd']}", expanded=True):
                email_texto = gerar_email_tecnico(loja, st.session_state.get('nome_atendente', 'Central'))
                st.code(email_texto)
                if st.button("📋 Copiar E-mail"): st.toast("Copiado!")

# ===== GESTÃO DE CRISES =====
elif menu_name == "Gestão de Crises":
    st.markdown("## ⚠️ Gestão de Crises")
    
    st.markdown("""
    <div style="background:rgba(248,113,113,0.1);border:1px solid rgba(248,113,113,0.3);border-radius:12px;padding:16px;margin-bottom:20px;">
        <h4 style="margin:0 0 8px 0;color:var(--red);">🚨 Alertas Ativos</h4>
        <p style="color:var(--text2);font-size:13px;margin:0;">Nenhum incidente ativo no momento</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab_ex, tab_gc, tab_iso = st.tabs(["🔴 Alertas Executivos", "🚨 Gestão de Crise", "⚡ Loja Isolada"])
    
    with tab_ex:
        col1, col2 = st.columns(2)
        with col1:
            escopo = st.selectbox("Escopo", ["Internet - MPLS", "Internet - INN", "Sistema POS", "Sistema ERP", "VPN", "Data Center", "Energia"])
            ident = st.selectbox("Identificação", ["Central identificou", "Acionada por terceiros", "Alerta automático"])
            inicio = st.time_input("Início")
            termino = st.time_input("Término")
        with col2:
            abrangencia = st.text_input("Abrangência", placeholder="Todo o parque SP...")
            equipes = st.text_input("Equipes", placeholder="NOC, Infra...")
        
        status = st.text_area("Status", height=80)
        
        col_chk1, col_chk2, col_chk3 = st.columns(3)
        gerar_ab = st.checkbox("🔴 Abertura", value=True)
        gerar_atu = st.checkbox("🟡 Atualização")
        gerar_norm = st.checkbox("🟢 Normalização")
        
        if st.button("🔄 Gerar", type="primary"):
            templates = gerar_alerta_executivo(escopo, ident, inicio, termino, abrangencia, equipes, status, gerar_ab, gerar_atu, gerar_norm)
            for t in templates:
                tipo_cls = "template-abertura" if t['tipo'] == 'abertura' else "template-atualizacao" if t['tipo'] == 'atualizacao' else "template-normalizacao"
                st.markdown(f"""
                <div class="template-box">
                    <div class="template-header">
                        <span>{t['label']}</span>
                        <span class="template-type {tipo_cls}">{t['tipo'].upper()}</span>
                    </div>
                    <div class="template-content">{t['texto']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📋 Copiar"): st.toast("Copiado!")
            
            if st.button("💾 Salvar"):
                try:
                    sheets_manager.salvar_template('AExec', templates)
                    st.success("✅ Salvo!")
                except:
                    st.success("✅ Salvo localmente!")
    
    with tab_gc:
        col1, col2 = st.columns(2)
        with col1:
            num_inc = st.text_input("Nº Incidente", placeholder="INC-0001")
            link_sala = st.text_input("Link Sala")
            unidades = st.text_input("Unidades")
            causa = st.text_input("Causa")
        with col2:
            resp_tec = st.text_input("Resp. Técnico")
            resp_cmd = st.text_input("Resp. Command")
            hora_inc = st.time_input("Hora Incidente")
            hora_acion = st.time_input("Hora Acionamento")
        
        atualizacao = st.text_area("Atualização", height=80)
        contador = st.number_input("Nº Atualizações", 1, 99, 1)
        
        if hora_inc:
            proximo = (datetime.combine(datetime.today(), hora_inc) + timedelta(minutes=30)).time()
            st.info(f"⏱️ Próximo: {proximo.strftime('%H:%M')}")
        
        gerar_gc_ab = st.checkbox("🔴 Abertura", value=True)
        gerar_gc_norm = st.checkbox("🟢 Normalização")
        
        if st.button("🔄 Gerar Crise", type="primary"):
            templates = gerar_gestao_crise(num_inc, link_sala, unidades, causa, resp_tec, resp_cmd, hora_inc, hora_acion, atualizacao, contador, gerar_gc_ab, gerar_gc_norm)
            for t in templates:
                st.markdown(f"""
                <div class="template-box">
                    <div class="template-content">{t['texto']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📋 Copiar"): st.toast("Copiado!")
    
    with tab_iso:
        col1, col2 = st.columns(2)
        with col1:
            vd_iso = st.text_input("VD", placeholder="2015")
            tipo_iso = st.selectbox("Tipo", ["Energia Elétrica", "Internet"])
            tipo = "energia" if "Energia" in tipo_iso else "internet"
        with col2:
            hora_in = st.time_input("Início")
            hora_ret = st.time_input("Retorno")
        
        if st.button("🔄 Gerar 4 Tipos", type="primary"):
            all_temps = []
            for t in ["energia", "internet"]:
                temps = gerar_loja_isolada(vd_iso, t, hora_in, hora_ret, lojas)
                all_temps.extend(temps)
            
            for t in all_temps:
                st.markdown(f"""
                <div class="template-box">
                    <div class="template-header"><span>{t['label']}</span></div>
                    <div class="template-content">{t['texto']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📋 Copiar"): st.toast("Copiado!")

# ===== HISTÓRICO =====
elif menu_name == "Histórico":
    st.markdown("## 📋 Histórico")
    
    try:
        historico = sheets_manager.get_historico()
        
        col1, col2, col3, col4 = st.columns(4)
        aexec = len([h for h in historico if 'AExec' in str(h)])
        gcrises = len([h for h in historico if 'GCrises' in str(h)])
        isoladas = len([h for h in historico if 'Isolada' in str(h)])
        
        st.metric("Alertas Executivos", aexec)
        st.metric("Gestão Crises", gcrises)
        st.metric("Lojas Isoladas", isoladas)
        st.metric("Total", len(historico))
        
        for reg in historico[:20]:
            icon = "🔴" if "AExec" in str(reg) else "🚨" if "GCrises" in str(reg) else "⚡"
            st.markdown(f"""
            <div class="template-box">
                <div class="template-header">
                    <span>{icon} {reg.get('tipo', 'N/A')}</span>
                    <span style="color:var(--text3)">{reg.get('data', '')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.info("Nenhum registro.")

# ===== CHAMADOS =====
elif menu_name == "Abertura de Chamados":
    st.markdown("## 📞 Abertura de Chamados")
    
    col1, col2 = st.columns(2)
    with col1:
        vd_ch = st.text_input("VD", placeholder="2015")
        desig_ch = st.text_input("Designação")
        nome_ch = st.text_input("Seu Nome")
    with col2:
        hora_ch = st.time_input("Hora Início")
        horario_ch = st.text_input("Horário Funcionamento")
        op = st.selectbox("Operadora", ["Vivo + Claro", "Apenas Vivo", "Apenas Claro"])
    
    if st.button("🔄 Gerar", type="primary"):
        if vd_ch and desig_ch:
            hora_str = hora_ch.strftime("%H:%M") if hora_ch else "--:--"
            
            # Buscar loja
            loja = None
            for l in lojas:
                if l.get('vd') == vd_ch:
                    loja = l
                    break
            
            if loja:
                vivo_txt = gerar_chamado_vivo(loja, nome_ch or "Atendente", hora_str)
                claro_txt = gerar_chamado_claro(loja, hora_str)
            else:
                vivo_txt = f"VD: {vd_ch} - Designação: {desig_ch}"
                claro_txt = f"VD: {vd_ch} - Designação: {desig_ch}"
            
            if op in ["Vivo + Claro", "Apenas Vivo"]:
                st.markdown("### 📱 VIVO")
                st.code(vivo_txt)
                if st.button("📋 Copiar Vivo"): st.toast("Copiado!")
            
            if op in ["Vivo + Claro", "Apenas Claro"]:
                st.markdown("### 🔵 CLARO")
                st.code(claro_txt)
                if st.button("📋 Copiar Claro"): st.toast("Copiado!")
        else:
            st.warning("Preencha VD e Designação!")

# ===== DASHBOARD =====
elif menu_name == "Dashboard":
    st.markdown("## 📈 Dashboard")
    st.markdown("*Visão geral das operações*")
    
    stats = data_loader.usage_logger.get_stats()
    
    kpi = st.session_state.kpi_data
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Buscas Hoje", stats.get("buscas", kpi['buscas_hoje']), "+12%", delta_color="normal")
    with col2:
        st.metric("Chamados Hoje", stats.get("chamados", kpi['chamados_hoje']), "+3%", delta_color="normal")
    with col3:
        st.metric("Crises Ativas", kpi['crises_ativas'], "-1", delta_color="normal")
    with col4:
        st.metric("MTTR Médio", kpi['mttr_medio'], "-5min", delta_color="normal")
    
    st.markdown("---")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.markdown("### 🏪 Lojas por Estado")
        estados = {}
        for l in lojas:
            e = l.get('estado', 'Outro')
            estados[e] = estados.get(e, 0) + 1
        
        for estado, count in sorted(estados.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(lojas)) * 100
            st.progress(pct/100, f"{estado}: {count} ({pct:.1f}%)")
    
    with col_d2:
        st.markdown("### 📊 Status das Lojas")
        abertas = len([l for l in lojas if l.get('status') == 'open'])
        fechadas = len([l for l in lojas if l.get('status') == 'closed'])
        st.metric("Abertas", abertas)
        st.metric("Fechadas", fechadas)
        pct_online = (abertas / len(lojas) * 100) if len(lojas) > 0 else 0
        st.progress(pct_online/100, f"Uptime: {pct_online:.1f}%")
    
    st.markdown("---")
    
    st.markdown("### 📈 Histórico de Uso (7 dias)")
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        st.metric("Total Buscas", stats.get("buscas", 0))
    with col_h2:
        st.metric("Total Chamados", stats.get("chamados", 0))
    with col_h3:
        st.metric("Usuários Únicos", stats.get("usuarios", 0))

# ===== AJUDA / FAQ =====
elif menu_name == "Ajuda":
    st.markdown("## ❓ Ajuda e FAQ")
    st.markdown("*Perguntas frequentes e instruções de uso*")
    
    with st.expander("🔍 Como buscar uma loja?", expanded=True):
        st.markdown("""
        1. Selecione o modo de busca (VD/Designação, Endereço, Nome ou Livre)
        2. Digite o termo de busca no campo de pesquisa
        3. O sistema irá mostrar sugestões automaticamente
        4. Clique na loja desejada para ver todos os detalhes
        """)
    
    with st.expander("📋 Como abrir um chamado?"):
        st.markdown("""
        1. Busque a loja pelo VD
        2. Clique no botão "Chamados" no card da loja
        3. Selecione a operadora (Vivo ou Claro)
        4. Copie o texto gerado e cole no portal da operadora
        """)
    
    with st.expander("⚠️ Como criar um alerta de crise?"):
        st.markdown("""
        1. Acesse "Gestão de Crises" no menu
        2. Escolha o tipo: Alertas Executivos, Gestão de Crise ou Loja Isolada
        3. Preencha os campos necessários
        4. Clique em "Gerar" para criar o template
        5. Copie ou salve o informativo
        """)
    
    with st.expander("⭐ Como usar favoritos?"):
        st.markdown("""
        1. Ao buscar uma loja, clique no botão de estrela (☆)
        2. A loja será adicionada aos favoritos na sidebar
        3. Você pode acessar rapidamente suas lojas favoritadas
        """)
    
    with st.expander("⌨️ Atalhos de teclado"):
        st.markdown("""
        - **Ctrl+K**: Abrir busca rápida
        - **1-4**: Navegar entre as abas do menu
        - **Esc**: Fechar modais
        """)
    
    st.markdown("---")
    st.markdown("**Contato de Suporte:**")
    st.markdown("- 📞 T.I. DPSP: (11) 5529-6003")
    st.markdown("- 📞 Central: (11) 3274-7527")
    st.markdown("- 📧 central.comando@dpsp.com.br")

# Rodapé
st.markdown("""
<div class="footer">
    <p><b>🛡️ Central de Comando DPSP v1.4</b></p>
    <p>Desenvolvido por Enzo Maranho - T.I. DPSP · Uso Interno</p>
</div>
""", unsafe_allow_html=True)
