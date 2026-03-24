def analisar_jogadores(jogadores):
    under_players = []

    for j in jogadores:
        if (
            j["threePointAttempts"] < 4 and
            j["threePointPct"] < 0.32 and
            j["minutes"] > 10  # evita jogadores irrelevantes
        ):
            under_players.append(j)

    return under_players
