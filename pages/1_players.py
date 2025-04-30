import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from controllers.data_controller import load_data
from login import login

login()

st.title("🏃 Estadísticas de Jugadores")

# Temporadas disponibles
temporadas = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
season = st.selectbox("Selecciona la temporada:", temporadas)

# Cargar datos desde SQLite
df = load_data(season)

# Crear "Shots on target per 90"
df["Shots"] = pd.to_numeric(df["Shots"], errors="coerce")
df["Shots on target, %"] = pd.to_numeric(df["Shots on target, %"], errors="coerce")
df["Minutes played"] = pd.to_numeric(df["Minutes played"], errors="coerce")

# Calcular Shots on target per 90
df["Shots on target per 90"] = (
    df["Shots"] * (df["Shots on target, %"] / 100)
) * 90 / df["Minutes played"]


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

# Opciones de métricas disponibles
metricas_disponibles = {
    "Goles": "Goals",
    "Asistencias": "Assists",
    "Minutos jugados": "Minutes played",
    "Tiros al arco (por 90')": "Shots on target per 90",
    "Pases clave (por 90')": "Key passes per 90"
}

# Selector de métrica
metrica_label = st.selectbox("Elige una métrica para el Top 10:", list(metricas_disponibles.keys()))
columna_metrica = metricas_disponibles[metrica_label]

# Asegurar tipo numérico y ordenar por métrica elegida
df[columna_metrica] = pd.to_numeric(df[columna_metrica], errors="coerce")
top10 = df.dropna(subset=[columna_metrica]).sort_values(by=columna_metrica, ascending=False).head(10)

if not top10.empty:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top10["Player"], top10[columna_metrica], color="#2c7be5")
    ax.set_xlabel(metrica_label)
    ax.set_title(f"Top 10 Jugadores por {metrica_label}")
    ax.invert_yaxis()
    st.pyplot(fig)
else:
    st.warning(f"No hay datos suficientes para mostrar el Top 10 de {metrica_label}.")



