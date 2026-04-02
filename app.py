"""
Central de Comando DPSP - Aplicação Principal
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

# CSS Customizado Premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
    
    :root {
        --bg: #0a0b0f;
        --bg2: #111318;
        --bg3: #181b22;
        --surface: #1e2128;
        --surface2: #252930;
        --border: rgba(255,255,255,0.07);
        --border2: rgba(255,255,255,0.12);
        --text: #e8eaf0;
        --text2: #8b909e;
        --text3: #555b6a;
        --accent: #4f8ef7;
        --green: #2dd4a0;
        --red: #f05252;
        --amber: #f59e0b;
    }
    
    .stApp { background: var(--bg); }
    section[data-testid="stSidebar"] { background: var(--bg2) !important; border-right: 1px solid var(--border); }
    h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: var(--text) !important; font-weight: 700 !important; }
    h1 { font-size: 28px !important; }
    
    .card {
        background: var(--bg2);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.2s ease;
    }
    .card:hover { border-color: var(--border2); transform: translateY(-2px); box-shadow: 0 4px 24px rgba(0,0,0,0.3); }
    
    .vd-badge { background: rgba(79,142,247,0.15); color: var(--accent); padding: 4px 10px; border-radius: 6px; font-family: 'DM Mono', monospace; font-size: 12px; }
    .status-open { background: rgba(45,212,160,0.15); color: var(--green); padding: 4px 12px; border-radius: 20px; font-size: 12px; }
    .status-closed { background: rgba(240,82,82,0.15); color: var(--red); padding: 4px 12px; border-radius: 20px; font-size: 12px; }
    
    .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .info-section { background: var(--surface); border-radius: 8px; padding: 14px; }
    .info-section h4 { font-family: 'DM Mono', monospace; font-size: 11px; color: var(--text3); text-transform: uppercase; margin-bottom: 10px; }
    .info-row { font-size: 13px; color: var(--text2); margin-bottom: 6px; }
    
    .desig-pill { display: inline-flex; font-family: 'DM Mono', monospace; font-size: 11px; padding: 3px 9px; border-radius: 4px; margin: 2px 4px 2px 0; }
    .desig-mpls { background: rgba(45,212,160,0.12); color: var(--green); border: 1px solid rgba(45,212,160,0.25); }
    .desig-inn { background: rgba(79,142,247,0.12); color: var(--accent); border: 1px solid rgba(79,142,247,0.25); }
    
    .template-box { background: var(--bg3); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 16px; }
    .template-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
    .template-type { font-family: 'DM Mono', monospace; font-size: 11px; padding: 3px 10px; border-radius: 4px; }
    .template-abertura { background: rgba(240,82,82,0.15); color: var(--red); }
    .template-atualizacao { background: rgba(245,158,11,0.15); color: var(--amber); }
    .template-normalizacao { background: rgba(45,212,160,0.15); color: var(--green); }
    .template-content { background: var(--surface); border-radius: 8px; padding: 16px; font-family: 'DM Mono', monospace; font-size: 12px; line-height: 1.7; white-space: pre-wrap; }
    
    [data-testid="stMetric"] { background: var(--bg2); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }
    [data-testid="stMetricLabel"] { color: var(--text3); font-family: 'DM Mono', monospace; font-size: 11px; }
    [data-testid="stMetricValue"] { color: var(--text); font-family: 'Syne', sans-serif; font-weight: 700; }
    
    .sidebar-logo { display: flex; align-items: center; gap: 10px; padding: 16px; margin-bottom: 8px; }
    .sidebar-logo-icon { width: 32px; height: 32px; background: var(--accent); border-radius: 8px; display: flex; align-items: center; justify-content: center; }
    .sidebar-logo-text { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 14px; }
    .sidebar-logo-sub { font-family: 'DM Mono', monospace; font-size: 10px; color: var(--text3); }
    
    .contact-card { background: var(--surface); border-radius: 8px; padding: 12px; margin-bottom: 8px; }
    .contact-item { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text2); }
    
    .footer { text-align: center; color: var(--text3); font-size: 12px; padding: 20px; border-top: 1px solid var(--border); margin-top: 40px; }
    
    .action-buttons { display: flex; gap: 8px; margin-top: 16px; }
    .action-btn { flex: 1; }
    
    .tab-content { padding: 16px 0; }
    
    .history-nav { display: flex; gap: 8px; justify-content: center; margin-bottom: 16px; }
</style>
""", unsafe_allow_html=True)

# Session State
if 'loja_selecionada' not in st.session_state:
    st.session_state.loja_selecionada = None
if 'loja_email' not in st.session_state:
    st.session_state.loja_email = None
if 'historico_offset' not in st.session_state:
    st.session_state.historico_offset = 0

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
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">
            <svg width="18" height="18" viewBox="0 0 16 16" fill="none">
                <circle cx="8" cy="8" r="3" fill="white"/>
                <path d="M8 2V4M8 12V14M2 8H4M12 8H14" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </div>
        <div>
            <div class="sidebar-logo-text">Central de Comando</div>
            <div class="sidebar-logo-sub">DPSP v1.2</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div style="display:flex;align-items:center;gap:8px;"><div style="width:8px;height:8px;background:#2dd4a0;border-radius:50%;"></div><span style="font-size:12px;color:#2dd4a0;font-family:monospace;">Sistema operacional</span></div>', unsafe_allow_html=True)
    
    menu = st.radio("Navegação", ["🏪 Consulta de Lojas", "⚠️ Gestão de Crises", "📋 Histórico", "📞 Abertura de Chamados"])
    
    st.markdown("---")
    st.markdown("**Contatos Suporte**")
    st.markdown('<div class="contact-card"><div class="contact-item"><span>📞</span><span>T.I. DPSP: (11) 5529-6003</span></div><div class="contact-item" style="margin-top:8px"><span>🎛️</span><span>Central: (11) 3274-7527</span></div><div class="contact-item" style="margin-top:8px"><span>✉️</span><span>central.comando@dpsp.com.br</span></div></div>', unsafe_allow_html=True)

menu_name = menu.split(" ", 1)[1] if " " in menu else menu

# ===== CONSULTA DE LOJAS =====
if menu_name == "Consulta de Lojas":
    st.markdown("## 🏪 Consulta de Lojas")
    st.markdown("*Busque informações completas de qualquer loja do parque DPSP*")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        modo_busca = st.selectbox("Modo", ["VD / Designação", "Endereço", "Nome de Loja", "Outra Informação"])
    with col2:
        termo_busca = st.text_input("", placeholder="Digite VD, endereço, nome ou designação...", label_visibility="collapsed")
    with col3:
        nome_atendente = st.text_input("Atendente", placeholder="Seu nome")
    
    if 'nome_atendente' not in st.session_state:
        st.session_state.nome_atendente = ""
    if nome_atendente:
        st.session_state.nome_atendente = nome_atendente
    
    if termo_busca:
        resultados = data_loader.buscar_loja(termo_busca, modo_busca, lojas)
        st.markdown(f"**{len(resultados)} resultado(s) encontrado(s)**")
        
        for i, loja in enumerate(resultados):
            status_text = 'Aberta' if loja['status'] == 'open' else 'Fechada'
            mpls_pill = f'<span class="desig-pill desig-mpls">MPLS {loja.get("mpls", "N/A")}</span>' if loja.get('mpls') else ''
            inn_pill = f'<span class="desig-pill desig-inn">INN {loja.get("inn", "N/A")}</span>' if loja.get('inn') else ''
            
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                    <div>
                        <span class="vd-badge">VD {loja['vd']}</span>
                        <h3 style="margin:12px 0 4px 0">{loja['nome']}</h3>
                        <p style="color:var(--text2);font-size:13px">{loja['cidade']} - {loja['estado']}</p>
                    </div>
                    <span class="status-{loja['status']}">● {status_text}</span>
                </div>
                <div class="info-grid">
                    <div class="info-section">
                        <h4>📍 Contato & Localização</h4>
                        <div class="info-row">{loja['endereco']}</div>
                        <div class="info-row">{loja['tel']}</div>
                        <div class="info-row"><a href="https://wa.me/55{loja['cel'].replace('-','').replace('(','').replace(')','')}" style="color:var(--accent)">{loja['cel']}</a></div>
                        <div class="info-row">{loja['email']}</div>
                    </div>
                    <div class="info-section">
                        <h4>🕐 Horários & Gestão</h4>
                        <div class="info-row">{loja['horario']}</div>
                        <div class="info-row" style="margin-top:10px"><strong>GGL:</strong> {loja['ggl']} · {loja['ggl_tel']}</div>
                        <div class="info-row"><strong>GR:</strong> {loja['gr']} · {loja['gr_tel']}</div>
                    </div>
                    <div class="info-section">
                        <h4>🔗 Designações</h4>
                        <div style="margin-bottom:6px">{mpls_pill} {inn_pill}</div>
                        <div class="info-row" style="font-family:monospace;font-size:11px;color:var(--text3)">CNPJ: {loja['cnpj']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botões de Ação
            col_bt1, col_bt2, col_bt3 = st.columns(3)
            with col_bt1:
                if st.button("📋 Gerar Chamados", key=f"ch_{loja['vd']}_{i}"):
                    st.session_state.loja_selecionada = loja
            with col_bt2:
                if st.button("📧 E-mail Técnico", key=f"em_{loja['vd']}_{i}"):
                    st.session_state.loja_email = loja
            with col_bt3:
                if st.button("⭐ Favoritar", key=f"fv_{loja['vd']}_{i}"):
                    st.toast(f"Loja {loja['vd']} favoritada!")
        
        # Exibir Called/Email se selecionado
        if st.session_state.loja_selecionada:
            st.markdown("---")
            st.markdown("### 📋 Chamados - VD " + st.session_state.loja_selecionada['vd'])
            loja = st.session_state.loja_selecionada
            nome_atend = st.session_state.get('nome_atendente', 'Atendente Central')
            horaAtual = datetime.now().strftime("%H:%M")
            
            # Vivo
            st.markdown("#### 📱 VIVO")
            vivo_texto = gerar_chamado_vivo(loja, nome_atend, horaAtual)
            st.code(vivo_texto)
            col_v, col_v_link = st.columns([1, 1])
            with col_v:
                if st.button("📋 Copiar Vivo", key="copy_vivo"):
                    st.toast("Copiado!")
            with col_v_link:
                st.markdown("[Abrir Portal Vivo](https://mve.vivo.com.br)")
            
            # Claro
            st.markdown("#### 🔵 CLARO")
            claro_texto = gerar_chamado_claro(loja, horaAtual)
            st.code(claro_texto)
            col_c, col_c_link = st.columns([1, 1])
            with col_c:
                if st.button("📋 Copiar Claro", key="copy_claro"):
                    st.toast("Copiado!")
            with col_c_link:
                st.markdown("[Abrir Portal Claro](https://webebt01.embratel.com.br)")
            
            if st.button("❌ Fechar", key="close_chamados"):
                st.session_state.loja_selecionada = None
                st.rerun()
        
        if st.session_state.loja_email:
            st.markdown("---")
            st.markdown("### 📧 E-mail Técnico - VD " + st.session_state.loja_email['vd'])
            loja = st.session_state.loja_email
            nome_atend = st.session_state.get('nome_atendente', 'Central de Comando')
            
            email_texto = gerar_email_tecnico(loja, nome_atend)
            st.code(email_texto)
            
            col_e, col_m = st.columns([1, 1])
            with col_e:
                if st.button("📋 Copiar E-mail", key="copy_email"):
                    st.toast("Copiado!")
            with col_m:
                mailto = f"mailto:{loja['email']}?subject=[DPSP] Técnico em campo - VD {loja['vd']}&body={email_texto}"
                st.markdown(f"[📧 Abrir Cliente de E-mail]({mailto})")
            
            if st.button("❌ Fechar E-mail", key="close_email"):
                st.session_state.loja_email = None
                st.rerun()

# ===== GESTÃO DE CRISES =====
elif menu_name == "Gestão de Crises":
    st.markdown("## ⚠️ Gestão de Crises")
    st.markdown("*Geração de comunicados padronizados para incidentes*")
    
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
        
        status = st.text_area("Status / Ação Atual", placeholder="Descreva a ação em andamento...", height=80)
        
        st.markdown("**Templates:**")
        col_chk1, col_chk2, col_chk3 = st.columns(3)
        with col_chk1:
            gerar_abertura = st.checkbox("🔴 Abertura", value=True)
        with col_chk2:
            gerar_atualizacao = st.checkbox("🟡 Atualização")
        with col_chk3:
            gerar_normalizacao = st.checkbox("🟢 Normalização")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("🔄 Gerar Templates", type="primary", use_container_width=True):
                templates = gerar_alerta_executivo(escopo, identificacao, inicio, termino, abrangencia, equipes, status, gerar_abertura, gerar_atualizacao, gerar_normalizacao)
                for t in templates:
                    tipo_classe = "template-abertura" if t['tipo'] == 'abertura' else "template-atualizacao" if t['tipo'] == 'atualizacao' else "template-normalizacao"
                    st.markdown(f"""
                    <div class="template-box">
                        <div class="template-header">
                            <span style="font-weight:600">{t['label']}</span>
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
                    sheets_manager.salvar_template('AExec', templates)
                    st.success("✅ Salvo com sucesso!")
                except Exception as e:
                    st.success("✅ Salvo localmente!")
    
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
        
        atualizacao = st.text_area("Atualização de Status", height=80)
        contador = st.number_input("Nº de Atualizações", min_value=1, value=1)
        
        # Próximo Status automático
        if hora_incidente:
            proximo = (datetime.combine(datetime.today(), hora_incidente) + timedelta(minutes=30)).time()
            st.info(f"⏱️ Próximo Status automático: {proximo.strftime('%H:%M')} (+30min)")
        
        col_chk_gc1, col_chk_gc2 = st.columns(2)
        with col_chk_gc1:
            gerar_gc_abertura = st.checkbox("🔴 Template Abertura", value=True)
        with col_chk_gc2:
            gerar_gc_normalizacao = st.checkbox("🟢 Template Normalização")
        
        if st.button("🔄 Gerar Templates de Crise", type="primary"):
            templates = gerar_gestao_crise(num_incidente, link_sala, unidades, causa, responsavel_tecnico, responsavel_command, hora_incidente, hora_acionamento, atualizacao, contador, gerar_gc_abertura, gerar_gc_normalizacao)
            for t in templates:
                st.markdown(f"""
                <div class="template-box">
                    <div class="template-header">
                        <span style="font-weight:600">{t['label']}</span>
                    </div>
                    <div class="template-content">{t['texto']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📋 Copiar {t['tipo']}", key=f"copy_gc_{t['tipo']}"):
                    st.toast("Copiado!")
            
            if st.button("💾 Salvar Gestão de Crise"):
                try:
                    sheets_manager.salvar_template('GCrises', templates)
                    st.success("✅ Salvo com sucesso!")
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
        
        if st.button("🔄 Gerar Informativos", type="primary"):
            templates = gerar_loja_isolada(vd_isolada, tipo_isol, hora_inicio_iso, hora_retorno_iso, lojas)
            for t in templates:
                st.markdown(f"""
                <div class="template-box">
                    <div class="template-header">
                        <span style="font-weight:600">{t['label']}</span>
                    </div>
                    <div class="template-content">{t['texto']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📋 Copiar", key=f"copy_iso_{t['tipo']}"):
                    st.toast("Copiado!")
            
            if st.button("💾 Salvar Loja Isolada"):
                try:
                    sheets_manager.salvar_template('Isolada', templates)
                    st.success("✅ Salvo com sucesso!")
                except:
                    st.success("✅ Salvo localmente!")

# ===== HISTÓRICO =====
elif menu_name == "Histórico":
    st.markdown("## 📋 Histórico")
    st.markdown("*Registros salvos no histórico*")
    
    # Navegação
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
            st.metric("Alertas Executivos", aexec)
        with col2:
            st.metric("Gestão de Crises", gcrises)
        with col3:
            st.metric("Lojas Isoladas", isoladas)
        with col4:
            st.metric("Total", len(historico))
        
        st.markdown(f"*Mostrando registros {st.session_state.historico_offset + 1} a {min(st.session_state.historico_offset + 20, len(historico))} de {len(historico)}*")
        
        if historico_paginado:
            for reg in historico_paginado:
                reg_tipo = reg.get('tipo', 'N/A')
                reg_data = reg.get('data', '')
                reg_label = reg.get('label', '')
                st.markdown(f"""
                <div class="template-box">
                    <div class="template-header">
                        <span style="font-weight:600">{reg_tipo} - {reg_label}</span>
                        <span style="color:var(--text3);font-size:12px">{reg_data}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum registro encontrado.")
    except Exception as e:
        st.info("Nenhum registro no histórico ainda.")

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
    
    if st.button("🔄 Gerar Textos de Chamado", type="primary"):
        if vd_chamado and desig_chamado:
            hora_ch = hora_inicio_ch.strftime("%H:%M") if hora_inicio_ch else "--:--"
            
            # Buscar loja para dados completos
            loja_encontrada = None
            for l in lojas:
                if l.get('vd') == vd_chamado:
                    loja_encontrada = l
                    break
            
            if loja_encontrada:
                vivo_text = gerar_chamado_vivo(loja_encontrada, nome_atendente_ch or "Atendente", hora_ch)
                claro_text = gerar_chamado_claro(loja_encontrada, hora_ch)
            else:
                vivo_text = f"""Portal Vivo MVE - Campos para preenchimento:
Nome: {nome_atendente_ch}
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br
Designação: {desig_chamado}
VD: {vd_chamado}
Horário de início: {hora_ch}
Horário de funcionamento: {horario_func or 'Consultar'}
Acesse: https://mve.vivo.com.br"""
                
                claro_text = f"""Portal Claro Empresas:
Designação: {desig_chamado}
VD: {vd_chamado}
Acesse: https://webebt01.embratel.com.br"""
            
            if operadora in ["Vivo + Claro", "Apenas Vivo"]:
                st.markdown("### 📱 VIVO")
                st.code(vivo_text)
                if st.button("📋 Copiar Vivo", key="ch_vivo"):
                    st.toast("Copiado!")
                st.markdown("[Abrir Portal Vivo](https://mve.vivo.com.br)")
            
            if operadora in ["Vivo + Claro", "Apenas Claro"]:
                st.markdown("### 🔵 CLARO")
                st.code(claro_text)
                if st.button("📋 Copiar Claro", key="ch_claro"):
                    st.toast("Copiado!")
                st.markdown("[Abrir Portal Claro](https://webebt01.embratel.com.br)")
        else:
            st.warning("Preencha VD e Designação!")

# Rodapé
st.markdown("""
<div class="footer">
    <p>🛡️ Central de Comando DPSP v1.2</p>
    <p>Desenvolvido por Enzo Maranho - T.I. DPSP · Uso Interno</p>
</div>
""", unsafe_allow_html=True)
