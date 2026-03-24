import requests
import os

API_KEY = os.getenv("API_KEY")

def get_players_data():
    url = "https://api-nba-v1.p.rapidapi.com/players?season=2023"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Erro API:", response.status_code)
        return []

    data = response.json()

    jogadores = []

    for item in data.get("response", []):
        try:
            jogador = {
                "name": item["firstname"] + " " + item["lastname"],
                "threePointAttempts": 0,  # essa API não traz direto
                "threePointPct": 0        # precisa de outro endpoint
            }

            jogadores.append(jogador)

        except:
            continue

    return jogadores
