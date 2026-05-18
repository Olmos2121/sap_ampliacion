import streamlit as st
import pandas as pd
import zipfile
from io import BytesIO

from config import TIPOS_MATERIAL
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

st.set_page_config(
    page_title="SAP — Ampliación masiva de materiales",
    page_icon="📦",
    layout="wide",
)

st.title("📦 SAP — Ampliación masiva de materiales")

# =============================================================================
# SIDEBAR — selección de flujo y tipo de material
# =============================================================================
with st.sidebar:
    st.header("Configuración")
    flujo = st.selectbox(
        "Flujo",
        ["Ampliación centros logísticos", "Ampliación sucursales", "Modificación datos básicos"],
    )
    tipo_mat = st.selectbox(
        "Tipo de material",
        list(TIPOS_MATERIAL.keys()),
        format_func=lambda x: x.replace("_"," "),
    )
    cfg = TIPOS_MATERIAL[tipo_mat]

    st.divider()
    st.caption("Los archivos .txt generados se copian directamente en SAP.")


# =============================================================================
# Definición dinámica de columnas según flujo y tipo de material
# =============================================================================
def get_columnas(flujo: str, tipo_mat: str, cfg: dict) -> list[dict]:
    """
    Devuelve lista de dicts con la definición de cada columna del formulario:
      {
        "campo":   nombre interno (clave del dict de material),
        "label":   lo que ve el usuario,
        "tipo":    "texto" | "numero" | "select" | "checkbox",
        "opciones": [...] (solo si tipo == "select"),
        "default": valor por defecto,
      }
    """
    cols = []

    # MATNR siempre
    cols.append({"campo": "MATNR", "label": "Nro. material (MATNR)", "tipo": "texto", "default": ""})

    if flujo == "Ampliación centros logísticos":
        cols.append({"campo": "MAKTX",      "label": "Descripción",           "tipo": "texto",   "default": ""})
        cols.append({"campo": "MATKL",      "label": "Grupo de productos (MATKL)", "tipo": "texto", "default": ""})
        cols.append({"campo": "PRDHA",      "label": "Jerarquía de productos (PRDHA)", "tipo": "texto", "default": ""})
        cols.append({"campo": "TEXTO_LARGO","label": "Texto largo",            "tipo": "texto",   "default": ""})

        # SPART con opciones solo para ZNOM
        if "SPART_opciones" in cfg:
            cols.append({"campo": "SPART", "label": "Partición (SPART)", "tipo": "select",
                         "opciones": cfg["SPART_opciones"], "default": cfg["SPART_opciones"][0]})

        # VOLUM solo si el tipo lo usa
        if cfg.get("VOLEH"):
            cols.append({"campo": "VOLUM", "label": "Volumen (VOLUM)", "tipo": "numero", "default": ""})

        # EKGRP y TAXIM por cada centro logístico (si tiene opciones)
        for centro in cfg.get("CL_centros", []):
            werks = centro["WERKS"]
            if "ekgrp_opciones" in centro:
                cols.append({
                    "campo": f"EKGRP_{werks}",
                    "label": f"Grupo de compra {werks} (EKGRP)",
                    "tipo": "select",
                    "opciones": centro["ekgrp_opciones"],
                    "default": centro["ekgrp_opciones"][0],
                })
            if "taxim_opciones" in centro:
                cols.append({
                    "campo": f"TAXIM_{werks}",
                    "label": f"Ind. impuestos {werks} (TAXIM)",
                    "tipo": "select",
                    "opciones": centro["taxim_opciones"],
                    "default": centro["taxim_opciones"][0],
                })

        # KTGRM para cadenas
        if cfg.get("CL_cadenas") and cfg.get("CL_ktgrm_opciones"):
            cols.append({
                "campo": "KTGRM",
                "label": "Grupo de imputación (KTGRM)",
                "tipo": "select",
                "opciones": cfg["CL_ktgrm_opciones"],
                "default": cfg["CL_ktgrm_opciones"][0],
            })

        # Bloqueo de material
        cols.append({"campo": "MSTAE", "label": "Bloquear material", "tipo": "checkbox", "default": False})

    elif flujo == "Ampliación sucursales":
        # Para sucursales solo se necesita MATNR (el resto es fijo del mapa de centros)
        pass  # MATNR ya está

    elif flujo == "Modificación datos básicos":
        mod_campos = cfg.get("MOD_campos", [])
        if "MAKTX" in mod_campos:
            cols.append({"campo": "MAKTX", "label": "Descripción (MAKTX)", "tipo": "texto", "default": ""})
        if "PRDHA" in mod_campos:
            cols.append({"campo": "PRDHA", "label": "Jerarquía (PRDHA)", "tipo": "texto", "default": ""})
        if "VOLUM" in mod_campos:
            cols.append({"campo": "VOLUM", "label": "Volumen (VOLUM)", "tipo": "numero", "default": ""})
        if "TEXTO_LARGO" in mod_campos:
            cols.append({"campo": "TEXTO_LARGO", "label": "Texto largo", "tipo": "texto", "default": ""})
        if "MSTAE" in mod_campos:
            cols.append({"campo": "MSTAE", "label": "Bloquear material", "tipo": "checkbox", "default": False})

    return cols


# =============================================================================
# Tabla de ingreso de materiales
# =============================================================================
columnas = get_columnas(flujo, tipo_mat, cfg)

st.subheader(f"{flujo} — {tipo_mat.replace('_',' ')}")

# Descripciones de vistas que se van a generar
with st.expander("📋 Vistas que se generarán", expanded=False):
    if flujo == "Ampliación centros logísticos":
        vistas_info = {
            "Datos básicos": "Siempre",
            "Datos de centro": "Siempre",
            "Cadenas de distribución": "✅" if cfg.get("CL_cadenas") else "No aplica",
            "Clasificación fiscal": "✅" if cfg.get("CL_fiscal") else "No aplica",
            "Datos de previsión": "✅" if cfg.get("CL_prevision") else "No aplica",
            "Lugares de almacenamiento": "✅" if cfg.get("CL_lugares") else "No aplica",
            "Área planif.nec.": "✅" if cfg.get("CL_area_planif") else "No aplica",
            "Datos de valoración": "✅" if cfg.get("CL_valoracion") else "No aplica",
        }
    elif flujo == "Ampliación sucursales":
        vistas_info = {
            "Datos básicos": "Siempre (solo vista almacenamiento)",
            "Datos de centro": f"{'✅ con campos extra' if cfg.get('SUC_datos_centro') else '✅ solo sociedad/beneficio'}",
            "Datos de valoración": "✅" if cfg.get("SUC_valoracion") else "No aplica",
        }
    else:
        vistas_info = {"Datos básicos": "Siempre (solo campos modificables)"}

    for vista, estado in vistas_info.items():
        st.markdown(f"- **{vista}**: {estado}")

# ─── Estado de la tabla en session_state ─────────────────────────────────────
tabla_key = f"tabla_{flujo}_{tipo_mat}"
if tabla_key not in st.session_state:
    # Fila vacía por defecto
    fila_default = {}
    for c in columnas:
        if c["tipo"] == "checkbox":
            fila_default[c["campo"]] = c["default"]
        else:
            fila_default[c["campo"]] = c.get("default", "")
    st.session_state[tabla_key] = [fila_default.copy()]

materiales_estado = st.session_state[tabla_key]

# ─── Renderizado fila por fila ────────────────────────────────────────────────
st.markdown("**Ingresá los materiales:**")

# Encabezados de columnas
header_cols = st.columns([3] * len(columnas) + [1])
for i, c in enumerate(columnas):
    header_cols[i].markdown(f"<small><b>{c['label']}</b></small>", unsafe_allow_html=True)
header_cols[-1].markdown("<small><b>Acción</b></small>", unsafe_allow_html=True)

filas_a_eliminar = []
for idx, fila in enumerate(materiales_estado):
    row_cols = st.columns([3] * len(columnas) + [1])
    for i, c in enumerate(columnas):
        campo = c["campo"]
        widget_key = f"{tabla_key}_{idx}_{campo}"

        if c["tipo"] == "texto":
            val = row_cols[i].text_input(
                label=campo, value=fila.get(campo, ""),
                key=widget_key, label_visibility="collapsed"
            )
        elif c["tipo"] == "numero":
            val = row_cols[i].text_input(
                label=campo, value=str(fila.get(campo, "")),
                key=widget_key, label_visibility="collapsed"
            )
        elif c["tipo"] == "select":
            opciones = c["opciones"]
            current = fila.get(campo, opciones[0])
            idx_sel = opciones.index(current) if current in opciones else 0
            val = row_cols[i].selectbox(
                label=campo, options=opciones, index=idx_sel,
                key=widget_key, label_visibility="collapsed"
            )
        elif c["tipo"] == "checkbox":
            val = row_cols[i].checkbox(
                label=campo, value=fila.get(campo, False),
                key=widget_key, label_visibility="collapsed"
            )
        else:
            val = ""

        materiales_estado[idx][campo] = val

    if row_cols[-1].button("🗑", key=f"del_{tabla_key}_{idx}", help="Eliminar fila"):
        filas_a_eliminar.append(idx)

# Eliminar filas marcadas
for idx in sorted(filas_a_eliminar, reverse=True):
    materiales_estado.pop(idx)
st.session_state[tabla_key] = materiales_estado

# ─── Botón agregar fila ───────────────────────────────────────────────────────
col_add, col_gen, col_info = st.columns([2, 2, 6])
if col_add.button("➕ Agregar material"):
    fila_nueva = {}
    for c in columnas:
        if c["tipo"] == "checkbox":
            fila_nueva[c["campo"]] = c["default"]
        else:
            # Heredar valores de selects de la última fila
            ultima = materiales_estado[-1] if materiales_estado else {}
            fila_nueva[c["campo"]] = ultima.get(c["campo"], c.get("default","")) if c["tipo"] == "select" else c.get("default","")
    materiales_estado.append(fila_nueva)
    st.session_state[tabla_key] = materiales_estado
    st.rerun()

col_info.caption(f"{len(materiales_estado)} material(es) cargado(s)")


# =============================================================================
# Procesamiento del checkbox MSTAE → valor SAP
# =============================================================================
def resolver_mstae(m: dict) -> str:
    """checkbox True = NO bloquea (/), False = bloquea (vacío)"""
    val = m.get("MSTAE", False)
    if isinstance(val, bool):
        return "/" if val else ""
    return str(val)


# =============================================================================
# Generación de archivos
# =============================================================================
st.divider()

if col_gen.button("⚙️ Generar archivos .txt", type="primary"):

    # Validar que hay al menos un material con MATNR
    mats_validos = [m for m in materiales_estado if str(m.get("MATNR","")).strip()]
    if not mats_validos:
        st.error("⚠️ Ingresá al menos un número de material (MATNR).")
        st.stop()

    # Normalizar MSTAE
    for m in mats_validos:
        m["MSTAE"] = resolver_mstae(m)

    archivos = {}  # nombre_archivo → bytes

    # ── Centros logísticos ────────────────────────────────────────────────────
    if flujo == "Ampliación centros logísticos":

        archivos["Datos_basicos.txt"] = gen_datos_basicos(mats_validos, cfg, "vistas_CL")
        archivos["Datos_de_centro.txt"] = gen_datos_centro_CL(mats_validos, cfg)

        cad = gen_cadenas(mats_validos, cfg)
        if cad:
            archivos["Cadenas_de_distribucion.txt"] = cad

        fisc = gen_clasificacion_fiscal(mats_validos, cfg)
        if fisc:
            archivos["Clasificacion_fiscal.txt"] = fisc

        prev = gen_datos_prevision(mats_validos, cfg)
        if prev:
            archivos["Datos_de_prevision.txt"] = prev

        lug = gen_lugares_almacenamiento(mats_validos, cfg)
        if lug:
            archivos["Lugares_de_almacenamiento.txt"] = lug

        area = gen_area_planificacion(mats_validos, cfg)
        if area:
            archivos["Area_planific_nec.txt"] = area

        val = gen_datos_valoracion(mats_validos, cfg, "CL_valoracion")
        if val:
            archivos["Datos_valoracion.txt"] = val

    # ── Sucursales ────────────────────────────────────────────────────────────
    elif flujo == "Ampliación sucursales":

        archivos["Datos_basicos.txt"] = gen_datos_basicos(mats_validos, cfg, "vistas_SUC")
        archivos["Datos_de_centro.txt"] = gen_datos_centro_SUC(mats_validos, cfg)

        val_suc = gen_datos_valoracion_SUC(mats_validos, cfg)
        if val_suc:
            archivos["Datos_valoracion.txt"] = val_suc

    # ── Modificación ──────────────────────────────────────────────────────────
    elif flujo == "Modificación datos básicos":
        archivos["Datos_basicos.txt"] = gen_datos_basicos(mats_validos, cfg, "vistas_MOD")

    # ── Empaquetar en ZIP ─────────────────────────────────────────────────────
    zip_buf = BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for nombre, contenido in archivos.items():
            zf.writestr(nombre, contenido)
    zip_buf.seek(0)

    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
    nombre_zip = f"SAP_{tipo_mat}_{flujo[:3].strip()}_{ts}.zip"

    st.success(f"✅ {len(archivos)} archivo(s) generado(s) con {len(mats_validos)} material(es).")

    # Mostrar preview de cada archivo
    with st.expander("👁 Preview de archivos generados"):
        for nombre, contenido in archivos.items():
            st.markdown(f"**{nombre}**")
            lineas = contenido.decode("utf-8").split("\r\n")
            preview = "\n".join(lineas[:min(6, len(lineas))])
            st.code(preview, language=None)

    st.download_button(
        label=f"⬇️ Descargar ZIP ({len(archivos)} archivos)",
        data=zip_buf.getvalue(),
        file_name=nombre_zip,
        mime="application/zip",
    )
