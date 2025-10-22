# RiskOptima Engine Run Script for Windows
# This script provides convenient commands to run the application

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("full", "backend", "frontend", "setup", "build")]
    [string]$Command = "full",

    [Parameter(Mandatory=$false)]
    [string]$Host = "127.0.0.1",

    [Parameter(Mandatory=$false)]
    [int]$Port = 8000
)

Write-Host "RiskOptima Engine Runner" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green

# Set working directory to project root
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

switch ($Command) {
    "setup" {
        Write-Host "Running setup script..." -ForegroundColor Yellow
        & $PSScriptRoot\setup.ps1
    }

    "build" {
        Write-Host "Building Rust extension..." -ForegroundColor Yellow
        try {
            & maturin develop
            Write-Host "✅ Rust extension built successfully" -ForegroundColor Green
        } catch {
            Write-Host "❌ Build failed" -ForegroundColor Red
            exit 1
        }
    }

    "backend" {
        Write-Host "Starting backend server on $Host`:$Port..." -ForegroundColor Yellow
        Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
        Write-Host "" -ForegroundColor Yellow

        try {
            & python -m risk_optima_engine backend --host $Host --port $Port
        } catch {
            Write-Host "❌ Backend failed to start" -ForegroundColor Red
        }
    }

    "frontend" {
        Write-Host "Starting Streamlit frontend..." -ForegroundColor Yellow
        Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
        Write-Host "" -ForegroundColor Yellow

        try {
            & python -m risk_optima_engine frontend
        } catch {
            Write-Host "❌ Frontend failed to start" -ForegroundColor Red
        }
    }

    "full" {
        Write-Host "Starting full RiskOptima Engine application..." -ForegroundColor Yellow
        Write-Host "Backend: http://$Host`:$Port" -ForegroundColor White
        Write-Host "Frontend: http://localhost:8501" -ForegroundColor White
        Write-Host "API Docs: http://$Host`:$Port/docs" -ForegroundColor White
        Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
        Write-Host "" -ForegroundColor Yellow

        try {
            & python -m risk_optima_engine full --host $Host --port $Port
        } catch {
            Write-Host "❌ Application failed to start" -ForegroundColor Red
        }
    }

    default {
        Write-Host "Usage: .\run.ps1 [-Command] {full|backend|frontend|setup|build} [-Host hostname] [-Port port]" -ForegroundColor Yellow
        Write-Host "" -ForegroundColor Yellow
        Write-Host "Commands:" -ForegroundColor White
        Write-Host "  full     - Run both backend and frontend (default)" -ForegroundColor White
        Write-Host "  backend  - Run only the FastAPI backend" -ForegroundColor White
        Write-Host "  frontend - Run only the Streamlit frontend" -ForegroundColor White
        Write-Host "  setup    - Run the setup script" -ForegroundColor White
        Write-Host "  build    - Build the Rust extension" -ForegroundColor White
        Write-Host "" -ForegroundColor Yellow
        Write-Host "Examples:" -ForegroundColor White
        Write-Host "  .\run.ps1" -ForegroundColor White
        Write-Host "  .\run.ps1 -Command backend -Port 8080" -ForegroundColor White
        Write-Host "  .\run.ps1 -Command setup" -ForegroundColor White
    }
}