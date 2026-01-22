"""
CONSUMER INSIGHTS DASHBOARD - VH26
Dashboard interactivo para análisis del mercado gastronómico de Villahermosa
Desarrollado por NO ROBOT | Enero 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import base64
import random
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================
st.set_page_config(
    page_title="Consumer Insights Dashboard - VH26",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CARGAR FONDO COMO BASE64
# ============================================================================
def get_bg_image():
    bg_path = Path(__file__).parent / "assets" / "fondo1.png"
    if bg_path.exists():
        with open(bg_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

bg_base64 = get_bg_image()

# ============================================================================
# ESTILOS CSS - DISEÑO CLARO Y LIMPIO
# ============================================================================
# CSS base sin variables
CSS_STYLES = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(219, 39, 119, 0.1) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #4a4a4a !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {
        color: #6b7280 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(219, 39, 119, 0.12);
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 4px 24px rgba(219, 39, 119, 0.08);
        transition: all 0.3s ease;
        min-height: auto;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(219, 39, 119, 0.12);
        border-color: rgba(219, 39, 119, 0.2);
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(252,231,243,0.9) 100%);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(219, 39, 119, 0.15);
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(219, 39, 119, 0.08);
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .kpi-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(219, 39, 119, 0.15);
    }
    
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #db2777 0%, #9333ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .kpi-label {
        color: #6b7280;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 8px;
    }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1f2937 0%, #db2777 50%, #9333ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 4px;
    }
    
    .subtitle {
        color: #6b7280;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 32px;
        font-weight: 400;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        margin: 28px 0 16px 0;
        padding-left: 14px;
        border-left: 4px solid #db2777;
    }
    
    .alert-success {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(34, 197, 94, 0.05) 100%);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 16px;
        padding: 18px;
        color: #166534;
        margin: 10px 0;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, rgba(234, 179, 8, 0.1) 0%, rgba(234, 179, 8, 0.05) 100%);
        border: 1px solid rgba(234, 179, 8, 0.3);
        border-radius: 16px;
        padding: 18px;
        color: #854d0e;
        margin: 10px 0;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 16px;
        padding: 18px;
        color: #991b1b;
        margin: 10px 0;
    }
    
    .alert-info {
        background: linear-gradient(135deg, rgba(219, 39, 119, 0.08) 0%, rgba(147, 51, 234, 0.05) 100%);
        border: 1px solid rgba(219, 39, 119, 0.2);
        border-radius: 16px;
        padding: 18px;
        color: #4a4a4a;
        margin: 10px 0;
    }
    
    .quote-card {
        background: rgba(255, 255, 255, 0.9);
        border-left: 4px solid #db2777;
        border-radius: 0 16px 16px 0;
        padding: 18px 22px;
        margin: 14px 0;
        font-style: italic;
        color: #374151;
        box-shadow: 0 2px 12px rgba(219, 39, 119, 0.06);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }
    
    p, span, div {
        color: #4b5563;
    }
    
    .stButton > button {
        background: white;
        color: #db2777 !important;
        border: 1px solid rgba(219, 39, 119, 0.3);
        border-radius: 10px;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: 0 2px 6px rgba(219, 39, 119, 0.1);
    }
    
    .stButton > button:hover {
        background: #fce7f3;
        border-color: #db2777;
        box-shadow: 0 4px 12px rgba(219, 39, 119, 0.15);
    }
    
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(219, 39, 119, 0.2) !important;
        border-radius: 12px !important;
        cursor: pointer !important;
    }
    
    .stSelectbox input,
    .stMultiSelect input {
        cursor: pointer !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #fce7f3 0%, #f5d0fe 100%) !important;
        border: 1px solid rgba(219, 39, 119, 0.3) !important;
        color: #831843 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 14px;
        padding: 6px;
        gap: 8px;
        border: 1px solid rgba(219, 39, 119, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #6b7280;
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #db2777 !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(219, 39, 119, 0.15) !important;
        border: 1px solid rgba(219, 39, 119, 0.2) !important;
    }
    
    .stDataFrame {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(219, 39, 119, 0.1) !important;
    }
    
    [data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #db2777 0%, #9333ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Ocultar header pero mantener el botón del sidebar visible */
    [data-testid="stHeader"] {
        background: transparent !important;
        height: 2.5rem !important;
    }
    
    /* Estilizar el botón de colapsar/expandir sidebar */
    [data-testid="collapsedControl"] {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 0 12px 12px 0 !important;
        border: 1px solid rgba(219, 39, 119, 0.15) !important;
        box-shadow: 0 2px 8px rgba(219, 39, 119, 0.1) !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: rgba(255, 255, 255, 1) !important;
        border-color: rgba(219, 39, 119, 0.3) !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(219, 39, 119, 0.05);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(219, 39, 119, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(219, 39, 119, 0.5);
    }
    
    .logo-container {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(219, 39, 119, 0.15);
    }
    
    .logo-text {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1f2937 !important;
        letter-spacing: 2px;
    }
    
    .filter-indicator {
        background: linear-gradient(135deg, rgba(219, 39, 119, 0.1) 0%, rgba(147, 51, 234, 0.08) 100%);
        border: 1px solid rgba(219, 39, 119, 0.2);
        border-radius: 14px;
        padding: 14px 20px;
        margin-bottom: 20px;
        color: #4a4a4a;
    }
    
    .ranking-item {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(219, 39, 119, 0.1);
        border-radius: 14px;
        padding: 16px 20px;
        margin: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s ease;
    }
    
    .ranking-item:hover {
        background: rgba(255, 255, 255, 0.98);
        border-color: rgba(219, 39, 119, 0.25);
        transform: translateX(4px);
    }
    
    .trend-up {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.08) 0%, rgba(34, 197, 94, 0.03) 100%);
        border: 1px solid rgba(34, 197, 94, 0.2);
        border-radius: 12px;
        padding: 14px 18px;
        margin: 8px 0;
        color: #166534;
    }
    
    .trend-down {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(239, 68, 68, 0.03) 100%);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 12px;
        padding: 14px 18px;
        margin: 8px 0;
        color: #991b1b;
    }
    
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.7) !important;
        border-radius: 12px !important;
        color: #1f2937 !important;
    }
</style>
"""

st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Aplicar fondo si existe
if bg_base64:
    st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================================
@st.cache_data
def load_encuestas():
    """Carga datos de encuestas"""
    df = pd.read_csv('data_encuestas.csv', encoding='utf-8-sig')
    return df

@st.cache_data
def load_gmb():
    """Carga datos de Google My Business"""
    df = pd.read_excel('data_gmb.xlsx')
    return df

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================
def get_restaurant_mentions(df):
    """Obtiene conteo de menciones de restaurantes"""
    rest_cols = ['Restaurante_1', 'Restaurante_2', 'Restaurante_3', 'Restaurante_4', 'Restaurante_5']
    cat_cols = ['Mariscos', 'Carne', 'Hamburguesas', 'Pizzas', 'Sushi', 'Tacos', 
                'Comida típica tabasqueña', 'Mexicana', 'Desayunos', 'Brunch', 
                'Bar', 'Bufete', 'Está de moda', 'Ya no está de moda:', 'Celebraciones']
    
    all_mentions = []
    for col in rest_cols + cat_cols:
        if col in df.columns:
            vals = df[col].dropna().astype(str)
            vals = vals[~vals.isin(['1', 'No responde', 'No sé', 'Ninguno', 'No se'])]
            all_mentions.extend(vals.tolist())
    
    return Counter(all_mentions)

# Función para generar seed aleatorio para comentarios
def get_comment_seed():
    if 'comment_seed' not in st.session_state:
        st.session_state.comment_seed = 42
    return st.session_state.comment_seed

def refresh_comments():
    st.session_state.comment_seed = random.randint(1, 10000)

def normalize_restaurant_name(name):
    """Normaliza nombres de restaurantes para evitar duplicados"""
    if not isinstance(name, str):
        return name
    # Convertir a título (primera letra mayúscula)
    name = name.strip().title()
    # Eliminar artículos y conectores duplicados
    name = name.replace('  ', ' ')
    # Normalizar variaciones comunes
    replacements = {
        'Pescados Y Mariscos': 'Pescados y Mariscos',
        'El Reina': 'El Reyna',
        'La Lupita Mariscos': 'La Lupita',
    }
    for old, new in replacements.items():
        if old.lower() == name.lower():
            name = new
    return name

def get_category_leaders(df):
    """Obtiene líderes por categoría con normalización de nombres"""
    categories = {
        'Mariscos': 'Mariscos',
        'Carne': 'Carne',
        'Hamburguesas': 'Hamburguesas',
        'Pizzas': 'Pizzas',
        'Sushi': 'Sushi',
        'Tacos': 'Tacos',
        'Desayunos': 'Desayunos',
        'Bar': 'Bar',
        'Bufete': 'Bufete',
        'Celebraciones': 'Celebraciones',
        'De Moda': 'Está de moda',
        'En Declive': 'Ya no está de moda:'
    }
    
    leaders = {}
    for name, col in categories.items():
        if col in df.columns:
            vals = df[col].dropna().astype(str)
            vals = vals[~vals.isin(['1', 'No responde', 'No sé', 'Ninguno', 'No se'])]
            # Normalizar nombres para evitar duplicados
            vals = vals.apply(normalize_restaurant_name)
            if len(vals) > 0:
                counts = Counter(vals)
                if counts:
                    top = counts.most_common(5)
                    leaders[name] = top
    
    return leaders

def match_gmb(restaurant_name, gmb_df):
    """Busca coincidencia en GMB con matching inteligente"""
    if not restaurant_name or len(restaurant_name) < 2:
        return None
    
    name_lower = restaurant_name.lower().strip()
    
    # Mapeo directo de nombres de encuesta -> búsqueda en GMB
    direct_mappings = {
        '7 quince': '7:quince',
        '7quince': '7:quince',
        'siete quince': '7:quince',
        'bostons': "boston's",
        'boston': "boston's",
        'el reyna': 'el reyna',
        'la lupita': 'la lupita',
        'pescados y mariscos': 'pescados',
        'fuego extremo': 'fuego extremo',
        'a takear': 'a takear',
        'sushi house': 'sushi house',
        'sushi roll': 'sushi roll',
        'di bari': 'di bari',
        'roma norte': 'roma norte',
        'milagrito': 'milagrito',
        'maiña': 'maiña',
    }
    
    # Usar mapeo directo si existe
    search_term = direct_mappings.get(name_lower, name_lower)
    
    # Buscar por nombre exacto primero
    match = gmb_df[gmb_df['name'].str.lower().str.strip() == search_term]
    if len(match) > 0:
        return match.iloc[0]
    
    # Buscar por contiene
    match = gmb_df[gmb_df['name'].str.lower().str.contains(search_term, na=False, regex=False)]
    if len(match) > 0:
        return match.iloc[0]
    
    # Si no encontró con el mapeo, buscar con el nombre original
    if search_term != name_lower:
        match = gmb_df[gmb_df['name'].str.lower().str.contains(name_lower[:6], na=False, regex=False)]
        if len(match) > 0:
            return match.iloc[0]
    
    # Buscar por primera palabra
    first_word = name_lower.split()[0] if ' ' in name_lower else name_lower
    if len(first_word) >= 4:
        match = gmb_df[gmb_df['name'].str.lower().str.contains(first_word, na=False, regex=False)]
        if len(match) > 0:
            return match.iloc[0]
    
    return None

# ============================================================================
# CARGA DE DATOS
# ============================================================================
try:
    df_encuestas = load_encuestas()
    df_gmb = load_gmb()
    data_loaded = True
except Exception as e:
    st.error(f"Error cargando datos: {e}")
    data_loaded = False

if not data_loaded:
    st.stop()

# ============================================================================
# SIDEBAR - NAVEGACIÓN Y FILTROS
# ============================================================================
# Callback para limpiar filtros (evita el error de session_state)
def clear_filters():
    st.session_state.filter_edad = []
    st.session_state.filter_zona = []
    st.session_state.filter_gasto = []
    st.session_state.filter_freq = []

# Función para cargar imagen como base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

with st.sidebar:
    # Logo NO ROBOT
    logo_path = Path(__file__).parent / "assets" / "logo.png"
    if logo_path.exists():
        logo_base64 = get_image_base64(logo_path)
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 10px; margin-bottom: 20px; 
                    border-bottom: 1px solid rgba(219, 39, 119, 0.15);">
            <img src="data:image/png;base64,{logo_base64}" 
                 style="max-width: 180px; height: auto; margin-bottom: 8px;">
            <p style="color: #9ca3af; font-size: 0.75rem; margin: 0;">Consumer Insights</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="logo-container">
            <div class="logo-text">NO ROBOT</div>
            <p style="color: #9ca3af; font-size: 0.8rem; margin-top: 4px;">Consumer Insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navegación
    st.markdown("#### 🧭 Navegación")
    pages = [
        "📈 Resumen Ejecutivo",
        "👥 Perfil del Consumidor",
        "🏆 Rankings por Categoría",
        "🔬 Análisis Detallado",
        "✅ Validación GMB",
        "📊 Tendencias",
        "💬 Voz del Cliente",
        "📁 Explorar y Descargar"
    ]
    
    selected_page = st.selectbox(
        "Ir a",
        pages,
        key="nav_page",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Filtros Globales con Multi-Select
    st.markdown("#### 🎯 Filtros")
    st.caption("Puedes seleccionar varios valores por filtro")
    
    # Columnas de filtros
    col_edad = "2. ¿Qué edad tienes?"
    col_zona = "5. ¿En qué zona o colonia de Villahermosa vives actualmente?"
    col_gasto = "12. En promedio, ¿cuánto gastan en tu grupo por persona cuando comen en un restaurante?"
    col_freq = "3. ¿Con qué frecuencia acostumbras comer en restaurantes en Villahermosa?"
    
    # Filtro Edad - MULTISELECT
    if col_edad in df_encuestas.columns:
        edad_options = sorted([x for x in df_encuestas[col_edad].dropna().unique() if x != 'No responde'])
        filter_edad = st.multiselect(
            "📅 Rango de edad",
            edad_options,
            default=[],
            key="filter_edad",
            placeholder="Todos los rangos"
        )
    else:
        filter_edad = []
    
    # Filtro Zona - MULTISELECT
    if col_zona in df_encuestas.columns:
        zona_options = sorted([x for x in df_encuestas[col_zona].dropna().unique() if x != 'No responde'])
        filter_zona = st.multiselect(
            "📍 Zona",
            zona_options,
            default=[],
            key="filter_zona",
            placeholder="Todas las zonas"
        )
    else:
        filter_zona = []
    
    # Filtro Gasto - MULTISELECT (ordenado de menor a mayor)
    if col_gasto in df_encuestas.columns:
        # Orden lógico de gasto
        gasto_orden = ['Menos de $200', '$200 – $350', '$350 – $500', '$500 – $700', 'Más de $700']
        gasto_disponibles = [x for x in df_encuestas[col_gasto].dropna().unique() if x != 'No responde']
        # Mantener solo los que existen en el dataset, en el orden correcto
        gasto_options = [g for g in gasto_orden if g in gasto_disponibles]
        filter_gasto = st.multiselect(
            "💰 Nivel de gasto",
            gasto_options,
            default=[],
            key="filter_gasto",
            placeholder="Todos los niveles"
        )
    else:
        filter_gasto = []
    
    # Filtro Frecuencia - MULTISELECT (ordenado de mayor a menor frecuencia)
    if col_freq in df_encuestas.columns:
        # Orden lógico de frecuencia
        freq_orden = ['Varias veces por semana', '1 vez por semana', '2–3 veces al mes', '1 vez al mes', 'Casi nunca']
        freq_disponibles = [x for x in df_encuestas[col_freq].dropna().unique() if x != 'No responde']
        freq_options = [f for f in freq_orden if f in freq_disponibles]
        filter_freq = st.multiselect(
            "🔄 Frecuencia",
            freq_options,
            default=[],
            key="filter_freq",
            placeholder="Todas las frecuencias"
        )
    else:
        filter_freq = []
    
    # Botón Reset y contador
    st.markdown("<br>", unsafe_allow_html=True)
    
    active_filters = sum([
        len(filter_edad) > 0,
        len(filter_zona) > 0,
        len(filter_gasto) > 0,
        len(filter_freq) > 0
    ])
    
    # Estilos para botones del sidebar
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] > div:first-child button {
        height: 42px !important;
        min-height: 42px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔄 Limpiar", use_container_width=True, on_click=clear_filters)
    
    with col2:
        filter_color = "#db2777" if active_filters > 0 else "#9ca3af"
        filter_bg = "linear-gradient(135deg, #fce7f3, #f5d0fe)" if active_filters > 0 else "#f9fafb"
        st.markdown(f"""
        <div style="background: {filter_bg}; 
                    padding: 8px 12px; border-radius: 8px; text-align: center;
                    border: 1px solid rgba(219, 39, 119, 0.2); height: 42px;
                    display: flex; align-items: center; justify-content: center; gap: 4px;">
            <span style="color: {filter_color}; font-weight: 700; font-size: 1rem;">{active_filters}</span>
            <span style="color: #6b7280; font-size: 0.8rem;">filtros</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Info del dataset
    st.markdown("#### 📊 Sobre los datos")
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.7); padding: 14px; border-radius: 14px; 
                border: 1px solid rgba(219, 39, 119, 0.1);">
        <p style="color: #4b5563; margin: 6px 0; font-size: 0.85rem;">
            📋 <strong>{len(df_encuestas)}</strong> personas encuestadas
        </p>
        <p style="color: #4b5563; margin: 6px 0; font-size: 0.85rem;">
            🌐 <strong>{len(df_gmb):,}</strong> restaurantes mapeados
        </p>
        <p style="color: #4b5563; margin: 6px 0; font-size: 0.85rem;">
            ⭐ Rating promedio: <strong>{df_gmb['rating'].mean():.2f}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# APLICAR FILTROS (MULTI-SELECT)
# ============================================================================
df_filtered = df_encuestas.copy()

if filter_edad and col_edad in df_filtered.columns:
    df_filtered = df_filtered[df_filtered[col_edad].isin(filter_edad)]
if filter_zona and col_zona in df_filtered.columns:
    df_filtered = df_filtered[df_filtered[col_zona].isin(filter_zona)]
if filter_gasto and col_gasto in df_filtered.columns:
    df_filtered = df_filtered[df_filtered[col_gasto].isin(filter_gasto)]
if filter_freq and col_freq in df_filtered.columns:
    df_filtered = df_filtered[df_filtered[col_freq].isin(filter_freq)]

# ============================================================================
# HEADER PRINCIPAL
# ============================================================================
st.markdown("""
<div class="main-title">Consumer Insights Dashboard</div>
<div class="subtitle">Estudio del mercado gastronómico en Villahermosa · Enero 2026</div>
""", unsafe_allow_html=True)

# Indicador de filtros activos
if active_filters > 0:
    filter_texts = []
    if filter_edad:
        filter_texts.append(f"Edad: {len(filter_edad)} seleccionados" if len(filter_edad) > 1 else f"Edad: {filter_edad[0]}")
    if filter_zona:
        filter_texts.append(f"Zona: {len(filter_zona)} seleccionadas")
    if filter_gasto:
        filter_texts.append(f"Gasto: {len(filter_gasto)} seleccionados" if len(filter_gasto) > 1 else f"Gasto: {filter_gasto[0]}")
    if filter_freq:
        filter_texts.append(f"Frecuencia: {len(filter_freq)} seleccionados" if len(filter_freq) > 1 else f"Frecuencia: {filter_freq[0]}")
    
    st.markdown(f"""
    <div class="filter-indicator">
        <strong>Filtros aplicados:</strong> {' · '.join(filter_texts)}<br>
        <span style="font-size: 0.9rem;">Mostrando <strong>{len(df_filtered)}</strong> de {len(df_encuestas)} encuestados</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PÁGINA 1: RESUMEN EJECUTIVO
# ============================================================================
if selected_page == "📈 Resumen Ejecutivo":
    
    mentions = get_restaurant_mentions(df_filtered)
    top_restaurant = mentions.most_common(1)[0] if mentions else ("N/A", 0)
    leaders = get_category_leaders(df_filtered)
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{len(df_filtered)}</div>
            <div class="kpi-label">Personas encuestadas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{len(mentions)}</div>
            <div class="kpi-label">Restaurantes mencionados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{len(df_gmb):,}</div>
            <div class="kpi-label">Negocios en Google Maps</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{df_gmb['rating'].mean():.1f}⭐</div>
            <div class="kpi-label">Rating promedio del mercado</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dos columnas principales
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown('<div class="section-title">Los favoritos de Villahermosa</div>', unsafe_allow_html=True)
        st.caption("Restaurantes que más mencionan los comensales cuando se les pregunta por sus preferidos")
        
        top_10 = mentions.most_common(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=[x[0] for x in top_10][::-1],
            x=[x[1] for x in top_10][::-1],
            orientation='h',
            marker=dict(
                color=[x[1] for x in top_10][::-1],
                colorscale=[[0, '#f9a8d4'], [0.5, '#db2777'], [1, '#9333ea']],
            ),
            text=[x[1] for x in top_10][::-1],
            textposition='outside',
            textfont=dict(color='#374151', size=12, family='Plus Jakarta Sans')
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#374151', family='Plus Jakarta Sans'),
            height=420,
            margin=dict(l=20, r=80, t=20, b=20),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, tickfont=dict(size=13, color='#374151'))
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.markdown('<div class="section-title">Hallazgos principales</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="alert-success">
            <strong>🏆 El favorito de la ciudad</strong><br>
            <span style="font-size: 1.15rem; font-weight: 600;">{top_restaurant[0]}</span> lidera 
            las preferencias con <strong>{top_restaurant[1]}</strong> menciones. Los tabasqueños 
            lo asocian con celebraciones especiales y cortes de carne.
        </div>
        """, unsafe_allow_html=True)
        
        if 'De Moda' in leaders and leaders['De Moda']:
            moda_leader = leaders['De Moda'][0]
            st.markdown(f"""
            <div class="alert-info">
                <strong>📈 En boca de todos</strong><br>
                <span style="font-weight: 600;">{moda_leader[0]}</span> está ganando 
                popularidad rápidamente ({moda_leader[1]} menciones como "de moda"). 
                Vale la pena observar qué están haciendo bien.
            </div>
            """, unsafe_allow_html=True)
        
        if 'En Declive' in leaders and leaders['En Declive']:
            # Filtrar respuestas inválidas
            valid_decline = [(n, c) for n, c in leaders['En Declive'] if n.lower() not in ['no', 'ninguno', 'no sé', 'ns']]
            if valid_decline:
                decline_leader = valid_decline[0]
                st.markdown(f"""
                <div class="alert-danger">
                    <strong>⚠️ Atención: Percepción en declive</strong><br>
                    <span style="font-weight: 600;">{decline_leader[0]}</span> fue mencionado 
                    {decline_leader[1]} veces como restaurante que "ya no está de moda". 
                    Esto puede indicar fatiga de marca o necesidad de reinvención.
                </div>
                """, unsafe_allow_html=True)
        
        # Oportunidad de mercado DINÁMICA basada en filtros
        col_falta = "11. ¿Qué tipo de restaurante o experiencia consideras que hacen falta o están poco desarrollados en Villahermosa?"
        if col_falta in df_filtered.columns:
            falta_data = df_filtered[col_falta].dropna().astype(str)
            falta_data = falta_data[~falta_data.isin(['No responde', 'No sé', 'Ninguno', 'No'])]
            if len(falta_data) > 0:
                falta_counts = Counter(falta_data)
                top_falta = falta_counts.most_common(3)
                
                # Construir mensaje dinámico
                if len(top_falta) >= 2:
                    oportunidades = f"<strong>{top_falta[0][0]}</strong> ({top_falta[0][1]} menciones) y <strong>{top_falta[1][0]}</strong> ({top_falta[1][1]} menciones)"
                elif len(top_falta) == 1:
                    oportunidades = f"<strong>{top_falta[0][0]}</strong> ({top_falta[0][1]} menciones)"
                else:
                    oportunidades = "nuevas experiencias gastronómicas"
                
                # Contexto según filtros activos
                contexto = "Los encuestados"
                if filter_edad:
                    edades = ", ".join(filter_edad)
                    contexto = f"El segmento de <strong>{edades}</strong>"
                
                st.markdown(f"""
                <div class="alert-warning">
                    <strong>💡 Oportunidad de mercado</strong><br>
                    {contexto} señalan que hace falta {oportunidades} en la ciudad. 
                    Un nicho con potencial de crecimiento.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-warning">
                    <strong>💡 Oportunidad de mercado</strong><br>
                    Aplica filtros para descubrir qué oportunidades detecta cada segmento demográfico.
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Líderes por categoría
    st.markdown('<div class="section-title">¿Quién domina cada categoría?</div>', unsafe_allow_html=True)
    st.caption("El restaurante que más mencionan cuando preguntas por cada tipo de comida")
    
    cols = st.columns(4)
    category_data = {
        'Carne': ('🥩', 'Cortes y parrilla'),
        'Mariscos': ('🦐', 'Pescados y mariscos'),
        'Pizzas': ('🍕', 'Pizzerías'),
        'Sushi': ('🍣', 'Comida japonesa'),
        'Desayunos': ('🍳', 'Para el desayuno'),
        'Bar': ('🍹', 'Bares y cantinas'),
        'Hamburguesas': ('🍔', 'Hamburguesas'),
        'Celebraciones': ('🎂', 'Eventos especiales')
    }
    
    for i, (cat, (icon, desc)) in enumerate(category_data.items()):
        with cols[i % 4]:
            if cat in leaders and leaders[cat]:
                data = leaders[cat][0]
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; padding: 20px;">
                    <div style="font-size: 2.2rem;">{icon}</div>
                    <div style="color: #6b7280; font-size: 0.75rem; margin: 8px 0;">{desc}</div>
                    <div style="color: #1f2937; font-weight: 600; font-size: 1rem;">{data[0]}</div>
                    <div style="color: #db2777; font-size: 0.9rem; font-weight: 500;">{data[1]} menciones</div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# PÁGINA 2: PERFIL DEL CONSUMIDOR
# ============================================================================
elif selected_page == "👥 Perfil del Consumidor":
    
    st.markdown('<div class="section-title">¿Quiénes participaron en el estudio?</div>', unsafe_allow_html=True)
    st.caption("Conoce el perfil de las personas que nos compartieron sus preferencias gastronómicas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if col_edad in df_filtered.columns:
            edad_counts = df_filtered[col_edad].value_counts()
            edad_counts = edad_counts[edad_counts.index != 'No responde']
            
            fig = px.pie(
                values=edad_counts.values,
                names=edad_counts.index,
                color_discrete_sequence=['#fce7f3', '#f9a8d4', '#f472b6', '#db2777', '#9333ea']
            )
            fig.update_layout(
                title=dict(text="Distribución por edad", font=dict(color='#1f2937', size=16)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#374151', family='Plus Jakarta Sans'),
                legend=dict(font=dict(color='#374151'))
            )
            fig.update_traces(textfont=dict(color='#374151'))
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if col_gasto in df_filtered.columns:
            gasto_counts = df_filtered[col_gasto].value_counts()
            gasto_counts = gasto_counts[gasto_counts.index != 'No responde']
            
            fig = px.pie(
                values=gasto_counts.values,
                names=gasto_counts.index,
                color_discrete_sequence=['#fae8ff', '#e9d5ff', '#c084fc', '#a855f7', '#7c3aed']
            )
            fig.update_layout(
                title=dict(text="¿Cuánto gastan por persona?", font=dict(color='#1f2937', size=16)),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#374151', family='Plus Jakarta Sans'),
                legend=dict(font=dict(color='#374151'))
            )
            fig.update_traces(textfont=dict(color='#374151'))
            st.plotly_chart(fig, use_container_width=True)
    
    # Matriz cruzada
    st.markdown('<div class="section-title">¿Cómo se relaciona la edad con el gasto?</div>', unsafe_allow_html=True)
    st.caption("Este mapa de calor muestra cuántas personas de cada grupo de edad gastan en cada rango de precios")
    
    if col_edad in df_filtered.columns and col_gasto in df_filtered.columns:
        cross_tab = pd.crosstab(df_filtered[col_edad], df_filtered[col_gasto])
        cross_tab = cross_tab.drop('No responde', errors='ignore')
        cross_tab = cross_tab.drop('No responde', axis=1, errors='ignore')
        
        fig = px.imshow(
            cross_tab,
            color_continuous_scale=['#fdf2f8', '#fce7f3', '#f9a8d4', '#db2777', '#9333ea'],
            aspect='auto',
            text_auto=True
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#374151', family='Plus Jakarta Sans'),
            height=400,
            xaxis_title="Gasto por persona",
            yaxis_title="Rango de edad"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top zonas
    st.markdown('<div class="section-title">¿De dónde vienen los encuestados?</div>', unsafe_allow_html=True)
    st.caption("Las colonias y zonas con mayor participación en el estudio")
    
    if col_zona in df_filtered.columns:
        zona_counts = df_filtered[col_zona].value_counts().head(10)
        zona_counts = zona_counts[zona_counts.index != 'No responde']
        
        fig = px.bar(
            x=zona_counts.values,
            y=zona_counts.index,
            orientation='h',
            color=zona_counts.values,
            color_continuous_scale=['#fce7f3', '#db2777', '#9333ea']
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#374151', family='Plus Jakarta Sans'),
            showlegend=False,
            height=400,
            xaxis_title="Número de encuestados",
            yaxis_title="",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PÁGINA 3: RANKINGS POR CATEGORÍA
# ============================================================================
elif selected_page == "🏆 Rankings por Categoría":
    
    st.markdown('<div class="section-title">Los preferidos según los tabasqueños</div>', unsafe_allow_html=True)
    st.caption("Elige una categoría para conocer cuáles restaurantes destacan en las preferencias")
    
    if len(df_filtered) == 0:
        st.error("⚠️ No hay datos con los filtros seleccionados. Por favor, ajusta los filtros en el panel lateral.")
    else:
        leaders = get_category_leaders(df_filtered)
        
        tabs = st.tabs(list(leaders.keys()))
        
        for i, (cat, data) in enumerate(leaders.items()):
            with tabs[i]:
                if data:
                    st.markdown(f"### Top 5 en {cat}")
                    
                    # Filtrar valores inválidos como "No", "No sé", etc.
                    valid_data = [(name, count) for name, count in data if name and len(name) > 2 and name.lower() not in ['no', 'no sé', 'ninguno', 'ns', 'n/a']]
                    
                    if not valid_data:
                        st.warning(f"🔍 No hay suficientes datos para mostrar el ranking de {cat} con los filtros actuales. Prueba ampliando tu selección.")
                        continue
                    
                    # Determinar cuántas columnas mostrar (máx 3)
                    top_count = min(3, len(valid_data))
                    cols = st.columns(top_count)
                    medals = ['🥇', '🥈', '🥉']
                    
                    for j, (name, count) in enumerate(valid_data[:top_count]):
                        with cols[j]:
                            gmb_match = match_gmb(name, df_gmb)
                            rating_text = f"⭐ {gmb_match['rating']}" if gmb_match is not None else "Sin datos GMB"
                            reviews_text = f"{int(gmb_match['reviews']):,} reseñas" if gmb_match is not None else ""
                            
                            st.markdown(f"""
                            <div class="glass-card" style="text-align: center;">
                                <div style="font-size: 3rem;">{medals[j]}</div>
                                <div style="font-size: 1.2rem; font-weight: 600; color: #1f2937; margin: 12px 0;">
                                    {name}
                                </div>
                                <div style="color: #db2777; font-size: 1.4rem; font-weight: 700;">
                                    {count} menciones
                                </div>
                                <div style="color: #6b7280; margin-top: 12px; font-size: 0.85rem;">
                                    {rating_text}<br>{reviews_text}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Mostrar posiciones 4 y 5 si existen
                    remaining = valid_data[3:5]
                    if remaining:
                        st.markdown("<br>", unsafe_allow_html=True)
                        remaining_cols = st.columns(len(remaining))
                        for j, (name, count) in enumerate(remaining):
                            with remaining_cols[j]:
                                st.markdown(f"""
                                <div class="ranking-item">
                                    <span style="color: #1f2937; font-weight: 500;">#{j+4} {name}</span>
                                    <span style="color: #db2777; font-weight: 600;">{count} menciones</span>
                                </div>
                                """, unsafe_allow_html=True)

# ============================================================================
# PÁGINA 4: ANÁLISIS DETALLADO
# ============================================================================
elif selected_page == "🔬 Análisis Detallado":
    
    st.markdown('<div class="section-title">Análisis por tipo de cocina</div>', unsafe_allow_html=True)
    st.caption("Explora cada categoría para entender las preferencias de los consumidores")
    
    categories = ['Mariscos', 'Carne', 'Hamburguesas', 'Pizzas', 'Sushi', 'Tacos', 
                  'Desayunos', 'Bar', 'Bufete', 'Celebraciones']
    
    # Usar tabs en lugar de selectbox para mejor navegación
    tabs = st.tabs(categories)
    
    for idx, selected_cat in enumerate(categories):
        with tabs[idx]:
            if selected_cat in df_filtered.columns:
                vals = df_filtered[selected_cat].dropna().astype(str)
                vals = vals[~vals.isin(['1', 'No responde', 'No sé', 'Ninguno', 'No se', 'No'])]
                # Normalizar nombres
                vals = vals.apply(normalize_restaurant_name)
                counts = Counter(vals)
                
                if not counts:
                    st.info(f"No hay suficientes datos para {selected_cat}")
                    continue
                
                # KPIs arriba
                col_k1, col_k2, col_k3, col_k4 = st.columns(4)
                
                top_10 = counts.most_common(10)
                leader = top_10[0] if top_10 else ("N/A", 0)
                second = top_10[1] if len(top_10) > 1 else ("N/A", 0)
                
                with col_k1:
                    st.metric("Total menciones", f"{sum(counts.values())}")
                with col_k2:
                    st.metric("Restaurantes únicos", f"{len(counts)}")
                with col_k3:
                    st.metric("🏆 Líder", leader[0])
                with col_k4:
                    ventaja = leader[1] - second[1] if second[1] > 0 else leader[1]
                    st.metric("Ventaja sobre #2", f"+{ventaja}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Gráfica de barras
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=[x[0] for x in top_10],
                    y=[x[1] for x in top_10],
                    marker=dict(
                        color=[x[1] for x in top_10],
                        colorscale=[[0, '#fce7f3'], [0.5, '#db2777'], [1, '#9333ea']],
                    ),
                    text=[x[1] for x in top_10],
                    textposition='outside',
                    textfont=dict(color='#374151', family='Plus Jakarta Sans')
                ))
                
                fig.update_layout(
                    title=dict(text=f"Top 10 en {selected_cat}", 
                              font=dict(color='#1f2937', size=16)),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#374151', family='Plus Jakarta Sans'),
                    height=400,
                    xaxis=dict(showgrid=False, tickangle=45),
                    yaxis=dict(showgrid=True, gridcolor='rgba(219, 39, 119, 0.1)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabla con datos GMB
                st.markdown("#### 📍 Validación con Google Maps")
                
                table_data = []
                for name, count in top_10:
                    gmb_match = match_gmb(name, df_gmb)
                    if gmb_match is not None:
                        table_data.append({
                            "Restaurante": name,
                            "Menciones": count,
                            "Rating GMB": f"⭐ {gmb_match['rating']}",
                            "Reseñas": f"{int(gmb_match['reviews']):,}"
                        })
                    else:
                        table_data.append({
                            "Restaurante": name,
                            "Menciones": count,
                            "Rating GMB": "—",
                            "Reseñas": "—"
                        })
                
                if table_data:
                    st.dataframe(
                        pd.DataFrame(table_data),
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.warning(f"No se encontró la columna {selected_cat} en los datos")

# ============================================================================
# PÁGINA 5: VALIDACIÓN GMB
# ============================================================================
elif selected_page == "✅ Validación GMB":
    
    st.markdown('<div class="section-title">¿Coincide lo que dicen con lo que califica Google?</div>', unsafe_allow_html=True)
    st.caption("Cruzamos los favoritos de las encuestas con sus calificaciones en Google Maps")
    
    mentions = get_restaurant_mentions(df_filtered)
    top_20 = mentions.most_common(20)
    
    validation_data = []
    for name, count in top_20:
        gmb_match = match_gmb(name, df_gmb)
        if gmb_match is not None:
            rating = gmb_match['rating']
            reviews = int(gmb_match['reviews'])
            
            if rating >= 4.5 and reviews >= 500:
                status = '✅ Validado'
            elif rating >= 4.0:
                status = '✅ OK'
            elif reviews < 200:
                status = '⚠️ Pocas reseñas'
            else:
                status = '⚠️ Revisar'
        else:
            rating = None
            reviews = None
            status = '❌ Sin datos'
        
        validation_data.append({
            'Restaurante': name,
            'Menciones': count,
            'Rating GMB': rating,
            'Reseñas': reviews,
            'Estado': status
        })
    
    df_validation = pd.DataFrame(validation_data)
    
    col1, col2, col3 = st.columns(3)
    
    validated = len([x for x in validation_data if '✅' in x['Estado']])
    warning = len([x for x in validation_data if '⚠️' in x['Estado']])
    no_data = len([x for x in validation_data if '❌' in x['Estado']])
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card" style="background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.05)); border-color: rgba(34,197,94,0.2);">
            <div class="kpi-value" style="-webkit-text-fill-color: #166534;">{validated}</div>
            <div class="kpi-label">Confirmados por Google</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="background: linear-gradient(135deg, rgba(234,179,8,0.1), rgba(234,179,8,0.05)); border-color: rgba(234,179,8,0.2);">
            <div class="kpi-value" style="-webkit-text-fill-color: #854d0e;">{warning}</div>
            <div class="kpi-label">Para revisar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.05)); border-color: rgba(239,68,68,0.2);">
            <div class="kpi-value" style="-webkit-text-fill-color: #991b1b;">{no_data}</div>
            <div class="kpi-label">Sin información</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.dataframe(
        df_validation,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Menciones': st.column_config.ProgressColumn(
                "Menciones",
                min_value=0,
                max_value=max([x[1] for x in top_20]),
                format="%d"
            ),
            'Rating GMB': st.column_config.NumberColumn(
                "Rating",
                format="⭐ %.1f"
            ),
            'Reseñas': st.column_config.NumberColumn(
                "Reseñas GMB",
                format="%d"
            )
        }
    )
    
    st.markdown('<div class="section-title">¿Qué nos dice esta comparación?</div>', unsafe_allow_html=True)
    
    # Análisis automático de los datos
    validated_items = [item for item in validation_data if item['Estado'] == '✅ Validado']
    ok_items = [item for item in validation_data if item['Estado'] == '✅ OK']
    warning_items = [item for item in validation_data if '⚠️' in item['Estado']]
    
    # Líder del mercado
    if validation_data:
        leader = validation_data[0]
        col_i1, col_i2 = st.columns(2)
        
        with col_i1:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #22c55e;">
                <h4 style="color: #166534; margin-bottom: 12px;">🏆 Líder indiscutible</h4>
                <p style="color: #4b5563; margin: 0;">
                    <strong>{leader['Restaurante']}</strong> domina con <strong>{leader['Menciones']} menciones</strong>. 
                    {f"Google lo respalda con ⭐{leader['Rating GMB']} y {leader['Reseñas']:,} reseñas." if leader['Rating GMB'] else ""}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_i2:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #3b82f6;">
                <h4 style="color: #1d4ed8; margin-bottom: 12px;">📊 Resumen de validación</h4>
                <p style="color: #4b5563; margin: 0;">
                    <strong>{len(validated_items) + len(ok_items)}</strong> de los 20 más mencionados tienen buenas 
                    calificaciones en Google. Esto significa que <strong>la percepción local coincide con la realidad</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Alertas si hay restaurantes con problemas
    if warning_items:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #f59e0b; margin-top: 12px;">
            <h4 style="color: #b45309; margin-bottom: 12px;">⚠️ Puntos de atención</h4>
            <p style="color: #4b5563; margin: 0;">
                {len(warning_items)} restaurante(s) popular(es) tienen calificaciones bajas o pocas reseñas: 
                <strong>{', '.join([item['Restaurante'] for item in warning_items[:3]])}</strong>. 
                Esto podría indicar una desconexión entre popularidad local y experiencia general.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Hidden gems
    hidden_gems = [item for item in validation_data if item['Rating GMB'] and item['Rating GMB'] >= 4.5 and item['Reseñas'] and item['Reseñas'] >= 1000 and item['Menciones'] < 50]
    if hidden_gems:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #8b5cf6; margin-top: 12px;">
            <h4 style="color: #6d28d9; margin-bottom: 12px;">💎 Joyas escondidas</h4>
            <p style="color: #4b5563; margin: 0;">
                <strong>{hidden_gems[0]['Restaurante']}</strong> tiene excelentes calificaciones en Google 
                (⭐{hidden_gems[0]['Rating GMB']}, {hidden_gems[0]['Reseñas']:,} reseñas) pero solo {hidden_gems[0]['Menciones']} 
                menciones locales. Oportunidad de marketing: ¿por qué no está en el radar del consumidor tabasqueño?
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PÁGINA 6: TENDENCIAS
# ============================================================================
elif selected_page == "📊 Tendencias":
    
    st.markdown('<div class="section-title">¿Quién sube y quién baja?</div>', unsafe_allow_html=True)
    st.caption("Identificamos qué restaurantes están ganando relevancia y cuáles la están perdiendo según la percepción del consumidor")
    
    col_moda = 'Está de moda'
    col_decline = 'Ya no está de moda:'
    
    moda_data = []
    decline_data = []
    
    if col_moda in df_filtered.columns:
        vals = df_filtered[col_moda].dropna().astype(str)
        vals = vals[~vals.isin(['1', 'No responde', 'No sé', 'Ninguno', 'No se'])]
        moda_data = Counter(vals).most_common(10)
    
    if col_decline in df_filtered.columns:
        vals = df_filtered[col_decline].dropna().astype(str)
        vals = vals[~vals.isin(['1', 'No responde', 'No sé', 'Ninguno', 'No se'])]
        decline_data = Counter(vals).most_common(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #22c55e;">
            <h3 style="color: #166534; margin: 0;">🚀 Ganando popularidad</h3>
            <p style="color: #6b7280; font-size: 0.85rem; margin-top: 4px;">Los que la gente percibe "de moda"</p>
        </div>
        """, unsafe_allow_html=True)
        
        for name, count in moda_data:
            st.markdown(f"""
            <div class="trend-up">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 500;">{name}</span>
                    <span style="font-weight: 700;">{count} 📈</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="border-left: 4px solid #ef4444;">
            <h3 style="color: #991b1b; margin: 0;">📉 Perdiendo terreno</h3>
            <p style="color: #6b7280; font-size: 0.85rem; margin-top: 4px;">Los que se perciben como "ya pasaron de moda"</p>
        </div>
        """, unsafe_allow_html=True)
        
        for name, count in decline_data:
            st.markdown(f"""
            <div class="trend-down">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 500;">{name}</span>
                    <span style="font-weight: 700;">{count} 📉</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">Índice de momentum</div>', unsafe_allow_html=True)
    st.caption("Cuando el ratio es mayor a 1, significa que más gente lo considera de moda que fuera de moda")
    
    all_restaurants = set([x[0] for x in moda_data] + [x[0] for x in decline_data])
    moda_dict = dict(moda_data)
    decline_dict = dict(decline_data)
    
    ratio_data = []
    for rest in all_restaurants:
        moda = moda_dict.get(rest, 0)
        decline = decline_dict.get(rest, 0)
        ratio = moda / max(decline, 1)
        
        if ratio > 2:
            status = '🚀 Muy bien posicionado'
        elif ratio > 1:
            status = '✅ En buena forma'
        elif ratio > 0.5:
            status = '⚠️ Cuidado'
        else:
            status = '🔴 Requiere atención'
        
        ratio_data.append({
            'Restaurante': rest,
            '"De moda"': moda,
            '"Ya no"': decline,
            'Ratio': round(ratio, 2),
            'Diagnóstico': status
        })
    
    df_ratio = pd.DataFrame(ratio_data).sort_values('Ratio', ascending=False)
    
    st.dataframe(
        df_ratio,
        use_container_width=True,
        hide_index=True
    )

# ============================================================================
# PÁGINA 7: VOZ DEL CLIENTE
# ============================================================================
elif selected_page == "💬 Voz del Cliente":
    
    st.markdown('<div class="section-title">Escuchando a los comensales</div>', unsafe_allow_html=True)
    st.caption("Insights directos de las encuestas y los focus groups")
    
    # Usar radio buttons con key para mantener estado entre reruns
    tab_options = ["🎯 Oportunidades", "💭 Lo que dicen", "😤 Lo que les molesta"]
    selected_tab = st.radio(
        "Sección",
        tab_options,
        horizontal=True,
        key="voz_cliente_tab",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if selected_tab == "🎯 Oportunidades":
        st.markdown("### ¿Qué tipo de restaurante hace falta en la ciudad?")
        st.caption("Analizamos las respuestas abiertas para encontrar necesidades no cubiertas")
        
        col_falta = "11. ¿Qué tipo de restaurante o experiencia consideras que hacen falta o están poco desarrollados en Villahermosa?"
        
        if col_falta in df_filtered.columns:
            resp = df_filtered[col_falta].dropna()
            resp = resp[~resp.isin(['1', 'No responde', 'No sé', 'Ninguno', 'ninguno', 'no', 'No', 'Nada'])]
            
            if len(resp) == 0:
                st.warning("🔍 No hay respuestas disponibles con los filtros seleccionados. Prueba ampliando tu selección.")
            else:
                categorias = {
                    '🥢 Comida asiática auténtica': ['asiatic', 'chino', 'china', 'japonés', 'japonesa', 'coreano', 'thai', 'ramen'],
                    '🍝 Cocina italiana de calidad': ['italian', 'pasta', 'pizza gourmet'],
                    '🍽️ Buffets con buen precio': ['buffet', 'buffete'],
                    '🎭 Experiencias temáticas': ['experiencia', 'diversión', 'entretenimiento', 'show', 'temático'],
                    '🏙️ Rooftops y terrazas': ['roof', 'rooftop', 'terraza', 'azotea'],
                    '🥗 Comida saludable': ['vegano', 'vegana', 'vegetarian', 'saludable', 'fit'],
                    '☕ Cafés y brunch': ['brunch', 'café', 'cafetería', 'desayuno'],
                    '🌍 Cocina internacional diversa': ['griega', 'libanés', 'árabe', 'turco', 'mediterráneo', 'francesa'],
                }
                
                results = Counter()
                otros_count = 0
                for r in resp:
                    r_lower = str(r).lower()
                    matched = False
                    for cat, keywords in categorias.items():
                        if any(kw in r_lower for kw in keywords):
                            results[cat] += 1
                            matched = True
                            break
                    if not matched:
                        otros_count += 1
                
                # Mostrar resultados categorizados
                for cat, count in results.most_common(8):
                    pct = count / len(resp) * 100
                    st.markdown(f"""
                    <div class="ranking-item">
                        <span style="font-size: 1.05rem;">{cat}</span>
                        <div style="text-align: right;">
                            <span style="color: #db2777; font-weight: 700; font-size: 1.1rem;">{count}</span>
                            <span style="color: #6b7280; font-size: 0.85rem;"> menciones ({pct:.1f}%)</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Mostrar categoría "Otros" si hay respuestas sin categorizar
                if otros_count > 0:
                    pct_otros = otros_count / len(resp) * 100
                    st.markdown(f"""
                    <div class="ranking-item" style="opacity: 0.7;">
                        <span style="font-size: 1.05rem;">📝 Otras menciones</span>
                        <div style="text-align: right;">
                            <span style="color: #6b7280; font-weight: 700; font-size: 1.1rem;">{otros_count}</span>
                            <span style="color: #6b7280; font-size: 0.85rem;"> respuestas ({pct_otros:.1f}%)</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif selected_tab == "💭 Lo que dicen":
        st.markdown("### Voces reales de consumidores")
        st.caption("Comentarios textuales de los encuestados en Villahermosa")
        
        # Obtener comentarios dinámicamente desde df_filtered
        col_comentarios = "Comentarios adicionales:"
        col_edad = "2. ¿Qué edad tienes?"
        
        # Filtrar comentarios válidos
        invalid_responses = ["no responde", "ninguno", "no", "x", ".", "-", "1", "na", "n/a", "nada", "ninguna"]
        
        df_comments = df_filtered[[col_comentarios, col_edad]].copy()
        df_comments = df_comments.dropna(subset=[col_comentarios])
        df_comments[col_comentarios] = df_comments[col_comentarios].astype(str)
        df_comments = df_comments[~df_comments[col_comentarios].str.lower().str.strip().isin(invalid_responses)]
        df_comments = df_comments[df_comments[col_comentarios].str.len() > 25]
        
        if len(df_comments) > 0:
            # Botón para ver otros comentarios
            col_btn, col_info = st.columns([1, 3])
            with col_btn:
                st.button("🔄 Ver otros", on_click=refresh_comments, use_container_width=True)
            with col_info:
                st.caption(f"Mostrando {min(6, len(df_comments))} de {len(df_comments)} comentarios disponibles")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Mostrar hasta 6 comentarios aleatorios con seed dinámico
            sample_size = min(6, len(df_comments))
            sampled = df_comments.sample(n=sample_size, random_state=get_comment_seed())
            
            for _, row in sampled.iterrows():
                comment = row[col_comentarios]
                edad = row[col_edad] if pd.notna(row[col_edad]) else "Encuestado"
                st.markdown(f"""
                <div class="quote-card">
                    <p style="margin: 0; font-size: 1rem; line-height: 1.6;">"{comment}"</p>
                    <p style="margin: 10px 0 0 0; color: #9ca3af; font-size: 0.85rem; font-style: normal;">— {edad}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Si no hay comentarios, mostrar mensaje personalizado
            st.warning("🔍 No hay comentarios disponibles con los filtros actuales. Prueba seleccionando otros rangos de edad o zonas.")
            
            # Mostrar citas predeterminadas como respaldo
            st.markdown("##### Insights generales del estudio:")
            default_quotes = [
                ("La atención al cliente es lo que más valoran los tabasqueños", "Insight del estudio"),
                ("El precio debe justificarse con calidad y experiencia", "Insight del estudio"),
                ("Los tiempos de espera son un factor crítico de satisfacción", "Insight del estudio"),
            ]
            for quote, source in default_quotes:
                st.markdown(f"""
                <div class="quote-card" style="opacity: 0.8;">
                    <p style="margin: 0; font-size: 0.95rem; line-height: 1.5;">{quote}</p>
                    <p style="margin: 8px 0 0 0; color: #9ca3af; font-size: 0.8rem;">— {source}</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif selected_tab == "😤 Lo que les molesta":
        st.markdown("### ¿Por qué no regresan?")
        st.caption("Los problemas que más mencionan y que afectan su decisión de volver")
        
        # Calcular pain points dinámicamente desde los datos filtrados
        col_no_regresar = "15. ¿Qué factores te harían NO regresar a un restaurante?."
        
        # Mapeo de categorías a emojis y descripciones
        pain_map = {
            "Comida de mala calidad / mal sabor": ("🍽️ Comida de mala calidad", "El sabor o la presentación no convencen", "#ef4444"),
            "Precio alto injustificado": ("💸 Precios no justificados", "Lo que cobran no vale lo que dan", "#f97316"),
            "Mucho tiempo de espera": ("⏱️ Tiempos de espera largos", "Esperan demasiado sin explicación", "#eab308"),
            "Mala atención y servicio": ("😤 Servicio deficiente", "Personal poco atento o grosero", "#f97316"),
            "Mal ambiente / volumen alto": ("🔊 Ambiente incómodo", "Ruido excesivo o atmósfera desagradable", "#8b5cf6"),
            "Mala reputación o reseñas": ("⭐ Mala reputación", "Comentarios negativos de otros clientes", "#6b7280"),
        }
        
        # Contar menciones (separadas por coma)
        pain_counter = Counter()
        for resp in df_filtered[col_no_regresar].dropna():
            for item in str(resp).split(","):
                item = item.strip()
                if item and item != "No responde":
                    # Normalizar nombres
                    for key in pain_map.keys():
                        if key.lower() in item.lower() or item.lower() in key.lower():
                            pain_counter[key] += 1
                            break
        
        total_mentions = sum(pain_counter.values())
        
        if total_mentions > 0:
            # Ordenar por frecuencia
            sorted_pains = pain_counter.most_common(6)
            
            for pain_key, count in sorted_pains:
                if pain_key in pain_map:
                    title, desc, color = pain_map[pain_key]
                    pct = round(count / total_mentions * 100)
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 4px solid {color}; padding: 18px 22px; min-height: auto;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <h4 style="color: #1f2937; margin: 0 0 6px 0;">{title}</h4>
                                <p style="color: #6b7280; margin: 0; font-size: 0.9rem;">{desc}</p>
                            </div>
                            <div style="text-align: right;">
                                <div style="color: {color}; font-size: 1.6rem; font-weight: 700;">{pct}%</div>
                                <div style="color: #9ca3af; font-size: 0.75rem;">de las quejas</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("🔍 No hay datos suficientes sobre quejas con los filtros seleccionados. Prueba ampliando tu selección de edad o zona.")

# ============================================================================
# PÁGINA 8: EXPLORAR Y DESCARGAR
# ============================================================================
elif selected_page == "📁 Explorar y Descargar":
    
    st.markdown('<div class="section-title">Accede a los datos del estudio</div>', unsafe_allow_html=True)
    st.caption("Explora las bases de datos y descarga lo que necesites")
    
    tabs = st.tabs(["🔍 Explorar", "📥 Descargar"])
    
    with tabs[0]:
        dataset_option = st.selectbox(
            "¿Qué datos quieres ver?",
            ["Encuestas (con filtros aplicados)", "Encuestas (base completa)", "Restaurantes Google Maps"]
        )
        
        if "filtros" in dataset_option:
            df_display = df_filtered
            st.info(f"Mostrando {len(df_display)} registros según tus filtros actuales")
        elif "completa" in dataset_option:
            df_display = df_encuestas
        else:
            df_display = df_gmb
        
        search = st.text_input("🔍 Buscar en los datos", placeholder="Escribe algo para filtrar...")
        
        if search:
            mask = df_display.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
            df_display = df_display[mask]
        
        st.dataframe(df_display, use_container_width=True, height=500)
    
    with tabs[1]:
        st.markdown("### Archivos disponibles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #1f2937;">📋 Encuestas completas</h4>
                <p style="color: #6b7280; font-size: 0.9rem;">
                    341 respuestas · 41 variables<br>
                    Base limpia y homologada
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            csv_encuestas = df_encuestas.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="⬇️ Descargar encuestas",
                data=csv_encuestas,
                file_name="encuestas_villahermosa_2026.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.markdown("""
            <div class="glass-card">
                <h4 style="color: #1f2937;">🌐 Base Google Maps</h4>
                <p style="color: #6b7280; font-size: 0.9rem;">
                    2,278 restaurantes mapeados<br>
                    Ratings, reseñas, contacto
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            csv_gmb = df_gmb.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="⬇️ Descargar GMB",
                data=csv_gmb,
                file_name="restaurantes_gmb_villahermosa.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #1f2937;">📊 Solo los datos filtrados</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">
                Descarga únicamente los registros que coinciden con tus filtros actuales
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        csv_filtered = df_filtered.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="⬇️ Descargar selección filtrada",
            data=csv_filtered,
            file_name="datos_filtrados.csv",
            mime="text/csv"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("📄 Documentos adicionales"):
            st.markdown("""
            Los siguientes documentos están disponibles bajo solicitud:
            
            - **Estudio Antropológico** - Análisis profundo de la psicología del consumidor tabasqueño
            - **Transcripciones de Focus Groups** - 2 sesiones con consumidores reales
            - **Resumen Ejecutivo en PDF** - Para presentaciones
            
            Contacta al equipo de NO ROBOT para acceder a estos materiales.
            """)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; padding: 24px; border-top: 1px solid rgba(219, 39, 119, 0.15);">
    <p style="color: #9ca3af; font-size: 0.85rem; margin: 0;">
        Consumer Insights Dashboard · Villahermosa 2026
    </p>
    <p style="color: #6b7280; font-size: 0.8rem; margin: 8px 0 0 0;">
        Desarrollado por <strong style="color: #db2777;">NO ROBOT</strong> · 
        {len(df_encuestas)} encuestados + {len(df_gmb):,} restaurantes + 2 focus groups
    </p>
</div>
""", unsafe_allow_html=True)
