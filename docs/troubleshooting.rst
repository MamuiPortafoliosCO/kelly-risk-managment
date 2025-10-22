Troubleshooting
===============

This guide helps you resolve common issues with RiskOptima Engine. If you can't find a solution here, check the GitHub issues or create a new issue.

Installation Issues
-------------------

Python Version Problems
~~~~~~~~~~~~~~~~~~~~~~~

**Error:** ``Python 3.9+ required but found 3.8``

**Solution:**

.. code-block:: bash

   # Check current Python version
   python --version

   # Install Python 3.9+ if needed
   # On Windows: Download from python.org
   # On Linux: sudo apt install python3.9
   # On macOS: brew install python@3.9

   # Use pyenv to manage multiple versions
   pyenv install 3.9.7
   pyenv global 3.9.7

**Error:** ``ModuleNotFoundError: No module named 'risk_optima_engine'``

**Solution:**

.. code-block:: bash

   # Reinstall the package
   pip uninstall risk-optima-engine
   pip install -e .

   # Or rebuild the Rust extension
   maturin develop --release

Rust Build Failures
~~~~~~~~~~~~~~~~~~~

**Error:** ``error: linker 'link.exe' not found``

**Solution:** Install Visual Studio Build Tools on Windows:

1. Download Visual Studio Build Tools
2. Install with "Desktop development with C++" workload
3. Restart command prompt and try again

**Error:** ``error: could not find 'rustc'``

**Solution:**

.. code-block:: bash

   # Install Rust
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   source ~/.cargo/env

   # Verify installation
   rustc --version
   cargo --version

**Error:** ``error[E0658]: use of unstable library feature``

**Solution:** Update Rust to the latest stable version:

.. code-block:: bash

   rustup update stable
   rustup default stable

Dependency Issues
~~~~~~~~~~~~~~~~~

**Error:** ``ResolutionImpossible: Can't install dependencies``

**Solution:**

.. code-block:: bash

   # Clear pip cache
   pip cache purge

   # Use uv for better dependency resolution
   uv sync --reinstall

   # Or upgrade pip and setuptools
   pip install --upgrade pip setuptools wheel

**Error:** ``ImportError: DLL load failed``

**Solution:** Install Microsoft Visual C++ Redistributables:

1. Download from Microsoft's website
2. Install the latest version (64-bit)
3. Restart your system

Startup Issues
--------------

Application Won't Start
~~~~~~~~~~~~~~~~~~~~~~~~

**Error:** ``Port already in use``

**Solution:**

.. code-block:: bash

   # Find process using the port
   netstat -ano | findstr :8000  # Windows
   lsof -i :8000                  # Linux/macOS

   # Kill the process
   taskkill /PID <PID> /F         # Windows
   kill -9 <PID>                 # Linux/macOS

   # Or change ports
   export API_PORT=8001
   export FRONTEND_PORT=8502

**Error:** ``Address already in use``

**Solution:** Wait for the previous instance to fully shut down, or force kill:

.. code-block:: bash

   # Find and kill all related processes
   pkill -f risk_optima_engine    # Linux/macOS
   taskkill /F /IM python.exe     # Windows (be careful!)

**Error:** ``Permission denied``

**Solution:**

.. code-block:: bash

   # Run with appropriate permissions
   sudo python -m risk_optima_engine full  # Linux/macOS

   # Or run as administrator on Windows
   # Right-click command prompt > Run as administrator

File Upload Issues
------------------

Invalid File Format
~~~~~~~~~~~~~~~~~~~

**Error:** ``Unsupported file format``

**Solution:**

- Ensure file has .csv or .xml extension
- Check that it's a valid MT5 export file
- Verify the file isn't corrupted
- Try re-exporting from MT5

**Supported Formats:**

.. code-block:: text

   CSV: Standard MT5 export with headers
   XML: MT5's XML export format

**Error:** ``File too large``

**Solution:**

.. code-block:: bash

   # Increase file size limit
   export MAX_FILE_SIZE_MB=50

   # Or split large files into smaller chunks
   # Process files separately

Data Parsing Errors
~~~~~~~~~~~~~~~~~~~

**Error:** ``Invalid numeric value in column X``

**Solution:**

- Check for non-numeric characters in numeric columns
- Ensure correct decimal separator (use . not ,)
- Remove any header rows or extra text
- Verify date formats are consistent

**Common Data Issues:**

.. code-block:: text

   Profit column: Should contain numbers like 85.50 or -45.20
   Volume column: Should contain positive numbers like 0.10 or 100
   Date columns: Should be in YYYY-MM-DD format

**Error:** ``Missing required columns``

**Solution:**

Required columns for CSV files:

.. code-block:: csv

   Symbol,Type,Volume,Open Price,Close Price,Profit

Optional but recommended:

.. code-block:: csv

   Commission,Swap,Ticket,Open Time,Close Time

MT5 Integration Issues
----------------------

Connection Failures
~~~~~~~~~~~~~~~~~~~

**Error:** ``MT5 terminal not found``

**Solution:**

1. **Install MT5 Terminal:**

   - Download from https://www.metatrader5.com/en/download
   - Install in default location
   - Run MT5 at least once to complete setup

2. **Verify MT5 is Running:**

   .. code-block:: bash

      # Check if MT5 processes are running
      tasklist | findstr terminal64  # Windows
      ps aux | grep terminal64       # Linux

3. **Enable Automation:**

   - Open MT5 terminal
   - Go to Tools → Options → Expert Advisors
   - Check "Allow automated trading"
   - Check "Allow DLL imports"

**Error:** ``MT5 login failed``

**Solution:**

.. code-block:: bash

   # Set correct credentials
   export MT5_LOGIN=123456
   export MT5_PASSWORD=your_password
   export MT5_SERVER=MetaQuotes-Demo

   # Or use demo account for testing
   # Create demo account in MT5 terminal

**Error:** ``Connection timeout``

**Solution:**

.. code-block:: bash

   # Increase timeout
   export MT5_TIMEOUT=60

   # Check network connectivity
   ping mt5.server.address

   # Verify firewall settings
   # Allow MT5 through firewall

Live Data Issues
~~~~~~~~~~~~~~~~

**Error:** ``No account data available``

**Solution:**

- Ensure you're logged into MT5
- Verify account has trading history
- Check account permissions
- Try reconnecting to MT5

**Error:** ``Real-time data not updating``

**Solution:**

- Check MT5 connection status in the UI
- Verify internet connectivity
- Restart MT5 terminal
- Check MT5 server status

Performance Issues
------------------

Slow Computations
~~~~~~~~~~~~~~~~~

**Error:** ``Simulations taking too long``

**Solution:**

.. code-block:: bash

   # Reduce simulation count
   export MAX_SIMULATIONS=1000

   # Increase thread pool size
   export THREAD_POOL_SIZE=8

   # Use faster settings for testing
   export SIMULATION_BATCH_SIZE=500

**Error:** ``Out of memory``

**Solution:**

.. code-block:: bash

   # Reduce memory usage
   export CACHE_SIZE_MB=50
   export MAX_SIMULATIONS=5000

   # Close other applications
   # Add more RAM to system

**Error:** ``High CPU usage``

**Solution:**

- Reduce thread pool size
- Lower simulation parameters
- Check for infinite loops in custom code
- Update to latest version

Analysis Issues
---------------

Calculation Errors
~~~~~~~~~~~~~~~~~~

**Error:** ``Division by zero in Kelly calculation``

**Solution:**

- Check for trades with zero or negative win rates
- Ensure sufficient trading history (minimum 10-20 trades)
- Review data for outliers or errors

**Error:** ``Invalid risk fraction``

**Solution:**

- Risk fractions should be between 0.001 and 0.05
- Check Kelly calculation inputs
- Verify win/loss ratio is positive

**Error:** ``Monte Carlo simulation failed``

**Solution:**

- Reduce number of simulations
- Check input parameters are valid
- Ensure sufficient historical data
- Try with different challenge parameters

Visualization Issues
--------------------

Charts Not Loading
~~~~~~~~~~~~~~~~~~

**Error:** ``Plotly chart failed to render``

**Solution:**

.. code-block:: bash

   # Update Plotly
   pip install --upgrade plotly

   # Check browser compatibility
   # Try different browser (Chrome recommended)

   # Clear browser cache
   # Disable browser extensions temporarily

**Error:** ``Export failed``

**Solution:**

- Check write permissions in output directory
- Ensure sufficient disk space
- Try different export formats
- Update matplotlib/plotly if needed

API Issues
----------

Endpoint Errors
~~~~~~~~~~~~~~~

**Error:** ``404 Not Found``

**Solution:**

- Verify correct API endpoint URL
- Check API server is running on correct port
- Review API documentation for correct paths

**Error:** ``422 Validation Error``

**Solution:**

- Check request payload format
- Verify required fields are present
- Ensure data types are correct
- Review API documentation for parameter requirements

**Error:** ``500 Internal Server Error``

**Solution:**

.. code-block:: bash

   # Check application logs
   tail -f logs/risk_optima_engine.log

   # Restart the application
   python -m risk_optima_engine backend

   # Check system resources
   top  # Linux
   taskmgr  # Windows

WebSocket Issues
~~~~~~~~~~~~~~~~

**Error:** ``WebSocket connection failed``

**Solution:**

- Check if backend server supports WebSockets
- Verify correct WebSocket URL (ws://localhost:8000/ws/...)
- Check firewall settings for WebSocket connections
- Try different browser

Docker Issues
-------------

Container Won't Start
~~~~~~~~~~~~~~~~~~~~~

**Error:** ``docker-compose up failed``

**Solution:**

.. code-block:: bash

   # Check Docker is running
   docker --version
   docker-compose --version

   # Rebuild containers
   docker-compose down
   docker-compose build --no-cache
   docker-compose up

   # Check container logs
   docker-compose logs

**Error:** ``Port binding failed``

**Solution:**

.. code-block:: bash

   # Change host ports in docker-compose.yml
   ports:
     - "8001:8000"  # Host:Container
     - "8502:8501"

   # Or stop services using those ports
   sudo lsof -i :8000 | xargs kill -9

**Error:** ``Permission denied in container``

**Solution:**

- Ensure proper file permissions on mounted volumes
- Run container with appropriate user permissions
- Check Docker Desktop settings on Windows/macOS

Development Issues
------------------

Testing Failures
~~~~~~~~~~~~~~~~

**Error:** ``pytest collection failed``

**Solution:**

.. code-block:: bash

   # Install test dependencies
   uv sync --dev

   # Run tests with verbose output
   pytest -v

   # Check specific test
   pytest tests/test_specific.py::test_function -s

**Error:** ``Rust tests failed``

**Solution:**

.. code-block:: bash

   # Run Rust tests
   cargo test --verbose

   # Check for specific test
   cargo test test_function_name

   # Run with backtrace
   RUST_BACKTRACE=1 cargo test

Code Quality Issues
~~~~~~~~~~~~~~~~~~~

**Error:** ``Linting failed``

**Solution:**

.. code-block:: bash

   # Run linters
   flake8 src/                    # Python
   cargo clippy                   # Rust

   # Auto-fix issues
   black src/                     # Python formatting
   cargo fmt                      # Rust formatting

**Error:** ``Type checking failed``

**Solution:**

.. code-block:: bash

   # Run type checker
   mypy src/risk_optima_engine/

   # Or use pyright
   pyright src/

Build Issues
~~~~~~~~~~~~

**Error:** ``Build failed``

**Solution:**

.. code-block:: bash

   # Clean and rebuild
   rm -rf build/ dist/ target/
   uv build

   # For Rust
   cargo clean
   cargo build --release

   # Check build logs for specific errors
   uv build --verbose

Logging and Debugging
---------------------

Enable Debug Logging
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Set debug level
   export LOG_LEVEL=DEBUG
   export DEBUG=true

   # Restart application
   python -m risk_optima_engine full

Check Application Logs
~~~~~~~~~~~~~~~~~~~~~~

**Default Log Locations:**

- Linux/macOS: ``~/.risk_optima_engine/logs/``
- Windows: ``%APPDATA%\risk_optima_engine\logs\``

**View Recent Logs:**

.. code-block:: bash

   # Linux/macOS
   tail -f ~/.risk_optima_engine/logs/risk_optima_engine.log

   # Windows PowerShell
   Get-Content $env:APPDATA\risk_optima_engine\logs\risk_optima_engine.log -Wait

**Log Levels:**

- ``DEBUG``: Detailed diagnostic information
- ``INFO``: General information about application operation
- ``WARNING``: Warning messages for potential issues
- ``ERROR``: Error messages for failures
- ``CRITICAL``: Critical errors that may cause application failure

Generate Debug Report
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Collect system information
   python -c "
   import sys, platform
   print('Python version:', sys.version)
   print('Platform:', platform.platform())
   print('Architecture:', platform.architecture())
   "

   # Collect dependency versions
   pip list | grep -E '(fastapi|streamlit|numpy|pandas)'

   # Collect Rust information
   rustc --version
   cargo --version

System Diagnostics
------------------

Check System Resources
~~~~~~~~~~~~~~~~~~~~~~

**Memory Usage:**

.. code-block:: bash

   # Linux
   free -h
   vmstat 1

   # Windows PowerShell
   Get-Counter '\Memory\Available MBytes'
   Get-Process | Sort-Object -Property WS -Descending | Select-Object -First 10

**Disk Space:**

.. code-block:: bash

   # Linux
   df -h

   # Windows
   wmic logicaldisk get size,freespace,caption

**CPU Usage:**

.. code-block:: bash

   # Linux
   top
   htop  # if installed

   # Windows
   taskmgr

Network Diagnostics
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Test connectivity
   ping 8.8.8.8

   # Check DNS resolution
   nslookup google.com

   # Test MT5 server connectivity (if applicable)
   ping mt5.server.address

Getting Help
------------

If these solutions don't resolve your issue:

1. **Check GitHub Issues:** Search for similar problems
2. **Create an Issue:** Provide detailed information including:
   - Operating system and version
   - Python/Rust versions
   - Full error message and traceback
   - Steps to reproduce the issue
   - Application logs
   - System resource usage

3. **Community Support:** Check Discord or forum discussions

4. **Professional Support:** Contact the development team for enterprise support

**Debug Information to Include:**

.. code-block:: bash

   # System information
   python -c "import platform; print(platform.uname())"

   # Python packages
   pip freeze | grep -E '(risk-optima-engine|fastapi|uvicorn|streamlit)'

   # Rust version
   rustc --version

   # Error logs
   # Include full traceback and any relevant log entries