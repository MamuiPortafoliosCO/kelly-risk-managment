Developer Guide
==============

This guide provides information for developers who want to contribute to RiskOptima Engine, understand the codebase, or extend its functionality.

Project Structure
-----------------

.. code-block:: text

   risk-optima-engine/
   ├── src/
   │   ├── lib.rs                    # Rust core library entry point
   │   └── risk_optima_engine/       # Python package
   │       ├── __init__.py           # Package initialization
   │       ├── _core.pyi             # Type stubs for Rust functions
   │       ├── main.py               # CLI entry point
   │       ├── backend.py            # FastAPI server
   │       ├── frontend.py           # Streamlit GUI
   │       ├── mt5_integration.py    # MT5 connection logic
   │       ├── mt5_live_data.py      # Live data fetching
   │       └── core.py               # Core business logic
   ├── pyproject.toml                # Python project configuration
   ├── Cargo.toml                    # Rust project configuration
   ├── docs/                         # Documentation
   ├── tests/                        # Test suites
   ├── scripts/                      # Build and deployment scripts
   └── uv.lock                       # Dependency lock file

Architecture Overview
---------------------

RiskOptima Engine follows a three-tier architecture:

**Frontend Layer (Python/Streamlit)**
   - User interface and data visualization
   - File upload and parameter input
   - Results display and export

**Backend Layer (Python/FastAPI)**
   - REST API for client communication
   - Request validation and orchestration
   - MT5 integration management

**Core Layer (Rust)**
   - High-performance mathematical computations
   - Statistical analysis and Monte Carlo simulations
   - Memory-efficient data processing

Development Environment Setup
------------------------------

Prerequisites
~~~~~~~~~~~~~

- **Python 3.9+** with pip
- **Rust 1.70+** with Cargo
- **Git** for version control
- **Visual Studio Code** (recommended) with Python and Rust extensions

Clone and Setup
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/your-repo/risk-optima-engine.git
   cd risk-optima-engine

   # Set up Python environment
   uv sync

   # Install development dependencies
   uv sync --dev

   # Build Rust extension
   maturin develop

   # Install pre-commit hooks
   pre-commit install

   # Run tests to verify setup
   pytest
   cargo test

Code Style and Standards
------------------------

Python Code Style
~~~~~~~~~~~~~~~~~

The project follows PEP 8 with some modifications:

.. code-block:: python

   # Good: Descriptive variable names
   def calculate_optimal_risk_fraction(win_probability, win_loss_ratio):
       return win_probability - (1 - win_probability) / win_loss_ratio

   # Bad: Undescriptive names
   def calc_f(wp, wlr):
       return wp - (1 - wp) / wlr

**Key Guidelines:**

- **Line Length**: 88 characters (Black default)
- **Imports**: Use absolute imports, group by type
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Required for all function parameters and return values
- **Naming**: snake_case for variables/functions, PascalCase for classes

Rust Code Style
~~~~~~~~~~~~~~~

Follow the official Rust style guidelines:

.. code-block:: rust

   // Good: Clear, descriptive function names
   pub fn calculate_kelly_criterion(
       win_probability: f64,
       win_loss_ratio: f64,
   ) -> f64 {
       win_probability - (1.0 - win_probability) / win_loss_ratio
   }

   // Bad: Unclear abbreviations
   pub fn calc_kelly(wp: f64, wlr: f64) -> f64 {
       wp - (1.0 - wp) / wlr
   }

**Key Guidelines:**

- **Formatting**: Use ``cargo fmt`` for consistent formatting
- **Linting**: Use ``cargo clippy`` for code quality checks
- **Documentation**: Document all public APIs with ``///`` comments
- **Error Handling**: Use ``Result`` and ``Option`` types appropriately
- **Memory Safety**: Leverage Rust's ownership system

Development Workflow
--------------------

Feature Development
~~~~~~~~~~~~~~~~~~~

1. **Create Feature Branch**

   .. code-block:: bash

      git checkout -b feature/new-risk-model
      git push -u origin feature/new-risk-model

2. **Implement Changes**

   - Write tests first (TDD approach)
   - Implement functionality
   - Update documentation
   - Run full test suite

3. **Code Quality Checks**

   .. code-block:: bash

      # Run Python tests
      pytest

      # Run Rust tests
      cargo test

      # Check code formatting
      black . --check
      cargo fmt --check

      # Run linters
      flake8
      cargo clippy

4. **Update Documentation**

   .. code-block:: bash

      # Build docs locally
      cd docs
      make html

5. **Create Pull Request**

   - Write clear description
   - Reference related issues
   - Request review from maintainers

Testing Strategy
----------------

Unit Tests
~~~~~~~~~~

**Python Tests**

Located in ``tests/`` directory:

.. code-block:: python

   # tests/test_kelly_criterion.py
   import pytest
   from risk_optima_engine.core import calculate_kelly_criterion

   def test_kelly_criterion_basic():
       """Test basic Kelly Criterion calculation."""
       result = calculate_kelly_criterion(0.6, 2.0)
       assert abs(result - 0.2) < 1e-6

   def test_kelly_criterion_edge_cases():
       """Test edge cases and error conditions."""
       with pytest.raises(ValueError):
           calculate_kelly_criterion(-0.1, 2.0)  # Invalid probability

**Rust Tests**

Located in ``src/lib.rs`` and separate test modules:

.. code-block:: rust

   #[cfg(test)]
   mod tests {
       use super::*;

       #[test]
       fn test_kelly_criterion_basic() {
           let result = calculate_kelly_criterion(0.6, 2.0);
           assert!((result - 0.2).abs() < 1e-6);
       }

       #[test]
       #[should_panic(expected = "Invalid win probability")]
       fn test_kelly_criterion_invalid_probability() {
           calculate_kelly_criterion(-0.1, 2.0);
       }
   }

Integration Tests
~~~~~~~~~~~~~~~~~

**API Integration Tests**

.. code-block:: python

   # tests/test_api_integration.py
   import pytest
   from fastapi.testclient import TestClient
   from risk_optima_engine.backend import app

   @pytest.fixture
   def client():
       return TestClient(app)

   def test_upload_trade_history(client):
       """Test file upload endpoint."""
       test_file = "tests/data/sample_trades.csv"
       with open(test_file, "rb") as f:
           response = client.post(
               "/api/v1/upload/trade-history",
               files={"file": ("sample_trades.csv", f, "text/csv")}
           )

       assert response.status_code == 200
       data = response.json()
       assert "file_id" in data
       assert data["status"] == "completed"

Performance Tests
~~~~~~~~~~~~~~~~~

**Benchmarking**

.. code-block:: rust

   // benches/performance.rs
   use criterion::{black_box, criterion_group, criterion_main, Criterion};

   fn benchmark_monte_carlo_simulation(c: &mut Criterion) {
       let trades = generate_sample_trades(1000);
       let params = ChallengeParams::default();

       c.bench_function("monte_carlo_1000_trades", |b| {
           b.iter(|| {
               run_monte_carlo_simulation(
                   black_box(&trades),
                   black_box(&params),
                   black_box(100)
               )
           })
       });
   }

   criterion_group!(benches, benchmark_monte_carlo_simulation);
   criterion_main!(benches);

**Load Testing**

.. code-block:: bash

   # Use locust or similar tool for API load testing
   locust -f tests/load_tests.py --host=http://localhost:8000

Contributing Guidelines
-----------------------

Pull Request Process
~~~~~~~~~~~~~~~~~~~~

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Update** documentation
6. **Submit** pull request

**PR Requirements:**

- **Tests**: All new code must have tests
- **Documentation**: Update relevant docs
- **Style**: Pass all linting checks
- **Reviews**: Require at least one approval

Code Review Checklist
~~~~~~~~~~~~~~~~~~~~~

**For Reviewers:**

- [ ] Code follows style guidelines
- [ ] Tests are comprehensive and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact assessed
- [ ] Error handling appropriate

**For Contributors:**

- [ ] Self-review completed
- [ ] All tests pass locally
- [ ] Documentation builds successfully
- [ ] Breaking changes documented
- [ ] Migration guide provided if needed

Extending the Engine
--------------------

Adding New Risk Models
~~~~~~~~~~~~~~~~~~~~~~~

1. **Define the Algorithm**

   .. code-block:: rust

      // src/risk_models.rs
      pub struct CustomRiskModel {
          pub parameters: CustomParameters,
      }

      impl CustomRiskModel {
          pub fn calculate_optimal_fraction(&self, trades: &[Trade]) -> f64 {
              // Implementation here
          }
      }

2. **Add Python Bindings**

   .. code-block:: rust

      // src/lib.rs
      use pyo3::prelude::*;

      #[pyfunction]
      pub fn custom_risk_model(trades: Vec<PyTrade>) -> PyResult<f64> {
          let model = CustomRiskModel::default();
          Ok(model.calculate_optimal_fraction(&trades))
      }

3. **Update Python Interface**

   .. code-block:: python

      # src/risk_optima_engine/core.py
      from ._core import custom_risk_model

      def calculate_custom_risk(trades: List[Trade]) -> float:
          """Calculate custom risk model."""
          return custom_risk_model(trades)

Adding New Analysis Metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Implement in Rust**

   .. code-block:: rust

      // src/metrics.rs
      pub fn calculate_new_metric(trades: &[Trade]) -> f64 {
          // Implementation
      }

2. **Add to Performance Metrics**

   .. code-block:: rust

      // src/performance.rs
      pub struct PerformanceMetrics {
          pub new_metric: f64,
          // ... existing fields
      }

3. **Update API Response**

   .. code-block:: python

      # src/risk_optima_engine/backend.py
      @app.post("/api/v1/analysis/performance")
      async def analyze_performance(request: AnalysisRequest):
          # ... existing code
          result["kpis"]["new_metric"] = calculate_new_metric(trades)
          return result

Adding New File Formats
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Create Parser**

   .. code-block:: rust

      // src/parsers.rs
      pub mod json_parser {
          pub fn parse_json_trades(content: &str) -> Result<Vec<Trade>, ParseError> {
              // JSON parsing logic
          }
      }

2. **Update File Detection**

   .. code-block:: rust

      // src/lib.rs
      pub fn detect_format(filename: &str, content: &str) -> FileFormat {
          if filename.ends_with(".json") {
              FileFormat::Json
          } else {
              // existing detection logic
          }
      }

3. **Add to API**

   .. code-block:: python

      # src/risk_optima_engine/backend.py
      @app.post("/upload/trade-history")
      async def upload_trade_history(file: UploadFile):
          # Add JSON format support
          if file.filename.endswith('.json'):
              # Handle JSON parsing

Debugging and Troubleshooting
-----------------------------

Common Issues
~~~~~~~~~~~~~

**Rust Compilation Errors**

.. code-block:: bash

   # Clean and rebuild
   cargo clean
   cargo build

   # Check for specific error details
   cargo build --verbose

**Python Import Errors**

.. code-block:: bash

   # Rebuild Rust extension
   maturin develop --release

   # Check Python path
   python -c "import risk_optima_engine; print(risk_optima_engine.__file__)"

**MT5 Connection Issues**

.. code-block:: python

   # Test MT5 connection
   import MetaTrader5 as mt5

   if not mt5.initialize():
       print(f"MT5 initialization failed: {mt5.last_error()}")

   if not mt5.login(login, password, server):
       print(f"MT5 login failed: {mt5.last_error()}")

Performance Profiling
~~~~~~~~~~~~~~~~~~~~~

**Python Profiling**

.. code-block:: python

   import cProfile
   import pstats

   profiler = cProfile.Profile()
   profiler.enable()

   # Run your code here
   result = run_analysis()

   profiler.disable()
   stats = pstats.Stats(profiler).sort_stats('cumulative')
   stats.print_stats()

**Rust Profiling**

.. code-block:: bash

   # Use cargo flamegraph for performance analysis
   cargo install flamegraph
   cargo flamegraph --bin your_binary

   # Profile specific functions
   #[cfg(feature = "profile")]
   use std::time::Instant;

   let start = Instant::now();
   // Code to profile
   let duration = start.elapsed();
   println!("Function took {:?}", duration);

Release Process
---------------

Version Management
~~~~~~~~~~~~~~~~~~

The project uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

**Version Files to Update:**

- ``pyproject.toml``: Python package version
- ``Cargo.toml``: Rust crate version
- ``src/risk_optima_engine/__init__.py``: Python version
- ``CHANGELOG.rst``: Release notes

Release Checklist
~~~~~~~~~~~~~~~~~

- [ ] Update version numbers in all files
- [ ] Update CHANGELOG.rst with release notes
- [ ] Run full test suite
- [ ] Build documentation
- [ ] Create git tag
- [ ] Build and test release artifacts
- [ ] Publish to PyPI
- [ ] Update GitHub release
- [ ] Announce release

Building Releases
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Build Python package
   uv build

   # Build Rust crate (if publishing separately)
   cargo build --release

   # Test installation
   pip install dist/risk_optima_engine-1.1.0.tar.gz --force-reinstall

   # Upload to PyPI
   uv publish

Support and Community
---------------------

**Getting Help**

- **Issues**: GitHub Issues for bugs and feature requests
- **Discussions**: GitHub Discussions for questions
- **Documentation**: Read the Docs for detailed guides
- **Discord**: Community chat (if available)

**Contribution Areas**

- **Core Algorithms**: Improve risk models and calculations
- **User Interface**: Enhance frontend experience
- **API Design**: Extend REST API capabilities
- **Documentation**: Improve guides and examples
- **Testing**: Add more comprehensive test coverage
- **Performance**: Optimize computational efficiency

**Code of Conduct**

All contributors must follow our code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn
- Maintain professional standards
- Respect differing viewpoints

Thank you for contributing to RiskOptima Engine! 🚀