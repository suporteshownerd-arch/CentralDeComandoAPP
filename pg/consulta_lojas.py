"""
Página de Consulta de Lojas
Central de Comando DPSP v3.1
"""

import re as _re
import streamlit as st

_POR_PAGINA = 10


def _wa_link(phone: str, label: str) -> str:
    digits = _re.sub(r"\D", "", phone)
    if len(digits) >= 10:
        return f"[{label}](https://wa.me/55{digits})"
    return label


def render_page(data_loader, lojas):

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="page-header">
            <div class="page-header-icon">🏪</div>
            <div>
                <h2 class="page-title">Consulta de Lojas</h2>
                <p class="page-sub">Busque por VD, nome, endereço ou circuito MPLS/INN</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total    = len(lojas) if lojas else 0
    ativas   = sum(1 for l in lojas if l.get("status") == "open")   if lojas else 0
    inativas = sum(1 for l in lojas if l.get("status") == "closed") if lojas else 0
    estados  = len({l.get("estado") for l in lojas if l.get("estado")}) if lojas else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total",    f"{total:,}")
    k2.metric("Ativas",   f"{ativas:,}")
    k3.metric("Inativas", f"{inativas:,}")
    k4.metric("Estados",  estados)

    # ── Busca ─────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    termo = st.text_input(
        "Buscar",
        placeholder="🔍  Digite VD, nome da loja, cidade, designação MPLS/INN...",
        key="consulta_termo",
        label_visibility="collapsed",
    )

    modo = st.radio(
        "Modo de busca",
        ["VD / Designação", "Nome de Loja", "Endereço", "Outra Informação"],
        key="consulta_modo",
        horizontal=True,
        label_visibility="collapsed",
    )

    # ── Filtros ───────────────────────────────────────────────────────────────
    with st.expander("⚙️  Filtros avançados", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            filtro_estado = st.selectbox("Estado", ["Todos"] + data_loader.get_estados(), key="f_estado")
        with fc2:
            filtro_regiao = st.selectbox("Região GGL", ["Todas"] + data_loader.get_regioes(), key="f_regiao")
        with fc3:
            filtro_status = st.selectbox("Status", ["Todos", "Ativa", "Inativa"], key="f_status")

    # ── Aplicar busca e filtros ───────────────────────────────────────────────
    resultados = data_loader.buscar_loja(termo, modo, lojas) if termo else list(lojas)

    if filtro_estado != "Todos":
        resultados = [l for l in resultados if l.get("estado") == filtro_estado]
    if filtro_regiao != "Todas":
        resultados = [l for l in resultados if l.get("regiao") == filtro_regiao]
    if filtro_status == "Ativa":
        resultados = [l for l in resultados if l.get("status") == "open"]
    elif filtro_status == "Inativa":
        resultados = [l for l in resultados if l.get("status") == "closed"]

    # ── Favoritos no topo ─────────────────────────────────────────────────────
    favs = st.session_state.get("favoritos", [])
    if favs and not termo:
        lojas_fav = [l for l in lojas if l.get("vd") in favs]
        if lojas_fav:
            st.markdown(
                "<p class='section-label'>⭐ Favoritos</p>",
                unsafe_allow_html=True,
            )
            for loja in lojas_fav:
                _render_card(loja, key_suffix="fav")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.divider()

    # ── Resultado e paginação ─────────────────────────────────────────────────
    filtros_ativos = (
        filtro_estado != "Todos"
        or filtro_regiao != "Todas"
        or filtro_status != "Todos"
    )
    total_res = len(resultados)
    if total_res == 0:
        if termo:
            st.info(f'Nenhuma loja encontrada para **"{termo}"**. Tente outro modo de busca.')
        elif filtros_ativos:
            st.info("Nenhuma loja encontrada com os filtros aplicados.")
        else:
            st.info("Use a busca acima para encontrar lojas.")
        return

    if termo or filtros_ativos:
        st.markdown(
            f"<p class='result-count'><b>{total_res:,}</b> loja(s) encontrada(s)</p>",
            unsafe_allow_html=True,
        )

    # Paginação
    paginas = max(1, -(-total_res // _POR_PAGINA))
    filtro_key = (termo, modo, filtro_estado, filtro_regiao, filtro_status)
    if st.session_state.get("_ultimo_filtro") != filtro_key:
        st.session_state.consulta_pagina = 1
        st.session_state["_ultimo_filtro"] = filtro_key
    if "consulta_pagina" not in st.session_state:
        st.session_state.consulta_pagina = 1

    pag = st.session_state.consulta_pagina
    ini = (pag - 1) * _POR_PAGINA
    fim = ini + _POR_PAGINA

    for i, loja in enumerate(resultados[ini:fim]):
        _render_card(loja, key_suffix=f"r{ini+i}")

    # Navegação de páginas
    if paginas > 1:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if pag > 1 and st.button("← Anterior", key="pg_prev", use_container_width=True):
                st.session_state.consulta_pagina -= 1
                st.rerun()
        with nav2:
            st.markdown(
                f"<p style='text-align:center;color:#5c6370;font-size:13px;margin:8px 0'>"
                f"Página {pag} de {paginas}</p>",
                unsafe_allow_html=True,
            )
        with nav3:
            if pag < paginas and st.button("Próxima →", key="pg_next", use_container_width=True):
                st.session_state.consulta_pagina += 1
                st.rerun()


def _render_card(loja: dict, key_suffix: str = ""):
    vd        = loja.get("vd", "")
    nome      = loja.get("nome", "—")
    bandeira  = loja.get("bandeira", "")
    status    = loja.get("status", "open")
    end       = loja.get("endereco", "")
    bairro    = loja.get("bairro", "")
    cidade    = loja.get("cidade", "")
    estado    = loja.get("estado", "")
    cep       = loja.get("cep", "")
    mpls      = loja.get("mpls", "")
    inn       = loja.get("inn", "")
    tel       = loja.get("tel", "")
    tel2      = loja.get("tel2", "")
    cel       = loja.get("cel", "")
    email     = loja.get("email", "")
    horario   = loja.get("horario", "")
    ggl       = loja.get("ggl", "")
    ggl_tel   = loja.get("ggl_tel", "")
    gr        = loja.get("gr", "")
    gr_tel    = loja.get("gr_tel", "")
    circuitos = loja.get("circuitos", [])
    regiao    = loja.get("regiao", "")

    # Status colors - v4.0 design system
    if status == "open":
        s_color, s_bg, s_label = "#10b981", "rgba(16,185,129,.12)", "Ativa"
    elif status == "pending":
        s_color, s_bg, s_label = "#f59e0b", "rgba(245,158,11,.12)", "A Inaugurar"
    else:
        s_color, s_bg, s_label = "#ef4444", "rgba(239,68,68,.12)", "Inativa"

    # Endereço
    parts = [p for p in [end, bairro, cidade] if p]
    addr  = ", ".join(parts)
    if estado: addr += f" · {estado}"
    if cep:    addr += f" · CEP {cep}"

    # Chips de circuito
    chips_html = ""
    if mpls:
        chips_html += f"<span class='chip chip-green'>MPLS&nbsp;{mpls}</span>"
    if inn:
        chips_html += f"<span class='chip chip-purple'>INN&nbsp;{inn}</span>"
    outros = [c for c in circuitos if c.get("des") not in (mpls, inn) and c.get("des")]
    for c in outros:
        chips_html += f"<span class='chip chip-cyan'>{c.get('op','')} {c.get('des','')}</span>"

    # Contato rápido visível
    contato_principal = cel or tel
    contato_html = ""
    if contato_principal:
        digs = _re.sub(r"\D", "", contato_principal)
        if len(digs) >= 10:
            contato_html = (
                f"<a href='https://wa.me/55{digs}' target='_blank' class='quick-contact green'>"
                f"📱 {contato_principal}</a>"
            )
        else:
            contato_html = f"<span class='quick-contact muted'>📞 {contato_principal}</span>"

    ggl_html = ""
    if ggl:
        if ggl_tel:
            digs_g = _re.sub(r"\D", "", ggl_tel)
            if len(digs_g) >= 10:
                ggl_html = (
                    f"<a href='https://wa.me/55{digs_g}' target='_blank' class='quick-contact accent'>"
                    f"👤 {ggl}</a>"
                )
            else:
                ggl_html = f"<span class='quick-contact muted'>👤 {ggl}</span>"
        else:
            ggl_html = f"<span class='quick-contact muted'>👤 {ggl}</span>"

    with st.container(border=True):
        # ── Cabeçalho do card ──────────────────────────────────────────────
        col_info, col_badge = st.columns([7, 1])
        with col_info:
            band_tag = f"<span class='card-bandeira'>{bandeira}</span>" if bandeira else ""
            st.markdown(
                f"<div class='card-header'>"
                f"<span class='card-vd'>VD {vd}</span>"
                f"<span class='card-nome'>{nome}</span>"
                f"{band_tag}"
                f"</div>",
                unsafe_allow_html=True,
            )
        with col_badge:
            st.markdown(
                f"<div style='text-align:right;padding-top:4px'>"
                f"<span style='background:{s_bg};color:{s_color};"
                f"font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;"
                f"white-space:nowrap'>● {s_label}</span></div>",
                unsafe_allow_html=True,
            )

        # ── Endereço + Região ──────────────────────────────────────────────
        meta_parts = []
        if addr:    meta_parts.append(f"📍 {addr}")
        if regiao:  meta_parts.append(f"🗺 {regiao}")
        if meta_parts:
            st.markdown(
                "<p class='card-meta'>" + "&emsp;·&emsp;".join(meta_parts) + "</p>",
                unsafe_allow_html=True,
            )

        # ── Chips + contatos rápidos ───────────────────────────────────────
        row_html = ""
        if chips_html:   row_html += chips_html
        if contato_html: row_html += contato_html
        if ggl_html:     row_html += ggl_html
        if row_html:
            st.markdown(
                f"<div class='card-row'>{row_html}</div>",
                unsafe_allow_html=True,
            )

        # ── Detalhes expandíveis ───────────────────────────────────────────
        with st.expander("Ver mais detalhes"):
            d1, d2, d3 = st.columns(3)

            with d1:
                st.markdown("**📞 Contato**")
                if tel:    st.markdown(_wa_link(tel,   f"📞 {tel}"))
                if tel2:   st.markdown(_wa_link(tel2,  f"📞 {tel2}"))
                if cel:    st.markdown(_wa_link(cel,   f"📱 {cel}"))
                if email:  st.caption(f"✉️ {email}")
                if horario:
                    st.markdown("**🕐 Horário**")
                    for h in horario.split(" | "):
                        if h: st.caption(h)

            with d2:
                st.markdown("**👥 Gestão**")
                if ggl:
                    st.caption(f"GGL: {ggl}")
                    if ggl_tel: st.markdown(_wa_link(ggl_tel, f"📱 {ggl_tel}"))
                if gr:
                    st.caption(f"GR: {gr}")
                    if gr_tel:  st.markdown(_wa_link(gr_tel,  f"📱 {gr_tel}"))

            with d3:
                st.markdown("**⚡ Ações**")
                favs   = st.session_state.get("favoritos", [])
                is_fav = vd in favs
                if st.button(
                    "★ Remover" if is_fav else "☆ Favoritar",
                    key=f"fav_{vd}_{key_suffix}",
                    use_container_width=True,
                ):
                    if is_fav:
                        st.session_state.favoritos.remove(vd)
                    elif len(favs) < 10:
                        st.session_state.favoritos.append(vd)
                    else:
                        st.warning("Limite de 10 favoritos atingido.")
                    st.rerun()

                if st.button("📞 Abrir Chamado", key=f"ch_{vd}_{key_suffix}", use_container_width=True):
                    st.session_state.loja_selecionada = loja
                    st.session_state.nav_page = "Abertura de Chamados"
                    st.session_state.pop("_ch_gerado", None)
                    st.rerun()
