#!/usr/bin/env python3
"""
AUDITORÍA COMPLETA DE LA BASE DE DATOS - DASHBOARD VH26
=========================================================
Este script realiza una revisión exhaustiva de todos los datos
para garantizar la integridad y calidad de la información.
"""
import pandas as pd
from collections import Counter, defaultdict
import re
import sys
sys.path.insert(0, '.')

from app import normalize_restaurant_name, is_valid_restaurant_name

# Cargar datos
print("=" * 100)
print("AUDITORÍA COMPLETA DE LA BASE DE DATOS - DASHBOARD VH26")
print("=" * 100)

df = pd.read_csv('data_encuestas.csv')

print(f"\n📊 INFORMACIÓN GENERAL:")
print(f"   Total de encuestas: {len(df)}")
print(f"   Total de columnas: {len(df.columns)}")

# =============================================================================
# 1. ANÁLISIS DE ESTRUCTURA DE DATOS
# =============================================================================
print("\n" + "=" * 100)
print("1. ESTRUCTURA DE DATOS")
print("=" * 100)

print("\nColumnas encontradas:")
for i, col in enumerate(df.columns, 1):
    non_null = df[col].notna().sum()
    print(f"   {i:2}. {col}: {non_null} valores no nulos")

# =============================================================================
# 2. COLUMNAS DE RESTAURANTES - ANÁLISIS DETALLADO
# =============================================================================
print("\n" + "=" * 100)
print("2. ANÁLISIS DE COLUMNAS DE RESTAURANTES")
print("=" * 100)

# Definir todas las columnas que contienen nombres de restaurantes
restaurant_columns = [
    'Restaurante_1', 'Restaurante_2', 'Restaurante_3', 'Restaurante_4', 'Restaurante_5',
    'Mariscos', 'Carne', 'Hamburguesas', 'Pizzas', 'Sushi', 'Tacos',
    'Comida típica tabasqueña', 'Mexicana', 'Desayunos', 'Brunch', 
    'Bar', 'Bufete', 'Está de moda', 'Ya no está de moda:', 'Celebraciones'
]

# Contador global de todos los restaurantes
all_restaurants = Counter()
all_restaurants_raw = Counter()  # Sin normalizar
restaurants_by_column = {}

for col in restaurant_columns:
    if col not in df.columns:
        print(f"\n⚠️  COLUMNA NO ENCONTRADA: {col}")
        continue
    
    counter_raw = Counter()
    counter_normalized = Counter()
    invalid_entries = []
    
    for val in df[col].dropna():
        name = str(val).strip()
        if not name:
            continue
        
        counter_raw[name] += 1
        all_restaurants_raw[name] += 1
        
        if is_valid_restaurant_name(name):
            normalized = normalize_restaurant_name(name)
            counter_normalized[normalized] += 1
            all_restaurants[normalized] += 1
        else:
            invalid_entries.append(name)
    
    restaurants_by_column[col] = {
        'raw': counter_raw,
        'normalized': counter_normalized,
        'invalid': invalid_entries
    }
    
    print(f"\n📌 {col}:")
    print(f"   Total respuestas: {len(counter_raw)}")
    print(f"   Restaurantes únicos (sin normalizar): {len(counter_raw)}")
    print(f"   Restaurantes únicos (normalizados): {len(counter_normalized)}")
    
    if invalid_entries:
        print(f"   ⚠️  Entradas filtradas como inválidas: {len(invalid_entries)}")
        for inv in list(set(invalid_entries))[:5]:
            print(f"      - '{inv}'")

# =============================================================================
# 3. DETECCIÓN DE DUPLICIDADES POTENCIALES NO NORMALIZADAS
# =============================================================================
print("\n" + "=" * 100)
print("3. BÚSQUEDA DE DUPLICIDADES POTENCIALES NO DETECTADAS")
print("=" * 100)

def similarity_check(name1, name2):
    """Verifica si dos nombres son potencialmente el mismo restaurante."""
    n1 = name1.lower().strip()
    n2 = name2.lower().strip()
    
    # Eliminar artículos y preposiciones comunes
    articles = ['el ', 'la ', 'los ', 'las ', 'de ', 'del ']
    for art in articles:
        if n1.startswith(art):
            n1_clean = n1[len(art):]
        else:
            n1_clean = n1
        if n2.startswith(art):
            n2_clean = n2[len(art):]
        else:
            n2_clean = n2
    
    # Si uno contiene al otro
    if n1 in n2 or n2 in n1:
        return True
    
    # Si comparten las primeras 5 letras
    if len(n1) >= 5 and len(n2) >= 5 and n1[:5] == n2[:5]:
        return True
    
    return False

# Obtener lista única de restaurantes normalizados
unique_restaurants = list(all_restaurants.keys())
potential_duplicates = []

print("\nBuscando posibles duplicados no detectados...")
checked = set()
for i, r1 in enumerate(unique_restaurants):
    for r2 in unique_restaurants[i+1:]:
        if (r1, r2) in checked or (r2, r1) in checked:
            continue
        
        # Normalizar para comparar
        n1 = normalize_restaurant_name(r1)
        n2 = normalize_restaurant_name(r2)
        
        if n1 != n2 and similarity_check(r1, r2):
            count1 = all_restaurants[r1]
            count2 = all_restaurants[r2]
            if count1 >= 3 or count2 >= 3:  # Solo mostrar si tienen menciones significativas
                potential_duplicates.append((r1, count1, r2, count2))
        
        checked.add((r1, r2))

if potential_duplicates:
    print(f"\n⚠️  POSIBLES DUPLICADOS ENCONTRADOS ({len(potential_duplicates)}):")
    potential_duplicates.sort(key=lambda x: x[1] + x[3], reverse=True)
    for r1, c1, r2, c2 in potential_duplicates[:30]:
        print(f"   '{r1}' ({c1}) <-> '{r2}' ({c2})")
else:
    print("\n✅ No se encontraron duplicados potenciales significativos")

# =============================================================================
# 4. ANÁLISIS DE ENTRADAS SOSPECHOSAS
# =============================================================================
print("\n" + "=" * 100)
print("4. ENTRADAS SOSPECHOSAS O PROBLEMÁTICAS")
print("=" * 100)

suspicious = []
for name, count in all_restaurants_raw.most_common():
    name_lower = name.lower()
    
    # Verificar patrones sospechosos
    issues = []
    
    # Emails
    if '@' in name or '.com' in name_lower or '.mx' in name_lower:
        issues.append("EMAIL")
    
    # URLs
    if 'http' in name_lower or 'www.' in name_lower:
        issues.append("URL")
    
    # Números de teléfono
    if re.search(r'\d{7,}', name):
        issues.append("TELÉFONO")
    
    # Muy largo (más de 50 caracteres)
    if len(name) > 50:
        issues.append("MUY LARGO")
    
    # Solo números
    if re.match(r'^[\d\s\-\.]+$', name):
        issues.append("SOLO NÚMEROS")
    
    # Caracteres extraños
    if re.search(r'[<>{}[\]\\|]', name):
        issues.append("CARACTERES EXTRAÑOS")
    
    if issues:
        suspicious.append((name, count, issues))

if suspicious:
    print(f"\n⚠️  ENTRADAS SOSPECHOSAS ENCONTRADAS ({len(suspicious)}):")
    for name, count, issues in suspicious:
        print(f"   [{', '.join(issues)}] '{name[:60]}...' ({count} menciones)" if len(name) > 60 else f"   [{', '.join(issues)}] '{name}' ({count} menciones)")
else:
    print("\n✅ No se encontraron entradas sospechosas")

# =============================================================================
# 5. TOP 50 RESTAURANTES GLOBALES (VERIFICACIÓN)
# =============================================================================
print("\n" + "=" * 100)
print("5. TOP 50 RESTAURANTES GLOBALES (NORMALIZADOS)")
print("=" * 100)

print("\nRanking global de restaurantes:")
for i, (name, count) in enumerate(all_restaurants.most_common(50), 1):
    # Verificar si es un nombre real
    status = "✅" if count >= 5 else "⚠️"
    print(f"   {i:2}. {status} {name}: {count}")

# =============================================================================
# 6. VERIFICACIÓN DE CATEGORÍAS ESPECÍFICAS
# =============================================================================
print("\n" + "=" * 100)
print("6. TOP 10 POR CATEGORÍA (VERIFICACIÓN)")
print("=" * 100)

category_columns = [
    'Mariscos', 'Carne', 'Hamburguesas', 'Pizzas', 'Sushi', 'Tacos',
    'Comida típica tabasqueña', 'Mexicana', 'Desayunos', 'Brunch', 
    'Bar', 'Bufete', 'Está de moda', 'Ya no está de moda:', 'Celebraciones'
]

for col in category_columns:
    if col not in restaurants_by_column:
        continue
    
    data = restaurants_by_column[col]['normalized']
    print(f"\n📌 {col}:")
    for i, (name, count) in enumerate(data.most_common(10), 1):
        print(f"   {i:2}. {name}: {count}")

# =============================================================================
# 7. VERIFICACIÓN DE NOMBRES CON POCAS MENCIONES
# =============================================================================
print("\n" + "=" * 100)
print("7. RESTAURANTES CON 1-2 MENCIONES (posibles errores de captura)")
print("=" * 100)

low_mentions = [(name, count) for name, count in all_restaurants.items() if count <= 2 and count >= 1]
low_mentions.sort(key=lambda x: x[0])

print(f"\nTotal de restaurantes con 1-2 menciones: {len(low_mentions)}")
print("\nMuestra de nombres (primeros 50):")
for name, count in low_mentions[:50]:
    # Verificar si podría ser variación de otro
    could_be_variation = False
    for top_name, top_count in all_restaurants.most_common(100):
        if top_count > 10 and similarity_check(name, top_name) and name != top_name:
            print(f"   ⚠️  '{name}' ({count}) - ¿Variación de '{top_name}' ({top_count})?")
            could_be_variation = True
            break
    
    if not could_be_variation:
        print(f"   '{name}' ({count})")

# =============================================================================
# 8. RESUMEN EJECUTIVO
# =============================================================================
print("\n" + "=" * 100)
print("8. RESUMEN EJECUTIVO DE LA AUDITORÍA")
print("=" * 100)

total_mentions = sum(all_restaurants.values())
unique_normalized = len(all_restaurants)
unique_raw = len(all_restaurants_raw)

print(f"""
📊 ESTADÍSTICAS GENERALES:
   • Total de encuestas: {len(df)}
   • Total de menciones de restaurantes: {total_mentions}
   • Restaurantes únicos (sin normalizar): {unique_raw}
   • Restaurantes únicos (normalizados): {unique_normalized}
   • Reducción por normalización: {unique_raw - unique_normalized} ({((unique_raw - unique_normalized) / unique_raw * 100):.1f}%)

🔍 PROBLEMAS DETECTADOS:
   • Posibles duplicados no normalizados: {len(potential_duplicates)}
   • Entradas sospechosas: {len(suspicious)}
   • Restaurantes con 1-2 menciones: {len(low_mentions)}

📈 TOP 5 RESTAURANTES:
""")

for i, (name, count) in enumerate(all_restaurants.most_common(5), 1):
    pct = count / total_mentions * 100
    print(f"   {i}. {name}: {count} menciones ({pct:.1f}%)")

print("\n" + "=" * 100)
print("FIN DE LA AUDITORÍA")
print("=" * 100)
