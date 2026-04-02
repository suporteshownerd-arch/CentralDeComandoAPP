"""
Módulo de templates para geração de comunicados
Desenvolvido por Enzo Maranho - T.I. DPSP
"""

from datetime import datetime


def gerar_alerta_executivo(
    escopo: str,
    identificacao: str,
    inicio: datetime,
    termino: datetime,
    abrangencia: str,
    equipes: str,
    status: str,
    gerar_abertura: bool = True,
    gerar_atualizacao: bool = False,
    gerar_normalizacao: bool = False
) -> list:
    """
    Gera templates de Alertas Executivos
    
    Args:
        escopo: Escopo da crise
        identificacao: Tipo de identificação
        inicio: Horário de início
        termino: Horário de término (opcional)
        abrangência: Abrangência do incidente
        equipes: Equipes acionadas
        status: Status atual
        gerar_abertura: Gerar template de abertura
        gerar_atualizacao: Gerar template de atualização
        gerar_normalizacao: Gerar template de normalização
    
    Returns:
        Lista de templates gerados
    """
    templates = []
    agora = datetime.now().strftime("%H:%M")
    
    inicio_str = inicio.strftime("%H:%M") if inicio else "--:--"
    termino_str = termino.strftime("%H:%M") if termino else "Sem previsão"
    
    if gerar_abertura:
        templates.append({
            "tipo": "abertura",
            "label": "🔴 ABERTURA",
            "texto": f"""🔴 *ABERTURA DE INCIDENTE — {escopo.upper()}*

*Escopo:* {escopo}
*Identificação:* {identificacao}
*Início:* {inicio_str}
*Previsão de retorno:* {termino_str}
*Abrangência:* {abrangencia}
*Equipes:* {equipes}

*Status:* {status}

_Central de Comando — T.I. DPSP_
_{agora}_"""
        })
    
    if gerar_atualizacao:
        templates.append({
            "tipo": "atualizacao",
            "label": "🟡 ATUALIZAÇÃO",
            "texto": f"""🟡 *ATUALIZAÇÃO — {escopo.upper()}*

*Escopo:* {escopo}
*Início:* {inicio_str}
*Abrangência:* {abrangencia}
*Equipes:* {equipes}

*Status atual:* {status}
*Próxima atualização:* Em 30 minutos

_Central de Comando — T.I. DPSP_
_{agora}_"""
        })
    
    if gerar_normalizacao:
        templates.append({
            "tipo": "normalizacao",
            "label": "🟢 NORMALIZAÇÃO",
            "texto": f"""🟢 *NORMALIZAÇÃO — {escopo.upper()}*

*Escopo:* {escopo}
*Início:* {inicio_str}
*Término:* {agora}
*Abrangência:* {abrangencia}
*Equipes:* {equipes}

*Resolução:* Serviço normalizado. {status}

_Central de Comando — T.I. DPSP_
_{agora}_"""
        })
    
    return templates


def gerar_gestao_crise(
    num_incidente: str,
    link_sala: str,
    unidades: str,
    causa: str,
    responsavel_tecnico: str,
    responsavel_command: str,
    hora_incidente: datetime,
    hora_acionamento: datetime,
    atualizacao: str,
    contador: int = 1,
    gerar_abertura: bool = True,
    gerar_normalizacao: bool = False
) -> list:
    """
    Gera templates de Gestão de Crise
    
    Args:
        num_incidente: Número do incidente
        link_sala: Link da sala de crise
        unidades: Unidades impactadas
        causa: Causa do incidente
        responsavel_tecnico: Responsável técnico
        responsavel_command: Responsável da Central
        hora_incidente: Horário do incidente
        hora_acionamento: Horário de acionamento
        atualizacao: Texto de atualização
        contador: Número de atualizações
        gerar_abertura: Gerar template de abertura
        gerar_normalizacao: Gerar template de normalização
    
    Returns:
        Lista de templates gerados
    """
    templates = []
    agora = datetime.now().strftime("%H:%M")
    
    h_inc = hora_incidente.strftime("%H:%M") if hora_incidente else "--:--"
    h_acion = hora_acionamento.strftime("%H:%M") if hora_acionamento else "--:--"
    
    if gerar_abertura:
        templates.append({
            "tipo": "abertura",
            "label": "🔴 ABERTURA",
            "texto": f"""🔴 *GESTÃO DE CRISE — {num_incidente}*

*Sala de Crise:* {link_sala}

*Unidades impactadas:* {unidades}
*Causa:* {causa}

*Responsável Técnico:* {responsavel_tecnico}
*Responsável Command:* {responsavel_command}

*Horário do incidente:* {h_inc}
*Horário de acionamento:* {h_acion}

*Atualização #: {contador}*
*Status atual:* {atualizacao}

*Próximo status:* {agora} (+30min)

_Central de Comando — T.I. DPSP_"""
        })
    
    if gerar_normalizacao:
        templates.append({
            "tipo": "normalizacao",
            "label": "🟢 NORMALIZAÇÃO",
            "texto": f"""🟢 *NORMALIZAÇÃO — {num_incidente}*

*Sala de Crise:* {link_sala}

*Unidades afetadas:* {unidades}
*Causa raiz identificada:* {causa}

*Responsável Técnico:* {responsavel_tecnico}
*Responsável Command:* {responsavel_command}

*Total de atualizações:* {contador}
*Início:* {h_inc} | *Acionamento:* {h_acion} | *Encerramento:* {agora}

*Resolução:* {atualizacao}

_Central de Comando — T.I. DPSP_"""
        })
    
    return templates


def gerar_loja_isolada(
    vd: str,
    tipo: str,
    hora_inicio: datetime,
    hora_retorno: datetime,
    lojas: list
) -> list:
    """
    Gera templates de Loja Isolada
    
    Args:
        vd: VD da loja
        tipo: Tipo de isolamento (energia/internet)
        hora_inicio: Horário de início
        hora_retorno: Horário de retorno previsto
        lojas: Lista de lojas para buscar nome
    
    Returns:
        Lista de templates gerados
    """
    templates = []
    
    # Buscar nome da loja
    nome_loja = f"Loja VD {vd}"
    for loja in lojas:
        if loja.get("vd") == vd:
            nome_loja = loja.get("nome", nome_loja)
            break
    
    inicio_str = hora_inicio.strftime("%H:%M") if hora_inicio else "--:--"
    retorno_str = hora_retorno.strftime("%H:%M") if hora_retorno else "Sem previsão"
    
    label = "ENERGIA ELÉTRICA" if tipo == "energia" else "INTERNET / CONECTIVIDADE"
    emoji = "⚡" if tipo == "energia" else "📡"
    
    # Template Abertura
    templates.append({
        "tipo": "abertura",
        "label": f"{emoji} ISOLA {label} — ABERTURA",
        "texto": f"""{emoji} *ISOLA {label}*

VD {vd} - {nome_loja}

*Tipo:* {label}
*Início:* {inicio_str}
*Previsão de retorno:* {retorno_str}

_Loja sem {'energia elétrica' if tipo == 'energia' else 'conectividade de internet'}. Equipe acionada._

_Central de Comando — T.I. DPSP_"""
    })
    
    # Template Fechamento/Retorno
    templates.append({
        "tipo": "fechamento",
        "label": f"✅ RETORNA {label} — FECHAMENTO",
        "texto": f"""✅ *RETORNA {label}*

VD {vd} - {nome_loja}

*Tipo:* {label}
*Início do incidente:* {inicio_str}
*Retorno:* {retorno_str}

_Loja normalizada. {'Energia elétrica restabelecida.' if tipo == 'energia' else 'Conectividade restabelecida.'}_

_Central de Comando — T.I. DPSP_"""
    })
    
    return templates


def gerar_email_tecnico(loja: dict, nome_atendente: str = "Central de Comando") -> str:
    """
    Gera e-mail formatado para técnicos de campo
    
    Args:
        loja: Dados da loja
        nome_atendente: Nome do atendente
    
    Returns:
        Texto do e-mail formatado
    """
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    return f"""To: {loja.get('email', '')}
CC: {loja.get('ggl', '')} <{loja.get('ggl_tel', '')}@dpsp.com.br>, {loja.get('gr', '')} <{loja.get('gr_tel', '')}@dpsp.com.br>
Subject: [DPSP] Técnico em campo - VD {loja.get('vd')} - {loja.get('nome')}

Prezados,

Segue abaixo as informações da loja para atendimento técnico:

═══════════════════════════════════════════════════════
DADOS DA LOJA
═══════════════════════════════════════════════════════
VD: {loja.get('vd')}
Nome: {loja.get('nome')}
CNPJ: {loja.get('cnpj')}
Endereço: {loja.get('endereco')}, {loja.get('cidade')} - {loja.get('estado')}
Telefone fixo: {loja.get('tel')}
Celular/WhatsApp: {loja.get('cel')}
Horário de funcionamento: {loja.get('horario')}

═══════════════════════════════════════════════════════
EQUIPE DE GESTÃO
═══════════════════════════════════════════════════════
GGL (Gerente Geral de Loja): {loja.get('ggl')}
Contato GGL: {loja.get('ggl_tel')}
GR (Gerente Regional): {loja.get('gr')}
Contato GR: {loja.get('gr_tel')}

═══════════════════════════════════════════════════════
DESIGNAÇÕES DE CIRCUITO
═══════════════════════════════════════════════════════
MPLS: {loja.get('mpls', 'N/A')}
INN: {loja.get('inn', 'N/A')}

═══════════════════════════════════════════════════════
INFORMAÇÕES ADICIONAIS
═══════════════════════════════════════════════════════
Data/Hora da solicitação: {agora}
Atendente: {nome_atendente}

Favor confirmar recebimento e informar previsão de atendimento.

Atenciosamente,
Central de Comando - T.I. DPSP
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br"""


def gerar_chamado_vivo(loja: dict, nome_atendente: str, hora_inicio: str) -> str:
    """Gera texto para abertura de chamado na Vivo"""
    return f"""Portal Vivo MVE — Campos para preenchimento:

Nome: {nome_atendente}
Telefone: (11) 3274-7527
E-mail: central.comando@dpsp.com.br
Designação: {loja.get('mpls', 'N/A')}
VD: {loja.get('vd')} — {loja.get('nome')}
Horário de início: {hora_inicio}
Horário de funcionamento: {loja.get('horario')}

Acesse: https://mve.vivo.com.br"""


def gerar_chamado_claro(loja: dict, hora_inicio: str) -> str:
    """Gera texto para abertura de chamado na Claro"""
    return f"""Portal Claro Empresas — Texto para abertura:

Designação: {loja.get('inn') or loja.get('mpls', 'N/A')}
Unidade: VD {loja.get('vd')} — {loja.get('nome')}
Endereço: {loja.get('endereco')}, {loja.get('cidade')} — {loja.get('estado')}
Horário do incidente: {hora_inicio}

Acesse: https://webebt01.embratel.com.br/claroempresasonline/index"""
