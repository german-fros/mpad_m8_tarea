import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

from controllers.data_controller import load_data
from login import login
from common.pdf_generator import exportar_pdf_stats

st.set_page_config(page_title="Campeonato Uruguayo", page_icon="", layout="wide")

login()

st.title("Estadísticas de Jugadores")
st.title("🇺🇾 Campeonato Uruguayo 🇺🇾")
st.markdown("---")

# Temporadas disponibles
temporadas = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
season = st.selectbox("Selecciona la temporada:", temporadas)

# Cargar datos desde SQLite
df = load_data(season)

# Dejar solo la primera posición si hay varias
df["Position"] = df["Position"].astype(str).apply(lambda x: x.split(",")[0].strip())

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

# Opciones de métricas disponibles
metricas_disponibles = {
    "Goles": "Goals",
    "Asistencias": "Assists",
    "Minutos jugados": "Minutes played",
    "Tiros al arco (por 90')": "Shots on target per 90",
    "Pases clave (por 90')": "Key passes per 90",
    "Intercepciones (por 90)": "Interceptions per 90"
}

metrica_orden = st.selectbox("📊 Ordenar jugadores por:", list(metricas_disponibles.keys()))
columna_orden = metricas_disponibles[metrica_orden]

# Asegurar tipo numérico antes de ordenar
df[columna_orden] = pd.to_numeric(df[columna_orden], errors="coerce")

# Ordenar y limitar
df_ordenado = df.sort_values(by=columna_orden, ascending=False).head(10)

st.dataframe(df_ordenado[columnas_mostrar])

st.markdown("---")

# Asegurar tipo numérico y ordenar por métrica elegida
df[columna_orden] = pd.to_numeric(df[columna_orden], errors="coerce")
top10 = df_ordenado.copy()

if not top10.empty:
    # top10 = top10.sort_values(by=columna_orden, ascending=False)
    valores = top10[columna_orden].fillna(0).values
    norm = plt.Normalize(valores.min(), valores.max())
    colors = cm.Wistia(norm(valores))  # Usamos cmap "Blues"

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(top10["Player"], valores, color=colors)

    # Estilo minimalista
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.xaxis.set_visible(False)

    # Fondo blanco para integrar con Streamlit
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    # Etiquetas de valor como enteros
    for i, (valor, jugador) in enumerate(zip(valores, top10["Player"])):
        if pd.notna(valor):
            ax.annotate(
                f"{valor:.2f}" if 'per 90' in columna_orden else f"{int(valor)}",xy=(valor, i),             
                xytext=(5, 0),             
                textcoords='offset points',
                va='center',
                ha='left',
                fontsize=10,
                color='white'
            )



    ax.set_title(f"Top 10 Jugadores por {metrica_orden}", color='white',fontweight='bold')
    ax.invert_yaxis()
    ax.tick_params(axis='y', size=0, colors='white', labelsize=10, pad=10)
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10["Player"], fontweight='bold')
    st.pyplot(fig)

    # Crear versión alternativa del gráfico con texto negro para el PDF
    fig_pdf, ax_pdf = plt.subplots(figsize=(7, 4.5))
    ax_pdf.barh(top10["Player"], valores, color=colors)

    # Estilo limpio
    ax_pdf.spines['top'].set_visible(False)
    ax_pdf.spines['right'].set_visible(False)
    ax_pdf.spines['bottom'].set_visible(False)
    ax_pdf.spines['left'].set_visible(False)
    ax_pdf.xaxis.set_visible(False)
    fig_pdf.patch.set_facecolor('none')
    ax_pdf.set_facecolor('none')

    # Título y ejes en negro
    ax_pdf.set_title(f"Top 10 Jugadores por {metrica_orden}", color='black', fontweight='bold')
    ax_pdf.tick_params(axis='y', size=0, colors='black', labelsize=10, pad=10)
    ax_pdf.set_yticks(range(len(top10)))
    ax_pdf.set_yticklabels(top10["Player"], fontweight='bold', color='black')

    # Etiquetas en negro
    for i, (valor, jugador) in enumerate(zip(valores, top10["Player"])):
        if pd.notna(valor):
            ax_pdf.annotate(
                f"{valor:.2f}" if 'per 90' in columna_orden else f"{int(valor)}",
                xy=(valor, i),
                xytext=(5, 0),
                textcoords='offset points',
                va='center',
                ha='left',
                fontsize=10,
                color='black'
            )

    ax_pdf.invert_yaxis()

    # Guardar gráfico para PDF
    fig_pdf.savefig("grafico_jugadores.png", dpi=300, bbox_inches="tight", transparent=True)
    plt.close(fig_pdf)  # liberar recursos

else:
    st.warning(f"No hay datos suficientes para mostrar el Top 10 de {metrica_orden}.")

with open(exportar_pdf_stats(df_ordenado, columnas_mostrar, season), "rb") as f:
    st.download_button(
        label="📄 Exportar a PDF",
        data=f,
        file_name="jugadores_stats.pdf",
        mime="application/pdf"
    )




