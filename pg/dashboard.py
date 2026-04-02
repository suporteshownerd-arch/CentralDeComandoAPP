"""
Página de Dashboard
Central de Comando DPSP v3.0
"""

import streamlit as st

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

_DARK_BG    = "#08090d"
_CARD_BG    = "#0f1118"
_TEXT       = "#eaecf0"
_TEXT2      = "#9094a6"
_ACCENT     = "#5b8def"
_GREEN      = "#34d399"
_RED        = "#f87171"
_AMBER      = "#fbbf24"
_PURPLE     = "#a78bfa"


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
    st.markdown("## 📈 Dashboard")
    st.markdown("*Visão geral das operações DPSP*")

    if not lojas:
        st.warning("Sem dados de lojas para exibir.")
        return

    # ── KPIs ──────────────────────────────────────────────────────────────────
    total    = len(lojas)
    ativas   = sum(1 for l in lojas if l.get("status") == "open")
    inativas = total - ativas
    estados  = len({l.get("estado") for l in lojas if l.get("estado")})
    regioes  = len({l.get("regiao") for l in lojas if l.get("regiao")})

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total de Lojas",   total)
    k2.metric("Lojas Ativas",     ativas,   delta=f"{round(ativas/total*100)}%" if total else None)
    k3.metric("Lojas Inativas",   inativas, delta=f"-{round(inativas/total*100)}%" if total else None, delta_color="inverse")
    k4.metric("Estados",          estados)
    k5.metric("Regiões",          regioes)

    st.markdown("---")

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
        st.markdown("---")
        st.markdown(f"#### 🔴 Lojas Inativas ({len(inativas_list)})")
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
