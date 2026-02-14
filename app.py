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


def post_data(endpoint, data):
    """Post data to API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}", json=data, timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erreur de connexion: {str(e)}")
        return None


# Dashboard Page
if page == "Dashboard":
    st.subheader("GROUPE 1 : Christian SONTSA - Stéphane NZATI - Brenda Sama")
    st.title("📈 Dashboard")

    # Get overview statistics
    stats = get_data("/stats/overview")

    if stats:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Transactions", f"{stats.get('total_count', 0):,}")

        with col2:
            st.metric("Total Amount", f"${stats.get('total_amount', 0):,.2f}")

        with col3:
            st.metric(
                "Average Amount", f"${stats.get('average_amount', 0):,.2f}"
            )

        with col4:
            min_date = stats.get("min_date", "N/A")
            max_date = stats.get("max_date", "N/A")
            min_date_str = (
                min_date[:10]
                if isinstance(min_date, str)
                else str(min_date)
            )
            max_date_str = (
                max_date[:10]
                if isinstance(max_date, str)
                else str(max_date)
            )
            st.metric(
                "Date Range",
                f"{min_date_str} to {max_date_str}",
            )

    # Get fraud statistics
    fraud_stats = get_data("/fraud/summary")
    if fraud_stats:
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Fraud Transactions",
                f"{fraud_stats.get('total_fraud_count', 0):,}",
            )
        with col2:
            st.metric(
                "Fraud Rate", f"{fraud_stats.get('fraud_rate', 0)*100:.2f}%"
            )

    # Daily statistics chart
    st.subheader("📅 Statistiques Quotidiennes")
    daily_stats = get_data("/stats/daily")
    if daily_stats:
        df_daily = pd.DataFrame(daily_stats)
        if not df_daily.empty:
            fig = px.line(
                df_daily, x="date", y="count", title="Transactions par Jour"
            )
            st.plotly_chart(fig, use_container_width=True)
