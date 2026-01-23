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
import re
import os
from pathlib import Path

# ============================================================================
# AUTENTICACIÓN SIMPLE
# ============================================================================
def get_logo_login():
    """Obtener logo codificado en base64 para login"""
    logo_path = Path(__file__).parent / "assets" / "logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def check_auth():
    """Verificar autenticación del usuario"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.set_page_config(
            page_title="Login - Dashboard VH26",
            page_icon="🍽️",
            layout="centered"
        )
        
        logo_login = get_logo_login()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if logo_login:
                st.markdown(f"""
                <div style='text-align: center; padding: 40px 0 20px 0;'>
                    <img src='data:image/png;base64,{logo_login}' style='width: 200px; margin-bottom: 20px;'/>
                    <h1 style='margin: 10px 0;'>Consumer Insights Dashboard</h1>
                    <p style='color: #666; font-size: 16px;'>VH26 - Villahermosa</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='text-align: center; padding: 40px 0;'>
                    <h1>Consumer Insights Dashboard</h1>
                    <p style='color: #666; font-size: 16px;'>VH26 - Villahermosa</p>
                </div>
                """, unsafe_allow_html=True)
            
            password = st.text_input("Contraseña:", type="password", placeholder="Ingresa la contraseña")
            
            if st.button("Acceder", use_container_width=True, type="primary"):
                if password == "admin123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")
        
        st.stop()

# Ejecutar verificación de autenticación
check_auth()

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
# CSS base con glassmorphism mejorado
CSS_STYLES = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Ocultar elementos de Streamlit/GitHub */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    .viewerBadge_container__r5tak {display: none !important;}
    .styles_viewerBadge__CvC9N {display: none !important;}
    
    /* Ocultar iconos flotantes de esquina inferior */
    .stActionButton {display: none !important;}
    [data-testid="manage-app-button"] {display: none !important;}
    .st-emotion-cache-zq5wmm {display: none !important;}
    .st-emotion-cache-1dp5vir {display: none !important;}
    iframe[title="streamlit_feedback.st_feedback"] {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    button[kind="icon"] {display: none !important;}
    .stApp > div:last-child > div:last-child > div:last-child {display: none !important;}
    
    /* Animaciones globales */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 4px 24px rgba(219, 39, 119, 0.1); }
        50% { box-shadow: 0 4px 32px rgba(219, 39, 119, 0.2); }
    }
    
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Sidebar mejorado con efecto glass real */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(252,231,243,0.9) 100%) !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
        border-right: 1px solid rgba(219, 39, 119, 0.15) !important;
        box-shadow: 4px 0 24px rgba(219, 39, 119, 0.08) !important;
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    [data-testid="stSidebar"] * {
        color: #4a4a4a !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {
        color: #6b7280 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Glass Card mejorada con inner glow */
    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 18px 20px;
        margin: 8px 0;
        box-shadow: 
            0 4px 24px rgba(219, 39, 119, 0.08),
            inset 0 1px 1px rgba(255, 255, 255, 0.8),
            inset 0 -1px 1px rgba(219, 39, 119, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        min-height: auto;
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 12px 40px rgba(219, 39, 119, 0.15),
            inset 0 1px 1px rgba(255, 255, 255, 0.9),
            inset 0 -1px 1px rgba(219, 39, 119, 0.08);
        border-color: rgba(219, 39, 119, 0.25);
    }
    
    /* KPI Cards con efecto premium */
    .kpi-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(252,231,243,0.85) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 28px 24px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 4px 24px rgba(219, 39, 119, 0.1),
            inset 0 2px 4px rgba(255, 255, 255, 0.9);
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .kpi-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.3) 50%, transparent 60%);
        animation: shimmer 3s infinite;
        pointer-events: none;
    }
    
    .kpi-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 
            0 16px 48px rgba(219, 39, 119, 0.2),
            inset 0 2px 4px rgba(255, 255, 255, 1);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #db2777 0%, #9333ea 50%, #db2777 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 4s linear infinite;
        letter-spacing: -1px;
    }
    
    .kpi-label {
        color: #6b7280;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1f2937 0%, #db2777 40%, #9333ea 70%, #db2777 100%);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 8px;
        animation: shimmer 6s linear infinite;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #6b7280;
        text-align: center;
        font-size: 1.05rem;
        margin-bottom: 36px;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    /* Separador de sección mejorado */
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1f2937;
        margin: 40px 0 20px 0;
        padding: 12px 18px;
        border-left: 4px solid #db2777;
        background: linear-gradient(90deg, rgba(219, 39, 119, 0.08) 0%, transparent 100%);
        border-radius: 0 12px 12px 0;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, rgba(219, 39, 119, 0.2), transparent);
    }
    
    /* Alerts con efecto glass */
    .alert-success {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.12) 0%, rgba(34, 197, 94, 0.05) 100%);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(34, 197, 94, 0.25);
        border-radius: 16px;
        padding: 20px 22px;
        color: #166534;
        margin: 14px 0;
        box-shadow: 0 4px 16px rgba(34, 197, 94, 0.1);
        animation: fadeInUp 0.4s ease-out;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, rgba(234, 179, 8, 0.12) 0%, rgba(234, 179, 8, 0.05) 100%);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(234, 179, 8, 0.25);
        border-radius: 16px;
        padding: 20px 22px;
        color: #854d0e;
        margin: 14px 0;
        box-shadow: 0 4px 16px rgba(234, 179, 8, 0.1);
        animation: fadeInUp 0.4s ease-out;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(239, 68, 68, 0.05) 100%);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-radius: 16px;
        padding: 20px 22px;
        color: #991b1b;
        margin: 14px 0;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.1);
        animation: fadeInUp 0.4s ease-out;
    }
    
    .alert-info {
        background: linear-gradient(135deg, rgba(219, 39, 119, 0.1) 0%, rgba(147, 51, 234, 0.06) 100%);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(219, 39, 119, 0.2);
        border-radius: 16px;
        padding: 20px 22px;
        color: #4a4a4a;
        margin: 14px 0;
        box-shadow: 0 4px 16px rgba(219, 39, 119, 0.08);
        animation: fadeInUp 0.4s ease-out;
    }
    
    .quote-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(252, 231, 243, 0.5) 100%);
        backdrop-filter: blur(12px);
        border-left: 4px solid #db2777;
        border-radius: 0 20px 20px 0;
        padding: 22px 26px;
        margin: 16px 0;
        font-style: italic;
        color: #374151;
        box-shadow: 
            0 4px 20px rgba(219, 39, 119, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        position: relative;
        transition: all 0.3s ease;
    }
    
    .quote-card::before {
        content: '"';
        position: absolute;
        top: 10px;
        left: 16px;
        font-size: 3rem;
        color: rgba(219, 39, 119, 0.15);
        font-family: Georgia, serif;
        line-height: 1;
    }
    
    .quote-card:hover {
        transform: translateX(4px);
        box-shadow: 0 6px 24px rgba(219, 39, 119, 0.12);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }
    
    p, span, div {
        color: #4b5563;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(252,231,243,0.9) 100%) !important;
        color: #db2777 !important;
        border: 1px solid rgba(219, 39, 119, 0.25) !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(219, 39, 119, 0.1) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #fce7f3 0%, #f5d0fe 100%) !important;
        border-color: #db2777 !important;
        box-shadow: 0 6px 20px rgba(219, 39, 119, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba(219, 39, 119, 0.15) !important;
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
    
    /* Tabs mejorados con efecto glass */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(252,231,243,0.6) 100%) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
        padding: 8px !important;
        gap: 6px !important;
        border: 1px solid rgba(219, 39, 119, 0.12) !important;
        box-shadow: 0 2px 12px rgba(219, 39, 119, 0.06) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #6b7280 !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(219, 39, 119, 0.06) !important;
        color: #db2777 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, white 0%, #fdf2f8 100%) !important;
        color: #db2777 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 16px rgba(219, 39, 119, 0.15) !important;
        border: 1px solid rgba(219, 39, 119, 0.2) !important;
    }
    
    /* Radio buttons (pestañas horizontales) mejorados */
    .stRadio > div {
        background: linear-gradient(135deg, rgba(255,255,255,0.85) 0%, rgba(252,231,243,0.7) 100%) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
        padding: 8px 12px !important;
        border: 1px solid rgba(219, 39, 119, 0.12) !important;
        gap: 8px !important;
    }
    
    .stRadio label {
        background: transparent !important;
        padding: 10px 18px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
    }
    
    .stRadio label:hover {
        background: rgba(219, 39, 119, 0.08) !important;
    }
    
    .stRadio label[data-checked="true"] {
        background: white !important;
        box-shadow: 0 2px 10px rgba(219, 39, 119, 0.15) !important;
        font-weight: 600 !important;
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
        background: linear-gradient(135deg, rgba(255,255,255,0.92) 0%, rgba(255,255,255,0.8) 100%);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(219, 39, 119, 0.1);
        border-radius: 16px;
        padding: 18px 22px;
        margin: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .ranking-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 0;
        background: linear-gradient(90deg, rgba(219, 39, 119, 0.1), transparent);
        transition: width 0.3s ease;
    }
    
    .ranking-item:hover {
        background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(252,231,243,0.9) 100%);
        border-color: rgba(219, 39, 119, 0.25);
        transform: translateX(6px);
        box-shadow: 0 4px 16px rgba(219, 39, 119, 0.1);
    }
    
    .ranking-item:hover::before {
        width: 4px;
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

# Aplicar fondo con overlay para mejor contraste
if bg_base64:
    st.markdown(f"""
    <style>
        .stApp {{
            background-image: 
                linear-gradient(135deg, rgba(255,255,255,0.85) 0%, rgba(252,231,243,0.75) 50%, rgba(255,255,255,0.85) 100%),
                url("data:image/png;base64,{bg_base64}");
            background-size: cover, cover;
            background-position: center, center;
            background-attachment: fixed, fixed;
        }}
    </style>
    """, unsafe_allow_html=True)
else:
    # Fondo sutil cuando no hay imagen
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #fdf2f8 0%, #faf5ff 25%, #f0f9ff 50%, #faf5ff 75%, #fdf2f8 100%);
            background-size: 400% 400%;
            animation: gradient-shift 15s ease infinite;
        }
        
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================================
@st.cache_data
def load_encuestas(data_mtime):
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
    """Obtiene conteo de menciones de restaurantes con normalización"""
    rest_cols = ['Restaurante_1', 'Restaurante_2', 'Restaurante_3', 'Restaurante_4', 'Restaurante_5']
    cat_cols = ['Mariscos', 'Carne', 'Hamburguesas', 'Pizzas', 'Sushi', 'Tacos', 
                'Comida típica tabasqueña', 'Mexicana', 'Desayunos', 'Brunch', 
                'Bar', 'Bufete', 'Está de moda', 'Ya no está de moda:', 'Celebraciones']
    protected_phrases = {
        'pescados y mariscos',
        'mar & co',
        'mar&co',
        'mar y tierra',
        'tortas y más tortas',
        'chavo, kiko y ñoño',
        'chavo kiko y ñoño',
        'kiko y ñoño'
    }
    invalid_mentions = {
        '1', 'No responde', 'No respondió', 'No respondio', 'No sé',
        'No se', 'No', 'Ninguno', 'N/A', 'Na', 'No Respondió', 'No Respondio'
    }
    split_pattern = re.compile(r'\s*(?:/|,|;|\by\b|&|\+)\s*', re.IGNORECASE)
    
    all_mentions = []
    for col in rest_cols + cat_cols:
        if col in df.columns:
            vals = df[col].dropna().astype(str)
            vals = vals[~vals.isin(list(invalid_mentions))]
            for raw_val in vals.tolist():
                raw_str = str(raw_val).strip()
                raw_lower = raw_str.lower()
                if raw_lower in protected_phrases:
                    parts = [raw_str]
                else:
                    parts = [p.strip() for p in split_pattern.split(raw_str) if p and p.strip()]
                for part in parts:
                    if part in invalid_mentions:
                        continue
                    all_mentions.append(normalize_restaurant_name(part))
    
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
    
    # Limpiar espacios
    name = name.strip()
    if not name:
        return name
    
    name_lower = name.lower()
    
    # Mapeo de variaciones a nombre canónico
    normalizations = {
        # Di Bari
        'di bari': 'Di Bari',
        'dibari': 'Di Bari',
        'dibaris': 'Di Bari',
        'd bari': 'Di Bari',
        'dbari': 'Di Bari',
        "di'bari": 'Di Bari',
        'de bari': 'Di Bari',
        'di baris': 'Di Bari',
        
        # Boston's
        'bostons': "Boston's",
        "boston's": "Boston's",
        "boston's pizza": "Boston's",
        'bostongs': "Boston's",
        'bostoons': "Boston's",
        'boston': "Boston's",
        
        # McDonald's
        "mcdonald's": "McDonald's",
        'mcdonalds': "McDonald's",
        'mc donalds': "McDonald's",
        'mc donald': "McDonald's",
        'magdonald': "McDonald's",
        'macdonald': "McDonald's",
        
        # Manila Garden
        'manila': 'Manila Garden',
        'manila garden': 'Manila Garden',
        'manila carden': 'Manila Garden',
        'centrico, manila': 'Manila Garden',
        
        # Groshi
        'groshi': 'Groshi',
        'groshi express': 'Groshi',
        'groshi expres': 'Groshi',
        
        # 7 Quince
        '7 quince': '7 Quince',
        '7quince': '7 Quince',
        '7:quince': '7 Quince',
        '7: quince': '7 Quince',
        '7/quince': '7 Quince',
        'siete quince': '7 Quince',
        
        # Sushi House
        'sushi house': 'Sushi House',
        
        # Sushi Roll
        'sushi roll': 'Sushi Roll',
        'sushi and roll': 'Sushi Roll',
        'sushiroll': 'Sushi Roll',
        
        # Carl's Jr
        "carl's jr": "Carl's Jr",
        'carls': "Carl's Jr",
        'carl jr': "Carl's Jr",
        "carl's jr": "Carl's Jr",
        
        # Wings - Son 3 restaurantes diferentes
        'wings army': 'Wings Army',
        'wingstop': 'Wingstop',
        'wings bunker': 'Wings Bunker',
        'wing stop': 'Wingstop',
        'wingstop altabrisa': 'Wingstop',
        
        # Otros
        'madison': 'Madison Grill',
        'madisson': 'Madison Grill',
        'madison grill': 'Madison Grill',
        'madison/grill': 'Madison Grill',
        'leo restaurante': 'Leo',
        'leo en tu casa': 'Leo',
        'salon caimito': 'Salón Caimito',
        'salón caimito': 'Salón Caimito',
        'a takear': 'A Takear',
        'atakear': 'A Takear',
        'mcdonalds': "McDonald's",
        "mcdonald’s": "McDonald's",
        'basilico': 'Basilico',
        'basílico': 'Basilico',
        'la cevicheria': 'La Cevichería',
        'la cevichería': 'La Cevichería',
        'el eden': 'El Edén',
        'el edén': 'El Edén',
        'dominos': "Domino's",
        "domino's": "Domino's",
        'dominós': "Domino's",
        "domino’s": "Domino's",
        'marisquería el eden': 'Marisquería El Edén',
        'marisquería el edén': 'Marisquería El Edén',
        'querreve': 'Querrevé',
        'querrevé': 'Querrevé',
        'mr bongle': 'Mr. Bongle',
        'mr. bongle': 'Mr. Bongle',
        'namu': 'Namú',
        'namú': 'Namú',
        'el rincon tabasqueño': 'El Rincón Tabasqueño',
        'el rincón tabasqueño': 'El Rincón Tabasqueño',
        'mar&co': 'Mar&Co',
        'mar &co': 'Mar&Co',
        'bisquets obregon': 'Bisquets Obregón',
        'bisquets obregón': 'Bisquets Obregón',
        'don chingon': 'Don Chingón',
        'don chingón': 'Don Chingón',
        'chilis': "Chili's",
        "chili's": "Chili's",
        'dominos pizza': "Domino's Pizza",
        'dominós pizza': "Domino's Pizza",
        'la toto': 'La Totó',
        'la totó': 'La Totó',
        'boi rojo': 'Boí Rojo',
        'boí rojo': 'Boí Rojo',
        'chicagomx': 'Chicago Mx',
        'chicago mx': 'Chicago Mx',
        'el asadero del ostion': 'El Asadero Del Ostión',
        'el asadero del ostión': 'El Asadero Del Ostión',
        'el reyna': 'El Reyna',
        'la lupita': 'La Lupita',
        'la lupita mariscos': 'La Lupita',
        'bar la lupita': 'La Lupita',
        'milagrito': 'Milagrito',
        'fuego extremo': 'Fuego Extremo',
        'fuego animal': 'Fuego Animal',
        'el machetazo': 'El Machetazo',
        'banquetacos': 'Banquetacos',
        'tacos joven': 'Tacos Joven',
        'sushito': 'Sushito',
        'han sushi': 'Han Sushi',
        
        # El Matador
        'matador': 'El Matador',
        'el matador': 'El Matador',
    }
    
    # Buscar coincidencia exacta
    if name_lower in normalizations:
        return normalizations[name_lower]
    
    # Buscar coincidencia parcial para casos con texto adicional
    for key, value in normalizations.items():
        if name_lower.startswith(key) or key in name_lower:
            return value
    
    # Si no hay coincidencia, convertir a título
    return name.title()

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
    protected_phrases = {
        'pescados y mariscos',
        'mar & co',
        'mar&co',
        'mar y tierra',
        'tortas y más tortas',
        'chavo, kiko y ñoño',
        'chavo kiko y ñoño',
        'kiko y ñoño'
    }
    invalid_mentions = {
        '1', 'No responde', 'No respondió', 'No respondio', 'No sé',
        'No se', 'No', 'Ninguno', 'N/A', 'Na', 'No Respondió', 'No Respondio'
    }
    split_pattern = re.compile(r'\s*(?:/|,|;|\by\b|&|\+)\s*', re.IGNORECASE)
    for name, col in categories.items():
        if col in df.columns:
            vals = df[col].dropna().astype(str)
            vals = vals[~vals.isin([
                '1', 'No responde', 'No respondió', 'No respondio', 'No sé',
                'No se', 'No', 'Ninguno', 'N/A', 'Na', 'No Respondió', 'No Respondio'
            ])]
            normalized_vals = []
            for raw_val in vals.tolist():
                raw_str = str(raw_val).strip()
                raw_lower = raw_str.lower()
                if raw_lower in protected_phrases:
                    parts = [raw_str]
                else:
                    parts = [p.strip() for p in split_pattern.split(raw_str) if p and p.strip()]
                for part in parts:
                    if part in invalid_mentions:
                        continue
                    normalized_vals.append(normalize_restaurant_name(part))
            if len(normalized_vals) > 0:
                counts = Counter(normalized_vals)
                if counts:
                    top = counts.most_common(5)
                    leaders[name] = top
    
    return leaders

def format_gmb_rating(value):
    """Formatea rating de GMB con manejo seguro de nulos"""
    try:
        v = float(value)
        if pd.isna(v):
            return "—"
        return f"⭐ {v:.1f}"
    except Exception:
        return "—"

def format_gmb_reviews(value):
    """Formatea reseñas de GMB con manejo seguro de nulos"""
    try:
        v = int(float(value))
        if v < 0:
            return "—"
        return f"{v:,}"
    except Exception:
        return "—"

def parse_gmb_rating(value):
    """Convierte rating a float seguro"""
    try:
        v = float(value)
        if pd.isna(v):
            return None
        return v
    except Exception:
        return None

def parse_gmb_reviews(value):
    """Convierte reseñas a int seguro"""
    try:
        v = int(float(value))
        if v < 0:
            return None
        return v
    except Exception:
        return None

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
    encuestas_path = Path(__file__).parent / "data_encuestas.csv"
    df_encuestas = load_encuestas(os.path.getmtime(encuestas_path))
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
    # Logo NO ROBOT con efecto premium
    logo_path = Path(__file__).parent / "assets" / "logo.png"
    if logo_path.exists():
        logo_base64 = get_image_base64(logo_path)
        st.markdown(f"""
        <div style="text-align: center; padding: 24px 10px; margin-bottom: 24px; 
                    background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(252,231,243,0.7) 100%);
                    border-radius: 20px;
                    border: 1px solid rgba(219, 39, 119, 0.1);
                    box-shadow: 0 4px 16px rgba(219, 39, 119, 0.08);">
            <img src="data:image/png;base64,{logo_base64}" 
                 style="max-width: 160px; height: auto; margin-bottom: 10px; 
                        filter: drop-shadow(0 2px 4px rgba(219, 39, 119, 0.15));">
            <p style="color: #9ca3af; font-size: 0.7rem; margin: 0; text-transform: uppercase; 
                      letter-spacing: 2px; font-weight: 600;">Consumer Insights</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 24px 10px; margin-bottom: 24px; 
                    background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(252,231,243,0.7) 100%);
                    border-radius: 20px;
                    border: 1px solid rgba(219, 39, 119, 0.1);
                    box-shadow: 0 4px 16px rgba(219, 39, 119, 0.08);">
            <div style="font-size: 1.4rem; font-weight: 800; 
                        background: linear-gradient(135deg, #db2777, #9333ea);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                        letter-spacing: 3px;">NO ROBOT</div>
            <p style="color: #9ca3af; font-size: 0.7rem; margin-top: 6px; text-transform: uppercase; 
                      letter-spacing: 2px; font-weight: 600;">Consumer Insights</p>
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
        "🌐 Ranking Google",
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
        edad_options = sorted([x for x in df_encuestas[col_edad].dropna().unique() if x not in ['No responde', 'No Respondió', 'No Respondio']])
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
        zona_options = sorted([x for x in df_encuestas[col_zona].dropna().unique() if x not in ['No responde', 'No Respondió', 'No Respondio']])
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
        gasto_disponibles = [x for x in df_encuestas[col_gasto].dropna().unique() if x not in ['No responde', 'No Respondió', 'No Respondio']]
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
        freq_disponibles = [x for x in df_encuestas[col_freq].dropna().unique() if x not in ['No responde', 'No Respondió', 'No Respondio']]
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
    
    # Botón de limpiar caché al final del sidebar
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🗑️ Limpiar caché", use_container_width=True, help="Actualiza los datos desde los archivos"):
        st.cache_data.clear()
        st.rerun()

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
        
        # Contexto dinámico según filtros
        filtro_activo = []
        if filter_edad:
            filtro_activo.append(f"edad: {', '.join(filter_edad)}")
        if filter_zona:
            filtro_activo.append(f"zona: {', '.join(filter_zona[:2])}{'...' if len(filter_zona) > 2 else ''}")
        contexto_filtro = f" para el segmento ({'; '.join(filtro_activo)})" if filtro_activo else ""
        
        # 1. El favorito - siempre dinámico
        if top_restaurant[0] != "N/A":
            # Obtener datos de Google si existen
            gmb_match = match_gmb(top_restaurant[0], df_gmb) if 'match_gmb' in dir() else None
            google_info = ""
            if gmb_match is not None:
                google_info = f" Google lo respalda con ⭐{gmb_match['rating']}."
            
            st.markdown(f"""
            <div class="alert-success">
                <strong>🏆 El favorito{contexto_filtro}</strong><br>
                <span style="font-size: 1.15rem; font-weight: 600;">{top_restaurant[0]}</span> lidera 
                con <strong>{top_restaurant[1]}</strong> menciones ({round(top_restaurant[1]/len(df_filtered)*100, 1) if len(df_filtered) > 0 else 0}% de los encuestados).{google_info}
            </div>
            """, unsafe_allow_html=True)
        
        # 2. Competencia del mercado - insight útil
        if len(mentions) >= 3:
            top_3 = mentions.most_common(3)
            top_3_total = sum([x[1] for x in top_3])
            total_menciones = sum(mentions.values())
            concentracion = round(top_3_total / total_menciones * 100) if total_menciones > 0 else 0
            num_restaurantes = len(mentions)
            
            # Determinar nivel de competencia
            if concentracion >= 40:
                color_class = "alert-danger"
                icon = "🏢"
                titulo = "Mercado dominado"
                insight = f"Solo 3 restaurantes concentran casi la mitad de las preferencias. <strong>Difícil competir</strong> sin diferenciación radical."
            elif concentracion >= 25:
                color_class = "alert-info"
                icon = "⚖️"
                titulo = "Competencia equilibrada"
                insight = f"Hay líderes claros pero todavía <strong>hay espacio para crecer</strong> si ofreces algo diferente."
            else:
                color_class = "alert-success"
                icon = "🎯"
                titulo = "Mercado abierto"
                insight = f"Con {num_restaurantes} opciones mencionadas, <strong>nadie domina</strong>. Oportunidad para posicionarte con buena estrategia."
            
            top_3_names = ", ".join([f"{x[0]} ({x[1]})" for x in top_3])
            st.markdown(f"""
            <div class="{color_class}">
                <strong>{icon} {titulo}</strong><br>
                Los más mencionados: <strong>{top_3_names}</strong>. {insight}
            </div>
            """, unsafe_allow_html=True)
        
        # 3. Tendencia - De Moda vs En Declive
        moda_names = set()
        declive_names = set()
        
        if 'De Moda' in leaders and leaders['De Moda']:
            valid_moda = [(n, c) for n, c in leaders['De Moda'] if len(n) > 3 and n.lower() not in ['no', 'ninguno', 'no sé', 'ns', 'no responde', 'no respondió']]
            if valid_moda:
                moda_leader = valid_moda[0]
                moda_names.add(moda_leader[0])
                st.markdown(f"""
                <div class="alert-info">
                    <strong>📈 En ascenso</strong><br>
                    <span style="font-weight: 600;">{moda_leader[0]}</span> está ganando popularidad 
                    ({moda_leader[1]} menciones como "de moda"). Observa qué están haciendo bien.
                </div>
                """, unsafe_allow_html=True)
        
        if 'En Declive' in leaders and leaders['En Declive']:
            valid_decline = [(n, c) for n, c in leaders['En Declive'] if len(n) > 3 and n.lower() not in ['no', 'ninguno', 'no sé', 'ns', 'no responde', 'no respondió']]
            if valid_decline:
                decline_leader = valid_decline[0]
                declive_names.add(decline_leader[0])
                st.markdown(f"""
                <div class="alert-danger">
                    <strong>⚠️ En declive</strong><br>
                    <span style="font-weight: 600;">{decline_leader[0]}</span> fue mencionado 
                    {decline_leader[1]} veces como "ya no está de moda". Posible fatiga de marca.
                </div>
                """, unsafe_allow_html=True)
        
        # 4. Oportunidad de mercado - qué hace falta
        col_falta = "11. ¿Qué tipo de restaurante o experiencia consideras que hacen falta o están poco desarrollados en Villahermosa?"
        if col_falta in df_filtered.columns:
            falta_data = df_filtered[col_falta].dropna().astype(str)
            # Filtrar respuestas inválidas y muy cortas
            falta_data = falta_data[
                (~falta_data.str.lower().isin(['no responde', 'no respondió', 'no respondio', 'no sé', 'ninguno', 'no', 'na', 'n/a'])) & 
                (falta_data.str.len() > 3)
            ]
            if len(falta_data) > 0:
                falta_counts = Counter(falta_data)
                top_falta = falta_counts.most_common(2)
                
                if top_falta:
                    oportunidades = " y ".join([f"<strong>{item[0]}</strong> ({item[1]})" for item in top_falta])
                    st.markdown(f"""
                    <div class="alert-warning">
                        <strong>💡 Oportunidad detectada</strong><br>
                        Los encuestados piden: {oportunidades}. Nichos con potencial de crecimiento.
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
            edad_counts = edad_counts[~edad_counts.index.isin(['No responde', 'No Respondió', 'No Respondio'])]
            
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
            gasto_counts = gasto_counts[~gasto_counts.index.isin(['No responde', 'No Respondió', 'No Respondio'])]
            
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
        cross_tab = cross_tab.drop(['No responde', 'No Respondió', 'No Respondio'], errors='ignore')
        cross_tab = cross_tab.drop(['No responde', 'No Respondió', 'No Respondio'], axis=1, errors='ignore')
        cross_tab = cross_tab.loc[cross_tab.sum(axis=1) > 0]
        
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
        zona_counts = zona_counts[~zona_counts.index.isin(['No responde', 'No Respondió', 'No Respondio'])]
        
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
    
    # ========== NUEVA SECCIÓN: Perfil de Consumo ==========
    st.markdown('<div class="section-title">💡 Perfil de Consumo</div>', unsafe_allow_html=True)
    st.caption("Insights clave sobre cómo y cuándo consumen los participantes del estudio")
    
    col_ocasion = "9. ¿Cuál es tu ocasión de consumo más frecuente?"
    col_relacion_gasto = "4. Pensando en tu día a día, ¿cuál de las siguientes frases describe mejor tu relación con el gasto en restaurantes?"
    
    col_oc1, col_oc2 = st.columns(2)
    
    with col_oc1:
        # Ocasiones de consumo - separar respuestas múltiples por coma
        if col_ocasion in df_filtered.columns:
            # Separar respuestas múltiples
            ocasion_raw = df_filtered[col_ocasion].dropna().astype(str)
            ocasion_list = []
            for o in ocasion_raw:
                ocasion_list.extend([x.strip() for x in o.split(',') if x.strip()])
            
            ocasion_counts = Counter(ocasion_list)
            # Filtrar valores no válidos
            invalid = ['no responde', 'no respondió', 'no respondio', 'no', 'ninguno', 'na', 'n/a', '1']
            ocasion_counts = {k: v for k, v in ocasion_counts.items() if k.lower() not in invalid and len(k) > 2}
            
            # Mapear a iconos
            ocasion_icons = {
                'Comida familiar': '👨‍👩‍👧‍👦',
                'Reunión con amigos': '👯',
                'Cita en pareja': '💑',
                'Negocio / trabajo': '💼',
                'Solo(a)': '🧘',
                'Consumo individual': '🧘',
                'Celebración especial': '🎉',
                'Celebraciones': '🎉',
            }
            
            if ocasion_counts:
                st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #1f2937; margin-bottom: 15px;">🎯 ¿Cuándo van a comer fuera?</h4>
                """, unsafe_allow_html=True)
                
                total_ocasiones = sum(ocasion_counts.values())
                sorted_ocasiones = sorted(ocasion_counts.items(), key=lambda x: x[1], reverse=True)[:6]
                
                for ocasion, count in sorted_ocasiones:
                    pct = count / total_ocasiones * 100
                    icon = ocasion_icons.get(ocasion, '🍽️')
                    bar_width = min(pct * 1.5, 100)
                    st.markdown(f"""
                    <div style="margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="color: #374151;">{icon} {ocasion}</span>
                            <span style="color: #db2777; font-weight: 600;">{pct:.0f}%</span>
                        </div>
                        <div style="background: #f3f4f6; border-radius: 10px; height: 8px;">
                            <div style="background: linear-gradient(90deg, #f9a8d4, #db2777); width: {bar_width}%; height: 100%; border-radius: 10px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    with col_oc2:
        # Relación con el gasto
        if col_relacion_gasto in df_filtered.columns:
            gasto_rel = df_filtered[col_relacion_gasto].value_counts()
            gasto_rel = gasto_rel[~gasto_rel.index.isin(['No responde', 'No Respondió', 'No Respondio', 'no responde', 'Prefiero no responder,'])]
            
            # Mapear a etiquetas cortas - valores reales del dataset
            gasto_map = {
                'Puedo salir a restaurantes pero cuido mi presupuesto': ('🎯 Moderados', 'Salen pero cuidan su presupuesto'),
                'Puedo salir a comer a restaurantes con frecuencia sin afectar mi presupuesto,': ('💎 Sin restricción', 'Comen fuera frecuentemente sin problemas'),
                'Puedo salir a comer a restaurantes con frecuencia sin afectar mi presupuesto': ('💎 Sin restricción', 'Comen fuera frecuentemente sin problemas'),
                'Salgo a comer fuera solo en ocasiones especiales,': ('🎂 Solo ocasiones', 'Reservan para celebraciones especiales'),
                'Rara vez salgo a comer fuera por temas de presupuesto,': ('💰 Presupuesto limitado', 'Rara vez salen por temas económicos'),
                'Rara vez salgo a comer fuera por temas de presupuesto': ('💰 Presupuesto limitado', 'Rara vez salen por temas económicos'),
            }
            
            if len(gasto_rel) > 0:
                st.markdown("""
                <div class="glass-card">
                    <h4 style="color: #1f2937; margin-bottom: 15px;">💸 Mentalidad de gasto</h4>
                """, unsafe_allow_html=True)
                
                total = gasto_rel.sum()
                for frase, count in gasto_rel.items():
                    pct = count / total * 100
                    mapped = gasto_map.get(frase)
                    if mapped:
                        label, desc = mapped
                    else:
                        # Fallback: crear etiqueta del texto original
                        label = '📊 ' + frase[:30] + ('...' if len(frase) > 30 else '')
                        desc = frase
                    
                    # Color según tipo
                    if 'Moderados' in label:
                        color = '#3b82f6'
                    elif 'Sin restricción' in label:
                        color = '#8b5cf6'
                    elif 'Solo ocasiones' in label:
                        color = '#f59e0b'
                    elif 'limitado' in label:
                        color = '#ef4444'
                    else:
                        color = '#10b981'
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 14px; padding: 12px; background: {color}10; border-radius: 10px; border-left: 4px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #1f2937; font-weight: 600; font-size: 1rem;">{label}</span>
                            <span style="color: {color}; font-weight: 700; font-size: 1.2rem;">{pct:.0f}%</span>
                        </div>
                        <div style="color: #6b7280; font-size: 0.85rem; margin-top: 6px;">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

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
                            if gmb_match is not None:
                                rating_text = f"⭐ {gmb_match['rating']}"
                                reviews_text = f"{int(gmb_match['reviews']):,} reseñas"
                            else:
                                rating_text = "Sin datos GMB"
                                reviews_text = "&nbsp;"  # Espacio para mantener altura
                            
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
                vals = vals[~vals.isin(['1', 'No responde', 'No Respondió', 'No Respondio', 'No sé', 'Ninguno', 'No se', 'No'])]
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
                            "Rating GMB": format_gmb_rating(gmb_match.get('rating')),
                            "Reseñas": format_gmb_reviews(gmb_match.get('reviews'))
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
            rating = parse_gmb_rating(gmb_match.get('rating'))
            reviews = parse_gmb_reviews(gmb_match.get('reviews'))
            
            if rating is not None and reviews is not None and rating >= 4.5 and reviews >= 500:
                status = '✅ Validado'
            elif rating is not None and rating >= 4.0:
                status = '✅ OK'
            elif reviews is not None and reviews < 200:
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
            'Rating GMB': format_gmb_rating(rating),
            'Reseñas': format_gmb_reviews(reviews),
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
        
        # Construir texto de Google de forma segura
        google_text = ""
        if leader['Rating GMB'] and leader['Reseñas']:
            try:
                google_text = f"Google lo respalda con ⭐{leader['Rating GMB']} y {int(leader['Reseñas']):,} reseñas."
            except (ValueError, TypeError):
                google_text = ""
        
        with col_i1:
            lider_texto = f"<strong>{leader['Restaurante']}</strong> domina con <strong>{leader['Menciones']} menciones</strong>."
            if google_text:
                lider_texto += f" {google_text}"
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #22c55e;">
                <h4 style="color: #166534; margin-bottom: 12px;">🏆 Líder indiscutible</h4>
                <p style="color: #4b5563; margin: 0;">{lider_texto}</p>
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
    
    # Hidden gems - filtrar NaN correctamente
    hidden_gems = []
    for item in validation_data:
        try:
            rating = item['Rating GMB']
            resenas = item['Reseñas']
            menciones = item['Menciones']
            if rating and rating >= 4.5 and resenas and resenas >= 1000 and menciones < 50:
                hidden_gems.append(item)
        except (TypeError, ValueError):
            continue
    
    if hidden_gems:
        gem = hidden_gems[0]
        try:
            reviews_text = f"{int(gem['Reseñas']):,}" if gem['Reseñas'] else "muchas"
        except (ValueError, TypeError):
            reviews_text = "muchas"
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #8b5cf6; margin-top: 12px;">
            <h4 style="color: #6d28d9; margin-bottom: 12px;">💎 Joyas escondidas</h4>
            <p style="color: #4b5563; margin: 0;">
                <strong>{gem['Restaurante']}</strong> tiene excelentes calificaciones en Google 
                (⭐{gem['Rating GMB']}, {reviews_text} reseñas) pero solo {gem['Menciones']} 
                menciones locales. Oportunidad de marketing: ¿por qué no está en el radar del consumidor tabasqueño?
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PÁGINA 6: RANKING GOOGLE
# ============================================================================
elif selected_page == "🌐 Ranking Google":
    
    # Cargar logo de GMB
    gmb_logo_path = Path(__file__).parent / "assets" / "gmb_logo.png"
    if gmb_logo_path.exists():
        with open(gmb_logo_path, "rb") as f:
            gmb_logo_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 20px;">
            <img src="data:image/png;base64,{gmb_logo_b64}" style="height: 50px;"/>
            <div>
                <h2 style="margin: 0; color: #1f2937;">Ranking Google My Business</h2>
                <p style="margin: 0; color: #6b7280;">Los mejor calificados según Google Maps</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-title">🌐 Ranking Google My Business</div>', unsafe_allow_html=True)
        st.caption("Los mejor calificados según Google Maps")
    
    # Filtrar restaurantes válidos (con rating y reseñas, SOLO de Villahermosa, SOLO restaurantes)
    df_gmb_valid = df_gmb[df_gmb['rating'].notna() & df_gmb['reviews'].notna()].copy()
    
    # Filtrar SOLO Villahermosa usando múltiples criterios
    def is_villahermosa(address):
        if pd.isna(address):
            return False
        addr_lower = str(address).lower()
        
        # Excluir explícitamente otras ciudades/estados
        exclude = ['cdmx', 'ciudad de méxico', 'cuauhtémoc', 'benito juárez', 'del valle',
                   'chihuahua', 'chih.', 'veracruz', 'ver.', 'oaxaca', 'camp.', 'carmen',
                   'mérida', 'yuc.', 'monterrey', 'guadalajara', 'puebla', 'cdad. del carmen']
        for ex in exclude:
            if ex in addr_lower:
                return False
        
        # Incluir si tiene indicadores de Villahermosa/Tabasco
        include = ['villahermosa', ', tab.', 'tabasco', ', tab,']
        for inc in include:
            if inc in addr_lower:
                return True
        
        # Incluir por código postal de Tabasco (86xxx)
        import re
        if re.search(r'\b86\d{3}\b', addr_lower):
            return True
        
        return False
    
    # Filtrar NO restaurantes (plazas, tiendas, hoteles, etc.)
    exclude_names = ['plaza altabrisa', 'plaza sendero', 'liverpool', 'mercado publico', 
                     'mercado la sierra', 'home depot', 'walmart', 'soriana', 'chedraui',
                     "sam's club", 'costco', 'office depot', 'hyatt', 'marriott', 'holiday inn',
                     'fiesta inn', 'hotel', 'motel', 'gasolinera', 'oxxo']
    
    def is_restaurant(name):
        if pd.isna(name):
            return False
        name_lower = str(name).lower()
        for kw in exclude_names:
            if kw in name_lower:
                return False
        return True
    
    df_gmb_valid = df_gmb_valid[
        df_gmb_valid['address'].apply(is_villahermosa) & 
        df_gmb_valid['name'].apply(is_restaurant)
    ]
    
    # KPIs de Google
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{len(df_gmb_valid):,}</div>
            <div class="kpi-label">Restaurantes en Google</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_rating = df_gmb_valid['rating'].mean()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{avg_rating:.1f}⭐</div>
            <div class="kpi-label">Rating promedio</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        top_rated_count = len(df_gmb_valid[df_gmb_valid['rating'] >= 4.5])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{top_rated_count}</div>
            <div class="kpi-label">Con ⭐4.5 o más</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_reviews = df_gmb_valid['reviews'].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{int(total_reviews):,}</div>
            <div class="kpi-label">Reseñas totales</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dos columnas: Top calificados y Más reseñados
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="section-title">🏆 Mejor calificados</div>', unsafe_allow_html=True)
        st.caption("Mínimo 300 reseñas para garantizar confiabilidad")
        
        top_rated = df_gmb_valid[df_gmb_valid['reviews'] >= 300].nlargest(10, 'rating')[['name', 'rating', 'reviews']]
        
        for i, (idx, row) in enumerate(top_rated.iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            st.markdown(f"""
            <div class="glass-card" style="padding: 16px; min-height: auto; margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; margin-right: 8px;">{medal}</span>
                        <strong style="color: #1f2937;">{row['name']}</strong>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #f59e0b; font-weight: 700;">⭐ {row['rating']}</span>
                        <span style="color: #6b7280; font-size: 0.8rem; margin-left: 8px;">{int(row['reviews']):,} reseñas</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="section-title">📊 Más reseñados</div>', unsafe_allow_html=True)
        st.caption("Los más populares por volumen de opiniones")
        
        most_reviewed = df_gmb_valid.nlargest(10, 'reviews')[['name', 'rating', 'reviews']]
        
        for i, (idx, row) in enumerate(most_reviewed.iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            st.markdown(f"""
            <div class="glass-card" style="padding: 16px; min-height: auto; margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; margin-right: 8px;">{medal}</span>
                        <strong style="color: #1f2937;">{row['name']}</strong>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #db2777; font-weight: 700;">{int(row['reviews']):,}</span>
                        <span style="color: #6b7280; font-size: 0.8rem; margin-left: 8px;">⭐ {row['rating']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # SECCIÓN: ANÁLISIS COMPARATIVO LOCAL VS GOOGLE
    # =========================================================================
    
    # Obtener menciones de la encuesta
    mentions = get_restaurant_mentions(df_filtered)
    mentioned_names = set([name.lower() for name in mentions.keys()])
    
    # Crear dataframe de comparación
    comparison_data = []
    for name, count in mentions.most_common(30):
        # Buscar en GMB
        match = df_gmb_valid[df_gmb_valid['name'].str.lower().str.contains(name.lower(), na=False)]
        if len(match) > 0:
            gmb_row = match.iloc[0]
            comparison_data.append({
                'name': name,
                'menciones': count,
                'rating': gmb_row['rating'],
                'reviews': int(gmb_row['reviews']) if pd.notna(gmb_row['reviews']) else 0
            })
    
    # =========================================================================
    # 1. SUBESTIMADOS: Buenos en Google pero poco mencionados localmente
    # =========================================================================
    st.markdown('<div class="section-title">📈 Subestimados localmente</div>', unsafe_allow_html=True)
    st.caption("Excelentes en Google pero con pocas menciones en la encuesta - Oportunidad de awareness")
    
    # Buscar restaurantes con buen rating pero pocas menciones
    underrated = df_gmb_valid[
        (df_gmb_valid['rating'] >= 4.5) & 
        (df_gmb_valid['reviews'] >= 300)
    ].copy()
    
    # Calcular menciones para cada uno
    def get_mentions(name):
        name_lower = str(name).lower()
        for m_name, m_count in mentions.items():
            if m_name.lower() in name_lower or name_lower in m_name.lower():
                return m_count
        return 0
    
    underrated['local_mentions'] = underrated['name'].apply(get_mentions)
    
    # Filtrar los que tienen pocas menciones pero buen rating
    underrated = underrated[underrated['local_mentions'] <= 10].nlargest(6, 'rating')
    
    if len(underrated) > 0:
        cols = st.columns(3)
        for i, (idx, row) in enumerate(underrated.iterrows()):
            with cols[i % 3]:
                mention_text = f"{int(row['local_mentions'])} menciones" if row['local_mentions'] > 0 else "Sin menciones"
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; border-left: 4px solid #8b5cf6;">
                    <div style="font-size: 1.8rem;">💎</div>
                    <div style="font-weight: 600; color: #1f2937; margin: 8px 0; font-size: 0.95rem;">{row['name']}</div>
                    <div style="color: #f59e0b; font-weight: 700; font-size: 1.2rem;">⭐ {row['rating']}</div>
                    <div style="color: #6b7280; font-size: 0.8rem;">{int(row['reviews']):,} reseñas Google</div>
                    <div style="background: #fef3c7; color: #92400e; padding: 4px 8px; border-radius: 12px; font-size: 0.75rem; margin-top: 8px; display: inline-block;">
                        {mention_text} locales
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-info" style="margin-top: 16px;">
            <strong>💡 Insight:</strong> Estos restaurantes tienen excelente reputación en Google pero los tabasqueños 
            no los mencionan mucho. Puede ser falta de awareness, marketing o posicionamiento local.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ Los mejor calificados en Google también son reconocidos localmente. ¡El mercado está alineado!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # 2. ALERTAS: Populares pero con rating bajo
    # =========================================================================
    st.markdown('<div class="section-title">⚠️ Alertas de reputación</div>', unsafe_allow_html=True)
    st.caption("Populares localmente pero con calificación baja en Google - Riesgo de percepción")
    
    # Encontrar alertas
    alerts = []
    for item in comparison_data:
        if item['rating'] < 4.2 and item['menciones'] >= 10:
            # Calcular brecha
            avg_rating = df_gmb_valid['rating'].mean()
            gap = round(avg_rating - item['rating'], 1)
            alerts.append({**item, 'gap': gap})
    
    alerts = sorted(alerts, key=lambda x: x['rating'])[:4]
    
    if alerts:
        for alert in alerts:
            # Color según severidad
            if alert['rating'] < 3.5:
                color = "#dc2626"
                severity = "🔴 Crítico"
            elif alert['rating'] < 4.0:
                color = "#f59e0b"
                severity = "🟡 Atención"
            else:
                color = "#eab308"
                severity = "🟡 Monitorear"
            
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid {color}; padding: 18px; min-height: auto;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <strong style="color: #1f2937; font-size: 1.1rem;">{alert['name']}</strong>
                            <span style="background: #dcfce7; color: #166534; padding: 2px 10px; border-radius: 12px; font-size: 0.8rem;">
                                📣 {alert['menciones']} menciones
                            </span>
                        </div>
                        <p style="color: #6b7280; margin: 8px 0 0 0; font-size: 0.85rem;">
                            Popular localmente pero {alert['gap']} puntos por debajo del promedio del mercado ({df_gmb_valid['rating'].mean():.1f}⭐).
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {color}; font-weight: 700; font-size: 1.3rem;">⭐ {alert['rating']}</div>
                        <div style="color: #6b7280; font-size: 0.75rem;">{alert['reviews']:,} reseñas</div>
                        <div style="color: {color}; font-size: 0.75rem; margin-top: 4px;">{severity}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-warning" style="margin-top: 16px;">
            <strong>⚡ Recomendación:</strong> Estos restaurantes tienen popularidad local pero su reputación en Google 
            no la refleja. Revisar comentarios negativos, mejorar servicio o incentivar reseñas positivas.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ Todos los restaurantes populares tienen buenas calificaciones en Google. ¡El mercado está alineado!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # 3. TOP PERFORMERS: Lo mejor de ambos mundos
    # =========================================================================
    st.markdown('<div class="section-title">🏆 Top Performers</div>', unsafe_allow_html=True)
    st.caption("Los que dominan tanto en percepción local como en Google")
    
    top_performers = [item for item in comparison_data if item['rating'] >= 4.5 and item['menciones'] >= 20]
    top_performers = sorted(top_performers, key=lambda x: (x['rating'], x['menciones']), reverse=True)[:5]
    
    if top_performers:
        cols = st.columns(len(top_performers))
        for i, perf in enumerate(top_performers):
            with cols[i]:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; border-top: 4px solid #22c55e; padding: 20px;">
                    <div style="font-size: 1.5rem;">{"🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "⭐"}</div>
                    <div style="font-weight: 600; color: #1f2937; margin: 8px 0;">{perf['name']}</div>
                    <div style="display: flex; justify-content: center; gap: 16px; margin-top: 8px;">
                        <div>
                            <div style="color: #f59e0b; font-weight: 700;">⭐ {perf['rating']}</div>
                            <div style="color: #9ca3af; font-size: 0.7rem;">Google</div>
                        </div>
                        <div>
                            <div style="color: #db2777; font-weight: 700;">{perf['menciones']}</div>
                            <div style="color: #9ca3af; font-size: 0.7rem;">Menciones</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-success" style="margin-top: 16px;">
            <strong>🎯 Los líderes del mercado:</strong> Estos restaurantes tienen excelente reputación en Google Y 
            son los favoritos de los tabasqueños. Son el benchmark a seguir.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Aplica filtros para ver los top performers del segmento seleccionado.")

# ============================================================================
# PÁGINA 7: TENDENCIAS
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
        vals = vals[~vals.isin(['1', 'No responde', 'No Respondió', 'No Respondio', 'No sé', 'Ninguno', 'No se'])]
        moda_data = Counter(vals).most_common(10)
    
    if col_decline in df_filtered.columns:
        vals = df_filtered[col_decline].dropna().astype(str)
        vals = vals[~vals.isin(['1', 'No responde', 'No Respondió', 'No Respondio', 'No sé', 'Ninguno', 'No se'])]
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
    
    # ========== NUEVA SECCIÓN: Marketing Digital ==========
    st.markdown('<div class="section-title">📱 ¿Dónde alcanzar a tu cliente?</div>', unsafe_allow_html=True)
    st.caption("Canales y contenido que más influyen en las decisiones de los consumidores")
    
    col_medios = "18. ¿A través de qué medios te enteras normalmente de promociones, ofertas o eventos de restaurantes en Villahermosa?"
    col_contenido = "18.1 ¿Qué tipo de contenido en redes sociales te motiva más a visitar un restaurante?"
    
    col_mk1, col_mk2 = st.columns(2)
    
    with col_mk1:
        if col_medios in df_filtered.columns:
            # Separar respuestas múltiples por coma
            medios_raw = df_filtered[col_medios].dropna().astype(str)
            medios_list = []
            for m in medios_raw:
                medios_list.extend([x.strip() for x in m.split(',') if x.strip()])
            
            medios_counts = Counter(medios_list)
            # Filtrar valores no válidos
            invalid = ['no responde', 'no respondió', 'no respondio', 'no', 'ninguno', 'na', 'n/a', '1']
            medios_counts = {k: v for k, v in medios_counts.items() if k.lower() not in invalid and len(k) > 2}
            
            if medios_counts:
                # Mapear a iconos
                canal_icons = {
                    'Instagram': '📸',
                    'Facebook': '📘',
                    'TikTok': '🎵',
                    'Recomendaciones de amigos/familiares': '👥',
                    'Google Maps / búsqueda en Google': '🗺️',
                    'WhatsApp': '💬',
                    'Periódicos / revistas locales': '📰',
                    'Radio': '📻',
                }
                
                st.markdown("""
                <div class="glass-card" style="border-left: 4px solid #e1306c;">
                    <h4 style="color: #1f2937; margin-bottom: 15px;">📢 Canales de descubrimiento</h4>
                    <p style="color: #6b7280; font-size: 0.8rem; margin-bottom: 15px;">Dónde se enteran de ofertas y promociones</p>
                """, unsafe_allow_html=True)
                
                total_menciones = sum(medios_counts.values())
                sorted_medios = sorted(medios_counts.items(), key=lambda x: x[1], reverse=True)[:6]
                
                for canal, count in sorted_medios:
                    pct = count / total_menciones * 100
                    icon = canal_icons.get(canal, '📌')
                    
                    # Colores por canal
                    if 'Instagram' in canal:
                        color = '#e1306c'
                    elif 'Facebook' in canal:
                        color = '#1877f2'
                    elif 'TikTok' in canal:
                        color = '#010101'
                    elif 'Google' in canal:
                        color = '#4285f4'
                    elif 'WhatsApp' in canal:
                        color = '#25d366'
                    elif 'amigos' in canal.lower() or 'Recomendaciones' in canal:
                        color = '#8b5cf6'
                    else:
                        color = '#6b7280'
                    
                    bar_width = min(pct * 1.5, 100)
                    st.markdown(f"""
                    <div style="margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                            <span style="color: #374151; font-size: 0.9rem;">{icon} {canal[:35]}</span>
                            <span style="color: {color}; font-weight: 600;">{pct:.0f}%</span>
                        </div>
                        <div style="background: #f3f4f6; border-radius: 6px; height: 6px;">
                            <div style="background: {color}; width: {bar_width}%; height: 100%; border-radius: 6px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    with col_mk2:
        if col_contenido in df_filtered.columns:
            # Separar respuestas múltiples
            contenido_raw = df_filtered[col_contenido].dropna().astype(str)
            contenido_list = []
            for c in contenido_raw:
                contenido_list.extend([x.strip() for x in c.split(',') if x.strip()])
            
            contenido_counts = Counter(contenido_list)
            invalid = ['no responde', 'no respondió', 'no respondio', 'no', 'ninguno', 'na', 'n/a', '1']
            contenido_counts = {k: v for k, v in contenido_counts.items() if k.lower() not in invalid and len(k) > 2}
            
            if contenido_counts:
                content_icons = {
                    'Fotos y videos de los platillos': '📷',
                    'Videos de la experiencia en el lugar': '🎬',
                    'Promociones y descuentos': '🏷️',
                    'Reseñas de influencers locales': '⭐',
                    'Menú con precios': '📋',
                    'Historias/reels del día a día': '📱',
                }
                
                st.markdown("""
                <div class="glass-card" style="border-left: 4px solid #8b5cf6;">
                    <h4 style="color: #1f2937; margin-bottom: 15px;">🎯 Contenido que convierte</h4>
                    <p style="color: #6b7280; font-size: 0.8rem; margin-bottom: 15px;">Qué tipo de posts motivan a visitar</p>
                """, unsafe_allow_html=True)
                
                total_cont = sum(contenido_counts.values())
                sorted_contenido = sorted(contenido_counts.items(), key=lambda x: x[1], reverse=True)[:6]
                
                for tipo, count in sorted_contenido:
                    pct = count / total_cont * 100
                    icon = content_icons.get(tipo, '📌')
                    bar_width = min(pct * 1.5, 100)
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                            <span style="color: #374151; font-size: 0.9rem;">{icon} {tipo[:40]}</span>
                            <span style="color: #8b5cf6; font-weight: 600;">{pct:.0f}%</span>
                        </div>
                        <div style="background: #f3f4f6; border-radius: 6px; height: 6px;">
                            <div style="background: linear-gradient(90deg, #c084fc, #8b5cf6); width: {bar_width}%; height: 100%; border-radius: 6px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Insight de marketing
    st.markdown("""
    <div class="alert-info" style="margin-top: 20px;">
        <strong>💡 Estrategia recomendada:</strong> El combo ganador para restaurantes en Villahermosa es 
        <strong>Instagram + fotos de platillos + promociones</strong>. TikTok está creciendo rápidamente 
        entre menores de 35 años. El boca a boca sigue siendo crítico - un cliente satisfecho es tu mejor publicidad.
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PÁGINA 7: VOZ DEL CLIENTE
# ============================================================================
elif selected_page == "💬 Voz del Cliente":
    
    st.markdown('<div class="section-title">Escuchando a los comensales</div>', unsafe_allow_html=True)
    st.caption("Insights directos de las encuestas y los focus groups")
    
    # Usar radio buttons con key para mantener estado entre reruns
    tab_options = ["🎯 Oportunidades", "🏷️ Promociones", "💭 Lo que dicen", "😤 Lo que les molesta"]
    selected_tab = st.radio(
        "Sección",
        tab_options,
        horizontal=True,
        key="voz_cliente_tab",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if selected_tab == "🏷️ Promociones":
        st.markdown("### ¿Qué promociones conquistan al comensal?")
        st.caption("Tipos de ofertas que más influyen en la decisión de visitar un restaurante")
        
        col_promos = "16. ¿Qué tipo de promociones te resultan más atractivas al elegir un restaurante?"
        
        if col_promos in df_filtered.columns:
            # Separar respuestas múltiples
            promos_raw = df_filtered[col_promos].dropna().astype(str)
            promos_list = []
            for p in promos_raw:
                promos_list.extend([x.strip() for x in p.split(',') if x.strip()])
            
            promos_counts = Counter(promos_list)
            invalid = ['no responde', 'no respondió', 'no respondio', 'no', 'ninguno', 'na', 'n/a', '1', 'ninguna']
            promos_counts = {k: v for k, v in promos_counts.items() if k.lower() not in invalid and len(k) > 3}
            
            if promos_counts:
                # Iconos y colores por tipo de promoción
                promo_config = {
                    'Descuentos en ciertos días u horarios': ('🗓️', '#3b82f6', 'Happy hour / días especiales'),
                    'Combos o paquetes familiares': ('👨‍👩‍👧‍👦', '#10b981', 'Ideales para familias'),
                    'Promociones de cumpleaños': ('🎂', '#f59e0b', 'Atraen grupos grandes'),
                    '2x1 en bebidas o alimentos': ('🍻', '#ef4444', 'Clásico que nunca falla'),
                    'Puntos o programas de lealtad': ('⭐', '#8b5cf6', 'Fidelización a largo plazo'),
                    'Cupones o descuentos por redes sociales': ('📱', '#e1306c', 'Engagement digital'),
                    'Descuentos por reservaciones anticipadas': ('📅', '#06b6d4', 'Planificación garantizada'),
                    'Ofertas flash (tiempo limitado)': ('⚡', '#f97316', 'Urgencia = acción'),
                }
                
                total_promos = sum(promos_counts.values())
                sorted_promos = sorted(promos_counts.items(), key=lambda x: x[1], reverse=True)
                
                # Dividir en dos columnas
                col_p1, col_p2 = st.columns(2)
                
                # Top 4 en columna izquierda con diseño destacado
                with col_p1:
                    st.markdown("""
                    <div class="glass-card">
                        <h4 style="color: #1f2937; margin-bottom: 15px;">🏆 Las más efectivas</h4>
                    """, unsafe_allow_html=True)
                    
                    for i, (promo, count) in enumerate(sorted_promos[:4]):
                        pct = count / total_promos * 100
                        icon, color, tip = promo_config.get(promo, ('🏷️', '#6b7280', 'Promoción general'))
                        
                        medal = ['🥇', '🥈', '🥉', '4️⃣'][i] if i < 4 else ''
                        
                        st.markdown(f"""
                        <div style="margin-bottom: 14px; padding: 12px; background: {color}10; border-radius: 10px; border-left: 4px solid {color};">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="color: #1f2937; font-weight: 500;">{medal} {icon} {promo[:45]}</span>
                                <span style="color: {color}; font-weight: 700; font-size: 1.2rem;">{pct:.0f}%</span>
                            </div>
                            <div style="color: #6b7280; font-size: 0.75rem; margin-top: 4px;">💡 {tip}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Resto en columna derecha
                with col_p2:
                    st.markdown("""
                    <div class="glass-card">
                        <h4 style="color: #1f2937; margin-bottom: 15px;">📊 También mencionadas</h4>
                    """, unsafe_allow_html=True)
                    
                    for promo, count in sorted_promos[4:8]:
                        pct = count / total_promos * 100
                        icon, color, tip = promo_config.get(promo, ('🏷️', '#6b7280', ''))
                        
                        st.markdown(f"""
                        <div style="margin-bottom: 10px; padding: 10px; background: #f9fafb; border-radius: 8px;">
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: #374151; font-size: 0.9rem;">{icon} {promo[:40]}</span>
                                <span style="color: #6b7280; font-weight: 600;">{pct:.0f}%</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Insight estratégico
                top_promo = sorted_promos[0][0] if sorted_promos else "descuentos"
                st.markdown(f"""
                <div class="alert-success" style="margin-top: 20px;">
                    <strong>🎯 Recomendación estratégica:</strong> La promoción más efectiva es 
                    <strong>"{sorted_promos[0][0]}"</strong> ({sorted_promos[0][1]/total_promos*100:.0f}% de preferencia). 
                    Combínala con <strong>redes sociales</strong> para maximizar alcance. Los <strong>cumpleaños</strong> 
                    son oportunidades de oro: un festejado trae en promedio 6-8 personas.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No hay datos de promociones disponibles.")
    
    elif selected_tab == "🎯 Oportunidades":
        st.markdown("### ¿Qué tipo de restaurante hace falta en la ciudad?")
        st.caption("Analizamos las respuestas abiertas para encontrar necesidades no cubiertas")
        
        col_falta = "11. ¿Qué tipo de restaurante o experiencia consideras que hacen falta o están poco desarrollados en Villahermosa?"
        
        if col_falta in df_filtered.columns:
            resp = df_filtered[col_falta].dropna()
            resp = resp[~resp.isin(['1', 'No responde', 'No Respondió', 'No Respondio', 'No sé', 'Ninguno', 'ninguno', 'no', 'No', 'Nada'])]
            
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
        invalid_responses = ["no responde", "no respondió", "no respondio", "ninguno", "no", "x", ".", "-", "1", "na", "n/a", "nada", "ninguna"]
        
        df_comments = df_filtered[[col_comentarios, col_edad]].copy()
        df_comments = df_comments.dropna(subset=[col_comentarios])
        df_comments[col_comentarios] = df_comments[col_comentarios].astype(str)
        df_comments = df_comments[~df_comments[col_comentarios].str.lower().str.strip().isin(invalid_responses)]
        df_comments = df_comments[df_comments[col_comentarios].str.len() > 25]
        
        if len(df_comments) > 0:
            # ===== NUEVO: Análisis temático de comentarios =====
            st.markdown("#### 📊 Temas principales en los comentarios")
            
            # Categorizar comentarios por tema
            tema_keywords = {
                '👨‍🍳 Servicio y atención': ['servicio', 'atención', 'mesero', 'amable', 'trato', 'personal', 'rapidez', 'lento'],
                '💰 Relación precio-calidad': ['precio', 'caro', 'económico', 'vale', 'barato', 'costoso', 'pagar'],
                '🍽️ Calidad de comida': ['comida', 'sabor', 'fresco', 'delicioso', 'rico', 'porción', 'platillo', 'menú'],
                '📍 Variedad y opciones': ['variedad', 'opciones', 'falta', 'diferentes', 'más', 'nuevo', 'propuesta'],
                '🏠 Ambiente y espacio': ['ambiente', 'lugar', 'espacio', 'limpio', 'bonito', 'agradable', 'ruido'],
            }
            
            tema_counts = Counter()
            for comment in df_comments[col_comentarios]:
                comment_lower = comment.lower()
                for tema, keywords in tema_keywords.items():
                    if any(kw in comment_lower for kw in keywords):
                        tema_counts[tema] += 1
            
            if tema_counts:
                total_temas = sum(tema_counts.values())
                cols_temas = st.columns(min(5, len(tema_counts)))
                
                for i, (tema, count) in enumerate(tema_counts.most_common(5)):
                    with cols_temas[i]:
                        pct = count / len(df_comments) * 100
                        st.markdown(f"""
                        <div style="text-align: center; padding: 10px; background: #f9fafb; border-radius: 10px;">
                            <div style="font-size: 1.5rem;">{tema.split()[0]}</div>
                            <div style="color: #1f2937; font-size: 0.8rem; font-weight: 500;">{tema.split(' ', 1)[1]}</div>
                            <div style="color: #db2777; font-weight: 700; font-size: 1.1rem;">{pct:.0f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 💬 Citas textuales")
            
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
                if item and item not in ["No responde", "No Respondió", "No Respondio"]:
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
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="color: #1f2937;">📋 Encuestas completas</h4>
                <p style="color: #6b7280; font-size: 0.9rem;">
                    {len(df_encuestas)} respuestas · {len(df_encuestas.columns)} variables<br>
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
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="color: #1f2937;">🌐 Base Google Maps</h4>
                <p style="color: #6b7280; font-size: 0.9rem;">
                    {len(df_gmb):,} restaurantes mapeados<br>
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
