@echo off
REM PANDA 系统快速启动脚本 (Windows)
REM 用途：一键启动前后端服务

setlocal enabledelayedexpansion

echo ========================================
echo PANDA 系统快速启动
echo ========================================
echo.

REM 检查Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到Python
    echo 请先安装Python 3.9+
    pause
    exit /b 1
)

REM 检查Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到Node.js
    echo 请先安装Node.js 16+
    pause
    exit /b 1
)

REM 检查MySQL
where mysql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [警告] 未找到MySQL命令
    echo 请确保MySQL服务已启动
)

echo [1/5] 检查数据库...
set /p DB_PASSWORD="请输入MySQL密码: "
mysql -u root -p%DB_PASSWORD% -e "USE panda;" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [警告] 数据库不存在，是否现在部署？(Y/N)
    set /p DEPLOY_DB=
    if /i "!DEPLOY_DB!"=="Y" (
        call backend\scripts\deploy_database.bat
    ) else (
        echo 请先部署数据库
        pause
        exit /b 1
    )
)
echo [成功] 数据库检查通过
echo.

echo [2/5] 检查后端依赖...
if not exist "backend\venv" (
    echo [提示] 创建Python虚拟环境...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
)
echo [成功] 后端依赖检查通过
echo.

echo [3/5] 检查前端依赖...
if not exist "frontend\node_modules" (
    echo [提示] 安装前端依赖...
    cd frontend
    call npm install
    cd ..
)
echo [成功] 前端依赖检查通过
echo.

echo [4/5] 启动后端服务...
start "PANDA Backend" cmd /k "cd backend && venv\Scripts\activate && python start.py"
timeout /t 3 >nul
echo [成功] 后端服务已启动: http://localhost:8000
echo.

echo [5/5] 启动前端服务...
start "PANDA Frontend" cmd /k "cd frontend && npm run dev"
timeout /t 3 >nul
echo [成功] 前端服务已启动: http://localhost:5173
echo.

echo ========================================
echo 🎉 PANDA系统启动成功！
echo ========================================
echo.
echo 服务地址：
echo 前端: http://localhost:5173
echo 后端: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 默认账号：
echo 管理员: admin@panda.com / admin123
echo 讲师:   teacher@panda.com / admin123
echo 学员:   nurse1@hospital.com / admin123
echo.
echo 按任意键打开浏览器...
pause >nul

start http://localhost:5173

echo.
echo 提示：关闭此窗口不会停止服务
echo 要停止服务，请关闭对应的命令行窗口
echo.
pause
