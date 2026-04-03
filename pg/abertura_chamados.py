"""
Página de Abertura de Chamados
Central de Comando DPSP v4.2
"""

import logging
import streamlit as st
from datetime import datetime
from templates import gerar_chamado_vivo, gerar_chamado_claro

try:
    from components.error_handler import handle_errors
except ImportError:
    def handle_errors(title="Erro", show_trace=False):
        def decorator(func):
            return func
        return decorator

logger = logging.getLogger(__name__)


def _step(num: str, title: str, sub: str = ""):
    sub_html = f"<div class='step-sub'>{sub}</div>" if sub else ""
    st.markdown(
        f"""<div class='step-header'>
            <div class='step-num'>{num}</div>
            <div><div class='step-title'>{title}</div>{sub_html}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def render_page(lojas):
    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="page-header">
            <div class="page-header-icon">📞</div>
            <div>
                <h2 class="page-title">Abertura de Chamados</h2>
                <p class="page-sub">Gere o texto para abertura de chamado nas operadoras Vivo e Claro</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 1. Identificar a loja ─────────────────────────────────────────────────
    _step("1", "Identificar a Loja", "Digite o VD para preenchimento automático")

    col_vd, col_info = st.columns([1, 3])

    loja_pre = st.session_state.get("loja_selecionada")
    vd_default = loja_pre.get("vd", "") if loja_pre else ""

    if vd_default and st.session_state.get("_ch_ultima_loja") != vd_default:
        st.session_state.pop("_ch_gerado", None)
        st.session_state["_ch_ultima_loja"] = vd_default

    with col_vd:
        vd = st.text_input(
            "VD da loja",
            value=vd_default,
            placeholder="Ex: 2015",
            key="ch_vd",
        )

    loja_encontrada = None
    if vd and vd.strip().isdigit():
        loja_encontrada = next((l for l in lojas if l.get("vd") == vd.strip()), None)

    with col_info:
        if loja_encontrada:
            st.markdown(
                f"<div style='background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.2);"
                f"border-radius:10px;padding:10px 16px;height:56px;display:flex;align-items:center'>"
                f"<span style='color:#34d399;font-size:13px;font-weight:600'>"
                f"✅ {loja_encontrada['nome']} — {loja_encontrada.get('cidade','')}/{loja_encontrada.get('estado','')}"
                f"</span></div>",
                unsafe_allow_html=True,
            )
        elif vd:
            st.warning("⚠️ VD não encontrado. Preencha os campos manualmente.")

    # Preview dos dados da loja
    if loja_encontrada:
        with st.expander("📋 Dados da loja que serão usados"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.caption(f"**Designação MPLS:** {loja_encontrada.get('mpls') or 'N/A'}")
                st.caption(f"**Designação INN:** {loja_encontrada.get('inn') or 'N/A'}")
            with c2:
                st.caption(f"**Endereço:** {loja_encontrada.get('endereco', '')}")
                st.caption(f"**Cidade/UF:** {loja_encontrada.get('cidade','')}/{loja_encontrada.get('estado','')}")
            with c3:
                st.caption(f"**Horário:** {loja_encontrada.get('horario') or 'N/A'}")
                st.caption(f"**Telefone:** {loja_encontrada.get('tel') or 'N/A'}")

    # ── 2. Dados do atendimento ───────────────────────────────────────────────
    _step("2", "Dados do Atendimento", "Seu nome, hora do incidente e operadora")

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

    # ── 3. Gerar ─────────────────────────────────────────────────────────────
    _step("3", "Gerar e Copiar o Texto")

    pode_gerar = bool(loja_encontrada or (vd and vd.strip()))
    if not pode_gerar:
        st.info("Informe um VD válido para gerar os textos.")
        return

    if st.button("🔄  Gerar Textos", type="primary", use_container_width=True, disabled=not pode_gerar):
        hora_str = hora_inicio.strftime("%H:%M") if hora_inicio else datetime.now().strftime("%H:%M")

        if loja_encontrada:
            vivo_txt  = gerar_chamado_vivo(loja_encontrada, nome_atendente or "Central de Comando", hora_str)
            claro_txt = gerar_chamado_claro(loja_encontrada, hora_str)
        else:
            loja_manual = {"vd": vd, "nome": f"VD {vd}", "mpls": "", "inn": "",
                           "endereco": "", "cidade": "", "estado": "", "horario": ""}
            vivo_txt  = gerar_chamado_vivo(loja_manual, nome_atendente or "Central de Comando", hora_str)
            claro_txt = gerar_chamado_claro(loja_manual, hora_str)

        st.session_state["_ch_vivo"]   = vivo_txt
        st.session_state["_ch_claro"]  = claro_txt
        st.session_state["_ch_gerado"] = True

    # ── Textos gerados ────────────────────────────────────────────────────────
    if st.session_state.get("_ch_gerado"):
        if operadora in ("Vivo + Claro", "Apenas Vivo"):
            with st.container(border=True):
                h1, h2 = st.columns([5, 1])
                with h1:
                    st.markdown(
                        "<div style='font-size:13px;font-weight:600;color:#eaecf0'>📱 Vivo MVE</div>",
                        unsafe_allow_html=True,
                    )
                with h2:
                    st.markdown(
                        "<div style='text-align:right'><span style='background:rgba(91,141,239,.15);"
                        "color:#5b8def;font-size:10px;padding:2px 8px;border-radius:20px;"
                        "font-family:DM Mono,monospace'>VIVO</span></div>",
                        unsafe_allow_html=True,
                    )
                st.code(st.session_state.get("_ch_vivo", ""), language=None)
                st.text_area(
                    "Selecione e copie (Ctrl+A → Ctrl+C):",
                    value=st.session_state.get("_ch_vivo", ""),
                    height=140, key="ta_vivo",
                )

        if operadora in ("Vivo + Claro", "Apenas Claro"):
            with st.container(border=True):
                h1, h2 = st.columns([5, 1])
                with h1:
                    st.markdown(
                        "<div style='font-size:13px;font-weight:600;color:#eaecf0'>🔵 Claro Empresas</div>",
                        unsafe_allow_html=True,
                    )
                with h2:
                    st.markdown(
                        "<div style='text-align:right'><span style='background:rgba(34,211,238,.1);"
                        "color:#22d3ee;font-size:10px;padding:2px 8px;border-radius:20px;"
                        "font-family:DM Mono,monospace'>CLARO</span></div>",
                        unsafe_allow_html=True,
                    )
                st.code(st.session_state.get("_ch_claro", ""), language=None)
                st.text_area(
                    "Selecione e copie (Ctrl+A → Ctrl+C):",
                    value=st.session_state.get("_ch_claro", ""),
                    height=140, key="ta_claro",
                )

    # ── Portais ───────────────────────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    with st.expander("🔗 Portais das Operadoras"):
        lc1, lc2 = st.columns(2)
        with lc1:
            st.markdown(
                """
                <div class='portal-card'>
                <div style='font-weight:700;font-size:13px;color:#eaecf0;margin-bottom:8px'>📱 Vivo MVE</div>
                <a href='https://mve.vivo.com.br' target='_blank'>→ Acessar portal Vivo MVE</a>
                <div style='font-size:12px;color:#5c6370;margin-top:6px'>
                Designação = campo <b>MPLS</b> da loja
                </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with lc2:
            st.markdown(
                """
                <div class='portal-card'>
                <div style='font-weight:700;font-size:13px;color:#eaecf0;margin-bottom:8px'>🔵 Claro Empresas</div>
                <a href='https://webebt01.embratel.com.br/claroempresasonline/index' target='_blank'>→ Acessar portal Claro</a>
                <div style='font-size:12px;color:#5c6370;margin-top:6px'>
                Designação = campo <b>INN</b> (ou MPLS se INN vazio)
                </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
