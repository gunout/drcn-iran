# dashboard_iran_complet.py
# Fusion des dashboards : Défense, Rial, Communes, Nucléaire
# Version constructive avec analyse géopolitique objective

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import json
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Iran - Analyse Intégrée",
    page_icon="🇮🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# STYLE CSS PERSONNALISÉ (fusion des styles des 4 dashboards)
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&family=Scheherazade:wght@400;700&display=swap');
    
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #239F40 0%, #FFFFFF 50%, #DA0000 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-family: 'Roboto', sans-serif;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .persian-header {
        font-family: 'Scheherazade', serif;
        font-size: 1.8rem;
        direction: rtl;
        text-align: center;
        color: #333;
        margin-bottom: 1rem;
    }
    
    .section-header {
        color: #1e3c72;
        border-bottom: 3px solid #239F40;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 5px solid #239F40;
        margin: 0.5rem 0;
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1e3c72;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.3rem;
    }
    
    .badge-iran {
        background-color: #239F40;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .badge-sanction {
        background-color: #DA0000;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .badge-oil {
        background-color: #FF6B35;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .badge-nuclear {
        background-color: #FFA500;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
        animation: pulse 2s infinite;
    }
    
    .badge-iaea {
        background-color: #2196f3;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .info-box {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .diplomacy-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .humanitarian-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1e3c72 !important;
        color: white !important;
    }
    
    .timezone-badge {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    
    .source-note {
        font-size: 0.8rem;
        color: #666;
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALISATION DES VARIABLES DE SESSION
# ============================================================================
def init_session_state():
    """Initialise toutes les variables de session des 4 dashboards"""
    
    # Dashboard Défense
    if 'selected_branch' not in st.session_state:
        st.session_state.selected_branch = "Forces Armées de la RII"
    if 'show_geopolitical' not in st.session_state:
        st.session_state.show_geopolitical = True
    if 'show_doctrinal' not in st.session_state:
        st.session_state.show_doctrinal = True
    
    # Dashboard Rial
    if 'price_alerts' not in st.session_state:
        st.session_state.price_alerts = []
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {}
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = ['USDIRR', 'EURIRR', 'GBPIRR', 'AEDIRR']
    if 'email_config' not in st.session_state:
        st.session_state.email_config = {'enabled': False}
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = True
    
    # Dashboard Communes
    if 'selected_commune' not in st.session_state:
        st.session_state.selected_commune = "Téhéran"
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False
    if 'comparison_communes' not in st.session_state:
        st.session_state.comparison_communes = []
    if 'show_euro_conversion' not in st.session_state:
        st.session_state.show_euro_conversion = True
    if 'show_toman' not in st.session_state:
        st.session_state.show_toman = True
    
    # Dashboard Nucléaire
    if 'selected_facility' not in st.session_state:
        st.session_state.selected_facility = "Isfahan"
    if 'show_weapons_grade' not in st.session_state:
        st.session_state.show_weapons_grade = True

init_session_state()

# ============================================================================
# DONNÉES PARTAGÉES ET CONSTANTES
# ============================================================================

# Taux de change
EUR_TO_IRR = 50000  # Taux officiel approximatif

# Liste des communes iraniennes
IRAN_CITIES = [
    "Téhéran", "Mashhad", "Ispahan", "Karaj", "Tabriz", "Chiraz", "Qom",
    "Ahvaz", "Kerman", "Orumiyeh", "Rasht", "Yazd", "Ardabil", "Zahedan",
    "Kermanshah", "Hamadan", "Bandar Abbas", "Arak", "Eslamshahr"
]

# Données nucléaires AIEA (février 2026)
NUCLEAR_DATA = {
    "report_date": "2026-02-27",
    "uranium_60_percent": 440.9,  # kg
    "uranium_total": 9247.6,  # kg
    "weapons_potential": 10,
    "breakout_time": 15,  # jours
    "last_inspection": "2025-06-10",
    "facilities": {
        "Isfahan": {"status": "Actif - Stockage", "access": "Non autorisé", "lat": 32.65, "lon": 51.68},
        "Natanz": {"status": "Activité observée", "access": "Non autorisé", "lat": 33.72, "lon": 51.72},
        "Fordow": {"status": "Actif", "access": "Non autorisé", "lat": 34.88, "lon": 50.99},
        "Arak": {"status": "Fonctionnement limité", "access": "Partiel", "lat": 34.37, "lon": 49.24},
        "Bushehr": {"status": "Opérationnel", "access": "Autorisé", "lat": 28.83, "lon": 50.89}
    }
}

# Données de change (démonstration)
CURRENCY_DATA = {
    'USDIRR': {'name': 'Dollar US', 'official': 1311134, 'free': 1749500},
    'EURIRR': {'name': 'Euro', 'official': 1549954, 'free': 2067500},
    'GBPIRR': {'name': 'Livre Sterling', 'official': 1764178, 'free': 2353500},
    'AEDIRR': {'name': 'Dirham UAE', 'official': 357014, 'free': 476000},
}

# Événements diplomatiques
DIPLOMATIC_EVENTS = [
    {"date": "2015-07-14", "event": "Signature JCPOA", "type": "accord"},
    {"date": "2018-05-08", "event": "Retrait US du JCPOA", "type": "crise"},
    {"date": "2021-04-01", "event": "Début enrichissement 60%", "type": "escalade"},
    {"date": "2025-06-15", "event": "Frappes sur sites nucléaires", "type": "attaque"},
    {"date": "2026-02-27", "event": "Rapport AIEA - Accès limité", "type": "rapport"},
    {"date": "2026-03-02", "event": "Négociations prévues à Vienne", "type": "diplomatie"}
]

# ============================================================================
# CLASSES PRINCIPALES (adaptées des 4 dashboards)
# ============================================================================

class IranDefenseAnalyzer:
    """Analyse des capacités de défense (adapté de Dashboard(3).py)"""
    
    def __init__(self):
        self.branches = [
            "Forces Armées", "Armée de Terre", "Marine", 
            "Force Aérienne", "IRGC", "Forces Quds", "Basij"
        ]
        self.missile_systems = {
            "Shahab-3": {"portee": 2000, "statut": "Opérationnel"},
            "Ghadr": {"portee": 1600, "statut": "Opérationnel"},
            "Emad": {"portee": 1700, "statut": "Opérationnel"},
            "Fateh-110": {"portee": 300, "statut": "Opérationnel"}
        }
    
    def generate_indicators(self):
        """Génère des indicateurs de défense simulés"""
        return {
            'budget_mds': 18.5,
            'personnel_k': 610,
            'missile_stock': 1200,
            'readiness': 82.5,
            'mobilization_days': 12
        }

class IranEconomyAnalyzer:
    """Analyse économique et monétaire (adapté de Dashboard(2).py)"""
    
    def __init__(self):
        self.inflation_rate = 42.2
        self.gdp_growth = -1.7
        self.oil_revenue = 23  # milliards $
        self.reserves = 25  # milliards $
    
    def get_currency_rate(self, pair='USDIRR', market='free'):
        """Retourne un taux de change simulé"""
        base_rates = {
            'USDIRR': {'official': 1311134, 'free': 1749500, 'nima': 1403083},
            'EURIRR': {'official': 1549954, 'free': 2067500, 'nima': 1658651}
        }
        return base_rates.get(pair, base_rates['USDIRR']).get(market, 1749500)
    
    def generate_inflation_history(self):
        """Génère l'historique de l'inflation"""
        dates = pd.date_range(start='2020-01-01', end='2026-02-01', freq='M')
        values = [20 + i*1.5 + np.random.normal(0, 2) for i in range(len(dates))]
        return pd.DataFrame({'date': dates, 'inflation': values})

class IranCityAnalyzer:
    """Analyse des finances municipales (adapté de Dashboard(1).py)"""
    
    def __init__(self, city_name="Téhéran"):
        self.city = city_name
        self.city_config = self._get_config(city_name)
    
    def _get_config(self, city):
        """Configuration spécifique à chaque ville"""
        configs = {
            "Téhéran": {"population": 8500000, "budget": 120, "type": "capitale"},
            "Mashhad": {"population": 3200000, "budget": 45, "type": "religieuse"},
            "Ispahan": {"population": 2200000, "budget": 38, "type": "culturelle"},
            "default": {"population": 500000, "budget": 10, "type": "locale"}
        }
        return configs.get(city, configs["default"])
    
    def generate_budget_data(self):
        """Génère des données budgétaires simulées"""
        years = list(range(2015, 2026))
        data = []
        for year in years:
            growth = 1 + (year - 2015) * 0.02 + np.random.normal(0, 0.05)
            data.append({
                'annee': year,
                'recettes': self.city_config['budget'] * growth * 1e9,
                'depenses': self.city_config['budget'] * growth * 1.05 * 1e9,
                'population': self.city_config['population'] * (1 + (year-2015)*0.015)
            })
        return pd.DataFrame(data)

class IranNuclearAnalyzer:
    """Analyse du programme nucléaire (adapté de Dashboard.py)"""
    
    def __init__(self):
        self.latest_data = NUCLEAR_DATA
    
    def generate_enrichment_history(self):
        """Génère l'historique de l'enrichissement"""
        dates = pd.date_range(start='2015-01-01', end='2026-02-01', freq='6M')
        stocks = [0, 0, 0, 0, 100, 300, 800, 1500, 2500, 4000, 6000, 8000, 9247.6]
        levels = [3.67, 3.67, 3.67, 3.67, 4.5, 4.5, 20, 20, 60, 60, 60, 60, 60]
        
        # Ajuster les longueurs
        min_len = min(len(dates), len(stocks), len(levels))
        return pd.DataFrame({
            'date': dates[:min_len],
            'stock': stocks[:min_len],
            'level': levels[:min_len]
        })
    
    def get_threat_level(self, percentage=60):
        """Détermine le niveau de menace"""
        if percentage >= 90:
            return "CRITIQUE", "🔴"
        elif percentage >= 60:
            return "ÉLEVÉ", "🟠"
        elif percentage >= 20:
            return "MODÉRÉ", "🟡"
        else:
            return "FAIBLE", "🟢"

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def format_rial(value, include_toman=True):
    """Formate une valeur en Rial"""
    if value is None or value == 0:
        return "N/A"
    
    if value >= 1e9:
        result = f"{value/1e9:.2f} milliards Rial"
    elif value >= 1e6:
        result = f"{value/1e6:.2f} millions Rial"
    else:
        result = f"{value:,.0f} Rial"
    
    if include_toman and value >= 10:
        toman = value / 10
        if toman >= 1e9:
            result += f" ({toman/1e9:.2f} Md Toman)"
        elif toman >= 1e6:
            result += f" ({toman/1e6:.2f} M Toman)"
        else:
            result += f" ({toman:,.0f} Toman)"
    
    return result

def format_euro(value, rate=EUR_TO_IRR):
    """Convertit des Rials en Euros"""
    if value is None or value == 0:
        return "N/A"
    euros = value / rate
    if euros >= 1e9:
        return f"{euros/1e9:.2f} Md€"
    elif euros >= 1e6:
        return f"{euros/1e6:.2f} M€"
    else:
        return f"{euros:,.0f} €"

def get_market_status():
    """Statut du marché des changes iranien"""
    now = datetime.now()
    # Simulation simple
    if now.weekday() >= 4:  # Jeudi ou Vendredi
        return "Fermé (week-end)", "🔴"
    elif 9 <= now.hour < 16:
        return "Ouvert", "🟢"
    else:
        return "Fermé", "🔴"

def get_city_emoji(city):
    """Emoji représentatif d'une ville"""
    emojis = {
        "Téhéran": "🏛️", "Mashhad": "🕌", "Ispahan": "🎨", "Chiraz": "🌸",
        "Qom": "📿", "Ahvaz": "🛢️", "Yazd": "🏜️", "default": "🏙️"
    }
    return emojis.get(city, emojis["default"])

# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================

# En-tête
st.markdown('<h1 class="main-header">🇮🇷 IRAN - ANALYSE INTÉGRÉE</h1>', unsafe_allow_html=True)
st.markdown('<p class="persian-header">تحلیل جامع ایران: دفاع، اقتصاد، هسته‌ای و شهرداری‌ها</p>', unsafe_allow_html=True)

# Badges contextuels
col_badges = st.columns(6)
with col_badges[0]:
    threat_level, threat_icon = IranNuclearAnalyzer().get_threat_level(60)
    st.markdown(f"<span class='badge-nuclear'>{threat_icon} Nucléaire: {threat_level}</span>", unsafe_allow_html=True)
with col_badges[1]:
    st.markdown("<span class='badge-sanction'>⚠️ Sous Sanctions</span>", unsafe_allow_html=True)
with col_badges[2]:
    st.markdown("<span class='badge-oil'>🛢️ OPEC</span>", unsafe_allow_html=True)
with col_badges[3]:
    st.markdown(f"<span class='badge-iran'>📈 Inflation: 42.2%</span>", unsafe_allow_html=True)
with col_badges[4]:
    st.markdown(f"<span class='badge-iaea'>📋 Dernier rapport: 27/02/26</span>", unsafe_allow_html=True)
with col_badges[5]:
    st.markdown(f"<span class='badge-iran'>💵 USD/IRR: 1.75M</span>", unsafe_allow_html=True)

# Barre d'information temporelle
market_status, market_icon = get_market_status()
st.markdown(f"""
<div class='timezone-badge'>
    <b>🕐 Informations temps réel:</b> 🇫🇷 Paris: {datetime.now().strftime('%H:%M:%S')} | 
    🇮🇷 Téhéran: {datetime.now().strftime('%H:%M:%S')} (UTC+3:30) | 
    📊 Marché: {market_icon} {market_status}
</div>
""", unsafe_allow_html=True)

# ============================================================================
# BARRE LATÉRALE DE NAVIGATION
# ============================================================================

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/ca/Flag_of_Iran.svg", width=80)
    st.markdown("## 🎛️ PANEL DE NAVIGATION")
    
    # Menu principal
    main_section = st.radio(
        "Section principale:",
        ["📊 Vue d'ensemble intégrée",
         "🛡️ Défense & Stratégie",
         "💵 Économie & Monnaie",
         "🏙️ Communes & Finances locales",
         "☢️ Programme nucléaire",
         "🕊️ Diplomatie & Paix",
         "📉 Analyse humanitaire"]
    )
    
    st.markdown("---")
    
    # Sous-menu contextuel (change selon la section)
    if main_section == "🛡️ Défense & Stratégie":
        st.markdown("### ⚙️ Options Défense")
        st.session_state.show_geopolitical = st.checkbox("Contexte géopolitique", value=True)
        st.session_state.show_doctrinal = st.checkbox("Analyse doctrinale", value=True)
        
    elif main_section == "💵 Économie & Monnaie":
        st.markdown("### ⚙️ Options Économie")
        st.session_state.show_euro_conversion = st.checkbox("Conversion en Euro", value=True)
        st.session_state.show_toman = st.checkbox("Conversion en Toman", value=True)
        
    elif main_section == "🏙️ Communes & Finances locales":
        st.markdown("### ⚙️ Options Communes")
        selected_city = st.selectbox("Commune principale", IRAN_CITIES, index=0)
        st.session_state.selected_commune = selected_city
        
        comparison = st.checkbox("Mode comparaison")
        if comparison:
            cities_comp = st.multiselect("Comparer avec", IRAN_CITIES, 
                                        default=["Mashhad", "Ispahan"][:2])
            st.session_state.comparison_mode = True
            st.session_state.comparison_communes = cities_comp
        else:
            st.session_state.comparison_mode = False
            
    elif main_section == "☢️ Programme nucléaire":
        st.markdown("### ⚙️ Options Nucléaire")
        facilities = list(NUCLEAR_DATA["facilities"].keys())
        st.session_state.selected_facility = st.selectbox("Site à surveiller", facilities)
        st.session_state.show_weapons_grade = st.checkbox("Afficher seuil 90%", value=True)
        
        st.markdown("### 📋 Dernier rapport AIEA")
        st.info(f"**Date:** {NUCLEAR_DATA['report_date']}\n\n"
                f"**Uranium 60%:** {NUCLEAR_DATA['uranium_60_percent']} kg\n\n"
                f"**Bombes potentielles:** {NUCLEAR_DATA['weapons_potential']}")
    
    st.markdown("---")
    st.caption("Sources: AIEA, Banque Centrale d'Iran, SIPRI, ONU")
    st.caption("Données simulées / mises à jour: mars 2026")

# ============================================================================
# SECTION 1: VUE D'ENSEMBLE INTÉGRÉE
# ============================================================================

if main_section == "📊 Vue d'ensemble intégrée":
    st.markdown('<h2 class="section-header">📊 TABLEAU DE BORD INTÉGRÉ - INDICATEURS CLÉS</h2>', 
                unsafe_allow_html=True)
    
    # Initialisation des analyseurs
    defense = IranDefenseAnalyzer()
    economy = IranEconomyAnalyzer()
    nuclear = IranNuclearAnalyzer()
    
    # Indicateurs principaux sur 4 colonnes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        def_indicators = defense.generate_indicators()
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>{:.1f} Md$</div>
            <div class='metric-label'>Budget Défense</div>
            <p style='font-size:0.8rem;'>{}K personnel · {} missiles</p>
        </div>
        """.format(def_indicators['budget_mds'], 
                   def_indicators['personnel_k'],
                   def_indicators['missile_stock']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>1 USD = {:.0f}</div>
            <div class='metric-label'>Taux de change (marché libre)</div>
            <p style='font-size:0.8rem;'>Officiel: 1,311,134 · NIMA: 1,403,083</p>
        </div>
        """.format(CURRENCY_DATA['USDIRR']['free']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>{:.1f} kg</div>
            <div class='metric-label'>Uranium enrichi à 60%</div>
            <p style='font-size:0.8rem;'>{} bombes potentielles · Breakout: {}j</p>
        </div>
        """.format(NUCLEAR_DATA['uranium_60_percent'],
                   NUCLEAR_DATA['weapons_potential'],
                   NUCLEAR_DATA['breakout_time']), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>{:.1f}%</div>
            <div class='metric-label'>Inflation annuelle</div>
            <p style='font-size:0.8rem;'>PIB 2025: -1.7% · Réserves: {} Md$</p>
        </div>
        """.format(economy.inflation_rate, economy.reserves), unsafe_allow_html=True)
    
    # Graphiques intégrés
    st.markdown("### 📈 Évolution comparée des indicateurs")
    
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        # Évolution du taux de change et de l'inflation
        dates = pd.date_range(start='2020-01-01', end='2026-02-01', freq='Q')
        usd_rates = [150000 + i*40000 + np.random.normal(0, 10000) for i in range(len(dates))]
        inflation = [20 + i*1.2 + np.random.normal(0, 2) for i in range(len(dates))]
        
        fig_eco = make_subplots(specs=[[{"secondary_y": True}]])
        fig_eco.add_trace(go.Scatter(x=dates, y=usd_rates, name="USD/IRR", 
                                     line=dict(color='#DA0000', width=2)), secondary_y=False)
        fig_eco.add_trace(go.Scatter(x=dates, y=inflation, name="Inflation %", 
                                     line=dict(color='#FFA500', width=2, dash='dash')), secondary_y=True)
        fig_eco.update_layout(title="Taux de change USD/IRR et Inflation", height=350)
        st.plotly_chart(fig_eco, use_container_width=True)
    
    with col_graph2:
        # Stock d'uranium enrichi
        nuc_hist = nuclear.generate_enrichment_history()
        fig_nuc = go.Figure()
        fig_nuc.add_trace(go.Scatter(x=nuc_hist['date'], y=nuc_hist['stock'],
                                     fill='tozeroy', name="Stock (kg)", line=dict(color='#FFA500', width=3)))
        fig_nuc.add_hline(y=42, line_dash="dash", line_color="#DA0000", 
                         annotation_text="Seuil 1 bombe")
        fig_nuc.update_layout(title="Stock d'uranium enrichi (kg)", height=350)
        st.plotly_chart(fig_nuc, use_container_width=True)
    
    # Chronologie des événements
    st.markdown("### 📅 Chronologie des événements majeurs")
    
    df_events = pd.DataFrame(DIPLOMATIC_EVENTS)
    fig_timeline = go.Figure()
    
    colors = {'accord': '#239F40', 'crise': '#FFA500', 'escalade': '#DA0000',
              'attaque': '#DA0000', 'rapport': '#2196f3', 'diplomatie': '#239F40'}
    
    for i, row in df_events.iterrows():
        fig_timeline.add_trace(go.Scatter(
            x=[row['date']], y=[1],
            mode='markers+text',
            marker=dict(size=15, color=colors.get(row['type'], '#666')),
            text=row['event'],
            textposition="top center",
            showlegend=False
        ))
    
    fig_timeline.update_layout(
        xaxis_title="Date",
        yaxis=dict(showticklabels=False, showgrid=False, range=[0.5, 1.5]),
        height=200,
        hovermode='x'
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

# ============================================================================
# SECTION 2: DÉFENSE & STRATÉGIE
# ============================================================================

elif main_section == "🛡️ Défense & Stratégie":
    st.markdown('<h2 class="section-header">🛡️ ANALYSE DES CAPACITÉS DE DÉFENSE</h2>', 
                unsafe_allow_html=True)
    
    defense = IranDefenseAnalyzer()
    
    col_def1, col_def2, col_def3 = st.columns(3)
    
    with col_def1:
        st.markdown("### 🚀 Missiles balistiques")
        missile_df = pd.DataFrame([
            {"Système": k, "Portée (km)": v["portee"], "Statut": v["statut"]}
            for k, v in defense.missile_systems.items()
        ])
        st.dataframe(missile_df, hide_index=True, use_container_width=True)
    
    with col_def2:
        st.markdown("### 👥 Effectifs militaires")
        personnel_data = {
            "Force": ["Armée de Terre", "Marine", "Force Aérienne", "IRGC", "Basij", "Total"],
            "Effectifs": [350000, 18000, 37000, 125000, 90000, 620000]
        }
        st.dataframe(pd.DataFrame(personnel_data), hide_index=True, use_container_width=True)
    
    with col_def3:
        st.markdown("### 📊 Indicateurs opérationnels")
        indicators = defense.generate_indicators()
        st.metric("Préparation opérationnelle", f"{indicators['readiness']}%")
        st.metric("Temps de mobilisation", f"{indicators['mobilization_days']} jours")
        st.metric("Exercices annuels", "45-60")
    
    # Doctrine militaire (constructive)
    if st.session_state.show_doctrinal:
        st.markdown("### 📚 Doctrine et stratégie")
        col_doc1, col_doc2 = st.columns(2)
        
        with col_doc1:
            st.markdown("""
            <div class='info-box'>
                <b>Doctrine officielle:</b> Défense nationale et dissuasion asymétrique.
                L'Iran met l'accent sur la défense territoriale et la capacité de 
                représailles en cas d'attaque.
            </div>
            """, unsafe_allow_html=True)
        
        with col_doc2:
            st.markdown("""
            <div class='diplomacy-box'>
                <b>Coopération internationale:</b> L'Iran participe à des exercices 
                navals avec la Russie et la Chine. Membre de l'Organisation de 
                Coopération de Shanghai (OCS).
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# SECTION 3: ÉCONOMIE & MONNAIE
# ============================================================================

elif main_section == "💵 Économie & Monnaie":
    st.markdown('<h2 class="section-header">💵 ANALYSE ÉCONOMIQUE ET MONÉTAIRE</h2>', 
                unsafe_allow_html=True)
    
    economy = IranEconomyAnalyzer()
    
    # Taux de change multiples
    st.markdown("### 💱 Taux de change du Rial (IRR)")
    
    col_curr1, col_curr2, col_curr3 = st.columns(3)
    
    with col_curr1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>1 USD</div>
            <div class='metric-label'>Taux officiel CBI</div>
            <p style='font-size:1.2rem;'>{:,} IRR</p>
        </div>
        """.format(CURRENCY_DATA['USDIRR']['official']), unsafe_allow_html=True)
    
    with col_curr2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>1 USD</div>
            <div class='metric-label'>Taux NIMA (commerce)</div>
            <p style='font-size:1.2rem;'>{:,} IRR</p>
        </div>
        """.format(1403083), unsafe_allow_html=True)
    
    with col_curr3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>1 USD</div>
            <div class='metric-label'>Marché libre</div>
            <p style='font-size:1.2rem;'>{:,} IRR</p>
        </div>
        """.format(CURRENCY_DATA['USDIRR']['free']), unsafe_allow_html=True)
    
    # Indicateurs macroéconomiques
    col_macro1, col_macro2 = st.columns(2)
    
    with col_macro1:
        st.markdown("### 📊 Indicateurs macroéconomiques")
        macro_data = {
            "Indicateur": ["PIB (estimé)", "Croissance PIB 2025", "Inflation", "Réserves de change", 
                          "Revenus pétroliers", "Dette publique (% PIB)"],
            "Valeur": ["~400 Mds $", "-1.7%", "42.2%", "~25 Mds $", "~23 Mds $", "~45%"]
        }
        st.dataframe(pd.DataFrame(macro_data), hide_index=True, use_container_width=True)
    
    with col_macro2:
        st.markdown("### 📈 Évolution de l'inflation")
        hist_inf = economy.generate_inflation_history()
        fig_inf = px.line(hist_inf.tail(24), x='date', y='inflation', 
                         title="Inflation mensuelle (derniers 24 mois)")
        fig_inf.add_hline(y=40, line_dash="dash", line_color="#DA0000")
        st.plotly_chart(fig_inf, use_container_width=True)
    
    # Impact social
    st.markdown("### 👥 Impact social de l'inflation")
    col_soc1, col_soc2 = st.columns(2)
    
    with col_soc1:
        st.markdown("""
        <div class='humanitarian-box'>
            <b>Pouvoir d'achat (simulation):</b><br>
            • Salaire minimum: 45,000,000 IRR (≈ 900 €)<br>
            • Prix du pain (1kg): 90,000 IRR<br>
            • Prix de l'essence: 18,000 IRR/litre<br>
            • Loyer moyen (Téhéran): 250,000,000 IRR/mois
        </div>
        """, unsafe_allow_html=True)
    
    with col_soc2:
        st.markdown("""
        <div class='warning-box'>
            <b>Programmes de soutien:</b><br>
            • Subventions alimentaires pour 60M de personnes<br>
            • Carte électronique pour produits de base<br>
            • Allocation mensuelle (environ 500,000 IRR/personne)
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# SECTION 4: COMMUNES & FINANCES LOCALES
# ============================================================================

elif main_section == "🏙️ Communes & Finances locales":
    st.markdown('<h2 class="section-header">🏙️ ANALYSE DES FINANCES MUNICIPALES</h2>', 
                unsafe_allow_html=True)
    
    if not st.session_state.comparison_mode:
        # Mode commune unique
        city = st.session_state.selected_commune
        analyzer = IranCityAnalyzer(city)
        data = analyzer.generate_budget_data()
        
        col_city1, col_city2, col_city3, col_city4 = st.columns(4)
        
        with col_city1:
            st.markdown(f"### {get_city_emoji(city)} {city}")
            st.markdown(f"**Type:** {analyzer.city_config['type']}")
        
        with col_city2:
            st.metric("Population 2025", f"{data['population'].iloc[-1]:,.0f}")
        
        with col_city3:
            recettes = data['recettes'].iloc[-1]
            st.metric("Budget annuel", format_rial(recettes))
        
        with col_city4:
            if st.session_state.show_euro_conversion:
                st.metric("en Euro", format_euro(recettes))
        
        # Graphique budget
        fig_budget = go.Figure()
        fig_budget.add_trace(go.Bar(x=data['annee'], y=data['recettes']/1e9, 
                                     name="Recettes", marker_color='#239F40'))
        fig_budget.add_trace(go.Bar(x=data['annee'], y=data['depenses']/1e9, 
                                     name="Dépenses", marker_color='#DA0000'))
        fig_budget.update_layout(title="Évolution budgétaire (milliards Rials)", height=400)
        st.plotly_chart(fig_budget, use_container_width=True)
    
    else:
        # Mode comparaison
        st.markdown("### 🔄 Comparaison des communes")
        
        comparison_data = []
        for city in st.session_state.comparison_communes:
            analyzer = IranCityAnalyzer(city)
            data = analyzer.generate_budget_data()
            last = data.iloc[-1]
            comparison_data.append({
                "Commune": city,
                "Population": f"{last['population']:,.0f}",
                "Budget (Rials)": format_rial(last['recettes'], False),
                "Budget/hab (Rials)": f"{last['recettes']/last['population']:,.0f}"
            })
        
        st.dataframe(pd.DataFrame(comparison_data), hide_index=True, use_container_width=True)
        
        # Graphique comparatif
        fig_comp = go.Figure()
        for city in st.session_state.comparison_communes:
            analyzer = IranCityAnalyzer(city)
            data = analyzer.generate_budget_data()
            fig_comp.add_trace(go.Scatter(x=data['annee'], y=data['recettes']/1e9,
                                          name=city, mode='lines+markers'))
        fig_comp.update_layout(title="Comparaison des budgets municipaux", height=400)
        st.plotly_chart(fig_comp, use_container_width=True)

# ============================================================================
# SECTION 5: PROGRAMME NUCLÉAIRE
# ============================================================================

elif main_section == "☢️ Programme nucléaire":
    st.markdown('<h2 class="section-header">☢️ ANALYSE DU PROGRAMME NUCLÉAIRE</h2>', 
                unsafe_allow_html=True)
    
    nuclear = IranNuclearAnalyzer()
    
    # Alerte si nécessaire
    days_since = (datetime.now() - datetime(2025, 6, 10)).days
    st.markdown(f"""
    <div class='warning-box'>
        <b>⚠️ Alerte AIEA:</b> {days_since} jours sans inspection complète des sites.
        L'agence ne peut pas vérifier la localisation ni la composition exacte du stock d'uranium.
    </div>
    """, unsafe_allow_html=True)
    
    col_nuc1, col_nuc2 = st.columns(2)
    
    with col_nuc1:
        st.markdown("### 📊 Stock d'uranium enrichi")
        hist = nuclear.generate_enrichment_history()
        fig_stock = go.Figure()
        fig_stock.add_trace(go.Scatter(x=hist['date'], y=hist['stock'],
                                       fill='tozeroy', name="Stock (kg)",
                                       line=dict(color='#FFA500', width=3)))
        fig_stock.add_hline(y=42, line_dash="dash", line_color="#DA0000",
                           annotation_text="Seuil 1 bombe")
        fig_stock.add_hline(y=440.9, line_dash="dash", line_color="#FFA500",
                           annotation_text="Stock 60% actuel")
        st.plotly_chart(fig_stock, use_container_width=True)
    
    with col_nuc2:
        st.markdown("### 🏭 Sites nucléaires")
        facilities_df = pd.DataFrame([
            {"Site": k, "Statut": v["status"], "Accès AIEA": v["access"]}
            for k, v in NUCLEAR_DATA["facilities"].items()
        ])
        st.dataframe(facilities_df, hide_index=True, use_container_width=True)
        
        # Site sélectionné
        site = st.session_state.selected_facility
        st.markdown(f"**Détails {site}:** {NUCLEAR_DATA['facilities'][site]['status']}")
    
    # Niveaux d'enrichissement
    st.markdown("### ⚗️ Niveaux d'enrichissement")
    col_levels = st.columns(4)
    
    with col_levels[0]:
        st.markdown("""
        <div style='background:#239F40; color:white; padding:1rem; border-radius:5px; text-align:center'>
            <h3>3.67%</h3>
            <p>Limite JCPOA</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_levels[1]:
        st.markdown("""
        <div style='background:#FFA500; color:white; padding:1rem; border-radius:5px; text-align:center'>
            <h3>20%</h3>
            <p>Atteint en 2021</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_levels[2]:
        st.markdown("""
        <div style='background:#DA0000; color:white; padding:1rem; border-radius:5px; text-align:center'>
            <h3>60%</h3>
            <p>Atteint (440.9 kg)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_levels[3]:
        st.markdown("""
        <div style='background:#666; color:white; padding:1rem; border-radius:5px; text-align:center'>
            <h3>90%</h3>
            <p>Seuil militaire</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# SECTION 6: DIPLOMATIE & PAIX
# ============================================================================

elif main_section == "🕊️ Diplomatie & Paix":
    st.markdown('<h2 class="section-header">🕊️ CADRE DIPLOMATIQUE ET RÉSOLUTION DE CONFLIT</h2>', 
                unsafe_allow_html=True)
    
    col_dip1, col_dip2 = st.columns(2)
    
    with col_dip1:
        st.markdown("""
        <div class='diplomacy-box'>
            <h4>📜 Initiatives diplomatiques en cours</h4>
            <p><strong>Négociations nucléaires:</strong> Cycles de discussions indirectes 
            États-Unis-Iran à Oman et en Suisse (2025-2026).</p>
            <p><strong>Médiateurs:</strong> Oman, Qatar, Union Européenne, Suisse.</p>
            <p><strong>Prochaine réunion:</strong> 2 mars 2026 à Vienne (Iran-AIEA).</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-box'>
            <h4>⚖️ Principes du droit international</h4>
            <ul>
                <li><strong>Charte des Nations Unies (Art. 2.4):</strong> Interdiction de la menace ou de l'emploi de la force.</li>
                <li><strong>Traité de non-prolifération (TNP):</strong> Droit à l'énergie nucléaire civile en échange de la non-prolifération.</li>
                <li><strong>Résolutions du Conseil de Sécurité:</strong> Exigences de coopération avec l'AIEA.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_dip2:
        st.markdown("""
        <div class='diplomacy-box'>
            <h4>🤝 Pistes de désescalade</h4>
            <ol>
                <li><strong>Mesures de confiance:</strong> Échanges d'informations, hotline militaire, notifications d'exercices.</li>
                <li><strong>Cadre régional de dialogue:</strong> Forum de coopération pour la sécurité du Golfe.</li>
                <li><strong>Retour au JCPOA:</strong> Accord nucléaire contre levée des sanctions, élargi aux questions régionales.</li>
                <li><strong>Garanties internationales:</strong> Engagement des puissances mondiales sur la sécurité de l'Iran.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='warning-box'>
            <h4>📊 Simulation: Impact économique de la paix</h4>
            <p><em>Scénario hypothétique de levée des sanctions:</em></p>
        """, unsafe_allow_html=True)
        
        # Simulation simple
        pib_actuel = 400
        croissance_paix = 5.0
        pib_5ans = pib_actuel * (1 + croissance_paix/100) ** 5
        
        st.metric("PIB actuel", f"{pib_actuel} Mds $")
        st.metric("PIB potentiel (5 ans)", f"{pib_5ans:.0f} Mds $", 
                 delta=f"+{pib_5ans-pib_actuel:.0f} Mds $")
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# SECTION 7: ANALYSE HUMANITAIRE
# ============================================================================

elif main_section == "📉 Analyse humanitaire":
    st.markdown('<h2 class="section-header">📉 ANALYSE DES COÛTS HUMAINS ET SOCIAUX</h2>', 
                unsafe_allow_html=True)
    
    col_hum1, col_hum2 = st.columns(2)
    
    with col_hum1:
        st.markdown("""
        <div class='humanitarian-box'>
            <h4>💔 Impact des sanctions sur la population</h4>
            <p><strong>Accès aux médicaments:</strong> Pénuries de 30-40% pour certains 
            traitements spécialisés (source: ONU).</p>
            <p><strong>Sécurité alimentaire:</strong> 25% de la population en insécurité 
            alimentaire modérée à sévère (2025).</p>
            <p><strong>Emploi:</strong> Taux de chômage officiel: 11%, réel estimé: 15-20%.</p>
            <p><strong>Émigration:</strong> +40% de départs de diplômés depuis 2018.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-box'>
            <h4>🏥 Indicateurs de santé</h4>
            <p><strong>Espérance de vie:</strong> 76.2 ans (en baisse de 0.8 an depuis 2017)</p>
            <p><strong>Mortalité infantile:</strong> 13.4/1000 (en hausse)</p>
            <p><strong>Dépenses de santé:</strong> 6.5% du PIB</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_hum2:
        st.markdown("""
        <div class='humanitarian-box'>
            <h4>💰 Coût d'opportunité des dépenses militaires</h4>
            <p><strong>Budget défense annuel:</strong> ~18.5 Mds $</p>
            <p><strong>Ce budget pourrait financer:</strong></p>
            <ul>
                <li>Éducation universelle pour 10 ans: 5 Mds $</li>
                <li>Système de santé modernisé: 8 Mds $</li>
                <li>Programme de logement social: 4 Mds $</li>
                <li>Subventions alimentaires élargies: 2 Mds $</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Graphique comparatif
        fig_opp = go.Figure(data=[
            go.Bar(name='Dépenses actuelles', x=['Défense'], y=[18.5], marker_color='#DA0000'),
            go.Bar(name='Besoins sociaux', x=['Éducation', 'Santé', 'Logement'], 
                   y=[5, 8, 4], marker_color='#239F40')
        ])
        fig_opp.update_layout(title="Coût d'opportunité (milliards $)", height=350)
        st.plotly_chart(fig_opp, use_container_width=True)
    
    # Graphique de l'impact social
    st.markdown("### 📊 Évolution des indicateurs sociaux")
    
    social_data = pd.DataFrame({
        'Année': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'Indice pauvreté': [18, 17, 16, 18, 21, 25, 28, 30, 32, 33, 35],
        'Chômage': [10.5, 11.2, 11.8, 12.5, 13.2, 14.1, 14.8, 15.2, 15.5, 15.8, 16.2]
    })
    
    fig_social = make_subplots(specs=[[{"secondary_y": True}]])
    fig_social.add_trace(go.Scatter(x=social_data['Année'], y=social_data['Indice pauvreté'],
                                     name="Indice de pauvreté", line=dict(color='#DA0000', width=3)),
                        secondary_y=False)
    fig_social.add_trace(go.Scatter(x=social_data['Année'], y=social_data['Chômage'],
                                     name="Taux de chômage %", line=dict(color='#FFA500', width=3)),
                        secondary_y=True)
    fig_social.update_layout(title="Évolution des indicateurs sociaux")
    st.plotly_chart(fig_social, use_container_width=True)

# ============================================================================
# FOOTER COMMUN
# ============================================================================

st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("""
    <div style='text-align:center'>
        <b>Sources principales:</b><br>
        AIEA · Banque Centrale d'Iran · SIPRI<br>
        ONU · Banque Mondiale · FMI
    </div>
    """, unsafe_allow_html=True)

with col_footer2:
    st.markdown("""
    <div style='text-align:center'>
        <b>Mise à jour:</b> mars 2026<br>
        <b>Contact:</b> analyse@geopolitique.org
    </div>
    """, unsafe_allow_html=True)

with col_footer3:
    st.markdown("""
    <div style='text-align:center'>
        <b>🇮🇷 تحلیل جامع ایران</b><br>
        Dashboard intégré - Version 2.0
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8rem; margin-top: 1rem;'>
    ⚠️ À titre informatif uniquement - Données partielles et simulées pour la démonstration.<br>
    Les analyses présentées ne constituent pas un conseil géopolitique ou financier.
</div>
""", unsafe_allow_html=True)
