from typing import Any
import streamlit as st


def init_state():

    defaults = {
        "flujo": None,
        "flujo_sel": None,
        "tipo_mat": None,
        "materiales": {},
        "n_mats": 0,
        "configurado": False,
        "centros_seleccionados": [],
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def get_n() -> int:
    return st.session_state.n_mats


def get_mats() -> dict:
    return st.session_state.materiales


def get_val(campo: str, idx: int, default: Any = "") -> Any:
    d = get_mats().get(campo, [])
    return d[idx] if idx < len(d) else default


def _limpiar(value: Any) -> Any:
    """Elimina saltos de línea y normaliza espacios entre palabras."""
    if isinstance(value, str):
        value = value.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
        while "  " in value:
            value = value.replace("  ", " ")
        return value.strip()
    return value


def set_val(campo: str, idx: int, value: Any):
    m = get_mats()
    if campo not in m:
        m[campo] = [""] * get_n()
    while len(m[campo]) < get_n():
        m[campo].append("")
    m[campo][idx] = _limpiar(value)


def fill_all(campo: str, value: Any):
    get_mats()[campo] = [_limpiar(value)] * get_n()


def resolver_mstae(idx: int) -> str:
    val = get_val("MSTAE", idx, True)
    return "/" if (val is True or val == True) else ""


def inicializar_materiales(lineas: list, cfg: dict):
    n = len(lineas)
    st.session_state.n_mats = n

    campos_base = [
        "MATNR", "MAKTX", "MATKL", "PRDHA",
        "VOLUM", "TEXTO_LARGO", "SPART", "KTGRM",
    ]
    for campo in campos_base:
        st.session_state.materiales[campo] = [""] * n

    st.session_state.materiales["MATNR"] = lineas
    st.session_state.materiales["MSTAE"] = [True] * n

    if cfg.get("MTART") == "ZMED":
        st.session_state.materiales["TRAZABLE"] = [True] * n

    for centro in cfg.get("CL_centros", []):
        werks = centro["WERKS"]
        st.session_state.materiales[f"EKGRP_{werks}"] = [""] * n
        st.session_state.materiales[f"TAXIM_{werks}"] = [""] * n

    if cfg.get("ZNOA_incluye_sucursales_en_CL"):
        st.session_state.materiales["TAXIM_SUC_znoa"] = ["1"] * n


def reset_state():
    """Reinicia toda la sesión."""
    st.session_state.configurado = False
    st.session_state.materiales  = {}
    st.session_state.n_mats      = 0
    st.session_state.flujo       = None
    st.session_state.flujo_sel   = None
    st.session_state.tipo_mat    = None
    st.session_state.centros_seleccionados = []


def cargar_desde_excel_preparado(df: "pd.DataFrame", cfg: dict) -> tuple[bool, str]:
    """
    Carga el estado de materiales desde el Excel preparado (hoja PARA_APP).
    Retorna (exito, mensaje_error).
    """
    import pandas as pd

    # Validar MATNRs completos
    sin_matnr = df["MATNR"].isna() | (df["MATNR"].astype(str).str.strip() == "")
    if sin_matnr.any():
        return False, f"{sin_matnr.sum()} material(es) sin MATNR. Completá todos los números antes de subir."

    # Validar tipo de material único
    tipos = df["Tipo material"].dropna().unique()
    if len(tipos) > 1:
        return False, f"El archivo tiene múltiples tipos de material: {', '.join(tipos)}. Separá por tipo y volvé a subir."

    # Validar centros únicos
    centros_por_mat = df["Centros"].dropna().unique()
    if len(centros_por_mat) > 1:
        return False, (
            f"El archivo tiene combinaciones de centros distintas: "
            f"{', '.join(centros_por_mat)}. "
            f"Separalos en archivos distintos para poder subirlos."
        )

    # Parsear centros
    centros_str = centros_por_mat[0] if len(centros_por_mat) == 1 else ""
    centros = [c.strip() for c in centros_str.split("+") if c.strip()]

    # Inicializar estado
    n = len(df)
    st.session_state.n_mats = n
    st.session_state.centros_seleccionados = centros

    campos_base = ["MATNR","MAKTX","MATKL","PRDHA","VOLUM","TEXTO_LARGO","SPART","KTGRM"]
    for campo in campos_base:
        st.session_state.materiales[campo] = [""] * n

    st.session_state.materiales["MSTAE"] = [True] * n

    # MSTAE desde Excel (NO → False, cualquier otra cosa → True)
    if "MSTAE" in df.columns:
        st.session_state.materiales["MSTAE"] = [
            str(v).strip().upper() != "NO"
            for v in df["MSTAE"].tolist()
        ]

    # TRAZABLE: solo para ZMED
    tipo_mat = df["Tipo material"].dropna().iloc[0] if len(df) > 0 else ""
    if tipo_mat == "ZMED":
        if "Trazable" in df.columns:
            st.session_state.materiales["TRAZABLE"] = [
                str(v).strip().upper() != "NO"
                for v in df["Trazable"].tolist()
            ]
        else:
            st.session_state.materiales["TRAZABLE"] = [True] * n

    # Llenar campos desde el Excel
    mapeo = {
        "MATNR":       "MATNR",
        "MAKTX":       "MAKTX",
        "TEXTO_LARGO": "TEXTO_LARGO",
        "MATKL":       "MATKL",
        "PRDHA":       "PRDHA",
        "VOLUM":       "VOLUM",
        "SPART":       "SPART",
        "KTGRM":       "KTGRM",
    }
    for campo_estado, col_excel in mapeo.items():
        if col_excel in df.columns:
            st.session_state.materiales[campo_estado] = [
                str(v).strip() if v is not None and str(v) not in ("nan","None","") else ""
                for v in df[col_excel].tolist()
            ]

    # EKGRP y TAXIM por centro
    for centro in cfg.get("CL_centros", []):
        werks = centro["WERKS"]
        if werks in centros:
            ekgrp_vals = [
                str(v).strip() if v is not None and str(v) not in ("nan","None","") else ""
                for v in df["EKGRP"].tolist()
            ] if "EKGRP" in df.columns else [""] * n
            taxim_vals = [
                str(v).strip() if v is not None and str(v) not in ("nan","None","") else ""
                for v in df["TAXIM"].tolist()
            ] if "TAXIM" in df.columns else [""] * n
            st.session_state.materiales[f"EKGRP_{werks}"] = ekgrp_vals
            st.session_state.materiales[f"TAXIM_{werks}"] = taxim_vals

    # TAXIM_SUC_znoa para ZNOA
    if cfg.get("ZNOA_incluye_sucursales_en_CL"):
        if "TAXIM" in df.columns:
            taxim_vals = [
                str(v).strip() if v is not None and str(v) not in ("nan","None","") else "1"
                for v in df["TAXIM"].tolist()
            ]
            st.session_state.materiales["TAXIM_SUC_znoa"] = taxim_vals
        else:
            st.session_state.materiales["TAXIM_SUC_znoa"] = ["1"] * n

    return True, ""