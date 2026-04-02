"""
Página de Consulta de Lojas
Central de Comando DPSP v3.0
"""

import streamlit as st

_POR_PAGINA = 10


def render_page(data_loader, lojas):
    st.markdown("## 🏪 Consulta de Lojas")
    st.markdown("*Busque qualquer loja do parque DPSP por VD, nome, endereço ou circuito*")

    # ── KPIs rápidos ──────────────────────────────────────────────────────────
    total   = len(lojas) if lojas else 0
    ativas  = sum(1 for l in lojas if l.get("status") == "open") if lojas else 0
    estados = len({l.get("estado") for l in lojas if l.get("estado")}) if lojas else 0
    k1, k2, k3 = st.columns(3)
    k1.metric("Total de Lojas", total)
    k2.metric("Lojas Ativas",   ativas)
    k3.metric("Estados",        estados)

    st.markdown("---")

    # ── Barra de busca ────────────────────────────────────────────────────────
    col_busca, col_modo = st.columns([3, 1])
    with col_busca:
        termo = st.text_input(
            "🔍 Buscar loja",
            placeholder="VD, nome, cidade, circuito MPLS/INN...",
            key="consulta_termo",
        )
    with col_modo:
        modo = st.selectbox(
            "Modo",
            ["VD / Designação", "Nome de Loja", "Endereço", "Outra Informação"],
            key="consulta_modo",
        )

    # ── Filtros avançados ─────────────────────────────────────────────────────
    with st.expander("🔽 Filtros avançados", expanded=False):
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
    total_res = len(resultados)
    if total_res == 0:
        if termo:
            st.info(f"Nenhuma loja encontrada para **\"{termo}\"**. Tente outro modo de busca.")
        else:
            st.info("Use a busca acima para encontrar lojas.")
        return

    st.markdown(f"**{total_res} loja(s) encontrada(s)**")

    # Paginação
    paginas = max(1, -(-total_res // _POR_PAGINA))
    if st.session_state.get("_ultimo_filtro") != (termo, modo, filtro_estado, filtro_regiao, filtro_status):
        st.session_state.consulta_pagina = 1
        st.session_state["_ultimo_filtro"] = (termo, modo, filtro_estado, filtro_regiao, filtro_status)
    if "consulta_pagina" not in st.session_state:
        st.session_state.consulta_pagina = 1

    pag = st.session_state.consulta_pagina
    ini = (pag - 1) * _POR_PAGINA
    fim = ini + _POR_PAGINA

    for i, loja in enumerate(resultados[ini:fim]):
        _render_card(loja, key_suffix=f"r{ini+i}")

    # Navegação
    if paginas > 1:
        st.markdown("---")
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if pag > 1 and st.button("← Anterior", key="pg_prev"):
                st.session_state.consulta_pagina -= 1
                st.rerun()
        with nav2:
            st.markdown(
                f"<p style='text-align:center;color:#9094a6;margin:8px 0'>Página {pag} de {paginas}</p>",
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

    status_color = "#34d399" if status == "open" else "#f87171"
    status_label = "Ativa" if status == "open" else "Inativa"

    # Endereço formatado
    addr_parts = [p for p in [end, bairro] if p]
    loc_parts  = [p for p in [cidade, estado] if p]
    addr_line  = ", ".join(addr_parts)
    loc_line   = "/".join(loc_parts) + (f" — CEP {cep}" if cep else "")

    with st.container(border=True):
        # ── Cabeçalho ────────────────────────────────────────────────────────
        head_l, head_r = st.columns([5, 1])
        with head_l:
            badge_band = f"<span style='font-size:10px;color:#9094a6;margin-left:8px'>{bandeira}</span>" if bandeira else ""
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:10px;flex-wrap:wrap'>"
                f"<span style='font-family:monospace;background:rgba(91,141,239,.18);color:#5b8def;"
                f"padding:3px 10px;border-radius:6px;font-size:13px;font-weight:600'>VD {vd}</span>"
                f"<span style='font-weight:700;font-size:16px;color:#eaecf0'>{nome}</span>"
                f"{badge_band}</div>",
                unsafe_allow_html=True,
            )
        with head_r:
            st.markdown(
                f"<div style='text-align:right;margin-top:4px'>"
                f"<span style='background:transparent;color:{status_color};"
                f"font-size:12px;font-weight:600'>● {status_label}</span></div>",
                unsafe_allow_html=True,
            )

        # ── Endereço ─────────────────────────────────────────────────────────
        if addr_line or loc_line:
            st.markdown(
                f"<p style='color:#9094a6;font-size:13px;margin:4px 0 6px 0'>"
                f"📍 {addr_line}{' — ' if addr_line and loc_line else ''}{loc_line}</p>",
                unsafe_allow_html=True,
            )

        # ── Chips de circuitos ────────────────────────────────────────────────
        chips_html = ""
        if mpls:
            chips_html += (
                f"<span style='background:rgba(52,211,153,.12);color:#34d399;border:1px solid rgba(52,211,153,.25);"
                f"padding:2px 10px;border-radius:12px;font-size:11px;font-family:monospace;margin-right:6px'>"
                f"MPLS {mpls}</span>"
            )
        if inn:
            chips_html += (
                f"<span style='background:rgba(167,139,250,.12);color:#a78bfa;border:1px solid rgba(167,139,250,.25);"
                f"padding:2px 10px;border-radius:12px;font-size:11px;font-family:monospace;margin-right:6px'>"
                f"INN {inn}</span>"
            )
        # Outros circuitos
        outros = [c for c in circuitos if c.get("des") not in (mpls, inn) and c.get("des")]
        for c in outros[:2]:
            chips_html += (
                f"<span style='background:rgba(34,211,238,.08);color:#22d3ee;border:1px solid rgba(34,211,238,.2);"
                f"padding:2px 10px;border-radius:12px;font-size:11px;font-family:monospace;margin-right:6px'>"
                f"{c.get('op','')} {c.get('des','')}</span>"
            )
        if chips_html:
            st.markdown(f"<div style='margin-bottom:6px'>{chips_html}</div>", unsafe_allow_html=True)

        # ── Detalhes expandíveis ─────────────────────────────────────────────
        with st.expander("Ver detalhes completos"):
            d1, d2, d3 = st.columns(3)

            with d1:
                st.markdown(
                    "<span style='font-family:monospace;font-size:10px;color:#5c6370;"
                    "text-transform:uppercase;letter-spacing:.1em'>📞 Contato</span>",
                    unsafe_allow_html=True,
                )
                if tel:   st.caption(f"Telefone: {tel}")
                if tel2:  st.caption(f"Telefone 2: {tel2}")
                if cel:   st.caption(f"Celular: {cel}")
                if email: st.caption(f"✉️ {email}")
                if horario:
                    st.markdown(
                        "<span style='font-family:monospace;font-size:10px;color:#5c6370;"
                        "text-transform:uppercase;letter-spacing:.1em'>🕐 Horário</span>",
                        unsafe_allow_html=True,
                    )
                    for h in horario.split(" | "):
                        st.caption(h)

            with d2:
                st.markdown(
                    "<span style='font-family:monospace;font-size:10px;color:#5c6370;"
                    "text-transform:uppercase;letter-spacing:.1em'>👥 Gestão</span>",
                    unsafe_allow_html=True,
                )
                if ggl:
                    st.caption(f"GGL: {ggl}")
                    if ggl_tel: st.caption(f"📱 {ggl_tel}")
                if gr:
                    st.caption(f"GR: {gr}")
                    if gr_tel: st.caption(f"📱 {gr_tel}")

            with d3:
                st.markdown(
                    "<span style='font-family:monospace;font-size:10px;color:#5c6370;"
                    "text-transform:uppercase;letter-spacing:.1em'>⚡ Ações</span>",
                    unsafe_allow_html=True,
                )
                favs = st.session_state.get("favoritos", [])
                is_fav = vd in favs
                btn_fav_label = "★ Remover" if is_fav else "☆ Favoritar"
                if st.button(btn_fav_label, key=f"fav_{vd}_{key_suffix}", use_container_width=True):
                    if is_fav:
                        st.session_state.favoritos.remove(vd)
                    elif len(favs) < 10:
                        st.session_state.favoritos.append(vd)
                    else:
                        st.warning("Limite de 10 favoritos atingido.")
                    st.rerun()

                if st.button("📞 Abrir Chamado", key=f"ch_{vd}_{key_suffix}", use_container_width=True):
                    st.session_state.loja_selecionada = loja
                    st.rerun()
