import streamlit as st
from controllers.data_controller import get_api_data, parse_matches

raw_data = get_api_data()
matches = parse_matches(raw_data)

for match in matches:
    st.write(f"{match.date}: {match.home_team} {match.home_score} - {match.away_score} {match.away_team} → Ganador: {match.winner()}")
