import pandas as pd

df = pd.read_excel("/Users/enrique/Documents/Proyectos/Dashboard_VH26/data_gmb.xlsx")

print("=== BUSCANDO RESTAURANTES ESPECÍFICOS ===\n")

searches = ["quince", "boston", "milag", "maiña", "maina", "maian"]
for term in searches:
    matches = df[df["name"].str.lower().str.contains(term, na=False, regex=False)]
    if len(matches) > 0:
        print(f"'{term}':")
        for _, row in matches.head(3).iterrows():
            print(f"  -> {row['name']} (Rating: {row['rating']}, Reviews: {int(row['reviews'])})")
        print()
    else:
        print(f"'{term}': NO ENCONTRADO\n")

print("\n=== TOP 50 RESTAURANTES POR REVIEWS ===\n")
top = df.nlargest(50, 'reviews')
for i, (_, row) in enumerate(top.iterrows(), 1):
    print(f"{i}. {row['name']} | ⭐{row['rating']} | {int(row['reviews'])} reseñas")
