# 数据库迁移说明

## 迁移文件

1. `001_create_admin_tables.sql` - 创建后台管理基础表
2. `002_alter_existing_tables.sql` - 扩展现有表结构
3. `003_init_default_data.sql` - 初始化默认数据

## 执行方式

### 方式1: 使用Python脚本
```bash
cd backend
python -m app.db.migrations.run_migrations
```

### 方式2: 手动执行SQL
按顺序执行SQL文件:
```bash
mysql -u用户名 -p数据库名 < 001_create_admin_tables.sql
mysql -u用户名 -p数据库名 < 002_alter_existing_tables.sql
mysql -u用户名 -p数据库名 < 003_init_default_data.sql
```

## 注意事项

- 执行前请备份数据库
- 确保数据库用户有CREATE、ALTER权限
- 如果表已存在，部分ALTER语句可能失败，可手动调整
