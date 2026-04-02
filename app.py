"""
Central de Comando DPSP - Aplicação Principal
Desenvolvido por Enzo Maranho - T.I. DPSP
"""

import streamlit as st
from data.loader import DataLoader
from templates import gerar_alerta_executivo, gerar_gestao_crise, gerar_loja_isolada
from utils.sheets import GoogleSheetsManager

# Configuração da página
st.set_page_config(
    page_title="Central de Comando - DPSP",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado
st.markdown("""
<style>
    /* Tema Escuro */
    .stApp {
        background: #0a0b0f;
    }
    .stSidebar {
        background: #111318 !important;
    }
    h1, h2, h3 {
        font-family: 'Syne', sans-serif;
        color: #e8eaf0;
    }
    .metric-card {
        background: #1e2128;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.07);
    }
    .store-card {
        background: #111318;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .template-box {
        background: #181b22;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 8px;
        padding: 16px;
        font-family: 'DM Mono', monospace;
        font-size: 13px;
    }
    .btn-primary {
        background: #4f8ef7;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
    }
    .btn-primary:hover {
        background: #3d7ef6;
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-family: 'DM Mono', monospace;
    }
    .status-open {
        background: rgba(45,212,160,0.15);
        color: #2dd4a0;
    }
    .status-closed {
        background: rgba(240,82,82,0.15);
        color: #f05252;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização
@st.cache_resource
def get_data_loader():
    return DataLoader()

@st.cache_resource
def get_sheets_manager():
    return GoogleSheetsManager()

data_loader = get_data_loader()
sheets_manager = get_sheets_manager()

# Carregar dados
lojas = data_loader.get_lojas()

# Sidebar
st.sidebar.title("🛡️ Central de Comando")
st.sidebar.markdown("**DPSP / T.I.**")

menu = st.sidebar.radio(
    "Navegação",
    ["Consulta de Lojas", "Gestão de Crises", "Histórico", "Abertura de Chamados"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Contatos Suporte**")
st.sidebar.markdown("""
- T.I. DPSP: (11) 5529-6003
- Central: (11) 3274-7527
- Email: central.comando@dpsp.com.br
""")

# ===== CONSULTA DE LOJAS =====
if menu == "Consulta de Lojas":
    st.title("🏪 Consulta de Lojas")
    st.markdown("Busque informações completas de qualquer loja do parque DPSP")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        modo_busca = st.selectbox(
            "Modo de Busca",
            ["VD / Designação", "Endereço", "Nome de Loja", "Outra Informação"]
        )
    with col2:
        termo_busca = st.text_input("Digite sua busca...", placeholder="Ex: 2015, Paulista, Drogasil...")
    with col3:
        nome_atendente = st.text_input("Seu nome", placeholder="Atendente")
    
    if termo_busca:
        resultados = data_loader.buscar_loja(termo_busca, modo_busca, lojas)
        
        st.markdown(f"**{len(resultados)} resultado(s) encontrado(s)**")
        
        for loja in resultados:
            with st.container():
                st.markdown(f"""
                <div class="store-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="background:rgba(79,142,247,0.15);color:#4f8ef7;padding:3px 8px;border-radius:4px;font-family:'DM Mono',monospace;font-size:11px;">VD {loja['vd']}</span>
                            <h3 style="margin:8px 0 4px 0;">{loja['nome']}</h3>
                            <p style="color:#8b909e;font-size:13px;">{loja['cidade']} - {loja['estado']}</p>
                        </div>
                        <span class="status-badge {'status-open' if loja['status'] == 'open' else 'status-closed'}">
                            {'● Aberta' if loja['status'] == 'open' else '● Fechada'}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.markdown("**Contato & Localização**")
                    st.write(f"📍 {loja['endereco']}")
                    st.write(f"📞 {loja['tel']}")
                    st.write(f"[WhatsApp](https://wa.me/55{loja['cel'].replace('-','').replace('(','').replace(')','')}): {loja['cel']}")
                    st.write(f"✉️ {loja['email']}")
                with col_b:
                    st.markdown("**Horário & Gestão**")
                    st.write(f"🕐 {loja['horario']}")
                    st.markdown(f"**GGL:** {loja['ggl']} - {loja['ggl_tel']}")
                    st.markdown(f"**GR:** {loja['gr']} - {loja['gr_tel']}")
                with col_c:
                    st.markdown("**Designações**")
                    if loja.get('mpls'):
                        st.code(f"MPLS: {loja['mpls']}")
                    if loja.get('inn'):
                        st.code(f"INN: {loja['inn']}")
                    st.code(f"CNPJ: {loja['cnpj']}")
                
                col_bt1, col_bt2, col_bt3 = st.columns([1, 1, 1])
                with col_bt1:
                    if st.button(f"📋 Gerar Chamados - VD {loja['vd']}", key=f"chamados_{loja['vd']}"):
                        st.session_state['loja_selecionada'] = loja
                        st.rerun()
                with col_bt2:
                    if st.button(f"📧 E-mail Técnico - VD {loja['vd']}", key=f"email_{loja['vd']}"):
                        st.session_state['loja_email'] = loja
                        st.rerun()
                with col_bt3:
                    if st.button(f"⭐ Favoritar - VD {loja['vd']}", key=f"fav_{loja['vd']}"):
                        st.toast(f"Loja {loja['vd']} favoritada!")
                
                st.markdown("---")

# ===== GESTÃO DE CRISES =====
elif menu == "Gestão de Crises":
    st.title("⚠️ Gestão de Crises")
    st.markdown("Geração de comunicados padronizados para incidentes")
    
    tab_executivo, tab_gestao, tab_isolada = st.tabs(["Alertas Executivos", "Gestão de Crise", "Loja Isolada"])
    
    # Alertas Executivos
    with tab_executivo:
        col1, col2 = st.columns(2)
        with col1:
            escopo = st.selectbox("Escopo da Crise", [
                "Internet - MPLS", "Internet - INN", "Sistema POS", 
                "Sistema ERP", "VPN Corporativa", "Data Center", "Energia Elétrica", "Custom..."
            ])
            if escopo == "Custom...":
                escopo = st.text_input("Escopo personalizado")
            identificacao = st.selectbox("Identificação", [
                "Central identificou o incidente", 
                "Central foi acionada por terceiros",
                "Alerta automático do sistema"
            ])
            inicio = st.time_input("Horário de Início")
            termino = st.time_input("Horário de Término (opcional)")
        with col2:
            abrangencia = st.text_input("Abrangência", placeholder="Todo o parque SP, Região Sul...")
            equipes = st.text_input("Equipes Acionadas", placeholder="NOC, Infraestrutura, Vivo...")
            status = st.text_area("Status / Ação Atual", placeholder="Descreva a ação em andamento...")
        
        st.markdown("**Templates a Gerar:**")
        col_chk1, col_chk2, col_chk3 = st.columns(3)
        with col_chk1:
            gerar_abertura = st.checkbox("Abertura", value=True)
        with col_chk2:
            gerar_atualizacao = st.checkbox("Atualização")
        with col_chk3:
            gerar_normalizacao = st.checkbox("Normalização")
        
        if st.button("🔄 Gerar Templates", type="primary"):
            templates = gerar_alerta_executivo(escopo, identificacao, inicio, termino, abrangencia, equipes, status, gerar_abertura, gerar_atualizacao, gerar_normalizacao)
            for t in templates:
                st.markdown(f"**{t['label']}**")
                st.code(t['texto'])
                if st.button(f"📋 Copiar {t['label']}", key=f"copy_{t['tipo']}"):
                    st.toast("Copiado para área de transferência!")
            
            if st.button("💾 Salvar no Histórico"):
                sheets_manager.salvar_template('AExec', templates)
                st.success("Template salvo no Google Sheets!")
    
    # Gestão de Crise
    with tab_gestao:
        col1, col2 = st.columns(2)
        with col1:
            num_incidente = st.text_input("Nº do Incidente", placeholder="INC-0001")
            link_sala = st.text_input("Link da Sala de Crise", placeholder="https://meet.google.com/...")
            unidades = st.text_input("Unidades Impactadas", placeholder="45 lojas SP, 12 lojas RJ")
            causa = st.text_input("Causa", placeholder="Em investigação / causa identificada")
        with col2:
            responsavel_tecnico = st.text_input("Responsável Técnico")
            responsavel_command = st.text_input("Responsável Command")
            hora_incidente = st.time_input("Horário do Incidente")
            hora_acionamento = st.time_input("Horário de Acionamento")
        
        atualizacao = st.text_area("Atualização de Status")
        contador = st.number_input("Nº de Atualizações", min_value=1, value=1)
        
        col_chk_gc1, col_chk_gc2 = st.columns(2)
        with col_chk_gc1:
            gerar_gc_abertura = st.checkbox("Template Abertura 🔴", value=True)
        with col_chk_gc2:
            gerar_gc_normalizacao = st.checkbox("Template Normalização 🟢")
        
        if st.button("🔄 Gerar Templates de Crise", type="primary"):
            templates = gerar_gestao_crise(num_incidente, link_sala, unidades, causa, responsavel_tecnico, responsavel_command, hora_incidente, hora_acionamento, atualizacao, contador, gerar_gc_abertura, gerar_gc_normalizacao)
            for t in templates:
                st.markdown(f"**{t['label']}**")
                st.code(t['texto'])
            
            if st.button("💾 Salvar Gestão de Crise"):
                sheets_manager.salvar_template('GCrises', templates)
                st.success("Template salvo no Google Sheets!")
    
    # Loja Isolada
    with tab_isolada:
        col1, col2 = st.columns(2)
        with col1:
            vd_isolada = st.text_input("VD da Loja", placeholder="Ex: 2015")
            tipo_isolamento = st.selectbox("Tipo de Isolamento", ["Energia Elétrica", "Internet / Conectividade"])
            tipo_isol = "energia" if "Energia" in tipo_isolamento else "internet"
        with col2:
            hora_inicio_iso = st.time_input("Horário de Início")
            hora_retorno_iso = st.time_input("Previsão de Retorno (opcional)")
        
        if st.button("🔄 Gerar Informativos", type="primary"):
            templates = gerar_loja_isolada(vd_isolada, tipo_isol, hora_inicio_iso, hora_retorno_iso, lojas)
            for t in templates:
                st.markdown(f"**{t['label']}**")
                st.code(t['texto'])
            
            if st.button("💾 Salvar Loja Isolada"):
                sheets_manager.salvar_template('Isolada', templates)
                st.success("Template salvo no Google Sheets!")

# ===== HISTÓRICO =====
elif menu == "Histórico":
    st.title("📋 Histórico")
    st.markdown("Registros salvos no Google Sheets")
    
    try:
        historico = sheets_manager.get_historico()
        
        if historico:
            st.markdown(f"**Total de registros: {len(historico)}**")
            
            for reg in historico:
                st.markdown(f"""
                <div class="template-box" style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <strong>{reg.get('tipo', 'N/A')} - {reg.get('titulo', '')}</strong>
                        <span style="color:#8b909e;font-size:12px;">{reg.get('data', '')}</span>
                    </div>
                    <p style="color:#8b909e;font-size:13px;">{reg.get('detalhes', '')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum registro no histórico.")
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")

# ===== ABERTURA DE CHAMADOS =====
elif menu == "Abertura de Chamados":
    st.title("📞 Abertura de Chamados")
    st.markdown("Geração de textos para abertura de chamado junto às operadoras")
    
    col1, col2 = st.columns(2)
    with col1:
        vd_chamado = st.text_input("VD da Loja", placeholder="Ex: 2015")
        desig_chamado = st.text_input("Designação", placeholder="Ex: rsp_mpls_2015")
        nome_atendente_ch = st.text_input("Seu Nome", placeholder="Nome do atendente")
    with col2:
        hora_inicio_ch = st.time_input("Horário de Início")
        horario_func = st.text_input("Horário de Funcionamento", placeholder="Seg-Sáb 9h-22h / Dom 10h-20h")
        operadora = st.selectbox("Operadora", ["Vivo + Claro", "Apenas Vivo", "Apenas Claro"])
    
    if st.button("🔄 Gerar Textos de Chamado", type="primary"):
        if vd_chamado and desig_chamado:
            vivo_text = f"""Portal Vivo MVE - Campos para preenchimento:
Nome: {nome_atendente_ch}
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br
Designação: {desig_chamado}
VD: {vd_chamado}
Horário de início: {hora_inicio_ch}
Horário de funcionamento: {horario_func}
Acesse: https://mve.vivo.com.br"""
            
            claro_text = f"""Portal Claro Empresas - Texto para abertura:
Designação: {desig_chamado}
Unidade: VD {vd_chamado}
Horário do incidente: {hora_inicio_ch}
Acesse: https://webebt01.embratel.com.br/claroempresasonline/index"""
            
            if operadora in ["Vivo + Claro", "Apenas Vivo"]:
                st.markdown("**📱 VIVO**")
                st.code(vivo_text)
                if st.button("📋 Copiar Texto Vivo"):
                    st.toast("Copiado!")
            
            if operadora in ["Vivo + Claro", "Apenas Claro"]:
                st.markdown("**🔵 CLARO**")
                st.code(claro_text)
                if st.button("📋 Copiar Texto Claro"):
                    st.toast("Copiado!")
        else:
            st.warning("Preencha VD e Designação!")

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#8b909e;font-size:12px;">
    <p>Central de Comando DPSP - v1.1</p>
    <p>Desenvolvido por Enzo Maranho - T.I. DPSP</p>
    <p>Uso Interno</p>
</div>
""", unsafe_allow_html=True)
