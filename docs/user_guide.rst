User Guide
=========

This comprehensive guide covers all features and workflows of RiskOptima Engine, from basic usage to advanced analysis techniques.

Overview
--------

RiskOptima Engine provides a complete toolkit for quantitative trading risk management. The application follows a three-tier architecture:

- **Frontend**: Web-based GUI for user interaction
- **Backend**: REST API for data processing
- **Core Engine**: High-performance Rust library for computations

Core Workflows
--------------

Data Ingestion and Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Supported File Formats**

RiskOptima Engine accepts MT5 trade history in two formats:

1. **CSV Format** (Recommended)

   .. code-block:: csv

      Symbol,Type,Volume,Open Price,Close Price,Profit,Commission,Swap
      EURUSD,buy,0.10,1.0850,1.0920,70.00,-0.50,-0.20
      GBPUSD,sell,0.05,1.2750,1.2680,-35.00,-0.25,-0.10

2. **XML Format** (MT5 Native)

   .. code-block:: xml

      <?xml version="1.0" encoding="UTF-8"?>
      <report>
        <account>123456</account>
        <trades>
          <trade>
            <symbol>EURUSD</symbol>
            <type>buy</type>
            <volume>0.10</volume>
            <open_price>1.0850</open_price>
            <close_price>1.0920</close_price>
            <profit>70.00</profit>
            <commission>-0.50</commission>
            <swap>-0.20</swap>
          </trade>
        </trades>
      </report>

**Data Validation Rules**

The system validates imported data for:

- **Required Fields**: Symbol, Type, Volume, Open Price, Close Price, Profit
- **Data Types**: Numeric fields must be valid numbers
- **Consistency**: Profit calculations are verified
- **Completeness**: All required fields must be present
- **Outlier Detection**: Statistical outliers are flagged

**File Size Limits**

- Maximum file size: 10MB
- Maximum trades: 10,000
- Recommended: < 1,000 trades for optimal performance

Performance Analysis
~~~~~~~~~~~~~~~~~~~~

**Key Performance Indicators (KPIs)**

RiskOptima Engine calculates comprehensive trading metrics:

**Basic Statistics**
   - **Total Trades**: Count of closed positions
   - **Win Count/Loss Count**: Number of profitable vs unprofitable trades
   - **Win Probability (p)**: Proportion of winning trades
   - **Loss Probability (q)**: 1 - p

**Profitability Metrics**
   - **Average Win**: Mean profit of winning trades
   - **Average Loss**: Mean loss of losing trades (absolute value)
   - **Win/Loss Ratio (R)**: Average win divided by average loss
   - **Profit Factor**: Gross profit divided by gross loss
   - **Mathematical Expectancy**: Expected value per trade

**Risk Metrics**
   - **Largest Loss**: Maximum single trade loss
   - **Maximum Drawdown**: Peak-to-trough equity decline
   - **Sharpe Ratio**: Risk-adjusted return metric
   - **Recovery Time**: Time to recover from drawdowns

**Equity Curve Analysis**

The equity curve visualization provides:

- **Time Series Plot**: Account balance over time
- **Drawdown Highlighting**: Red areas show drawdown periods
- **Interactive Features**: Zoom, pan, and crosshair tools
- **Export Options**: PNG/SVG formats for reports

Risk Modeling Algorithms
~~~~~~~~~~~~~~~~~~~~~~~~

**Kelly Criterion**

The Kelly Criterion calculates the optimal fraction of capital to risk:

.. math::

   f^* = p - \frac{q}{R}

Where:
- :math:`f^*` = Optimal fraction to risk
- :math:`p` = Probability of winning
- :math:`q` = Probability of losing
- :math:`R` = Win/loss ratio

**Fractional Kelly Options**
   - **Full Kelly (1.0x)**: Maximum growth rate
   - **Half Kelly (0.5x)**: Balanced risk/reward
   - **Quarter Kelly (0.25x)**: Conservative approach

**Optimal F (Ralph Vince)**

Optimal F finds the position size that maximizes terminal wealth:

.. math::

   TWR(f) = \prod(1 + f \times (-\frac{trade_i}{largest\_loss}))

Where :math:`trade_i` represents each historical trade outcome.

**Algorithm Features**
   - Grid search optimization
   - Convergence criteria
   - Sensitivity analysis
   - Confidence intervals

Challenge Optimization
~~~~~~~~~~~~~~~~~~~~~~

**Monte Carlo Simulation**

RiskOptima Engine uses Monte Carlo methods to optimize prop firm challenge success:

**Simulation Parameters**
   - **Sample Size**: Equal to historical trade count
   - **Resampling Method**: Bootstrap with replacement
   - **Risk Fractions**: Tested from 0.1% to 2.0%
   - **Simulation Count**: Minimum 1,000 runs per fraction

**Challenge Rules Implementation**

The simulator enforces prop firm requirements:

1. **Profit Target**: Must reach specified profit percentage
2. **Daily Loss Limit**: Cannot exceed daily drawdown threshold
3. **Overall Loss Limit**: Total drawdown cannot breach maximum
4. **Trading Days**: Must complete minimum trading period

**Pass/Fail Criteria**

A simulation "passes" if:
- Profit target is achieved
- No daily loss limit is breached
- Overall loss limit is not exceeded
- Minimum trading days are completed

**Optimization Results**

The system provides:
- **Optimal Risk Fraction**: Percentage with highest success rate
- **Success Probability**: Estimated pass rate at optimal fraction
- **Confidence Intervals**: Statistical uncertainty bounds
- **Risk Metrics**: Drawdown analysis for successful simulations

MT5 Live Integration
~~~~~~~~~~~~~~~~~~~~

**Connection Setup**

To enable live MT5 features:

1. **Launch MT5 Terminal**
2. **Enable Automation** (if required)
3. **Note Credentials**: Account number, password, server
4. **Connect in Application**

**Available Live Data**

- **Account Information**: Balance, Equity, Margin
- **Real-time Metrics**: Current P&L, margin usage
- **Connection Status**: Health monitoring and auto-reconnection

**Security Considerations**

- All communication occurs locally
- No data transmission to external servers
- Credentials stored securely (optional)
- IPC connection with timeout handling

Reporting and Export
~~~~~~~~~~~~~~~~~~~~

**Report Types**

1. **Performance Analysis Report**
   - Executive summary
   - KPI dashboard
   - Equity curve analysis
   - Risk metrics breakdown

2. **Risk Optimization Report**
   - Model comparison (Kelly vs Optimal F)
   - Challenge simulation results
   - Sensitivity analysis
   - Risk warnings and caveats

3. **Comprehensive Report**
   - All metrics combined
   - Scenario comparisons
   - Historical trends
   - Forward projections

**Export Formats**

- **PDF**: Professional formatted reports
- **CSV**: Raw data export
- **PNG/SVG**: Chart images
- **JSON**: Structured data

Advanced Features
-----------------

Batch Processing
~~~~~~~~~~~~~~~~

Process multiple trade files simultaneously:

.. code-block:: python

   from risk_optima_engine import batch_analyze

   results = batch_analyze([
       'trades_q1.csv',
       'trades_q2.csv',
       'trades_q3.csv'
   ])

Custom Risk Models
~~~~~~~~~~~~~~~~~~

Implement custom position sizing algorithms:

.. code-block:: python

   from risk_optima_engine.core import CustomRiskModel

   class MyRiskModel(CustomRiskModel):
       def calculate_position_size(self, capital, risk_fraction):
           # Custom logic here
           return optimal_size

Scenario Analysis
~~~~~~~~~~~~~~~~~

Compare different trading scenarios:

- **What-if Analysis**: Change historical outcomes
- **Parameter Sensitivity**: Test different assumptions
- **Market Condition Analysis**: Performance by market regime
- **Time Period Analysis**: Performance across different timeframes

API Integration
~~~~~~~~~~~~~~~

Use the REST API for programmatic access:

.. code-block:: python

   import requests

   # Upload trade data
   response = requests.post(
       'http://localhost:8000/api/v1/upload/trade-history',
       files={'file': open('trades.csv', 'rb')}
   )

   # Run analysis
   analysis = requests.post(
       'http://localhost:8000/api/v1/analysis/performance',
       json={'file_id': response.json()['file_id']}
   )

Best Practices
--------------

Data Quality
~~~~~~~~~~~~

**Data Preparation**
   - Export complete trade history from MT5
   - Include all closed positions
   - Verify profit calculations
   - Remove incomplete or erroneous trades

**Validation Checks**
   - Review import summary for errors
   - Check for outliers and anomalies
   - Verify date ranges and completeness
   - Confirm commission and swap calculations

Risk Management
~~~~~~~~~~~~~~~

**Position Sizing**
   - Start with conservative risk fractions
   - Gradually increase based on backtesting
   - Consider market volatility
   - Account for gap risk and slippage

**Challenge Optimization**
   - Use realistic challenge parameters
   - Consider multiple scenarios
   - Account for changing market conditions
   - Plan for drawdown periods

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

**Regular Reviews**
   - Update analysis with new trades
   - Monitor key metrics trends
   - Review risk parameter effectiveness
   - Adjust strategies based on results

**Benchmarking**
   - Compare against market indices
   - Track performance vs goals
   - Analyze seasonal patterns
   - Review risk-adjusted returns

Troubleshooting
---------------

**Common Issues**

**Data Import Problems**
   - Check file format and encoding
   - Verify required columns are present
   - Ensure numeric fields are properly formatted
   - Review error messages for specific issues

**Performance Issues**
   - Reduce simulation count for faster results
   - Close unnecessary applications
   - Ensure adequate system resources
   - Use smaller datasets for testing

**MT5 Connection Issues**
   - Verify MT5 terminal is running
   - Check account credentials
   - Confirm firewall settings
   - Test connection manually

**Calculation Errors**
   - Review input parameters
   - Check for division by zero
   - Verify data consistency
   - Contact support for complex issues

Next Steps
----------

- **API Reference**: See :doc:`api_reference` for detailed API documentation
- **Examples**: Check :doc:`examples` for code samples
- **Configuration**: Learn about settings in :doc:`configuration`
- **Development**: Contribute to the project via :doc:`developer_guide`