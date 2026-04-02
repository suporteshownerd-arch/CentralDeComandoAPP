"""
Módulo de componentes de UI
Central de Comando DPSP v2.0
"""

import streamlit as st
from typing import Optional, List, Dict


def render_vd_badge(vd: str) -> str:
    """Renderiza badge do VD"""
    return f'<span class="vd-badge">VD {vd}</span>'


def render_status_badge(status: str) -> str:
    """Renderiza badge de status (open/closed)"""
    if status == "open":
        return '<span class="status-open">● Aberta</span>'
    return '<span class="status-closed">● Fechada</span>'


def render_desig_pill(tipo: str, valor: str) -> str:
    """Renderiza pill de designação (MPLS/INN)"""
    if tipo.upper() == "MPLS":
        return f'<span class="desig-pill desig-mpls">MPLS {valor}</span>'
    return f'<span class="desig-pill desig-inn">INN {valor}</span>'


def render_card(
    title: str = None,
    content: str = None,
    footer: str = None,
    html: str = None
) -> str:
    """Renderiza um card premium"""
    if html:
        return f'<div class="card">{html}</div>'
    
    parts = []
    if title:
        parts.append(f'<h3 style="margin:0 0 12px 0;font-size:20px;">{title}</h3>')
    if content:
        parts.append(f'<div>{content}</div>')
    if footer:
        parts.append(f'<div style="margin-top:12px;color:var(--text3);font-size:12px;">{footer}</div>')
    
    return f'<div class="card">{"".join(parts)}</div>'


def render_info_section(title: str, rows: List[Dict[str, str]]) -> str:
    """Renderiza seção de informações com chave-valor"""
    rows_html = ""
    for row in rows:
        icon = row.get("icon", "")
        label = row.get("label", "")
        value = row.get("value", "")
        link = row.get("link", None)
        
        if link:
            value_html = f'<a href="{link}" target="_blank">{value}</a>'
        else:
            value_html = value
        
        rows_html += f'<div class="info-row">{icon} {label}: {value_html}</div>'
    
    return f'''
    <div class="info-section">
        <h4>{title}</h4>
        {rows_html}
    </div>
    '''


def render_template_box(label: str, tipo: str, conteudo: str) -> str:
    """Renderiza box de template de comunicação"""
    tipo_class = f"template-{tipo}"
    return f'''
    <div class="template-box">
        <div class="template-header">
            <span>{label}</span>
            <span class="template-type {tipo_class}">{tipo.upper()}</span>
        </div>
        <div class="template-content">{conteudo}</div>
    </div>
    '''


def render_kpi_card(label: str, value: str, delta: str = None, color: str = "var(--accent)") -> str:
    """Renderiza card de KPI"""
    delta_html = ""
    if delta:
        is_positive = not delta.startswith("-")
        color_delta = "var(--green)" if is_positive else "var(--red)"
        delta_html = f'<div style="color:{color_delta};font-size:12px;margin-top:4px;">{delta}</div>'
    
    return f'''
    <div class="kpi-card">
        <div class="kpi-value" style="color:{color}">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    '''


def render_sidebar_logo():
    """Renderiza logo na sidebar"""
    return '''
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="4" fill="white"/>
                <path d="M12 2V6M12 18V22M2 12H6M18 12H22" stroke="white" stroke-width="2" stroke-linecap="round"/>
            </svg>
        </div>
        <div>
            <div class="sidebar-logo-text">Central de Comando</div>
            <div class="sidebar-logo-sub">DPSP v2.0</div>
        </div>
    </div>
    '''


def render_status_indicator(label: str = "Sistema operacional") -> str:
    """Renderiza indicador de status"""
    return f'''
    <div class="status-indicator">
        <div class="status-dot"></div>
        <span style="color:var(--green);font-size:12px;font-family:monospace;">{label}</span>
    </div>
    '''


def render_contact_card(contatos: List[Dict[str, str]]) -> str:
    """Renderiza card de contatos"""
    items = ""
    for contato in contatos:
        items += f'<div class="contact-item">{contato["icon"]} {contato["label"]}: {contato["value"]}</div>'
    
    return f'<div class="contact-card">{items}</div>'


def render_alert_banner(titulo: str, mensagem: str, tipo: str = "error") -> str:
    """Renderiza banner de alerta"""
    return f'''
    <div class="alert-banner">
        <h4>🚨 {titulo}</h4>
        <p>{mensagem}</p>
    </div>
    '''


def render_suggestions_box(items: List[Dict]) -> str:
    """Renderiza caixa de sugestões"""
    if not items:
        return ""
    
    items_html = ""
    for item in items:
        items_html += f'''
        <div class="suggestion-item">
            <div class="suggestion-vd">VD {item.get('vd', '')}</div>
            <div class="suggestion-nome">{item.get('nome', '')}</div>
            <div class="suggestion-endereco">{item.get('endereco', '')}</div>
        </div>
        '''
    
    return f'<div class="suggestions-box">{items_html}</div>'


def render_faq_item(pergunta: str, resposta: str) -> str:
    """Renderiza item de FAQ"""
    return f'''
    <div class="faq-item">
        <div class="faq-question">{pergunta}</div>
        <div class="faq-answer">{resposta}</div>
    </div>
    '''


def render_loja_card(loja: dict, index: int) -> str:
    """Renderiza card completo de loja"""
    status_text = 'Aberta' if loja['status'] == 'open' else 'Fechada'
    
    mpls_pill = render_desig_pill("MPLS", loja.get("mpls", "N/A")) if loja.get('mpls') else ""
    inn_pill = render_desig_pill("INN", loja.get("inn", "N/A")) if loja.get('inn') else ""
    
    contato = render_info_section("Contato", [
        {"icon": "📞", "label": "Telefone", "value": loja.get('tel', 'N/A')},
        {"icon": "📱", "label": "WhatsApp", "value": loja.get('cel', 'N/A'), "link": f'https://wa.me/55{loja.get("cel", "").replace("-","").replace("(","").replace(")","")}'},
        {"icon": "✉️", "label": "Email", "value": loja.get('email', 'N/A')},
    ])
    
    horario = render_info_section("Horário & Gestão", [
        {"icon": "🕐", "label": "Horário", "value": loja.get('horario', 'N/A')},
        {"icon": "👤", "label": "GGL", "value": loja.get('ggl', 'N/A')},
        {"icon": "👤", "label": "GR", "value": loja.get('gr', 'N/A')},
    ])
    
    designacoes = render_info_section("Designações", [
        {"icon": "", "label": "MPLS", "value": loja.get('mpls', 'N/A')},
        {"icon": "", "label": "INN", "value": loja.get('inn', 'N/A')},
    ]) if mpls_pill or inn_pill else ""
    
    return f'''
    <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
            <div>
                {render_vd_badge(loja['vd'])}
                <h3 style="margin:16px 0 6px 0;font-size:22px;">{loja['nome']}</h3>
                <p style="color:var(--text2);font-size:14px">📍 {loja['endereco']} · {loja['cidade']} - {loja['estado']}</p>
            </div>
            {render_status_badge(loja['status'])}
        </div>
        <div class="info-grid">
            {contato}
            {horario}
            <div class="info-section">
                <h4>Designações</h4>
                <div>{mpls_pill} {inn_pill}</div>
            </div>
        </div>
    </div>
    '''


def render_progress_bar(label: str, value: int, total: int) -> str:
    """Renderiza barra de progresso com label"""
    pct = (value / total * 100) if total > 0 else 0
    return f'<div class="progress-container"><div class="progress-bar" style="width:{pct}%"></div><span class="progress-label">{label}: {value} ({pct:.1f}%)</span></div>'


def toast(message: str, icon: str = "✅"):
    """Exibe toast de notificação"""
    st.toast(f"{icon} {message}")


def success_toast(message: str):
    """Exibe toast de sucesso"""
    toast(message, "✅")


def error_toast(message: str):
    """Exibe toast de erro"""
    st.toast(f"❌ {message}")


def info_toast(message: str):
    """Exibe toast de informação"""
    toast(message, "ℹ️")