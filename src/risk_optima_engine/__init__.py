from risk_optima_engine._core import (
    Trade,
    PerformanceMetrics,
    ChallengeParams,
    parse_mt5_csv,
    parse_mt5_xml,
    calculate_performance_metrics,
    calculate_kelly_criterion,
    calculate_optimal_f,
    run_monte_carlo_simulation,
)

# Import MT5 modules
from . import mt5_integration
from . import mt5_live_data

__version__ = "1.1.0"
__all__ = [
    "Trade",
    "PerformanceMetrics",
    "ChallengeParams",
    "parse_mt5_csv",
    "parse_mt5_xml",
    "calculate_performance_metrics",
    "calculate_kelly_criterion",
    "calculate_optimal_f",
    "run_monte_carlo_simulation",
    "mt5_integration",
    "mt5_live_data",
]
