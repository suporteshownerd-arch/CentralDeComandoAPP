"""
Página de Dashboard
Central de Comando DPSP v4.1
"""

import streamlit as st

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

_DARK_BG    = "#0a0a0f"
_CARD_BG    = "#12121a"
_TEXT       = "#f0f0f5"
_TEXT2      = "#a0a0b0"
_ACCENT     = "#6366f1"
_GREEN      = "#10b981"
_RED        = "#ef4444"
_AMBER      = "#f59e0b"
_PURPLE     = "#a855f7"
_CYAN       = "#06b6d4"


def _pie(labels, values, title, colors):
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color=_CARD_BG, width=2)),
        textinfo="percent+label",
        textfont=dict(color=_TEXT, size=11),
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(color=_TEXT, size=14), x=0.5),
        paper_bgcolor=_CARD_BG, plot_bgcolor=_CARD_BG,
        legend=dict(font=dict(color=_TEXT2)),
        margin=dict(t=40, b=10, l=10, r=10),
        showlegend=False,
        height=260,
    )
    return fig


def _bar_h(labels, values, title, color=_ACCENT):
    fig = go.Figure(go.Bar(
        x=values, y=labels,
        orientation="h",
        marker=dict(color=color, line=dict(color="rgba(0,0,0,0)")),
        text=values, textposition="outside",
        textfont=dict(color=_TEXT2, size=11),
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(color=_TEXT, size=14), x=0),
        paper_bgcolor=_CARD_BG, plot_bgcolor=_CARD_BG,
        xaxis=dict(showgrid=False, showticklabels=False, color=_TEXT2),
        yaxis=dict(tickfont=dict(color=_TEXT, size=11), autorange="reversed"),
        margin=dict(t=40, b=10, l=10, r=40),
        height=max(220, len(labels) * 30 + 60),
    )
    return fig


def render_page(_data_loader, lojas):
    st.markdown(
        """
        <div class="page-header">
            <div class="page-header-icon">📈</div>
            <div>
                <h2 class="page-title">Dashboard</h2>
                <p class="page-sub">Visão geral do parque de lojas DPSP</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not lojas:
        st.warning("Sem dados de lojas para exibir.")
        return

    # ── KPIs melhorados ────────────────────────────────────────────────────────
    total    = len(lojas)
    ativas   = sum(1 for l in lojas if l.get("status") == "open")
    inativas = total - ativas
    estados  = len({l.get("estado") for l in lojas if l.get("estado")})
    regioes  = len({l.get("regiao") for l in lojas if l.get("regiao")})
    
    # KPIs adicionais
    com_mpls = sum(1 for l in lojas if l.get("mpls"))
    com_inn  = sum(1 for l in lojas if l.get("inn"))
    com_circ = com_mpls + com_inn
    
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("🏪 Total",        f"{total:,}")
    k2.metric("🟢 Ativas",      ativas,   delta=f"{round(ativas/total*100)}%" if total else None)
    k3.metric("🔴 Inativas",    inativas, delta=f"-{round(inativas/total*100)}%" if total else None, delta_color="inverse")
    k4.metric("🗺️ Estados",     estados)
    k5.metric("🗺 Regiões",     regioes)
    k6.metric("🌐 Circuits",    com_circ, delta=f"{round(com_circ/total*100)}%" if total else None)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Gráficos ──────────────────────────────────────────────────────────────
    if not PLOTLY_OK:
        st.info("Instale `plotly` para visualizar os gráficos: `pip install plotly`")
        _tabela_fallback(lojas)
        return

    col_pie, col_bar = st.columns([1, 2])

    # Pie: Ativas vs Inativas
    with col_pie:
        fig_pie = _pie(
            labels=["Ativas", "Inativas"],
            values=[ativas, inativas],
            title="Status das Lojas",
            colors=[_GREEN, _RED],
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Bar: Lojas por Estado (top 15)
    with col_bar:
        estados_cnt: dict = {}
        for l in lojas:
            e = l.get("estado", "Outro")
            if e:
                estados_cnt[e] = estados_cnt.get(e, 0) + 1
        top_estados = sorted(estados_cnt.items(), key=lambda x: x[1], reverse=True)[:15]
        if top_estados:
            labs, vals = zip(*top_estados)
            fig_bar = _bar_h(list(labs), list(vals), "Lojas por Estado (Top 15)")
            st.plotly_chart(fig_bar, use_container_width=True)

    # Bar: Lojas por Região
    regioes_cnt: dict = {}
    for l in lojas:
        r = l.get("regiao", "")
        if r:
            regioes_cnt[r] = regioes_cnt.get(r, 0) + 1

    if regioes_cnt:
        st.markdown("#### Lojas por Região")
        top_reg = sorted(regioes_cnt.items(), key=lambda x: x[1], reverse=True)
        rl, rv = zip(*top_reg)
        colors = [_ACCENT, _PURPLE, _GREEN, _AMBER, _RED]
        fig_reg = _bar_h(list(rl), list(rv), "", color=[colors[i % len(colors)] for i in range(len(rl))])
        st.plotly_chart(fig_reg, use_container_width=True)

    # ── Tabela de lojas inativas ──────────────────────────────────────────────
    inativas_list = [l for l in lojas if l.get("status") == "closed"]
    if inativas_list:
        st.markdown(
            f"<div style='font-family:DM Mono,monospace;font-size:10px;color:#5c6370;"
            f"text-transform:uppercase;letter-spacing:.14em;margin:24px 0 10px 0'>"
            f"🔴 Lojas Inativas · {len(inativas_list)}</div>",
            unsafe_allow_html=True,
        )
        rows = [
            {
                "VD":       l.get("vd", ""),
                "Nome":     l.get("nome", ""),
                "Cidade":   l.get("cidade", ""),
                "Estado":   l.get("estado", ""),
                "Região":   l.get("regiao", ""),
            }
            for l in inativas_list
        ]
        st.dataframe(rows, use_container_width=True, hide_index=True)


def _tabela_fallback(lojas):
    """Exibe distribuição por estado como tabela quando Plotly não está disponível."""
    estados_cnt: dict = {}
    for l in lojas:
        e = l.get("estado", "Outro")
        if e:
            estados_cnt[e] = estados_cnt.get(e, 0) + 1
    st.markdown("#### Lojas por Estado")
    for estado, count in sorted(estados_cnt.items(), key=lambda x: x[1], reverse=True):
        st.write(f"**{estado}**: {count}")
