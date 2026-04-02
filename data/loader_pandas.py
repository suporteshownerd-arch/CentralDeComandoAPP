"""
Módulo de carregamento de dados com Pandas
Central de Comando DPSP v2.1
Integração com CSVs reais
"""

import os
import pandas as pd
import json
import time
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from cryptography.fernet import Fernet


class CacheManager:
    """Gerenciador de cache inteligente para dados"""
    
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, tuple] = {}
    
    def get(self, key: str) -> Optional[any]:
        """Obtém valor do cache se não expirou"""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: any) -> None:
        """Define valor no cache com timestamp"""
        self._cache[key] = (value, time.time())
    
    def invalidate(self, key: str = None) -> None:
        """Invalida cache específico ou todo"""
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()


class UsageLogger:
    """Sistema de logs de uso"""
    
    def __init__(self, log_file: str = "data/usage.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else "data", exist_ok=True)
    
    def log(self, action: str, user: str = "anonymous", details: dict = None):
        """Registra ação no log"""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                details_str = json.dumps(details) if details else "{}"
                f.write(f"[{timestamp}] {action} | user:{user} | {details_str}\n")
        except Exception as e:
            print(f"Erro ao salvar log: {e}")
    
    def get_stats(self, days: int = 7) -> dict:
        """Retorna estatísticas de uso"""
        try:
            if not os.path.exists(self.log_file):
                return {"buscas": 0, "chamados": 0, "templates": 0, "usuarios": 0}
            
            stats = {"buscas": 0, "chamados": 0, "templates": 0, "usuarios": set()}
            
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if "busca" in line.lower():
                        stats["buscas"] += 1
                    if "chamado" in line.lower():
                        stats["chamados"] += 1
                    if "template" in line.lower():
                        stats["templates"] += 1
                    if "user:" in line:
                        user = line.split("user:")[1].split("|")[0].strip()
                        stats["usuarios"].add(user)
            
            stats["usuarios"] = len(stats["usuarios"])
            return stats
        except:
            return {"buscas": 0, "chamados": 0, "templates": 0, "usuarios": 0}


class DataLoaderPandas:
    """
    Loader de dados usando Pandas para melhor performance
    Integra dados de múltiplos CSVs: relacao, designacao, GGL, GR
    """
    
    def __init__(self, csv_dir: str = None, master_key: str = None):
        """
        Args:
            csv_dir: Diretório contendo os CSVs (padrão: ../consulta lojas python/csvs)
            master_key: Chave Fernet para descriptografar arquivos
        """
        if csv_dir is None:
            csv_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "consulta lojas python", "csvs")
        
        self.csv_dir = csv_dir
        self.master_key = master_key or os.getenv("MASTER_KEY", "").encode()
        self.cache = CacheManager(ttl_seconds=300)
        self.usage_logger = UsageLogger()
        
        self._df_lojas = None
        self._df_designacoes = None
        self._df_ggl = None
        self._df_gr = None
        
        self._init_fernet()
    
    def _init_fernet(self):
        """Inicializa o criptografador Fernet"""
        try:
            if self.master_key:
                self.cipher = Fernet(self.master_key)
            else:
                self.cipher = None
        except Exception:
            self.cipher = None
    
    def _load_csv(self, filename: str, encoding: str = "utf-8") -> pd.DataFrame:
        """Carrega um CSV com tratamento de erros"""
        filepath = os.path.join(self.csv_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Arquivo não encontrado: {filepath}")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(filepath, encoding=encoding, on_bad_lines='skip')
            print(f"Carregado {filename}: {len(df)} linhas")
            return df
        except Exception as e:
            print(f"Erro ao carregar {filename}: {e}")
            return pd.DataFrame()
    
    def _load_all_data(self):
        """Carrega todos os CSVs e integra"""
        cached = self.cache.get("all_data")
        if cached is not None:
            self._df_lojas, self._df_designacoes, self._df_ggl, self._df_gr = cached
            return
        
        self._df_lojas = self._load_csv("relacao.csv")
        self._df_designacoes = self._load_csv("designacao.csv")
        self._df_ggl = self._load_csv("GGL.csv")
        self._df_gr = self._load_csv("GR.csv")
        
        self._process_data()
        
        self.cache.set("all_data", (self._df_lojas, self._df_designacoes, self._df_ggl, self._df_gr))
    
    def _process_data(self):
        """Processa e normaliza os dados dos CSVs"""
        
        if self._df_lojas.empty:
            return
        
        col_mapping = {
            'CODIGO': 'vd',
            'LOJAS': 'nome',
            'ENDEREÇO': 'endereco',
            'BAIRRO': 'bairro',
            'CIDADE': 'cidade',
            'ESTADO': 'estado',
            'CEP': 'cep',
            'LATITUDE': 'latitude',
            'LONGITUDE': 'longitude',
            'TELEFONE1': 'tel',
            'CELULAR': 'cel',
            'E-MAIL': 'email',
            '2ª a 6ª': 'horario_semana',
            'SAB': 'horario_sab',
            'DOM': 'horario_dom',
            'STATUS': 'status',
            'REGIAO GGL': 'regiao_ggl',
            'REGIAO GR': 'regiao_gr',
            'NOME GGL': 'ggl',
            'NOME GR': 'gr',
            'CNPJ': 'cnpj',
            'INSCR. ESTADUAL': 'inscricao_estadual',
            'PDVs ATIVOS': 'pdvs',
            'ÁREA DE VENDA': 'area_venda',
            'CLUSTER': 'cluster',
            'TIPO LOJA': 'tipo_loja',
            'CD SUPRIDOR': 'cd_supridor',
        }
        
        existing_cols = {k: v for k, v in col_mapping.items() if k in self._df_lojas.columns}
        self._df_lojas = self._df_lojas.rename(columns=existing_cols)
        
        if 'vd' not in self._df_lojas.columns and 'CODIGO' in self._df_lojas.columns:
            self._df_lojas['vd'] = self._df_lojas['CODIGO'].astype(str)
        
        if 'status' in self._df_lojas.columns:
            self._df_lojas['status'] = self._df_lojas['status'].apply(
                lambda x: 'open' if str(x).upper() == 'ATIVA' else 'closed'
            )
        
        if 'horario_semana' in self._df_lojas.columns:
            self._df_lojas['horario'] = self._df_lojas['horario_semana'].fillna('')
        
        print(f"Processado: {len(self._df_lojas)} lojas")
    
    def get_df(self) -> pd.DataFrame:
        """Retorna DataFrame de lojas"""
        self._load_all_data()
        return self._df_lojas
    
    def get_lojas_list(self) -> List[Dict]:
        """Retorna lista de lojas como dicionários (compatibilidade com código anterior)"""
        df = self.get_df()
        if df.empty:
            return self._get_sample_data()
        
        cols_to_keep = ['vd', 'nome', 'endereco', 'bairro', 'cidade', 'estado', 'cep',
                       'tel', 'cel', 'email', 'status', 'horario', 'ggl', 'gr',
                       'latitude', 'longitude', 'cluster', 'tipo_loja']
        
        available_cols = [c for c in cols_to_keep if c in df.columns]
        df_subset = df[available_cols].copy()
        
        df_subset = df_subset.fillna('')
        
        return df_subset.to_dict('records')
    
    def _get_sample_data(self):
        """Dados de exemplo se não encontrar CSVs"""
        return [
            {"vd": "318", "nome": "DSP SANTA BARBARA D'OESTE", "endereco": "AV DE CILLO,167", "cidade": "SANTA BARBARA D'OESTE", "estado": "SP", "status": "open", "horario": "07 ÀS 23"},
            {"vd": "322", "nome": "DSP SAO CARLOS", "endereco": "AV SAO CARLOS,2358", "cidade": "SAO CARLOS", "estado": "SP", "status": "open", "horario": "24 HORAS"},
        ]
    
    def buscar_loja(self, termo: str, modo: str = "VD / Designação") -> List[Dict]:
        """Busca lojas usando pandas (mais rápido)"""
        df = self.get_df()
        
        if df.empty:
            return []
        
        termo = str(termo).strip().lower()
        
        if modo == "VD / Designação":
            mask = df['vd'].astype(str).str.lower().str.contains(termo, na=False)
        
        elif modo == "Endereço":
            addr_col = 'endereco' if 'endereco' in df.columns else 'ENDEREÇO'
            if addr_col in df.columns:
                mask = df[addr_col].astype(str).str.lower().str.contains(termo, na=False)
            else:
                mask = pd.Series([False] * len(df))
        
        elif modo == "Nome de Loja":
            nome_col = 'nome' if 'nome' in df.columns else 'LOJAS'
            if nome_col in df.columns:
                mask = df[nome_col].astype(str).str.lower().str.contains(termo, na=False)
            else:
                mask = pd.Series([False] * len(df))
        
        elif modo == "Outra Informação":
            text_cols = df.select_dtypes(include=['object']).columns
            mask = df[text_cols].apply(lambda x: x.astype(str).str.lower().str.contains(termo, na=False)).any(axis=1)
        
        else:
            mask = pd.Series([False] * len(df))
        
        results = df[mask].head(50)
        
        cols_to_keep = ['vd', 'nome', 'endereco', 'cidade', 'estado', 'tel', 'cel', 'email', 'status', 'horario', 'ggl', 'gr']
        available_cols = [c for c in cols_to_keep if c in results.columns]
        return results[available_cols].fillna('').to_dict('records')
    
    def validar_vd(self, vd: str) -> Dict[str, any]:
        """Valida se VD existe"""
        if not vd:
            return {"valido": False, "loja": None, "mensagem": "VD não fornecido"}
        
        vd = vd.strip()
        
        if not vd.isdigit():
            return {"valido": False, "loja": None, "mensagem": "VD deve conter apenas números"}
        
        df = self.get_df()
        
        if 'vd' in df.columns:
            match = df[df['vd'].astype(str) == vd]
        
        elif 'CODIGO' in df.columns:
            match = df[df['CODIGO'].astype(str) == vd]
        
        else:
            return {"valido": False, "loja": None, "mensagem": "Coluna VD não encontrada"}
        
        if not match.empty:
            loja = match.iloc[0].to_dict()
            return {"valido": True, "loja": loja, "mensagem": "VD encontrado"}
        
        return {"valido": False, "loja": None, "mensagem": f"VD {vd} não encontrado"}
    
    def get_loja_by_vd(self, vd: str) -> Optional[Dict]:
        """Retorna loja pelo VD"""
        df = self.get_df()
        
        if 'vd' in df.columns:
            match = df[df['vd'].astype(str) == vd]
        elif 'CODIGO' in df.columns:
            match = df[df['CODIGO'].astype(str) == vd]
        else:
            return None
        
        if not match.empty:
            return match.iloc[0].to_dict()
        return None
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas do parque de lojas"""
        df = self.get_df()
        
        if df.empty:
            return {"total": 0, "ativas": 0, "inativas": 0, "por_estado": {}, "por_tipo": {}}
        
        total = len(df)
        
        if 'status' in df.columns:
            ativas = len(df[df['status'] == 'open'])
            inativas = len(df[df['status'] == 'closed'])
        else:
            ativas = total
            inativas = 0
        
        por_estado = {}
        if 'estado' in df.columns:
            por_estado = df['estado'].value_counts().to_dict()
        
        por_tipo = {}
        if 'tipo_loja' in df.columns or 'TIPO LOJA' in df.columns:
            col = 'tipo_loja' if 'tipo_loja' in df.columns else 'TIPO LOJA'
            por_tipo = df[col].value_counts().to_dict()
        
        return {
            "total": total,
            "ativas": ativas,
            "inativas": inativas,
            "por_estado": por_estado,
            "por_tipo": por_tipo
        }
    
    def get_designacoes(self) -> pd.DataFrame:
        """Retorna DataFrame de designações"""
        self._load_all_data()
        return self._df_designacoes
    
    def get_lojas_com_designacao(self) -> pd.DataFrame:
        """Retorna lojas com informações de designação (MPLS/INN)"""
        df_lojas = self.get_df()
        df_desig = self.get_designacoes()
        
        if df_lojas.empty or df_desig.empty:
            return df_lojas
        
        df_desig_vd = df_desig[df_desig['vd'].notna()].copy()
        
        if not df_desig_vd.empty:
            mpls_df = df_desig_vd[df_desig_vd['Tipo de acesso'].str.contains('MPLS', na=False, case=False)]
            inn_df = df_desig_vd[df_desig_vd['Tipo de acesso'].str.contains('INN', na=False, case=False)]
            
            mpls_by_vd = mpls_df.groupby('vd')['Número (Designação)'].first().to_dict()
            inn_by_vd = inn_df.groupby('vd')['Número (Designação)'].first().to_dict()
            
            df_lojas['mpls'] = df_lojas['vd'].astype(str).map(mpls_by_vd)
            df_lojas['inn'] = df_lojas['vd'].astype(str).map(inn_by_vd)
        
        return df_lojas


def get_sample_data_legacy():
    """Dados de exemplo legacy para fallback"""
    return [
        {"vd": "2015", "nome": "Drogasil Paulista", "endereco": "Av. Paulista, 1500", "cidade": "São Paulo", "estado": "SP", "tel": "(11) 3001-2015", "cel": "(11) 91234-5678", "email": "paulista@dpsp.com.br", "horario": "Seg-Sex 07h-22h", "ggl": "Marcos Silva", "gr": "Ana Paula Torres", "mpls": "rsp_mpls_2015", "inn": "rsp_inn_2015", "status": "open"},
        {"vd": "1502", "nome": "RD Interlagos", "endereco": "Av. Interlagos, 2500", "cidade": "São Paulo", "estado": "SP", "tel": "(11) 3001-1502", "cel": "(11) 91234-1502", "email": "interlagos@dpsp.com.br", "horario": "Seg-Dom 08h-22h", "ggl": "Carla Mendes", "gr": "Roberto Faria", "mpls": "rsp_mpls_1502", "inn": "rsp_inn_1502", "status": "open"},
        {"vd": "3001", "nome": "Drogasil Moema", "endereco": "Av. Ibirapuera, 3103", "cidade": "São Paulo", "estado": "SP", "tel": "(11) 3001-3001", "cel": "(11) 97777-3001", "email": "moema@dpsp.com.br", "horario": "Seg-Sex 08h-21h", "ggl": "Felipe Rocha", "gr": "Ana Paula Torres", "mpls": "rsp_mpls_3001", "inn": None, "status": "closed"},
        {"vd": "4200", "nome": "RD Campinas Centro", "endereco": "Rua Barão de Jaguara, 400", "cidade": "Campinas", "estado": "SP", "tel": "(19) 3001-4200", "cel": "(19) 98888-4200", "email": "campinas@dpsp.com.br", "horario": "Seg-Dom 07h-23h", "ggl": "Lucia Alves", "gr": "José Pereira", "mpls": "rcp_mpls_4200", "inn": "rcp_inn_4200", "status": "open"},
        {"vd": "5200", "nome": "DrogariasRD Rio de Janeiro", "endereco": "Av. Nossa Senhora de Copacabana, 500", "cidade": "Rio de Janeiro", "estado": "RJ", "tel": "(21) 3001-5200", "cel": "(21) 98888-5200", "email": "copacabana@dpsp.com.br", "horario": "Seg-Dom 08h-22h", "ggl": "Paulo Santos", "gr": "Maria Oliveira", "mpls": "rio_mpls_5200", "inn": "rio_inn_5200", "status": "open"},
    ]