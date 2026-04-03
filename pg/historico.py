"""
Página de Histórico
Central de Comando DPSP v4.2
"""

import logging
import streamlit as st

try:
    from components.error_handler import handle_errors, render_empty_state
except ImportError:
    def handle_errors(title="Erro", show_trace=False):
        def decorator(func):
            return func
        return decorator
    
    def render_empty_state(icon="📭", title="Nenhum dado", message="", action_label=None, action_callback=None):
        st.info(f"{icon} {title}: {message}")

logger = logging.getLogger(__name__)

_TIPOS = ["Todos", "AExec", "GCrises", "Isolada"]

_ICONES = {
    "AExec":   "🔴",
    "GCrises": "🚨",
    "Isolada": "⚡",
}

_BADGE_COLORS = {
    "AExec":   ("#f87171", "rgba(248,113,113,.12)"),
    "GCrises": ("#fbbf24", "rgba(251,191,36,.12)"),
    "Isolada": ("#a78bfa", "rgba(167,139,250,.12)"),
}

_BORDER_COLORS = {
    "AExec":   "#f87171",
    "GCrises": "#fbbf24",
    "Isolada": "#a78bfa",
}


def render_page(sheets_manager):
    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="page-header">
            <div class="page-header-icon">📋</div>
            <div>
                <h2 class="page-title">Histórico</h2>
                <p class="page-sub">Registro de templates e comunicados gerados</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Filtro + Atualizar ────────────────────────────────────────────────────
    col_f, col_btn = st.columns([3, 1])
    with col_f:
        tipo_filtro = st.selectbox("Filtrar por tipo", _TIPOS, key="hist_tipo",
                                   label_visibility="collapsed")
    with col_btn:
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
    try:
        todos = sheets_manager.get_historico(limite=200) if tipo_filtro != "Todos" else historico
    except Exception:
        todos = historico

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Alertas Exec.",   sum(1 for h in todos if str(h.get("tipo","")).startswith("AExec")))
    col2.metric("Gestão Crises",   sum(1 for h in todos if str(h.get("tipo","")).startswith("GCrises")))
    col3.metric("Lojas Isoladas",  sum(1 for h in todos if str(h.get("tipo","")).startswith("Isolada")))
    col4.metric("Total",           len(todos))

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Lista de registros ────────────────────────────────────────────────────
    if not historico:
        st.info("Nenhum registro encontrado.")
    else:
        for i, reg in enumerate(historico):
            tipo  = str(reg.get("tipo", ""))
            sub   = str(reg.get("subtipo", ""))
            label = str(reg.get("label", sub or tipo))
            texto = str(reg.get("texto", ""))
            data  = str(reg.get("data", reg.get("Timestamp", "")))
            icon  = _ICONES.get(tipo, "📄")
            bdr   = _BORDER_COLORS.get(tipo, "#5c6370")
            fc, bg = _BADGE_COLORS.get(tipo, ("#9094a6", "rgba(144,148,166,.12)"))

            with st.container(border=True):
                # Apply colored left border via inline override
                st.markdown(
                    f"<style>[data-testid='stVerticalBlockBorderWrapper']:nth-child({i+1})"
                    f"{{border-left:3px solid {bdr} !important}}</style>",
                    unsafe_allow_html=True,
                )
                hcol1, hcol2 = st.columns([5, 1])
                with hcol1:
                    st.markdown(
                        f"<div style='font-weight:700;font-size:14px;color:#eaecf0'>{icon} {label}</div>",
                        unsafe_allow_html=True,
                    )
                    if data:
                        st.markdown(
                            f"<div style='font-size:11px;color:#5c6370;font-family:DM Mono,monospace;"
                            f"margin-top:2px'>🕐 {data}</div>",
                            unsafe_allow_html=True,
                        )
                with hcol2:
                    st.markdown(
                        f"<div style='text-align:right;padding-top:4px'>"
                        f"<span style='background:{bg};color:{fc};"
                        f"padding:2px 10px;border-radius:20px;font-size:10px;"
                        f"font-family:DM Mono,monospace;font-weight:600'>{tipo}</span></div>",
                        unsafe_allow_html=True,
                    )

                if texto:
                    preview = texto[:200] + ("…" if len(texto) > 200 else "")
                    st.code(preview, language=None)

                if texto and len(texto) > 200:
                    with st.expander("Ver texto completo"):
                        st.code(texto, language=None)

                act1, act2, _ = st.columns([1, 1, 3])
                with act1:
                    if st.button("📋 Copiar", key=f"copy_h_{i}", use_container_width=True):
                        st.session_state[f"_copied_{i}"] = texto
                        st.toast("✅ Texto disponível no campo abaixo!")
                with act2:
                    if st.button("🗑️ Excluir", key=f"del_h_{i}", use_container_width=True):
                        st.warning("Exclusão individual ainda não implementada.")

                if st.session_state.get(f"_copied_{i}"):
                    st.text_area(
                        "Selecione e copie (Ctrl+A → Ctrl+C):",
                        value=st.session_state[f"_copied_{i}"],
                        height=120, key=f"ta_copy_{i}",
                    )

    # ── Zona perigosa ─────────────────────────────────────────────────────────
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    with st.expander("⚠️ Zona perigosa"):
        st.warning("Esta ação apaga **todos** os registros permanentemente.")
        if st.button("🗑️ Limpar Histórico Completo", type="primary"):
            try:
                sheets_manager.limpar_historico()
                st.success("✅ Histórico limpo!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao limpar: {e}")
