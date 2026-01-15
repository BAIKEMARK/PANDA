#!/bin/bash
# ================================================
# PANDA - 围产期抑郁管理智能培训系统
# 项目初始化脚本 (Linux/Mac)
# ================================================

set -e

echo ""
echo "==============================================="
echo "PANDA 项目初始化"
echo "==============================================="
echo ""

# 检查 Python
echo "[1/5] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 未安装"
    echo "请安装 Python 3.12.12: https://www.python.org/downloads/"
    exit 1
fi
python3 --version
echo "✅ Python 环境正常"
echo ""

# 检查 Node.js
echo "[2/5] 检查 Node.js 环境..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    echo "请安装 Node.js v20.15.1: https://nodejs.org/"
    exit 1
fi
node --version
echo "✅ Node.js 环境正常"
echo ""

# 检查 MySQL
echo "[3/5] 检查 MySQL 环境..."
if ! command -v mysql &> /dev/null; then
    echo "⚠️  MySQL 未安装或未添加到 PATH"
    echo "请安装 MySQL 8.0.43+: https://dev.mysql.com/downloads/mysql/"
    echo ""
    read -p "是否继续初始化? (y/n): " continue
    if [ "$continue" != "y" ]; then
        exit 1
    fi
else
    mysql --version
    echo "✅ MySQL 环境正常"
    echo ""
fi

# 安装后端依赖
echo "[4/5] 安装 Python 后端依赖..."
cd app
if [ ! -f ".env" ]; then
    echo "创建 .env 配置文件..."
    cp .env.example .env
    echo "⚠️  请编辑 app/.env 文件，配置数据库密码和AI密钥"
fi
pip3 install -r requirements.txt
echo "✅ Python 依赖安装完成"
echo ""

# 安装前端依赖
echo "[5/5] 安装 Node.js 前端依赖..."
cd ../frontend
if [ ! -f ".env.local" ]; then
    echo "创建 .env.local 配置文件..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
fi
npm install
echo "✅ Node.js 依赖安装完成"
echo ""

cd ..

echo ""
echo "==============================================="
echo "✅ 项目初始化完成！"
echo "==============================================="
echo ""
echo "下一步操作："
echo ""
echo "1. 配置数据库："
echo "   mysql -u root -p < app/database/schema.sql"
echo ""
echo "2. 配置环境变量："
echo "   编辑 app/.env 文件，设置："
echo "   - DB_PASSWORD (MySQL密码)"
echo "   - AI_TEXT_KEY (阿里百炼API密钥)"
echo ""
echo "3. 启动后端服务："
echo "   cd app && python3 main.py"
echo ""
echo "4. 启动前端服务（新终端）："
echo "   cd frontend && npm run dev"
echo ""
echo "5. 访问应用："
echo "   前端: http://localhost:3000"
echo "   API文档: http://localhost:8000/api/docs"
echo ""
echo "==============================================="
