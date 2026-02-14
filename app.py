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

# Clients Page
elif page == "Clients":
    st.title("👥 Clients")

    tab1, tab2, tab3 = st.tabs(
        ["Liste des Clients", "Détails Client", "Top Clients"]
    )

    with tab1:
        st.subheader("Liste Paginée des Clients")

        col1, col2 = st.columns(2)
        with col1:
            limit = st.selectbox(
                "Éléments par page", [10, 25, 50], key="customer_limit"
            )

        customers_data = get_data(
            "/customers",
            params={"page": st.session_state.customer_page, "limit": limit},
        )

        if customers_data:
            if isinstance(customers_data, dict) and "data" in customers_data:
                df = pd.DataFrame(customers_data["data"])
                st.dataframe(df, use_container_width=True)

                # Pagination
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("⬅️ Précédent", key="prev_customer"):
                        if st.session_state.customer_page > 1:
                            st.session_state.customer_page -= 1
                            st.rerun()

                with col2:
                    st.write(f"Page {st.session_state.customer_page}")

                with col3:
                    if st.button("Suivant ➡️", key="next_customer"):
                        st.session_state.customer_page += 1
                        st.rerun()

    with tab2:
        st.subheader("Détails Client")
        customer_id = st.text_input("ID Client")

        if customer_id:
            customer = get_data(f"/customers/{customer_id}")
            if customer:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("ID Client", customer.get("customer_id", "N/A"))
                with col2:
                    st.metric(
                        "Nombre de Transactions",
                        customer.get("transaction_count", 0),
                    )
                with col3:
                    st.metric(
                        "Montant Total",
                        f"${customer.get('total_amount', 0):,.2f}",
                    )

                st.metric(
                    "Montant Moyen",
                    f"${customer.get('average_amount', 0):,.2f}",
                )

    with tab3:
        st.subheader("Top Clients")
        n = st.slider("Nombre de clients", 1, 50, 10)

        top_customers = get_data("/customers/Ranked/top", params={"n": n})
        if top_customers:
            df = pd.DataFrame(top_customers)
            st.dataframe(df, use_container_width=True)

            # Chart
            if not df.empty:
                fig = px.bar(
                    df,
                    x="customer_id",
                    y="transaction_count",
                    title="Top Clients par Nombre de Transactions",
                )
                st.plotly_chart(fig, use_container_width=True)

# Transactions Page
elif page == "Transactions":
    st.title("💳 Transactions")

    tab1, tab2 = st.tabs(["Liste des Transactions", "Recherche Avancée"])

    with tab1:
        st.subheader("Liste Paginée des Transactions")

        col1, col2 = st.columns(2)
        with col1:
            limit = st.selectbox(
                "Éléments par page", [10, 25, 50], key="transaction_limit"
            )

        transactions_data = get_data(
            "/transaction",
            params={"page": st.session_state.transaction_page, "limit": limit},
        )

        if transactions_data:
            if (
                isinstance(transactions_data, dict)
                and "data" in transactions_data
            ):
                df = pd.DataFrame(transactions_data["data"])
                st.dataframe(df, use_container_width=True)

                # Pagination
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("⬅️ Précédent", key="prev_transaction"):
                        if st.session_state.transaction_page > 1:
                            st.session_state.transaction_page -= 1
                            st.rerun()

                with col2:
                    st.write(f"Page {st.session_state.transaction_page}")

                with col3:
                    if st.button("Suivant ➡️", key="next_transaction"):
                        st.session_state.transaction_page += 1
                        st.rerun()

    with tab2:
        st.subheader("Recherche Multi-Critères")

        col1, col2 = st.columns(2)
        with col1:
            client_id = st.text_input("ID Client (optionnel)")
            min_amount = st.number_input("Montant Minimum", value=0.0)

        with col2:
            use_chip = st.selectbox(
                "Type de Transaction",
                [
                    "",
                    "Swipe Transaction",
                    "Online Transaction",
                    "Chip Transaction",
                ],
            )
            max_amount = st.number_input("Montant Maximum", value=10000.0)

        if st.button("Rechercher"):
            search_data = {}
            if client_id:
                search_data["client_id"] = client_id
            if min_amount > 0:
                search_data["min_amount"] = min_amount
            if max_amount > 0:
                search_data["max_amount"] = max_amount
            if use_chip:
                search_data["use_chip"] = use_chip

            results = post_data(
                "/transaction/transactionResearch/search", search_data
            )
            if results:
                if isinstance(results, dict) and "data" in results:
                    df = pd.DataFrame(results["data"])
                    st.dataframe(df, use_container_width=True)
                    st.write(
                        f"Total: {results.get('total_count', 0)} transactions"
                    )

# Fraude Page
elif page == "Fraude":
    st.title("🚨 Détection de Fraude")

    tab1, tab2 = st.tabs(["Fraudes Détectées", "Statistiques par Type"])

    with tab1:
        st.subheader("Transactions Frauduleuses")

        fraud_summary = get_data("/fraud/summary")
        if fraud_summary:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Fraudes Détectées",
                    fraud_summary.get("total_fraud_count", 0),
                )
            with col2:
                st.metric(
                    "Taux de Fraude",
                    f"{fraud_summary.get('fraud_rate', 0)*100:.2f}%",
                )
            with col3:
                st.metric(
                    "Montant Frauduleux",
                    f"${fraud_summary.get('total_fraud_amount', 0):,.2f}",
                )

    with tab2:
        st.subheader("Fraudes par Type de Transaction")

        fraud_by_type = get_data("/fraud/by-type")
        if fraud_by_type:
            df = pd.DataFrame(fraud_by_type)
            st.dataframe(df, use_container_width=True)

            # Chart
            if not df.empty:
                fig = px.bar(
                    df,
                    x="type",
                    y="fraud_count",
                    title="Fraudes par Type de Transaction",
                )
                st.plotly_chart(fig, use_container_width=True)

# Statistiques Page
elif page == "Statistiques":
    st.title("📊 Statistiques Avancées")

    tab1, tab2, tab3 = st.tabs(
        [
            "Statistiques Quotidiennes",
            "Distribution des Montants",
            "Statistiques par Type",
        ]
    )

    with tab1:
        st.subheader("Statistiques Quotidiennes")

        daily_stats = get_data("/stats/daily")
        if daily_stats:
            df = pd.DataFrame(daily_stats)
            st.dataframe(df, use_container_width=True)

            if not df.empty:
                fig = px.line(
                    df, x="date", y="count", title="Transactions par Jour"
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Distribution des Montants")

        amount_dist = get_data("/stats/amount-distribution")
        if amount_dist and "buckets" in amount_dist:
            df = pd.DataFrame(amount_dist["buckets"])
            st.dataframe(df, use_container_width=True)

            if not df.empty:
                fig = px.bar(
                    df, x="range", y="count", title="Distribution des Montants"
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Statistiques par Type de Transaction")

        type_stats = get_data("/stats/by-type")
        if type_stats:
            df = pd.DataFrame(type_stats)
            st.dataframe(df, use_container_width=True)

            if not df.empty:
                fig = px.bar(
                    df, x="type", y="count", title="Transactions par Type"
                )
                st.plotly_chart(fig, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Groupe**")
st.sidebar.markdown("**Christian SONTSA**")
st.sidebar.markdown("**Stéphane NZATI** ")
st.sidebar.markdown("**Brenda Camélia Sama**")
