"""Streamlit application for Transaction API."""

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
# removed unused imports

# Configuration
API_BASE_URL = "http://localhost:8000/api"
st.set_page_config(
    page_title="Transaction Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "customer_page" not in st.session_state:
    st.session_state.customer_page = 1
if "transaction_page" not in st.session_state:
    st.session_state.transaction_page = 1
if "fraud_page" not in st.session_state:
    st.session_state.fraud_page = 1    
# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select a section:",
    ["Dashboard", "Clients", "Transactions", "Fraude", "Statistiques"],
)


# Helper functions
def get_data(endpoint, params=None):
    """Fetch data from API."""
    try:
        response = requests.get(
            f"{API_BASE_URL}{endpoint}", params=params, timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erreur de connexion: {str(e)}")
        return None
