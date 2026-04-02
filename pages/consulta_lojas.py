"""
Página de Consulta de Lojas
Central de Comando DPSP v2.1
Com Pandas e Data Editor
"""

import streamlit as st
import pandas as pd
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


def get_suggestions(termo: str, modo: str, df: pd.DataFrame) -> List[dict]:
    """Retorna sugestões baseadas no termo de busca usando pandas"""
    if not termo or len(termo) < 2 or df.empty:
        return []
    
    termo = termo.lower()
    
    if modo == "VD / Designação":
        mask = df['vd'].astype(str).str.lower().str.contains(termo, na=False)
    elif modo == "Endereço":
        addr_col = 'endereco' if 'endereco' in df.columns else 'ENDEREÇO'
        mask = df[addr_col].astype(str).str.lower().str.contains(termo, na=False) if addr_col in df.columns else pd.Series([False]*len(df))
    elif modo == "Nome de Loja":
        nome_col = 'nome' if 'nome' in df.columns else 'LOJAS'
        mask = df[nome_col].astype(str).str.lower().str.contains(termo, na=False) if nome_col in df.columns else pd.Series([False]*len(df))
    else:
        text_cols = df.select_dtypes(include=['object']).columns
        mask = df[text_cols].apply(lambda x: x.astype(str).str.lower().str.contains(termo, na=False)).any(axis=1)
    
    return df[mask].head(8).to_dict('records')


def render_search_box(
    data_loader,
    df: pd.DataFrame,
    validar_vd: bool = True
) -> tuple:
    """Renderiza box de busca com auto-complete e validação"""
    col1, col2, col3 = st.columns([1, 2.5, 1])
    
    with col1:
        modo_busca = st.selectbox(
            "Modo",
            ["VD / Designação", "Endereço", "Nome de Loja", "Outra Informação"]
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
            sugestoes = get_suggestions(termo_busca, modo_busca, df)
            if sugestoes:
                st.markdown(render_suggestions_box([
                    {"vd": s.get('vd', ''), "nome": s.get('nome', ''), "endereco": s.get('endereco', '')}
                    for s in sugestoes
                ]), unsafe_allow_html=True)
                for s in sugestoes:
                    if st.button(
                        f"**VD {s.get('vd', '')}** - {s.get('nome', '')}\n\n📍 {s.get('endereco', '')}",
                        key=f"sug_{s.get('vd', '')}"
                    ):
                        st.session_state.termo_selecionado = str(s.get('vd', ''))
                        st.rerun()
        
        # Validação de VD
        if termo_busca and modo_busca == "VD / Designação" and termo_busca.isdigit():
            if validar_vd:
                validacao = data_loader.validar_vd(termo_busca)
                if validacao["valido"]:
                    st.success(f"✅ VD {termo_busca} válido - {validacao['loja'].get('nome', 'N/A')}")
                else:
                    st.warning(f"⚠️ {validacao['mensagem']}")
            
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


def render_filters(df: pd.DataFrame) -> tuple:
    """Renderiza filtros de busca usando pandas"""
    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    
    estados = []
    if 'estado' in df.columns:
        estados = sorted(df['estado'].dropna().unique().tolist())
    
    with col1:
        filtro_estado = st.multiselect("Estado", estados if estados else ["SP", "RJ", "MG", "PR", "RS"])
    
    with col2:
        filtro_status = st.multiselect("Status", ["Aberta", "Fechada"])
    
    with col3:
        colunas_ordenar = ['nome', 'vd', 'cidade', 'estado']
        disponiveis = [c for c in colunas_ordenar if c in df.columns]
        ordenar_por = st.selectbox("Ordenar por", disponiveis if disponiveis else ['vd'])
    
    return filtro_estado, filtro_status, ordenar_por


def render_data_editor(resultados: List[Dict]):
    """Renderiza resultados como tabela interativa"""
    if not resultados:
        return
    
    df_result = pd.DataFrame(resultados)
    
    colunas_exibir = ['vd', 'nome', 'endereco', 'cidade', 'estado', 'status']
    colunas_disponiveis = [c for c in colunas_exibir if c in df_result.columns]
    
    if not colunas_disponiveis:
        colunas_disponiveis = list(df_result.columns[:6])
    
    df_exibir = df_result[colunas_disponiveis].copy()
    
    column_config = {}
    for col in df_exibir.columns:
        if col == 'vd':
            column_config[col] = st.column_config.TextColumn("VD", width="small", disabled=True)
        elif col == 'nome':
            column_config[col] = st.column_config.TextColumn("Loja", width="medium", disabled=True)
        elif col == 'status':
            column_config[col] = st.column_config.SelectboxColumn(
                "Status",
                options=["open", "closed"],
                width="small"
            )
        else:
            column_config[col] = st.column_config.TextColumn(col.title(), width="medium")
    
    st.data_editor(
        df_exibir,
        column_config=column_config,
        hide_index=True,
        use_container_width=True,
        num_rows="fixed"
    )


def render_loja_card_html(loja: dict, index: int) -> str:
    """Renderiza card de loja em HTML"""
    status_val = loja.get('status', 'open')
    status_text = 'Aberta' if status_val == 'open' else 'Fechada'
    
    mpls = loja.get('mpls', '')
    inn = loja.get('inn', '')
    
    mpls_pill = render_desig_pill("MPLS", mpls) if mpls else ""
    inn_pill = render_desig_pill("INN", inn) if inn else ""
    
    nome = loja.get('nome', 'N/A')
    endereco = loja.get('endereco', 'N/A')
    cidade = loja.get('cidade', 'N/A')
    estado = loja.get('estado', 'N/A')
    tel = loja.get('tel', 'N/A')
    cel = loja.get('cel', 'N/A')
    email = loja.get('email', 'N/A')
    ggl = loja.get('ggl', 'N/A')
    gr = loja.get('gr', 'N/A')
    horario = loja.get('horario', 'N/A')
    
    return f"""
    <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
            <div>
                {render_vd_badge(loja.get('vd', ''))}
                <h3 style="margin:16px 0 6px 0;font-size:22px;">{nome}</h3>
                <p style="color:var(--text2);font-size:14px">📍 {endereco} · {cidade} - {estado}</p>
            </div>
            {render_status_badge(status_val)}
        </div>
        <div class="info-grid">
            {render_info_section('Contato', [
                {'icon': '📞', 'label': 'Telefone', 'value': tel},
                {'icon': '📱', 'label': 'WhatsApp', 'value': cel, 'link': f"https://wa.me/55{str(cel).replace('-','').replace('(','').replace(')','')}" if cel else None},
                {'icon': '✉️', 'label': 'Email', 'value': email}
            ])}
            {render_info_section('Horário & Gestão', [
                {'icon': '🕐', 'label': 'Horário', 'value': horario},
                {'icon': '👤', 'label': 'GGL', 'value': ggl},
                {'icon': '👤', 'label': 'GR', 'value': gr}
            ])}
            <div class="info-section">
                <h4>Designações</h4>
                <div>{mpls_pill} {inn_pill}</div>
            </div>
        </div>
    </div>
    """


def render_loja_detail(loja: dict):
    """Renderiza detalhes completos de uma loja"""
    st.markdown("---")
    
    nome_atend = st.session_state.get('nome_atendente', 'Atendente')
    hora_atual = datetime.now().strftime("%H:%M")
    
    from templates import gerar_chamado_vivo, gerar_chamado_claro, gerar_email_tecnico
    
    with st.expander(f"📋 Chamados - VD {loja.get('vd', '')}", expanded=True):
        st.markdown("### 📱 VIVO")
        vivo_texto = gerar_chamado_vivo(loja, nome_atend, hora_atual)
        st.code(vivo_texto)
        
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("📋 Copiar Vivo", key=f"copy_vivo_{loja.get('vd', '')}"):
                st.toast("✅ Copiado!")
        with col_v2:
            st.markdown("[Portal Vivo](https://mve.vivo.com.br)")
        
        st.markdown("### 🔵 CLARO")
        claro_texto = gerar_chamado_claro(loja, hora_atual)
        st.code(claro_texto)
        if st.button("📋 Copiar Claro", key=f"copy_claro_{loja.get('vd', '')}"):
            st.toast("✅ Copiado!")
    
    if st.session_state.get('loja_email'):
        st.markdown("---")
        with st.expander(f"📧 E-mail - VD {loja.get('vd', '')}", expanded=True):
            email_texto = gerar_email_tecnico(loja, nome_atend)
            st.code(email_texto)
            if st.button("📋 Copiar E-mail", key=f"copy_email_{loja.get('vd', '')}"):
                st.toast("✅ Copiado!")


def render_page(data_loader, lojas: List[dict]):
    """Renderiza a página completa de Consulta de Lojas"""
    st.markdown("## 🏪 Consulta de Lojas")
    st.markdown("*Busque informações completas de qualquer loja do parque DPSP*")
    
    # Obter DataFrame
    df = data_loader.get_df()
    
    # Estatísticas do parque
    if not df.empty:
        col_est1, col_est2, col_est3 = st.columns(3)
        with col_est1:
            st.metric("Total Lojas", len(df))
        with col_est2:
            ativas = len(df[df['status'] == 'open']) if 'status' in df.columns else len(df)
            st.metric("Lojas Ativas", ativas)
        with col_est3:
            if 'estado' in df.columns:
                st.metric("Estados", df['estado'].nunique())
    
    st.markdown("---")
    
    # Export buttons
    col_exp, col_busca = st.columns([1, 4])
    with col_exp:
        with st.expander("📥 Exportar"):
            if st.button("📄 Exportar CSV"):
                import csv
                import io
                output = io.StringIO()
                df.to_csv(output, index=False)
                st.download_button(
                    "⬇️ Download CSV",
                    output.getvalue(),
                    "lojas_dpsp.csv",
                    "text/csv"
                )
            if st.button("📊 Exportar JSON"):
                st.download_button(
                    "⬇️ Download JSON",
                    df.to_json(orient="records", indent=2),
                    "lojas_dpsp.json",
                    "application/json"
                )
    
    # Search
    termo_busca, modo_busca, nome_atendente = render_search_box(data_loader, df)
    
    # Filters
    filtro_estado, filtro_status, ordenar_por = render_filters(df)
    
    # Loading
    if st.session_state.loading:
        st.markdown("""
        <div class="skeleton skeleton-card"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text-short"></div>
        """, unsafe_allow_html=True)
    elif termo_busca or st.session_state.get('termo_selecionado'):
        search_term = st.session_state.get('termo_selecionado') or termo_busca
        resultados = data_loader.buscar_loja(search_term, modo_busca)
        
        # Apply filters
        if filtro_estado:
            resultados = [l for l in resultados if l.get('estado') in filtro_estado]
        if filtro_status:
            status_map = {"Aberta": "open", "Fechada": "closed"}
            resultados = [
                l for l in resultados
                if l.get('status') in [status_map.get(s, '') for s in filtro_status]
            ]
        
        # Ordenar
        if resultados and ordenar_por:
            resultados = sorted(resultados, key=lambda x: x.get(ordenar_por, ''))
        
        st.markdown(f"### 📋 {len(resultados)} resultado(s)")
        
        # Toggle entre Cards e Tabela
        modo_exibicao = st.radio("Modo de visualização", ["Cards", "Tabela"], horizontal=True)
        
        if modo_exibicao == "Tabela":
            render_data_editor(resultados)
        else:
            for i, loja in enumerate(resultados):
                st.markdown(render_loja_card_html(loja, i), unsafe_allow_html=True)
                
                # Action buttons
                col_bt1, col_bt2, col_bt3, col_bt4 = st.columns(4)
                
                with col_bt1:
                    if st.button("📋 Chamados", key=f"ch_{loja.get('vd', '')}_{i}", use_container_width=True):
                        st.session_state.loja_selecionada = loja
                
                with col_bt2:
                    if st.button("📧 E-mail", key=f"em_{loja.get('vd', '')}_{i}", use_container_width=True):
                        st.session_state.loja_email = loja
                
                with col_bt3:
                    vd_val = str(loja.get('vd', ''))
                    is_fav = vd_val in st.session_state.favoritos
                    if st.button(
                        f"{'⭐' if is_fav else '☆'}",
                        key=f"fv_{vd_val}_{i}",
                        use_container_width=True
                    ):
                        if is_fav:
                            st.session_state.favoritos.remove(vd_val)
                        else:
                            st.session_state.favoritos.append(vd_val)
                        st.rerun()
                
                with col_bt4:
                    if st.button("📥 Exportar", key=f"ex_{vd_val}_{i}", use_container_width=True):
                        st.toast("Arquivo exportado!")
        
        # Panels
        if st.session_state.get('loja_selecionada'):
            render_loja_detail(st.session_state.loja_selecionada)
    else:
        # Mostrar todas as lojas se não há busca
        if not df.empty:
            st.markdown("### 📋 Todas as lojas")
            
            # Usar DataFrame para exibir
            cols_display = ['vd', 'nome', 'endereco', 'cidade', 'estado', 'status']
            cols_available = [c for c in cols_display if c in df.columns]
            
            if cols_available:
                st.dataframe(
                    df[cols_available].head(50),
                    use_container_width=True,
                    hide_index=True
                )