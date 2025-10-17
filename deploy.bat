@echo off
REM ========================================
REM Sleuth v1.1 - Complete Deployment Script
REM ========================================

echo ========================================
echo Sleuth v1.1 Deployment
echo ========================================
echo.

REM Step 1: Git commit and push
echo [Step 1/3] Committing changes to Git...
echo.

git status

echo.
set /p confirm="Do you want to commit and push these changes? (y/n): "
if /i "%confirm%" NEQ "y" (
    echo Deployment cancelled.
    pause
    exit /b
)

echo.
echo Adding all changes...
git add .

echo.
echo Creating commit...
git commit -m "feat(v1.1): Add comprehensive enhancements - Bootstrap, LLM support, data validation, visualizations"

echo.
echo Pushing to GitHub...
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ Git push failed. Please check your credentials and try again.
    pause
    exit /b 1
)

echo.
echo ✅ Successfully pushed to GitHub!
echo.

REM Step 2: Build and deploy web app
echo [Step 2/3] Building Web App...
echo.

cd web-app

echo Installing dependencies (if needed)...
call npm install

if %errorlevel% neq 0 (
    echo.
    echo ❌ npm install failed.
    pause
    exit /b 1
)

echo.
echo Building production bundle...
call npm run build

if %errorlevel% neq 0 (
    echo.
    echo ❌ Build failed.
    cd ..
    pause
    exit /b 1
)

echo.
echo ✅ Build successful!
echo.

REM Step 3: Deploy to GitHub Pages
echo [Step 3/3] Deploying to GitHub Pages...
echo.

call npm run deploy

if %errorlevel% neq 0 (
    echo.
    echo ❌ Deployment failed.
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo ========================================
echo 🎉 DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo ✅ Code committed and pushed to GitHub
echo ✅ Web App built successfully
echo ✅ Deployed to GitHub Pages
echo.
echo 🌐 Your website will be live at:
echo    https://hongping-zh.github.io/circular-bias-detection/
echo.
echo ⏰ GitHub Pages may take 1-3 minutes to update.
echo    Refresh your browser if you don't see changes immediately.
echo.
echo ========================================
pause
