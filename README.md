# RiskOptima Engine

*Quantitative Risk Analysis and Management Tool for MT5 Traders*

RiskOptima Engine is a comprehensive, locally-hosted risk analysis and management tool designed for stock market traders using the MetaTrader 5 (MT5) platform. It empowers traders to make data-driven decisions on position sizing by analyzing historical performance and calculating optimal risk parameters.

## Features

### Core Functionality
- **Historical Data Ingestion**: Parse and validate MT5 trade history files (CSV/XML)
- **Performance Analysis**: Calculate comprehensive statistical KPIs and metrics
- **Risk Modeling**: Implement Kelly Criterion and Optimal F position sizing algorithms
- **Challenge Optimization**: Monte Carlo simulation for prop firm challenge success
- **Real-time Integration**: Live MT5 account monitoring and data retrieval
- **Reporting & Visualization**: Interactive charts and exportable reports

### Key Algorithms
- **Kelly Criterion**: Mathematical formula for optimal bet sizing
- **Optimal F**: Ralph Vince's position sizing method for maximum geometric growth
- **Monte Carlo Simulation**: Statistical modeling for challenge success probability
- **Robust Statistics**: Outlier-resistant calculations for reliable risk metrics

## Architecture

RiskOptima Engine follows a modern three-tier architecture:

- **Frontend**: Streamlit-based GUI for user interaction
- **Backend**: FastAPI server with async processing
- **Quantitative Core**: High-performance Rust library for computations

All processing occurs locally on the user's machine, ensuring data privacy and low latency.

## Installation

### Prerequisites
- Python 3.9+
- Rust 1.70+
- MetaTrader 5 terminal (for live integration)
- Windows 10/11 (MT5 requirement)

### Setup
```bash
# Clone or download the project
cd risk-optima-engine

# Set up environment (builds Rust extension and installs dependencies)
python -m risk_optima_engine setup

# Or manually:
uv sync
maturin develop
```

## Usage

### Quick Start
```bash
# Run full application (backend + frontend)
python -m risk_optima_engine full

# Or run components separately:
python -m risk_optima_engine backend  # API server on port 8000
python -m risk_optima_engine frontend # Streamlit UI on port 8501
```

### Workflow
1. **Data Upload**: Import your MT5 trade history (CSV or XML format)
2. **Performance Analysis**: View comprehensive KPIs and equity curves
3. **Risk Modeling**: Calculate optimal position sizing with Kelly/Optimal F
4. **Challenge Optimization**: Simulate prop firm challenge success rates
5. **Live Monitoring**: Connect to MT5 for real-time account data
6. **Reporting**: Generate and export analysis reports

## API Documentation

The backend provides a RESTful API with the following endpoints:

### File Operations
- `POST /api/v1/upload/trade-history` - Upload trade history files
- `GET /api/v1/upload/status/{file_id}` - Check upload status

### Analysis
- `POST /api/v1/analysis/performance` - Calculate performance metrics
- `POST /api/v1/analysis/kelly` - Kelly Criterion calculation
- `POST /api/v1/analysis/optimal-f` - Optimal F calculation

### Optimization
- `POST /api/v1/optimization/challenge` - Monte Carlo challenge simulation

### MT5 Integration
- `POST /api/v1/mt5/connect` - Connect to MT5 terminal
- `GET /api/v1/mt5/account-info` - Get account information

### Reports
- `POST /api/v1/reports/generate` - Generate analysis reports
- `GET /api/v1/reports/download/{report_id}` - Download reports

## Configuration

### Environment Variables
- `MT5_TIMEOUT` - MT5 connection timeout (default: 30s)
- `API_HOST` - Backend server host (default: 127.0.0.1)
- `API_PORT` - Backend server port (default: 8000)

### Challenge Parameters
Configure prop firm challenge requirements:
- Account size
- Profit target percentage
- Maximum daily/overall loss limits
- Minimum trading days

## Development

### Project Structure
```
risk-optima-engine/
├── src/
│   └── risk_optima_engine/
│       ├── __init__.py          # Package exports
│       ├── main.py             # CLI entry point
│       ├── backend.py          # FastAPI server
│       ├── frontend.py         # Streamlit UI
│       ├── mt5_integration.py  # MT5 connection
│       └── _core.pyi           # Type stubs
├── src/lib.rs                  # Rust core library
├── pyproject.toml              # Python configuration
├── Cargo.toml                  # Rust configuration
└── README.md
```

### Building
```bash
# Build Rust extension
maturin develop

# Install Python dependencies
uv sync

# Run tests
pytest
```

### Testing
```bash
# Run Python tests
pytest

# Run Rust tests
cargo test
```

## Performance

- **Computation Speed**: <60 seconds for Monte Carlo simulations (1000+ runs)
- **Memory Usage**: <500MB for typical usage scenarios
- **Scalability**: Handles up to 10,000 trades efficiently
- **Parallel Processing**: Utilizes multiple CPU cores for simulations

## Security

- **Local Processing**: All data processing occurs on user's machine
- **No External Transmission**: Trade data never leaves the local environment
- **Encrypted Storage**: Sensitive data encrypted when persisted
- **Input Validation**: Comprehensive validation of all user inputs

## License

This project is proprietary software. See LICENSE file for details.

## Support

For support and documentation:
- Check the inline code documentation
- Review the API documentation at `http://localhost:8000/docs` when running
- Ensure MT5 terminal is running for live integration features

## Version History

- **v1.1.0**: Initial release with full feature set
  - Historical data analysis
  - Kelly Criterion and Optimal F implementation
  - Monte Carlo challenge optimization
  - MT5 integration
  - Streamlit frontend
  - FastAPI backend
  - Rust performance core