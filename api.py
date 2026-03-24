import requests
import os

API_KEY = os.getenv("API_KEY")

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}

# 🔹 Pega estatísticas completas
def get_players_stats():
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics?season=2023"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Erro ao buscar stats:", response.status_code)
        return []

    data = response.json()
    return data.get("response", [])


# 🔹 Processa dados para seu bot
def get_players_data():
    stats_data = get_players_stats()

    jogadores = []

    for item in stats_data:
        try:
            player = item["player"]
            stats = item["statistics"][0]

            jogador = {
                "name": player["firstname"] + " " + player["lastname"],
                "threePointAttempts": stats.get("fg3a", 0),
                "threePointPct": stats.get("fg3p", 0) / 100,
                "minutes": stats.get("min", 0),
                "games": stats.get("games", 0)
            }

            jogadores.append(jogador)

        except:
            continue

    return jogadores
