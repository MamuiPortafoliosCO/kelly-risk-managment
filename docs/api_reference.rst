API Reference
=============

This section provides comprehensive documentation for the RiskOptima Engine REST API.

Base URL
--------

.. code-block:: text

   http://localhost:8000/api/v1

Authentication
--------------

RiskOptima Engine runs locally and does not require authentication. All API endpoints are accessible without credentials.

File Upload Endpoints
---------------------

POST /upload/trade-history
~~~~~~~~~~~~~~~~~~~~~~~~~~

Upload and validate MT5 trade history files.

**Request**

.. code-block:: http

   POST /api/v1/upload/trade-history
   Content-Type: multipart/form-data

   file: <trade_history_file>  # CSV or XML file
   format: "csv" | "xml"       # Optional, auto-detected

**Parameters**

- ``file`` (file, required): MT5 trade history file (.csv or .xml)
- ``format`` (string, optional): File format, defaults to auto-detection

**Response**

.. code-block:: json

   {
     "file_id": "string",
     "status": "processing|completed|failed",
     "message": "string",
     "record_count": 150,
     "errors": []
   }

**Status Codes**

- ``200``: Upload successful
- ``400``: Invalid file or format
- ``413``: File too large
- ``422``: Validation errors

GET /upload/status/{file_id}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check the status of a file upload and processing.

**Request**

.. code-block:: http

   GET /api/v1/upload/status/{file_id}

**Parameters**

- ``file_id`` (path, required): File identifier from upload response

**Response**

.. code-block:: json

   {
     "status": "processing|completed|failed",
     "progress": 0.85,
     "message": "string",
     "errors": [
       {
         "line": 42,
         "field": "profit",
         "message": "Invalid numeric value"
       }
     ]
   }

Analysis Endpoints
------------------

POST /analysis/performance
~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate comprehensive performance metrics from trade data.

**Request**

.. code-block:: http

   POST /api/v1/analysis/performance
   Content-Type: application/json

   {
     "file_id": "string",
     "parameters": {
       "robust_statistics": true,
       "include_equity_curve": true
     }
   }

**Parameters**

- ``file_id`` (string, required): Processed trade data file ID
- ``parameters`` (object, optional): Analysis configuration

**Response**

.. code-block:: json

   {
     "kpis": {
       "total_trades": 150,
       "win_probability": 0.65,
       "loss_probability": 0.35,
       "avg_win": 85.50,
       "avg_loss": 45.20,
       "win_loss_ratio": 1.89,
       "profit_factor": 1.85,
       "expectancy": 28.75,
       "max_drawdown": 1250.00,
       "sharpe_ratio": 1.23
     },
     "equity_curve": [
       {"timestamp": "2024-01-01", "equity": 10000.00},
       {"timestamp": "2024-01-02", "equity": 10085.50}
     ],
     "status": "completed"
   }

POST /analysis/kelly
~~~~~~~~~~~~~~~~~~~~

Calculate Kelly Criterion optimal risk fraction.

**Request**

.. code-block:: http

   POST /api/v1/analysis/kelly
   Content-Type: application/json

   {
     "performance_data": {
       "win_probability": 0.65,
       "win_loss_ratio": 1.89
     },
     "fractional_multiplier": 0.5
   }

**Parameters**

- ``performance_data`` (object, required): Performance metrics from analysis
- ``fractional_multiplier`` (float, optional): Kelly fraction multiplier (0.25-1.0)

**Response**

.. code-block:: json

   {
     "optimal_fraction": 0.012,
     "full_kelly_fraction": 0.024,
     "fractional_kelly_fraction": 0.012,
     "warnings": [
       "Risk fraction exceeds 2% - consider conservative approach"
     ],
     "confidence_interval": [0.010, 0.014]
   }

POST /analysis/optimal-f
~~~~~~~~~~~~~~~~~~~~~~~~

Calculate Optimal F position sizing.

**Request**

.. code-block:: http

   POST /api/v1/analysis/optimal-f
   Content-Type: application/json

   {
     "trade_data": [
       {"profit": 85.50, "loss": -45.20},
       {"profit": 92.30, "loss": -38.75}
     ],
     "parameters": {
       "precision": 0.001,
       "max_iterations": 1000
     }
   }

**Parameters**

- ``trade_data`` (array, required): Array of trade outcomes
- ``parameters`` (object, optional): Optimization settings

**Response**

.. code-block:: json

   {
     "optimal_f": 0.015,
     "terminal_wealth_relative": 1.234,
     "convergence_iterations": 45,
     "sensitivity_analysis": {
       "f_range": [0.010, 0.020],
       "twr_range": [1.189, 1.267]
     }
   }

Optimization Endpoints
----------------------

POST /optimization/challenge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run Monte Carlo simulation for prop firm challenge optimization.

**Request**

.. code-block:: http

   POST /api/v1/optimization/challenge
   Content-Type: application/json

   {
     "challenge_params": {
       "account_size": 100000.00,
       "profit_target_percent": 10.0,
       "max_daily_loss_percent": 5.0,
       "max_overall_loss_percent": 10.0,
       "min_trading_days": 30
     },
     "trade_data": [...],
     "simulation_count": 1000,
     "risk_fraction_range": {
       "min": 0.001,
       "max": 0.020,
       "step": 0.001
     }
   }

**Parameters**

- ``challenge_params`` (object, required): Challenge requirements
- ``trade_data`` (array, required): Historical trade data
- ``simulation_count`` (integer, optional): Number of simulations (default: 1000)
- ``risk_fraction_range`` (object, optional): Risk fraction testing range

**Response**

.. code-block:: json

   {
     "recommended_fraction": 0.012,
     "pass_rate": 0.78,
     "confidence_interval": [0.75, 0.81],
     "simulation_results": [
       {
         "risk_fraction": 0.010,
         "pass_rate": 0.72,
         "avg_drawdown": 0.085,
         "max_drawdown": 0.125
       }
     ],
     "processing_time_seconds": 45.2
   }

GET /optimization/status/{task_id}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check the status of a long-running optimization task.

**Request**

.. code-block:: http

   GET /api/v1/optimization/status/{task_id}

**Parameters**

- ``task_id`` (path, required): Task identifier from optimization request

**Response**

.. code-block:: json

   {
     "status": "running|completed|failed",
     "progress": 0.65,
     "eta_seconds": 120,
     "current_simulation": 650,
     "total_simulations": 1000
   }

MT5 Integration Endpoints
-------------------------

POST /mt5/connect
~~~~~~~~~~~~~~~~~

Establish connection to MT5 terminal.

**Request**

.. code-block:: http

   POST /api/v1/mt5/connect
   Content-Type: application/json

   {
     "timeout": 30,
     "account": "123456",
     "password": "secret",
     "server": "MetaQuotes-Demo"
   }

**Parameters**

- ``timeout`` (integer, optional): Connection timeout in seconds
- ``account`` (string, optional): MT5 account number
- ``password`` (string, optional): MT5 account password
- ``server`` (string, optional): MT5 server name

**Response**

.. code-block:: json

   {
     "connected": true,
     "account_info": {
       "balance": 10000.00,
       "equity": 9850.50,
       "margin": 1250.00,
       "free_margin": 8600.50
     },
     "connection_id": "mt5_conn_123"
   }

GET /mt5/account-info
~~~~~~~~~~~~~~~~~~~~~

Retrieve current MT5 account information.

**Request**

.. code-block:: http

   GET /api/v1/mt5/account-info

**Response**

.. code-block:: json

   {
     "balance": 10000.00,
     "equity": 9850.50,
     "margin": 1250.00,
     "free_margin": 8600.50,
     "margin_level": 788.04,
     "leverage": 100,
     "currency": "USD"
   }

POST /mt5/disconnect
~~~~~~~~~~~~~~~~~~~~

Disconnect from MT5 terminal.

**Request**

.. code-block:: http

   POST /api/v1/mt5/disconnect

**Response**

.. code-block:: json

   {
     "success": true,
     "message": "Disconnected from MT5"
   }

Report Endpoints
----------------

POST /reports/generate
~~~~~~~~~~~~~~~~~~~~~~

Generate analysis reports.

**Request**

.. code-block:: http

   POST /api/v1/reports/generate
   Content-Type: application/json

   {
     "report_type": "performance|optimization|comprehensive",
     "data": {...},
     "format": "pdf|csv|json",
     "include_charts": true
   }

**Parameters**

- ``report_type`` (string, required): Type of report to generate
- ``data`` (object, required): Analysis data for the report
- ``format`` (string, optional): Output format (default: pdf)
- ``include_charts`` (boolean, optional): Include charts in report

**Response**

.. code-block:: json

   {
     "report_id": "report_123",
     "download_url": "/api/v1/reports/download/report_123",
     "format": "pdf",
     "size_bytes": 245760
   }

GET /reports/download/{report_id}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download generated report.

**Request**

.. code-block:: http

   GET /api/v1/reports/download/{report_id}

**Parameters**

- ``report_id`` (path, required): Report identifier

**Response**

File download (PDF, CSV, or JSON depending on report format).

Error Handling
--------------

All API endpoints follow consistent error response format:

.. code-block:: json

   {
     "error": {
       "code": "VALIDATION_ERROR|PROCESSING_ERROR|CONNECTION_ERROR",
       "message": "Human-readable error description",
       "details": {
         "field": "file_id",
         "value": "invalid_id",
         "constraint": "must be valid UUID"
       }
     }
   }

**Common Error Codes**

- ``VALIDATION_ERROR`` (400): Invalid input parameters
- ``NOT_FOUND`` (404): Resource not found
- ``PROCESSING_ERROR`` (500): Internal processing error
- ``CONNECTION_ERROR`` (503): External service unavailable

Rate Limiting
-------------

- **Global Limit**: 100 requests per minute
- **Upload Limit**: 10 MB per file
- **Simulation Limit**: 10,000 simulations per request
- **Timeout**: 300 seconds for optimization tasks

WebSocket Endpoints
-------------------

WS /ws/analysis/{task_id}
~~~~~~~~~~~~~~~~~~~~~~~~~~

Real-time updates for long-running analysis tasks.

**Connection**

.. code-block:: javascript

   const ws = new WebSocket('ws://localhost:8000/ws/analysis/task_123');

**Messages**

.. code-block:: json

   {
     "type": "progress",
     "data": {
       "progress": 0.65,
       "current": 650,
       "total": 1000,
       "eta_seconds": 120
     }
   }

   {
     "type": "completed",
     "data": {
       "result": {...},
       "processing_time": 45.2
     }
   }

   {
     "type": "error",
     "data": {
       "message": "Simulation failed",
       "details": {...}
     }
   }

Python Client Example
---------------------

.. code-block:: python

   import requests
   from typing import Dict, Any

   class RiskOptimaClient:
       def __init__(self, base_url: str = "http://localhost:8000"):
           self.base_url = base_url

       def upload_trades(self, file_path: str) -> Dict[str, Any]:
           with open(file_path, 'rb') as f:
               response = requests.post(
                   f"{self.base_url}/api/v1/upload/trade-history",
                   files={'file': f}
               )
           return response.json()

       def analyze_performance(self, file_id: str) -> Dict[str, Any]:
           response = requests.post(
               f"{self.base_url}/api/v1/analysis/performance",
               json={"file_id": file_id}
           )
           return response.json()

       def optimize_challenge(self, file_id: str, challenge_params: Dict) -> Dict[str, Any]:
           # First get trade data
           perf_data = self.analyze_performance(file_id)

           response = requests.post(
               f"{self.base_url}/api/v1/optimization/challenge",
               json={
                   "challenge_params": challenge_params,
                   "trade_data": perf_data.get('trade_data', []),
                   "simulation_count": 1000
               }
           )
           return response.json()

   # Usage example
   client = RiskOptimaClient()
   result = client.upload_trades("trades.csv")
   file_id = result["file_id"]

   analysis = client.analyze_performance(file_id)
   print(f"Win Rate: {analysis['kpis']['win_probability']:.1%}")

   challenge_params = {
       "account_size": 100000,
       "profit_target_percent": 10,
       "max_daily_loss_percent": 5,
       "max_overall_loss_percent": 10,
       "min_trading_days": 30
   }

   optimization = client.optimize_challenge(file_id, challenge_params)
   print(f"Optimal Risk: {optimization['recommended_fraction']:.1%}")
   print(f"Success Rate: {optimization['pass_rate']:.1%}")

API Versioning
--------------

The API uses semantic versioning:

- **v1**: Current stable version
- **Breaking Changes**: Will be released as v2, v3, etc.
- **Backward Compatibility**: Maintained within major versions
- **Deprecation Notices**: 6 months notice for breaking changes

For the latest API documentation, visit ``http://localhost:8000/docs`` when the server is running.