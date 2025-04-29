from controllers.data_controller import load_match_data

import streamlit as st

st.title("📊 Resultados de Partidos")

# Cargar datos desde la API
try:
    df = load_match_data()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

# Filtros dinámicos
equipos = sorted(set(df['home_team'].dropna().unique()).union(df['away_team'].dropna().unique()))

equipo_sel = st.selectbox("Filtrar por equipo:", ["Todos"] + equipos)

# Aplicar filtros
if equipo_sel != "Todos":
    df = df[(df['home_team'] == equipo_sel) | (df['away_team'] == equipo_sel)]

# Columnas a mostrar
columnas_mostrar = [
    "date", "home_team", "home_score", "away_score", "away_team"
]

st.dataframe(df[columnas_mostrar])
