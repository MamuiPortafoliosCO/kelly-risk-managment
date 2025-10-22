Configuration
=============

RiskOptima Engine can be configured through environment variables, configuration files, and runtime parameters. This guide covers all available configuration options.

Environment Variables
---------------------

Core Application Settings
~~~~~~~~~~~~~~~~~~~~~~~~~

**API Configuration**

.. code-block:: bash

   # Backend server settings
   API_HOST=127.0.0.1          # Server host (default: 127.0.0.1)
   API_PORT=8000               # Server port (default: 8000)
   API_WORKERS=4               # Number of worker processes (default: 4)

   # Frontend settings
   FRONTEND_HOST=127.0.0.1     # Frontend host (default: 127.0.0.1)
   FRONTEND_PORT=8501          # Frontend port (default: 8501)

   # Application settings
   DEBUG=false                 # Enable debug mode (default: false)
   LOG_LEVEL=INFO              # Logging level (DEBUG, INFO, WARNING, ERROR)
   SECRET_KEY=your-secret-key   # Secret key for sessions (auto-generated if not set)

MT5 Integration Settings
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Connection settings
   MT5_TIMEOUT=30              # Connection timeout in seconds (default: 30)
   MT5_RECONNECT_ATTEMPTS=3    # Number of reconnection attempts (default: 3)
   MT5_RECONNECT_DELAY=5       # Delay between reconnection attempts (default: 5)

   # Account credentials (optional - can be set at runtime)
   MT5_LOGIN=123456            # MT5 account number
   MT5_PASSWORD=your_password  # MT5 account password
   MT5_SERVER=MetaQuotes-Demo  # MT5 server name

Performance Settings
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Computation settings
   MAX_SIMULATIONS=10000       # Maximum Monte Carlo simulations (default: 10000)
   SIMULATION_BATCH_SIZE=1000  # Batch size for parallel processing (default: 1000)
   THREAD_POOL_SIZE=8          # Number of threads for computations (default: CPU cores)

   # Memory management
   MAX_FILE_SIZE_MB=10         # Maximum upload file size in MB (default: 10)
   CACHE_SIZE_MB=100           # Result cache size in MB (default: 100)
   CLEANUP_INTERVAL_HOURS=24   # Temporary file cleanup interval (default: 24)

Data Processing Settings
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # File processing
   SUPPORTED_FORMATS=csv,xml,json  # Supported file formats
   AUTO_DETECT_FORMAT=true         # Auto-detect file format (default: true)
   VALIDATE_DATA=true              # Enable data validation (default: true)

   # Parsing options
   DATE_FORMAT=%Y-%m-%d            # Expected date format
   DECIMAL_SEPARATOR=.              # Decimal separator (default: .)
   CSV_DELIMITER=,                  # CSV field delimiter (default: ,)

Security Settings
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # CORS settings (for local development)
   CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
   CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
   CORS_HEADERS=Content-Type,Authorization

   # Rate limiting
   RATE_LIMIT_REQUESTS=100         # Requests per minute (default: 100)
   RATE_LIMIT_BURST=20             # Burst allowance (default: 20)

   # Encryption
   ENCRYPT_TEMP_FILES=true         # Encrypt temporary files (default: true)
   ENCRYPTION_KEY=auto             # Encryption key (auto-generated if not set)

Configuration File
------------------

You can also configure RiskOptima Engine using a TOML configuration file:

.. code-block:: toml

   # config.toml
   [api]
   host = "127.0.0.1"
   port = 8000
   workers = 4

   [frontend]
   host = "127.0.0.1"
   port = 8501

   [mt5]
   timeout = 30
   reconnect_attempts = 3
   reconnect_delay = 5

   [performance]
   max_simulations = 10000
   simulation_batch_size = 1000
   thread_pool_size = 8

   [data]
   max_file_size_mb = 10
   supported_formats = ["csv", "xml", "json"]
   auto_detect_format = true

   [security]
   encrypt_temp_files = true
   rate_limit_requests = 100

To use a configuration file, set the ``CONFIG_FILE`` environment variable:

.. code-block:: bash

   export CONFIG_FILE=/path/to/config.toml
   python -m risk_optima_engine full

Runtime Configuration
---------------------

Challenge Parameters
~~~~~~~~~~~~~~~~~~~~

Configure prop firm challenge requirements through the web interface or API:

.. code-block:: json

   {
     "account_size": 100000.00,
     "profit_target_percent": 10.0,
     "max_daily_loss_percent": 5.0,
     "max_overall_loss_percent": 10.0,
     "min_trading_days": 30,
     "max_trading_days": 90,
     "reset_daily_loss": true,
     "allow_weekend_holding": false
   }

**Parameter Explanations:**

- ``account_size``: Initial account balance in base currency
- ``profit_target_percent``: Required profit percentage to pass challenge
- ``max_daily_loss_percent``: Maximum loss allowed in a single trading day
- ``max_overall_loss_percent``: Maximum total drawdown from peak balance
- ``min_trading_days``: Minimum number of trading days required
- ``max_trading_days``: Maximum allowed trading days (optional)
- ``reset_daily_loss``: Whether daily loss limits reset each day
- ``allow_weekend_holding``: Whether positions can be held over weekends

Risk Model Settings
~~~~~~~~~~~~~~~~~~~

Configure risk calculation parameters:

.. code-block:: json

   {
     "kelly_fraction": 1.0,
     "use_fractional_kelly": true,
     "robust_statistics": true,
     "outlier_threshold": 3.0,
     "confidence_level": 0.95,
     "bootstrap_samples": 1000
   }

**Parameter Explanations:**

- ``kelly_fraction``: Kelly multiplier (0.25 = quarter Kelly, 1.0 = full Kelly)
- ``use_fractional_kelly``: Use fractional Kelly for reduced volatility
- ``robust_statistics``: Use median-based calculations for outlier resistance
- ``outlier_threshold``: Standard deviation threshold for outlier detection
- ``confidence_level``: Statistical confidence level for intervals
- ``bootstrap_samples``: Number of bootstrap samples for confidence intervals

Visualization Settings
~~~~~~~~~~~~~~~~~~~~~~~

Customize chart appearance and behavior:

.. code-block:: json

   {
     "theme": "light",
     "color_scheme": "default",
     "chart_height": 400,
     "show_grid": true,
     "enable_zoom": true,
     "export_formats": ["png", "svg", "pdf"],
     "date_format": "%Y-%m-%d",
     "currency_symbol": "$",
     "locale": "en-US"
   }

**Parameter Explanations:**

- ``theme``: Chart theme (light, dark, auto)
- ``color_scheme``: Color palette for charts
- ``chart_height``: Default chart height in pixels
- ``show_grid``: Display grid lines on charts
- ``enable_zoom``: Allow zoom and pan interactions
- ``export_formats``: Supported export formats
- ``date_format``: Date display format
- ``currency_symbol``: Currency symbol for displays
- ``locale``: Localization settings

Docker Configuration
--------------------

When using Docker, configuration can be passed through environment variables or mounted config files:

**docker-compose.yml**

.. code-block:: yaml

   version: '3.8'
   services:
     risk-optima-engine:
       image: risk-optima-engine:latest
       environment:
         - API_PORT=8000
         - FRONTEND_PORT=8501
         - MT5_TIMEOUT=30
         - DEBUG=false
       volumes:
         - ./config.toml:/app/config.toml:ro
         - ./data:/app/data
       ports:
         - "8000:8000"
         - "8501:8501"

**Environment File**

Create a ``.env`` file for Docker:

.. code-block:: bash

   # .env
   API_HOST=0.0.0.0
   API_PORT=8000
   FRONTEND_HOST=0.0.0.0
   FRONTEND_PORT=8501
   MT5_TIMEOUT=30
   DEBUG=false
   LOG_LEVEL=INFO

Development Configuration
-------------------------

For development environments, use these settings:

.. code-block:: bash

   # Development settings
   export DEBUG=true
   export LOG_LEVEL=DEBUG
   export API_HOST=127.0.0.1
   export API_PORT=8000
   export FRONTEND_HOST=127.0.0.1
   export FRONTEND_PORT=8501

   # Relaxed security for development
   export CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
   export RATE_LIMIT_REQUESTS=1000

   # Development database (if applicable)
   export DATABASE_URL=sqlite:///dev.db

Production Configuration
------------------------

For production deployments, use these security-focused settings:

.. code-block:: bash

   # Production settings
   export DEBUG=false
   export LOG_LEVEL=WARNING
   export SECRET_KEY=$(openssl rand -hex 32)

   # Security hardening
   export ENCRYPT_TEMP_FILES=true
   export RATE_LIMIT_REQUESTS=100
   export API_WORKERS=8

   # Performance optimization
   export THREAD_POOL_SIZE=16
   export MAX_SIMULATIONS=50000
   export CACHE_SIZE_MB=500

Configuration Validation
------------------------

RiskOptima Engine validates configuration on startup and reports any issues:

**Common Validation Errors:**

- **Invalid Port Numbers**: Ports must be between 1024-65535
- **Invalid File Paths**: Configuration files must exist and be readable
- **Invalid MT5 Credentials**: Account numbers must be numeric
- **Invalid Percentages**: Risk percentages must be between 0-100
- **Invalid Memory Settings**: Values must be positive and reasonable

**Validation Example:**

.. code-block:: bash

   $ python -m risk_optima_engine full
   INFO: Validating configuration...
   ERROR: Invalid MT5_TIMEOUT: must be positive integer
   ERROR: Invalid API_PORT: port 80 requires elevated privileges
   CRITICAL: Configuration validation failed. Exiting.

Configuration Precedence
------------------------

Configuration values are loaded in this order (later sources override earlier ones):

1. **Default Values**: Built-in defaults
2. **Configuration File**: TOML file specified by ``CONFIG_FILE``
3. **Environment Variables**: System environment variables
4. **Runtime Parameters**: API parameters and web interface settings
5. **Command Line Arguments**: CLI flags (highest precedence)

**Example Precedence:**

.. code-block:: bash

   # 1. Default: API_PORT=8000
   # 2. Config file: API_PORT=9000
   # 3. Environment: export API_PORT=8080
   # 4. Runtime: API parameter port=8501
   # Result: API runs on port 8501

Dynamic Configuration
---------------------

Some settings can be changed at runtime through the web interface:

**Real-time Settings:**

- MT5 connection parameters
- Challenge optimization settings
- Visualization preferences
- Export format options

**Persistent Settings:**

Settings that persist across sessions are stored in:

- ``~/.risk_optima_engine/config.json`` (user preferences)
- ``~/.risk_optima_engine/cache/`` (computed results cache)
- ``/tmp/risk_optima_engine/`` (temporary files)

Configuration Backup and Restore
---------------------------------

**Backup Configuration:**

.. code-block:: bash

   # Backup user configuration
   cp ~/.risk_optima_engine/config.json config_backup.json

   # Backup environment variables
   env | grep RISK_OPTIMA > env_backup.txt

**Restore Configuration:**

.. code-block:: bash

   # Restore user configuration
   mkdir -p ~/.risk_optima_engine
   cp config_backup.json ~/.risk_optima_engine/config.json

   # Restore environment variables
   source env_backup.txt

Troubleshooting Configuration
-----------------------------

**Configuration Not Loading:**

.. code-block:: bash

   # Check configuration file syntax
   python -c "import tomllib; tomllib.load(open('config.toml', 'rb'))"

   # Validate environment variables
   python -c "import os; print(os.environ.get('API_PORT', 'Not set'))"

**MT5 Connection Issues:**

.. code-block:: bash

   # Test MT5 configuration
   python -c "
   import os
   print('MT5_TIMEOUT:', os.environ.get('MT5_TIMEOUT', '30'))
   print('MT5_LOGIN:', os.environ.get('MT5_LOGIN', 'Not set'))
   print('MT5_SERVER:', os.environ.get('MT5_SERVER', 'Not set'))
   "

**Performance Issues:**

.. code-block:: bash

   # Check performance settings
   python -c "
   import os
   print('THREAD_POOL_SIZE:', os.environ.get('THREAD_POOL_SIZE', 'auto'))
   print('MAX_SIMULATIONS:', os.environ.get('MAX_SIMULATIONS', '10000'))
   print('CACHE_SIZE_MB:', os.environ.get('CACHE_SIZE_MB', '100'))
   "

**Permission Issues:**

.. code-block:: bash

   # Check file permissions
   ls -la ~/.risk_optima_engine/
   ls -la /tmp/risk_optima_engine/

   # Fix permissions
   chmod 755 ~/.risk_optima_engine/
   chmod 1777 /tmp/risk_optima_engine/

For additional help with configuration, see the :doc:`troubleshooting` guide.