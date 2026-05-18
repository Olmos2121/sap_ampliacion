import streamlit as st
import pandas as pd
import zipfile
from io import BytesIO

from config import TIPOS_MATERIAL, CENTRO_BENEFICIO_MAP
from txt_generator import (
    gen_datos_basicos, gen_datos_centro_CL, gen_datos_centro_SUC,
    gen_cadenas, gen_clasificacion_fiscal, gen_datos_prevision,
    gen_lugares_almacenamiento, gen_area_planificacion,
    gen_datos_valoracion, gen_datos_valoracion_SUC,
)

# ─────────────────────────────────────────────────────────────────────────────
# Página y estilos
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SAP Materiales",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background: #0f1117; }

.app-header { padding: 2rem 0 1.5rem 0; border-bottom: 1px solid #2a2d3a; margin-bottom: 2rem; }
.app-header h1 { font-family: 'IBM Plex Mono', monospace; font-size: 1.4rem; font-weight: 500; color: #e2e8f0; letter-spacing: -0.02em; margin: 0; }
.app-header .subtitle { font-size: 0.78rem; color: #64748b; margin-top: 0.3rem; font-family: 'IBM Plex Mono', monospace; }

.section-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; color: #475569; margin-bottom: 0.5rem; margin-top: 1.2rem; }

.field-card { background: #1e2130; border: 1px solid #2a2d3a; border-radius: 6px; padding: 0.7rem 1rem; margin-bottom: 0.4rem; }
.field-label { font-size: 0.7rem; color: #64748b; font-family: 'IBM Plex Mono', monospace; margin-bottom: 0.25rem; }
.field-tag { background: #1a2744; color: #60a5fa; border-radius: 4px; padding: 0.1rem 0.45rem; font-size: 0.78rem; font-family: 'IBM Plex Mono', monospace; margin-right: 0.3rem; display: inline-block; }

.ctx-bar { background: #161822; border: 1px solid #2a2d3a; border-radius: 8px; padding: 0.6rem 1.2rem; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 1rem; }
.ctx-flujo { font-weight: 600; color: #e2e8f0; font-size: 0.85rem; }
.ctx-tipo { font-family: 'IBM Plex Mono', monospace; background: #1a2744; color: #93c5fd; border-radius: 4px; padding: 0.15rem 0.6rem; font-size: 0.78rem; }
.ctx-n { color: #64748b; font-size: 0.78rem; }

.stTabs [data-baseweb="tab-list"] { background: #161822; border-radius: 8px 8px 0 0; border-bottom: 1px solid #2a2d3a; padding: 0 0.5rem; gap: 0; }
.stTabs [data-baseweb="tab"] { font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: #64748b; border-bottom: 2px solid transparent !important; padding: 0.65rem 1rem; background: transparent !important; }
.stTabs [aria-selected="true"] { color: #93c5fd !important; border-bottom-color: #3b82f6 !important; }
.stTabs [data-baseweb="tab-panel"] { background: #161822; border-radius: 0 0 8px 8px; border: 1px solid #2a2d3a; border-top: none; padding: 1.5rem; }

.stTextInput>div>div>input, .stTextArea>div>div>textarea { background: #1e2130 !important; border: 1px solid #2a2d3a !important; color: #e2e8f0 !important; border-radius: 6px !important; font-family: 'IBM Plex Sans', sans-serif; }
.stSelectbox>div>div { background: #1e2130 !important; border: 1px solid #2a2d3a !important; color: #e2e8f0 !important; border-radius: 6px !important; }

.stButton>button { border-radius: 6px !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.78rem !important; transition: all 0.15s; }
.stButton>button[kind="primary"] { background: #1d4ed8 !important; border: none !important; color: white !important; }
.stButton>button[kind="primary"]:hover { background: #2563eb !important; }
.stButton>button[kind="secondary"] { background: #161822 !important; border: 1px solid #2a2d3a !important; color: #94a3b8 !important; }
.stButton>button[kind="secondary"]:hover { border-color: #3b82f6 !important; color: #e2e8f0 !important; }

.gen-bar { background: #111827; border: 1px solid #1e3a5f; border-radius: 8px; padding: 1rem 1.2rem; margin-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Estado global
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "flujo": None, "tipo_mat": None,
        "materiales": {}, "n_mats": 0,
        "configurado": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def get_n():    return st.session_state.n_mats
def get_mats(): return st.session_state.materiales

def get_val(campo, idx, default=""):
    d = get_mats().get(campo, [])
    return d[idx] if idx < len(d) else default

def set_val(campo, idx, value):
    m = get_mats()
    if campo not in m: m[campo] = [""] * get_n()
    while len(m[campo]) < get_n(): m[campo].append("")
    m[campo][idx] = value

def fill_all(campo, value):
    get_mats()[campo] = [value] * get_n()

def resolver_mstae(idx):
    val = get_val("MSTAE", idx, True)
    return "/" if (val is True or val == True) else ""


# ─────────────────────────────────────────────────────────────────────────────
# Encabezado
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <h1>📦 SAP — Ampliación masiva de materiales</h1>
  <div class="subtitle">Generador de archivos .txt para carga masiva en SAP</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PASO 1 — Configuración
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.configurado:

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="section-label">¿Qué querés hacer?</div>', unsafe_allow_html=True)

        FLUJOS = {
            "Ampliación centros logísticos": "Amplía materiales a centros A110 / A120 / A130. Genera hasta 8 archivos .txt.",
            "Ampliación sucursales":         "Amplía materiales a los ~70 centros de sucursales. Genera 2–3 archivos .txt.",
            "Modificación datos básicos":    "Modifica campos de materiales ya existentes. Genera 1 archivo .txt.",
        }
        for nombre, desc in FLUJOS.items():
            activo = st.session_state.flujo == nombre
            if st.button(nombre, key=f"op_{nombre}", use_container_width=True,
                         type="primary" if activo else "secondary"):
                if st.session_state.flujo != nombre:
                    st.session_state.flujo = nombre
                    st.session_state.tipo_mat = None
                    st.session_state.materiales = {}
                    st.session_state.n_mats = 0
                st.rerun()
            st.caption(desc)

    with col_right:
        if st.session_state.flujo:
            st.markdown('<div class="section-label">Tipo de material</div>', unsafe_allow_html=True)

            TIPOS_POR_FLUJO = {
                "Ampliación centros logísticos": list(TIPOS_MATERIAL.keys()),
                "Ampliación sucursales":         ["ZMED", "ZNOM", "ZINS"],
                "Modificación datos básicos":    list(TIPOS_MATERIAL.keys()),
            }
            tipos_disp = TIPOS_POR_FLUJO[st.session_state.flujo]
            cols_t = st.columns(min(len(tipos_disp), 4))
            for i, t in enumerate(tipos_disp):
                activo = st.session_state.tipo_mat == t
                if cols_t[i % 4].button(t.replace("_"," "), key=f"chip_{t}",
                                        type="primary" if activo else "secondary",
                                        use_container_width=True):
                    if st.session_state.tipo_mat != t:
                        st.session_state.tipo_mat = t
                        st.session_state.materiales = {}
                        st.session_state.n_mats = 0
                    st.rerun()

            if st.session_state.tipo_mat:
                st.markdown('<div class="section-label" style="margin-top:1.5rem">Números de material (MATNR)</div>', unsafe_allow_html=True)
                st.caption("Copiá y pegá desde Excel (una columna, un número por línea), o escribilos manualmente.")

                texto_matnr = st.text_area(
                    label="matnr", label_visibility="collapsed",
                    placeholder="3010002429\n4000013248\n4000035781\n...",
                    height=180, key="input_matnr",
                )

                if st.button("Confirmar y continuar →", type="primary", use_container_width=True):
                    lineas = [l.strip() for l in texto_matnr.replace("\t","\n").splitlines() if l.strip()]
                    if not lineas:
                        st.error("Ingresá al menos un número de material.")
                    else:
                        n = len(lineas)
                        st.session_state.n_mats = n
                        cfg_tmp = TIPOS_MATERIAL[st.session_state.tipo_mat]
                        campos_init = ["MATNR","MAKTX","MATKL","PRDHA","VOLUM",
                                       "TEXTO_LARGO","SPART","KTGRM"]
                        for campo in campos_init:
                            st.session_state.materiales[campo] = [""] * n
                        st.session_state.materiales["MATNR"]  = lineas
                        st.session_state.materiales["MSTAE"]  = [True] * n
                        for c in cfg_tmp.get("CL_centros", []):
                            werks = c["WERKS"]
                            st.session_state.materiales[f"EKGRP_{werks}"] = [""] * n
                            st.session_state.materiales[f"TAXIM_{werks}"] = [""] * n
                        st.session_state.configurado = True
                        st.rerun()
        else:
            st.markdown("")
            st.info("Seleccioná una operación para continuar.")

    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# PASO 2 — Vistas
# ─────────────────────────────────────────────────────────────────────────────
flujo    = st.session_state.flujo
tipo_mat = st.session_state.tipo_mat
cfg      = TIPOS_MATERIAL[tipo_mat]
n        = get_n()
mats     = get_mats()

# Barra de contexto
c1, c2, c3 = st.columns([5, 3, 2])
c1.markdown(
    f'<div style="display:flex;align-items:center;gap:0.8rem;padding:0.4rem 0">'
    f'<span style="font-weight:600;color:#e2e8f0;font-size:0.9rem">{flujo}</span>'
    f'<span class="ctx-tipo">{tipo_mat.replace("_"," ")}</span>'
    f'<span style="color:#64748b;font-size:0.78rem">{n} material{"es" if n!=1 else ""}</span>'
    f'</div>',
    unsafe_allow_html=True
)
if c3.button("← Volver", use_container_width=True):
    st.session_state.configurado = False
    st.session_state.materiales  = {}
    st.session_state.n_mats      = 0
    st.rerun()

st.markdown("")


# ─────────────────────────────────────────────────────────────────────────────
# Helpers de UI
# ─────────────────────────────────────────────────────────────────────────────
def campo_editable(label, campo, tipo="texto", opciones=None, ayuda=None):
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)
    if ayuda:
        st.caption(ayuda)

    if tipo == "checkbox":
        df = pd.DataFrame({
            "MATNR": mats.get("MATNR",[""]*n),
            "Activo (no bloqueado)": [bool(get_val(campo,i,True)) for i in range(n)],
        })
        edited = st.data_editor(df, key=f"de_{campo}", use_container_width=True,
                                hide_index=True, disabled=["MATNR"],
                                column_config={
                                    "MATNR": st.column_config.TextColumn("MATNR", width=160),
                                    "Activo (no bloqueado)": st.column_config.CheckboxColumn(width=180),
                                })
        for i in range(n): set_val(campo, i, bool(edited.iloc[i]["Activo (no bloqueado)"]))
        if n > 1 and st.button("↕ Aplicar primero a todos", key=f"fill_{campo}"):
            fill_all(campo, bool(edited.iloc[0]["Activo (no bloqueado)"])); st.rerun()
        return

    if tipo == "select" and opciones:
        df = pd.DataFrame({
            "MATNR": mats.get("MATNR",[""]*n),
            label: [get_val(campo,i,opciones[0]) for i in range(n)],
        })
        edited = st.data_editor(df, key=f"de_{campo}", use_container_width=True,
                                hide_index=True, disabled=["MATNR"],
                                column_config={
                                    "MATNR": st.column_config.TextColumn("MATNR", width=160),
                                    label: st.column_config.SelectboxColumn(options=opciones, width=220),
                                })
        for i in range(n): set_val(campo, i, edited.iloc[i][label])
        if n > 1 and st.button("↕ Aplicar primero a todos", key=f"fill_{campo}"):
            fill_all(campo, edited.iloc[0][label]); st.rerun()
        return

    # texto / numero
    df = pd.DataFrame({
        "MATNR": mats.get("MATNR",[""]*n),
        label: [get_val(campo,i,"") for i in range(n)],
    })
    col_cfg = {
        "MATNR": st.column_config.TextColumn("MATNR", width=160),
        label: st.column_config.NumberColumn(width=250) if tipo=="numero"
               else st.column_config.TextColumn(width=350),
    }
    edited = st.data_editor(df, key=f"de_{campo}", use_container_width=True,
                            hide_index=True, disabled=["MATNR"], column_config=col_cfg)
    for i in range(n):
        v = edited.iloc[i][label]
        set_val(campo, i, "" if v is None else str(v))
    if n > 1 and st.button("↕ Aplicar primero a todos", key=f"fill_{campo}"):
        v = edited.iloc[0][label]
        fill_all(campo, "" if v is None else str(v)); st.rerun()


def seccion_fijos(titulo, fijos):
    with st.expander(f"🔒 Valores fijos — {titulo}", expanded=False):
        cols = st.columns(4)
        for i,(k,v) in enumerate(fijos.items()):
            cols[i%4].markdown(
                f'<div class="field-card"><div class="field-label">{k}</div>'
                f'<span class="field-tag">{v if v else "(vacío)"}</span></div>',
                unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Validación y generación
# ─────────────────────────────────────────────────────────────────────────────
def validar():
    errores, avisos = [], []
    if n == 0: return ["No hay materiales cargados."], []
    for i in range(n):
        matnr = str(get_val("MATNR",i,"")).strip()
        if not matnr: errores.append(f"Fila {i+1}: MATNR vacío.")
    if flujo != "Ampliación sucursales":
        for i in range(n):
            if not str(get_val("MAKTX",i,"")).strip():
                errores.append(f"Fila {i+1}: Descripción (MAKTX) vacía.")
    if flujo == "Ampliación centros logísticos":
        for i in range(n):
            if not str(get_val("MATKL",i,"")).strip():
                avisos.append(f"Fila {i+1}: Grupo de productos (MATKL) vacío.")
            if not str(get_val("PRDHA",i,"")).strip():
                avisos.append(f"Fila {i+1}: Jerarquía (PRDHA) vacía.")
            if cfg.get("VOLEH") and not str(get_val("VOLUM",i,"")).strip():
                avisos.append(f"Fila {i+1}: Volumen (VOLUM) vacío.")
    return errores, avisos


def construir_lista():
    lista = []
    for i in range(n):
        m = {campo: (vals[i] if i < len(vals) else "") for campo, vals in mats.items()}
        m["MSTAE"] = resolver_mstae(i)
        if not m.get("SPART"): m["SPART"] = cfg.get("SPART","")
        if not m.get("TEXTO_LARGO"): m["TEXTO_LARGO"] = m.get("MAKTX","")
        lista.append(m)
    return lista


def generar_zip():
    lista = construir_lista()
    archivos = {}
    if flujo == "Ampliación centros logísticos":
        archivos["Datos_basicos.txt"]   = gen_datos_basicos(lista, cfg, "vistas_CL")
        archivos["Datos_de_centro.txt"] = gen_datos_centro_CL(lista, cfg)
        for nombre, fn, arg in [
            ("Cadenas_de_distribucion.txt",  gen_cadenas,              lista),
            ("Clasificacion_fiscal.txt",      gen_clasificacion_fiscal, lista),
            ("Datos_de_prevision.txt",        gen_datos_prevision,      lista),
            ("Lugares_de_almacenamiento.txt", gen_lugares_almacenamiento, lista),
            ("Area_planific_nec.txt",         gen_area_planificacion,   lista),
        ]:
            r = fn(arg, cfg)
            if r: archivos[nombre] = r
        r = gen_datos_valoracion(lista, cfg, "CL_valoracion")
        if r: archivos["Datos_valoracion.txt"] = r
    elif flujo == "Ampliación sucursales":
        archivos["Datos_basicos.txt"]   = gen_datos_basicos(lista, cfg, "vistas_SUC")
        archivos["Datos_de_centro.txt"] = gen_datos_centro_SUC(lista, cfg)
        r = gen_datos_valoracion_SUC(lista, cfg)
        if r: archivos["Datos_valoracion.txt"] = r
    else:
        archivos["Datos_basicos.txt"] = gen_datos_basicos(lista, cfg, "vistas_MOD")

    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for nombre, contenido in archivos.items():
            zf.writestr(nombre, contenido)
    buf.seek(0)
    return buf.getvalue(), archivos


def boton_generar(key):
    st.markdown('<div class="gen-bar">', unsafe_allow_html=True)
    errores, avisos = validar()

    c_btn, c_status = st.columns([2, 5])
    generar = c_btn.button("⚙️ Generar .txt", type="primary", key=f"gen_{key}")

    if errores:
        c_status.error("  ".join(f"• {e}" for e in errores[:3])
                       + (f"  … y {len(errores)-3} más" if len(errores)>3 else ""))
    elif avisos:
        c_status.warning(f"{len(avisos)} campo(s) vacío(s) — se puede generar igual.")
    else:
        c_status.success(f"✅ {n} material(es) listos para generar.")

    if generar:
        if errores:
            st.error("Corregí los errores antes de generar.")
        else:
            with st.spinner("Generando archivos..."):
                zip_bytes, archivos = generar_zip()
            ts   = pd.Timestamp.now().strftime("%Y%m%d_%H%M")
            nombre_zip = f"SAP_{tipo_mat}_{ts}.zip"
            st.success(f"✅ {len(archivos)} archivo(s) generado(s).")
            with st.expander("👁 Preview de archivos"):
                for nombre, contenido in archivos.items():
                    st.markdown(f"**{nombre}**")
                    lineas = contenido.decode("utf-8").split("\r\n")
                    st.code("\n".join(lineas[:min(5,len(lineas))]), language=None)
            st.download_button(
                f"⬇️ Descargar ZIP ({len(archivos)} archivos)",
                data=zip_bytes, file_name=nombre_zip,
                mime="application/zip", key=f"dl_{key}",
            )
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────────────────────────────────────
def tabs_para_flujo():
    if flujo == "Ampliación centros logísticos":
        t = ["Datos básicos", "Datos de centro"]
        if cfg.get("CL_cadenas"):       t.append("Cadenas de distribución")
        if cfg.get("CL_fiscal"):        t.append("Clasificación fiscal")
        if cfg.get("CL_prevision"):     t.append("Datos de previsión")
        if cfg.get("CL_lugares"):       t.append("Lugares de almacenamiento")
        if cfg.get("CL_area_planif"):   t.append("Área planif. MRP")
        if cfg.get("CL_valoracion"):    t.append("Datos de valoración")
        return t
    if flujo == "Ampliación sucursales":
        t = ["Datos básicos", "Datos de centro"]
        if cfg.get("SUC_valoracion"): t.append("Datos de valoración")
        return t
    return ["Datos básicos"]

nombres_tabs = tabs_para_flujo()
tabs = st.tabs(nombres_tabs)


# ══════════════════════════════════════════════════════════════════════════════
# TAB: DATOS BÁSICOS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    if flujo == "Ampliación sucursales":
        st.info("Para sucursales la vista Datos básicos solo activa el flag de almacenamiento. No requiere campos adicionales.")
        st.dataframe(pd.DataFrame({
            "MATNR": mats.get("MATNR",[""]*n),
            "Vista almacenamiento": ["X"]*n,
        }), use_container_width=True, hide_index=True)
    else:
        campo_editable("Descripción (MAKTX)", "MAKTX", ayuda="Nombre del material en SAP.")
        if flujo == "Ampliación centros logísticos":
            campo_editable("Grupo de productos (MATKL)", "MATKL", ayuda="Ej: J0101, J0104.")
            campo_editable("Jerarquía de productos (PRDHA)", "PRDHA", ayuda="Ej: J010109.")
            if cfg.get("VOLEH"):
                campo_editable("Volumen (VOLUM)", "VOLUM", tipo="numero",
                               ayuda=f"Unidad: {cfg.get('VOLEH','CM3')}.")
            if "SPART_opciones" in cfg:
                campo_editable("Partición (SPART)", "SPART", tipo="select",
                               opciones=cfg["SPART_opciones"])
        campo_editable("Texto largo", "TEXTO_LARGO",
                       ayuda="Si se deja vacío, se usa la descripción.")
        campo_editable("Bloqueo de material (MSTAE)", "MSTAE", tipo="checkbox",
                       ayuda="✅ Marcado = material activo (/). Desmarcado = bloqueado.")

        fijos = {k: v for k,v in cfg.items()
                 if k in ("MTART","SPART","XCHPF","MTPOS","VOLEH","EKWSL","TRAGR","IPRKZ","MHDRZ","SERIAL") and v}
        if fijos: seccion_fijos("Datos básicos", fijos)

    boton_generar("basicos")


# ══════════════════════════════════════════════════════════════════════════════
# TAB: DATOS DE CENTRO
# ══════════════════════════════════════════════════════════════════════════════
if "Datos de centro" in nombres_tabs:
    with tabs[nombres_tabs.index("Datos de centro")]:
        if flujo == "Ampliación centros logísticos":
            for centro in cfg.get("CL_centros", []):
                werks = centro["WERKS"]
                st.markdown(f'<div class="section-label">Centro {werks}</div>',
                            unsafe_allow_html=True)
                if "ekgrp_opciones" in centro:
                    campo_editable(f"Grupo de compra — {werks} (EKGRP)",
                                   f"EKGRP_{werks}", tipo="select",
                                   opciones=centro["ekgrp_opciones"])
                if "taxim_opciones" in centro:
                    campo_editable(f"Indicador de impuestos — {werks} (TAXIM)",
                                   f"TAXIM_{werks}", tipo="select",
                                   opciones=centro["taxim_opciones"])
                fijos_c = {k:v for k,v in centro.items()
                           if k not in ("WERKS","ekgrp_opciones","taxim_opciones") and v}
                if fijos_c: seccion_fijos(f"Centro {werks}", fijos_c)
                st.markdown("---")

        elif flujo == "Ampliación sucursales":
            st.info(f"Se generan {len(CENTRO_BENEFICIO_MAP)} filas por material. "
                    f"Sociedad CO y Centro de beneficio se toman del mapa de centros.")
            df_mapa = pd.DataFrame([
                {"WERKS": k, "KOKRS": v["KOKRS"], "PRCTR": v["PRCTR"]}
                for k, v in CENTRO_BENEFICIO_MAP.items()
            ])
            st.dataframe(df_mapa, use_container_width=True, hide_index=True, height=280)
            if cfg.get("SUC_datos_centro"):
                seccion_fijos("Valores fijos adicionales", {
                    "EKGRP": cfg.get("SUC_ekgrp",""),
                    "KAUTB": cfg.get("SUC_kautb",""),
                    "TAXIM": cfg.get("SUC_taxim",""),
                })

        boton_generar("centro")


# ══════════════════════════════════════════════════════════════════════════════
# TAB: CADENAS DE DISTRIBUCIÓN
# ══════════════════════════════════════════════════════════════════════════════
if "Cadenas de distribución" in nombres_tabs:
    with tabs[nombres_tabs.index("Cadenas de distribución")]:
        opciones_k = cfg.get("CL_ktgrm_opciones", ["01"])
        campo_editable("Grupo de imputación (KTGRM)", "KTGRM",
                       tipo="select", opciones=opciones_k,
                       ayuda="Se aplica a todas las filas de cadenas del material.")

        st.markdown('<div class="section-label">Estructura de cadenas (fija por tipo)</div>',
                    unsafe_allow_html=True)
        filas_c = []
        for c in cfg.get("CL_cadenas", []):
            for canal in c["canales"]:
                filas_c.append({"VKORG": c["VKORG"], "VTWEG": canal,
                                 "DWERK": c["DWERK"], "MTPOS": c["MTPOS"],
                                 "KTGRM": opciones_k[0], "PRODH": "(jerarquía)"})
        if filas_c:
            st.dataframe(pd.DataFrame(filas_c), use_container_width=True, hide_index=True)

        boton_generar("cadenas")


# ══════════════════════════════════════════════════════════════════════════════
# TAB: CLASIFICACIÓN FISCAL
# ══════════════════════════════════════════════════════════════════════════════
if "Clasificación fiscal" in nombres_tabs:
    with tabs[nombres_tabs.index("Clasificación fiscal")]:
        fiscal = cfg.get("CL_fiscal", {})
        st.info("Clasificación fiscal fija por tipo de material. No requiere ingreso.")
        seccion_fijos("Clasificación fiscal", {
            "ALAND": "AR", "TATYP1": "J1AU",
            f"TAXM1": fiscal.get("TAXM1",""),
            "TATYP2": "J901", "TAXM2": fiscal.get("TAXM2",""),
        })
        st.dataframe(pd.DataFrame({
            "MATNR": mats.get("MATNR",[""]*n),
            "ALAND": ["AR"]*n,
            "TATYP1": ["J1AU"]*n, "TAXM1": [fiscal.get("TAXM1","")]*n,
            "TATYP2": ["J901"]*n,  "TAXM2": [fiscal.get("TAXM2","")]*n,
        }), use_container_width=True, hide_index=True)
        boton_generar("fiscal")


# ══════════════════════════════════════════════════════════════════════════════
# TAB: DATOS DE PREVISIÓN
# ══════════════════════════════════════════════════════════════════════════════
if "Datos de previsión" in nombres_tabs:
    with tabs[nombres_tabs.index("Datos de previsión")]:
        st.info("Fijo: centro A130, modelo de pronóstico J.")
        st.dataframe(pd.DataFrame({
            "MATNR": mats.get("MATNR",[""]*n),
            "WERKS": ["A130"]*n, "PRMOD": ["J"]*n,
        }), use_container_width=True, hide_index=True)
        boton_generar("prevision")


# ══════════════════════════════════════════════════════════════════════════════
# TAB: LUGARES DE ALMACENAMIENTO
# ══════════════════════════════════════════════════════════════════════════════
if "Lugares de almacenamiento" in nombres_tabs:
    with tabs[nombres_tabs.index("Lugares de almacenamiento")]:
        st.info("Ubicaciones fijas por tipo de material.")
        lugares = cfg.get("CL_lugares", {})
        filas_l = [{"MATNR": m, "WERKS": w, "LGORT": lg}
                   for m in mats.get("MATNR",[])
                   for w, locs in lugares.items() for lg in locs]
        if filas_l:
            st.dataframe(pd.DataFrame(filas_l), use_container_width=True,
                         hide_index=True, height=280)
        boton_generar("lugares")


# ══════════════════════════════════════════════════════════════════════════════
# TAB: ÁREA PLANIF. MRP
# ══════════════════════════════════════════════════════════════════════════════
if "Área planif. MRP" in nombres_tabs:
    with tabs[nombres_tabs.index("Área planif. MRP")]:
        st.info("Fijo: centro A130, área A130_0040.")
        seccion_fijos("Área planif. MRP", {
            "WERKS":"A130","BERID":"A130_0040","DISMM":"V1","DISPO":"Z01",
            "DISGR":"0000","MINBE":"10","DISLS":"EX","BSTMI":"1",
            "PLIFZ":"4","MODAV":"2","KZINI":"X","PRMOD":"J",
            "SIGGR":"4","PERAN":"60","ANZPR":"12","AUTRU":"X",
        })
        st.dataframe(pd.DataFrame({
            "MATNR": mats.get("MATNR",[""]*n),
            "WERKS": ["A130"]*n, "BERID": ["A130_0040"]*n,
            "DISMM": ["V1"]*n,   "DISPO": ["Z01"]*n,
        }), use_container_width=True, hide_index=True)
        boton_generar("planif")


# ══════════════════════════════════════════════════════════════════════════════
# TAB: DATOS DE VALORACIÓN
# ══════════════════════════════════════════════════════════════════════════════
if "Datos de valoración" in nombres_tabs:
    with tabs[nombres_tabs.index("Datos de valoración")]:
        if flujo == "Ampliación centros logísticos":
            val_cfg = cfg.get("CL_valoracion", [])
            st.info("Valoración fija por tipo de material.")
            filas_v = [{"MATNR": m, "BWKEY": v["BWKEY"], "BKLAS": v["BKLAS"],
                        "VPRSV": v["VPRSV"], "VERPR": v.get("VERPR",""),
                        "STPRS": v.get("STPRS","")}
                       for m in mats.get("MATNR",[]) for v in val_cfg]
            if filas_v:
                st.dataframe(pd.DataFrame(filas_v), use_container_width=True,
                             hide_index=True, height=250)
        else:
            st.info(f"Se generan {len(CENTRO_BENEFICIO_MAP)} filas por material (una por sucursal).")
            seccion_fijos("Valoración sucursales", {
                "BKLAS": cfg.get("SUC_bklas",""),
                "VPRSV": cfg.get("SUC_vprsv",""),
                "VERPR": cfg.get("SUC_verpr",""),
                "PEINH": cfg.get("SUC_peinh","1"),
            })
        boton_generar("valoracion")
