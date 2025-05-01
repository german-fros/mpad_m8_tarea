import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd

from controllers.data_controller import load_match_data
from login import login

# login()

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

# Guardar imagen para PDF (opcional)
fig.savefig("grafico_resultados.png", dpi=300, bbox_inches="tight", transparent=True)

