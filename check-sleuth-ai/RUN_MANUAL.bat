@echo off
chcp 65001 >nul
echo ========================================
echo Check Sleuth AI - 手动启动助手
echo ========================================
echo.
echo 📖 完整步骤请查看: MANUAL_SETUP.md
echo.
echo ⚡ 这个脚本将帮助你分步启动服务
echo.
pause

echo.
echo ========================================
echo 步骤 1/5: 检查前置条件
echo ========================================
echo.

echo [检查] Node.js 版本...
node --version
if errorlevel 1 (
    echo ❌ Node.js 未安装！
    echo 请从 https://nodejs.org/ 下载安装
    pause
    exit /b 1
)
echo ✅ Node.js 已安装
echo.

echo [检查] Python 版本...
python --version
if errorlevel 1 (
    echo ❌ Python 未安装！
    echo 请从 https://python.org/ 下载安装
    pause
    exit /b 1
)
echo ✅ Python 已安装
echo.

echo ========================================
echo 步骤 2/5: 安装前端依赖
echo ========================================
echo.
echo 当前目录: %cd%
echo.

if not exist "node_modules" (
    echo [安装] 前端依赖 (npm install)...
    echo 这可能需要几分钟，请耐心等待...
    call npm install
    if errorlevel 1 (
        echo ❌ 前端依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 前端依赖安装完成
) else (
    echo ✅ 前端依赖已存在，跳过安装
)
echo.

echo ========================================
echo 步骤 3/5: 安装后端依赖
echo ========================================
echo.

cd ..\backend
echo 当前目录: %cd%
echo.

echo [检查] Flask 是否已安装...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [安装] 后端依赖 (pip install)...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 后端依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 后端依赖安装完成
) else (
    echo ✅ 后端依赖已安装
)
echo.

echo ========================================
echo 步骤 4/5: 配置环境变量
echo ========================================
echo.

if "%GEMINI_API_KEY%"=="" (
    echo ⚠️  GEMINI_API_KEY 未设置
    echo.
    echo 你有两个选择:
    echo   1. 按任意键继续（使用 Mock 数据演示模式）
    echo   2. 按 Ctrl+C 退出，手动设置后重新运行
    echo.
    echo 设置方法（PowerShell）:
    echo   $env:GEMINI_API_KEY="your-api-key"
    echo.
    echo 获取 API Key: https://makersuite.google.com/app/apikey
    echo.
    pause
    echo.
    echo ▶ 将使用 Mock 数据模式运行
) else (
    echo ✅ GEMINI_API_KEY 已设置
)
echo.

echo ========================================
echo 步骤 5/5: 启动服务
echo ========================================
echo.
echo 即将启动两个服务器...
echo.
echo 📌 重要提示:
echo   - 将打开 2 个新的命令行窗口
echo   - 后端服务器: http://localhost:5000
echo   - 前端服务器: http://localhost:3000
echo   - 请保持这两个窗口运行
echo   - 按 Ctrl+C 可以停止任一服务器
echo.
pause

echo.
echo [启动] 后端服务器...
start "🔧 Sleuth Backend - Port 5000" cmd /k "cd %~dp0..\backend && python app.py"
timeout /t 3 /nobreak >nul

echo [启动] 前端开发服务器...
cd %~dp0
start "🌐 Sleuth Frontend - Port 3000" cmd /k "npm run dev"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo ✅ 启动完成！
echo ========================================
echo.
echo 📊 服务器地址:
echo   后端 API:  http://localhost:5000
echo   前端应用:  http://localhost:3000
echo.
echo 🧪 测试文件:
echo   test_sample.csv (已准备好，可直接上传)
echo.
echo 📖 详细说明:
echo   MANUAL_SETUP.md (完整步骤和故障排查)
echo.
echo 🔍 验证服务器:
echo   在新的 PowerShell 中运行:
echo   curl http://localhost:5000/health
echo.
echo ⚠️  注意:
echo   - 请保持新开的两个窗口运行
echo   - 不要关闭它们，否则服务会停止
echo   - 要停止服务，在相应窗口按 Ctrl+C
echo.
echo 🎉 现在可以在浏览器访问 http://localhost:3000 了！
echo.
pause

echo.
echo 是否要在默认浏览器中打开应用？(Y/N)
choice /C YN /N
if errorlevel 2 goto :end
if errorlevel 1 (
    echo 正在打开浏览器...
    start http://localhost:3000
)

:end
echo.
echo 有问题请查看 MANUAL_SETUP.md 或随时请教！
echo.
pause
