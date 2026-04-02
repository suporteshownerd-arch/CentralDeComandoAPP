"""
Módulo de integração com Google Sheets
Desenvolvido por Enzo Maranho - T.I. DPSP
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False


class GoogleSheetsManager:
    """Classe para gerenciar integração com Google Sheets"""
    
    def __init__(self, credentials_dict: str = None, sheets_ids: dict = None):
        """
        Inicializa o gerenciador do Google Sheets
        
        Args:
            credentials_dict: JSON da Service Account (ou caminho para arquivo)
            sheets_ids: Dicionário com IDs das planilhas
                       {'aexec': 'id_aexec', 'gcrises': 'id_gcrises'}
        """
        self.credentials = None
        self.client = None
        self.sheets_ids = sheets_ids or {
            'aexec': os.getenv('SHEETS_ID_AEXEC', ''),
            'gcrises': os.getenv('SHEETS_ID_GCRISES', '')
        }
        self._init_client(credentials_dict)
    
    def _init_client(self, credentials_dict: str = None):
        """Inicializa o cliente gspread"""
        if not GSPREAD_AVAILABLE:
            print("Aviso: gspread não disponível. Usando fallback localStorage.")
            return
        
        try:
            # Tentar obter credenciais
            if credentials_dict:
                if os.path.exists(credentials_dict):
                    with open(credentials_dict, 'r') as f:
                        creds = json.load(f)
                else:
                    creds = json.loads(credentials_dict)
            else:
                # Tentar do ambiente
                gcp_creds = os.getenv('GCP_SERVICE_ACCOUNT')
                if gcp_creds:
                    creds = json.loads(gcp_creds)
                else:
                    return
            
            # Autenticar
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            credentials = Credentials.from_service_account_info(creds, scopes=scope)
            self.client = gspread.authorize(credentials)
            
        except Exception as e:
            print(f"Erro ao inicializar Google Sheets: {e}")
            self.client = None
    
    def _get_worksheet(self, sheet_type: str):
        """Obtém worksheet pelo tipo"""
        if not self.client:
            return None
        
        sheet_id = self.sheets_ids.get(sheet_type)
        if not sheet_id:
            return None
        
        try:
            spreadsheet = self.client.open_by_key(sheet_id)
            return spreadsheet.sheet1
        except Exception as e:
            print(f"Erro ao abrir planilha {sheet_type}: {e}")
            return None
    
    def salvar_template(self, tipo: str, templates: List[Dict]) -> bool:
        """
        Salva templates no Google Sheets
        
        Args:
            tipo: Tipo de template ('AExec', 'GCrises', 'Isolada')
            templates: Lista de templates
        
        Returns:
            True se bem-sucedido
        """
        if tipo == 'AExec':
            sheet = self._get_worksheet('aexec')
        elif tipo in ['GCrises', 'Isolada']:
            sheet = self._get_worksheet('gcrises')
        else:
            sheet = None
        
        if not sheet:
            # Fallback para localStorage (usado no frontend)
            return self._salvar_local(tipo, templates)
        
        try:
            # Verificar limite de 99 registros
            existing = sheet.get_all_records()
            if len(existing) >= 99:
                # Remover registro mais antigo
                sheet.delete_row(2)  # Row 1 é header
            
            # Preparar dados
            for t in templates:
                row = [
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    tipo,
                    t.get('tipo', ''),
                    t.get('label', ''),
                    t.get('texto', '')
                ]
                sheet.append_row(row)
            
            return True
            
        except Exception as e:
            print(f"Erro ao salvar no Sheets: {e}")
            return self._salvar_local(tipo, templates)
    
    def _salvar_local(self, tipo: str, templates: List[Dict]) -> bool:
        """Fallback para salvar localmente (para desenvolvimento)"""
        try:
            import sqlite3
            
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'historico.db')
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            
            # Criar tabela se não existir
            c.execute('''CREATE TABLE IF NOT EXISTS historico
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         tipo TEXT,
                         subtipo TEXT,
                         label TEXT,
                         texto TEXT,
                         data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            for t in templates:
                c.execute('INSERT INTO historico (tipo, subtipo, label, texto) VALUES (?, ?, ?, ?)',
                         (tipo, t.get('tipo', ''), t.get('label', ''), t.get('texto', '')))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Erro ao salvar local: {e}")
            return False
    
    def get_historico(self, tipo: str = None, limite: int = 50) -> List[Dict]:
        """
        Récupera histórico do Google Sheets
        
        Args:
            tipo: Tipo específico (opcional)
            limite: Número máximo de registros
        
        Returns:
            Lista de registros
        """
        # Tentar Sheets primeiro
        if tipo == 'AExec':
            sheet = self._get_worksheet('aexec')
        elif tipo in ['GCrises', 'Isolada']:
            sheet = self._get_worksheet('gcrises')
        else:
            # Buscar em todas
            records = []
            for sheet_type in ['aexec', 'gcrises']:
                sheet = self._get_worksheet(sheet_type)
                if sheet:
                    try:
                        records.extend(sheet.get_all_records())
                    except:
                        pass
            return records[-limite:] if records else []
        
        if not sheet:
            # Fallback local
            return self._get_local(tipo, limite)
        
        try:
            records = sheet.get_all_records()
            if tipo:
                records = [r for r in records if r.get('Tipo') == tipo]
            return records[-limite:]
        except Exception as e:
            print(f"Erro ao ler Sheets: {e}")
            return self._get_local(tipo, limite)
    
    def _get_local(self, tipo: str = None, limite: int = 50) -> List[Dict]:
        """Fallback para ler localmente"""
        try:
            import sqlite3
            
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'historico.db')
            if not os.path.exists(db_path):
                return []
            
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            
            if tipo:
                c.execute('SELECT * FROM historico WHERE tipo = ? ORDER BY data DESC LIMIT ?', (tipo, limite))
            else:
                c.execute('SELECT * FROM historico ORDER BY data DESC LIMIT ?', (limite,))
            
            rows = c.fetchall()
            conn.close()
            
            return [{'tipo': r[1], 'subtipo': r[2], 'label': r[3], 'texto': r[4], 'data': r[5]} for r in rows]
            
        except Exception as e:
            print(f"Erro ao ler local: {e}")
            return []
    
    def limpar_historico(self) -> bool:
        """Limpa todo o histórico"""
        try:
            # Limpar Sheets
            for sheet_type in ['aexec', 'gcrises']:
                sheet = self._get_worksheet(sheet_type)
                if sheet:
                    sheet.clear()
            
            # Limpar local
            import sqlite3
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'historico.db')
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute('DELETE FROM historico')
                conn.commit()
                conn.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao limpar: {e}")
            return False
