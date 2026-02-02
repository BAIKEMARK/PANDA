# 数据库迁移说明

## 迁移文件

1. `01_create_tables.sql` - 建表脚本（新建表 + 扩展现有表）
2. `02_init_data.sql` - 初始化数据（机构、角色、权限、角色权限关联）

## 前置条件

**重要**：执行迁移前，需要先创建基础表（users, courses, scenarios, certificates等）。

如果还没有基础表，请先执行：
```bash
mysql -u用户名 -p数据库名 < backend/app/db/panda.sql
```

或者使用ORM自动创建：
```bash
cd backend
python -m app.db.init_db
```

## 执行方式

### 方式1: 使用Python脚本（推荐）
```bash
cd backend
python -m app.db.migrations.run_migrations
```

脚本会自动忽略以下错误：
- 表已存在
- 列已存在
- 索引已存在
- 外键引用的表不存在（基础表未创建时会跳过）

### 方式2: 手动执行SQL
按顺序执行SQL文件:
```bash
mysql -u用户名 -p数据库名 < backend/app/db/migrations/01_create_tables.sql
mysql -u用户名 -p数据库名 < backend/app/db/migrations/02_init_data.sql
```

## 注意事项

- 执行前请备份数据库
- 确保数据库用户有CREATE、ALTER权限
- 如果基础表（users, courses等）不存在，外键约束会失败，这是正常的，迁移脚本会自动跳过
- 基础表创建后，可以手动添加外键约束（SQL文件中已注释）
