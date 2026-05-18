import streamlit as st
import pandas as pd
from io import BytesIO
from config import TIPOS_MATERIAL, CENTRO_BENEFICIO_MAP, SOCIEDAD_MAP
from generators.centros_logisticos import generar_centros_logisticos
from generators.sucursales import generar_sucursales
from generators.modificacion import generar_modificacion

st.set_page_config(
    page_title="SAP - Ampliación masiva de materiales",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Ampliación masiva de materiales SAP")
st.caption("Generador de archivos para carga masiva vía LSMW / MM17")

tab1, tab2, tab3 = st.tabs([
    "🏭 Ampliación centros logísticos",
    "🏪 Ampliación sucursales",
    "✏️ Modificación datos básicos"
])

# ─── TAB 1: CENTROS LOGÍSTICOS ────────────────────────────────────────────────
with tab1:
    st.subheader("Ampliación de centros logísticos")
    st.info("Genera las vistas: Datos básicos, Datos de centro, Cadenas de distribución, Clasificación fiscal, Datos de previsión, Lugares de almacenamiento, Área planif. MRP y Datos de valoración.")

    col1, col2 = st.columns([1, 2])

    with col1:
        tipo_mat_cl = st.selectbox(
            "Tipo de material",
            options=list(TIPOS_MATERIAL.keys()),
            key="tipo_cl"
        )
        uploaded_cl = st.file_uploader(
            "Cargar Excel con materiales",
            type=["xlsx", "xls"],
            key="upload_cl",
            help="El archivo debe tener una hoja con columnas: MATNR, MAKTX, MATKL, PRDHA, VOLUM y campos variables según el tipo."
        )

    with col2:
        st.markdown("**Campos requeridos en el Excel de entrada:**")
        campos_req = TIPOS_MATERIAL[tipo_mat_cl]["campos_entrada"]
        cols = st.columns(3)
        for i, campo in enumerate(campos_req):
            cols[i % 3].markdown(f"- `{campo}`")

    if uploaded_cl:
        try:
            df_input = pd.read_excel(uploaded_cl, dtype=str).fillna("")
            df_input.columns = df_input.columns.str.strip()
            st.success(f"✅ {len(df_input)} materiales cargados")
            st.dataframe(df_input.head(5), use_container_width=True)

            campos_faltantes = [c for c in campos_req if c not in df_input.columns]
            if campos_faltantes:
                st.error(f"⚠️ Faltan columnas en el Excel: {', '.join(campos_faltantes)}")
            else:
                if st.button("Generar archivo SAP", key="btn_cl", type="primary"):
                    with st.spinner("Generando..."):
                        output = generar_centros_logisticos(df_input, tipo_mat_cl)
                    st.download_button(
                        label="⬇️ Descargar Excel SAP",
                        data=output,
                        file_name=f"Ampliacion_CL_{tipo_mat_cl}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_cl"
                    )
        except Exception as e:
            st.error(f"Error leyendo el archivo: {e}")

    with st.expander("📋 Ver plantilla de entrada"):
        campos_req = TIPOS_MATERIAL[tipo_mat_cl]["campos_entrada"]
        df_plantilla = pd.DataFrame(columns=campos_req)
        buf = BytesIO()
        df_plantilla.to_excel(buf, index=False)
        st.download_button(
            "⬇️ Descargar plantilla",
            data=buf.getvalue(),
            file_name=f"Plantilla_{tipo_mat_cl}_CL.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="tpl_cl"
        )

# ─── TAB 2: SUCURSALES ────────────────────────────────────────────────────────
with tab2:
    st.subheader("Ampliación de sucursales")
    st.info("Genera las vistas: Datos básicos (solo almacenamiento) y Datos de centro para los ~70 centros de sucursales.")

    TIPOS_SUCURSALES = {k: v for k, v in TIPOS_MATERIAL.items() if k in ["ZMED", "ZNOM", "ZINS"]}

    col1, col2 = st.columns([1, 2])

    with col1:
        tipo_mat_suc = st.selectbox(
            "Tipo de material",
            options=list(TIPOS_SUCURSALES.keys()),
            key="tipo_suc"
        )
        uploaded_suc = st.file_uploader(
            "Cargar Excel con materiales",
            type=["xlsx", "xls"],
            key="upload_suc"
        )

    with col2:
        st.markdown("**Campos requeridos:**")
        st.markdown("- `MATNR` — Número de material")
        st.markdown("Los centros/sociedad/beneficio se toman del mapa de centros configurado.")

    if uploaded_suc:
        try:
            df_input_suc = pd.read_excel(uploaded_suc, dtype=str).fillna("")
            df_input_suc.columns = df_input_suc.columns.str.strip()
            st.success(f"✅ {len(df_input_suc)} materiales cargados")
            st.dataframe(df_input_suc.head(5), use_container_width=True)

            if "MATNR" not in df_input_suc.columns:
                st.error("⚠️ El archivo debe tener la columna MATNR")
            else:
                if st.button("Generar archivo SAP", key="btn_suc", type="primary"):
                    with st.spinner("Generando..."):
                        output = generar_sucursales(df_input_suc, tipo_mat_suc)
                    st.download_button(
                        label="⬇️ Descargar Excel SAP",
                        data=output,
                        file_name=f"Ampliacion_SUC_{tipo_mat_suc}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_suc"
                    )
        except Exception as e:
            st.error(f"Error leyendo el archivo: {e}")

    with st.expander("🗺️ Ver mapa de centros cargado"):
        df_mapa = pd.DataFrame([
            {"WERKS": k, "KOKRS": v["KOKRS"], "PRCTR": v["PRCTR"]}
            for k, v in CENTRO_BENEFICIO_MAP.items()
        ])
        st.dataframe(df_mapa, use_container_width=True)

# ─── TAB 3: MODIFICACIÓN ─────────────────────────────────────────────────────
with tab3:
    st.subheader("Modificación de datos básicos")
    st.info("Genera la vista Datos básicos con los campos modificables: descripción, jerarquía, volumen, texto largo y bloqueo.")

    col1, col2 = st.columns([1, 2])

    with col1:
        tipo_mat_mod = st.selectbox(
            "Tipo de material",
            options=list(TIPOS_MATERIAL.keys()),
            key="tipo_mod"
        )
        uploaded_mod = st.file_uploader(
            "Cargar Excel con materiales a modificar",
            type=["xlsx", "xls"],
            key="upload_mod"
        )

    with col2:
        st.markdown("**Campos requeridos en el Excel de entrada:**")
        campos_mod = TIPOS_MATERIAL[tipo_mat_mod]["campos_modificacion"]
        for c in campos_mod:
            st.markdown(f"- `{c}`")

    if uploaded_mod:
        try:
            df_input_mod = pd.read_excel(uploaded_mod, dtype=str).fillna("")
            df_input_mod.columns = df_input_mod.columns.str.strip()
            st.success(f"✅ {len(df_input_mod)} materiales cargados")
            st.dataframe(df_input_mod.head(5), use_container_width=True)

            campos_faltantes = [c for c in ["MATNR"] if c not in df_input_mod.columns]
            if campos_faltantes:
                st.error(f"⚠️ Falta la columna MATNR")
            else:
                if st.button("Generar archivo SAP", key="btn_mod", type="primary"):
                    with st.spinner("Generando..."):
                        output = generar_modificacion(df_input_mod, tipo_mat_mod)
                    st.download_button(
                        label="⬇️ Descargar Excel SAP",
                        data=output,
                        file_name=f"Modificacion_{tipo_mat_mod}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="dl_mod"
                    )
        except Exception as e:
            st.error(f"Error leyendo el archivo: {e}")

    with st.expander("📋 Ver plantilla de entrada"):
        campos_mod = TIPOS_MATERIAL[tipo_mat_mod]["campos_modificacion"]
        df_plantilla_mod = pd.DataFrame(columns=campos_mod)
        buf2 = BytesIO()
        df_plantilla_mod.to_excel(buf2, index=False)
        st.download_button(
            "⬇️ Descargar plantilla",
            data=buf2.getvalue(),
            file_name=f"Plantilla_Modificacion_{tipo_mat_mod}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="tpl_mod"
        )
