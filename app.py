from pathlib import Path
from io import BytesIO
import streamlit as st
import pandas as pd

from config import TIPOS_MATERIAL, CENTRO_BENEFICIO_MAP, CENTROS_DISPONIBLES

from ui.helpers import load_css
from ui.layout import (
    shell_bar,
    breadcrumb,
    page_title,
    section_open,
    section_close,
)

from core.state import (
    init_state,
    reset_state,
    cargar_desde_excel_preparado,
)
from core.preparar import procesar, _detectar_formato
from core.generators import generar_zip


# ─────────────────────────────────────────────────────────────────────────────
# Configuración de página
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="SAP — Ampliación masiva de materiales",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css("assets/styles.css")
init_state()

shell_bar()

# ─────────────────────────────────────────────────────────────────────────────
# Selector de modo principal
# ─────────────────────────────────────────────────────────────────────────────

if "modo" not in st.session_state:
    st.session_state.modo = "ampliar"

col_m1, col_m2, col_m3 = st.columns([2, 2, 6])
if col_m1.button(
    "📦 Ampliación / Modificación",
    type="primary" if st.session_state.modo == "ampliar" else "secondary",
    use_container_width=True,
):
    st.session_state.modo = "ampliar"
    reset_state()
    st.rerun()
if col_m2.button(
    "⚙️ Preparar materiales",
    type="primary" if st.session_state.modo == "preparar" else "secondary",
    use_container_width=True,
):
    st.session_state.modo = "preparar"
    st.rerun()

st.markdown("")


# ─────────────────────────────────────────────────────────────────────────────
# MODO: PREPARAR MATERIALES
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.modo == "preparar":

    breadcrumb("Preparar materiales")
    page_title("Gestión de materiales", "⚙️ Preparar materiales para la app")

    section_open("Archivos de entrada", "📂")
    st.markdown('<div class="sap-table-label">Excel de altas (hoja ABM)</div>',
                unsafe_allow_html=True)
    archivo_altas = st.file_uploader(
        "altas", type=["xlsx"], label_visibility="collapsed",
        key="up_altas"
    )
    section_close()

    CONV_PATH = Path("Conversion_Materiales_SAP.xlsx")

    if archivo_altas:
        if not CONV_PATH.exists():
            st.error("No se encontró 'Conversion_Materiales_SAP.xlsx' en la carpeta del proyecto.")
            st.stop()

        bytes_altas = archivo_altas.read()

        section_open("Vista previa", "👁")
        try:
            fmt_altas = _detectar_formato(bytes_altas)
            if fmt_altas == "nuevo":
                df_prev = pd.read_excel(BytesIO(bytes_altas), sheet_name="ABM", header=1, dtype=str)
                df_prev["ID_CATEGORIA"] = df_prev["Category2"].str.extract(r"^(J\d{4})", expand=False)
            else:
                df_prev = pd.read_excel(BytesIO(bytes_altas), sheet_name="ABM", header=2, dtype=str)
            df_prev = df_prev[
                df_prev["ID_CATEGORIA"].notna() &
                df_prev["ID_CATEGORIA"].str.match(r"^J\d{4}$", na=False)
            ]
            st.caption(f"{len(df_prev)} materiales detectados en el archivo.")
            df_prev_display = df_prev[["ID_CATEGORIA", "NOMBRE MATERIAL SAP",
                                       "Volumen (CM3)", "E-Commerce", "IVA"]].head(10).copy()
            def _fmt_volumen(v):
                if not v or str(v).strip() in ("", "nan"):
                    return v
                import re
                s = str(v).strip().replace(",", ".")
                m = re.search(r"\d+(\.\d+)?", s)
                if not m:
                    return v
                num = float(m.group())
                return str(int(num)) if num == int(num) else str(num)
            df_prev_display["Volumen (CM3)"] = df_prev_display["Volumen (CM3)"].apply(_fmt_volumen)
            st.dataframe(df_prev_display, use_container_width=True, hide_index=True)
        except Exception as e:
            st.warning(f"No se pudo previsualizar: {e}")
        section_close()

        section_open("Generar", "⚙️")
        if st.button("⚙️ Procesar y descargar", type="primary"):
            with st.spinner("Procesando..."):
                try:
                    bytes_conv = CONV_PATH.read_bytes()
                    excel_out, n_mats, advertencias = procesar(bytes_altas, bytes_conv)

                    st.success(f"✅ {n_mats} materiales procesados.")
                    for av in advertencias:
                        st.warning(av)

                    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
                    st.download_button(
                        label=f"⬇️ Descargar Excel preparado ({n_mats} materiales)",
                        data=excel_out,
                        file_name=f"Materiales_SAP_{ts}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_preparar",
                    )
                except Exception as e:
                    st.error(f"Error al procesar: {e}")
        section_close()

    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# MODO: AMPLIACIÓN / MODIFICACIÓN — Paso 1: elegir operación
# ─────────────────────────────────────────────────────────────────────────────

breadcrumb("Ampliación / Modificación")
page_title("Gestión de materiales", "Ampliación / Modificación masiva")

if "flujo_sel" not in st.session_state:
    st.session_state.flujo_sel = None

FLUJOS = {
    "Ampliación centros logísticos":     {"icon": "🏭", "desc": "Hasta 8 vistas"},
    "Ampliación sucursales":             {"icon": "🏪", "desc": "Todas las sucursales"},
    "Ampliación sucursales específicas": {"icon": "🏪", "desc": "Sucursales seleccionadas"},
    "Modificación datos básicos":        {"icon": "✏️",  "desc": "1 vista"},
}

section_open("1. Tipo de operación", "📋")
cols_flujo = st.columns(4)
for i, (nombre, info) in enumerate(FLUJOS.items()):
    activo = st.session_state.flujo_sel == nombre
    if cols_flujo[i].button(
        f"{info['icon']}  {nombre}",
        key=f"op_{nombre}",
        use_container_width=True,
        type="primary" if activo else "secondary",
    ):
        if st.session_state.flujo_sel != nombre:
            st.session_state.flujo_sel = nombre
            st.session_state.sucursales_especificas = []
        st.rerun()
    cols_flujo[i].caption(info["desc"])
section_close()

if not st.session_state.flujo_sel:
    st.info("Seleccioná una operación para continuar.")
    st.stop()

flujo_detectado = st.session_state.flujo_sel

# ─────────────────────────────────────────────────────────────────────────────
# Selector de sucursales específicas
# ─────────────────────────────────────────────────────────────────────────────

if flujo_detectado == "Ampliación sucursales específicas":
    section_open("2. Sucursales a ampliar", "🏪")
    sucursales_disponibles = sorted(CENTRO_BENEFICIO_MAP.keys())
    sucursales_sel = st.multiselect(
        "Seleccioná las sucursales:",
        options=sucursales_disponibles,
        default=st.session_state.get("sucursales_especificas", []),
        key="ms_sucursales",
    )
    st.session_state.sucursales_especificas = sucursales_sel
    if not sucursales_sel:
        st.warning("⚠️ Seleccioná al menos una sucursal para continuar.")
    else:
        st.caption(f"{len(sucursales_sel)} sucursal(es): {', '.join(sucursales_sel)}")
    section_close()

    if not st.session_state.get("sucursales_especificas"):
        st.stop()
else:
    st.session_state.sucursales_especificas = []

# ─────────────────────────────────────────────────────────────────────────────
# Subir archivo preparado
# ─────────────────────────────────────────────────────────────────────────────

paso_archivo = "3." if flujo_detectado == "Ampliación sucursales específicas" else "2."

section_open(f"{paso_archivo} Archivo preparado (Excel)", "📂")
st.caption(
    "Subí el Excel generado por 'Preparar materiales' con los MATNR y todos los datos completados."
)
archivo_prep = st.file_uploader(
    "prep", type=["xlsx"], label_visibility="collapsed",
    key=f"up_prep_{flujo_detectado}",
)
section_close()

if not archivo_prep:
    st.info("📂 Subí el archivo preparado para continuar.")
    st.stop()

# ── Leer y validar ────────────────────────────────────────────────────────────

try:
    df_prep = pd.read_excel(archivo_prep, sheet_name="PARA_APP", dtype=str)
except Exception as e:
    st.error(f"Error al leer el archivo: {e}")
    st.stop()

cols_requeridas = {"MATNR", "Tipo material"}
faltantes = cols_requeridas - set(df_prep.columns)
if faltantes:
    st.error(f"El archivo no tiene las columnas requeridas: {', '.join(sorted(faltantes))}.")
    st.stop()

sin_matnr = df_prep["MATNR"].isna() | (df_prep["MATNR"].astype(str).str.strip() == "")
if sin_matnr.any():
    st.error(f"❌ {sin_matnr.sum()} material(es) sin MATNR.")
    st.stop()

tipos = df_prep["Tipo material"].dropna().unique()
if len(tipos) == 0:
    st.error("No se detectó ningún tipo de material en el archivo.")
    st.stop()
if len(tipos) > 1:
    st.error(f"El archivo tiene múltiples tipos de material: {', '.join(tipos)}. Separalos por tipo.")
    st.stop()
tipo_detectado = tipos[0].strip()
if tipo_detectado not in TIPOS_MATERIAL:
    st.error(f"Tipo de material '{tipo_detectado}' no reconocido.")
    st.stop()

TIPOS_POR_FLUJO = {
    "Ampliación centros logísticos":     list(TIPOS_MATERIAL.keys()),
    "Ampliación sucursales":             ["ZMED", "ZNOM", "ZINS", "ZSER_C", "ZSER_NC"],
    "Ampliación sucursales específicas": ["ZMED", "ZNOM", "ZINS", "ZSER_C", "ZSER_NC"],
    "Modificación datos básicos":        list(TIPOS_MATERIAL.keys()),
}
if tipo_detectado not in TIPOS_POR_FLUJO[flujo_detectado]:
    st.error(f"El tipo '{tipo_detectado}' no es compatible con '{flujo_detectado}'.")
    st.stop()

cfg = TIPOS_MATERIAL[tipo_detectado]

# ── Vista previa ─────────────────────────────────────────────────────────────

paso_prev = "4." if flujo_detectado == "Ampliación sucursales específicas" else "3."

section_open(f"{paso_prev} Vista previa", "👁")
cols_preview = [c for c in ["MATNR", "Tipo material", "MAKTX", "Centros", "EKGRP", "TAXIM"] if c in df_prep.columns]
st.caption(f"**{len(df_prep)} materiales** · Tipo: **{tipo_detectado}** · Operación: **{flujo_detectado}**")
st.dataframe(df_prep[cols_preview].head(10), use_container_width=True, hide_index=True)
section_close()

# ── Generar ───────────────────────────────────────────────────────────────────

paso_gen = "5." if flujo_detectado == "Ampliación sucursales específicas" else "4."

section_open(f"{paso_gen} Generar archivos SAP", "⚙️")

if st.button("⚙️ Generar y descargar .txt", type="primary", use_container_width=True):
    with st.spinner("Generando archivos..."):
        try:
            exito, error = cargar_desde_excel_preparado(df_prep, cfg)
            if not exito:
                st.error(error)
                st.stop()

            st.session_state.tipo_mat = tipo_detectado
            st.session_state.flujo    = flujo_detectado

            zip_bytes, archivos = generar_zip(flujo_detectado, cfg)

            st.success(f"✅ {len(df_prep)} materiales · {len(archivos)} archivo(s) generado(s).")
            for nombre in archivos:
                st.caption(f"  📄 {nombre}")

            ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
            st.download_button(
                label=f"⬇️ Descargar ZIP ({len(archivos)} archivos)",
                data=zip_bytes,
                file_name=f"SAP_{tipo_detectado}_{ts}.zip",
                mime="application/zip",
                key="dl_zip",
            )
        except Exception as e:
            st.error(f"Error al generar: {e}")
            raise e

section_close()