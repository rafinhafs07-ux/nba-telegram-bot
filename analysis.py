def analisar_jogadores(jogadores):
    under_players = []

    for j in jogadores:
        if j["threePointAttempts"] < 4 and j["threePointPct"] < 0.32:
            under_players.append(j)

    return under_players
