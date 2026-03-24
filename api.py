import requests
import os

API_KEY = os.getenv("API_KEY")

def get_players_data():
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics?season=2023"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Erro na API:", response.status_code)
        return []

    data = response.json()

    jogadores = []

    for item in data.get("response", []):
        try:
            stats = item["statistics"][0]

            jogador = {
                "name": item["player"]["firstname"] + " " + item["player"]["lastname"],
                "threePointAttempts": stats.get("fg3a", 0),
                "threePointPct": stats.get("fg3p", 0) / 100
            }

            jogadores.append(jogador)

        except Exception as e:
            continue

    return jogadores
