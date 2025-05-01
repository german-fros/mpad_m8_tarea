from login import login

import streamlit as st

st.set_page_config(
    page_title="Streamlit - German Fros",
    page_icon="⚽",
    layout="centered"
)

login()


st.title(f"⚽ Bienvenido, {st.session_state.usuario}")
st.write("Usa el menú lateral para navegar entre las páginas.")
