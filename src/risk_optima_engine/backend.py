"""
FastAPI backend for RiskOptima Engine
Provides REST API endpoints for all system operations
"""

import asyncio
import tempfile
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

try:
    from . import (
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
except ImportError:
    # Fallback for when Rust extension is not built
    Trade = None
    PerformanceMetrics = None
    ChallengeParams = None
    parse_mt5_csv = None
    parse_mt5_xml = None
    calculate_performance_metrics = None
    calculate_kelly_criterion = None
    calculate_optimal_f = None
    run_monte_carlo_simulation = None

from .mt5_integration import (
    connect_mt5,
    disconnect_mt5,
    get_mt5_account_info,
    get_mt5_connection_status,
)

# Pydantic models for API
class UploadResponse(BaseModel):
    file_id: str
    status: str
    message: str

class AnalysisRequest(BaseModel):
    file_id: str
    parameters: Optional[Dict[str, Any]] = None

class PerformanceResponse(BaseModel):
    kpis: Dict[str, Any]
    equity_curve: List[float]
    status: str

class KellyRequest(BaseModel):
    performance_data: Dict[str, Any]
    fractional_multiplier: float = Field(default=1.0, ge=0.0, le=1.0)

class KellyResponse(BaseModel):
    optimal_fraction: float
    warnings: List[str]

class OptimalFRequest(BaseModel):
    trade_data: List[Dict[str, Any]]
    parameters: Optional[Dict[str, Any]] = None

class OptimalFResponse(BaseModel):
    optimal_f: float
    twr: float
    sensitivity: Dict[str, Any]

class ChallengeRequest(BaseModel):
    challenge_params: Dict[str, Any]
    trade_data: List[Dict[str, Any]]
    simulation_count: int = Field(default=1000, ge=100, le=10000)

class OptimizationResponse(BaseModel):
    recommended_fraction: float
    pass_rate: float
    confidence_interval: List[float]
    status: str

class TaskStatus(BaseModel):
    status: str
    progress: float
    eta: Optional[str] = None

class ConnectionRequest(BaseModel):
    timeout: int = Field(default=30, ge=5, le=300)

class ConnectionResponse(BaseModel):
    connected: bool
    account_info: Optional[Dict[str, Any]] = None

class AccountInfo(BaseModel):
    balance: float
    equity: float
    margin: float

class ReportRequest(BaseModel):
    report_type: str
    data: Dict[str, Any]
    format: str = Field(default="pdf", regex="^(pdf|csv)$")

class ReportResponse(BaseModel):
    report_id: str
    download_url: str

# Global state (in production, use proper database/cache)
uploaded_files: Dict[str, str] = {}
background_tasks: Dict[str, Dict[str, Any]] = {}

app = FastAPI(
    title="RiskOptima Engine API",
    description="Quantitative Risk Analysis and Management Tool for MT5 Traders",
    version="1.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_trades_from_data(trade_data: List[Dict[str, Any]]) -> List[Trade]:
    """Convert API trade data to Trade objects"""
    if Trade is None:
        raise ValueError("Rust extension not available")

    trades = []
    for data in trade_data:
        trade = Trade(
            symbol=data.get("symbol", ""),
            trade_type=data.get("trade_type", ""),
            volume=data.get("volume", 0.0),
            open_price=data.get("open_price", 0.0),
            close_price=data.get("close_price", 0.0),
            profit=data.get("profit", 0.0),
            commission=data.get("commission"),
            swap=data.get("swap"),
        )
        trades.append(trade)
    return trades

@app.post("/api/v1/upload/trade-history", response_model=UploadResponse)
async def upload_trade_history(
    file: UploadFile = File(...),
    format: str = "csv"
) -> UploadResponse:
    """Upload and validate MT5 trade history file"""
    try:
        # Validate file type
        if format not in ["csv", "xml"]:
            raise HTTPException(status_code=400, detail="Unsupported format. Use 'csv' or 'xml'")

        # Read file content
        content = await file.read()
        content_str = content.decode("utf-8")

        # Parse and validate
        if format == "csv":
            if parse_mt5_csv is None:
                raise HTTPException(status_code=500, detail="Rust extension not available")
            trades = parse_mt5_csv(content_str)
        else:
            if parse_mt5_xml is None:
                raise HTTPException(status_code=500, detail="Rust extension not available")
            trades = parse_mt5_xml(content_str)

        if not trades:
            raise HTTPException(status_code=400, detail="No valid trades found in file")

        # Save file temporarily
        import uuid
        import tempfile
        import os

        file_id = str(uuid.uuid4())
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, f"{file_id}.{format}")

        with open(file_path, "wb") as f:
            f.write(content)

        uploaded_files[file_id] = file_path

        return UploadResponse(
            file_id=file_id,
            status="success",
            message=f"Successfully uploaded {len(trades)} trades"
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")

@app.get("/api/v1/upload/status/{file_id}")
async def get_upload_status(file_id: str):
    """Get status of uploaded file"""
    if file_id not in uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")

    return {"status": "ready", "progress": 1.0}

@app.post("/api/v1/analysis/performance", response_model=PerformanceResponse)
async def analyze_performance(request: AnalysisRequest):
    """Calculate performance metrics from trade data"""
    try:
        if request.file_id not in uploaded_files:
            raise HTTPException(status_code=404, detail="File not found")

        file_path = uploaded_files[request.file_id]

        # Read and parse file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Determine format from file extension
        if file_path.endswith(".csv"):
            if parse_mt5_csv is None:
                raise HTTPException(status_code=500, detail="Rust extension not available")
            trades = parse_mt5_csv(content)
        else:
            if parse_mt5_xml is None:
                raise HTTPException(status_code=500, detail="Rust extension not available")
            trades = parse_mt5_xml(content)

        # Calculate metrics
        if calculate_performance_metrics is None:
            raise HTTPException(status_code=500, detail="Rust extension not available")
        metrics = calculate_performance_metrics(trades)

        # Generate equity curve
        equity_curve = []
        equity = 0.0
        for trade in trades:
            equity += trade.profit
            equity_curve.append(equity)

        return PerformanceResponse(
            kpis={
                "total_trades": metrics.total_trades,
                "win_probability": metrics.win_probability,
                "loss_probability": metrics.loss_probability,
                "avg_win": metrics.avg_win,
                "avg_loss": metrics.avg_loss,
                "win_loss_ratio": metrics.win_loss_ratio,
                "profit_factor": metrics.profit_factor,
                "expectancy": metrics.expectancy,
                "max_drawdown": metrics.max_drawdown,
                "sharpe_ratio": metrics.sharpe_ratio,
            },
            equity_curve=equity_curve,
            status="success"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/v1/analysis/kelly", response_model=KellyResponse)
async def calculate_kelly(request: KellyRequest):
    """Calculate Kelly Criterion optimal bet size"""
    try:
        win_prob = request.performance_data.get("win_probability", 0.0)
        win_loss_ratio = request.performance_data.get("win_loss_ratio", 0.0)

        if calculate_kelly_criterion is None:
            raise HTTPException(status_code=500, detail="Rust extension not available")

        optimal_fraction = calculate_kelly_criterion(
            win_prob,
            win_loss_ratio,
            request.fractional_multiplier
        )

        warnings = []
        if optimal_fraction > 0.1:
            warnings.append("High risk fraction detected (>10%). Consider using fractional Kelly.")
        if optimal_fraction < 0:
            warnings.append("Negative Kelly fraction indicates unfavorable risk/reward.")

        return KellyResponse(
            optimal_fraction=optimal_fraction,
            warnings=warnings
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kelly calculation failed: {str(e)}")

@app.post("/api/v1/analysis/optimal-f", response_model=OptimalFResponse)
async def calculate_optimal_f_endpoint(request: OptimalFRequest):
    """Calculate Optimal F position sizing"""
    try:
        if calculate_optimal_f is None:
            raise HTTPException(status_code=500, detail="Rust extension not available")

        trades = parse_trades_from_data(request.trade_data)
        optimal_f = calculate_optimal_f(trades, 1000, 1e-6)

        # Calculate TWR for the optimal f
        largest_loss = min((t.profit for t in trades if t.profit < 0.0), default=-1.0, key=abs)

        twr = 1.0
        for trade in trades:
            twr *= 1.0 + optimal_f * (-trade.profit / abs(largest_loss))

        return OptimalFResponse(
            optimal_f=optimal_f,
            twr=twr,
            sensitivity={}  # Placeholder for future implementation
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimal F calculation failed: {str(e)}")

@app.post("/api/v1/optimization/challenge", response_model=OptimizationResponse)
async def optimize_challenge(
    request: ChallengeRequest,
    background_tasks: BackgroundTasks
):
    """Run Monte Carlo optimization for challenge parameters"""
    try:
        if run_monte_carlo_simulation is None or ChallengeParams is None:
            raise HTTPException(status_code=500, detail="Rust extension not available")

        # Parse challenge parameters
        challenge_params = ChallengeParams(
            account_size=request.challenge_params["account_size"],
            profit_target_percent=request.challenge_params["profit_target_percent"],
            max_daily_loss_percent=request.challenge_params["max_daily_loss_percent"],
            max_overall_loss_percent=request.challenge_params["max_overall_loss_percent"],
            min_trading_days=request.challenge_params["min_trading_days"],
        )

        trades = parse_trades_from_data(request.trade_data)

        # For now, run synchronously (implement async background tasks later)
        # Test different risk fractions
        risk_fractions = [0.001, 0.002, 0.005, 0.01, 0.015, 0.02]  # 0.1% to 2.0%
        best_fraction = 0.0
        best_pass_rate = 0.0

        for risk_fraction in risk_fractions:
            results = run_monte_carlo_simulation(
                trades,
                challenge_params,
                risk_fraction,
                request.simulation_count
            )

            pass_rate = results.get("pass_rate", 0.0)
            if pass_rate > best_pass_rate:
                best_pass_rate = pass_rate
                best_fraction = risk_fraction

        return OptimizationResponse(
            recommended_fraction=best_fraction,
            pass_rate=best_pass_rate,
            confidence_interval=[best_pass_rate - 0.05, best_pass_rate + 0.05],  # Simplified
            status="success"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@app.get("/api/v1/optimization/status/{task_id}")
async def get_optimization_status(task_id: str):
    """Get status of optimization task"""
    if task_id not in background_tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    return background_tasks[task_id]

# MT5 Integration endpoints
@app.post("/api/v1/mt5/connect", response_model=ConnectionResponse)
async def connect_mt5_endpoint(request: ConnectionRequest):
    """Connect to MT5 terminal"""
    try:
        success, error_msg = connect_mt5(request.timeout)
        if success:
            account_info = get_mt5_account_info()
            return ConnectionResponse(connected=True, account_info=account_info)
        else:
            return ConnectionResponse(connected=False, account_info=None)
    except Exception as e:
        return ConnectionResponse(connected=False, account_info=None)

@app.get("/api/v1/mt5/account-info", response_model=AccountInfo)
async def get_account_info():
    """Get MT5 account information"""
    try:
        account_data = get_mt5_account_info()
        if account_data:
            return AccountInfo(
                balance=account_data.get("balance", 0.0),
                equity=account_data.get("equity", 0.0),
                margin=account_data.get("margin", 0.0)
            )
        else:
            return AccountInfo(balance=0.0, equity=0.0, margin=0.0)
    except Exception as e:
        return AccountInfo(balance=0.0, equity=0.0, margin=0.0)

@app.post("/api/v1/reports/generate", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """Generate analysis report"""
    # Placeholder - implement report generation
    import uuid
    report_id = str(uuid.uuid4())
    return ReportResponse(
        report_id=report_id,
        download_url=f"/api/v1/reports/download/{report_id}"
    )

@app.get("/api/v1/reports/download/{report_id}")
async def download_report(report_id: str):
    """Download generated report"""
    # Placeholder - implement report download
    raise HTTPException(status_code=404, detail="Report not found")

def run_backend(host: str = "127.0.0.1", port: int = 8000):
    """Run the FastAPI backend server"""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_backend()