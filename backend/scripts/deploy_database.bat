@echo off
REM PANDA 数据库快速部署脚本 (Windows)
REM 用途：在新环境中一键部署数据库

setlocal enabledelayedexpansion

REM 配置
set DB_NAME=panda
set DB_USER=root
set DB_HOST=localhost
set DB_PORT=3306

REM 脚本目录
set SCRIPT_DIR=%~dp0
set DB_DIR=%SCRIPT_DIR%..\app\db
set SCHEMA_FILE=%DB_DIR%\init_schema.sql
set DATA_FILE=%DB_DIR%\init_data.sql

echo ========================================
echo PANDA 数据库部署工具
echo ========================================
echo.

REM 检查MySQL是否安装
where mysql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到MySQL命令
    echo 请先安装MySQL客户端并添加到PATH
    exit /b 1
)

REM 检查SQL文件是否存在
if not exist "%SCHEMA_FILE%" (
    echo [错误] 未找到表结构文件: init_schema.sql
    exit /b 1
)
if not exist "%DATA_FILE%" (
    echo [错误] 未找到数据文件: init_data.sql
    exit /b 1
)

REM 提示输入密码
set /p DB_PASSWORD="请输入MySQL密码: "
echo.

REM 构建MySQL连接参数
set MYSQL_CMD=mysql -h%DB_HOST% -P%DB_PORT% -u%DB_USER% -p%DB_PASSWORD%

echo [1/4] 检查数据库连接...
%MYSQL_CMD% -e "SELECT 1" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 无法连接到MySQL服务器
    echo 请检查连接参数和密码
    exit /b 1
)
echo [成功] 数据库连接成功
echo.

echo [2/5] 创建数据库表结构...
%MYSQL_CMD% < "%SCHEMA_FILE%"
echo [成功] 表结构创建完成
echo.

echo [3/5] 导入模拟数据...
%MYSQL_CMD% < "%DATA_FILE%"
echo [成功] 数据导入完成
echo.

echo [4/5] 验证部署...
for /f %%i in ('%MYSQL_CMD% %DB_NAME% -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='%DB_NAME%';"') do set TABLE_COUNT=%%i
for /f %%i in ('%MYSQL_CMD% %DB_NAME% -N -e "SELECT COUNT(*) FROM users;"') do set USER_COUNT=%%i
for /f %%i in ('%MYSQL_CMD% %DB_NAME% -N -e "SELECT COUNT(*) FROM courses;"') do set COURSE_COUNT=%%i
for /f %%i in ('%MYSQL_CMD% %DB_NAME% -N -e "SELECT COUNT(*) FROM scenarios;"') do set SCENARIO_COUNT=%%i

echo [成功] 表数量: %TABLE_COUNT%
echo [成功] 用户数量: %USER_COUNT%
echo [成功] 课程数量: %COURSE_COUNT%
echo [成功] 场景数量: %SCENARIO_COUNT%
echo.

echo ========================================
echo 🎉 数据库部署成功！
echo ========================================
echo.
echo 默认账号信息：
echo 管理员: admin@panda.com / admin123
echo 讲师:   teacher@panda.com / admin123
echo 学员:   nurse1@hospital.com / admin123
echo.
echo 下一步：
echo 1. 配置后端 .env 文件
echo 2. 启动后端服务: python backend\start.py
echo 3. 启动前端服务: cd frontend ^&^& npm run dev
echo.

pause
