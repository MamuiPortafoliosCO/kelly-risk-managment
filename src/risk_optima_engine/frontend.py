"""
Streamlit Frontend for RiskOptima Engine
Provides the user interface for data upload, analysis, and visualization
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional
import requests
import time
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="RiskOptima Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
API_BASE_URL = "http://localhost:8000/api/v1"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def api_request(endpoint: str, method: str = "GET", data: Optional[Dict] = None, files: Optional[Dict] = None) -> Dict:
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"

        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files, data=data)
            else:
                response = requests.post(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return {}

def display_metrics_grid(metrics: Dict[str, Any]):
    """Display KPIs in a grid layout"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Trades", f"{metrics.get('total_trades', 0)}")
        st.metric("Win Rate", f"{metrics.get('win_probability', 0):.1%}")

    with col2:
        st.metric("Profit Factor", f"{metrics.get('profit_factor', 0):.2f}")
        st.metric("Expectancy", f"${metrics.get('expectancy', 0):.2f}")

    with col3:
        st.metric("Avg Win", f"${metrics.get('avg_win', 0):.2f}")
        st.metric("Avg Loss", f"${metrics.get('avg_loss', 0):.2f}")

    with col4:
        st.metric("Win/Loss Ratio", f"{metrics.get('win_loss_ratio', 0):.2f}")
        st.metric("Max Drawdown", f"${metrics.get('max_drawdown', 0):.2f}")

def plot_equity_curve(equity_curve: List[float]):
    """Create equity curve plot"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(range(len(equity_curve))),
        y=equity_curve,
        mode='lines',
        name='Equity Curve',
        line=dict(color='#1f77b4', width=2)
    ))

    fig.update_layout(
        title="Equity Curve",
        xaxis_title="Trade Number",
        yaxis_title="Account Equity ($)",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

def main():
    """Main application"""
    st.markdown('<h1 class="main-header">RiskOptima Engine</h1>', unsafe_allow_html=True)
    st.markdown("*Quantitative Risk Analysis and Management Tool for MT5 Traders*")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Data Upload & Analysis", "Challenge Optimizer", "Live Account Status", "Reports"]
    )

    # MT5 Connection Status in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("MT5 Connection")

    if st.sidebar.button("Connect to MT5"):
        with st.spinner("Connecting to MT5..."):
            result = api_request("/mt5/connect", "POST", {"timeout": 30})
            if result.get("connected"):
                st.sidebar.success("✅ Connected")
            else:
                st.sidebar.error("❌ Connection Failed")

    # Get account info if connected
    account_info = api_request("/mt5/account-info")
    if account_info:
        st.sidebar.metric("Balance", f"${account_info.get('balance', 0):.2f}")
        st.sidebar.metric("Equity", f"${account_info.get('equity', 0):.2f}")
        st.sidebar.metric("Margin", f"${account_info.get('margin', 0):.2f}")

    # Main content based on selected page
    if page == "Data Upload & Analysis":
        show_data_upload_page()
    elif page == "Challenge Optimizer":
        show_challenge_optimizer_page()
    elif page == "Live Account Status":
        show_live_account_page()
    elif page == "Reports":
        show_reports_page()

def show_data_upload_page():
    """Data upload and performance analysis page"""
    st.header("📊 Data Upload & Performance Analysis")

    st.markdown("""
    Upload your MT5 trade history file to analyze your trading performance and calculate key risk metrics.
    """)

    # File upload
    uploaded_file = st.file_uploader(
        "Choose MT5 export file",
        type=["csv", "xml"],
        help="Upload your MT5 trade history in CSV or XML format"
    )

    format_type = st.selectbox(
        "File Format",
        ["csv", "xml"],
        help="Select the format of your MT5 export file"
    )

    if uploaded_file is not None and st.button("Analyze Trades"):
        with st.spinner("Uploading and analyzing trade data..."):
            # Upload file
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/plain")}
            upload_result = api_request(
                "/upload/trade-history",
                "POST",
                {"format": format_type},
                files
            )

            if upload_result.get("file_id"):
                file_id = upload_result["file_id"]

                # Analyze performance
                analysis_result = api_request(
                    "/analysis/performance",
                    "POST",
                    {"file_id": file_id}
                )

                if analysis_result.get("status") == "success":
                    st.success("✅ Analysis completed successfully!")

                    # Display metrics
                    st.subheader("Key Performance Indicators")
                    display_metrics_grid(analysis_result.get("kpis", {}))

                    # Equity curve
                    st.subheader("Equity Curve")
                    equity_curve = analysis_result.get("equity_curve", [])
                    if equity_curve:
                        fig = plot_equity_curve(equity_curve)
                        st.plotly_chart(fig, use_container_width=True)

                    # Store results in session state for other pages
                    st.session_state.analysis_results = analysis_result
                    st.session_state.file_id = file_id

                else:
                    st.error("❌ Analysis failed")
            else:
                st.error("❌ File upload failed")

def show_challenge_optimizer_page():
    """Challenge optimization page"""
    st.header("🎯 Challenge Optimizer")

    st.markdown("""
    Optimize your risk management strategy for proprietary trading firm challenges.
    Input your challenge parameters and get recommended position sizing.
    """)

    # Check if we have analysis results
    if "analysis_results" not in st.session_state:
        st.warning("⚠️ Please upload and analyze your trade data first on the Data Upload page.")
        return

    # Challenge parameters form
    st.subheader("Challenge Parameters")

    col1, col2 = st.columns(2)

    with col1:
        account_size = st.number_input(
            "Account Size ($)",
            min_value=100.0,
            max_value=100000.0,
            value=100000.0,
            step=1000.0,
            help="Initial account balance for the challenge"
        )

        profit_target = st.slider(
            "Profit Target (%)",
            min_value=1,
            max_value=50,
            value=10,
            help="Required profit percentage to pass the challenge"
        )

        min_trading_days = st.number_input(
            "Minimum Trading Days",
            min_value=1,
            max_value=365,
            value=30,
            help="Minimum number of days required to trade"
        )

    with col2:
        max_daily_loss = st.slider(
            "Max Daily Loss (%)",
            min_value=1,
            max_value=10,
            value=5,
            help="Maximum loss allowed in a single day"
        )

        max_overall_loss = st.slider(
            "Max Overall Loss (%)",
            min_value=5,
            max_value=20,
            value=10,
            help="Maximum total loss allowed for the account"
        )

    # Optimization button
    if st.button("🚀 Run Optimization", type="primary"):
        with st.spinner("Running Monte Carlo simulations... This may take a few minutes."):

            # Prepare challenge data
            challenge_params = {
                "account_size": account_size,
                "profit_target_percent": profit_target,
                "max_daily_loss_percent": max_daily_loss,
                "max_overall_loss_percent": max_overall_loss,
                "min_trading_days": min_trading_days,
            }

            # Get trade data from analysis results
            # Extract trade data from stored analysis results
            trade_data = []
            if "analysis_results" in st.session_state:
                # This is a simplified approach - in production, you'd store trade data properly
                # For now, we'll use placeholder data since we don't have the original trades
                trade_data = []  # Placeholder - need to implement proper trade data storage

            optimization_result = api_request(
                "/optimization/challenge",
                "POST",
                {
                    "challenge_params": challenge_params,
                    "trade_data": trade_data,
                    "simulation_count": 1000
                }
            )

            if optimization_result.get("status") == "success":
                st.success("✅ Optimization completed!")

                # Display results
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Recommended Risk Fraction",
                        f"{optimization_result.get('recommended_fraction', 0):.2%}"
                    )

                with col2:
                    st.metric(
                        "Simulated Pass Rate",
                        f"{optimization_result.get('pass_rate', 0):.1%}"
                    )

                with col3:
                    confidence = optimization_result.get('confidence_interval', [0, 0])
                    st.metric(
                        "Confidence Interval",
                        f"±{abs(confidence[1] - confidence[0])/2:.1%}"
                    )

                # Risk warnings
                risk_fraction = optimization_result.get('recommended_fraction', 0)
                if risk_fraction > 0.02:
                    st.markdown("""
                    <div class="warning-box">
                    ⚠️ <strong>High Risk Warning:</strong> The recommended risk fraction is above 2%.
                    Consider using a more conservative approach or fractional Kelly.
                    </div>
                    """, unsafe_allow_html=True)
                elif risk_fraction < 0.005:
                    st.markdown("""
                    <div class="warning-box">
                    ⚠️ <strong>Low Risk Notice:</strong> The recommended risk fraction is below 0.5%.
                    This may result in very slow progress toward your profit target.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="success-box">
                    ✅ <strong>Optimal Range:</strong> The recommended risk fraction appears reasonable
                    for your trading style and challenge requirements.
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.error("❌ Optimization failed")

def show_live_account_page():
    """Live account status page"""
    st.header("📈 Live Account Status")

    st.markdown("""
    Monitor your MT5 account in real-time. Connect to your terminal to view current metrics.
    """)

    # Auto-refresh toggle
    auto_refresh = st.checkbox("Auto-refresh every 30 seconds", value=True)

    # Manual refresh button
    if st.button("🔄 Refresh Now"):
        st.rerun()

    # Display account info
    account_info = api_request("/mt5/account-info")

    if account_info:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Balance", f"${account_info.get('balance', 0):.2f}")

        with col2:
            st.metric("Equity", f"${account_info.get('equity', 0):.2f}")

        with col3:
            st.metric("Margin", f"${account_info.get('margin', 0):.2f}")

        with col4:
            margin_level = account_info.get('margin_level', 0)
            st.metric("Margin Level", f"{margin_level:.1f}%" if margin_level else "N/A")

        # Additional metrics
        st.subheader("Additional Metrics")
        col1, col2 = st.columns(2)

        with col1:
            st.info(f"**Free Margin:** ${account_info.get('margin_free', 0):.2f}")
            st.info(f"**Unrealized P&L:** ${account_info.get('profit', 0):.2f}")

        with col2:
            st.info(f"**Leverage:** {account_info.get('leverage', 0)}:1")
            st.info(f"**Currency:** {account_info.get('currency', 'USD')}")

    else:
        st.warning("⚠️ MT5 not connected. Please connect using the sidebar.")

    # Auto-refresh logic
    if auto_refresh:
        time.sleep(30)
        st.rerun()

def show_reports_page():
    """Reports and visualization page"""
    st.header("📋 Reports & Visualizations")

    st.markdown("""
    Generate comprehensive reports and visualizations of your trading analysis.
    """)

    # Report generation options
    report_type = st.selectbox(
        "Report Type",
        ["Performance Analysis", "Risk Optimization", "Comprehensive Analysis"]
    )

    export_format = st.selectbox(
        "Export Format",
        ["PDF", "CSV"]
    )

    if st.button("📄 Generate Report"):
        with st.spinner("Generating report..."):

            # Prepare report data
            report_data = {
                "report_type": report_type.lower().replace(" ", "_"),
                "data": st.session_state.get("analysis_results", {}),
                "format": export_format.lower()
            }

            report_result = api_request("/reports/generate", "POST", report_data)

            if report_result.get("report_id"):
                st.success("✅ Report generated successfully!")

                # Download link (placeholder)
                st.info("Report download functionality will be implemented in the next version.")

                # Display sample visualizations
                if "analysis_results" in st.session_state:
                    results = st.session_state.analysis_results

                    # Sample charts
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Performance Distribution")
                        # Placeholder for performance distribution chart
                        st.info("Chart will be displayed here")

                    with col2:
                        st.subheader("Risk Metrics")
                        # Placeholder for risk metrics chart
                        st.info("Chart will be displayed here")

            else:
                st.error("❌ Report generation failed")

if __name__ == "__main__":
    main()