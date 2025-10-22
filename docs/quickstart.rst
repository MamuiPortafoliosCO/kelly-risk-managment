Quick Start Guide
================

Get up and running with RiskOptima Engine in minutes. This guide covers the basic workflow for analyzing your trading performance and calculating optimal risk parameters.

Prerequisites
-------------

Before starting, ensure you have:

- RiskOptima Engine installed (see :doc:`installation`)
- MetaTrader 5 terminal installed and running (optional, for live data)
- Your MT5 trade history file (CSV or XML format)

Launch the Application
----------------------

Start RiskOptima Engine with a single command:

.. code-block:: bash

   # Launch full application (backend + frontend)
   python -m risk_optima_engine full

This will start:
- **Backend API** on http://localhost:8000
- **Frontend GUI** on http://localhost:8501

Open your web browser and navigate to http://localhost:8501 to access the application.

Import Your Trade History
-------------------------

1. **Upload Your Data**

   In the web interface, locate the file upload section and:

   - Click "Browse files" or drag and drop your MT5 export file
   - Supported formats: CSV (.csv) and XML (.xml)
   - File size limit: Up to 10,000 trades

2. **Data Validation**

   The system will automatically:
   - Parse your trade data
   - Validate required fields
   - Show a preview of imported trades
   - Display any validation errors

Analyze Performance
-------------------

Once your data is uploaded, view comprehensive performance metrics:

**Key Performance Indicators**
   - Total trades and win/loss counts
   - Win probability and profit factor
   - Average win/loss and risk-reward ratio
   - Maximum drawdown and Sharpe ratio

**Equity Curve**
   - Interactive chart showing account balance over time
   - Drawdown periods highlighted
   - Zoom and pan capabilities

Calculate Risk Parameters
-------------------------

Configure your prop firm challenge requirements:

1. **Set Challenge Parameters**

   - **Account Size**: Initial capital amount
   - **Profit Target**: Required profit percentage (e.g., 10%)
   - **Daily Loss Limit**: Maximum daily drawdown (e.g., 5%)
   - **Overall Loss Limit**: Maximum total drawdown (e.g., 10%)
   - **Minimum Trading Days**: Required trading period

2. **Run Optimization**

   Click "Calculate Optimal Risk" to start Monte Carlo simulations.

3. **Review Results**

   The system will display:
   - **Recommended Risk Fraction**: Optimal percentage of capital to risk per trade
   - **Success Probability**: Estimated chance of passing the challenge
   - **Expected Drawdown**: Projected maximum loss periods

Monitor Live Account (Optional)
-------------------------------

If MT5 is connected:

1. **Connect to MT5**

   - Enter your MT5 account credentials
   - Click "Connect" to establish the link

2. **View Live Metrics**

   - Real-time balance and equity
   - Current margin usage
   - Active positions (if any)

3. **Live Dashboard**

   - Auto-refreshing account status
   - Connection health indicator
   - Recent account activity

Generate Reports
----------------

Export your analysis results:

1. **Report Types**

   - **Performance Report**: Comprehensive KPI analysis
   - **Risk Optimization Report**: Challenge success probabilities
   - **Combined Report**: All metrics in one document

2. **Export Formats**

   - **PDF**: Professional formatted reports
   - **CSV**: Raw data for external analysis
   - **Interactive Charts**: PNG/SVG images

Example Workflow
----------------

Here's a complete example using sample data:

.. code-block:: bash

   # 1. Start the application
   python -m risk_optima_engine full

   # 2. Open browser to http://localhost:8501

   # 3. Upload sample data (or use example_mt5_data.csv)
   # - File: example_mt5_data.csv
   # - Format: CSV

   # 4. Review performance metrics
   # - Total Trades: 150
   # - Win Rate: 65%
   # - Profit Factor: 1.8

   # 5. Configure challenge parameters
   # - Account Size: $100,000
   # - Profit Target: 10%
   # - Daily Loss Limit: 5%
   # - Overall Loss Limit: 10%
   # - Minimum Days: 30

   # 6. Run Monte Carlo simulation
   # - Simulations: 1,000 runs
   # - Processing Time: ~30 seconds

   # 7. View results
   # - Optimal Risk: 1.2% per trade
   # - Success Rate: 78%
   # - Max Drawdown: 8.5%

Command Line Usage
------------------

For advanced users, RiskOptima Engine can be controlled via command line:

.. code-block:: bash

   # Run only the backend API
   python -m risk_optima_engine backend

   # Run only the frontend GUI
   python -m risk_optima_engine frontend

   # Run in development mode with auto-reload
   python -m risk_optima_engine dev

   # Test MT5 connection
   python -m risk_optima_engine mt5-test

Troubleshooting
---------------

**Application Won't Start**
   - Check Python version (3.9+ required)
   - Verify all dependencies are installed
   - Ensure ports 8000 and 8501 are available

**File Upload Fails**
   - Check file format (CSV/XML only)
   - Verify file size (< 10MB)
   - Ensure proper MT5 export format

**MT5 Connection Issues**
   - Confirm MT5 terminal is running
   - Verify account credentials
   - Check firewall settings

**Slow Performance**
   - Close other applications
   - Ensure adequate RAM (8GB+)
   - Use SSD storage

Next Steps
----------

Now that you've completed the quick start:

- Explore advanced features in the :doc:`user_guide`
- Learn about configuration options in :doc:`configuration`
- Check out code examples in :doc:`examples`
- Review the API reference in :doc:`api_reference`

For detailed usage instructions and advanced features, continue reading the user guide.