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

def pegar_en_bloque(label: str, campo: str, n: int):
    """Modal de pegado en bloque estilo Excel."""
    key_open  = f"bloque_open_{campo}"
    key_texto = f"bloque_texto_{campo}"
    key_apply = f"bloque_applied_{campo}"

    if key_open not in st.session_state:
        st.session_state[key_open] = False

    if st.button("📋 Pegar en bloque", key=f"btn_bloque_{campo}"):
        st.session_state[key_open] = not st.session_state[key_open]
        st.rerun()

    if st.session_state[key_open]:
        st.markdown("""
        <style>
        .modal-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.45);
            z-index: 9998;
        }
        .modal-box {
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 520px;
            background: #fff;
            border-radius: 6px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.22);
            z-index: 9999;
            overflow: hidden;
        }
        .modal-header {
            background: #0a6ed1;
            color: white;
            padding: 0.7rem 1.2rem;
            font-size: 13px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .modal-body {
            padding: 1rem 1.2rem 0.5rem;
            font-size: 12px;
            color: #6a6d70;
        }
        .modal-footer {
            padding: 0.6rem 1.2rem 1rem;
            display: flex;
            gap: 0.5rem;
        }
        </style>
        <div class="modal-overlay"></div>
        <div class="modal-box">
          <div class="modal-header">📋 Pegado en bloque</div>
          <div class="modal-body">
            Pegá un valor por línea, en el mismo orden que los materiales.<br>
            Las líneas vacías se ignoran.
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Contenedor del textarea y botones encima del overlay
        with st.container():
            st.markdown("""
            <style>
            /* Empujar el widget de Streamlit dentro del modal visual */
            div[data-testid="stVerticalBlock"]:has(
                > div > div[data-testid="stTextArea"]
            ) {
                position: fixed;
                top: calc(50% - 80px);
                left: 50%;
                transform: translate(-50%, 0);
                width: 490px;
                z-index: 10000;
                background: transparent;
            }
            </style>
            """, unsafe_allow_html=True)

            texto = st.text_area(
                label=f"bloque_{campo}",
                label_visibility="collapsed",
                placeholder="\n".join([f"Valor {i+1}" for i in range(min(n, 4))] + ["..."]),
                height=220,
                key=key_texto,
            )

            c1, c2, _ = st.columns([2, 2, 4])
            if c1.button("✅ Aplicar", key=f"apply_bloque_{campo}", type="primary"):
                lineas = [l.strip() for l in texto.splitlines() if l.strip()]
                for i, linea in enumerate(lineas):
                    if i < n:
                        set_val(campo, i, linea)
                st.session_state[key_open] = False
                st.rerun()

            if c2.button("✖ Cancelar", key=f"cancel_bloque_{campo}"):
                st.session_state[key_open] = False
                st.rerun()

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

    col_lbl, col_paste = st.columns([6, 2])
    col_lbl.markdown(f'<div class="sap-table-label">{full_label}</div>', unsafe_allow_html=True)

    if tipo == "texto":
        with col_paste:
            pegar_en_bloque(label, campo, n)

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
            v = edited.iloc[i][label]
            set_val(campo, i, str(v).strip() if v is not None else "")

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
        v = "" if v is None else str(v)
        set_val(campo, i, v.replace("\r\n", " ").replace("\r", " ").replace("\n", " ").strip())

    if n > 1:
        c1, _ = st.columns([2, 6])
        if c1.button("↕ Aplicar a todos", key=f"fill_{campo}", use_container_width=True):
            v = edited.iloc[0][label]
            fill_all(campo, "" if v is None else str(v))
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Tabla simple (solo lectura)
# ─────────────────────────────────────────────────────────────────────────────

def simple_table(data: list[dict] | dict, height: int = None):
    """Muestra un DataFrame de solo lectura a partir de una lista de dicts o dict de listas."""
    df = pd.DataFrame(data)
    kwargs = {"use_container_width": True, "hide_index": True}
    if height is not None:
        kwargs["height"] = height
    st.dataframe(df, **kwargs)


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
