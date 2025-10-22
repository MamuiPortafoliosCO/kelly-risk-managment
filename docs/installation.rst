Installation and Setup
====================

This guide will help you install and set up RiskOptima Engine on your system.

System Requirements
-------------------

**Operating System**
   - Windows 10/11 (64-bit) - Required for MT5 compatibility
   - Linux/macOS - Limited support (MT5 integration not available)

**Hardware Requirements**
   - **Processor**: Quad-core CPU (recommended: 8+ cores for simulations)
   - **Memory**: 8GB RAM minimum, 16GB recommended
   - **Storage**: 10GB free disk space
   - **Display**: 1920x1080 resolution minimum

**Software Prerequisites**
   - Python 3.9+
   - Rust 1.70+
   - MetaTrader 5 terminal (for live integration)
   - Visual C++ Redistributables (for Rust dependencies)

Installation Methods
-------------------

Method 1: Automated Setup (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install RiskOptima Engine is using the automated setup script:

.. code-block:: bash

   # Clone or download the project
   git clone https://github.com/your-repo/risk-optima-engine.git
   cd risk-optima-engine

   # Run the automated setup (builds Rust extension and installs dependencies)
   python -m risk_optima_engine setup

This command will:
- Install Python dependencies using uv
- Build the Rust core library
- Set up the development environment
- Run basic tests to verify installation

Method 2: Manual Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For advanced users or custom installations:

1. **Install Python Dependencies**

   .. code-block:: bash

      # Install uv package manager (if not already installed)
      pip install uv

      # Install dependencies
      uv sync

2. **Build Rust Core**

   .. code-block:: bash

      # Install Rust (if not already installed)
      curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

      # Build the Rust extension
      maturin develop

3. **Verify Installation**

   .. code-block:: bash

      # Run tests to verify everything works
      pytest

Docker Installation
-------------------

RiskOptima Engine can also be run using Docker for isolated environments:

.. code-block:: bash

   # Build the Docker image
   docker-compose build

   # Run the application
   docker-compose up

For more details, see :doc:`../DOCKER_DEPLOYMENT.md`.

MT5 Integration Setup
----------------------

To enable live MT5 integration features:

1. **Install MetaTrader 5 Terminal**

   Download and install MT5 from the official MetaQuotes website:
   https://www.metatrader5.com/en/download

2. **Configure MT5**

   - Launch MT5 terminal
   - Log in to your trading account
   - Enable automated trading if required
   - Note your account credentials for connection

3. **Test Connection**

   .. code-block:: bash

      # Test MT5 connection
      python -m risk_optima_engine mt5-test

Development Setup
-----------------

For developers contributing to the project:

1. **Clone Repository**

   .. code-block:: bash

      git clone https://github.com/your-repo/risk-optima-engine.git
      cd risk-optima-engine

2. **Set Up Development Environment**

   .. code-block:: bash

      # Install development dependencies
      uv sync --dev

      # Install pre-commit hooks
      pre-commit install

3. **Build Documentation**

   .. code-block:: bash

      # Install documentation dependencies
      pip install sphinx sphinx-rtd-theme myst-parser

      # Build documentation
      cd docs
      make html

4. **Run Development Server**

   .. code-block:: bash

      # Run full application in development mode
      python -m risk_optima_engine dev

Environment Configuration
-------------------------

Create a ``.env`` file in the project root for custom configuration:

.. code-block:: bash

   # MT5 Configuration
   MT5_TIMEOUT=30
   MT5_LOGIN=your_login
   MT5_PASSWORD=your_password
   MT5_SERVER=your_server

   # Application Configuration
   API_HOST=127.0.0.1
   API_PORT=8000
   FRONTEND_PORT=8501

   # Development Settings
   DEBUG=true
   LOG_LEVEL=INFO

Troubleshooting Installation
----------------------------

**Common Issues**

**Rust Build Failures**
   - Ensure Rust 1.70+ is installed: ``rustc --version``
   - Install Visual C++ Build Tools on Windows
   - Clear Rust cache: ``cargo clean``

**Python Dependency Issues**
   - Use uv for consistent dependency resolution
   - Create fresh virtual environment: ``uv venv``
   - Update pip: ``pip install --upgrade pip``

**MT5 Connection Issues**
   - Verify MT5 terminal is running
   - Check firewall settings for local connections
   - Ensure correct account credentials

**Permission Errors**
   - Run commands as administrator (Windows) or with sudo (Linux)
   - Check write permissions in project directory

**Performance Issues**
   - Ensure sufficient RAM (16GB recommended)
   - Close other resource-intensive applications
   - Use SSD storage for better performance

Next Steps
----------

After successful installation:

1. **Quick Start**: Run ``python -m risk_optima_engine full`` to launch the application
2. **Upload Data**: Import your MT5 trade history in the web interface
3. **Explore Features**: Try the performance analysis and risk modeling tools
4. **Read the Guide**: Continue with the :doc:`user_guide` for detailed usage instructions

For additional help, see the :doc:`troubleshooting` guide or check the GitHub issues.