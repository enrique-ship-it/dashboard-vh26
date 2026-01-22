import pandas as pd
import re
import unicodedata
from pathlib import Path

base = Path('/Users/enrique/Documents/Proyectos/Dashboard_VH26')
new_fp = base / 'data_encuestas_raw_nuevo.csv'
old_fp = base / 'data_encuestas.csv'
output_fp = base / 'data_encuestas_limpio_nuevo.csv'

old_cols = list(pd.read_csv(old_fp, nrows=0).columns)
new = pd.read_csv(new_fp)

# Detect columns by prefix to avoid encoding issues
col_q7 = next((c for c in new.columns if c.startswith('7. Menciona el primer restaurante')), None)
col_q71 = next((c for c in new.columns if c.startswith('7.1')), None)
col_id = 'Submission ID'

NO_RESP = {
    'no respondio', 'no responde', 'prefiero no responder'
}


def normalize_ascii(text: str) -> str:
    normalized = unicodedata.normalize('NFKD', text)
    return ''.join(ch for ch in normalized if not unicodedata.combining(ch))


def clean_text(val):
    if pd.isna(val):
        return val
    s = str(val)
    s = s.replace('\r', ' ').replace('\n', ', ')
    s = re.sub(r'\s+', ' ', s).strip()
    s_norm = normalize_ascii(s).lower().strip()
    if s_norm in NO_RESP:
        return 'No responde'
    return s


def split_rest_list(val):
    if pd.isna(val):
        return []
    s = clean_text(val)
    if not s:
        return []
    parts = re.split(r'[;,]', s)
    cleaned = []
    seen = set()
    for p in parts:
        item = re.sub(r'\s+', ' ', p).strip()
        if not item:
            continue
        key = normalize_ascii(item).lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(item)
    return cleaned


# Pre-clean string columns
for c in new.columns:
    if new[c].dtype == object:
        new[c] = new[c].map(clean_text)

# Build output with old schema
out = pd.DataFrame(columns=old_cols)

# ID
if 'ID' in out.columns and col_id in new.columns:
    out['ID'] = new[col_id]

# Copy matching columns
for c in old_cols:
    if c in new.columns:
        out[c] = new[c]

# Q7
if col_q7 and col_q7 in new.columns and col_q7 in out.columns:
    out[col_q7] = new[col_q7]

# Restaurante_1..5 from 7.1
rest_cols = [c for c in out.columns if c.startswith('Restaurante_')]
if col_q71 and rest_cols:
    rest_lists = new[col_q71].map(split_rest_list)
    for i, rc in enumerate(rest_cols):
        out[rc] = rest_lists.map(lambda lst: lst[i] if i < len(lst) else '')

# Fill NaN in text columns (except ID)
for c in out.columns:
    if c != 'ID' and out[c].dtype == object:
        out[c] = out[c].fillna('')

out.to_csv(output_fp, index=False)

print('guardado:', output_fp)
print('filas:', len(out), 'columnas:', out.shape[1])
