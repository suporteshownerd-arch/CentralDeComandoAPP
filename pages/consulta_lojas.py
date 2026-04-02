"""
Página de Consulta de Lojas
Central de Comando DPSP v3.0
"""

import streamlit as st

_POR_PAGINA = 10


def render_page(data_loader, lojas):
    st.markdown("## 🏪 Consulta de Lojas")
    st.markdown("*Busque informações completas de qualquer loja do parque DPSP*")

    # ── Barra de busca ────────────────────────────────────────────────────────
    col_busca, col_modo = st.columns([3, 1])
    with col_busca:
        termo = st.text_input(
            "Buscar",
            placeholder="VD, nome, cidade, designação MPLS/INN...",
            key="consulta_termo",
        )
    with col_modo:
        modo = st.selectbox(
            "Modo",
            ["VD / Designação", "Nome de Loja", "Endereço", "Outra Informação"],
            key="consulta_modo",
        )

    # ── Filtros ───────────────────────────────────────────────────────────────
    with st.expander("🔽 Filtros avançados", expanded=False):
        fcol1, fcol2, fcol3 = st.columns(3)
        with fcol1:
            estados = ["Todos"] + data_loader.get_estados()
            filtro_estado = st.selectbox("Estado", estados, key="f_estado")
        with fcol2:
            regioes = ["Todas"] + data_loader.get_regioes()
            filtro_regiao = st.selectbox("Região", regioes, key="f_regiao")
        with fcol3:
            filtro_status = st.selectbox("Status", ["Todos", "Ativa", "Inativa"], key="f_status")

    # ── Aplicar busca e filtros ───────────────────────────────────────────────
    if termo:
        resultados = data_loader.buscar_loja(termo, modo, lojas)
    else:
        resultados = list(lojas)

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
                _render_loja_card(loja, key_suffix="fav")
            st.markdown("---")

    # ── Contagem e paginação ──────────────────────────────────────────────────
    total = len(resultados)
    st.markdown(f"**{total} loja(s) encontrada(s)**")

    if total == 0:
        if termo:
            st.info(f"Nenhuma loja encontrada para **{termo}**. Tente outro termo ou modo de busca.")
        return

    # Controle de página
    paginas = max(1, -(-total // _POR_PAGINA))  # ceil division
    if "consulta_pagina" not in st.session_state:
        st.session_state.consulta_pagina = 1
    # Resetar página ao mudar busca
    if st.session_state.get("_ultimo_termo") != termo or st.session_state.get("_ultimo_modo") != modo:
        st.session_state.consulta_pagina = 1
        st.session_state["_ultimo_termo"] = termo
        st.session_state["_ultimo_modo"] = modo

    pagina_atual = st.session_state.consulta_pagina
    inicio = (pagina_atual - 1) * _POR_PAGINA
    fim = inicio + _POR_PAGINA
    pagina_lojas = resultados[inicio:fim]

    # ── Cards de resultado ────────────────────────────────────────────────────
    for i, loja in enumerate(pagina_lojas):
        _render_loja_card(loja, key_suffix=f"res_{inicio + i}")

    # ── Navegação de páginas ──────────────────────────────────────────────────
    if paginas > 1:
        st.markdown("---")
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if pagina_atual > 1:
                if st.button("← Anterior"):
                    st.session_state.consulta_pagina -= 1
                    st.rerun()
        with nav2:
            st.markdown(
                f"<div style='text-align:center;color:#9094a6'>Página {pagina_atual} de {paginas}</div>",
                unsafe_allow_html=True,
            )
        with nav3:
            if pagina_atual < paginas:
                if st.button("Próxima →"):
                    st.session_state.consulta_pagina += 1
                    st.rerun()


def _render_loja_card(loja: dict, key_suffix: str = ""):
    vd     = loja.get("vd", "N/A")
    nome   = loja.get("nome", "N/A")
    end    = loja.get("endereco", "")
    cidade = loja.get("cidade", "")
    estado = loja.get("estado", "")
    status = loja.get("status", "open")
    mpls   = loja.get("mpls", "")
    inn    = loja.get("inn", "")
    ggl    = loja.get("ggl", "")
    ggl_tel = loja.get("ggl_tel", "")
    gr     = loja.get("gr", "")
    gr_tel = loja.get("gr_tel", "")
    tel    = loja.get("tel", "")
    cel    = loja.get("cel", "")
    horario = loja.get("horario", "")

    status_icon  = "🟢" if status == "open" else "🔴"
    status_label = "Ativa" if status == "open" else "Inativa"

    with st.container(border=True):
        # Cabeçalho do card
        h1, h2 = st.columns([4, 1])
        with h1:
            st.markdown(
                f"<span style='font-family:monospace;background:rgba(91,141,239,.18);"
                f"color:#5b8def;padding:2px 8px;border-radius:6px;font-size:13px'>VD {vd}</span>"
                f"&nbsp;&nbsp;<strong style='font-size:16px'>{nome}</strong>",
                unsafe_allow_html=True,
            )
        with h2:
            st.markdown(
                f"<div style='text-align:right'>{status_icon} {status_label}</div>",
                unsafe_allow_html=True,
            )

        # Endereço
        if end or cidade:
            st.caption(f"📍 {end}{', ' if end and cidade else ''}{cidade}/{estado}")

        # Chips de designação
        chips = []
        if mpls:
            chips.append(f"<span style='background:rgba(52,211,153,.15);color:#34d399;padding:2px 8px;border-radius:12px;font-size:11px;font-family:monospace'>MPLS {mpls}</span>")
        if inn:
            chips.append(f"<span style='background:rgba(167,139,250,.15);color:#a78bfa;padding:2px 8px;border-radius:12px;font-size:11px;font-family:monospace'>INN {inn}</span>")
        if chips:
            st.markdown(" ".join(chips), unsafe_allow_html=True)

        # Detalhes expandíveis
        with st.expander("Ver detalhes"):
            dcol1, dcol2, dcol3 = st.columns(3)
            with dcol1:
                st.markdown("**Contato da Loja**")
                if tel:    st.caption(f"📞 {tel}")
                if cel:    st.caption(f"📱 {cel}")
                if horario: st.caption(f"🕐 {horario}")
            with dcol2:
                st.markdown("**Gerência**")
                if ggl:    st.caption(f"👤 GGL: {ggl}")
                if ggl_tel: st.caption(f"📞 {ggl_tel}")
                if gr:     st.caption(f"👤 GR: {gr}")
                if gr_tel: st.caption(f"📞 {gr_tel}")
            with dcol3:
                st.markdown("**Ações**")
                # Favoritar
                favs = st.session_state.get("favoritos", [])
                is_fav = vd in favs
                if st.button(
                    "★ Remover favorito" if is_fav else "☆ Favoritar",
                    key=f"fav_{vd}_{key_suffix}",
                ):
                    if is_fav:
                        st.session_state.favoritos.remove(vd)
                    else:
                        if len(favs) < 10:
                            st.session_state.favoritos.append(vd)
                        else:
                            st.warning("Limite de 10 favoritos atingido.")
                    st.rerun()

                # Atalho para abertura de chamado
                if st.button("📞 Abrir Chamado", key=f"ch_{vd}_{key_suffix}"):
                    st.session_state.loja_selecionada = loja
                    st.session_state.pagina_ativa = "Abertura de Chamados"
                    st.rerun()
