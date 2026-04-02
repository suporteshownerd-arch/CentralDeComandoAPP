"""
Páginas do sistema - Central de Comando DPSP v2.0
"""

from .consulta_lojas import render_page as render_consulta_lojas
from .gestao_crises import render_page as render_gestao_crises
from .historico import render_page as render_historico
from .abertura_chamados import render_page as render_abertura_chamados
from .dashboard import render_page as render_dashboard
from .ajuda import render_page as render_ajuda

__all__ = [
    'render_consulta_lojas',
    'render_gestao_crises',
    'render_historico',
    'render_abertura_chamados',
    'render_dashboard',
    'render_ajuda'
]