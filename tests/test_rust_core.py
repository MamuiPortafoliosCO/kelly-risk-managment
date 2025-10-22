"""
Tests for the Rust core computational functions
"""

import pytest
from risk_optima_engine import (
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


class TestDataStructures:
    """Test data structure creation and manipulation"""

    def test_trade_creation(self):
        """Test creating a Trade object"""
        trade = Trade(
            symbol="EURUSD",
            trade_type="Buy",
            volume=1.0,
            open_price=1.1000,
            close_price=1.1050,
            profit=50.0,
            commission=-2.0,
            swap=0.0,
        )

        assert trade.symbol == "EURUSD"
        assert trade.trade_type == "Buy"
        assert trade.volume == 1.0
        assert trade.open_price == 1.1000
        assert trade.close_price == 1.1050
        assert trade.profit == 50.0
        assert trade.commission == -2.0
        assert trade.swap == 0.0

    def test_performance_metrics_creation(self):
        """Test creating a PerformanceMetrics object"""
        metrics = PerformanceMetrics(
            total_trades=100,
            win_probability=0.55,
            loss_probability=0.45,
            avg_win=100.0,
            avg_loss=-80.0,
            win_loss_ratio=1.25,
            profit_factor=1.2,
            expectancy=5.0,
            max_drawdown=500.0,
            sharpe_ratio=0.8,
        )

        assert metrics.total_trades == 100
        assert metrics.win_probability == 0.55
        assert metrics.profit_factor == 1.2
        assert metrics.expectancy == 5.0

    def test_challenge_params_creation(self):
        """Test creating a ChallengeParams object"""
        params = ChallengeParams(
            account_size=100000.0,
            profit_target_percent=10.0,
            max_daily_loss_percent=5.0,
            max_overall_loss_percent=10.0,
            min_trading_days=30,
        )

        assert params.account_size == 100000.0
        assert params.profit_target_percent == 10.0
        assert params.max_daily_loss_percent == 5.0
        assert params.max_overall_loss_percent == 10.0
        assert params.min_trading_days == 30


class TestDataParsing:
    """Test MT5 data parsing functions"""

    def test_parse_mt5_csv_basic(self):
        """Test basic CSV parsing"""
        csv_content = """Symbol,Type,Volume,Open Price,Close Price,Profit,Commission,Swap
EURUSD,Buy,1.0,1.1000,1.1050,50.0,-2.0,0.0
GBPUSD,Sell,0.5,1.3000,1.2950,-25.0,-1.0,-0.5"""

        trades = parse_mt5_csv(csv_content)

        assert len(trades) == 2
        assert trades[0].symbol == "EURUSD"
        assert trades[0].trade_type == "Buy"
        assert trades[0].profit == 50.0
        assert trades[1].symbol == "GBPUSD"
        assert trades[1].trade_type == "Sell"
        assert trades[1].profit == -25.0

    def test_parse_mt5_csv_empty(self):
        """Test parsing empty CSV"""
        csv_content = "Symbol,Type,Volume,Open Price,Close Price,Profit,Commission,Swap"
        trades = parse_mt5_csv(csv_content)
        assert len(trades) == 0

    def test_parse_mt5_csv_invalid_data(self):
        """Test parsing CSV with invalid data"""
        csv_content = """Symbol,Type,Volume,Open Price,Close Price,Profit,Commission,Swap
EURUSD,Buy,invalid,1.1000,1.1050,50.0,-2.0,0.0"""

        # Should handle invalid data gracefully
        trades = parse_mt5_csv(csv_content)
        assert len(trades) == 1
        assert trades[0].volume == 0.0  # Default for invalid parse


class TestPerformanceAnalysis:
    """Test performance analysis functions"""

    def test_calculate_performance_metrics_basic(self):
        """Test basic performance metrics calculation"""
        trades = [
            Trade("EURUSD", "Buy", 1.0, 1.1000, 1.1050, 50.0, -2.0, 0.0),
            Trade("GBPUSD", "Sell", 0.5, 1.3000, 1.2950, -25.0, -1.0, -0.5),
            Trade("USDJPY", "Buy", 1.0, 150.00, 150.50, 50.0, -2.0, 0.0),
        ]

        metrics = calculate_performance_metrics(trades)

        assert metrics.total_trades == 3
        assert metrics.win_probability == 2.0 / 3.0  # 2 winning trades
        assert metrics.loss_probability == 1.0 / 3.0  # 1 losing trade
        assert metrics.avg_win > 0
        assert metrics.avg_loss < 0
        assert metrics.profit_factor > 1.0  # Profitable system

    def test_calculate_performance_metrics_empty(self):
        """Test performance metrics with no trades"""
        with pytest.raises(Exception):  # Should raise an error for empty trades
            calculate_performance_metrics([])

    def test_calculate_performance_metrics_all_wins(self):
        """Test performance metrics with all winning trades"""
        trades = [
            Trade("EURUSD", "Buy", 1.0, 1.1000, 1.1050, 50.0, -2.0, 0.0),
            Trade("GBPUSD", "Buy", 1.0, 1.3000, 1.3050, 50.0, -2.0, 0.0),
        ]

        metrics = calculate_performance_metrics(trades)

        assert metrics.total_trades == 2
        assert metrics.win_probability == 1.0
        assert metrics.loss_probability == 0.0
        assert metrics.avg_loss == 0.0  # No losses

    def test_calculate_performance_metrics_all_losses(self):
        """Test performance metrics with all losing trades"""
        trades = [
            Trade("EURUSD", "Sell", 1.0, 1.1000, 1.0950, -50.0, -2.0, 0.0),
            Trade("GBPUSD", "Sell", 1.0, 1.3000, 1.2950, -50.0, -2.0, 0.0),
        ]

        metrics = calculate_performance_metrics(trades)

        assert metrics.total_trades == 2
        assert metrics.win_probability == 0.0
        assert metrics.loss_probability == 1.0
        assert metrics.avg_win == 0.0  # No wins


class TestKellyCriterion:
    """Test Kelly Criterion calculations"""

    def test_kelly_criterion_basic(self):
        """Test basic Kelly Criterion calculation"""
        win_prob = 0.55
        win_loss_ratio = 1.25
        fractional_multiplier = 1.0

        kelly_fraction = calculate_kelly_criterion(win_prob, win_loss_ratio, fractional_multiplier)

        expected = win_prob - ((1.0 - win_prob) / win_loss_ratio)
        assert abs(kelly_fraction - expected) < 1e-6

    def test_kelly_criterion_fractional(self):
        """Test fractional Kelly Criterion"""
        win_prob = 0.55
        win_loss_ratio = 1.25
        fractional_multiplier = 0.5  # Half Kelly

        kelly_fraction = calculate_kelly_criterion(win_prob, win_loss_ratio, fractional_multiplier)

        full_kelly = win_prob - ((1.0 - win_prob) / win_loss_ratio)
        expected = full_kelly * fractional_multiplier
        assert abs(kelly_fraction - expected) < 1e-6

    def test_kelly_criterion_edge_cases(self):
        """Test Kelly Criterion edge cases"""
        # Win probability = 1.0 (always win)
        with pytest.raises(Exception):
            calculate_kelly_criterion(1.0, 1.25, 1.0)

        # Win probability = 0.0 (never win)
        with pytest.raises(Exception):
            calculate_kelly_criterion(0.0, 1.25, 1.0)

        # Win/loss ratio = 0 (undefined)
        with pytest.raises(Exception):
            calculate_kelly_criterion(0.55, 0.0, 1.0)


class TestOptimalF:
    """Test Optimal F calculations"""

    def test_optimal_f_basic(self):
        """Test basic Optimal F calculation"""
        trades = [
            Trade("EURUSD", "Buy", 1.0, 1.1000, 1.1050, 50.0, -2.0, 0.0),
            Trade("GBPUSD", "Sell", 1.0, 1.3000, 1.2950, -50.0, -2.0, 0.0),
            Trade("USDJPY", "Buy", 1.0, 150.00, 150.50, 50.0, -2.0, 0.0),
        ]

        optimal_f = calculate_optimal_f(trades, 1000, 1e-6)

        assert isinstance(optimal_f, float)
        assert optimal_f >= 0.0  # Should be non-negative

    def test_optimal_f_no_losses(self):
        """Test Optimal F with no losses"""
        trades = [
            Trade("EURUSD", "Buy", 1.0, 1.1000, 1.1050, 50.0, -2.0, 0.0),
            Trade("GBPUSD", "Buy", 1.0, 1.3000, 1.3050, 50.0, -2.0, 0.0),
        ]

        optimal_f = calculate_optimal_f(trades, 1000, 1e-6)

        assert optimal_f == 0.0  # No losses means no risk management needed

    def test_optimal_f_empty_trades(self):
        """Test Optimal F with empty trades"""
        with pytest.raises(Exception):
            calculate_optimal_f([], 1000, 1e-6)


class TestMonteCarloSimulation:
    """Test Monte Carlo simulation functions"""

    def test_monte_carlo_basic(self):
        """Test basic Monte Carlo simulation"""
        trades = [
            Trade("EURUSD", "Buy", 1.0, 1.1000, 1.1050, 50.0, -2.0, 0.0),
            Trade("GBPUSD", "Sell", 1.0, 1.3000, 1.2950, -50.0, -2.0, 0.0),
        ]

        challenge_params = ChallengeParams(
            account_size=100000.0,
            profit_target_percent=10.0,
            max_daily_loss_percent=5.0,
            max_overall_loss_percent=10.0,
            min_trading_days=30,
        )

        results = run_monte_carlo_simulation(trades, challenge_params, 0.01, 100)

        assert isinstance(results, dict)
        assert "pass_rate" in results
        assert "total_simulations" in results
        assert "passed_simulations" in results
        assert results["total_simulations"] == 100
        assert 0.0 <= results["pass_rate"] <= 1.0

    def test_monte_carlo_empty_trades(self):
        """Test Monte Carlo with empty trades"""
        challenge_params = ChallengeParams(
            account_size=100000.0,
            profit_target_percent=10.0,
            max_daily_loss_percent=5.0,
            max_overall_loss_percent=10.0,
            min_trading_days=30,
        )

        with pytest.raises(Exception):
            run_monte_carlo_simulation([], challenge_params, 0.01, 100)

    def test_monte_carlo_edge_cases(self):
        """Test Monte Carlo edge cases"""
        trades = [Trade("EURUSD", "Buy", 1.0, 1.1000, 1.1050, 50.0, -2.0, 0.0)]

        challenge_params = ChallengeParams(
            account_size=100000.0,
            profit_target_percent=10.0,
            max_daily_loss_percent=5.0,
            max_overall_loss_percent=10.0,
            min_trading_days=30,
        )

        # Test with very high risk fraction
        results = run_monte_carlo_simulation(trades, challenge_params, 0.1, 50)
        assert isinstance(results, dict)

        # Test with very low risk fraction
        results = run_monte_carlo_simulation(trades, challenge_params, 0.001, 50)
        assert isinstance(results, dict)


if __name__ == "__main__":
    pytest.main([__file__])