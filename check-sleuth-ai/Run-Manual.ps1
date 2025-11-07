# Check Sleuth AI - PowerShell Startup Script
# UTF-8 Encoding

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Check Sleuth AI - Manual Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Prerequisites
Write-Host "Step 1/5: Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

Write-Host "[Check] Node.js version..." -ForegroundColor Gray
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not installed!" -ForegroundColor Red
    Write-Host "Please download from https://nodejs.org/" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "[Check] Python version..." -ForegroundColor Gray
try {
    $pythonVersion = python --version
    Write-Host "✓ Python installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not installed!" -ForegroundColor Red
    Write-Host "Please download from https://python.org/" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""

# Step 2: Install Frontend Dependencies
Write-Host "Step 2/5: Installing frontend dependencies..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
Write-Host ""

if (!(Test-Path "node_modules")) {
    Write-Host "[Installing] Frontend dependencies (npm install)..." -ForegroundColor Gray
    Write-Host "This may take a few minutes..." -ForegroundColor Gray
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Frontend dependencies installation failed" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✓ Frontend dependencies already exist, skipping" -ForegroundColor Green
}

Write-Host ""

# Step 3: Install Backend Dependencies
Write-Host "Step 3/5: Installing backend dependencies..." -ForegroundColor Yellow
Write-Host ""

Push-Location ..\backend
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
Write-Host ""

Write-Host "[Check] Is Flask installed..." -ForegroundColor Gray
python -c "import flask" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[Installing] Backend dependencies (pip install)..." -ForegroundColor Gray
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Backend dependencies installation failed" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "✓ Backend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✓ Backend dependencies already installed" -ForegroundColor Green
}

Pop-Location
Write-Host ""

# Step 4: Configure Environment Variables
Write-Host "Step 4/5: Configuring environment variables..." -ForegroundColor Yellow
Write-Host ""

if ([string]::IsNullOrEmpty($env:GEMINI_API_KEY)) {
    Write-Host "⚠ GEMINI_API_KEY not set" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You have two options:"
    Write-Host "  1. Press any key to continue (use Mock data demo mode)"
    Write-Host "  2. Press Ctrl+C to exit, set manually and re-run"
    Write-Host ""
    Write-Host "To set (PowerShell):"
    Write-Host '  $env:GEMINI_API_KEY="your-api-key"' -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Get API Key: https://makersuite.google.com/app/apikey"
    Write-Host ""
    pause
    Write-Host ""
    Write-Host "▶ Will run in Mock data mode" -ForegroundColor Yellow
} else {
    Write-Host "✓ GEMINI_API_KEY is set" -ForegroundColor Green
}

Write-Host ""

# Step 5: Start Services
Write-Host "Step 5/5: Starting services..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Will start two servers..." -ForegroundColor Gray
Write-Host ""
Write-Host "📌 Important notes:"
Write-Host "  - Will open 2 new windows"
Write-Host "  - Backend server: http://localhost:5000"
Write-Host "  - Frontend server: http://localhost:3000"
Write-Host "  - Keep both windows running"
Write-Host "  - Press Ctrl+C to stop any server"
Write-Host ""
pause

Write-Host ""
Write-Host "[Starting] Backend server..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\..\backend'; python app.py"
Start-Sleep -Seconds 3

Write-Host "[Starting] Frontend dev server..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; npm run dev"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Startup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Server addresses:"
Write-Host "  Backend API:  http://localhost:5000"
Write-Host "  Frontend app: http://localhost:3000"
Write-Host ""
Write-Host "🧪 Test file:"
Write-Host "  test_sample.csv (ready to upload)"
Write-Host ""
Write-Host "📖 Detailed instructions:"
Write-Host "  MANUAL_SETUP.md (complete steps and troubleshooting)"
Write-Host ""
Write-Host "🔍 Verify servers:"
Write-Host "  In a new PowerShell window run:"
Write-Host '  curl http://localhost:5000/health' -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠ Note:"
Write-Host "  - Keep the two new windows running"
Write-Host "  - Do not close them, or services will stop"
Write-Host "  - To stop services, press Ctrl+C in each window"
Write-Host ""
Write-Host "🎉 You can now visit http://localhost:3000 in your browser!"
Write-Host ""
pause

Write-Host ""
Write-Host "Open app in default browser? (Y/N)"
$choice = Read-Host
if ($choice -eq "Y" -or $choice -eq "y") {
    Write-Host "Opening browser..." -ForegroundColor Gray
    Start-Process "http://localhost:3000"
}

Write-Host ""
Write-Host "If you have questions, check MANUAL_SETUP.md or ask anytime!"
Write-Host ""
pause
