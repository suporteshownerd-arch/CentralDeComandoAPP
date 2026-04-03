"""
Página de Gestão de Crises
Central de Comando DPSP v3.1
"""

import streamlit as st
from datetime import datetime, timedelta


def _step(num: str, title: str, sub: str = ""):
    sub_html = f"<div class='step-sub'>{sub}</div>" if sub else ""
    st.markdown(
        f"""<div class='step-header'>
            <div class='step-num'>{num}</div>
            <div><div class='step-title'>{title}</div>{sub_html}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def render_page(sheets_manager, lojas):
    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="page-header">
            <div class="page-header-icon">🚨</div>
            <div>
                <h2 class="page-title">Gestão de Crises</h2>
                <p class="page-sub">Gere templates para alertas executivos, crises e lojas isoladas</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_ex, tab_gc, tab_iso = st.tabs([
        "🔴  Alertas Executivos",
        "🚨  Gestão de Crise",
        "⚡  Loja Isolada",
    ])

    with tab_ex:
        render_alertas_executivos()

    with tab_gc:
        render_gestao_crise()

    with tab_iso:
        render_loja_isolada(lojas)


# ── Alertas Executivos ────────────────────────────────────────────────────────

def render_alertas_executivos():
    from templates import gerar_alerta_executivo

    _step("1", "Configurar o Incidente", "Defina escopo, horário e abrangência")

    c1, c2, c3 = st.columns(3)
    with c1:
        escopo = st.selectbox(
            "Escopo",
            ["Internet - MPLS", "Internet - INN", "Sistema POS", "Sistema ERP",
             "VPN", "Data Center", "Energia"],
            key="ex_escopo",
        )
    with c2:
        ident = st.selectbox(
            "Identificação",
            ["Central identificou", "Acionada por terceiros", "Alerta automático"],
            key="ex_ident",
        )
    with c3:
        abrangencia = st.text_input(
            "Abrangência",
            placeholder="Ex: Todo o parque SP...",
            key="ex_abrang",
        )

    c4, c5, c6 = st.columns(3)
    with c4:
        inicio = st.time_input("Início", key="ex_inicio")
    with c5:
        termino = st.time_input("Término", key="ex_termino")
    with c6:
        equipes = st.text_input("Equipes envolvidas", placeholder="NOC, Infra...", key="ex_equipes")

    _step("2", "Status Atual", "Descreva o estado do incidente")
    status = st.text_area("Status do incidente", height=90, key="ex_status",
                          placeholder="Instabilidade identificada em circuitos MPLS...")

    _step("3", "Selecionar Templates a Gerar")
    ck1, ck2, ck3 = st.columns(3)
    with ck1:
        gerar_ab   = st.checkbox("🔴 Abertura",      value=True,  key="ex_ab")
    with ck2:
        gerar_atu  = st.checkbox("🟡 Atualização",   value=False, key="ex_atu")
    with ck3:
        gerar_norm = st.checkbox("🟢 Normalização",  value=False, key="ex_norm")

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    if st.button("🔄  Gerar Templates", type="primary", key="ex_gerar", use_container_width=True):
        templates = gerar_alerta_executivo(
            escopo, ident, inicio, termino,
            abrangencia, equipes, status,
            gerar_ab, gerar_atu, gerar_norm,
        )
        st.session_state["_ex_templates"] = templates

    if st.session_state.get("_ex_templates"):
        _render_templates(st.session_state["_ex_templates"], prefix="ex")


# ── Gestão de Crise ───────────────────────────────────────────────────────────

def render_gestao_crise():
    from templates import gerar_gestao_crise

    _step("1", "Dados do Incidente", "Preencha o número, responsáveis e horários")

    c1, c2, c3 = st.columns(3)
    with c1:
        num_inc   = st.text_input("Nº Incidente",     placeholder="INC-0001",   key="gc_num")
        link_sala = st.text_input("Link da Sala",     placeholder="https://...", key="gc_link")
    with c2:
        resp_tec  = st.text_input("Resp. Técnico",    placeholder="Nome",        key="gc_tec")
        resp_cmd  = st.text_input("Resp. Command",    placeholder="Nome",        key="gc_cmd")
    with c3:
        hora_inc   = st.time_input("Hora do Incidente",   key="gc_hora_inc")
        hora_acion = st.time_input("Hora do Acionamento", key="gc_hora_acion")

    c4, c5 = st.columns(2)
    with c4:
        unidades = st.text_input("Unidades afetadas", placeholder="SP, RJ...", key="gc_unidades")
    with c5:
        causa = st.text_input("Causa identificada",  placeholder="Falha de enlace...", key="gc_causa")

    _step("2", "Atualização", "Descreva o estado atual")

    col_atu, col_cnt = st.columns([4, 1])
    with col_atu:
        atualizacao = st.text_area("Texto de atualização", height=90, key="gc_atu",
                                   placeholder="Aguardando retorno da operadora...")
    with col_cnt:
        contador = st.number_input("Nº Atualizações", 1, 99, 1, key="gc_cnt")
        if hora_inc:
            proximo = (datetime.combine(datetime.today(), hora_inc) + timedelta(minutes=30)).time()
            st.markdown(
                f"<div style='background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.2);"
                f"border-radius:8px;padding:8px 12px;margin-top:6px;text-align:center'>"
                f"<div style='font-size:10px;color:#5c6370;font-family:DM Mono,monospace'>PRÓX. ATU.</div>"
                f"<div style='font-size:16px;color:#fbbf24;font-weight:700;font-family:Syne,sans-serif'>"
                f"{proximo.strftime('%H:%M')}</div></div>",
                unsafe_allow_html=True,
            )

    _step("3", "Selecionar Templates")
    ck1, ck2 = st.columns(2)
    with ck1:
        gerar_gc_ab   = st.checkbox("🔴 Abertura",      value=True,  key="gc_ab")
    with ck2:
        gerar_gc_norm = st.checkbox("🟢 Normalização",  value=False, key="gc_norm")

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    if st.button("🔄  Gerar Templates", type="primary", key="gc_gerar", use_container_width=True):
        templates = gerar_gestao_crise(
            num_inc, link_sala, unidades, causa,
            resp_tec, resp_cmd, hora_inc, hora_acion,
            atualizacao, contador, gerar_gc_ab, gerar_gc_norm,
        )
        st.session_state["_gc_templates"] = templates

    if st.session_state.get("_gc_templates"):
        _render_templates(st.session_state["_gc_templates"], prefix="gc")


# ── Loja Isolada ─────────────────────────────────────────────────────────────

def render_loja_isolada(lojas):
    from templates import gerar_loja_isolada

    _step("1", "Identificar a Loja e o Incidente")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vd_iso = st.text_input("VD da loja", placeholder="Ex: 2015", key="iso_vd")
    with c2:
        tipo_iso = st.selectbox("Tipo", ["Energia Elétrica", "Internet"], key="iso_tipo")
    with c3:
        hora_in  = st.time_input("Início", key="iso_in")
    with c4:
        hora_ret = st.time_input("Previsão de retorno", key="iso_ret")

    # Preview da loja se VD válido
    if vd_iso and vd_iso.strip().isdigit():
        loja_enc = next((l for l in lojas if l.get("vd") == vd_iso.strip()), None)
        if loja_enc:
            st.markdown(
                f"<div style='background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.2);"
                f"border-radius:10px;padding:10px 16px;margin:8px 0 0 0'>"
                f"<span style='color:#34d399;font-size:12px;font-weight:600'>"
                f"✅ {loja_enc.get('nome','—')} — {loja_enc.get('cidade','')}/{loja_enc.get('estado','')}"
                f"</span></div>",
                unsafe_allow_html=True,
            )
        else:
            st.warning("VD não encontrado na base de dados.")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("🔄  Gerar Templates", type="primary", key="iso_gerar", use_container_width=True):
        tipo_key = "energia" if "Energia" in tipo_iso else "internet"
        templates = gerar_loja_isolada(vd_iso, tipo_key, hora_in, hora_ret, lojas)
        st.session_state["_iso_templates"] = templates

    if st.session_state.get("_iso_templates"):
        _render_templates(st.session_state["_iso_templates"], prefix="iso")


# ── Renderização de templates ─────────────────────────────────────────────────

def _render_templates(templates: list, prefix: str = ""):
    if not templates:
        return

    st.markdown(
        "<div style='margin:20px 0 10px 0;font-family:DM Mono,monospace;font-size:9px;"
        "color:#5c6370;text-transform:uppercase;letter-spacing:.14em'>Templates Gerados</div>",
        unsafe_allow_html=True,
    )

    _badge_map = {
        "abertura":      ("tpl-badge-ab",   "🔴 ABERTURA"),
        "atualizacao":   ("tpl-badge-atu",  "🟡 ATUALIZAÇÃO"),
        "normalizacao":  ("tpl-badge-norm", "🟢 NORMALIZAÇÃO"),
    }

    for i, t in enumerate(templates):
        label  = t.get("label", t.get("tipo", "Template"))
        tipo   = t.get("tipo", "abertura").lower()
        texto  = t.get("texto", "")
        badge_cls, badge_txt = _badge_map.get(tipo, ("tpl-badge-ab", tipo.upper()))

        with st.container(border=True):
            h1, h2 = st.columns([5, 1])
            with h1:
                st.markdown(
                    f"<div style='font-size:13px;font-weight:600;color:#eaecf0'>{label}</div>",
                    unsafe_allow_html=True,
                )
            with h2:
                st.markdown(
                    f"<div style='text-align:right'><span class='{badge_cls}'>{badge_txt}</span></div>",
                    unsafe_allow_html=True,
                )

            st.code(texto, language=None)

            col_copy, _ = st.columns([1, 4])
            with col_copy:
                if st.button(f"📋 Copiar", key=f"copy_{prefix}_{i}", use_container_width=True):
                    st.session_state[f"_copy_{prefix}_{i}"] = texto
                    st.toast("✅ Texto disponível no campo abaixo!")

            if st.session_state.get(f"_copy_{prefix}_{i}"):
                st.text_area(
                    "Selecione e copie (Ctrl+A → Ctrl+C):",
                    value=st.session_state[f"_copy_{prefix}_{i}"],
                    height=120,
                    key=f"ta_{prefix}_{i}",
                )
