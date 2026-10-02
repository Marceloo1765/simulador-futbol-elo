import pandas as pd

def probabilidad_esperada(rating_a, rating_b):
    """Probabilidad de que el equipo A le gane al equipo B."""
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def actualizar_rating(rating, resultado, esperado, k=20):
    """
    resultado: 1 si ganó, 0.5 si empató, 0 si perdió
    esperado: la probabilidad calculada con probabilidad_esperada()
    """
    return rating + k * (resultado - esperado)

def procesar_partido(ratings, home, away, ftr, k=20):
    """
    Actualiza los ratings de dos equipos tras un partido.
    ratings: diccionario {equipo: rating}
    ftr: 'H' (gana local), 'D' (empate), 'A' (gana visita)
    """
    rating_home = ratings[home]
    rating_away = ratings[away]

    esperado_home = probabilidad_esperada(rating_home, rating_away)
    esperado_away = 1 - esperado_home  # son complementarios

    if ftr == "H":
        resultado_home, resultado_away = 1, 0
    elif ftr == "A":
        resultado_home, resultado_away = 0, 1
    else:  # empate
        resultado_home, resultado_away = 0.5, 0.5

    ratings[home] = actualizar_rating(rating_home, resultado_home, esperado_home, k)
    ratings[away] = actualizar_rating(rating_away, resultado_away, esperado_away, k)

    return ratings


# --- Cargar datos ---
cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
df_2024 = pd.read_csv("data/epl_2024_25.csv")[cols]

# Ordenar por fecha (CRUCIAL: el Elo depende del orden cronológico)
df_2024["Date"] = pd.to_datetime(df_2024["Date"], dayfirst=True)
df_2024 = df_2024.sort_values("Date").reset_index(drop=True)

# --- Inicializar ratings ---
equipos = set(df_2024["HomeTeam"]) | set(df_2024["AwayTeam"])
ratings = {equipo: 1500 for equipo in equipos}

# --- Recorrer todos los partidos ---
for _, partido in df_2024.iterrows():
    ratings = procesar_partido(ratings, partido["HomeTeam"], partido["AwayTeam"], partido["FTR"])

# --- Ver resultado final ---
ranking_final = sorted(ratings.items(), key=lambda x: x[1], reverse=True)

print("Ranking Elo al final de la temporada 2024-25:\n")
for i, (equipo, rating) in enumerate(ranking_final, 1):
    print(f"{i}. {equipo}: {rating:.1f}")