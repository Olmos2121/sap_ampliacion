import streamlit as st


def load_css(file_name: str):
    """Carga un archivo CSS externo e inyecta en la app con st.markdown."""
    with open(file_name, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
