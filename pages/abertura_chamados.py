"""
Página de Abertura de Chamados
Central de Comando DPSP v3.0
"""

import streamlit as st
from datetime import datetime
from templates import gerar_chamado_vivo, gerar_chamado_claro


def render_page(lojas):
    st.markdown("## 📞 Abertura de Chamados")
    st.markdown("*Gere o texto para abertura de chamado nas operadoras Vivo e Claro*")

    # ── Busca da loja ─────────────────────────────────────────────────────────
    st.markdown("### 1. Identificar a Loja")
    col_vd, col_info = st.columns([1, 3])

    # Permite pré-selecionar loja vinda da página de Consulta
    loja_pre = st.session_state.get("loja_selecionada")
    vd_default = loja_pre.get("vd", "") if loja_pre else ""

    with col_vd:
        vd = st.text_input(
            "VD da loja",
            value=vd_default,
            placeholder="Ex: 2015",
            key="ch_vd",
        )

    # Lookup automático ao digitar VD
    loja_encontrada = None
    if vd and vd.strip().isdigit():
        loja_encontrada = next((l for l in lojas if l.get("vd") == vd.strip()), None)

    with col_info:
        if loja_encontrada:
            st.success(f"✅ **{loja_encontrada['nome']}** — {loja_encontrada.get('cidade', '')}/{loja_encontrada.get('estado', '')}")
        elif vd:
            st.warning("⚠️ VD não encontrado. Preencha os campos manualmente.")

    st.markdown("---")

    # ── Dados do atendente ────────────────────────────────────────────────────
    st.markdown("### 2. Dados do Atendimento")
    col1, col2, col3 = st.columns(3)
    with col1:
        nome_atendente = st.text_input(
            "Seu nome",
            value=st.session_state.get("nome_atendente", ""),
            placeholder="Ex: João da Silva",
            key="ch_nome",
        )
        if nome_atendente:
            st.session_state.nome_atendente = nome_atendente
    with col2:
        hora_inicio = st.time_input("Hora do incidente", value=datetime.now().time(), key="ch_hora")
    with col3:
        operadora = st.selectbox("Operadora", ["Vivo + Claro", "Apenas Vivo", "Apenas Claro"], key="ch_op")

    # ── Preview dos dados da loja ─────────────────────────────────────────────
    if loja_encontrada:
        with st.expander("📋 Dados da loja que serão usados"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.caption(f"**Designação MPLS:** {loja_encontrada.get('mpls') or 'N/A'}")
                st.caption(f"**Designação INN:** {loja_encontrada.get('inn') or 'N/A'}")
            with c2:
                st.caption(f"**Endereço:** {loja_encontrada.get('endereco', '')}")
                st.caption(f"**Cidade/UF:** {loja_encontrada.get('cidade', '')}/{loja_encontrada.get('estado', '')}")
            with c3:
                st.caption(f"**Horário:** {loja_encontrada.get('horario') or 'N/A'}")
                st.caption(f"**Telefone:** {loja_encontrada.get('tel') or 'N/A'}")

    st.markdown("---")

    # ── Geração dos textos ────────────────────────────────────────────────────
    st.markdown("### 3. Gerar Texto")

    pode_gerar = bool(loja_encontrada or (vd and vd.strip()))
    if not pode_gerar:
        st.info("Informe um VD válido para gerar os textos.")
        return

    if st.button("🔄 Gerar Textos", type="primary", disabled=not pode_gerar):
        hora_str = hora_inicio.strftime("%H:%M") if hora_inicio else datetime.now().strftime("%H:%M")

        if loja_encontrada:
            vivo_txt  = gerar_chamado_vivo(loja_encontrada, nome_atendente or "Central de Comando", hora_str)
            claro_txt = gerar_chamado_claro(loja_encontrada, hora_str)
        else:
            # Fallback: loja não encontrada no banco
            loja_manual = {"vd": vd, "nome": f"VD {vd}", "mpls": "", "inn": "",
                           "endereco": "", "cidade": "", "estado": "", "horario": ""}
            vivo_txt  = gerar_chamado_vivo(loja_manual, nome_atendente or "Central de Comando", hora_str)
            claro_txt = gerar_chamado_claro(loja_manual, hora_str)

        st.session_state["_ch_vivo"]  = vivo_txt
        st.session_state["_ch_claro"] = claro_txt
        st.session_state["_ch_gerado"] = True

    # ── Exibição dos textos gerados ───────────────────────────────────────────
    if st.session_state.get("_ch_gerado"):
        if operadora in ("Vivo + Claro", "Apenas Vivo"):
            st.markdown("#### 📱 Vivo MVE")
            st.code(st.session_state.get("_ch_vivo", ""), language=None)
            st.text_area(
                "Selecione e copie (Ctrl+A → Ctrl+C):",
                value=st.session_state.get("_ch_vivo", ""),
                height=160,
                key="ta_vivo",
            )

        if operadora in ("Vivo + Claro", "Apenas Claro"):
            st.markdown("#### 🔵 Claro Empresas")
            st.code(st.session_state.get("_ch_claro", ""), language=None)
            st.text_area(
                "Selecione e copie (Ctrl+A → Ctrl+C):",
                value=st.session_state.get("_ch_claro", ""),
                height=160,
                key="ta_claro",
            )

    # ── Links dos portais ─────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔗 Portais das Operadoras")
    lc1, lc2 = st.columns(2)
    with lc1:
        st.markdown(
            """
            **📱 Vivo MVE**
            [→ Acessar portal](https://mve.vivo.com.br)
            - Login com credenciais corporativas DPSP
            - Designação = campo MPLS da loja
            """
        )
    with lc2:
        st.markdown(
            """
            **🔵 Claro Empresas**
            [→ Acessar portal](https://webebt01.embratel.com.br/claroempresasonline/index)
            - Login com credenciais corporativas DPSP
            - Designação = campo INN (ou MPLS se INN vazio)
            """
        )
