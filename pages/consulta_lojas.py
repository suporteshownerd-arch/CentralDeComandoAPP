"""
Página de Consulta de Lojas
Central de Comando DPSP v2.0
"""

import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime
from components import (
    render_vd_badge,
    render_status_badge,
    render_desig_pill,
    render_info_section,
    render_suggestions_box,
    success_toast,
    toast
)


def get_suggestions(termo: str, modo: str, lojas: List[dict]) -> List[dict]:
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
        elif modo == "Otra Informação":
            dados = str(loja).lower()
            if termo in dados:
                sugestoes.append(loja)
    
    return sugestoes[:8]


def render_search_box(
    data_loader,
    lojas: List[dict],
    validar_vd: bool = True
) -> tuple:
    """
    Renderiza box de busca com auto-complete e validação
    
    Returns:
        tupla (termo_busca, modo_busca, nome_atendente)
    """
    col1, col2, col3 = st.columns([1, 2.5, 1])
    
    with col1:
        modo_busca = st.selectbox(
            "Modo",
            ["VD / Designação", "Endereço", "Nome de Loja", "Otra Informação"]
        )
    
    with col2:
        termo_busca = st.text_input(
            "",
            placeholder="🔍 Digite para buscar...",
            label_visibility="collapsed",
            key="busca_input"
        )
        
        # Auto-complete
        if termo_busca and len(termo_busca) >= 2:
            sugestoes = get_suggestions(termo_busca, modo_busca, lojas)
            if sugestoes:
                st.markdown(render_suggestions_box([
                    {"vd": s['vd'], "nome": s['nome'], "endereco": s['endereco']}
                    for s in sugestoes
                ]), unsafe_allow_html=True)
                for s in sugestoes:
                    if st.button(
                        f"**VD {s['vd']}** - {s['nome']}\n\n📍 {s['endereco']}",
                        key=f"sug_{s['vd']}"
                    ):
                        st.session_state.termo_selecionado = s['vd']
                        st.rerun()
        
        # Validação de VD
        if termo_busca and modo_busca == "VD / Designação" and termo_busca.isdigit():
            if validar_vd:
                validacao = data_loader.validar_vd(termo_busca)
                if validacao["valido"]:
                    st.success(f"✅ VD {termo_busca} válido - {validacao['loja']['nome']}")
                else:
                    st.warning(f"⚠️ {validacao['mensagem']}")
            
            # Log de uso
            data_loader.usage_logger.log(
                "busca_vd",
                st.session_state.get("nome_atendente", "anonymous"),
                {"vd": termo_busca}
            )
    
    with col3:
        nome_atendente = st.text_input("👤 Atendente", placeholder="Seu nome")
        if nome_atendente:
            st.session_state.nome_atendente = nome_atendente
    
    return termo_busca, modo_busca, nome_atendente


def render_filters() -> tuple:
    """Renderiza filtros de busca"""
    col_f1, col_f2 = st.columns([1, 1])
    
    with col1:
        filtro_estado = st.multiselect(
            "Estado",
            ["SP", "RJ", "MG", "PR", "RS", "BA", "PE", "CE", "DF"]
        )
    
    with col2:
        filtro_status = st.multiselect(
            "Status",
            ["Aberta", "Fechada"]
        )
    
    return filtro_estado, filtro_status


def render_loja_detail(loja: dict, data_loader):
    """Renderiza detalhes completos de uma loja"""
    st.markdown("---")
    
    nome_atend = st.session_state.get('nome_atendente', 'Atendente')
    hora_atual = datetime.now().strftime("%H:%M")
    
    from templates import gerar_chamado_vivo, gerar_chamado_claro, gerar_email_tecnico
    
    with st.expander(f"📋 Chamados - VD {loja['vd']}", expanded=True):
        st.markdown("### 📱 VIVO")
        vivo_texto = gerar_chamado_vivo(loja, nome_atend, hora_atual)
        st.code(vivo_texto)
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("📋 Copiar Vivo", key=f"copy_vivo_{loja['vd']}"):
                st.toast("✅ Copiado!")
        with col_v2:
            st.markdown("[Portal Vivo](https://mve.vivo.com.br)")
        
        st.markdown("### 🔵 CLARO")
        claro_texto = gerar_chamado_claro(loja, hora_atual)
        st.code(claro_texto)
        if st.button("📋 Copiar Claro", key=f"copy_claro_{loja['vd']}"):
            st.toast("✅ Copiado!")
    
    if st.session_state.loja_email:
        st.markdown("---")
        with st.expander(f"📧 E-mail - VD {loja['vd']}", expanded=True):
            email_texto = gerar_email_tecnico(loja, nome_atend)
            st.code(email_texto)
            if st.button("📋 Copiar E-mail", key=f"copy_email_{loja['vd']}"):
                st.toast("✅ Copiado!")


def render_loja_card_html(loja: dict, index: int) -> str:
    """Renderiza card de loja em HTML"""
    status_text = 'Aberta' if loja['status'] == 'open' else 'Fechada'
    
    mpls_pill = render_desig_pill("MPLS", loja.get("mpls", "N/A")) if loja.get('mpls') else ""
    inn_pill = render_desig_pill("INN", loja.get("inn", "N/A")) if loja.get('inn') else ""
    
    return f"""
    <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
            <div>
                {render_vd_badge(loja['vd'])}
                <h3 style="margin:16px 0 6px 0;font-size:22px;">{loja['nome']}</h3>
                <p style="color:var(--text2);font-size:14px">📍 {loja['endereco']} · {loja['cidade']} - {loja['estado']}</p>
            </div>
            {render_status_badge(loja['status'])}
        </div>
        <div class="info-grid">
            {render_info_section('Contato', [
                {'icon': '📞', 'label': 'Telefone', 'value': loja.get('tel', 'N/A')},
                {'icon': '📱', 'label': 'WhatsApp', 'value': loja.get('cel', 'N/A'), 'link': f"https://wa.me/55{loja.get('cel', '').replace('-','').replace('(','').replace(')','')}"},
                {'icon': '✉️', 'label': 'Email', 'value': loja.get('email', 'N/A')}
            ])}
            {render_info_section('Horário & Gestão', [
                {'icon': '🕐', 'label': 'Horário', 'value': loja.get('horario', 'N/A')},
                {'icon': '👤', 'label': 'GGL', 'value': loja.get('ggl', 'N/A')},
                {'icon': '👤', 'label': 'GR', 'value': loja.get('gr', 'N/A')}
            ])}
            <div class="info-section">
                <h4>Designações</h4>
                <div>{mpls_pill} {inn_pill}</div>
            </div>
        </div>
    </div>
    """


def render_page(data_loader, lojas: List[dict]):
    """Renderiza a página completa de Consulta de Lojas"""
    st.markdown("## 🏪 Consulta de Lojas")
    st.markdown("*Busque informações completas de qualquer loja do parque DPSP*")
    
    # Export buttons
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
                st.download_button(
                    "⬇️ Download CSV",
                    output.getvalue(),
                    "lojas_dpsp.csv",
                    "text/csv"
                )
            if st.button("📊 Exportar JSON"):
                import json
                st.download_button(
                    "⬇️ Download JSON",
                    json.dumps(lojas, indent=2),
                    "lojas_dpsp.json",
                    "application/json"
                )
    
    # Search
    termo_busca, modo_busca, nome_atendente = render_search_box(data_loader, lojas)
    
    # Filters
    filtro_estado, filtro_status = render_filters()
    
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
            resultados = [
                l for l in resultados
                if l.get('status') in [status_map.get(s, '') for s in filtro_status]
            ]
        
        st.markdown(f"### 📋 {len(resultados)} resultado(s)")
        
        for i, loja in enumerate(resultados):
            st.markdown(render_loja_card_html(loja, i), unsafe_allow_html=True)
            
            # Action buttons
            col_bt1, col_bt2, col_bt3, col_bt4 = st.columns(4)
            
            with col_bt1:
                if st.button("📋 Chamados", key=f"ch_{loja['vd']}_{i}", use_container_width=True):
                    st.session_state.loja_selecionada = loja
            
            with col_bt2:
                if st.button("📧 E-mail", key=f"em_{loja['vd']}_{i}", use_container_width=True):
                    st.session_state.loja_email = loja
            
            with col_bt3:
                is_fav = loja['vd'] in st.session_state.favoritos
                if st.button(
                    f"{'⭐' if is_fav else '☆'}",
                    key=f"fv_{loja['vd']}_{i}",
                    use_container_width=True
                ):
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
            render_loja_detail(st.session_state.loja_selecionada, data_loader)