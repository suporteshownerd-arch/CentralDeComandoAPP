"""
Módulo de tratamento de erros
Central de Comando DPSP v4.2
"""

import streamlit as st
import traceback
import logging
from datetime import datetime
from typing import Optional, Callable
from functools import wraps


logger = logging.getLogger(__name__)


class ErrorHandler:
    """Handler centralizado para erros"""
    
    @staticmethod
    def show_error(title: str, message: str, details: str = None):
        """Exibe erro formatado"""
        st.error(f"**{title}**")
        st.markdown(message)
        if details:
            with st.expander("🔍 Detalhes técnicos"):
                st.code(details, language="text")
    
    @staticmethod
    def show_warning(title: str, message: str):
        """Exibe aviso formatado"""
        st.warning(f"**{title}**\n\n{message}")
    
    @staticmethod
    def show_info(title: str, message: str):
        """Exibe info formatado"""
        st.info(f"**{title}**\n\n{message}")
    
    @staticmethod
    def log_error(error: Exception, context: str = ""):
        """Registra erro no log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        trace = traceback.format_exc()
        log_msg = f"[{timestamp}] {context}: {str(error)}\n{trace}"
        logger.error(log_msg)
        
        if "error_log" not in st.session_state:
            st.session_state.error_log = []
        
        st.session_state.error_log.append({
            "timestamp": timestamp,
            "error": str(error),
            "context": context,
            "trace": trace
        })
        
        if len(st.session_state.error_log) > 10:
            st.session_state.error_log = st.session_state.error_log[-10:]


def handle_errors(title: str = "Erro inesperado", show_trace: bool = False):
    """Decorador para tratar erros em funções"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ErrorHandler.log_error(e, context=func.__name__)
                ErrorHandler.show_error(
                    title=title,
                    message=f"Ocorreu um erro ao executar esta ação: **{str(e)}**",
                    details=traceback.format_exc() if show_trace else None
                )
                return None
        return wrapper
    return decorator


def render_error_page(error_type: str = "generic"):
    """Renderiza página de erro customizada"""
    error_configs = {
        "no_data": {
            "icon": "📊",
            "title": "Sem dados disponíveis",
            "message": "Não foi possível carregar os dados necessários.",
            "suggestion": "Verifique se os arquivos de dados estão disponíveis."
        },
        "connection": {
            "icon": "🌐",
            "title": "Erro de conexão",
            "message": "Não foi possível conectar ao servidor.",
            "suggestion": "Verifique sua conexão com a internet e tente novamente."
        },
        "permission": {
            "icon": "🔒",
            "title": "Acesso negado",
            "message": "Você não tem permissão para acessar este recurso.",
            "suggestion": "Entre em contato com o administrador."
        },
        "not_found": {
            "icon": "🔍",
            "title": "Não encontrado",
            "message": "O recurso solicitado não foi encontrado.",
            "suggestion": "Verifique se o link está correto."
        },
        "generic": {
            "icon": "⚠️",
            "title": "Algo deu errado",
            "message": "Ocorreu um erro inesperado.",
            "suggestion": "Tente novamente ou entre em contato com o suporte."
        }
    }
    
    config = error_configs.get(error_type, error_configs["generic"])
    
    st.markdown(
        f"""
        <div class="error-page">
            <div class="error-icon">{config['icon']}</div>
            <h2 class="error-title">{config['title']}</h2>
            <p class="error-message">{config['message']}</p>
            <p class="error-suggestion">{config['suggestion']}</p>
            <button class="error-button" onclick="window.location.reload()">
                🔄 Tentar novamente
            </button>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_loading_spinner(message: str = "Carregando..."):
    """Renderiza spinner de carregamento"""
    return st.spinner(f"⏳ {message}")


def render_empty_state(
    icon: str = "📭",
    title: str = "Nenhum dado encontrado",
    message: str = "Tente ajustar seus filtros ou busca.",
    action_label: str = None,
    action_callback: Callable = None
):
    """Renderiza estado vazio"""
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-icon">{icon}</div>
            <h3 class="empty-title">{title}</h3>
            <p class="empty-message">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if action_label and action_callback:
        if st.button(action_label, key="empty_action"):
            action_callback()


def render_error_banner(message: str, error_type: str = "error"):
    """Renderiza banner de erro flutuante"""
    colors = {
        "error": ("#ef4444", "rgba(239,68,68,0.15)"),
        "warning": ("#f59e0b", "rgba(245,158,11,0.15)"),
        "success": ("#10b981", "rgba(16,185,129,0.15)"),
        "info": ("#6366f1", "rgba(99,102,241,0.15)")
    }
    color, bg = colors.get(error_type, colors["error"])
    
    st.markdown(
        f"""
        <div class="error-banner" style="background:{bg};border-left:4px solid {color}">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )