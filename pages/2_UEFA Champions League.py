import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd

from controllers.data_controller import load_match_data
from common.pdf_generator import exportar_resultados_pdf
from login import login

st.set_page_config(page_title="UEFA Champions League", page_icon="", layout="centered")

login()

st.title("UEFA Champions League")
st.title("📊 Resultados | Fase de grupos")
st.markdown("---")

# Cargar datos desde la API
try:
    df = load_match_data()

    df["home_score"] = pd.to_numeric(df["home_score"], errors="coerce").fillna(0).astype(int)
    df["away_score"] = pd.to_numeric(df["away_score"], errors="coerce").fillna(0).astype(int)

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

st.markdown("---")

df = df.drop_duplicates(subset="match_id")

st.markdown("### Top 10 Equipos")

tipo_metrica = st.selectbox("Seleccionar métrica:", ["Goles a favor", "Goles en contra"])
orden_metrica = st.selectbox("Ordenar:", ["Mayor a menor", "Menor a mayor"])

# Unificar en una sola tabla
df_goles = pd.DataFrame()

# Goles a favor: sumando por equipo como local y visitante
goles_local = df.groupby("home_team")["home_score"].sum()
goles_visitante = df.groupby("away_team")["away_score"].sum()
goles_favor = goles_local.add(goles_visitante, fill_value=0)

# Goles en contra
goles_contra_local = df.groupby("home_team")["away_score"].sum()
goles_contra_visitante = df.groupby("away_team")["home_score"].sum()
goles_contra = goles_contra_local.add(goles_contra_visitante, fill_value=0)

df_goles["Goles a favor"] = goles_favor
df_goles["Goles en contra"] = goles_contra
df_goles = df_goles.fillna(0)

ascendente = orden_metrica == "Menor a mayor"
columna = tipo_metrica

top_equipos = df_goles.sort_values(by=columna, ascending=ascendente).head(10)

fig, ax = plt.subplots(figsize=(7, 4))
valores = top_equipos[columna].values
norm = plt.Normalize(valores.min(), valores.max())
colors = cm.Wistia(norm(valores))  # Podés usar cm.Blues, cm.Oranges, etc.

bars = ax.barh(top_equipos.index, valores, color=colors)

# Estilo minimalista
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.xaxis.set_visible(False)

fig.patch.set_facecolor('none')
ax.set_facecolor('none')

# Etiquetas en blanco al lado de la barra
for i, (equipo, valor) in enumerate(zip(top_equipos.index, top_equipos[columna])):
    ax.annotate(
        f"{int(valor)}",
        xy=(valor, i),
        xytext=(5, 0),
        textcoords='offset points',
        va='center',
        ha='left',
        fontsize=10,
        color='white'
    )

ax.set_title(f"Top 10 Equipos por {columna}", color='white', fontweight='bold')
ax.invert_yaxis()
ax.tick_params(axis='y', size=0, colors='white', labelsize=10, pad=10)
ax.set_yticks(range(len(top_equipos)))
ax.set_yticklabels(top_equipos.index, fontweight='bold', color='white')

st.pyplot(fig)

# Crear versión alternativa del gráfico con texto negro para PDF
fig_pdf, ax_pdf = plt.subplots(figsize=(7, 4.5))
ax_pdf.barh(top_equipos.index, valores, color=colors)

# Estilo visual limpio
ax_pdf.spines['top'].set_visible(False)
ax_pdf.spines['right'].set_visible(False)
ax_pdf.spines['bottom'].set_visible(False)
ax_pdf.spines['left'].set_visible(False)
ax_pdf.xaxis.set_visible(False)

fig_pdf.patch.set_facecolor('none')
ax_pdf.set_facecolor('none')

# Etiquetas en negro
for i, (equipo, valor) in enumerate(zip(top_equipos.index, valores)):
    ax_pdf.annotate(
        str(int(valor)),
        xy=(valor, i),
        xytext=(5, 0),
        textcoords='offset points',
        va='center',
        ha='left',
        fontsize=10,
        color='black'
    )

# Título y estilo
ax_pdf.set_title(f"Top 10 Equipos por {columna}", color='black', fontweight='bold')
ax_pdf.invert_yaxis()
ax_pdf.tick_params(axis='y', size=0, colors='black', labelsize=10, pad=10)
ax_pdf.set_yticks(range(len(top_equipos)))
ax_pdf.set_yticklabels(top_equipos.index, fontweight='bold', color='black')

# Guardar imagen
fig_pdf.savefig("grafico_resultados.png", dpi=300, bbox_inches="tight", transparent=True)
plt.close(fig_pdf)

with open(exportar_resultados_pdf(df, columnas_mostrar), "rb") as f:
    st.download_button(
        label="📄 Exportar a PDF",
        data=f,
        file_name="resultados_partidos.pdf",
        mime="application/pdf"
    )