#!/usr/bin/env python3
"""Verifica que las normalizaciones funcionen correctamente."""
import pandas as pd
from collections import Counter
import sys
sys.path.insert(0, '.')

# Importar la función del app
from app import normalize_restaurant_name, is_valid_restaurant_name

# Cargar datos
df = pd.read_csv('data_encuestas.csv')

# Columnas de categorías
category_columns = [
    'Mariscos', 'Carne', 'Hamburguesas', 'Pizzas', 'Sushi', 'Tacos',
    'Comida típica tabasqueña', 'Mexicana', 'Desayunos', 'Brunch', 
    'Bar', 'Bufete', 'Está de moda', 'Ya no está de moda:', 'Celebraciones'
]

# Columnas generales
general_columns = ['Restaurante_1', 'Restaurante_2', 'Restaurante_3', 'Restaurante_4', 'Restaurante_5']

# Contar todas las menciones con normalización
all_counter = Counter()

for col in category_columns + general_columns:
    if col in df.columns:
        for val in df[col].dropna():
            name = str(val).strip()
            if name and is_valid_restaurant_name(name):
                normalized = normalize_restaurant_name(name)
                if normalized:
                    all_counter[normalized] += 1

print("=" * 80)
print("TOP 30 RESTAURANTES GLOBALES (CON NORMALIZACIÓN)")
print("=" * 80)

for i, (name, count) in enumerate(all_counter.most_common(30), 1):
    print(f"{i:3}. {name}: {count}")

print("\n" + "=" * 80)
print("VERIFICACIÓN DE DUPLICIDADES ESPECÍFICAS")
print("=" * 80)

# Verificar que las variaciones se consolidaron
test_cases = [
    ('El Teapaneco', ['el teapaneco', 'teapaneco', 'El Teapaneco', 'Teapaneco']),
    ('El Edén', ['el eden', 'el edén', 'eden', 'edén', 'El Eden', 'El Edén', 'Eden']),
    ('7 Quince', ['7 quince', '7quince', '715', '7:15', '7 Quince', '7Quince']),
    ('Los Tulipanes', ['los tulipanes', 'tulipanes', 'Los Tulipanes', 'Tulipanes']),
    ('Madison Grill', ['madison', 'madison grill', 'Madison', 'Madison Grill']),
    ('A Takear', ['a takear', 'atakear', 'a taquear', 'A Takear', 'Atakear']),
    ('El Matador', ['el matador', 'matador', 'El Matador', 'Matador']),
    ('El Ganadero', ['el ganadero', 'ganadero', 'El Ganadero', 'Ganadero']),
    ("Domino's", ['dominos', "domino's", 'dominós', 'Dominos', "Domino's"]),
    ('Banquetacos', ['banquetacos', 'banquetakos', 'banketacos', 'Banquetacos']),
    ('El Rincón Tabasqueño', ['el rincon tabasqueño', 'rincón tabasqueño', 'rincon tabasqueño']),
    ('Karukay', ['karukay', 'karukai', 'Karukay', 'Karukai']),
]

for canonical, variants in test_cases:
    results = []
    for v in variants:
        normalized = normalize_restaurant_name(v)
        results.append(f"{v} -> {normalized}")
    
    all_match = all(normalize_restaurant_name(v) == canonical for v in variants)
    status = "✅" if all_match else "❌"
    print(f"\n{status} {canonical}:")
    for r in results:
        print(f"   {r}")

print("\n" + "=" * 80)
print("ANÁLISIS POR CATEGORÍA (TOP 5)")
print("=" * 80)

for col in category_columns:
    if col in df.columns:
        counter = Counter()
        for val in df[col].dropna():
            name = str(val).strip()
            if name and is_valid_restaurant_name(name):
                normalized = normalize_restaurant_name(name)
                if normalized:
                    counter[normalized] += 1
        
        print(f"\n{col}:")
        for name, count in counter.most_common(5):
            print(f"   {name}: {count}")
