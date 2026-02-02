"""
数据库迁移执行脚本
执行顺序: 001 -> 002 -> 003
"""
import os
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

os.chdir(backend_dir)

from sqlalchemy import create_engine, text
from app.config.config import settings


def run_migrations():
    db_url = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset=utf8mb4"
    engine = create_engine(db_url)
    
    migrations_dir = Path(__file__).parent
    migration_files = [
        "001_create_admin_tables.sql",
        "002_alter_existing_tables.sql",
        "003_init_default_data.sql"
    ]
    
    with engine.connect() as conn:
        for migration_file in migration_files:
            file_path = migrations_dir / migration_file
            if not file_path.exists():
                print(f"⚠️  迁移文件不存在: {migration_file}")
                continue
            
            print(f"📝 执行迁移: {migration_file}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                sql = f.read()
            
            try:
                for statement in sql.split(';'):
                    statement = statement.strip()
                    if statement and not statement.startswith('--'):
                        conn.execute(text(statement))
                conn.commit()
                print(f"✅ {migration_file} 执行成功")
            except Exception as e:
                print(f"❌ {migration_file} 执行失败: {e}")
                conn.rollback()
                raise
    
    print("\n🎉 所有迁移执行完成!")


if __name__ == "__main__":
    run_migrations()
