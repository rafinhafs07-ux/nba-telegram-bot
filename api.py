import requests

API_KEY = "SUA_API_KEY"

def get_players_data():
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    jogadores = []

    try:
        for item in data["response"]:
            jogadores.append({
                "name": item["player"]["firstname"] + " " + item["player"]["lastname"],
                "threePointAttempts": item["statistics"][0]["fg3a"],
                "threePointPct": item["statistics"][0]["fg3p"] / 100
            })
    except:
        return []

    return jogadores
