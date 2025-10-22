Examples
========

This section provides practical examples and code samples for using RiskOptima Engine in different scenarios.

Basic Usage Examples
--------------------

Analyzing Trade History
~~~~~~~~~~~~~~~~~~~~~~~

**Example 1: Basic Performance Analysis**

.. code-block:: python

   from risk_optima_engine import analyze_performance

   # Load your MT5 trade data
   trades_df = pd.read_csv('my_trades.csv')

   # Analyze performance
   results = analyze_performance(trades_df)

   print(f"Total Trades: {results['total_trades']}")
   print(f"Win Rate: {results['win_probability']:.1%}")
   print(f"Profit Factor: {results['profit_factor']:.2f}")
   print(f"Max Drawdown: {results['max_drawdown']:.2f}")

**Example 2: Kelly Criterion Calculation**

.. code-block:: python

   from risk_optima_engine import calculate_kelly_criterion

   # Calculate optimal risk fraction
   win_probability = 0.65
   win_loss_ratio = 1.8

   kelly_fraction = calculate_kelly_criterion(
       win_probability=win_probability,
       win_loss_ratio=win_loss_ratio
   )

   print(f"Full Kelly: {kelly_fraction:.3f}")
   print(f"Half Kelly: {kelly_fraction * 0.5:.3f}")
   print(f"Quarter Kelly: {kelly_fraction * 0.25:.3f}")

**Example 3: Challenge Optimization**

.. code-block:: python

   from risk_optima_engine import optimize_challenge

   # Define challenge parameters
   challenge_params = {
       "account_size": 100000,
       "profit_target_percent": 10,
       "max_daily_loss_percent": 5,
       "max_overall_loss_percent": 10,
       "min_trading_days": 30
   }

   # Load historical trades
   trades_df = pd.read_csv('historical_trades.csv')

   # Run optimization
   optimization_result = optimize_challenge(
       trades_df,
       challenge_params,
       num_simulations=1000
   )

   print(f"Recommended Risk Fraction: {optimization_result['optimal_fraction']:.3f}")
   print(f"Success Probability: {optimization_result['pass_rate']:.1%}")

API Usage Examples
------------------

REST API Integration
~~~~~~~~~~~~~~~~~~~~

**Example 4: File Upload via API**

.. code-block:: python

   import requests

   # Upload trade history file
   with open('trades.csv', 'rb') as f:
       response = requests.post(
           'http://localhost:8000/api/v1/upload/trade-history',
           files={'file': f}
       )

   if response.status_code == 200:
       file_id = response.json()['file_id']
       print(f"File uploaded successfully. ID: {file_id}")
   else:
       print(f"Upload failed: {response.text}")

**Example 5: Performance Analysis via API**

.. code-block:: python

   import requests

   # Analyze uploaded file
   analysis_request = {
       "file_id": "your_file_id_here",
       "parameters": {
           "robust_statistics": True,
           "include_equity_curve": True
       }
   }

   response = requests.post(
       'http://localhost:8000/api/v1/analysis/performance',
       json=analysis_request
   )

   if response.status_code == 200:
       results = response.json()
       kpis = results['kpis']
       print(f"Performance KPIs: {kpis}")
   else:
       print(f"Analysis failed: {response.text}")

**Example 6: Monte Carlo Simulation via API**

.. code-block:: python

   import requests

   # Run challenge optimization
   optimization_request = {
       "challenge_params": {
           "account_size": 100000,
           "profit_target_percent": 10,
           "max_daily_loss_percent": 5,
           "max_overall_loss_percent": 10,
           "min_trading_days": 30
       },
       "trade_data": [...],  # Your trade data
       "simulation_count": 1000
   }

   response = requests.post(
       'http://localhost:8000/api/v1/optimization/challenge',
       json=optimization_request
   )

   if response.status_code == 200:
       result = response.json()
       print(f"Optimal Risk: {result['recommended_fraction']:.3f}")
       print(f"Success Rate: {result['pass_rate']:.1%}")
   else:
       print(f"Optimization failed: {response.text}")

MT5 Integration Examples
------------------------

Live Data Access
~~~~~~~~~~~~~~~~

**Example 7: MT5 Connection and Account Info**

.. code-block:: python

   from risk_optima_engine import MT5Connector

   # Connect to MT5
   mt5 = MT5Connector()
   if mt5.connect(login=123456, password="password", server="MetaQuotes-Demo"):
       print("Connected to MT5 successfully")

       # Get account information
       account_info = mt5.get_account_info()
       print(f"Balance: ${account_info['balance']:.2f}")
       print(f"Equity: ${account_info['equity']:.2f}")
       print(f"Margin: ${account_info['margin']:.2f}")

       mt5.disconnect()
   else:
       print("Failed to connect to MT5")

**Example 8: Real-time Data Monitoring**

.. code-block:: python

   from risk_optima_engine import MT5LiveData
   import time

   # Initialize live data monitor
   live_data = MT5LiveData()

   # Monitor account for 5 minutes
   start_time = time.time()
   while time.time() - start_time < 300:  # 5 minutes
       account_data = live_data.get_account_status()
       if account_data:
           print(f"Balance: ${account_data['balance']:.2f} | "
                 f"P&L: ${account_data['pl']:.2f}")

       time.sleep(10)  # Update every 10 seconds

   live_data.cleanup()

Advanced Analysis Examples
--------------------------

Custom Risk Models
~~~~~~~~~~~~~~~~~~

**Example 9: Implementing Custom Risk Model**

.. code-block:: python

   from risk_optima_engine.core import BaseRiskModel
   import numpy as np

   class CustomRiskModel(BaseRiskModel):
       """Custom risk model based on volatility-adjusted Kelly."""

       def __init__(self, volatility_multiplier=0.8):
           self.volatility_multiplier = volatility_multiplier

       def calculate_optimal_fraction(self, trades_df):
           # Calculate basic Kelly
           win_prob = len(trades_df[trades_df['profit'] > 0]) / len(trades_df)
           avg_win = trades_df[trades_df['profit'] > 0]['profit'].mean()
           avg_loss = abs(trades_df[trades_df['profit'] < 0]['profit'].mean())
           win_loss_ratio = avg_win / avg_loss

           kelly = win_prob - (1 - win_prob) / win_loss_ratio

           # Adjust for volatility
           returns = trades_df['profit'] / trades_df['volume']  # Return per unit
           volatility = returns.std()
           adjusted_kelly = kelly * (1 - volatility) * self.volatility_multiplier

           return max(0.001, min(adjusted_kelly, 0.05))  # Clamp to reasonable range

   # Usage
   model = CustomRiskModel(volatility_multiplier=0.7)
   optimal_fraction = model.calculate_optimal_fraction(trades_df)
   print(f"Custom Optimal Fraction: {optimal_fraction:.4f}")

**Example 10: Portfolio Risk Analysis**

.. code-block:: python

   from risk_optima_engine import PortfolioAnalyzer
   import pandas as pd

   # Multiple trading accounts/systems
   accounts = {
       'System_A': pd.read_csv('system_a_trades.csv'),
       'System_B': pd.read_csv('system_b_trades.csv'),
       'System_C': pd.read_csv('system_c_trades.csv')
   }

   # Analyze portfolio
   portfolio = PortfolioAnalyzer(accounts)

   # Calculate portfolio metrics
   portfolio_metrics = portfolio.calculate_metrics()
   print("Portfolio Performance:")
   print(f"Total Return: {portfolio_metrics['total_return']:.2f}")
   print(f"Sharpe Ratio: {portfolio_metrics['sharpe_ratio']:.2f}")
   print(f"Max Drawdown: {portfolio_metrics['max_drawdown']:.2f}")

   # Optimize portfolio allocation
   optimal_weights = portfolio.optimize_allocation(target_return=0.15)
   print(f"Optimal Weights: {optimal_weights}")

Data Processing Examples
------------------------

Data Cleaning and Preparation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Example 11: Cleaning MT5 Data**

.. code-block:: python

   import pandas as pd
   from risk_optima_engine.data import clean_mt5_data

   # Load raw MT5 data
   raw_data = pd.read_csv('mt5_export.csv')

   # Clean and validate data
   cleaned_data = clean_mt5_data(raw_data)

   # Remove outliers (optional)
   from scipy import stats
   z_scores = stats.zscore(cleaned_data['profit'])
   cleaned_data = cleaned_data[abs(z_scores) < 3]  # Remove 3-sigma outliers

   # Filter by date range
   cleaned_data['close_time'] = pd.to_datetime(cleaned_data['close_time'])
   recent_trades = cleaned_data[
       cleaned_data['close_time'] >= '2024-01-01'
   ]

   print(f"Original trades: {len(raw_data)}")
   print(f"Cleaned trades: {len(cleaned_data)}")
   print(f"Recent trades: {len(recent_trades)}")

**Example 12: Data Augmentation**

.. code-block:: python

   import pandas as pd
   import numpy as np

   def augment_trade_data(trades_df, num_augmentations=5):
       """Augment trade data with realistic variations."""
       augmented_data = []

       for _ in range(num_augmentations):
           # Add noise to profits (realistic market variations)
           noise_factor = np.random.normal(1.0, 0.05, len(trades_df))
           augmented_profits = trades_df['profit'] * noise_factor

           # Slightly vary volumes
           volume_noise = np.random.normal(1.0, 0.1, len(trades_df))
           augmented_volumes = trades_df['volume'] * volume_noise

           augmented_trades = trades_df.copy()
           augmented_trades['profit'] = augmented_profits
           augmented_trades['volume'] = augmented_volumes

           augmented_data.append(augmented_trades)

       return pd.concat(augmented_data, ignore_index=True)

   # Augment your data for more robust analysis
   original_trades = pd.read_csv('my_trades.csv')
   augmented_trades = augment_trade_data(original_trades, num_augmentations=3)

   print(f"Original: {len(original_trades)} trades")
   print(f"Augmented: {len(augmented_trades)} trades")

Visualization Examples
----------------------

Custom Charts and Reports
~~~~~~~~~~~~~~~~~~~~~~~~~

**Example 13: Equity Curve with Drawdown**

.. code-block:: python

   import plotly.graph_objects as go
   from plotly.subplots import make_subplots

   def create_equity_chart(trades_df):
       """Create equity curve with drawdown visualization."""

       # Calculate cumulative equity
       trades_df = trades_df.sort_values('close_time')
       trades_df['cumulative_profit'] = trades_df['profit'].cumsum()
       trades_df['equity'] = 10000 + trades_df['cumulative_profit']  # Starting capital

       # Calculate drawdown
       trades_df['peak'] = trades_df['equity'].expanding().max()
       trades_df['drawdown'] = (trades_df['equity'] - trades_df['peak']) / trades_df['peak']

       # Create subplot figure
       fig = make_subplots(
           rows=2, cols=1,
           shared_xaxes=True,
           vertical_spacing=0.05,
           subplot_titles=('Equity Curve', 'Drawdown')
       )

       # Equity curve
       fig.add_trace(
           go.Scatter(
               x=trades_df['close_time'],
               y=trades_df['equity'],
               mode='lines',
               name='Equity',
               line=dict(color='blue', width=2)
           ),
           row=1, col=1
       )

       # Drawdown
       fig.add_trace(
           go.Scatter(
               x=trades_df['close_time'],
               y=trades_df['drawdown'],
               fill='tozeroy',
               mode='lines',
               name='Drawdown',
               line=dict(color='red', width=1)
           ),
           row=2, col=1
       )

       fig.update_layout(
           title='Trading Performance Analysis',
           height=600,
           showlegend=False
       )

       return fig

   # Create and display chart
   trades_df = pd.read_csv('trades.csv')
   fig = create_equity_chart(trades_df)
   fig.show()

**Example 14: Risk vs Return Scatter Plot**

.. code-block:: python

   import plotly.express as px

   def create_risk_return_plot(trades_df):
       """Create risk vs return analysis plot."""

       # Group by symbol or strategy
       symbol_stats = trades_df.groupby('symbol').agg({
           'profit': ['count', 'sum', 'std'],
           'volume': 'sum'
       }).reset_index()

       symbol_stats.columns = ['symbol', 'num_trades', 'total_profit', 'profit_std', 'total_volume']

       # Calculate metrics
       symbol_stats['avg_profit'] = symbol_stats['total_profit'] / symbol_stats['num_trades']
       symbol_stats['profitability'] = symbol_stats['total_profit'] / symbol_stats['total_volume']
       symbol_stats['volatility'] = symbol_stats['profit_std'] / symbol_stats['total_volume']

       # Create scatter plot
       fig = px.scatter(
           symbol_stats,
           x='volatility',
           y='profitability',
           size='num_trades',
           color='symbol',
           hover_data=['num_trades', 'total_profit'],
           title='Risk vs Return Analysis by Symbol',
           labels={
               'volatility': 'Profit Volatility',
               'profitability': 'Profit per Volume',
               'num_trades': 'Number of Trades'
           }
       )

       fig.update_layout(
           xaxis_title="Risk (Profit Volatility)",
           yaxis_title="Return (Profit per Volume)",
           height=500
       )

       return fig

   # Create and display plot
   fig = create_risk_return_plot(trades_df)
   fig.show()

Automation Examples
-------------------

Batch Processing
~~~~~~~~~~~~~~~~

**Example 15: Batch Analysis of Multiple Files**

.. code-block:: python

   import os
   import pandas as pd
   from risk_optima_engine import batch_analyze

   def analyze_trading_folder(folder_path):
       """Analyze all CSV files in a folder."""

       results = {}
       summary_stats = []

       for filename in os.listdir(folder_path):
           if filename.endswith('.csv'):
               file_path = os.path.join(folder_path, filename)
               strategy_name = filename.replace('.csv', '')

               try:
                   # Load and analyze data
                   trades_df = pd.read_csv(file_path)
                   analysis_result = analyze_performance(trades_df)

                   results[strategy_name] = analysis_result

                   # Collect summary stats
                   summary_stats.append({
                       'strategy': strategy_name,
                       'total_trades': analysis_result['total_trades'],
                       'win_rate': analysis_result['win_probability'],
                       'profit_factor': analysis_result['profit_factor'],
                       'max_drawdown': analysis_result['max_drawdown']
                   })

               except Exception as e:
                   print(f"Error analyzing {filename}: {e}")
                   continue

       # Create summary DataFrame
       summary_df = pd.DataFrame(summary_stats)

       # Find best performing strategy
       best_strategy = summary_df.loc[summary_df['profit_factor'].idxmax()]

       return results, summary_df, best_strategy

   # Usage
   results, summary, best = analyze_trading_folder('./trading_data/')
   print(f"Best Strategy: {best['strategy']} (PF: {best['profit_factor']:.2f})")

**Example 16: Automated Daily Report**

.. code-block:: python

   import schedule
   import time
   from datetime import datetime
   from risk_optima_engine import generate_daily_report

   def daily_analysis_job():
       """Run daily analysis and generate report."""

       print(f"Running daily analysis at {datetime.now()}")

       try:
           # Connect to MT5 and get latest data
           from risk_optima_engine import MT5Connector
           mt5 = MT5Connector()

           if mt5.connect():
               # Get today's trades
               today_trades = mt5.get_today_trades()

               if not today_trades.empty:
                   # Analyze today's performance
                   analysis = analyze_performance(today_trades)

                   # Generate report
                   report_path = generate_daily_report(
                       analysis,
                       output_dir='./daily_reports/',
                       include_charts=True
                   )

                   print(f"Daily report generated: {report_path}")
               else:
                   print("No trades today")

               mt5.disconnect()

       except Exception as e:
           print(f"Error in daily analysis: {e}")

   # Schedule daily report at 6 PM
   schedule.every().day.at("18:00").do(daily_analysis_job)

   print("Daily analysis scheduler started. Press Ctrl+C to stop.")

   while True:
       schedule.run_pending()
       time.sleep(60)  # Check every minute

Integration Examples
--------------------

Trading Platform Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Example 17: TradingView Webhook Integration**

.. code-block:: python

   from flask import Flask, request, jsonify
   from risk_optima_engine import analyze_performance

   app = Flask(__name__)

   @app.route('/webhook/tradingview', methods=['POST'])
   def tradingview_webhook():
       """Receive trading signals from TradingView."""

       data = request.json

       if data.get('action') == 'analyze_portfolio':
           # Extract trade data from webhook
           trades_data = data.get('trades', [])

           if trades_data:
               trades_df = pd.DataFrame(trades_data)

               # Analyze performance
               analysis = analyze_performance(trades_df)

               # Calculate risk metrics
               kelly_fraction = calculate_kelly_criterion(
                   analysis['win_probability'],
                   analysis['win_loss_ratio']
               )

               response = {
                   'analysis': analysis,
                   'recommended_risk_fraction': kelly_fraction,
                   'timestamp': datetime.now().isoformat()
               }

               return jsonify(response)

       return jsonify({'error': 'Invalid request'}), 400

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)

**Example 18: Excel Integration**

.. code-block:: python

   import pandas as pd
   from openpyxl import Workbook
   from openpyxl.styles import Font, PatternFill
   from risk_optima_engine import comprehensive_analysis

   def export_to_excel(trades_df, output_file='trading_analysis.xlsx'):
       """Export comprehensive analysis to Excel."""

       # Create workbook
       wb = Workbook()

       # Performance Analysis Sheet
       ws_perf = wb.active
       ws_perf.title = "Performance Analysis"

       # Run comprehensive analysis
       analysis = comprehensive_analysis(trades_df)

       # Write KPIs
       ws_perf['A1'] = 'Key Performance Indicators'
       ws_perf['A1'].font = Font(bold=True, size=14)

       kpis = analysis['kpis']
       row = 3
       for key, value in kpis.items():
           ws_perf[f'A{row}'] = key.replace('_', ' ').title()
           ws_perf[f'B{row}'] = value
           row += 1

       # Equity Curve Sheet
       ws_equity = wb.create_sheet("Equity Curve")
       ws_equity['A1'] = 'Date'
       ws_equity['B1'] = 'Equity'

       equity_data = analysis['equity_curve']
       for i, point in enumerate(equity_data, 2):
           ws_equity[f'A{i}'] = point['timestamp']
           ws_equity[f'B{i}'] = point['equity']

       # Risk Optimization Sheet
       ws_risk = wb.create_sheet("Risk Optimization")

       # Add challenge parameters and results
       challenge_params = {
           'account_size': 100000,
           'profit_target_percent': 10,
           'max_daily_loss_percent': 5,
           'max_overall_loss_percent': 10,
           'min_trading_days': 30
       }

       optimization = optimize_challenge(trades_df, challenge_params)

       ws_risk['A1'] = 'Challenge Optimization Results'
       ws_risk['A1'].font = Font(bold=True, size=14)

       ws_risk['A3'] = 'Parameter'
       ws_risk['B3'] = 'Value'
       ws_risk['A3'].font = Font(bold=True)
       ws_risk['B3'].font = Font(bold=True)

       row = 4
       for key, value in optimization.items():
           if key != 'simulation_results':  # Skip detailed results
               ws_risk[f'A{row}'] = key.replace('_', ' ').title()
               ws_risk[f'B{row}'] = value
               row += 1

       # Save workbook
       wb.save(output_file)
       print(f"Analysis exported to {output_file}")

   # Usage
   trades_df = pd.read_csv('trades.csv')
   export_to_excel(trades_df)

These examples demonstrate the versatility of RiskOptima Engine for various trading analysis scenarios. For more advanced usage, refer to the API documentation and developer guide.