#!/bin/bash
# PANDA 系统快速启动脚本 (Linux/macOS)
# 用途：一键启动前后端服务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}PANDA 系统快速启动${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到Python${NC}"
    echo "请先安装Python 3.9+"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}错误: 未找到Node.js${NC}"
    echo "请先安装Node.js 16+"
    exit 1
fi

# 检查MySQL
if ! command -v mysql &> /dev/null; then
    echo -e "${YELLOW}警告: 未找到MySQL命令${NC}"
    echo "请确保MySQL服务已启动"
fi

echo -e "${BLUE}[1/5] 检查数据库...${NC}"
echo -e "${YELLOW}请输入MySQL密码:${NC}"
read -s DB_PASSWORD
echo ""

if ! mysql -u root -p"$DB_PASSWORD" -e "USE panda;" &> /dev/null; then
    echo -e "${YELLOW}警告: 数据库不存在，是否现在部署？(y/n)${NC}"
    read -r DEPLOY_DB
    if [ "$DEPLOY_DB" = "y" ] || [ "$DEPLOY_DB" = "Y" ]; then
        export DB_PASSWORD
        bash backend/scripts/deploy_database.sh
    else
        echo "请先部署数据库"
        exit 1
    fi
fi
echo -e "${GREEN}✓ 数据库检查通过${NC}"
echo ""

echo -e "${BLUE}[2/5] 检查后端依赖...${NC}"
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}提示: 创建Python虚拟环境...${NC}"
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi
echo -e "${GREEN}✓ 后端依赖检查通过${NC}"
echo ""

echo -e "${BLUE}[3/5] 检查前端依赖...${NC}"
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}提示: 安装前端依赖...${NC}"
    cd frontend
    npm install
    cd ..
fi
echo -e "${GREEN}✓ 前端依赖检查通过${NC}"
echo ""

echo -e "${BLUE}[4/5] 启动后端服务...${NC}"
cd backend
source venv/bin/activate
nohup python start.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd ..
sleep 3
echo -e "${GREEN}✓ 后端服务已启动: http://localhost:8000 (PID: $BACKEND_PID)${NC}"
echo ""

echo -e "${BLUE}[5/5] 启动前端服务...${NC}"
cd frontend
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..
sleep 3
echo -e "${GREEN}✓ 前端服务已启动: http://localhost:5173 (PID: $FRONTEND_PID)${NC}"
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 PANDA系统启动成功！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}服务地址：${NC}"
echo -e "前端: ${BLUE}http://localhost:5173${NC}"
echo -e "后端: ${BLUE}http://localhost:8000${NC}"
echo -e "API文档: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}默认账号：${NC}"
echo -e "管理员: ${GREEN}admin@panda.com${NC} / ${GREEN}admin123${NC}"
echo -e "讲师:   ${GREEN}teacher@panda.com${NC} / ${GREEN}admin123${NC}"
echo -e "学员:   ${GREEN}nurse1@hospital.com${NC} / ${GREEN}admin123${NC}"
echo ""
echo -e "${YELLOW}日志文件：${NC}"
echo -e "后端: logs/backend.log"
echo -e "前端: logs/frontend.log"
echo ""
echo -e "${YELLOW}停止服务：${NC}"
echo -e "bash stop_services.sh"
echo ""

# 在macOS上自动打开浏览器
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:5173
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost:5173 2>/dev/null || true
fi
