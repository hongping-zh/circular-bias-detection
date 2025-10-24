@echo off
REM Batch script to run circular bias amplification simulation
REM For Windows systems

echo ========================================
echo Circular Bias Amplification Simulation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
pip show numpy >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Dependencies already installed.
)

echo.
echo [2/3] Running simulation...
echo This may take 10-30 seconds...
echo.

python iterative_learning_simulation.py

if errorlevel 1 (
    echo.
    echo ERROR: Simulation failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Simulation complete!
echo.
echo Results saved to: simulation_results\
echo   - figure5_simulation_results.png
echo   - metrics.json
echo.
echo Opening results folder...
start simulation_results

pause
