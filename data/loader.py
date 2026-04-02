"""
Módulo de carregamento e manipulação de dados
Desenvolvido por Enzo Maranho - T.I. DPSP
"""

import os
import csv
import json
from cryptography.fernet import Fernet


class DataLoader:
    """Classe para carregar dados dos arquivos CSV criptografados"""
    
    def __init__(self, data_dir: str = "data", master_key: str = None):
        self.data_dir = data_dir
        self.master_key = master_key or os.getenv("MASTER_KEY", "").encode()
        self.lojas_cache = None
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
    
    def _decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Descriptografa dados usando Fernet"""
        if not self.cipher:
            return encrypted_data
        return self.cipher.decrypt(encrypted_data)
    
    def get_lojas(self):
        """
        Carrega dados de todas as lojas
        Tenta ler de arquivos CSV criptografados, 
        fallback para dados de exemplo se não encontrar
        """
        if self.lojas_cache is not None:
            return self.lojas_cache
        
        # Tentar carregar de CSV
        lojas = self._load_from_csv()
        
        # Fallback para dados de exemplo
        if not lojas:
            lojas = self._get_sample_data()
        
        self.lojas_cache = lojas
        return lojas
    
    def _load_from_csv(self):
        """Carrega dados dos arquivos CSV"""
        lojas = []
        
        # Arquivos esperados
        csv_files = [
            "relacao.csv",
            "designacao.csv", 
            "escalacao.csv",
            "links.csv",
            "GR.csv",
            "GGL.csv"
        ]
        
        # Tentar carregar arquivo principal de relationship
        relacao_file = os.path.join(self.data_dir, "relacao.csv.enc")
        
        if os.path.exists(relacao_file):
            try:
                with open(relacao_file, "rb") as f:
                    encrypted = f.read()
                    decrypted = self._decrypt_data(encrypted)
                    content = decrypted.decode("utf-8")
                    
                reader = csv.DictReader(content.splitlines())
                for row in reader:
                    loja = {
                        "vd": row.get("VD", ""),
                        "nome": row.get("Nome", ""),
                        "cnpj": row.get("CNPJ", ""),
                        "endereco": row.get("Endereco", ""),
                        "cidade": row.get("Cidade", ""),
                        "estado": row.get("Estado", ""),
                        "tel": row.get("Telefone", ""),
                        "cel": row.get("Celular", ""),
                        "email": row.get("Email", ""),
                        "horario": row.get("Horario", ""),
                        "status": row.get("Status", "open"),
                        "mpls": row.get("MPLS", ""),
                        "inn": row.get("INN", ""),
                        "ggl": row.get("GGL", ""),
                        "ggl_tel": row.get("GGL_Telefone", ""),
                        "gr": row.get("GR", ""),
                        "gr_tel": row.get("GR_Telefone", "")
                    }
                    if loja["vd"]:
                        lojas.append(loja)
            except Exception as e:
                print(f"Erro ao carregar CSV: {e}")
        
        return lojas
    
    def _get_sample_data(self):
        """Dados de exemplo para desenvolvimento"""
        return [
            {
                "vd": "2015",
                "nome": "Drogasil Paulista",
                "cnpj": "12.345.678/0001-99",
                "endereco": "Av. Paulista, 1500",
                "cidade": "São Paulo",
                "estado": "SP",
                "regiao": "Sudeste",
                "tel": "(11) 3001-2015",
                "cel": "(11) 91234-5678",
                "email": "paulista@dpsp.com.br",
                "horario": "Seg-Sex 07h-22h / Sáb 08h-20h / Dom 09h-18h",
                "ggl": "Marcos Silva",
                "ggl_tel": "(11) 99876-5432",
                "gr": "Ana Paula Torres",
                "gr_tel": "(11) 98765-4321",
                "mpls": "rsp_mpls_2015",
                "inn": "rsp_inn_2015",
                "status": "open"
            },
            {
                "vd": "1502",
                "nome": "RD Interlagos",
                "cnpj": "12.345.678/0002-80",
                "endereco": "Av. Interlagos, 2500",
                "cidade": "São Paulo",
                "estado": "SP",
                "regiao": "Sudeste",
                "tel": "(11) 3001-1502",
                "cel": "(11) 91234-1502",
                "email": "interlagos@dpsp.com.br",
                "horario": "Seg-Dom 08h-22h",
                "ggl": "Carla Mendes",
                "ggl_tel": "(11) 99000-1502",
                "gr": "Roberto Faria",
                "gr_tel": "(11) 98000-1502",
                "mpls": "rsp_mpls_1502",
                "inn": "rsp_inn_1502",
                "status": "open"
            },
            {
                "vd": "3001",
                "nome": "Drogasil Moema",
                "cnpj": "12.345.678/0003-61",
                "endereco": "Av. Ibirapuera, 3103",
                "cidade": "São Paulo",
                "estado": "SP",
                "regiao": "Sudeste",
                "tel": "(11) 3001-3001",
                "cel": "(11) 97777-3001",
                "email": "moema@dpsp.com.br",
                "horario": "Seg-Sex 08h-21h / Sáb-Dom 09h-20h",
                "ggl": "Felipe Rocha",
                "ggl_tel": "(11) 96666-3001",
                "gr": "Ana Paula Torres",
                "gr_tel": "(11) 98765-4321",
                "mpls": "rsp_mpls_3001",
                "inn": None,
                "status": "closed"
            },
            {
                "vd": "4200",
                "nome": "RD Campinas Centro",
                "cnpj": "12.345.678/0004-42",
                "endereco": "Rua Barão de Jaguara, 400",
                "cidade": "Campinas",
                "estado": "SP",
                "regiao": "Sudeste",
                "tel": "(19) 3001-4200",
                "cel": "(19) 98888-4200",
                "email": "campinas@dpsp.com.br",
                "horario": "Seg-Dom 07h-23h",
                "ggl": "Lucia Alves",
                "ggl_tel": "(19) 97777-4200",
                "gr": "José Pereira",
                "gr_tel": "(19) 96666-4200",
                "mpls": "rcp_mpls_4200",
                "inn": "rcp_inn_4200",
                "status": "open"
            },
            {
                "vd": "5200",
                "nome": "DrogariasRD Rio de Janeiro",
                "cnpj": "12.345.678/0005-23",
                "endereco": "Av. Nossa Senhora de Copacabana, 500",
                "cidade": "Rio de Janeiro",
                "estado": "RJ",
                "regiao": "Sudeste",
                "tel": "(21) 3001-5200",
                "cel": "(21) 98888-5200",
                "email": "copacabana@dpsp.com.br",
                "horario": "Seg-Dom 08h-22h",
                "ggl": "Paulo Santos",
                "ggl_tel": "(21) 97777-5200",
                "gr": "Maria Oliveira",
                "gr_tel": "(21) 96666-5200",
                "mpls": "rio_mpls_5200",
                "inn": "rio_inn_5200",
                "status": "open"
            },
            {
                "vd": "6100",
                "nome": "RD Belo Horizonte",
                "cnpj": "12.345.678/0006-04",
                "endereco": "Av. Amazonas, 1200",
                "cidade": "Belo Horizonte",
                "estado": "MG",
                "regiao": "Sudeste",
                "tel": "(31) 3001-6100",
                "cel": "(31) 98888-6100",
                "email": "bh@dpsp.com.br",
                "horario": "Seg-Sex 08h-21h / Sáb 09h-20h",
                "ggl": "Lucas Souza",
                "ggl_tel": "(31) 97777-6100",
                "gr": "Carla Silva",
                "gr_tel": "(31) 96666-6100",
                "mpls": "bh_mpls_6100",
                "inn": "bh_inn_6100",
                "status": "open"
            },
            {
                "vd": "7100",
                "nome": "RD Curitiba",
                "cnpj": "12.345.678/0007-95",
                "endereco": "Av. Sete de Setembro, 2500",
                "cidade": "Curitiba",
                "estado": "PR",
                "regiao": "Sul",
                "tel": "(41) 3001-7100",
                "cel": "(41) 98888-7100",
                "email": "curitiba@dpsp.com.br",
                "horario": "Seg-Dom 08h-22h",
                "ggl": "Ana Costa",
                "ggl_tel": "(41) 97777-7100",
                "gr": "Roberto Alves",
                "gr_tel": "(41) 96666-7100",
                "mpls": "cwb_mpls_7100",
                "inn": "cwb_inn_7100",
                "status": "open"
            },
            {
                "vd": "8100",
                "nome": "RD Porto Alegre",
                "cnpj": "12.345.678/0008-76",
                "endereco": "Av. Borges de Medeiros, 800",
                "cidade": "Porto Alegre",
                "estado": "RS",
                "regiao": "Sul",
                "tel": "(51) 3001-8100",
                "cel": "(51) 98888-8100",
                "email": "poa@dpsp.com.br",
                "horario": "Seg-Sáb 09h-22h / Dom 10h-20h",
                "ggl": "Bruno Lima",
                "ggl_tel": "(51) 97777-8100",
                "gr": "Juliana Martins",
                "gr_tel": "(51) 96666-8100",
                "mpls": "poa_mpls_8100",
                "inn": "poa_inn_8100",
                "status": "open"
            },
            {
                "vd": "9100",
                "nome": "RD Salvador",
                "cnpj": "12.345.678/0009-57",
                "endereco": "Av. Tancredo Neves, 1200",
                "cidade": "Salvador",
                "estado": "BA",
                "regiao": "Nordeste",
                "tel": "(71) 3001-9100",
                "cel": "(71) 98888-9100",
                "email": "ssa@dpsp.com.br",
                "horario": "Seg-Sex 08h-21h / Sáb 09h-20h",
                "ggl": "Patricia Santos",
                "ggl_tel": "(71) 97777-9100",
                "gr": "Fernando Oliveira",
                "gr_tel": "(71) 96666-9100",
                "mpls": "ssa_mpls_9100",
                "inn": "ssa_inn_9100",
                "status": "open"
            },
            {
                "vd": "0100",
                "nome": "RD Recife",
                "cnpj": "12.345.678/0010-40",
                "endereco": "Av. Recife, 500",
                "cidade": "Recife",
                "estado": "PE",
                "regiao": "Nordeste",
                "tel": "(81) 3001-0100",
                "cel": "(81) 98888-0100",
                "email": "recife@dpsp.com.br",
                "horario": "Seg-Dom 08h-22h",
                "ggl": "Ricardo Alves",
                "ggl_tel": "(81) 97777-0100",
                "gr": "Amanda Costa",
                "gr_tel": "(81) 96666-0100",
                "mpls": "rec_mpls_0100",
                "inn": "rec_inn_0100",
                "status": "open"
            },
            {
                "vd": "0110",
                "nome": "RD Brasília",
                "cnpj": "12.345.678/0011-21",
                "endereco": "Setor Comercial Sul, Quadra 3",
                "cidade": "Brasília",
                "estado": "DF",
                "regiao": "Centro-Oeste",
                "tel": "(61) 3001-0110",
                "cel": "(61) 98888-0110",
                "email": "bsb@dpsp.com.br",
                "horario": "Seg-Sex 08h-20h / Sáb 09h-18h",
                "ggl": "Gustavo Lima",
                "ggl_tel": "(61) 97777-0110",
                "gr": "Renata Souza",
                "gr_tel": "(61) 96666-0110",
                "mpls": "bsb_mpls_0110",
                "inn": "bsb_inn_0110",
                "status": "open"
            }
        ]
    
    def buscar_loja(self, termo: str, modo: str = "VD / Designação", lojas: list = None):
        """
        Busca lojas por diferentes critérios
        
        Args:
            termo: Termo de busca
            modo: Modo de busca (VD/Designação, Endereço, Nome, Livre)
            lojas: Lista de lojas (opcional, usa cache se não informado)
        
        Returns:
            Lista de lojas encontradas
        """
        if not termo:
            return []
        
        if lojas is None:
            lojas = self.get_lojas()
        
        termo = termo.strip().lower()
        resultados = []
        
        for loja in lojas:
            if modo == "VD / Designação":
                if (termo == loja.get("vd", "").lower() or 
                    termo in str(loja.get("mpls", "")).lower() or 
                    termo in str(loja.get("inn", "")).lower()):
                    resultados.append(loja)
            elif modo == "Endereço":
                if termo in loja.get("endereco", "").lower():
                    resultados.append(loja)
            elif modo == "Nome de Loja":
                if termo in loja.get("nome", "").lower():
                    resultados.append(loja)
            elif modo == "Outra Informação":
                # Busca em todos os campos
                dados = json.dumps(loja).lower()
                if termo in dados:
                    resultados.append(loja)
        
        return resultados
    
    def get_loja_by_vd(self, vd: str) -> dict:
        """Retorna loja pelo VD"""
        lojas = self.get_lojas()
        for loja in lojas:
            if loja.get("vd") == vd:
                return loja
        return None
