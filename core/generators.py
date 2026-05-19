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
    n    = get_n()
    mats = get_mats()
    lista = construir_lista(n, mats, cfg)
    archivos = {}

    # ── Ampliación centros logísticos ─────────────────────────────────────
    if flujo == "Ampliación centros logísticos":

        archivos["Datos_basicos.txt"] = gen_datos_basicos(
            lista, cfg, "vistas_CL"
        )

        archivos["Datos_de_centro.txt"] = gen_datos_centro_CL(lista, cfg)

        for nombre, fn in [
            ("Cadenas_de_distribucion.txt",   gen_cadenas),
            ("Clasificacion_fiscal.txt",       gen_clasificacion_fiscal),
            ("Datos_de_prevision.txt",         gen_datos_prevision),
            ("Lugares_de_almacenamiento.txt",  gen_lugares_almacenamiento),
            ("Area_planific_nec.txt",          gen_area_planificacion),
        ]:
            resultado = fn(lista, cfg)
            if resultado:
                archivos[nombre] = resultado

        resultado = gen_datos_valoracion(lista, cfg, "CL_valoracion")
        if resultado:
            archivos["Datos_valoracion.txt"] = resultado

    # ── Ampliación sucursales ─────────────────────────────────────────────
    elif flujo == "Ampliación sucursales":

        archivos["Datos_basicos.txt"] = gen_datos_basicos(
            lista, cfg, "vistas_SUC"
        )

        archivos["Datos_de_centro.txt"] = gen_datos_centro_SUC(lista, cfg)

        resultado = gen_datos_valoracion_SUC(lista, cfg)
        if resultado:
            archivos["Datos_valoracion.txt"] = resultado

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
