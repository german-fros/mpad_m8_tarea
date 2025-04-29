from models.match_model import Match

def extract_matches(api_data):
    return [
        Match(
            m['date'], m['home_team'], m['away_team'],
            int(m['home_score']), int(m['away_score'])
        )
        for m in api_data
    ]
