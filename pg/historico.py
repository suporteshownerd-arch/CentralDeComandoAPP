"""
Página de Histórico
Central de Comando DPSP v3.0
"""

import streamlit as st


_TIPOS = ["Todos", "AExec", "GCrises", "Isolada"]

_ICONES = {
    "AExec":   "🔴",
    "GCrises": "🚨",
    "Isolada": "⚡",
}


def render_page(sheets_manager):
    st.markdown("## 📋 Histórico")
    st.markdown("*Registro de templates e comunicados gerados*")

    # ── Filtro de tipo ────────────────────────────────────────────────────────
    col_f, col_btn = st.columns([3, 1])
    with col_f:
        tipo_filtro = st.selectbox("Filtrar por tipo", _TIPOS, key="hist_tipo")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()

    # ── Buscar registros ──────────────────────────────────────────────────────
    try:
        tipo_arg = None if tipo_filtro == "Todos" else tipo_filtro
        historico = sheets_manager.get_historico(tipo=tipo_arg, limite=50)
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")
        historico = []

    # ── KPIs ──────────────────────────────────────────────────────────────────
    todos = sheets_manager.get_historico(limite=200) if tipo_filtro != "Todos" else historico
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Alertas Exec.", sum(1 for h in todos if str(h.get("tipo", "")).startswith("AExec")))
    with col2:
        st.metric("Gestão Crises", sum(1 for h in todos if str(h.get("tipo", "")).startswith("GCrises")))
    with col3:
        st.metric("Lojas Isoladas", sum(1 for h in todos if str(h.get("tipo", "")).startswith("Isolada")))
    with col4:
        st.metric("Total", len(todos))

    st.markdown("---")

    # ── Lista de registros ────────────────────────────────────────────────────
    if not historico:
        st.info("Nenhum registro encontrado.")
        return

    for i, reg in enumerate(historico):
        tipo  = str(reg.get("tipo", ""))
        sub   = str(reg.get("subtipo", ""))
        label = str(reg.get("label", sub or tipo))
        texto = str(reg.get("texto", ""))
        data  = str(reg.get("data", reg.get("Timestamp", "")))
        icon  = _ICONES.get(tipo, "📄")

        with st.container(border=True):
            hcol1, hcol2 = st.columns([5, 1])
            with hcol1:
                st.markdown(f"**{icon} {label}**")
                if data:
                    st.caption(f"🕐 {data}")
            with hcol2:
                tipo_badge_color = {"AExec": "#f87171", "GCrises": "#fbbf24", "Isolada": "#a78bfa"}.get(tipo, "#9094a6")
                st.markdown(
                    f"<span style='background:rgba(255,255,255,.08);color:{tipo_badge_color};"
                    f"padding:2px 8px;border-radius:8px;font-size:11px'>{tipo}</span>",
                    unsafe_allow_html=True,
                )

            # Preview do texto
            if texto:
                preview = texto[:200] + ("..." if len(texto) > 200 else "")
                st.code(preview, language=None)

            # Texto completo em expander
            if texto and len(texto) > 200:
                with st.expander("Ver texto completo"):
                    st.code(texto, language=None)

            # Ações
            act1, act2, _ = st.columns([1, 1, 3])
            with act1:
                if st.button("📋 Copiar", key=f"copy_h_{i}"):
                    st.session_state[f"_copied_{i}"] = texto
                    st.toast("✅ Texto disponível no campo abaixo!")
            with act2:
                if st.button("🗑️ Excluir", key=f"del_h_{i}"):
                    st.warning("Exclusão individual ainda não implementada. Use 'Limpar Histórico' para apagar tudo.")

            # Campo copiável (aparece após clicar Copiar)
            if st.session_state.get(f"_copied_{i}"):
                st.text_area(
                    "Selecione e copie (Ctrl+A → Ctrl+C):",
                    value=st.session_state[f"_copied_{i}"],
                    height=120,
                    key=f"ta_copy_{i}",
                )

    # ── Limpar histórico ──────────────────────────────────────────────────────
    st.markdown("---")
    with st.expander("⚠️ Zona perigosa"):
        st.warning("Esta ação apaga **todos** os registros permanentemente.")
        if st.button("🗑️ Limpar Histórico Completo", type="primary"):
            try:
                sheets_manager.limpar_historico()
                st.success("✅ Histórico limpo!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao limpar: {e}")
