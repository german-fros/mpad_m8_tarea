import streamlit as st

# === CONFIGURACIÓN BÁSICA ===
st.set_page_config(
    page_title="Título de la Página",
    page_icon="⚽",
    layout="wide",    # "centered" o "wide"
    initial_sidebar_state="expanded"
)

# === CABECERA O TÍTULO PRINCIPAL ===
st.title("Bienvenido a mi Aplicación")

# === SUBTÍTULOS O TEXTOS ===
st.header("Análisis de datos")
st.subheader("Sección de visualización")
st.text("Este es un texto normal de explicación.")

# === ELEMENTOS INTERACTIVOS ===
opcion = st.selectbox(
    'Elige una opción:',
    ('Opción 1', 'Opción 2', 'Opción 3')
)

valor_slider = st.slider('Selecciona un valor:', 0, 100, 50)

# === MOSTRAR DATAFRAMES O TABLAS ===
import pandas as pd
df = pd.DataFrame({
    'Columna 1': [1, 2, 3],
    'Columna 2': ['A', 'B', 'C']
})

st.dataframe(df)

# === MOSTRAR GRÁFICOS ===
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [10, 20, 30])
st.pyplot(fig)

# === CÓDIGOS O ALERTAS ===
st.code("print('Hola Mundo')", language='python')
st.success('Operación realizada con éxito.')
st.error('Hubo un error en la operación.')
st.warning('Advertencia: Verifica tus datos.')

# === SIDEBAR ===
st.sidebar.title("Menú Lateral")
st.sidebar.button("Botón lateral")

# === FOOTER O CIERRE ===
st.write("Gracias por visitar la aplicación.")
