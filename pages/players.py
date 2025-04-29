import streamlit as st
from controllers.sqlite_controller import load_data, build_players

df = load_data(season="2022")
players = build_players(df)

for p in players:
    st.write(f"{p.name} - Goles/90: {p.goals_per_90():.2f}")
