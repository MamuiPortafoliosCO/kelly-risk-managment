use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

// Data structures
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct Trade {
    #[pyo3(get, set)]
    pub symbol: String,
    #[pyo3(get, set)]
    pub trade_type: String, // "Buy" or "Sell"
    #[pyo3(get, set)]
    pub volume: f64,
    #[pyo3(get, set)]
    pub open_price: f64,
    #[pyo3(get, set)]
    pub close_price: f64,
    #[pyo3(get, set)]
    pub profit: f64,
    #[pyo3(get, set)]
    pub commission: Option<f64>,
    #[pyo3(get, set)]
    pub swap: Option<f64>,
}

#[pymethods]
impl Trade {
    #[new]
    fn new(
        symbol: String,
        trade_type: String,
        volume: f64,
        open_price: f64,
        close_price: f64,
        profit: f64,
        commission: Option<f64>,
        swap: Option<f64>,
    ) -> Self {
        Trade {
            symbol,
            trade_type,
            volume,
            open_price,
            close_price,
            profit,
            commission,
            swap,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct PerformanceMetrics {
    #[pyo3(get)]
    pub total_trades: usize,
    #[pyo3(get)]
    pub win_probability: f64,
    #[pyo3(get)]
    pub loss_probability: f64,
    #[pyo3(get)]
    pub avg_win: f64,
    #[pyo3(get)]
    pub avg_loss: f64,
    #[pyo3(get)]
    pub win_loss_ratio: f64,
    #[pyo3(get)]
    pub profit_factor: f64,
    #[pyo3(get)]
    pub expectancy: f64,
    #[pyo3(get)]
    pub max_drawdown: f64,
    #[pyo3(get)]
    pub sharpe_ratio: Option<f64>,
}

#[pymethods]
impl PerformanceMetrics {
    #[new]
    fn new(
        total_trades: usize,
        win_probability: f64,
        loss_probability: f64,
        avg_win: f64,
        avg_loss: f64,
        win_loss_ratio: f64,
        profit_factor: f64,
        expectancy: f64,
        max_drawdown: f64,
        sharpe_ratio: Option<f64>,
    ) -> Self {
        PerformanceMetrics {
            total_trades,
            win_probability,
            loss_probability,
            avg_win,
            avg_loss,
            win_loss_ratio,
            profit_factor,
            expectancy,
            max_drawdown,
            sharpe_ratio,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct ChallengeParams {
    #[pyo3(get, set)]
    pub account_size: f64,
    #[pyo3(get, set)]
    pub profit_target_percent: f64,
    #[pyo3(get, set)]
    pub max_daily_loss_percent: f64,
    #[pyo3(get, set)]
    pub max_overall_loss_percent: f64,
    #[pyo3(get, set)]
    pub min_trading_days: u32,
}

#[pymethods]
impl ChallengeParams {
    #[new]
    fn new(
        account_size: f64,
        profit_target_percent: f64,
        max_daily_loss_percent: f64,
        max_overall_loss_percent: f64,
        min_trading_days: u32,
    ) -> Self {
        ChallengeParams {
            account_size,
            profit_target_percent,
            max_daily_loss_percent,
            max_overall_loss_percent,
            min_trading_days,
        }
    }
}

// Core computational functions
#[pyfunction]
fn parse_mt5_csv(content: &str) -> PyResult<Vec<Trade>> {
    let mut trades = Vec::new();
    let mut reader = csv::Reader::from_reader(content.as_bytes());

    for result in reader.records() {
        let record = result.map_err(|e| PyValueError::new_err(format!("CSV parsing error: {}", e)))?;

        // Skip header and non-trade rows
        if record.len() < 8 || record.get(0).unwrap_or("").contains("Positions") {
            continue;
        }

        let trade = Trade {
            symbol: record.get(0).unwrap_or("").to_string(),
            trade_type: record.get(1).unwrap_or("").to_string(),
            volume: record.get(2).unwrap_or("0").parse().unwrap_or(0.0),
            open_price: record.get(3).unwrap_or("0").parse().unwrap_or(0.0),
            close_price: record.get(4).unwrap_or("0").parse().unwrap_or(0.0),
            profit: record.get(5).unwrap_or("0").parse().unwrap_or(0.0),
            commission: record.get(6).and_then(|s| s.parse().ok()),
            swap: record.get(7).and_then(|s| s.parse().ok()),
        };

        trades.push(trade);
    }

    Ok(trades)
}

#[pyfunction]
fn parse_mt5_xml(content: &str) -> PyResult<Vec<Trade>> {
    let mut trades = Vec::new();

    // Simple XML parsing for MT5 format
    // This is a simplified implementation - in production, use a proper XML parser
    let positions_start = content.find("<Positions>").unwrap_or(0);
    let positions_end = content.find("</Positions>").unwrap_or(content.len());

    if positions_start == 0 {
        return Err(PyValueError::new_err("Invalid MT5 XML format: Positions section not found"));
    }

    let positions_content = &content[positions_start..positions_end];

    // Parse individual position entries
    // This is a basic implementation - enhance for production use
    for line in positions_content.lines() {
        if line.contains("<Position>") && line.contains("</Position>") {
            // Extract trade data from XML line
            // Simplified parsing - use proper XML parsing in production
            let trade = Trade {
                symbol: "EURUSD".to_string(), // Placeholder
                trade_type: "Buy".to_string(), // Placeholder
                volume: 1.0,
                open_price: 1.0,
                close_price: 1.0,
                profit: 0.0,
                commission: None,
                swap: None,
            };
            trades.push(trade);
        }
    }

    Ok(trades)
}

#[pyfunction]
fn calculate_performance_metrics(trades: Vec<Trade>) -> PyResult<PerformanceMetrics> {
    if trades.is_empty() {
        return Err(PyValueError::new_err("No trades provided"));
    }

    let total_trades = trades.len();

    let winning_trades: Vec<_> = trades.iter().filter(|t| t.profit > 0.0).collect();
    let losing_trades: Vec<_> = trades.iter().filter(|t| t.profit < 0.0).collect();

    let win_probability = winning_trades.len() as f64 / total_trades as f64;
    let loss_probability = losing_trades.len() as f64 / total_trades as f64;

    let avg_win = if !winning_trades.is_empty() {
        winning_trades.iter().map(|t| t.profit).sum::<f64>() / winning_trades.len() as f64
    } else {
        0.0
    };

    let avg_loss = if !losing_trades.is_empty() {
        losing_trades.iter().map(|t| t.profit).sum::<f64>() / losing_trades.len() as f64
    } else {
        0.0
    };

    // Robust Win/Loss Ratio using median
    let mut win_amounts: Vec<f64> = winning_trades.iter().map(|t| t.profit).collect();
    let mut loss_amounts: Vec<f64> = losing_trades.iter().map(|t| t.profit.abs()).collect();

    win_amounts.sort_by(|a, b| a.partial_cmp(b).unwrap());
    loss_amounts.sort_by(|a, b| a.partial_cmp(b).unwrap());

    let median_win = if !win_amounts.is_empty() {
        let mid = win_amounts.len() / 2;
        if win_amounts.len() % 2 == 0 {
            (win_amounts[mid - 1] + win_amounts[mid]) / 2.0
        } else {
            win_amounts[mid]
        }
    } else {
        0.0
    };

    let median_loss = if !loss_amounts.is_empty() {
        let mid = loss_amounts.len() / 2;
        if loss_amounts.len() % 2 == 0 {
            (loss_amounts[mid - 1] + loss_amounts[mid]) / 2.0
        } else {
            loss_amounts[mid]
        }
    } else {
        0.0
    };

    let win_loss_ratio = if median_loss != 0.0 { median_win / median_loss } else { 0.0 };

    let gross_profit: f64 = winning_trades.iter().map(|t| t.profit).sum();
    let gross_loss: f64 = losing_trades.iter().map(|t| t.profit.abs()).sum();
    let profit_factor = if gross_loss != 0.0 { gross_profit / gross_loss } else { 0.0 };

    let expectancy = win_probability * avg_win - loss_probability * avg_loss.abs();

    // Calculate equity curve for drawdown
    let mut equity = 0.0;
    let mut peak = 0.0;
    let mut max_drawdown = 0.0;

    for trade in &trades {
        equity += trade.profit;
        if equity > peak {
            peak = equity;
        }
        let drawdown = peak - equity;
        if drawdown > max_drawdown {
            max_drawdown = drawdown;
        }
    }

    // Sharpe ratio calculation (simplified - requires daily returns)
    let sharpe_ratio = None; // Placeholder for future implementation

    Ok(PerformanceMetrics::new(
        total_trades,
        win_probability,
        loss_probability,
        avg_win,
        avg_loss,
        win_loss_ratio,
        profit_factor,
        expectancy,
        max_drawdown,
        sharpe_ratio,
    ))
}

#[pyfunction]
fn calculate_kelly_criterion(win_prob: f64, win_loss_ratio: f64, fractional_multiplier: f64) -> PyResult<f64> {
    if win_prob <= 0.0 || win_prob >= 1.0 {
        return Err(PyValueError::new_err("Win probability must be between 0 and 1"));
    }
    if win_loss_ratio <= 0.0 {
        return Err(PyValueError::new_err("Win/loss ratio must be positive"));
    }

    let kelly_fraction = win_prob - ((1.0 - win_prob) / win_loss_ratio);
    let optimal_fraction = kelly_fraction * fractional_multiplier;

    Ok(optimal_fraction)
}

#[pyfunction]
fn calculate_optimal_f(trades: Vec<Trade>, max_iterations: usize, tolerance: f64) -> PyResult<f64> {
    if trades.is_empty() {
        return Err(PyValueError::new_err("No trades provided"));
    }

    // Find the largest loss
    let largest_loss = trades.iter()
        .map(|t| t.profit)
        .filter(|&p| p < 0.0)
        .min_by(|a, b| a.partial_cmp(b).unwrap())
        .unwrap_or(-1.0)
        .abs();

    if largest_loss == 0.0 {
        return Ok(0.0); // No losses, no risk management needed
    }

    // Grid search for optimal f
    let mut best_f = 0.0;
    let mut best_twr = f64::NEG_INFINITY;

    for i in 0..1000 {
        let f = (i as f64) / 10000.0; // f from 0.000 to 0.100

        let twr: f64 = trades.iter()
            .map(|trade| 1.0 + f * (-trade.profit / largest_loss))
            .product();

        if twr > best_twr {
            best_twr = twr;
            best_f = f;
        }
    }

    // Refine with gradient ascent
    let mut f = best_f;
    let learning_rate = 0.001;

    for _ in 0..max_iterations {
        let mut gradient = 0.0;

        for trade in &trades {
            let term = 1.0 + f * (-trade.profit / largest_loss);
            if term > 0.0 {
                gradient += (-trade.profit / largest_loss) / term;
            }
        }

        let twr: f64 = trades.iter()
            .map(|trade| 1.0 + f * (-trade.profit / largest_loss))
            .product();

        gradient *= twr;

        let new_f = f + learning_rate * gradient;
        if new_f < 0.0 {
            break;
        }

        let new_twr: f64 = trades.iter()
            .map(|trade| 1.0 + new_f * (-trade.profit / largest_loss))
            .product();

        if (new_twr - twr).abs() < tolerance {
            f = new_f;
            break;
        }

        if new_twr > twr {
            f = new_f;
        } else {
            break;
        }
    }

    Ok(f)
}

#[pyfunction]
fn run_monte_carlo_simulation(
    trades: Vec<Trade>,
    challenge_params: ChallengeParams,
    risk_fraction: f64,
    num_simulations: usize,
) -> PyResult<HashMap<String, f64>> {
    use rand::prelude::*;
    use rayon::prelude::*;

    if trades.is_empty() {
        return Err(PyValueError::new_err("No trades provided"));
    }

    let returns: Vec<f64> = trades.iter().map(|t| t.profit).collect();
    let mut rng = rand::thread_rng();

    let results: Vec<bool> = (0..num_simulations)
        .into_par_iter()
        .map(|_| {
            // Bootstrap resampling
            let mut simulation_returns = Vec::new();
            for _ in 0..trades.len() {
                let idx = rng.gen_range(0..returns.len());
                simulation_returns.push(returns[idx]);
            }

            // Run simulation
            let mut equity = challenge_params.account_size;
            let mut peak_equity = equity;
            let mut daily_pl = 0.0;
            let mut passed = true;

            for &ret in &simulation_returns {
                let position_size = equity * risk_fraction;
                let trade_pl = position_size * (ret / 100.0); // Assuming returns are in percent
                daily_pl += trade_pl;
                equity += trade_pl;

                // Check daily loss limit
                if daily_pl / challenge_params.account_size < -challenge_params.max_daily_loss_percent / 100.0 {
                    passed = false;
                    break;
                }

                // Check overall loss limit
                if equity < challenge_params.account_size * (1.0 - challenge_params.max_overall_loss_percent / 100.0) {
                    passed = false;
                    break;
                }

                // Check profit target
                if equity >= challenge_params.account_size * (1.0 + challenge_params.profit_target_percent / 100.0) {
                    break; // Success
                }

                // Reset daily P&L at end of day (simplified)
                if simulation_returns.len() > 100 { // Arbitrary day length
                    daily_pl = 0.0;
                }
            }

            passed && equity >= challenge_params.account_size * (1.0 + challenge_params.profit_target_percent / 100.0)
        })
        .collect();

    let pass_count = results.iter().filter(|&&p| p).count();
    let pass_rate = pass_count as f64 / num_simulations as f64;

    let mut result = HashMap::new();
    result.insert("pass_rate".to_string(), pass_rate);
    result.insert("total_simulations".to_string(), num_simulations as f64);
    result.insert("passed_simulations".to_string(), pass_count as f64);

    Ok(result)
}

/// A Python module implemented in Rust.
#[pymodule]
fn risk_optima_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Trade>()?;
    m.add_class::<PerformanceMetrics>()?;
    m.add_class::<ChallengeParams>()?;
    m.add_function(wrap_pyfunction!(parse_mt5_csv, m)?)?;
    m.add_function(wrap_pyfunction!(parse_mt5_xml, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_performance_metrics, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_kelly_criterion, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_optimal_f, m)?)?;
    m.add_function(wrap_pyfunction!(run_monte_carlo_simulation, m)?)?;
    Ok(())
}
