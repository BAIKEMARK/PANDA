@echo off
REM ================================================
REM PANDA - 围产期抑郁管理智能培训系统
REM 项目初始化脚本 (Windows)
REM ================================================

echo.
echo ===============================================
echo PANDA 项目初始化
echo ===============================================
echo.

REM 检查 Python
echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装或未添加到 PATH
    echo 请安装 Python 3.12.12: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo ✅ Python 环境正常
echo.

REM 检查 Node.js
echo [2/5] 检查 Node.js 环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装或未添加到 PATH
    echo 请安装 Node.js v20.15.1: https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo ✅ Node.js 环境正常
echo.

REM 检查 MySQL
echo [3/5] 检查 MySQL 环境...
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  MySQL 未安装或未添加到 PATH
    echo 请安装 MySQL 8.0.43+: https://dev.mysql.com/downloads/mysql/
    echo.
    set /p continue="是否继续初始化? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
) else (
    mysql --version
    echo ✅ MySQL 环境正常
    echo.
)

REM 安装后端依赖
echo [4/5] 安装 Python 后端依赖...
cd app
if not exist ".env" (
    echo 创建 .env 配置文件...
    copy .env.example .env
    echo ⚠️  请编辑 app\.env 文件，配置数据库密码和AI密钥
)
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Python 依赖安装失败
    pause
    exit /b 1
)
echo ✅ Python 依赖安装完成
echo.

REM 安装前端依赖
echo [5/5] 安装 Node.js 前端依赖...
cd ..\frontend
if not exist ".env.local" (
    echo 创建 .env.local 配置文件...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > .env.local
)
call npm install
if %errorlevel% neq 0 (
    echo ❌ Node.js 依赖安装失败
    pause
    exit /b 1
)
echo ✅ Node.js 依赖安装完成
echo.

cd ..

echo.
echo ===============================================
echo ✅ 项目初始化完成！
echo ===============================================
echo.
echo 下一步操作：
echo.
echo 1. 配置数据库：
echo    mysql -u root -p ^< app\database\schema.sql
echo.
echo 2. 配置环境变量：
echo    编辑 app\.env 文件，设置：
echo    - DB_PASSWORD (MySQL密码)
echo    - AI_TEXT_KEY (阿里百炼API密钥)
echo.
echo 3. 启动后端服务：
echo    cd app ^&^& python main.py
echo.
echo 4. 启动前端服务（新终端）：
echo    cd frontend ^&^& npm run dev
echo.
echo 5. 访问应用：
echo    前端: http://localhost:3000
echo    API文档: http://localhost:8000/api/docs
echo.
echo ===============================================
pause
