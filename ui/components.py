import streamlit as st
import pandas as pd

from core.state import get_mats, get_n, get_val, set_val, fill_all
from core.validators import validar
from core.generators import generar_zip
from ui.layout import table_label


# ─────────────────────────────────────────────────────────────────────────────
# Status bar
# ─────────────────────────────────────────────────────────────────────────────

def status_bar(tipo: str, mensaje: str):
    """
    Barra de estado SAP con semáforo.
    tipo: "ok" | "warn" | "error"
    """
    clases = {"ok": "sap-status-ok", "warn": "sap-status-warn", "error": "sap-status-error"}
    iconos = {"ok": "🟢", "warn": "🟡", "error": "🔴"}

    st.markdown(f"""
    <div class="sap-status-bar">
      <span class="sap-status-icon">{iconos[tipo]}</span>
      <span class="{clases[tipo]}">{mensaje}</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Bloque de valores fijos (solo lectura)
# ─────────────────────────────────────────────────────────────────────────────

def bloque_fijos(titulo: str, datos: dict):
    """
    Expander colapsable con los valores fijos del sistema para una vista.
    Los valores se muestran como tags azules estilo SAP.
    """
    items_html = ""
    for k, v in datos.items():
        if v is None:
            continue
        items_html += f"""
        <div class="sap-field-row">
          <span class="sap-field-label">{k}</span>
          <span class="sap-field-value">
            <span class="sap-tag">{v if v else "(vacío)"}</span>
          </span>
        </div>
        """

    with st.expander(f"Valores fijos del sistema — {titulo}", expanded=False):
        st.markdown(items_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Tabla editable por campo
# ─────────────────────────────────────────────────────────────────────────────

def campo_editable(
    label: str,
    campo: str,
    tipo: str = "texto",
    opciones: list | None = None,
    ayuda: str | None = None,
    tecnico: str = "",
):
    """
    Renderiza una tabla editable (una fila por material) para un campo dado.
    Incluye botón "Aplicar a todos" cuando hay más de un material.

    Parámetros:
        label:    Nombre visible del campo
        campo:    Clave interna del estado (ej: "MAKTX", "EKGRP_A130")
        tipo:     "texto" | "numero" | "select" | "checkbox"
        opciones: Lista de opciones (solo para tipo "select")
        ayuda:    Texto de ayuda que aparece debajo del label
        tecnico:  Nombre técnico SAP para mostrar entre paréntesis
    """
    n    = get_n()
    mats = get_mats()

    full_label = f"{label}" + (f" ({tecnico})" if tecnico else "")
    table_label(full_label)

    if ayuda:
        st.caption(ayuda)

    # ── Checkbox (MSTAE) ──────────────────────────────────────────────────
    if tipo == "checkbox":
        df = pd.DataFrame({
            "MATNR": mats.get("MATNR", [""]*n),
            "Activo (sin bloqueo)": [bool(get_val(campo, i, True)) for i in range(n)],
        })
        edited = st.data_editor(
            df, key=f"de_{campo}", use_container_width=True, hide_index=True,
            disabled=["MATNR"],
            column_config={
                "MATNR": st.column_config.TextColumn("MATNR", width=200),
                "Activo (sin bloqueo)": st.column_config.CheckboxColumn(
                    "Activo (sin bloqueo)", width=180,
                    help="✅ Marcado = material activo (/). Desmarcado = bloqueado.",
                ),
            },
        )
        for i in range(n):
            set_val(campo, i, bool(edited.iloc[i]["Activo (sin bloqueo)"]))

        if n > 1:
            c1, _ = st.columns([2, 6])
            if c1.button("↕ Aplicar a todos", key=f"fill_{campo}", use_container_width=True):
                fill_all(campo, bool(edited.iloc[0]["Activo (sin bloqueo)"]))
                st.rerun()
        return

    # ── Select (desplegable) ──────────────────────────────────────────────
    if tipo == "select" and opciones:
        df = pd.DataFrame({
            "MATNR": mats.get("MATNR", [""]*n),
            label:   [get_val(campo, i, opciones[0]) for i in range(n)],
        })
        edited = st.data_editor(
            df, key=f"de_{campo}", use_container_width=True, hide_index=True,
            disabled=["MATNR"],
            column_config={
                "MATNR": st.column_config.TextColumn("MATNR", width=200),
                label:   st.column_config.SelectboxColumn(label, options=opciones, width=200),
            },
        )
        for i in range(n):
            set_val(campo, i, edited.iloc[i][label])

        if n > 1:
            c1, _ = st.columns([2, 6])
            if c1.button("↕ Aplicar a todos", key=f"fill_{campo}", use_container_width=True):
                fill_all(campo, edited.iloc[0][label])
                st.rerun()
        return

    # ── Texto / Número ────────────────────────────────────────────────────
    df = pd.DataFrame({
        "MATNR": mats.get("MATNR", [""]*n),
        label:   [get_val(campo, i, "") for i in range(n)],
    })
    col_cfg = {
        "MATNR": st.column_config.TextColumn("MATNR", width=200),
        label: (
            st.column_config.NumberColumn(label, width=250)
            if tipo == "numero"
            else st.column_config.TextColumn(label, width=350)
        ),
    }
    edited = st.data_editor(
        df, key=f"de_{campo}", use_container_width=True,
        hide_index=True, disabled=["MATNR"], column_config=col_cfg,
    )
    for i in range(n):
        v = edited.iloc[i][label]
        set_val(campo, i, "" if v is None else str(v))

    if n > 1:
        c1, _ = st.columns([2, 6])
        if c1.button("↕ Aplicar a todos", key=f"fill_{campo}", use_container_width=True):
            v = edited.iloc[0][label]
            fill_all(campo, "" if v is None else str(v))
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Tabla simple (solo lectura)
# ─────────────────────────────────────────────────────────────────────────────

def simple_table(data: list[dict] | dict, height: int | None = None):
    """Muestra un DataFrame de solo lectura a partir de una lista de dicts o dict de listas."""
    df = pd.DataFrame(data).reset_index(drop=True)
    # Avoid passing a kwargs dict to st.dataframe to satisfy strict type checkers
    if height is not None:
        st.dataframe(df, use_container_width=True, height=height)
    else:
        st.dataframe(df, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# Mensaje de sección
# ─────────────────────────────────────────────────────────────────────────────

def section_message(tipo: str, texto: str):
    """Wrapper de mensajes de Streamlit con tipo unificado."""
    {"info": st.info, "success": st.success,
     "warning": st.warning, "error": st.error}.get(tipo, st.info)(texto)


# ─────────────────────────────────────────────────────────────────────────────
# Barra de generación (status + botón + descarga)
# ─────────────────────────────────────────────────────────────────────────────

def barra_generacion(key: str, flujo: str, cfg: dict):
    """
    Barra completa de generación reutilizable en cada tab.
    Muestra el estado de validación, el botón generar y, al generar,
    la descarga del ZIP y preview de archivos.

    Parámetros:
        key:   Sufijo único para evitar duplicados de key en Streamlit
        flujo: Flujo activo ("Ampliación centros logísticos", etc.)
        cfg:   Configuración del tipo de material
    """
    n = get_n()
    errores, avisos = validar(n, flujo, cfg)

    # Status
    if errores:
        tipo_status, msg_status = "error", f"{len(errores)} error(es) — corregí antes de generar."
    elif avisos:
        tipo_status, msg_status = "warn", f"{len(avisos)} campo(s) opcionales vacíos — podés generar igual."
    else:
        tipo_status, msg_status = "ok", f"{n} material(es) listos para generar."

    status_bar(tipo_status, msg_status)

    c_btn, c_rest = st.columns([2, 8])

    if c_btn.button("⚙️  Generar .txt", type="primary", key=f"gen_{key}", use_container_width=True):
        if errores:
            for e in errores:
                st.error(e)
        else:
            with st.spinner("Generando archivos..."):
                zip_bytes, archivos = generar_zip(flujo, cfg)

            ts         = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
            tipo_mat   = st.session_state.tipo_mat
            nombre_zip = f"SAP_{tipo_mat}_{ts}.zip"

            st.success(f"✅ {len(archivos)} archivo(s) generado(s) para {n} material(es).")

            with st.expander("Vista previa de archivos generados"):
                for nombre, contenido in archivos.items():
                    st.markdown(f"**{nombre}**")
                    lineas = contenido.decode("utf-8").split("\r\n")
                    st.code("\n".join(lineas[:min(5, len(lineas))]), language=None)

            c_rest.download_button(
                label=f"⬇️  Descargar ZIP — {len(archivos)} archivo(s)",
                data=zip_bytes,
                file_name=nombre_zip,
                mime="application/zip",
                key=f"dl_{key}",
                use_container_width=True,
            )
