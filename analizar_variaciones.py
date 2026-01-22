import pandas as pd
from collections import Counter

df = pd.read_csv("data_encuestas.csv")
rest_cols = ["Restaurante_1", "Restaurante_2", "Restaurante_3", "Restaurante_4", "Restaurante_5"]
cat_cols = ["Mariscos", "Carne", "Hamburguesas", "Pizzas", "Sushi", "Tacos", "Desayunos", "Bar", "Bufete", "Celebraciones", "Está de moda", "Ya no está de moda:"]

all_mentions = []
for col in rest_cols + cat_cols:
    if col in df.columns:
        vals = df[col].dropna().astype(str).str.strip()
        vals = vals[~vals.isin(["1", "No responde", "No sé", "Ninguno"])]
        all_mentions.extend(vals.tolist())

keywords = ["bari", "bosto", "donald", "manila", "groshi", "machet", "sushi", "quince", "reyn", "lupita", "milag", "wing", "carl", "tacos", "fuego"]
for kw in keywords:
    matches = [m for m in all_mentions if kw.lower() in m.lower()]
    if matches:
        counts = Counter(matches)
        print(f"=== {kw.upper()} ===")
        for name, count in counts.most_common(10):
            print(f"  {count}: {name}")
        print()
