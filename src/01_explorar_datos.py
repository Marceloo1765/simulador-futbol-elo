import pandas as pd

cols = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]

df_2024 = pd.read_csv("data/epl_2024_25.csv")[cols]
df_2025 = pd.read_csv("data/epl_2025_26.csv")[cols]
df_2026 = pd.read_csv("data/epl_2026_27.csv")[cols]

print("\nResultados 2024-25:")
print(df_2024["FTR"].value_counts())

# Verifica consistencia de nombres de equipos entre temporadas
equipos_2024 = set(df_2024["HomeTeam"])
equipos_2025 = set(df_2025["HomeTeam"])
equipos_2026 = set(df_2026["HomeTeam"])

print("\nEquipos solo en 24-25:", equipos_2024 - equipos_2025 - equipos_2026)
print("Equipos solo en 25-26:", equipos_2025 - equipos_2024 - equipos_2026)
print("Equipos solo en 26-27:", equipos_2026 - equipos_2024 - equipos_2025)