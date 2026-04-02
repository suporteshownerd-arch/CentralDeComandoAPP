"""
Página de Gestão de Crises
Central de Comando DPSP v2.0
"""

import streamlit as st
from datetime import datetime, timedelta
from components import render_alert_banner


def render_page(sheets_manager, lojas):
    """Renderiza a página de Gestão de Crises"""
    st.markdown("## ⚠️ Gestão de Crises")
    
    # Alertas ativos
    st.markdown(render_alert_banner(
        "Alertas Ativos",
        "Nenhum incidente ativo no momento"
    ), unsafe_allow_html=True)
    
    tab_ex, tab_gc, tab_iso = st.tabs([
        "🔴 Alertas Executivos",
        "🚨 Gestão de Crise",
        "⚡ Loja Isolada"
    ])
    
    with tab_ex:
        render_alertas_executivos()
    
    with tab_gc:
        render_gestao_crise()
    
    with tab_iso:
        render_loja_isolada(lojas)


def render_alertas_executivos():
    """Renderiza formulário de Alertas Executivos"""
    from templates import gerar_alerta_executivo
    
    col1, col2 = st.columns(2)
    
    with col1:
        escopo = st.selectbox(
            "Escopo",
            ["Internet - MPLS", "Internet - INN", "Sistema POS", "Sistema ERP", "VPN", "Data Center", "Energia"]
        )
        ident = st.selectbox(
            "Identificação",
            ["Central identificou", "Acionada por terceiros", "Alerta automático"]
        )
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
        templates = gerar_alerta_executivo(
            escopo, ident, inicio, termino,
            abrangencia, equipes, status,
            gerar_ab, gerar_atu, gerar_norm
        )
        
        from components import render_template_box
        
        for t in templates:
            tipo_cls = f"template-{t['tipo']}"
            st.markdown(render_template_box(
                t['label'],
                t['tipo'],
                t['texto']
            ), unsafe_allow_html=True)
            
            if st.button(f"📋 Copiar {t['tipo']}", key=f"copy_{t['tipo']}"):
                st.toast("✅ Copiado!")
        
        if st.button("💾 Salvar"):
            try:
                from utils.sheets import GoogleSheetsManager
                sheets = GoogleSheetsManager()
                sheets.salvar_template('AExec', templates)
                st.success("✅ Salvo no Sheets!")
            except:
                st.success("✅ Salvo localmente!")


def render_gestao_crise():
    """Renderiza formulário de Gestão de Crise"""
    from templates import gerar_gestao_crise
    
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
        templates = gerar_gestao_crise(
            num_inc, link_sala, unidades, causa,
            resp_tec, resp_cmd, hora_inc, hora_acion,
            atualizacao, contador, gerar_gc_ab, gerar_gc_norm
        )
        
        from components import render_template_box
        
        for t in templates:
            st.markdown(render_template_box(
                t['label'],
                t['tipo'],
                t['texto']
            ), unsafe_allow_html=True)
            
            if st.button(f"📋 Copiar {t['tipo']}", key=f"copy_gc_{t['tipo']}"):
                st.toast("✅ Copiado!")


def render_loja_isolada(lojas):
    """Renderiza formulário de Loja Isolada"""
    from templates import gerar_loja_isolada
    
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
        
        from components import render_template_box
        
        for t in all_temps:
            st.markdown(render_template_box(
                t['label'],
                t.get('tipo', 'abertura'),
                t['texto']
            ), unsafe_allow_html=True)
            
            if st.button(f"📋 Copiar {t['label']}", key=f"copy_iso_{t['label']}"):
                st.toast("✅ Copiado!")