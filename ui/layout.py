import streamlit as st


def shell_bar():
    """Barra azul superior estilo SAP Fiori."""
    st.markdown("""
    <div class="sap-shell">
      <div>
        <span class="sap-shell-title">🔷 SAP Material Management</span>
        <span class="sap-shell-sub" style="margin-left:1rem">
          Ampliación y modificación masiva
        </span>
      </div>
      <div style="font-size:11px;opacity:0.7;color:white">v4.0</div>
    </div>
    """, unsafe_allow_html=True)


def breadcrumb(titulo: str):
    """Ruta de navegación debajo del shell bar."""
    st.markdown(f"""
    <div class="sap-breadcrumb">
      <a href="#">Inicio</a> &rsaquo;
      Gestión de materiales &rsaquo;
      <strong>{titulo}</strong>
    </div>
    """, unsafe_allow_html=True)


def page_title(tipo: str, titulo: str):
    """Encabezado de página con tipo de objeto y título principal."""
    st.markdown(f"""
    <div class="sap-page-title">
      <div>
        <div class="sap-obj-type">{tipo}</div>
        <h1>{titulo}</h1>
      </div>
    </div>
    """, unsafe_allow_html=True)


def context_bar(tipo_mat: str, flujo: str, n_materiales: int):
    """Barra con el contexto de la operación actual."""
    st.markdown(f"""
    <div class="sap-ctx-bar">
      <span>Tipo de material:
        <span class="sap-ctx-val">{tipo_mat.replace("_", " ")}</span>
      </span>
      <span class="sap-ctx-sep">|</span>
      <span>Operación:
        <span class="sap-ctx-val">{flujo}</span>
      </span>
      <span class="sap-ctx-sep">|</span>
      <span>Materiales cargados:
        <span class="sap-ctx-val">{n_materiales}</span>
      </span>
    </div>
    """, unsafe_allow_html=True)


def section_open(titulo: str, icono: str = "📄"):
    """Abre un bloque de sección SAP (card con header gris)."""
    st.markdown(f"""
    <div class="sap-section">
      <div class="sap-section-header">{icono} {titulo}</div>
      <div class="sap-section-body">
    """, unsafe_allow_html=True)


def section_close():
    """Cierra el bloque de sección SAP."""
    st.markdown("""
      </div>
    </div>
    """, unsafe_allow_html=True)


def section_header_inline(texto: str, icono: str = "📍"):
    """Header de sección secundaria (usado para separar centros dentro de un tab)."""
    st.markdown(f"""
    <div class="sap-section-header"
         style="border-radius:4px;margin:1rem 0 0.6rem;border:1px solid #d9d9d9">
      {icono} {texto}
    </div>
    """, unsafe_allow_html=True)


def table_label(texto: str):
    """Label de tabla SAP (uppercase, gris, con borde inferior)."""
    st.markdown(
        f'<div class="sap-table-label">{texto}</div>',
        unsafe_allow_html=True,
    )
