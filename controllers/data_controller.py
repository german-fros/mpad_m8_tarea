from models.match_model import Match
from models.player_model import Player

import sqlite3
import streamlit as st
import pandas as pd
from pathlib import Path
import requests

DB_PATH = Path("data/processed/processed_stats_futbol_uruguayo.db")

@st.cache_data
def load_data(season: int = None) -> pd.DataFrame:
    """Carga los datos desde SQLite. Si se indica una temporada, filtra por ella."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM stats"
    if season:
        query += f" WHERE Season = {season}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


BASE_URL = "https://api-cafecito.onrender.com"
HEADERS = {"Authorization": "Bearer EAAHlp1ycWFIBOzFZASIPjVtB1n30C8jUBKHo"}

@st.cache_data
def load_match_data() -> pd.DataFrame:
    """Carga datos de partidos desde la API y los devuelve como DataFrame."""
    url = f"{BASE_URL}/matches/competition/Europe-Champions-League-2024-2025/season/10456"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    data = response.json()
    df = pd.DataFrame(data)

    # Filtrar por stage
    df = df[df['stage'] == '23663']
    
    return df