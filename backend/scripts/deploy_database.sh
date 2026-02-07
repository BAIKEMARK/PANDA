#!/bin/bash
# PANDA 数据库快速部署脚本
# 用途：在新环境中一键部署数据库

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
DB_NAME="panda"
DB_USER="${DB_USER:-root}"
DB_PASSWORD="${DB_PASSWORD}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-3306}"

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_DIR="$SCRIPT_DIR/../app/db"
SCHEMA_FILE="$DB_DIR/init_schema.sql"
DATA_FILE="$DB_DIR/init_data.sql"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}PANDA 数据库部署工具${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查MySQL是否安装
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}错误: 未找到MySQL命令${NC}"
    echo "请先安装MySQL客户端"
    exit 1
fi

# 检查SQL文件是否存在
if [ ! -f "$SCHEMA_FILE" ]; then
    echo -e "${RED}错误: 未找到表结构文件: init_schema.sql${NC}"
    exit 1
fi
if [ ! -f "$DATA_FILE" ]; then
    echo -e "${RED}错误: 未找到数据文件: init_data.sql${NC}"
    exit 1
fi

# 提示输入密码（如果未设置）
if [ -z "$DB_PASSWORD" ]; then
    echo -e "${YELLOW}请输入MySQL密码:${NC}"
    read -s DB_PASSWORD
    echo ""
fi

# 构建MySQL连接参数
MYSQL_CMD="mysql -h$DB_HOST -P$DB_PORT -u$DB_USER -p$DB_PASSWORD"

echo -e "${GREEN}[1/4] 检查数据库连接...${NC}"
if ! $MYSQL_CMD -e "SELECT 1" &> /dev/null; then
    echo -e "${RED}错误: 无法连接到MySQL服务器${NC}"
    echo "请检查连接参数和密码"
    exit 1
fi
echo -e "${GREEN}✓ 数据库连接成功${NC}"
echo ""

echo -e "${GREEN}[2/5] 创建数据库表结构...${NC}"
$MYSQL_CMD < "$SCHEMA_FILE"
echo -e "${GREEN}✓ 表结构创建完成${NC}"
echo ""

echo -e "${GREEN}[3/5] 导入模拟数据...${NC}"
$MYSQL_CMD < "$DATA_FILE"
echo -e "${GREEN}✓ 数据导入完成${NC}"
echo ""

echo -e "${GREEN}[4/5] 验证部署...${NC}"
TABLE_COUNT=$($MYSQL_CMD $DB_NAME -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB_NAME';")
USER_COUNT=$($MYSQL_CMD $DB_NAME -N -e "SELECT COUNT(*) FROM users;")
COURSE_COUNT=$($MYSQL_CMD $DB_NAME -N -e "SELECT COUNT(*) FROM courses;")
SCENARIO_COUNT=$($MYSQL_CMD $DB_NAME -N -e "SELECT COUNT(*) FROM scenarios;")

echo -e "${GREEN}✓ 表数量: $TABLE_COUNT${NC}"
echo -e "${GREEN}✓ 用户数量: $USER_COUNT${NC}"
echo -e "${GREEN}✓ 课程数量: $COURSE_COUNT${NC}"
echo -e "${GREEN}✓ 场景数量: $SCENARIO_COUNT${NC}"
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 数据库部署成功！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}默认账号信息：${NC}"
echo -e "管理员: ${GREEN}admin@panda.com${NC} / ${GREEN}admin123${NC}"
echo -e "讲师:   ${GREEN}teacher@panda.com${NC} / ${GREEN}admin123${NC}"
echo -e "学员:   ${GREEN}nurse1@hospital.com${NC} / ${GREEN}admin123${NC}"
echo ""
echo -e "${YELLOW}下一步：${NC}"
echo "1. 配置后端 .env 文件"
echo "2. 启动后端服务: python backend/start.py"
echo "3. 启动前端服务: cd frontend && npm run dev"
echo ""
