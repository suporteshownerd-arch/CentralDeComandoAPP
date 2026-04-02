"""
Módulo de navegação e sidebar
Central de Comando DPSP v3.0
"""

import streamlit as st
from typing import List


_MENU = [
    ("🏪", "Consulta de Lojas"),
    ("🚨", "Gestão de Crises"),
    ("📞", "Abertura de Chamados"),
    ("📋", "Histórico"),
    ("📈", "Dashboard"),
    ("❓", "Ajuda"),
]


def render_sidebar(lojas: List[dict], favoritos: List[str], **_) -> str:
    """
    Renderiza a sidebar e retorna o nome da página selecionada.
    """
    total   = len(lojas) if lojas else 0
    ativas  = sum(1 for l in lojas if l.get("status") == "open") if lojas else 0
    pct_ativas = round(ativas / total * 100) if total else 0

    # ── Logo ─────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="padding:20px 4px 12px 4px">
            <div style="display:flex;align-items:center;gap:12px">
                <div style="width:40px;height:40px;background:linear-gradient(135deg,#5b8def,#7c3aed);
                            border-radius:12px;display:flex;align-items:center;justify-content:center;
                            font-size:20px;flex-shrink:0">🛡️</div>
                <div>
                    <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;
                                color:#eaecf0;line-height:1.2">Central de Comando</div>
                    <div style="font-family:'DM Mono',monospace;font-size:10px;color:#5c6370;
                                letter-spacing:.05em">DPSP T.I. · v3.0</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Status online ─────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;
                    background:rgba(52,211,153,.08);border:1px solid rgba(52,211,153,.2);
                    border-radius:10px;margin-bottom:4px">
            <div style="width:7px;height:7px;background:#34d399;border-radius:50%;
                        animation:pulse 2s infinite"></div>
            <span style="font-size:12px;color:#34d399;font-weight:600">Sistema Operacional</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='margin:16px 0 8px 0;border-top:1px solid rgba(255,255,255,.06)'></div>",
                unsafe_allow_html=True)

    # ── KPIs das lojas ────────────────────────────────────────────────────────
    st.markdown(
        "<p style='font-family:DM Mono,monospace;font-size:10px;color:#5c6370;"
        "text-transform:uppercase;letter-spacing:.12em;margin:0 0 8px 2px'>Parque de Lojas</p>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""<div style="background:#0f1118;border:1px solid rgba(255,255,255,.06);
                border-radius:12px;padding:12px;text-align:center">
                <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:700;
                            color:#5b8def">{total:,}</div>
                <div style="font-family:'DM Mono',monospace;font-size:10px;color:#5c6370;
                            text-transform:uppercase;margin-top:2px">Total</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div style="background:#0f1118;border:1px solid rgba(255,255,255,.06);
                border-radius:12px;padding:12px;text-align:center">
                <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:700;
                            color:#34d399">{ativas:,}</div>
                <div style="font-family:'DM Mono',monospace;font-size:10px;color:#5c6370;
                            text-transform:uppercase;margin-top:2px">Ativas</div>
            </div>""",
            unsafe_allow_html=True,
        )

    # Barra de progresso ativas/inativas
    st.markdown(
        f"""<div style="margin:10px 0 4px 0">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="font-size:11px;color:#34d399">● Ativas {pct_ativas}%</span>
                <span style="font-size:11px;color:#f87171">● Inativas {100-pct_ativas}%</span>
            </div>
            <div style="background:rgba(248,113,113,.25);border-radius:4px;height:6px">
                <div style="background:#34d399;width:{pct_ativas}%;height:6px;border-radius:4px;
                            transition:width .5s"></div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("<div style='margin:16px 0 8px 0;border-top:1px solid rgba(255,255,255,.06)'></div>",
                unsafe_allow_html=True)

    # ── Navegação ─────────────────────────────────────────────────────────────
    st.markdown(
        "<p style='font-family:DM Mono,monospace;font-size:10px;color:#5c6370;"
        "text-transform:uppercase;letter-spacing:.12em;margin:0 0 8px 2px'>Navegação</p>",
        unsafe_allow_html=True,
    )

    menu_labels = [f"{icon} {nome}" for icon, nome in _MENU]
    escolha = st.radio("nav", menu_labels, label_visibility="collapsed")
    pagina = escolha.split(" ", 1)[1] if " " in escolha else escolha

    st.markdown("<div style='margin:16px 0 8px 0;border-top:1px solid rgba(255,255,255,.06)'></div>",
                unsafe_allow_html=True)

    # ── Favoritos ─────────────────────────────────────────────────────────────
    if favoritos:
        st.markdown(
            "<p style='font-family:DM Mono,monospace;font-size:10px;color:#5c6370;"
            "text-transform:uppercase;letter-spacing:.12em;margin:0 0 8px 2px'>⭐ Favoritos</p>",
            unsafe_allow_html=True,
        )
        # Montar lookup de nomes
        idx = {l.get("vd"): l.get("nome", "") for l in lojas} if lojas else {}
        for vd in favoritos[:5]:
            nome = idx.get(vd, f"VD {vd}")
            nome_curto = nome[:22] + "…" if len(nome) > 22 else nome
            st.markdown(
                f"""<div style="display:flex;align-items:center;gap:8px;padding:6px 10px;
                    background:rgba(91,141,239,.06);border-radius:8px;margin-bottom:4px;cursor:pointer">
                    <span style="font-family:'DM Mono',monospace;font-size:11px;color:#5b8def;
                                 background:rgba(91,141,239,.15);padding:1px 6px;border-radius:4px">
                        {vd}</span>
                    <span style="font-size:12px;color:#9094a6">{nome_curto}</span>
                </div>""",
                unsafe_allow_html=True,
            )
        st.markdown("<div style='margin:12px 0 8px 0;border-top:1px solid rgba(255,255,255,.06)'></div>",
                    unsafe_allow_html=True)

    # ── Contatos ──────────────────────────────────────────────────────────────
    st.markdown(
        "<p style='font-family:DM Mono,monospace;font-size:10px;color:#5c6370;"
        "text-transform:uppercase;letter-spacing:.12em;margin:0 0 8px 2px'>Contatos</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div style="background:#0f1118;border:1px solid rgba(255,255,255,.06);
                border-radius:10px;padding:10px 12px">
            <div style="font-size:12px;color:#9094a6;margin-bottom:6px">
                🎛️ <b style="color:#eaecf0">Central</b> · (11) 3274-7527
            </div>
            <div style="font-size:12px;color:#9094a6">
                💻 <b style="color:#eaecf0">T.I. DPSP</b> · (11) 5529-6003
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    return pagina


def render_page_header(title: str, subtitle: str = None, icon: str = None):
    if icon:
        title = f"{icon} {title}"
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")


def render_footer():
    st.markdown(
        """<div class="footer">
            <b>🛡️ Central de Comando DPSP v3.0</b><br>
            Desenvolvido por Enzo Maranho — T.I. DPSP · Uso Interno
        </div>""",
        unsafe_allow_html=True,
    )


def init_session_state():
    defaults = {
        "loja_selecionada": None,
        "nome_atendente": "",
        "favoritos": [],
        "consulta_pagina": 1,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def setup_page_config():
    st.set_page_config(
        page_title="Central de Comando — DPSP",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
