import zipfile
from io import BytesIO

from txt_generator import (
    gen_datos_basicos,
    gen_datos_centro_CL,
    gen_datos_centro_SUC,
    gen_cadenas,
    gen_clasificacion_fiscal,
    gen_datos_prevision,
    gen_lugares_almacenamiento,
    gen_area_planificacion,
    gen_datos_valoracion,
    gen_datos_valoracion_SUC,
    gen_datos_centro_ZNOA,
    gen_datos_valoracion_ZNOA,
)

from core.state import get_mats, get_n, resolver_mstae


def construir_lista(n: int, mats: dict, cfg: dict) -> list[dict]:
    """
    Convierte el estado de materiales (listas por campo) en una
    lista de dicts, uno por material, lista para pasar a los generadores.
    """
    lista = []

    for i in range(n):
        m = {
            campo: (vals[i] if i < len(vals) else "")
            for campo, vals in mats.items()
        }

        # Resolver MSTAE: True → "/" (activo), False → "" (bloqueado)
        m["MSTAE"] = resolver_mstae(i)

        # SPART: usar el del material o el fijo del tipo
        if not m.get("SPART"):
            m["SPART"] = cfg.get("SPART", "")

        # TEXTO_LARGO: default a descripción si está vacío
        if not m.get("TEXTO_LARGO"):
            m["TEXTO_LARGO"] = m.get("MAKTX", "")

        lista.append(m)

    return lista


def generar_zip(flujo: str, cfg: dict) -> tuple[bytes, dict]:
    """
    Genera todos los .txt correspondientes al flujo y tipo de material,
    los empaqueta en un ZIP en memoria y lo devuelve.
    Retorna (bytes_del_zip, dict_nombre→bytes_del_txt).
    """
    import streamlit as st
    centros = st.session_state.get("centros_seleccionados", None) or None

    n    = get_n()
    mats = get_mats()
    lista = construir_lista(n, mats, cfg)
    archivos = {}

    # ── Ampliación centros logísticos ─────────────────────────────────────
    if flujo == "Ampliación centros logísticos":

        archivos["Datos_basicos.txt"] = gen_datos_basicos(
            lista, cfg, "vistas_CL"
        )

        if cfg.get("ZNOA_incluye_sucursales_en_CL"):
            archivos["Datos_de_centro.txt"] = gen_datos_centro_ZNOA(lista, cfg, centros)
        else:
            archivos["Datos_de_centro.txt"] = gen_datos_centro_CL(lista, cfg, centros)

        r = gen_cadenas(lista, cfg, centros)
        if r: archivos["Cadenas_de_distribucion.txt"] = r

        r = gen_clasificacion_fiscal(lista, cfg)
        if r: archivos["Clasificacion_fiscal.txt"] = r

        if centros is None or "A130" in centros:
            r = gen_datos_prevision(lista, cfg)
            if r: archivos["Datos_de_prevision.txt"] = r
            r = gen_area_planificacion(lista, cfg)
            if r: archivos["Area_planific_nec.txt"] = r

        r = gen_lugares_almacenamiento(lista, cfg, centros)
        if r: archivos["Lugares_de_almacenamiento.txt"] = r

        if cfg.get("ZNOA_incluye_sucursales_en_CL"):
            archivos["Datos_valoracion.txt"] = gen_datos_valoracion_ZNOA(lista, cfg, centros)
        else:
            r = gen_datos_valoracion(lista, cfg, "CL_valoracion", centros)
            if r: archivos["Datos_valoracion.txt"] = r
    
    # ── Ampliación sucursales ─────────────────────────────────────────────
    elif flujo == "Ampliación sucursales":

        archivos["Datos_basicos.txt"] = gen_datos_basicos(
            lista, cfg, "vistas_SUC"
        )

        archivos["Datos_de_centro.txt"] = gen_datos_centro_SUC(lista, cfg)

        r = gen_datos_valoracion_SUC(lista, cfg)
        if r: archivos["Datos_valoracion.txt"] = r

    # ── Modificación datos básicos ────────────────────────────────────────
    elif flujo == "Modificación datos básicos":

        archivos["Datos_basicos.txt"] = gen_datos_basicos(
            lista, cfg, "vistas_MOD"
        )

    # ── Empaquetar en ZIP ─────────────────────────────────────────────────
    buf = BytesIO()

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for nombre, contenido in archivos.items():
            zf.writestr(nombre, contenido)

    buf.seek(0)
    return buf.getvalue(), archivos