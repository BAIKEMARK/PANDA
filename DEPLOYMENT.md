# PANDA 系统部署指南

## 概述
本文档提供PANDA围产期抑郁管理智能培训系统的完整部署指南，适用于在新环境中快速搭建系统。

## 系统要求

### 硬件要求
- CPU: 2核心及以上
- 内存: 4GB及以上
- 硬盘: 20GB可用空间

### 软件要求
- **操作系统**: Windows 10/11, Ubuntu 20.04+, macOS 10.15+
- **Python**: 3.9+
- **Node.js**: 16+
- **MySQL**: 8.0+
- **Redis**: 6.0+ (可选，用于缓存)

## 快速部署（推荐）

### 1. 克隆项目
```bash
git clone <repository-url>
cd PANDA
```

### 2. 部署数据库

#### Windows
```bash
cd backend\scripts
deploy_database.bat
```

#### Linux/macOS
```bash
cd backend/scripts
chmod +x deploy_database.sh
./deploy_database.sh
```

### 3. 配置后端

#### 创建虚拟环境
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置以下内容：
# DATABASE_URL=mysql+pymysql://root:password@localhost:3306/panda
# SECRET_KEY=your-secret-key-here
# OPENAI_API_KEY=your-openai-api-key
```

#### 启动后端服务
```bash
python start.py
```

后端服务将在 `http://localhost:8000` 启动

### 4. 配置前端

#### 安装依赖
```bash
cd frontend
npm install
```

#### 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置API地址：
# VITE_API_BASE_URL=http://localhost:8000
```

#### 启动前端服务
```bash
npm run dev
```

前端服务将在 `http://localhost:5173` 启动

## 手动部署

### 1. 数据库部署

#### 方式一：使用SQL文件
```bash
# 1. 创建数据库并导入表结构
mysql -u root -p < backend/app/db/init_schema.sql

# 2. 导入模拟数据
mysql -u root -p panda < backend/app/db/init_data.sql
```

### 2. 验证数据库
```bash
# 检查表数量
mysql -u root -p panda -e "SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema='panda';"

# 检查用户数据
mysql -u root -p panda -e "SELECT id, email, name, role FROM users;"

# 检查课程数据
mysql -u root -p panda -e "SELECT id, title, level FROM courses LIMIT 5;"
```

## 默认账号

### 管理员账号
- **邮箱**: admin@panda.com
- **密码**: admin123
- **权限**: 系统管理员，拥有所有权限

### 讲师账号
- **邮箱**: teacher@panda.com
- **密码**: admin123
- **权限**: 讲师，可查看课程和学员进度

### 学员账号
- **邮箱**: nurse1@hospital.com
- **密码**: admin123
- **权限**: 学员，可学习课程和进行情景模拟

## 生产环境配置

### 1. 数据库优化

#### MySQL配置 (my.cnf)
```ini
[mysqld]
# 字符集
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci

# 时区
default-time-zone='+00:00'

# 连接数
max_connections=200

# 缓冲池
innodb_buffer_pool_size=1G
innodb_log_file_size=256M

# 查询缓存
query_cache_type=1
query_cache_size=64M
```

### 2. 后端配置

#### 生产环境变量 (.env)
```bash
# 数据库
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/panda

# 安全
SECRET_KEY=<生成强密钥>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI服务
OPENAI_API_KEY=<your-api-key>
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4

# Redis (可选)
REDIS_URL=redis://localhost:6379/0

# 日志
LOG_LEVEL=INFO
LOG_FILE=/var/log/panda/app.log

# CORS
CORS_ORIGINS=https://yourdomain.com
```

#### 使用Gunicorn部署
```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

### 3. 前端配置

#### 生产构建
```bash
cd frontend
npm run build
```

#### 使用Nginx部署
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 故障排除

### 问题1: 数据库连接失败
```bash
# 检查MySQL服务状态
systemctl status mysql  # Linux
net start MySQL80       # Windows

# 检查端口是否开放
netstat -an | grep 3306

# 测试连接
mysql -h localhost -u root -p
```

### 问题2: 后端启动失败
```bash
# 检查Python版本
python --version

# 检查依赖
pip list

# 查看详细错误
python start.py --debug
```

### 问题3: 前端无法访问后端
```bash
# 检查CORS配置
# 确保后端 .env 中 CORS_ORIGINS 包含前端地址

# 检查网络
curl http://localhost:8000/health
```

### 问题4: 字符集问题
```sql
-- 修改数据库字符集
ALTER DATABASE panda CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 修改表字符集
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 性能优化

### 1. 数据库索引
所有常用查询字段已添加索引，详见 `backend/app/db/migrations/20260207_optimize_indexes.sql`

### 2. 缓存策略
- 使用Redis缓存用户会话
- 缓存课程和场景数据
- 实现查询结果缓存

### 3. 前端优化
- 代码分割和懒加载
- 图片压缩和CDN
- 启用Gzip压缩

## 监控和日志

### 1. 应用日志
```bash
# 查看后端日志
tail -f /var/log/panda/app.log

# 查看Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 2. 数据库监控
```sql
-- 查看慢查询
SHOW VARIABLES LIKE 'slow_query_log';
SHOW VARIABLES LIKE 'long_query_time';

-- 查看连接数
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';
```

## 备份和恢复

### 数据库备份
```bash
# 完整备份
mysqldump -u root -p panda > backup_$(date +%Y%m%d).sql

# 仅备份结构
mysqldump -u root -p --no-data panda > schema_backup.sql

# 仅备份数据
mysqldump -u root -p --no-create-info panda > data_backup.sql
```

### 数据库恢复
```bash
# 恢复数据库
mysql -u root -p panda < backup_20260207.sql
```

## 安全建议

1. **修改默认密码**: 首次登录后立即修改所有默认账号密码
2. **使用HTTPS**: 生产环境必须启用SSL/TLS
3. **定期备份**: 建立自动备份机制
4. **更新依赖**: 定期更新系统依赖包
5. **访问控制**: 配置防火墙规则，限制数据库访问
6. **日志审计**: 启用审计日志，记录关键操作

## 技术支持

如遇到问题，请查看：
1. 项目文档: `docs/` 目录
2. API文档: `http://localhost:8000/docs`

## 数据库文件说明

项目提供两个SQL文件用于数据库初始化：

1. **init_schema.sql** - 数据库表结构（25张表）
   - 核心业务表：users, courses, scenarios, chat_sessions, chat_messages, evaluation_reports等
   - 管理后台表：organizations, roles, permissions, menus, training_classes等
   
2. **init_data.sql** - 初始化模拟数据
   - 5个测试用户（admin, teacher, 3个students）
   - 10个THP分层课程（L1-L4）
   - 5个虚拟患者场景（难度1-5）
   - 12个菜单项及权限配置

## 更新日志

- 2026-02-07: 初始版本
  - 完整的数据库结构
  - 前后端分离架构
  - 管理后台功能
  - 异步评估报告生成
  - 数据库索引优化
