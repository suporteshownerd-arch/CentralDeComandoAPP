"""
Página de Consulta de Lojas
Central de Comando DPSP v2.2
Robusta com tratamento de erros
"""

import streamlit as st
import pandas as pd
import io
from typing import List, Dict


def render_page(data_loader, lojas: List[dict]):
    """Renderiza a página completa de Consulta de Lojas"""
    
    st.markdown("## 🏪 Consulta de Lojas")
    st.markdown("*Busque informações completas de qualquer loja do parque DPSP*")
    
    # Obter DataFrame com segurança
    try:
        df = data_loader.get_df()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        df = pd.DataFrame()
    
    # Estatísticas do parque
    try:
        if df is not None and not df.empty:
            col_est1, col_est2, col_est3 = st.columns(3)
            with col_est1:
                st.metric("Total Lojas", len(df))
            with col_est2:
                ativas = len(df[df['status'] == 'open']) if 'status' in df.columns else len(df)
                st.metric("Lojas Ativas", ativas)
            with col_est3:
                if 'estado' in df.columns:
                    st.metric("Estados", df['estado'].nunique())
        else:
            st.metric("Total Lojas", len(lojas) if lojas else 0)
    except Exception:
        st.metric("Total Lojas", len(lojas) if lojas else 0)
    
    st.markdown("---")
    
    # Renderizar busca
    termo_busca, modo_busca = render_busca_simples(data_loader, df)
    
    # Resultados
    try:
        if termo_busca or st.session_state.get('termo_selecionado'):
            search_term = st.session_state.get('termo_selecionado') or termo_busca
            
            # Usar lista de lojas (mais robusto)
            resultados = data_loader.buscar_loja(search_term, modo_busca) if hasattr(data_loader, 'buscar_loja') else []
            
            if not resultados and lojas:
                # Fallback para busca na lista
                termo_lower = search_term.lower()
                resultados = [l for l in lojas if termo_lower in str(l.get('vd', '')).lower() or termo_lower in str(l.get('nome', '')).lower()]
            
            st.markdown(f"### 📋 {len(resultados)} resultado(s)")
            
            # Exibir resultados
            if resultados:
                for i, loja in enumerate(resultados[:20]):
                    render_loja_card(loja, i)
        else:
            # Mostrar lojas iniciais
            if lojas:
                st.markdown("### 📋 Lojas do Parque")
                for i, loja in enumerate(lojas[:10]):
                    render_loja_card(loja, i)
    except Exception as e:
        st.error(f"Erro na busca: {e}")


def render_busca_simples(data_loader, df):
    """Renderiza busca simples"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        modo_busca = st.selectbox(
            "Modo",
            ["VD / Designação", "Nome de Loja", "Endereço"]
        )
    
    with col2:
        termo_busca = st.text_input(
            "",
            placeholder="🔍 Digite para buscar...",
            label_visibility="collapsed",
            key="busca_input"
        )
        
        # Validação de VD
        if termo_busca and modo_busca == "VD / Designação" and termo_busca.isdigit():
            try:
                validacao = data_loader.validar_vd(termo_busca)
                if validacao["valido"]:
                    st.success(f"✅ VD {termo_busca}")
                else:
                    st.warning(f"⚠️ VD não encontrado")
            except Exception:
                pass
    
    return termo_busca, modo_busca


def render_loja_card(loja: dict, index: int):
    """Renderiza card de loja"""
    from components import render_vd_badge, render_status_badge, render_desig_pill, render_info_section
    
    vd = loja.get('vd', 'N/A')
    nome = loja.get('nome', 'N/A')
    endereco = loja.get('endereco', 'N/A')
    cidade = loja.get('cidade', 'N/A')
    estado = loja.get('estado', 'N/A')
    status = loja.get('status', 'open')
    tel = loja.get('tel', 'N/A')
    cel = loja.get('cel', 'N/A')
    email = loja.get('email', 'N/A')
    ggl = loja.get('ggl', 'N/A')
    gr = loja.get('gr', 'N/A')
    mpls = loja.get('mpls', '')
    inn = loja.get('inn', '')
    
    mpls_pill = render_desig_pill("MPLS", mpls) if mpls else ""
    inn_pill = render_desig_pill("INN", inn) if inn else ""
    
    st.markdown(f"""
    <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
            <div>
                {render_vd_badge(vd)}
                <h3 style="margin:16px 0 6px 0;font-size:22px;">{nome}</h3>
                <p style="color:var(--text2);font-size:14px">📍 {endereco} · {cidade} - {estado}</p>
            </div>
            {render_status_badge(status)}
        </div>
        <div class="info-grid">
            {render_info_section('Contato', [
                {'icon': '📞', 'label': 'Telefone', 'value': tel},
                {'icon': '📱', 'label': 'WhatsApp', 'value': cel},
                {'icon': '✉️', 'label': 'Email', 'value': email}
            ])}
            {render_info_section('Horário & Gestão', [
                {'icon': '🕐', 'label': 'GGL', 'value': ggl},
                {'icon': '👤', 'label': 'GR', 'value': gr}
            ])}
            <div class="info-section">
                <h4>Designações</h4>
                <div>{mpls_pill} {inn_pill}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botões de ação
    col_bt1, col_bt2, col_bt3 = st.columns(3)
    with col_bt1:
        if st.button("📋 Chamados", key=f"ch_{vd}_{index}", use_container_width=True):
            st.session_state.loja_selecionada = loja
    with col_bt2:
        vd_str = str(vd)
        is_fav = vd_str in st.session_state.favoritos
        if st.button(f"{'⭐' if is_fav else '☆'}", key=f"fv_{vd_str}_{index}", use_container_width=True):
            if is_fav:
                st.session_state.favoritos.remove(vd_str)
            else:
                st.session_state.favoritos.append(vd_str)
            st.rerun()
    with col_bt3:
        if st.button("📧 E-mail", key=f"em_{vd}_{index}", use_container_width=True):
            st.session_state.loja_email = loja