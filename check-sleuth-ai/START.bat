@echo off
echo ========================================
echo Check Sleuth AI - Quick Start
echo ========================================
echo.

echo Step 1: Checking if dependencies are installed...
if not exist "node_modules" (
    echo [!] Node modules not found. Installing...
    call npm install
    echo.
) else (
    echo [✓] Node modules found
    echo.
)

echo Step 2: Checking backend dependencies...
cd ..\backend
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [!] Backend dependencies not found. Installing...
    pip install -r requirements.txt
    echo.
) else (
    echo [✓] Backend dependencies found
    echo.
)

echo Step 3: Checking for GEMINI_API_KEY...
if "%GEMINI_API_KEY%"=="" (
    echo [!] GEMINI_API_KEY not set!
    echo.
    echo Please set your Gemini API key:
    echo     PowerShell: $env:GEMINI_API_KEY="your-key"
    echo     CMD:        set GEMINI_API_KEY=your-key
    echo.
    echo Get your API key from: https://makersuite.google.com/app/apikey
    echo.
    echo [i] The app will run with MOCK DATA if API key is not set.
    pause
) else (
    echo [✓] GEMINI_API_KEY is set
    echo.
)

echo Step 4: Starting backend server...
start "Sleuth Backend" cmd /k "cd %~dp0..\backend && python app.py"
timeout /t 3 >nul

echo Step 5: Starting frontend dev server...
cd %~dp0
start "Sleuth Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo Services Starting...
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Two terminal windows will open.
echo Press Ctrl+C in each to stop the servers.
echo.
pause
