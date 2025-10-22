Contributing
============

We welcome contributions to RiskOptima Engine! This document provides guidelines and information for contributors.

Getting Started
---------------

Development Environment
~~~~~~~~~~~~~~~~~~~~~~~

1. **Fork and Clone**

   .. code-block:: bash

      # Fork the repository on GitHub
      # Then clone your fork
      git clone https://github.com/your-username/risk-optima-engine.git
      cd risk-optima-engine

2. **Set Up Development Environment**

   .. code-block:: bash

      # Install uv package manager
      pip install uv

      # Set up environment with all dependencies
      uv sync

      # Install development dependencies
      uv sync --dev

      # Build Rust extension
      maturin develop

3. **Install Pre-commit Hooks**

   .. code-block:: bash

      # Install pre-commit
      pip install pre-commit

      # Install hooks
      pre-commit install

4. **Verify Setup**

   .. code-block:: bash

      # Run tests
      pytest

      # Run Rust tests
      cargo test

      # Check code formatting
      black --check src/
      cargo fmt --check

Development Workflow
--------------------

Branching Strategy
~~~~~~~~~~~~~~~~~~

We use a simplified Git branching model:

- ``main``: Production-ready code
- ``develop``: Integration branch for features
- ``feature/*``: Feature branches
- ``bugfix/*``: Bug fix branches
- ``hotfix/*``: Critical fixes for production

**Creating a Feature Branch:**

.. code-block:: bash

   # Create and switch to feature branch
   git checkout -b feature/new-risk-model

   # Push to remote
   git push -u origin feature/new-risk-model

Making Changes
~~~~~~~~~~~~~~

1. **Write Tests First** (TDD approach)

   .. code-block:: python

      # tests/test_new_feature.py
      def test_new_risk_model():
          # Arrange
          trades = load_sample_trades()

          # Act
          result = calculate_new_risk_model(trades)

          # Assert
          assert result > 0
          assert result < 0.1  # Reasonable bounds

2. **Implement the Feature**

   Follow the existing code patterns and architecture.

3. **Update Documentation**

   - Add docstrings to new functions
   - Update relevant documentation files
   - Add examples if applicable

4. **Run Quality Checks**

   .. code-block:: bash

      # Run all tests
      pytest

      # Check code coverage
      pytest --cov=risk_optima_engine --cov-report=html

      # Lint Python code
      flake8 src/

      # Format code
      black src/

      # Type checking
      mypy src/risk_optima_engine/

      # Rust checks
      cargo test
      cargo clippy
      cargo fmt --check

Submitting Changes
~~~~~~~~~~~~~~~~~~

1. **Commit Your Changes**

   .. code-block:: bash

      # Stage your changes
      git add .

      # Commit with descriptive message
      git commit -m "feat: add new risk model algorithm

      - Implements advanced volatility-adjusted Kelly criterion
      - Adds comprehensive test coverage
      - Updates documentation with examples

      Closes #123"

2. **Push to Your Fork**

   .. code-block:: bash

      git push origin feature/new-risk-model

3. **Create Pull Request**

   - Go to GitHub and create a PR from your branch
   - Fill out the PR template
   - Request review from maintainers
   - Address any CI failures

Pull Request Guidelines
-----------------------

PR Requirements
~~~~~~~~~~~~~~~

**Must Have:**
- [ ] Tests pass on all supported platforms
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes without deprecation
- [ ] Commit messages follow conventional format

**Should Have:**
- [ ] Comprehensive test coverage
- [ ] Performance benchmarks if applicable
- [ ] Examples or usage documentation
- [ ] Migration guide for breaking changes

PR Template
~~~~~~~~~~~

.. code-block:: markdown

   ## Description
   Brief description of the changes.

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   - [ ] Performance improvement

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Integration tests pass
   - [ ] Manual testing performed

   ## Documentation
   - [ ] Docstrings added/updated
   - [ ] User documentation updated
   - [ ] API documentation updated

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Linting passes
   - [ ] Type checking passes
   - [ ] No security vulnerabilities
   - [ ] Performance impact assessed

Code Style Guidelines
---------------------

Python Style
~~~~~~~~~~~~

**PEP 8 Compliance**

We follow PEP 8 with some modifications enforced by Black:

.. code-block:: python

   # Good: Black-formatted code
   def calculate_kelly_criterion(
       win_probability: float,
       win_loss_ratio: float,
       fractional_multiplier: float = 1.0,
   ) -> float:
       """Calculate Kelly Criterion optimal fraction.

       Args:
           win_probability: Probability of winning (0.0 to 1.0)
           win_loss_ratio: Average win divided by average loss
           fractional_multiplier: Kelly fraction multiplier

       Returns:
           Optimal fraction of capital to risk
       """
       full_kelly = win_probability - (1 - win_probability) / win_loss_ratio
       return full_kelly * fractional_multiplier

   # Bad: Non-compliant formatting
   def calculate_kelly_criterion(win_probability,win_loss_ratio,fractional_multiplier=1.0):
       full_kelly=win_probability-(1-win_probability)/win_loss_ratio
       return full_kelly*fractional_multiplier

**Type Hints**

All function parameters and return values must have type hints:

.. code-block:: python

   from typing import List, Dict, Optional, Union
   import pandas as pd

   def analyze_performance(
       trades_df: pd.DataFrame,
       robust_statistics: bool = True,
       include_equity_curve: bool = True,
   ) -> Dict[str, Union[float, List[Dict[str, float]]]]:
       """Analyze trading performance."""
       # Implementation here
       pass

**Docstrings**

Use Google-style docstrings:

.. code-block:: python

   def optimize_challenge(
       trades_df: pd.DataFrame,
       challenge_params: Dict[str, float],
       num_simulations: int = 1000,
   ) -> Dict[str, float]:
       """Optimize prop firm challenge success using Monte Carlo simulation.

       This function runs multiple simulations of the challenge period
       using bootstrap resampling to find the optimal risk fraction.

       Args:
           trades_df: DataFrame with historical trade data
           challenge_params: Dictionary with challenge requirements
           num_simulations: Number of Monte Carlo simulations to run

       Returns:
           Dictionary with optimization results including:
           - recommended_fraction: Optimal risk fraction
           - pass_rate: Estimated success probability
           - confidence_interval: Statistical confidence bounds

       Raises:
           ValueError: If input parameters are invalid
           RuntimeError: If simulation fails

       Example:
           >>> trades = pd.read_csv('my_trades.csv')
           >>> params = {'account_size': 100000, 'profit_target': 0.1}
           >>> result = optimize_challenge(trades, params)
           >>> print(f"Optimal risk: {result['recommended_fraction']:.3f}")
       """
       # Implementation here
       pass

Rust Style
~~~~~~~~~~

**Official Rust Style**

Follow the official Rust style guidelines and use ``cargo fmt``:

.. code-block:: rust

   // Good: Properly formatted Rust code
   pub fn calculate_kelly_criterion(
       win_probability: f64,
       win_loss_ratio: f64,
       fractional_multiplier: f64,
   ) -> Result<f64, RiskOptimaError> {
       if !(0.0..=1.0).contains(&win_probability) {
           return Err(RiskOptimaError::Validation {
               field: "win_probability".to_string(),
               message: "Must be between 0.0 and 1.0".to_string(),
           });
       }

       let full_kelly = win_probability - (1.0 - win_probability) / win_loss_ratio;
       let fractional_kelly = full_kelly * fractional_multiplier;

       Ok(fractional_kelly)
   }

   // Bad: Poorly formatted and unsafe code
   pub fn calc_kelly(wp:f64,wl:f64,fm:f64)->f64{
       wp-(1.0-wp)/wl*fm
   }

**Error Handling**

Use ``Result`` and ``Option`` types appropriately:

.. code-block:: rust

   use thiserror::Error;

   #[derive(Error, Debug)]
   pub enum RiskOptimaError {
       #[error("Validation error: {field} - {message}")]
       Validation { field: String, message: String },

       #[error("Processing error: {message}")]
       Processing { message: String },
   }

   pub fn validate_trade_data(trades: &[Trade]) -> Result<(), RiskOptimaError> {
       for (i, trade) in trades.iter().enumerate() {
           if trade.volume <= 0.0 {
               return Err(RiskOptimaError::Validation {
                   field: format!("trades[{}].volume", i),
                   message: "Volume must be positive".to_string(),
               });
           }
       }
       Ok(())
   }

**Documentation**

Document all public APIs with ``///`` comments:

.. code-block:: rust

   /// Calculate the optimal fraction of capital to risk using the Kelly Criterion.
   ///
   /// The Kelly Criterion determines the optimal position size that maximizes
   /// the expected logarithmic growth of capital.
   ///
   /// # Arguments
   ///
   /// * `win_probability` - Probability of winning a trade (0.0 to 1.0)
   /// * `win_loss_ratio` - Ratio of average win to average loss
   /// * `fractional_multiplier` - Multiplier for fractional Kelly (0.25 for quarter Kelly)
   ///
   /// # Returns
   ///
   /// Returns the optimal fraction of capital to risk, or an error if validation fails.
   ///
   /// # Examples
   ///
   /// ```
   /// let kelly = calculate_kelly_criterion(0.6, 2.0, 1.0)?;
   /// assert!((kelly - 0.2).abs() < 1e-6);
   /// ```
   pub fn calculate_kelly_criterion(
       win_probability: f64,
       win_loss_ratio: f64,
       fractional_multiplier: f64,
   ) -> Result<f64, RiskOptimaError> {
       // Implementation here
   }

Testing Guidelines
------------------

Unit Tests
~~~~~~~~~~

**Python Tests**

.. code-block:: python

   # tests/test_kelly_criterion.py
   import pytest
   import pandas as pd
   from risk_optima_engine.core import calculate_kelly_criterion

   class TestKellyCriterion:
       def test_basic_calculation(self):
           """Test basic Kelly Criterion calculation."""
           result = calculate_kelly_criterion(0.6, 2.0)
           assert abs(result - 0.2) < 1e-6

       def test_fractional_kelly(self):
           """Test fractional Kelly with multiplier."""
           result = calculate_kelly_criterion(0.6, 2.0, fractional_multiplier=0.5)
           assert abs(result - 0.1) < 1e-6

       @pytest.mark.parametrize("win_prob,win_loss,expected", [
           (0.5, 1.0, 0.0),  # Fair coin
           (0.6, 2.0, 0.2),  # Advantageous bet
           (0.7, 1.5, 0.2667),  # Another case
       ])
       def test_parametrized_cases(self, win_prob, win_loss, expected):
           """Test multiple Kelly cases."""
           result = calculate_kelly_criterion(win_prob, win_loss)
           assert abs(result - expected) < 1e-4

       def test_invalid_inputs(self):
           """Test error handling for invalid inputs."""
           with pytest.raises(ValueError, match="win_probability must be between 0 and 1"):
               calculate_kelly_criterion(-0.1, 2.0)

           with pytest.raises(ValueError, match="win_loss_ratio must be positive"):
               calculate_kelly_criterion(0.6, -1.0)

**Rust Tests**

.. code-block:: rust

   #[cfg(test)]
   mod tests {
       use super::*;
       use approx::assert_relative_eq;

       #[test]
       fn test_kelly_criterion_basic() {
           let result = calculate_kelly_criterion(0.6, 2.0, 1.0).unwrap();
           assert_relative_eq!(result, 0.2, epsilon = 1e-6);
       }

       #[test]
       fn test_kelly_criterion_fractional() {
           let result = calculate_kelly_criterion(0.6, 2.0, 0.5).unwrap();
           assert_relative_eq!(result, 0.1, epsilon = 1e-6);
       }

       #[test]
       fn test_kelly_criterion_invalid_probability() {
           let result = calculate_kelly_criterion(-0.1, 2.0, 1.0);
           assert!(result.is_err());
           assert!(matches!(result.unwrap_err(), RiskOptimaError::Validation { .. }));
       }

       #[test]
       fn test_kelly_criterion_edge_cases() {
           // Test with very small win probability
           let result = calculate_kelly_criterion(0.001, 100.0, 1.0).unwrap();
           assert!(result < 0.01);  // Should be very conservative

           // Test with very high win probability
           let result = calculate_kelly_criterion(0.999, 1.001, 1.0).unwrap();
           assert!(result > 0.9);  # Should be very aggressive
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

   @pytest.fixture
   def sample_csv_content():
       return """Symbol,Type,Volume,Open Price,Close Price,Profit
   EURUSD,buy,0.10,1.0850,1.0920,70.00
   GBPUSD,sell,0.05,1.2750,1.2680,-35.00"""

   def test_upload_and_analyze_workflow(client, sample_csv_content):
       """Test complete workflow from upload to analysis."""

       # Upload file
       response = client.post(
           "/api/v1/upload/trade-history",
           files={"file": ("trades.csv", sample_csv_content, "text/csv")}
       )
       assert response.status_code == 200
       file_id = response.json()["file_id"]

       # Analyze performance
       response = client.post(
           "/api/v1/analysis/performance",
           json={"file_id": file_id}
       )
       assert response.status_code == 200
       result = response.json()

       # Verify results
       assert "kpis" in result
       assert result["kpis"]["total_trades"] == 2
       assert result["kpis"]["win_probability"] == 0.5

Performance Tests
~~~~~~~~~~~~~~~~~

**Benchmarking**

.. code-block:: python

   # tests/test_performance.py
   import pytest
   import time
   import pandas as pd
   from risk_optima_engine.core import run_monte_carlo_simulation

   @pytest.mark.performance
   def test_monte_carlo_performance(benchmark):
       """Benchmark Monte Carlo simulation performance."""
       # Generate large dataset
       trades = generate_sample_trades(1000)

       # Benchmark the function
       result = benchmark(run_monte_carlo_simulation, trades, 1000)

       # Assert performance requirements
       assert result < 60.0  # Should complete in under 60 seconds

   def test_memory_usage():
       """Test memory usage doesn't grow excessively."""
       import psutil
       import os

       process = psutil.Process(os.getpid())
       initial_memory = process.memory_info().rss

       # Run memory-intensive operation
       large_simulation()

       final_memory = process.memory_info().rss
       memory_increase = final_memory - initial_memory

       # Assert memory increase is reasonable (less than 500MB)
       assert memory_increase < 500 * 1024 * 1024

Code Review Process
-------------------

Review Checklist
~~~~~~~~~~~~~~~~

**For Reviewers:**

- [ ] **Functionality**: Does the code work as intended?
- [ ] **Tests**: Are there comprehensive tests covering edge cases?
- [ ] **Style**: Does the code follow our style guidelines?
- [ ] **Documentation**: Are docstrings and comments clear and complete?
- [ ] **Performance**: Is the code efficient and scalable?
- [ ] **Security**: Are there any security vulnerabilities?
- [ ] **Error Handling**: Are errors handled appropriately?
- [ ] **Breaking Changes**: Are there any breaking changes? If so, is there a migration guide?

**For Contributors:**

- [ ] **Self-Review**: Have you reviewed your own code?
- [ ] **Tests Pass**: Do all tests pass locally?
- [ ] **Linting**: Does the code pass all linting checks?
- [ ] **Documentation**: Have you updated relevant documentation?
- [ ] **Edge Cases**: Have you considered edge cases and error conditions?
- [ ] **Performance**: Have you considered performance implications?

Review Comments
~~~~~~~~~~~~~~~

**Good Review Comments:**

.. code-block:: text

   # ✅ Specific and actionable
   "The error message could be more descriptive. Consider including the invalid value in the message."

   # ✅ Suggests improvement with reasoning
   "This function is doing too many things. Consider splitting it into smaller, focused functions for better maintainability."

   # ✅ Provides context and alternatives
   "Using a list comprehension here would be more Pythonic and potentially faster than the current loop."

**Poor Review Comments:**

.. code-block:: text

   # ❌ Vague and unhelpful
   "This looks wrong."

   # ❌ Demanding without explanation
   "Change this to use a different approach."

   # ❌ Personal preference without justification
   "I don't like this variable name."

Areas for Contribution
----------------------

Core Development
~~~~~~~~~~~~~~~~

- **Algorithm Implementation**: New risk models, optimization algorithms
- **Performance Optimization**: Faster computations, memory efficiency
- **Platform Support**: Linux/macOS compatibility, ARM support
- **API Extensions**: New endpoints, WebSocket support, GraphQL

User Experience
~~~~~~~~~~~~~~~

- **UI/UX Improvements**: Better interface design, accessibility
- **Visualization**: New chart types, interactive dashboards
- **Mobile Support**: Responsive design, PWA capabilities
- **Internationalization**: Multi-language support

Data & Integration
~~~~~~~~~~~~~~~~~~

- **New Data Sources**: Additional broker integrations, data formats
- **Export Formats**: More report formats, API integrations
- **Data Quality**: Better validation, cleaning, and preprocessing
- **Real-time Features**: Live data streaming, alerts

Documentation & Testing
~~~~~~~~~~~~~~~~~~~~~~~

- **Documentation**: Tutorials, examples, API docs
- **Testing**: More comprehensive test coverage, performance tests
- **CI/CD**: Better automation, deployment pipelines
- **Tooling**: Development tools, debugging aids

Community & Ecosystem
~~~~~~~~~~~~~~~~~~~~~

- **Plugins**: Plugin architecture for custom algorithms
- **Marketplace**: Third-party algorithm marketplace
- **Community Tools**: Utilities, libraries, integrations
- **Education**: Tutorials, courses, educational content

Getting Help
------------

**Questions and Discussion**

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bugs and feature requests
- **Discord**: For real-time community chat (if available)

**Finding Tasks**

- **Good First Issues**: Look for issues labeled "good first issue"
- **Help Wanted**: Issues that need community contribution
- **Bugs**: Fix reported bugs and improve stability
- **Documentation**: Help improve documentation and examples

**Communication Guidelines**

- Be respectful and inclusive
- Provide context and examples
- Use clear, concise language
- Be open to feedback and different viewpoints
- Help newcomers learn and contribute

Thank you for contributing to RiskOptima Engine! Your contributions help make quantitative trading risk management more accessible and effective for everyone. 🚀