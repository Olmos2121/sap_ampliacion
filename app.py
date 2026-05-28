from pathlib import Path
import streamlit as st
import pandas as pd

from config import TIPOS_MATERIAL, CENTRO_BENEFICIO_MAP
from config import TIPOS_MATERIAL, CENTRO_BENEFICIO_MAP, CENTROS_DISPONIBLES

from ui.helpers import load_css
from ui.layout import (
    shell_bar,
    breadcrumb,
    page_title,
    context_bar,
    section_open,
    section_close,
    section_header_inline,
)
from ui.components import (
    status_bar,
    bloque_fijos,
    campo_editable,
    simple_table,
    section_message,
    barra_generacion,
)

from core.state import (
    init_state,
    get_n,
    get_mats,
    inicializar_materiales,
    reset_state,
)
from core.preparar import procesar
from core.validators import validar
from core.generators import generar_zip
from core.tabs import tabs_para_flujo


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


# ─────────────────────────────────────────────────────────────────────────────
# Shell bar (siempre visible)
# ─────────────────────────────────────────────────────────────────────────────

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
    st.caption(
        "Subí el Excel de altas que recibís del otro área y la tabla de conversión. "
        "El resultado es un Excel listo para pegar en la app de ampliación."
    )

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
        section_open("Vista previa", "👁")
        try:
            df_prev = pd.read_excel(archivo_altas, sheet_name="ABM", header=2, dtype=str)
            df_prev = df_prev[
                df_prev["ID_CATEGORIA"].notna() &
                df_prev["ID_CATEGORIA"].str.match(r"^J\d{4}$", na=False)
            ]
            st.caption(f"{len(df_prev)} materiales detectados en el archivo.")
            st.dataframe(
                df_prev[["ID_CATEGORIA", "NOMBRE MATERIAL SAP",
                          "Volumen (CM3)", "E-Commerce", "IVA"]].head(10),
                use_container_width=True, hide_index=True,
            )
            archivo_altas.seek(0)
        except Exception as e:
            st.warning(f"No se pudo previsualizar: {e}")
        section_close()

        section_open("Generar", "⚙️")
        if st.button("⚙️ Procesar y descargar", type="primary"):
            with st.spinner("Procesando..."):
                try:
                    bytes_altas = archivo_altas.read()
                    bytes_conv  = CONV_PATH.read_bytes()
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
# PASO 1 — Configuración inicial
# ─────────────────────────────────────────────────────────────────────────────

if not st.session_state.configurado:

    breadcrumb("Nueva operación")
    page_title("Gestión de materiales", "Nueva operación masiva")

    # ── Fila superior: 3 selectores ──────────────────────────────────────
    col_op, col_mat, col_centros = st.columns([1, 1, 1], gap="medium")

    # ── Columna 1: Tipo de operación ──────────────────────────────────────
    with col_op:
        section_open("1. Tipo de operación", "📋")
        FLUJOS = {
            "Ampliación centros logísticos": {"icon": "🏭", "desc": "Hasta 8 vistas"},
            "Ampliación sucursales":         {"icon": "🏪", "desc": "2–3 vistas"},
            "Modificación datos básicos":    {"icon": "✏️",  "desc": "1 vista"},
        }
        for nombre, info in FLUJOS.items():
            activo = st.session_state.flujo == nombre
            if st.button(
                f"{info['icon']}  {nombre}",
                key=f"op_{nombre}",
                use_container_width=True,
                type="primary" if activo else "secondary",
            ):
                if st.session_state.flujo != nombre:
                    st.session_state.flujo              = nombre
                    st.session_state.tipo_mat           = None
                    st.session_state.materiales         = {}
                    st.session_state.n_mats             = 0
                    st.session_state.centros_seleccionados = []
                st.rerun()
            st.caption(info["desc"])
        section_close()

    # ── Columna 2: Tipo de material ───────────────────────────────────────
    with col_mat:
        section_open("2. Tipo de material", "🏷️")
        if st.session_state.flujo:
            TIPOS_POR_FLUJO = {
                "Ampliación centros logísticos": list(TIPOS_MATERIAL.keys()),
                "Ampliación sucursales":         ["ZMED", "ZNOM", "ZINS"],
                "Modificación datos básicos":    list(TIPOS_MATERIAL.keys()),
            }
            tipos_disp = TIPOS_POR_FLUJO[st.session_state.flujo]
            cols_t = st.columns(2)
            for i, t in enumerate(tipos_disp):
                activo = st.session_state.tipo_mat == t
                if cols_t[i % 2].button(
                    t.replace("_", " "),
                    key=f"chip_{t}",
                    type="primary" if activo else "secondary",
                    use_container_width=True,
                ):
                    if st.session_state.tipo_mat != t:
                        st.session_state.tipo_mat           = t
                        st.session_state.materiales         = {}
                        st.session_state.n_mats             = 0
                        st.session_state.centros_seleccionados = []
                    st.rerun()
        else:
            st.caption("Seleccioná una operación primero.")
        section_close()

    # ── Columna 3: Centros logísticos ─────────────────────────────────────
    with col_centros:
        section_open("3. Centros logísticos", "📍")
        es_CL = st.session_state.flujo == "Ampliación centros logísticos"
        if es_CL and st.session_state.tipo_mat:
            centros_disp = CENTROS_DISPONIBLES.get(st.session_state.tipo_mat, [])
            st.caption("Seleccioná en qué centros ampliar.")
            seleccionados = []
            for centro in centros_disp:
                activo = centro in st.session_state.centros_seleccionados
                if st.button(
                    f"{'✅' if activo else '⬜'}  {centro}",
                    key=f"btn_centro_{centro}",
                    use_container_width=True,
                    type="primary" if activo else "secondary",
                ):
                    nuevos = list(st.session_state.centros_seleccionados)
                    if centro in nuevos:
                        nuevos.remove(centro)
                    else:
                        nuevos.append(centro)
                    st.session_state.centros_seleccionados = nuevos
                    st.rerun()
            if not st.session_state.centros_seleccionados:
                st.caption("⚠️ Seleccioná al menos un centro.")
        elif not es_CL and st.session_state.flujo:
            st.caption("No aplica para este flujo.")
        else:
            st.caption("Seleccioná operación y tipo primero.")
        section_close()

    # ── Fila inferior: MATNR + Continuar ─────────────────────────────────
    if st.session_state.flujo and st.session_state.tipo_mat:
        section_open("Números de material (MATNR)", "🔢")
        st.caption("Copiá y pegá desde Excel (una columna, un número por línea).")

        col_area, col_btn = st.columns([4, 1])

        with col_area:
            texto_matnr = st.text_area(
                label="matnr_input",
                label_visibility="collapsed",
                placeholder="4000039050\n4000038251\n4000038252\n...",
                height=120,
                key="input_matnr",
            )

        lineas_preview = [
            l.strip()
            for l in texto_matnr.replace("\t", "\n").splitlines()
            if l.strip()
        ]

        with col_btn:
            st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
            sin_centros = (
                st.session_state.flujo == "Ampliación centros logísticos"
                and not st.session_state.centros_seleccionados
            )
            if st.button("Continuar →", type="primary", use_container_width=True,
                         disabled=sin_centros or not lineas_preview):
                cfg_tmp = TIPOS_MATERIAL[st.session_state.tipo_mat]
                inicializar_materiales(lineas_preview, cfg_tmp)
                st.session_state.configurado = True
                st.rerun()
            st.caption(f"{len(lineas_preview)} material(es)")

        section_close()

    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# PASO 2 — Formulario por vistas
# ─────────────────────────────────────────────────────────────────────────────

flujo    = st.session_state.flujo
tipo_mat = st.session_state.tipo_mat
cfg      = TIPOS_MATERIAL[tipo_mat]
n        = get_n()
mats     = get_mats()
centros_sel = st.session_state.get("centros_seleccionados", [])

# Breadcrumb y título
breadcrumb(flujo)
page_title(
    f"Gestión de materiales — {tipo_mat.replace('_', ' ')}",
    f"{flujo}",
)

# Barra de contexto + botón volver
col_ctx, col_back = st.columns([8, 2])
col_ctx.markdown("")          # separador visual
context_bar(tipo_mat, flujo, n)

if col_back.button("← Nueva operación", use_container_width=True):
    reset_state()
    st.rerun()

# ─── Tabs ────────────────────────────────────────────────────────────────────

nombres_tabs = tabs_para_flujo(flujo, cfg, centros_sel)
tabs = st.tabs(nombres_tabs)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: DATOS BÁSICOS
# ══════════════════════════════════════════════════════════════════════════════

with tabs[0]:

    section_open("Datos básicos del material", "📄")

    if flujo == "Ampliación sucursales":
        section_message(
            "info",
            "Para sucursales la vista Datos básicos activa únicamente el flag "
            "de almacenamiento. No se requieren campos adicionales.",
        )
        simple_table({
            "MATNR": mats.get("MATNR", [""]*n),
            "Vista almacenamiento": ["X"] * n,
        })

    else:
        campo_editable(
            "Descripción", "MAKTX", tecnico="MAKTX",
            ayuda="Nombre del material tal como aparecerá en SAP.",
        )

        if flujo == "Ampliación centros logísticos":
            campo_editable(
                "Grupo de productos", "MATKL", tecnico="MATKL",
                ayuda="Ej: J0101, J0104, J0606.",
            )
            campo_editable(
                "Jerarquía de productos", "PRDHA", tecnico="PRDHA",
                ayuda="Ej: J010109, J010405.",
            )
            if cfg.get("VOLEH"):
                campo_editable(
                    "Volumen", "VOLUM", tipo="numero", tecnico="VOLUM",
                    ayuda=f"En {cfg.get('VOLEH', 'CM3')}.",
                )
            if "SPART_opciones" in cfg:
                campo_editable(
                    "Partición", "SPART", tipo="select", tecnico="SPART",
                    opciones=cfg["SPART_opciones"],
                )

        if flujo == "Modificación datos básicos":
            mod_campos = cfg.get("MOD_campos", [])
            if "PRDHA" in mod_campos:
                campo_editable(
                    "Jerarquía de productos", "PRDHA", tecnico="PRDHA",
                    ayuda="Ej: J010109, J010405.",
                )
            if "VOLUM" in mod_campos:
                campo_editable(
                    "Volumen", "VOLUM", tipo="numero", tecnico="VOLUM",
                    ayuda=f"En {cfg.get('VOLEH', 'CM3')}.",
                )

        campo_editable(
            "Texto largo", "TEXTO_LARGO",
            ayuda="Si se deja vacío se usa la descripción (MAKTX).",
        )
        campo_editable(
            "Estado del material", "MSTAE", tipo="checkbox", tecnico="MSTAE",
        )

        # Valores fijos
        fijos = {
            k: v for k, v in cfg.items()
            if k in ("MTART","SPART","XCHPF","MTPOS","VOLEH",
                      "EKWSL","TRAGR","IPRKZ","MHDRZ","SERIAL")
            and v
        }
        if fijos:
            bloque_fijos("Datos básicos", fijos)

    section_close()
    barra_generacion("basicos", flujo, cfg)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: DATOS DE CENTRO
# ══════════════════════════════════════════════════════════════════════════════

if "Datos de centro" in nombres_tabs:

    with tabs[nombres_tabs.index("Datos de centro")]:

        if flujo == "Ampliación centros logísticos":

            for centro in cfg.get("CL_centros", []):
                werks = centro["WERKS"]
                if werks not in centros_sel:
                    continue

                section_open(f"Centro {werks}", "📍")

                if "ekgrp_opciones" in centro:
                    campo_editable(
                        "Grupo de compra", f"EKGRP_{werks}",
                        tipo="select", tecnico="EKGRP",
                        opciones=centro["ekgrp_opciones"],
                    )
                if "taxim_opciones" in centro:
                    campo_editable(
                        "Indicador de impuestos", f"TAXIM_{werks}",
                        tipo="select", tecnico="TAXIM",
                        opciones=centro["taxim_opciones"],
                    )

                fijos_c = {
                    k: v for k, v in centro.items()
                    if k not in ("WERKS", "ekgrp_opciones", "taxim_opciones",
                                 "KOKRS", "PRCTR")
                    and v
                }
                if fijos_c:
                    bloque_fijos(f"Centro {werks}", fijos_c)

                section_close()
                st.markdown("")

            # Sucursales ZNOA — fuera del loop, se renderiza una sola vez
            if cfg.get("ZNOA_incluye_sucursales_en_CL"):
                section_open("Sucursales (~70 centros)", "🏪")
                st.caption(
                    f"Se agregarán {len(CENTRO_BENEFICIO_MAP)} sucursales al mismo archivo. "
                    "EKGRP = 007 y KAUTB = X son fijos."
                )
                campo_editable(
                    "Indicador de impuestos — Sucursales", "TAXIM_SUC_znoa",
                    tipo="select",
                    opciones=[str(i) for i in range(1, 7)],
                    tecnico="TAXIM",
                    ayuda="Se aplica a todas las sucursales.",
                )
                section_close()

        elif flujo == "Ampliación sucursales":

            section_open("Mapa de centros de sucursales", "🗺️")

            st.caption(
                f"Se generarán {len(CENTRO_BENEFICIO_MAP)} filas por material. "
                "Sociedad CO y Centro de beneficio provienen del mapa configurado."
            )
            simple_table(
                [
                    {
                        "Centro (WERKS)": k,
                        "Sociedad CO (KOKRS)": v["KOKRS"],
                        "Centro beneficio (PRCTR)": v["PRCTR"],
                    }
                    for k, v in CENTRO_BENEFICIO_MAP.items()
                ],
                height=300,
            )

            if cfg.get("SUC_datos_centro"):
                bloque_fijos("Valores adicionales", {
                    "EKGRP": cfg.get("SUC_ekgrp", ""),
                    "KAUTB": cfg.get("SUC_kautb", ""),
                    "TAXIM": cfg.get("SUC_taxim", ""),
                })

            section_close()

        barra_generacion("centro", flujo, cfg)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: CADENAS DE DISTRIBUCIÓN
# ══════════════════════════════════════════════════════════════════════════════

if "Cadenas de distribución" in nombres_tabs:

    with tabs[nombres_tabs.index("Cadenas de distribución")]:

        section_open("Cadenas de distribución", "🔗")

        opciones_k = cfg.get("CL_ktgrm_opciones", ["01"])
        campo_editable(
            "Grupo de imputación", "KTGRM",
            tipo="select", tecnico="KTGRM",
            opciones=opciones_k,
            ayuda="Se aplica a todas las filas de cadenas de este material.",
        )

        st.markdown("")
        section_message("info", "La estructura de cadenas es fija por tipo de material.")

        filas_c = [
            {
                "VKORG": c["VKORG"],
                "VTWEG": canal,
                "DWERK": c["DWERK"],
                "MTPOS": c["MTPOS"],
                "KTGRM": opciones_k[0],
                "PRODH": "(jerarquía del material)",
            }
            for c in cfg.get("CL_cadenas", [])
            if not centros_sel or c["DWERK"] in centros_sel
            for canal in c["canales"]
        ]
        if filas_c:
            simple_table(filas_c)

        section_close()
        barra_generacion("cadenas", flujo, cfg)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: CLASIFICACIÓN FISCAL
# ══════════════════════════════════════════════════════════════════════════════

if "Clasificación fiscal" in nombres_tabs:

    with tabs[nombres_tabs.index("Clasificación fiscal")]:

        section_open("Clasificación fiscal", "🧾")

        fiscal = cfg.get("CL_fiscal", {})
        section_message(
            "info",
            "Clasificación fiscal generada automáticamente por tipo de material.",
        )
        bloque_fijos("Valores fiscales", {
            "País/Región (ALAND)":       "AR",
            "Clase impuesto 1 (TATYP1)": "J1AU",
            "Clasif. fiscal 1 (TAXM1)":  fiscal.get("TAXM1", ""),
            "Clase impuesto 2 (TATYP2)": "J901",
            "Clasif. fiscal 2 (TAXM2)":  fiscal.get("TAXM2", ""),
        })
        simple_table({
            "MATNR":  mats.get("MATNR", [""]*n),
            "ALAND":  ["AR"] * n,
            "TATYP1": ["J1AU"] * n,
            "TAXM1":  [fiscal.get("TAXM1", "")] * n,
            "TATYP2": ["J901"] * n,
            "TAXM2":  [fiscal.get("TAXM2", "")] * n,
        })

        section_close()
        barra_generacion("fiscal", flujo, cfg)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: DATOS DE PREVISIÓN
# ══════════════════════════════════════════════════════════════════════════════

if "Datos de previsión" in nombres_tabs:

    with tabs[nombres_tabs.index("Datos de previsión")]:

        section_open("Datos de previsión", "📈")

        section_message("info", "Centro A130 — Modelo de pronóstico: J. Valores fijos.")
        simple_table({
            "MATNR": mats.get("MATNR", [""]*n),
            "WERKS": ["A130"] * n,
            "PRMOD": ["J"] * n,
        })

        section_close()
        barra_generacion("prevision", flujo, cfg)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: LUGARES DE ALMACENAMIENTO
# ══════════════════════════════════════════════════════════════════════════════

if "Lugares de almacenamiento" in nombres_tabs:

    with tabs[nombres_tabs.index("Lugares de almacenamiento")]:

        section_open("Lugares de almacenamiento", "🏗️")

        section_message(
            "info",
            "Ubicaciones asignadas automáticamente por tipo de material y centro.",
        )
        lugares = cfg.get("CL_lugares", {})
        filas_l = [
            {"MATNR": m, "WERKS": w, "LGORT": lg}
            for m in mats.get("MATNR", [])
            for w, locs in lugares.items()
            if not centros_sel or w in centros_sel
            for lg in locs
        ]
        if filas_l:
            simple_table(filas_l, height=300)

        section_close()
        barra_generacion("lugares", flujo, cfg)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: ÁREA PLANIF. MRP
# ══════════════════════════════════════════════════════════════════════════════

if "Área planif. MRP" in nombres_tabs:

    with tabs[nombres_tabs.index("Área planif. MRP")]:

        section_open("Área de planificación MRP", "📊")

        section_message("info", "Centro A130 — Área A130_0040. Valores fijos del sistema.")
        bloque_fijos("Área planif. MRP", {
            "WERKS": "A130", "BERID": "A130_0040",
            "DISMM": "V1",   "DISPO": "Z01",
            "DISGR": "0000", "MINBE": "10",
            "DISLS": "EX",   "BSTMI": "1",
            "PLIFZ": "4",    "MODAV": "2",
            "KZINI": "X",    "PRMOD": "J",
            "SIGGR": "4",    "PERAN": "60",
            "ANZPR": "12",   "AUTRU": "X",
        })
        simple_table({
            "MATNR": mats.get("MATNR", [""]*n),
            "WERKS": ["A130"] * n,
            "BERID": ["A130_0040"] * n,
            "DISMM": ["V1"] * n,
            "DISPO": ["Z01"] * n,
        })

        section_close()
        barra_generacion("planif", flujo, cfg)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: DATOS DE VALORACIÓN
# ══════════════════════════════════════════════════════════════════════════════

if "Datos de valoración" in nombres_tabs:

    with tabs[nombres_tabs.index("Datos de valoración")]:

        section_open("Datos de valoración", "💰")

        section_message("info", "Valores de valoración fijos por tipo de material.")

        if flujo == "Ampliación centros logísticos":
            val_cfg = cfg.get("CL_valoracion", [])
            filas_v = [
                {
                    "MATNR": m,
                    "BWKEY": v["BWKEY"],
                    "BKLAS": v["BKLAS"],
                    "VPRSV": v["VPRSV"],
                    "VERPR": v.get("VERPR", ""),
                    "STPRS": v.get("STPRS", ""),
                }
                for m in mats.get("MATNR", [])
                for v in val_cfg
                if not centros_sel or v["BWKEY"] in centros_sel
            ]
            if filas_v:
                simple_table(filas_v, height=250)

        elif flujo == "Ampliación sucursales":
            st.caption(
                f"Se generarán {len(CENTRO_BENEFICIO_MAP)} filas por material "
                "(una por cada sucursal)."
            )
            bloque_fijos("Valoración sucursales", {
                "BKLAS": cfg.get("SUC_bklas", ""),
                "VPRSV": cfg.get("SUC_vprsv", ""),
                "VERPR": cfg.get("SUC_verpr", ""),
                "PEINH": cfg.get("SUC_peinh", "1"),
            })

        section_close()
        barra_generacion("valoracion", flujo, cfg)
