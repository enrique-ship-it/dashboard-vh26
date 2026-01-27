#!/usr/bin/env python3
"""
Análisis exhaustivo de la base de datos de restaurantes
Para detectar duplicidades y verificar menciones
"""

import pandas as pd
from collections import Counter
import re

# Cargar datos
df = pd.read_csv('data_encuestas.csv')

print("=" * 80)
print("ANÁLISIS EXHAUSTIVO DE BASE DE DATOS - RESTAURANTES VH26")
print("=" * 80)
print(f"\nTotal de encuestas: {len(df)}")
print(f"Total de columnas: {len(df.columns)}")

# Columnas de restaurantes por categoría
categoria_cols = {
    'Mariscos': 'Mariscos',
    'Carne': 'Carne', 
    'Hamburguesas': 'Hamburguesas',
    'Pizzas': 'Pizzas',
    'Sushi': 'Sushi',
    'Tacos': 'Tacos',
    'Comida típica tabasqueña': 'Comida típica tabasqueña',
    'Mexicana': 'Mexicana',
    'Desayunos': 'Desayunos',
    'Brunch': 'Brunch',
    'Bar': 'Bar',
    'Bufete': 'Bufete',
    'Está de moda': 'Está de moda',
    'Ya no está de moda:': 'Ya no está de moda:',
    'Celebraciones': 'Celebraciones'
}

# Columnas de restaurantes generales
rest_cols = ['Restaurante_1', 'Restaurante_2', 'Restaurante_3', 'Restaurante_4', 'Restaurante_5']

# Valores inválidos a excluir
invalid_vals = {'1', 'No responde', 'No respondió', 'No respondio', 'No sé', 
                'No se', 'No', 'Ninguno', 'N/A', 'Na', 'No Respondió', 'No Respondio',
                '', 'nan', 'NaN'}

def clean_name(name):
    """Limpia y normaliza un nombre de restaurante"""
    if pd.isna(name):
        return None
    name = str(name).strip()
    if name.lower() in [v.lower() for v in invalid_vals]:
        return None
    # Detectar emails
    if '@' in name or '.com' in name.lower() or '.mx' in name.lower():
        return None
    return name

def get_all_mentions(df, columns):
    """Extrae todas las menciones de una lista de columnas"""
    all_mentions = []
    for col in columns:
        if col in df.columns:
            vals = df[col].dropna().astype(str)
            for val in vals:
                cleaned = clean_name(val)
                if cleaned:
                    # Separar por comas, /, etc.
                    parts = re.split(r'\s*[,/;]\s*', cleaned)
                    for part in parts:
                        part = part.strip()
                        if part and part.lower() not in [v.lower() for v in invalid_vals]:
                            all_mentions.append(part)
    return all_mentions

print("\n" + "=" * 80)
print("ANÁLISIS POR CATEGORÍA")
print("=" * 80)

for cat_name, col_name in categoria_cols.items():
    if col_name in df.columns:
        mentions = get_all_mentions(df, [col_name])
        counter = Counter(mentions)
        
        print(f"\n{'='*60}")
        print(f"CATEGORÍA: {cat_name}")
        print(f"{'='*60}")
        print(f"Total menciones válidas: {len(mentions)}")
        print(f"Restaurantes únicos: {len(counter)}")
        print(f"\nTop 15:")
        for i, (name, count) in enumerate(counter.most_common(15), 1):
            print(f"  {i:2}. {name}: {count}")

print("\n" + "=" * 80)
print("ANÁLISIS DE RESTAURANTES GENERALES (Restaurante_1 a _5)")
print("=" * 80)

general_mentions = get_all_mentions(df, rest_cols)
general_counter = Counter(general_mentions)
print(f"Total menciones: {len(general_mentions)}")
print(f"Restaurantes únicos: {len(general_counter)}")
print(f"\nTop 20:")
for i, (name, count) in enumerate(general_counter.most_common(20), 1):
    print(f"  {i:2}. {name}: {count}")

print("\n" + "=" * 80)
print("BÚSQUEDA DE DUPLICIDADES POTENCIALES")
print("=" * 80)

# Recopilar TODOS los nombres de todas las columnas
all_names = []
all_cols = rest_cols + list(categoria_cols.values())
for col in all_cols:
    if col in df.columns:
        vals = df[col].dropna().astype(str)
        for val in vals:
            cleaned = clean_name(val)
            if cleaned:
                all_names.append(cleaned)

all_counter = Counter(all_names)

# Buscar variaciones similares
print("\nBuscando nombres similares que podrían ser el mismo restaurante...")

unique_names = list(all_counter.keys())
potential_duplicates = []

for i, name1 in enumerate(unique_names):
    for name2 in unique_names[i+1:]:
        n1_lower = name1.lower().replace(' ', '').replace("'", "").replace(".", "")
        n2_lower = name2.lower().replace(' ', '').replace("'", "").replace(".", "")
        
        # Si son muy similares
        if n1_lower == n2_lower:
            potential_duplicates.append((name1, all_counter[name1], name2, all_counter[name2]))
        elif n1_lower in n2_lower or n2_lower in n1_lower:
            if abs(len(n1_lower) - len(n2_lower)) <= 5:
                potential_duplicates.append((name1, all_counter[name1], name2, all_counter[name2]))

print(f"\nPosibles duplicados encontrados: {len(potential_duplicates)}")
for dup in sorted(potential_duplicates, key=lambda x: x[1]+x[3], reverse=True)[:50]:
    print(f"  '{dup[0]}' ({dup[1]}) <-> '{dup[2]}' ({dup[3]})")

print("\n" + "=" * 80)
print("BÚSQUEDA ESPECÍFICA: FUEGO EXTREMO")
print("=" * 80)

fuego_variants = []
for name in unique_names:
    if 'fuego' in name.lower():
        fuego_variants.append((name, all_counter[name]))

print("Variantes encontradas con 'fuego':")
for name, count in sorted(fuego_variants, key=lambda x: x[1], reverse=True):
    print(f"  '{name}': {count} menciones")

# Buscar en qué columnas específicas aparece
print("\nDesglose por columna:")
for col in all_cols:
    if col in df.columns:
        vals = df[col].dropna().astype(str)
        fuego_count = sum(1 for v in vals if 'fuego' in v.lower())
        if fuego_count > 0:
            print(f"  {col}: {fuego_count}")

print("\n" + "=" * 80)
print("TOP 30 RESTAURANTES GLOBALES (todas las columnas)")
print("=" * 80)

for i, (name, count) in enumerate(all_counter.most_common(30), 1):
    print(f"  {i:2}. {name}: {count}")

print("\n" + "=" * 80)
print("FIN DEL ANÁLISIS")
print("=" * 80)
