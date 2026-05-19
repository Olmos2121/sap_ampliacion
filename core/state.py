from typing import Any
import streamlit as st


def init_state():

    defaults = {
        "flujo": None,
        "tipo_mat": None,
        "materiales": {},
        "n_mats": 0,
        "configurado": False,
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


def set_val(campo: str, idx: int, value: Any):
    m = get_mats()
    if campo not in m:
        m[campo] = [""] * get_n()
    while len(m[campo]) < get_n():
        m[campo].append("")
    m[campo][idx] = value


def fill_all(campo: str, value: Any):
    get_mats()[campo] = [value] * get_n()


def resolver_mstae(idx: int) -> str:
    val = get_val("MSTAE", idx, True)
    return "/" if (val is True or val == True) else ""


def inicializar_materiales(lineas: list, cfg: dict):
    """
    Llamado al confirmar los MATNR en el paso 1.
    Inicializa el estado completo de materiales.
    """
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

    # Inicializar campos por centro logístico
    for centro in cfg.get("CL_centros", []):
        werks = centro["WERKS"]
        st.session_state.materiales[f"EKGRP_{werks}"] = [""] * n
        st.session_state.materiales[f"TAXIM_{werks}"] = [""] * n


def reset_state():
    """Reinicia toda la sesión para volver al paso 1."""
    st.session_state.configurado = False
    st.session_state.materiales  = {}
    st.session_state.n_mats      = 0
    st.session_state.flujo       = None
    st.session_state.tipo_mat    = None
