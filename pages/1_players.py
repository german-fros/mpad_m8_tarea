import streamlit as st
from controllers.data_controller import load_data

st.title("🏃 Estadísticas de Jugadores")

# Temporadas disponibles
temporadas = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
season = st.selectbox("Selecciona la temporada:", temporadas)

# Cargar datos desde SQLite
df = load_data(season)

# Mostrar tabla con columnas esenciales
columnas_esenciales = [
    "Player", "Team", "Position", "Matches played", "Minutes played",
    "Goals", "Assists", "Shots on target per 90", 
    "Shot accuracy, %", "Key passes per 90", "Pass accuracy, %",
    "Tackles per 90", "Interceptions per 90"
]

# Filtrar columnas que existan (por si hay diferencias entre temporadas)
columnas_mostrar = [col for col in columnas_esenciales if col in df.columns]

st.dataframe(df[columnas_mostrar])

