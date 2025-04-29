from models.player_model import Player

def build_players(df):
    players = []
    for _, row in df.iterrows():
        p = Player(row['Name'], row['Minutes Played'], row['Goals'], row['Assists'])
        players.append(p)
    return players
