@echo off
REM RiskOptima Engine - MQL5 Build Script
REM This script compiles MQL5 components for MetaTrader 5

echo ========================================
echo RiskOptima Engine - MQL5 Build Script
echo ========================================

REM Check if MetaEditor is available
where metaeditor >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: MetaEditor not found in PATH
    echo Please ensure MetaTrader 5 is installed and metaeditor.exe is in PATH
    pause
    exit /b 1
)

REM Set paths
set "MQL5_SRC_DIR=%~dp0..\mql5"
set "MT5_ROOT=%APPDATA%\MetaQuotes\Terminal"
set "MQL5_DEST_DIR=%MT5_ROOT%\MQL5"

echo Source directory: %MQL5_SRC_DIR%
echo Destination directory: %MQL5_DEST_DIR%

REM Check if source directory exists
if not exist "%MQL5_SRC_DIR%" (
    echo ERROR: MQL5 source directory not found: %MQL5_SRC_DIR%
    pause
    exit /b 1
)

REM Create destination directories
echo Creating destination directories...
if not exist "%MQL5_DEST_DIR%\Experts" mkdir "%MQL5_DEST_DIR%\Experts"
if not exist "%MQL5_DEST_DIR%\Include" mkdir "%MQL5_DEST_DIR%\Include"
if not exist "%MQL5_DEST_DIR%\Scripts" mkdir "%MQL5_DEST_DIR%\Scripts"
if not exist "%MQL5_DEST_DIR%\Files\RiskOptima" mkdir "%MQL5_DEST_DIR%\Files\RiskOptima"

REM Copy MQL5 files
echo Copying MQL5 files...
if exist "%MQL5_SRC_DIR%\Experts\*" (
    copy "%MQL5_SRC_DIR%\Experts\*" "%MQL5_DEST_DIR%\Experts\"
    echo Copied Expert Advisors
)

if exist "%MQL5_SRC_DIR%\Include\*" (
    copy "%MQL5_SRC_DIR%\Include\*" "%MQL5_DEST_DIR%\Include\"
    echo Copied Include files
)

if exist "%MQL5_SRC_DIR%\Scripts\*" (
    copy "%MQL5_SRC_DIR%\Scripts\*" "%MQL5_DEST_DIR%\Scripts\"
    echo Copied Scripts
)

REM Compile Expert Advisor
echo.
echo Compiling RiskOptimaEA.mq5...
metaeditor /compile:"%MQL5_DEST_DIR%\Experts\RiskOptimaEA.mq5" /log
if %errorlevel% neq 0 (
    echo ERROR: Failed to compile RiskOptimaEA.mq5
    echo Check the compilation log above for details
) else (
    echo SUCCESS: RiskOptimaEA.mq5 compiled successfully
)

REM Compile Test Script
echo.
echo Compiling RiskOptimaTester.mq5...
metaeditor /compile:"%MQL5_DEST_DIR%\Scripts\RiskOptimaTester.mq5" /log
if %errorlevel% neq 0 (
    echo ERROR: Failed to compile RiskOptimaTester.mq5
    echo Check the compilation log above for details
) else (
    echo SUCCESS: RiskOptimaTester.mq5 compiled successfully
)

REM Verify compilation
echo.
echo Verifying compilation results...
if exist "%MQL5_DEST_DIR%\Experts\RiskOptimaEA.ex5" (
    echo ✓ RiskOptimaEA.ex5 found
) else (
    echo ✗ RiskOptimaEA.ex5 not found - compilation may have failed
)

if exist "%MQL5_DEST_DIR%\Scripts\RiskOptimaTester.ex5" (
    echo ✓ RiskOptimaTester.ex5 found
) else (
    echo ✗ RiskOptimaTester.ex5 not found - compilation may have failed
)

echo.
echo ========================================
echo Build Summary
echo ========================================
echo MQL5 components have been copied to: %MQL5_DEST_DIR%
echo.
echo Next steps:
echo 1. Open MetaTrader 5 terminal
echo 2. Navigate to Experts in the Navigator
echo 3. Find and attach RiskOptimaEA to a chart
echo 4. Configure the Expert Advisor parameters
echo 5. Enable automated trading
echo.
echo For testing:
echo 1. Run RiskOptimaTester script from Scripts
echo 2. Check terminal logs for test results
echo ========================================

pause