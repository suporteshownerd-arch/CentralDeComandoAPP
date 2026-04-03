"""
Módulo de carregamento e manipulação de dados
Desenvolvido por Enzo Maranho - T.I. DPSP

Mapeamento real dos CSVs (confirmado na fonte):
  relacao.csv   → CODIGO=VD, LOJAS=nome, STATUS=ATIVA/INATIVA, REGIAO GGL=região,
                   NOME GGL/GR, ENDEREÇO, BAIRRO, CIDADE, ESTADO, CEP, CNPJ,
                   TELEFONE1, TELEFONE2, CELULAR, E-MAIL,
                   2ª a 6ª, SAB, DOM, FUNC., BANDEIRA
  designacao.csv → People=VD (join com CODIGO), Operadora, Número (Designação)
                   VIVO → circuito principal / EMBRATEL/CLARO → circuito backup
  GGL.csv        → NOME GGL, CELULAR  (keyed by nome, sem VD)
  GR.csv         → NOME GR, CELULAR.1 (keyed by nome, sem VD)
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
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, tuple] = {}

    def get(self, key: str) -> Optional[any]:
        if key in self._cache:
            value, ts = self._cache[key]
            if time.time() - ts < self.ttl_seconds:
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
    def __init__(self, log_file: str = "data/usage.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else "data", exist_ok=True)

    def log(self, action: str, user: str = "anonymous", details: dict = None):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{ts}] {action} | user:{user} | {json.dumps(details or {})}\n")
        except Exception:
            pass


class DataLoader:
    """Carrega e normaliza dados das lojas DPSP."""

    def __init__(self, data_dir: str = None, master_key=None):
        # Resolve diretório de CSVs
        base = os.path.dirname(os.path.abspath(__file__))
        if data_dir:
            self.data_dir = data_dir
        else:
            candidatos = [
                os.path.join(base, "..", "..", "consulta lojas python", "csvs"),
                os.path.join(base, ".."),
                base,
            ]
            self.data_dir = next(
                (p for p in candidatos
                 if os.path.isdir(p) and any(f.endswith((".csv", ".csv.enc")) for f in os.listdir(p))),
                base,
            )

        # Chave Fernet (opcional)
        raw = master_key or os.getenv("MASTER_KEY", "")
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

    # ── I/O ──────────────────────────────────────────────────────────────────

    def _decrypt(self, data: bytes) -> bytes:
        if self.cipher:
            try:
                return self.cipher.decrypt(data)
            except Exception:
                pass
        return data

    def _read_csv(self, filename: str) -> List[dict]:
        """Lê CSV com ou sem encriptação.
        Com cipher: prefere .csv.enc, fallback .csv
        Sem cipher: usa .csv direto (evita ler binário encriptado).
        """
        # Ordem: .enc quando temos cipher, .csv sempre como fallback
        suffixes = ([".csv.enc", ".csv"] if self.cipher else [".csv", ".csv.enc"])
        csv.field_size_limit(10 * 1024 * 1024)
        for suffix in suffixes:
            path = os.path.join(self.data_dir, filename + suffix)
            if not os.path.exists(path):
                continue
            with open(path, "rb") as f:
                raw = self._decrypt(f.read())
            try:
                content = raw.decode("utf-8", errors="replace")
                rows = list(csv.DictReader(content.splitlines()))
                if rows:
                    return rows
            except Exception:
                continue
        return []

    # ── Loaders auxiliares ────────────────────────────────────────────────────

    def _build_ggl_idx(self) -> Dict[str, str]:
        """Dicionário {nome_ggl: telefone} a partir de GGL.csv."""
        idx = {}
        for row in self._read_csv("GGL"):
            nome = row.get("NOME GGL", "").strip()
            tel  = row.get("CELULAR", "").strip()
            if nome and nome != "-":
                idx[nome] = tel
        return idx

    def _build_gr_idx(self) -> Dict[str, str]:
        """Dicionário {nome_gr: telefone} a partir de GR.csv."""
        idx = {}
        for row in self._read_csv("GR"):
            nome = row.get("NOME GR", "").strip()
            tel  = row.get("CELULAR.1", "").strip()
            if nome and nome != "-":
                idx[nome] = tel
        return idx

    def _build_desig_idx(self) -> Dict[str, dict]:
        """
        Dicionário {vd: {mpls: str, inn: str, circuitos: list}} a partir de designacao.csv.
        Join key: designacao.People → relacao.CODIGO
        Tipo de acesso "VPN IP MPLS" → circuito principal (mpls)
        Tipo de acesso "INN"         → circuito backup   (inn)
        """
        idx: Dict[str, dict] = {}
        for row in self._read_csv("designacao"):
            vd   = str(row.get("People", "")).strip()
            tipo = row.get("Tipo de acesso", "").strip().upper()
            op   = row.get("Operadora", "").strip()
            des  = row.get("Número (Designação)", "").strip()
            sta  = row.get("Status", "").strip().upper()
            if not vd or not des or sta == "INATIVO":
                continue
            if vd not in idx:
                idx[vd] = {"mpls": "", "inn": "", "circuitos": []}
            idx[vd]["circuitos"].append({"op": op, "tipo": tipo, "des": des})
            # "VPN IP MPLS" → mpls principal; "INN" → backup inn
            if tipo == "VPN IP MPLS" and not idx[vd]["mpls"]:
                idx[vd]["mpls"] = des
            elif tipo == "INN" and not idx[vd]["inn"]:
                idx[vd]["inn"] = des
        return idx

    # ── Loader principal ──────────────────────────────────────────────────────

    def _load_from_csv(self) -> List[dict]:
        ggl_idx   = self._build_ggl_idx()
        gr_idx    = self._build_gr_idx()
        desig_idx = self._build_desig_idx()

        lojas = []
        for row in self._read_csv("relacao"):
            vd = str(row.get("CODIGO", "")).strip()
            if not vd:
                continue

            status_raw = row.get("STATUS", "").strip().upper()
            if status_raw == "ATIVA":
                status = "open"
            elif status_raw == "A INAUGURAR":
                status = "pending"
            else:
                status = "closed"

            # Horário: combina dias úteis + sábado + domingo
            hora_semana = row.get("2ª a 6ª", "").strip()
            hora_sab    = row.get("SAB", "").strip()
            hora_dom    = row.get("DOM", "").strip()
            horario_parts = []
            if hora_semana: horario_parts.append(f"Seg-Sex {hora_semana}")
            if hora_sab:    horario_parts.append(f"Sáb {hora_sab}")
            if hora_dom:    horario_parts.append(f"Dom {hora_dom}")
            horario = " | ".join(horario_parts)

            ggl_nome = row.get("NOME GGL", "").strip()
            gr_nome  = row.get("NOME GR",  "").strip()
            desig    = desig_idx.get(vd, {})

            loja = {
                "vd":        vd,
                "nome":      row.get("LOJAS", "").strip(),
                "bandeira":  row.get("BANDEIRA", "").strip(),
                "cnpj":      row.get("CNPJ", "").strip(),
                "endereco":  row.get("ENDEREÇO", "").strip(),
                "bairro":    row.get("BAIRRO", "").strip(),
                "cidade":    row.get("CIDADE", "").strip(),
                "estado":    row.get("ESTADO", "").strip(),
                "cep":       row.get("CEP", "").strip(),
                "regiao":    row.get("REGIAO GGL", "").strip(),
                "regiao_gr": row.get("REGIAO GR", "").strip(),
                "regiao_div":row.get("REGIAO DIV", "").strip(),
                "tel":       row.get("TELEFONE1", "").strip(),
                "tel2":      row.get("TELEFONE2", "").strip(),
                "cel":       row.get("CELULAR", "").strip(),
                "email":     row.get("E-MAIL", "").strip(),
                "horario":   horario,
                "status":    status,
                "ggl":       ggl_nome,
                "ggl_tel":   ggl_idx.get(ggl_nome, ""),
                "gr":        gr_nome,
                "gr_tel":    gr_idx.get(gr_nome, ""),
                "mpls":      desig.get("mpls", ""),
                "inn":       desig.get("inn", ""),
                "circuitos": desig.get("circuitos", []),
                "cluster":   row.get("CLUSTER", "").strip(),
                "tipo_loja": row.get("TIPO LOJA", "").strip(),
                "cd":        row.get("CD SUPRIDOR", "").strip(),
            }
            lojas.append(loja)

        return lojas

    # ── API pública ───────────────────────────────────────────────────────────

    def get_lojas(self) -> List[dict]:
        cached = self.cache_manager.get("all_lojas")
        if cached is not None:
            return cached
        lojas = self._load_from_csv()
        if not lojas:
            lojas = self._get_sample_data()
        self.cache_manager.set("all_lojas", lojas)
        return lojas

    def get_loja_by_vd(self, vd: str) -> Optional[dict]:
        """Lookup O(1) por VD."""
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
        loja = self.get_loja_by_vd(vd)
        if loja:
            return {"valido": True, "loja": loja, "mensagem": "VD encontrado"}
        return {"valido": False, "loja": None, "mensagem": f"VD {vd} não encontrado"}

    def buscar_loja(self, termo: str, modo: str = "VD / Designação", lojas: list = None) -> List[dict]:
        if not termo:
            return []
        if lojas is None:
            lojas = self.get_lojas()

        t = termo.strip().lower()
        import re as _re
        t_clean = _re.sub(r"[^a-z0-9]", "", t)
        # VD = apenas dígitos com até 4 caracteres (ex: "318", "2015")
        # Designação = número longo (≥5 dígitos) ou alfanumérico (INN, MPLS)
        e_vd = t.isdigit() and len(t) <= 4
        resultados = []

        for loja in lojas:
            if modo == "VD / Designação":
                if e_vd:
                    # Número curto → match exato de VD apenas
                    match = (t == loja.get("vd", "").lower())
                else:
                    # Número longo ou alfanumérico → busca em MPLS, INN e circuitos
                    def _des_match(des: str) -> bool:
                        d = _re.sub(r"[^a-z0-9]", "", des.lower())
                        return bool(t_clean) and (t_clean == d or d.startswith(t_clean) or t_clean in d)
                    match = (
                        _des_match(loja.get("mpls", ""))
                        or _des_match(loja.get("inn", ""))
                        or any(_des_match(c.get("des", "")) for c in loja.get("circuitos", []))
                    )
            elif modo == "Endereço":
                match = (
                    t in loja.get("endereco", "").lower()
                    or t in loja.get("cidade", "").lower()
                    or t in loja.get("bairro", "").lower()
                    or t in loja.get("cep", "").lower()
                )
            elif modo == "Nome de Loja":
                match = t in loja.get("nome", "").lower()
            else:  # Outra Informação
                blob = " ".join([
                    loja.get("nome",""), loja.get("ggl",""), loja.get("gr",""),
                    loja.get("email",""), loja.get("tel",""), loja.get("cnpj",""),
                    loja.get("cd",""), loja.get("cidade",""), loja.get("estado",""),
                ]).lower()
                match = t in blob

            if match:
                resultados.append(loja)

        # Fuzzy fallback para busca por nome
        if not resultados and FUZZY_AVAILABLE and modo in ("Nome de Loja", "Outra Informação"):
            nomes = [l.get("nome", "") for l in lojas]
            hits = rfprocess.extract(termo, nomes, scorer=fuzz.partial_ratio, limit=5, score_cutoff=65)
            hit_names = {h[0] for h in hits}
            resultados = [l for l in lojas if l.get("nome") in hit_names]

        return resultados

    def get_estados(self) -> List[str]:
        return sorted({l.get("estado", "") for l in self.get_lojas() if l.get("estado")})

    def get_regioes(self) -> List[str]:
        return sorted({l.get("regiao", "") for l in self.get_lojas() if l.get("regiao")})

    # ── Sample data (fallback sem CSVs) ───────────────────────────────────────

    def _get_sample_data(self) -> List[dict]:
        return [
            {"vd":"318","nome":"DSP SANTA BARBARA DOESTE","bandeira":"DSP","cnpj":"61.412.110/0265-45",
             "endereco":"AV DE CILLO,167","bairro":"CENTRO","cidade":"SANTA BARBARA D OESTE",
             "estado":"SP","cep":"13450041","regiao":"SP AMERICANA","regiao_gr":"SP INTERIOR","regiao_div":"SP",
             "tel":"(19)3455-4096","tel2":"","cel":"19998838331","email":"sbdoeste@dpsp.com.br",
             "horario":"Seg-Sex 07 ÀS 23 | Sáb 07 ÀS 23 | Dom 07 ÀS 23",
             "status":"open","ggl":"FERNANDO LUCHINE","ggl_tel":"","gr":"FERNANDA MALAQUIAS","gr_tel":"",
             "mpls":"","inn":"","circuitos":[],"cluster":"AR_G","tipo_loja":"Meio de Quadra","cd":"VD910"},
            {"vd":"322","nome":"DSP SAO CARLOS","bandeira":"DSP","cnpj":"61.412.110/0266-26",
             "endereco":"AV SAO CARLOS,2358","bairro":"CENTRO","cidade":"SAO CARLOS",
             "estado":"SP","cep":"13560002","regiao":"SP ARARAQUARA","regiao_gr":"SP NOROESTE","regiao_div":"SP",
             "tel":"","tel2":"","cel":"","email":"",
             "horario":"","status":"open","ggl":"IVAN OLIVEIRA","ggl_tel":"","gr":"OLIVEIRA JUNIOR","gr_tel":"",
             "mpls":"","inn":"","circuitos":[],"cluster":"","tipo_loja":"","cd":""},
        ]
