from fpdf import FPDF
import os

class JugadoresPDF(FPDF):
    def __init__(self, season):
        super().__init__()
        self.season = season

    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Estadísticas de Jugadores | Temporada {self.season}", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def exportar_pdf(df, columnas, season, nombre_archivo="jugadores_stats.pdf"):
    pdf = JugadoresPDF(season)
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 10)

    # Mapeo de alias para el encabezado
    alias_columnas = {
        "Matches played": "MP",
        "Minutes played": "Min",
        "Goals": "G",
        "Assists": "A",
        "Shots on target per 90": "SOT/90",
        "Shot accuracy, %": "SAcc%",
        "Key passes per 90": "KP/90",
        "Pass accuracy, %": "PAcc%",
        "Tackles per 90": "Tkl/90",
        "Interceptions per 90": "Int/90"
    }

    columnas_aliasadas = [alias_columnas.get(col, col) for col in columnas]
    col_width = 190 / len(columnas)

    # Encabezado con alias
    pdf.set_fill_color(230, 230, 230)
    for alias in columnas_aliasadas:
        pdf.cell(col_width, 8, alias, border=1, ln=0, align="C", fill=True)
    pdf.ln()

    # Filas
    for _, row in df[columnas].iterrows():
        for col in columnas:
            valor = row[col]
            if isinstance(valor, float):
                texto = f"{valor:.2f}"
            else:
                texto = str(valor)
            texto = texto[:20]

            if col in ["Player", "Team"]:
                pdf.set_font("Arial", "", 8)
            else:
                pdf.set_font("Arial", "", 10)

            pdf.cell(col_width, 8, texto, border=1, ln=0, align="C")
        pdf.ln()

    # Añadir imagen del gráfico debajo de la tabla
    if os.path.exists("grafico_jugadores.png"):
        pdf.ln(10)
        pdf.image("grafico_jugadores.png", x=10, w=190)  # ajusta ancho si querés
        os.remove("grafico_jugadores.png")


    pdf.output(nombre_archivo)
    return nombre_archivo

