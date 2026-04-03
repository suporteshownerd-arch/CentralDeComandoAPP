"""
Componentes reutilizáveis - Central de Comando DPSP v4.2
"""

from .styles import (
    get_base_css,
    get_responsive_css,
    get_animations_css,
    get_component_css,
    get_full_css,
    render_styles,
    Colors,
    Fonts,
    Spacing,
    BorderRadius
)

from .ui import (
    render_vd_badge,
    render_status_badge,
    render_desig_pill,
    render_card,
    render_info_section,
    render_template_box,
    render_kpi_card,
    render_sidebar_logo,
    render_status_indicator,
    render_contact_card,
    render_alert_banner,
    render_suggestions_box,
    render_faq_item,
    render_loja_card,
    render_progress_bar,
    toast,
    success_toast,
    error_toast,
    info_toast
)

from .nav import (
    render_sidebar,
    render_page_header,
    render_footer,
    init_session_state,
    setup_page_config
)

from .error_handler import (
    ErrorHandler,
    handle_errors,
    render_error_page,
    render_empty_state,
    render_loading_spinner,
    render_error_banner
)

__all__ = [
    # Styles
    'get_base_css',
    'get_responsive_css',
    'get_animations_css',
    'get_component_css',
    'get_full_css',
    'render_styles',
    'Colors',
    'Fonts',
    'Spacing',
    'BorderRadius',
    # UI
    'render_vd_badge',
    'render_status_badge',
    'render_desig_pill',
    'render_card',
    'render_info_section',
    'render_template_box',
    'render_kpi_card',
    'render_sidebar_logo',
    'render_status_indicator',
    'render_contact_card',
    'render_alert_badge',
    'render_alert_banner',
    'render_suggestions_box',
    'render_faq_item',
    'render_loja_card',
    'render_progress_bar',
    'toast',
    'success_toast',
    'error_toast',
    'info_toast',
    # Nav
    'render_sidebar',
    'render_page_header',
    'render_footer',
    'init_session_state',
    'setup_page_config',
    # Error Handler
    'ErrorHandler',
    'handle_errors',
    'render_error_page',
    'render_empty_state',
    'render_loading_spinner',
    'render_error_banner'
]