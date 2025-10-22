# RiskOptima Engine Setup Script for Windows
# This script sets up the development environment

Write-Host "RiskOptima Engine Setup Script" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if Rust is installed
Write-Host "Checking Rust installation..." -ForegroundColor Yellow
try {
    $rustVersion = & rustc --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Rust is installed: $rustVersion" -ForegroundColor Green
    } else {
        throw "Rust not found"
    }
} catch {
    Write-Host "❌ Rust is not installed. Please install Rust from https://rustup.rs/" -ForegroundColor Red
    Write-Host "After installing Rust, run this script again." -ForegroundColor Yellow
    exit 1
}

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python is installed: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.9+ from https://python.org/" -ForegroundColor Red
    exit 1
}

# Check if uv is installed
Write-Host "Checking uv installation..." -ForegroundColor Yellow
try {
    $uvVersion = & uv --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ uv is installed: $uvVersion" -ForegroundColor Green
    } else {
        throw "uv not found"
    }
} catch {
    Write-Host "❌ uv is not installed. Installing uv..." -ForegroundColor Yellow
    try {
        & python -m pip install uv
        Write-Host "✅ uv installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install uv. Please install manually: pip install uv" -ForegroundColor Red
        exit 1
    }
}

# Check if maturin is installed
Write-Host "Checking maturin installation..." -ForegroundColor Yellow
try {
    $maturinVersion = & maturin --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ maturin is installed: $maturinVersion" -ForegroundColor Green
    } else {
        throw "maturin not found"
    }
} catch {
    Write-Host "❌ maturin is not installed. Installing maturin..." -ForegroundColor Yellow
    try {
        & python -m pip install maturin
        Write-Host "✅ maturin installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install maturin. Please install manually: pip install maturin" -ForegroundColor Red
        exit 1
    }
}

# Check for Visual Studio Build Tools (required for Rust on Windows)
Write-Host "Checking for Visual Studio Build Tools..." -ForegroundColor Yellow
try {
    $vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
    if (Test-Path $vswhere) {
        $vsInstallation = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
        if ($vsInstallation) {
            Write-Host "✅ Visual Studio Build Tools found at: $vsInstallation" -ForegroundColor Green
        } else {
            throw "Visual Studio Build Tools not found"
        }
    } else {
        throw "vswhere not found"
    }
} catch {
    Write-Host "⚠️  Visual Studio Build Tools not found or not properly configured." -ForegroundColor Yellow
    Write-Host "   This is required for Rust compilation on Windows." -ForegroundColor Yellow
    Write-Host "   Please install Visual Studio 2019/2022 with C++ build tools, or:" -ForegroundColor Yellow
    Write-Host "   Download Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/" -ForegroundColor Yellow
    Write-Host "" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 1
    }
}

# Set up the project
Write-Host "Setting up RiskOptima Engine project..." -ForegroundColor Yellow

# Navigate to project directory
Set-Location $PSScriptRoot\..

# Sync Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    & uv sync
    Write-Host "✅ Python dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}

# Build Rust extension
Write-Host "Building Rust extension..." -ForegroundColor Yellow
try {
    & maturin develop
    Write-Host "✅ Rust extension built successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to build Rust extension" -ForegroundColor Red
    Write-Host "Error details:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Write-Host "" -ForegroundColor Green
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "To run the application:" -ForegroundColor White
Write-Host "  • Full application: python -m risk_optima_engine full" -ForegroundColor White
Write-Host "  • Backend only:    python -m risk_optima_engine backend" -ForegroundColor White
Write-Host "  • Frontend only:   python -m risk_optima_engine frontend" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "The application will be available at:" -ForegroundColor White
Write-Host "  • Frontend: http://localhost:8501" -ForegroundColor White
Write-Host "  • Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  • API Docs: http://localhost:8000/docs" -ForegroundColor White