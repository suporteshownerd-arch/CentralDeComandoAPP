"""
Página de Consulta de Lojas
Central de Comando DPSP v3.0
"""

import streamlit as st

_POR_PAGINA = 10


def render_page(data_loader, lojas):
    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="margin-bottom:24px">
            <h2 style="margin:0;font-family:'Syne',sans-serif;font-size:26px;font-weight:700;color:#eaecf0">
                🏪 Consulta de Lojas
            </h2>
            <p style="margin:4px 0 0 0;font-size:14px;color:#5c6370">
                Busque qualquer loja do parque DPSP por VD, nome, endereço ou circuito
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total   = len(lojas) if lojas else 0
    ativas  = sum(1 for l in lojas if l.get("status") == "open") if lojas else 0
    estados = len({l.get("estado") for l in lojas if l.get("estado")}) if lojas else 0

    k1, k2, k3 = st.columns(3)
    k1.metric("Total de Lojas", f"{total:,}")
    k2.metric("Lojas Ativas",   f"{ativas:,}")
    k3.metric("Estados",        estados)

    st.markdown("<div style='margin:20px 0 0 0'></div>", unsafe_allow_html=True)

    # ── Busca ─────────────────────────────────────────────────────────────────
    col_busca, col_modo = st.columns([4, 1])
    with col_busca:
        termo = st.text_input(
            "Buscar loja",
            placeholder="🔍  VD, nome, cidade, circuito MPLS/INN...",
            key="consulta_termo",
            label_visibility="collapsed",
        )
    with col_modo:
        modo = st.selectbox(
            "Modo",
            ["VD / Designação", "Nome de Loja", "Endereço", "Outra Informação"],
            key="consulta_modo",
            label_visibility="collapsed",
        )

    # ── Filtros ───────────────────────────────────────────────────────────────
    with st.expander("Filtros avançados", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            filtro_estado = st.selectbox("Estado", ["Todos"] + data_loader.get_estados(), key="f_estado")
        with fc2:
            filtro_regiao = st.selectbox("Região", ["Todas"] + data_loader.get_regioes(), key="f_regiao")
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
            st.markdown("### ⭐ Favoritos")
            for loja in lojas_fav:
                _render_card(loja, key_suffix="fav")
            st.markdown("---")

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

    st.markdown(
        f"<p style='font-size:13px;color:#5c6370;margin:8px 0 12px 0'>"
        f"<b style='color:#eaecf0'>{total_res:,}</b> loja(s) encontrada(s)</p>",
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
        st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if pag > 1 and st.button("← Anterior", key="pg_prev"):
                st.session_state.consulta_pagina -= 1
                st.rerun()
        with nav2:
            st.markdown(
                f"<p style='text-align:center;color:#5c6370;font-size:13px;margin:8px 0'>"
                f"Página {pag} de {paginas}</p>",
                unsafe_allow_html=True,
            )
        with nav3:
            if pag < paginas and st.button("Próxima →", key="pg_next"):
                st.session_state.consulta_pagina += 1
                st.rerun()


def _render_card(loja: dict, key_suffix: str = ""):
    vd       = loja.get("vd", "")
    nome     = loja.get("nome", "—")
    bandeira = loja.get("bandeira", "")
    status   = loja.get("status", "open")
    end      = loja.get("endereco", "")
    bairro   = loja.get("bairro", "")
    cidade   = loja.get("cidade", "")
    estado   = loja.get("estado", "")
    cep      = loja.get("cep", "")
    mpls     = loja.get("mpls", "")
    inn      = loja.get("inn", "")
    tel      = loja.get("tel", "")
    tel2     = loja.get("tel2", "")
    cel      = loja.get("cel", "")
    email    = loja.get("email", "")
    horario  = loja.get("horario", "")
    ggl      = loja.get("ggl", "")
    ggl_tel  = loja.get("ggl_tel", "")
    gr       = loja.get("gr", "")
    gr_tel   = loja.get("gr_tel", "")
    circuitos = loja.get("circuitos", [])

    is_open = status == "open"
    status_color = "#34d399" if is_open else "#f87171"
    status_label = "Ativa" if is_open else "Inativa"
    status_bg    = "rgba(52,211,153,.1)" if is_open else "rgba(248,113,113,.1)"

    addr_parts = [p for p in [end, bairro] if p]
    loc_parts  = [p for p in [cidade, estado] if p]
    addr_line  = ", ".join(addr_parts)
    loc_line   = "/".join(loc_parts)
    if cep:
        loc_line += f" · CEP {cep}"

    # Chips de circuito
    chips = ""
    if mpls:
        chips += (
            f"<span style='background:rgba(52,211,153,.1);color:#34d399;"
            f"border:1px solid rgba(52,211,153,.2);padding:2px 9px;border-radius:10px;"
            f"font-size:11px;font-family:monospace;margin-right:5px'>MPLS {mpls}</span>"
        )
    if inn:
        chips += (
            f"<span style='background:rgba(167,139,250,.1);color:#a78bfa;"
            f"border:1px solid rgba(167,139,250,.2);padding:2px 9px;border-radius:10px;"
            f"font-size:11px;font-family:monospace;margin-right:5px'>INN {inn}</span>"
        )
    outros = [c for c in circuitos if c.get("des") not in (mpls, inn) and c.get("des")]
    for c in outros[:2]:
        chips += (
            f"<span style='background:rgba(34,211,238,.08);color:#22d3ee;"
            f"border:1px solid rgba(34,211,238,.18);padding:2px 9px;border-radius:10px;"
            f"font-size:11px;font-family:monospace;margin-right:5px'>"
            f"{c.get('op','')} {c.get('des','')}</span>"
        )

    with st.container(border=True):
        # Linha de título
        col_title, col_status = st.columns([6, 1])
        with col_title:
            band_html = f" <span style='font-size:11px;color:#5c6370'>· {bandeira}</span>" if bandeira else ""
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:2px 0'>"
                f"<code style='background:rgba(91,141,239,.15);color:#5b8def;"
                f"padding:3px 10px;border-radius:6px;font-size:13px;font-weight:600;"
                f"border:1px solid rgba(91,141,239,.2)'>VD {vd}</code>"
                f"<span style='font-weight:700;font-size:16px;color:#eaecf0'>{nome}</span>"
                f"{band_html}</div>",
                unsafe_allow_html=True,
            )
        with col_status:
            st.markdown(
                f"<div style='text-align:right;margin-top:6px'>"
                f"<span style='background:{status_bg};color:{status_color};"
                f"font-size:11px;font-weight:600;padding:3px 10px;border-radius:10px'>"
                f"● {status_label}</span></div>",
                unsafe_allow_html=True,
            )

        # Endereço
        if addr_line or loc_line:
            full_addr = f"{addr_line} · {loc_line}" if addr_line and loc_line else addr_line or loc_line
            st.markdown(
                f"<p style='color:#9094a6;font-size:13px;margin:4px 0 6px 0'>📍 {full_addr}</p>",
                unsafe_allow_html=True,
            )

        # Chips
        if chips:
            st.markdown(f"<div style='margin-bottom:4px'>{chips}</div>", unsafe_allow_html=True)

        # Detalhes expandíveis
        with st.expander("Ver detalhes"):
            d1, d2, d3 = st.columns(3)

            with d1:
                st.markdown("**📞 Contato**")
                if tel:   st.caption(f"Fone 1: {tel}")
                if tel2:  st.caption(f"Fone 2: {tel2}")
                if cel:   st.caption(f"Celular: {cel}")
                if email: st.caption(f"✉️ {email}")
                if horario:
                    st.markdown("**🕐 Horário**")
                    for h in horario.split(" | "):
                        if h:
                            st.caption(h)

            with d2:
                st.markdown("**👥 Gestão**")
                if ggl:
                    st.caption(f"GGL: {ggl}")
                    if ggl_tel: st.caption(f"📱 {ggl_tel}")
                if gr:
                    st.caption(f"GR: {gr}")
                    if gr_tel: st.caption(f"📱 {gr_tel}")

            with d3:
                st.markdown("**⚡ Ações**")
                favs = st.session_state.get("favoritos", [])
                is_fav = vd in favs
                if st.button(
                    "★ Remover dos favoritos" if is_fav else "☆ Favoritar",
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
