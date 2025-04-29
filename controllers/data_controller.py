from models.match_model import Match
from models.player_model import Player

import sqlite3
import pandas as pd
from pathlib import Path

def extract_matches(api_data):
    return [
        Match(
            m['date'], m['home_team'], m['away_team'],
            int(m['home_score']), int(m['away_score'])
        )
        for m in api_data
    ]


def build_players(df):
    players = []
    for _, row in df.iterrows():
        p = Player(row['Name'], row['Minutes Played'], row['Goals'], row['Assists'])
        players.append(p)
    return players

DB_PATH = Path("data/processed_stats_futbol_uruguayo.db")

def load_data(season: int = None) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM stats"
    if season:
        query += f" WHERE Season = {season}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df