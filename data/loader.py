"""
Módulo de carregamento e manipulação de dados
Desenvolvido por Enzo Maranho - T.I. DPSP
"""

import os
import csv
import json
import time
from datetime import datetime
from cryptography.fernet import Fernet
from typing import Optional, Dict, List

try:
    from rapidfuzz import fuzz, process as rfprocess
    FUZZY_AVAILABLE = True
except ImportError:
    FUZZY_AVAILABLE = False


class CacheManager:
    """Gerenciador de cache com TTL"""

    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, tuple] = {}

    def get(self, key: str) -> Optional[any]:
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value: any) -> None:
        self._cache[key] = (value, time.time())

    def invalidate(self, key: str = None) -> None:
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()


class UsageLogger:
    """Log de uso da aplicação"""

    def __init__(self, log_file: str = "data/usage.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else "data", exist_ok=True)

    def log(self, action: str, user: str = "anonymous", details: dict = None):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                details_str = json.dumps(details or {})
                f.write(f"[{timestamp}] {action} | user:{user} | {details_str}\n")
        except Exception:
            pass

    def get_stats(self) -> dict:
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
        except Exception:
            return {"buscas": 0, "chamados": 0, "templates": 0, "usuarios": 0}


class DataLoader:
    """Carrega dados dos arquivos CSV criptografados"""

    def __init__(self, data_dir: str = None, master_key=None):
        # Resolve o diretório de dados
        if data_dir:
            self.data_dir = data_dir
        else:
            # Tenta encontrar o diretório de CSVs automaticamente
            base = os.path.dirname(os.path.abspath(__file__))
            candidatos = [
                os.path.join(base, "..", "..", "consulta lojas python", "csvs"),
                os.path.join(base, ".."),
                base,
            ]
            self.data_dir = next(
                (p for p in candidatos if os.path.isdir(p) and any(
                    f.endswith(".enc") for f in os.listdir(p)
                )),
                base,
            )

        # Chave Fernet
        if master_key:
            raw = master_key
        else:
            raw = os.getenv("MASTER_KEY", "")

        if isinstance(raw, str):
            raw = raw.encode()
        self.master_key = raw

        self.cache_manager = CacheManager(ttl_seconds=300)
        self.usage_logger = UsageLogger()
        self._init_fernet()

    def _init_fernet(self):
        try:
            self.cipher = Fernet(self.master_key) if self.master_key else None
        except Exception:
            self.cipher = None

    def _decrypt(self, data: bytes) -> bytes:
        if self.cipher:
            try:
                return self.cipher.decrypt(data)
            except Exception:
                pass
        return data

    def _read_enc_csv(self, filename: str) -> List[dict]:
        """Lê um arquivo .csv.enc ou .csv e devolve lista de dicts."""
        for ext in [".csv.enc", ".csv"]:
            path = os.path.join(self.data_dir, filename.replace(".csv", "") + ext)
            if os.path.exists(path):
                with open(path, "rb") as f:
                    raw = f.read()
                content = self._decrypt(raw).decode("utf-8", errors="replace")
                reader = csv.DictReader(content.splitlines())
                return list(reader)
        return []

    def _load_from_csv(self) -> List[dict]:
        """Carrega e mescla todos os CSVs de dados."""
        relacao = self._read_enc_csv("relacao")
        if not relacao:
            return []

        # Índices auxiliares por VD
        desig_idx: Dict[str, dict] = {}
        for row in self._read_enc_csv("designacao"):
            vd = row.get("VD", "").strip()
            if vd:
                desig_idx[vd] = row

        ggl_idx: Dict[str, dict] = {}
        for row in self._read_enc_csv("GGL"):
            vd = row.get("VD", "").strip()
            if vd:
                ggl_idx[vd] = row

        gr_idx: Dict[str, dict] = {}
        for row in self._read_enc_csv("GR"):
            vd = row.get("VD", "").strip()
            if vd:
                gr_idx[vd] = row

        lojas = []
        for row in relacao:
            vd = str(row.get("VD", row.get("vd", ""))).strip()
            if not vd:
                continue

            d = desig_idx.get(vd, {})
            g = ggl_idx.get(vd, {})
            r = gr_idx.get(vd, {})

            loja = {
                "vd":      vd,
                "nome":    row.get("Nome", row.get("nome", "")),
                "cnpj":    row.get("CNPJ", row.get("cnpj", "")),
                "endereco": row.get("Endereco", row.get("endereco", row.get("Endereço", ""))),
                "cidade":  row.get("Cidade", row.get("cidade", "")),
                "estado":  row.get("Estado", row.get("estado", "")),
                "regiao":  row.get("Regiao", row.get("regiao", row.get("Região", ""))),
                "tel":     row.get("Telefone", row.get("tel", "")),
                "cel":     row.get("Celular", row.get("cel", "")),
                "email":   row.get("Email", row.get("email", "")),
                "horario": row.get("Horario", row.get("horario", row.get("Horário", ""))),
                "status":  row.get("Status", row.get("status", "open")),
                "mpls":    d.get("MPLS", row.get("MPLS", row.get("mpls", ""))),
                "inn":     d.get("INN", row.get("INN", row.get("inn", ""))),
                "ggl":     g.get("Nome", g.get("GGL", row.get("GGL", row.get("ggl", "")))),
                "ggl_tel": g.get("Telefone", g.get("GGL_Telefone", row.get("GGL_Telefone", ""))),
                "gr":      r.get("Nome", r.get("GR", row.get("GR", row.get("gr", "")))),
                "gr_tel":  r.get("Telefone", r.get("GR_Telefone", row.get("GR_Telefone", ""))),
            }
            lojas.append(loja)

        return lojas

    def get_lojas(self) -> List[dict]:
        """Retorna lista de lojas (com cache)."""
        cached = self.cache_manager.get("all_lojas")
        if cached is not None:
            return cached

        lojas = self._load_from_csv()
        if not lojas:
            lojas = self._get_sample_data()

        self.cache_manager.set("all_lojas", lojas)
        return lojas

    def get_loja_by_vd(self, vd: str) -> Optional[dict]:
        """Lookup O(1) por VD usando índice cacheado."""
        idx = self.cache_manager.get("idx_vd")
        if idx is None:
            idx = {l["vd"]: l for l in self.get_lojas()}
            self.cache_manager.set("idx_vd", idx)
        return idx.get(str(vd).strip())

    def validar_vd(self, vd: str) -> Dict[str, any]:
        if not vd:
            return {"valido": False, "loja": None, "mensagem": "VD não fornecido"}
        vd = vd.strip()
        if not vd.isdigit():
            return {"valido": False, "loja": None, "mensagem": "VD deve conter apenas números"}
        if len(vd) > 6:
            return {"valido": False, "loja": None, "mensagem": "VD deve ter no máximo 6 dígitos"}
        loja = self.get_loja_by_vd(vd)
        if loja:
            return {"valido": True, "loja": loja, "mensagem": "VD encontrado"}
        return {"valido": False, "loja": None, "mensagem": f"VD {vd} não encontrado"}

    def buscar_loja(self, termo: str, modo: str = "VD / Designação", lojas: list = None) -> List[dict]:
        """
        Busca lojas por critério.
        Modos: 'VD / Designação' | 'Endereço' | 'Nome de Loja' | 'Outra Informação'
        """
        if not termo:
            return []

        if lojas is None:
            lojas = self.get_lojas()

        termo_lower = termo.strip().lower()
        resultados = []

        for loja in lojas:
            if modo == "VD / Designação":
                match = (
                    termo_lower == loja.get("vd", "").lower()
                    or termo_lower in str(loja.get("mpls", "")).lower()
                    or termo_lower in str(loja.get("inn", "")).lower()
                )
            elif modo == "Endereço":
                match = (
                    termo_lower in loja.get("endereco", "").lower()
                    or termo_lower in loja.get("cidade", "").lower()
                )
            elif modo == "Nome de Loja":
                match = termo_lower in loja.get("nome", "").lower()
            else:  # Outra Informação — busca em todos os campos
                match = termo_lower in json.dumps(loja, ensure_ascii=False).lower()

            if match:
                resultados.append(loja)

        # Fuzzy fallback: se não achou nada e modo é Nome ou Livre
        if not resultados and FUZZY_AVAILABLE and modo in ("Nome de Loja", "Outra Informação"):
            nomes = [l.get("nome", "") for l in lojas]
            matches = rfprocess.extract(termo, nomes, scorer=fuzz.partial_ratio, limit=5, score_cutoff=65)
            matched_names = {m[0] for m in matches}
            resultados = [l for l in lojas if l.get("nome") in matched_names]

        return resultados

    def get_estados(self) -> List[str]:
        return sorted({l.get("estado", "") for l in self.get_lojas() if l.get("estado")})

    def get_regioes(self) -> List[str]:
        return sorted({l.get("regiao", "") for l in self.get_lojas() if l.get("regiao")})

    # ── Dados de exemplo (fallback) ──────────────────────────────────────────
    def _get_sample_data(self) -> List[dict]:
        return [
            {"vd": "318",  "nome": "DSP SANTA BARBARA D'OESTE", "endereco": "AV DE CILLO,167",              "cidade": "SANTA BARBARA D'OESTE", "estado": "SP", "regiao": "Sudeste", "tel": "", "cel": "", "email": "", "horario": "", "ggl": "", "ggl_tel": "", "gr": "", "gr_tel": "", "mpls": "rsp_mpls_318",  "inn": "rsp_inn_318",  "status": "open"},
            {"vd": "322",  "nome": "DSP SAO CARLOS",             "endereco": "AV SAO CARLOS,2358",           "cidade": "SAO CARLOS",            "estado": "SP", "regiao": "Sudeste", "tel": "", "cel": "", "email": "", "horario": "", "ggl": "", "ggl_tel": "", "gr": "", "gr_tel": "", "mpls": "rsp_mpls_322",  "inn": "rsp_inn_322",  "status": "open"},
            {"vd": "339",  "nome": "DSP SHOPPING TAMBORE",       "endereco": "AVENIDA PIRACEMA,669",          "cidade": "BARUERI",               "estado": "SP", "regiao": "Sudeste", "tel": "", "cel": "", "email": "", "horario": "", "ggl": "", "ggl_tel": "", "gr": "", "gr_tel": "", "mpls": "rsp_mpls_339",  "inn": "",             "status": "open"},
            {"vd": "345",  "nome": "DSP PORTUGAL II",            "endereco": "AV PORTUGAL,602",              "cidade": "SANTO ANDRE",           "estado": "SP", "regiao": "Sudeste", "tel": "", "cel": "", "email": "", "horario": "", "ggl": "", "ggl_tel": "", "gr": "", "gr_tel": "", "mpls": "rsp_mpls_345",  "inn": "rsp_inn_345",  "status": "open"},
            {"vd": "348",  "nome": "DSP JARDIM MIRIAM",          "endereco": "AV CUPECE,5400",               "cidade": "SAO PAULO",             "estado": "SP", "regiao": "Sudeste", "tel": "", "cel": "", "email": "", "horario": "", "ggl": "", "ggl_tel": "", "gr": "", "gr_tel": "", "mpls": "rsp_mpls_348",  "inn": "rsp_inn_348",  "status": "closed"},
            {"vd": "2015", "nome": "Drogasil Paulista",          "endereco": "Av. Paulista, 1500",           "cidade": "São Paulo",             "estado": "SP", "regiao": "Sudeste", "tel": "(11) 3001-2015", "cel": "(11) 91234-5678", "email": "paulista@dpsp.com.br", "horario": "Seg-Sex 07h-22h", "ggl": "Marcos Silva", "ggl_tel": "(11) 99876-5432", "gr": "Ana Paula Torres", "gr_tel": "(11) 98765-4321", "mpls": "rsp_mpls_2015", "inn": "rsp_inn_2015", "status": "open"},
            {"vd": "5200", "nome": "DrogariasRD Copacabana",     "endereco": "Av. N.S. de Copacabana, 500",  "cidade": "Rio de Janeiro",        "estado": "RJ", "regiao": "Sudeste", "tel": "(21) 3001-5200", "cel": "(21) 98888-5200", "email": "copa@dpsp.com.br",     "horario": "Seg-Dom 08h-22h",  "ggl": "Paulo Santos",  "ggl_tel": "(21) 97777-5200", "gr": "Maria Oliveira",   "gr_tel": "(21) 96666-5200", "mpls": "rio_mpls_5200",  "inn": "rio_inn_5200",  "status": "open"},
            {"vd": "6100", "nome": "RD Belo Horizonte",          "endereco": "Av. Amazonas, 1200",           "cidade": "Belo Horizonte",        "estado": "MG", "regiao": "Sudeste", "tel": "(31) 3001-6100", "cel": "(31) 98888-6100", "email": "bh@dpsp.com.br",        "horario": "Seg-Sex 08h-21h",  "ggl": "Lucas Souza",   "ggl_tel": "(31) 97777-6100", "gr": "Carla Silva",      "gr_tel": "(31) 96666-6100", "mpls": "bh_mpls_6100",   "inn": "bh_inn_6100",   "status": "open"},
            {"vd": "7100", "nome": "RD Curitiba",                "endereco": "Av. Sete de Setembro, 2500",   "cidade": "Curitiba",              "estado": "PR", "regiao": "Sul",     "tel": "(41) 3001-7100", "cel": "(41) 98888-7100", "email": "cwb@dpsp.com.br",       "horario": "Seg-Dom 08h-22h",  "ggl": "Ana Costa",     "ggl_tel": "(41) 97777-7100", "gr": "Roberto Alves",    "gr_tel": "(41) 96666-7100", "mpls": "cwb_mpls_7100",  "inn": "cwb_inn_7100",  "status": "open"},
            {"vd": "9100", "nome": "RD Salvador",                "endereco": "Av. Tancredo Neves, 1200",     "cidade": "Salvador",              "estado": "BA", "regiao": "Nordeste","tel": "(71) 3001-9100", "cel": "(71) 98888-9100", "email": "ssa@dpsp.com.br",        "horario": "Seg-Sex 08h-21h",  "ggl": "Patricia Santos","ggl_tel": "(71) 97777-9100", "gr": "Fernando Oliveira","gr_tel": "(71) 96666-9100", "mpls": "ssa_mpls_9100",  "inn": "ssa_inn_9100",  "status": "open"},
        ]
