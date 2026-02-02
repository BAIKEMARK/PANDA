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
        "01_create_tables.sql",
        "02_init_data.sql"
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
                statements = []
                current_statement = ""
                for line in sql.split('\n'):
                    line = line.strip()
                    # 跳过注释行
                    if line.startswith('--') or not line:
                        continue
                    current_statement += line + " "
                    # 如果行以分号结尾，说明是一个完整的语句
                    if line.endswith(';'):
                        statements.append(current_statement.strip())
                        current_statement = ""
                
                # 处理最后一个语句（可能没有分号）
                if current_statement.strip():
                    statements.append(current_statement.strip())
                
                for statement in statements:
                    if not statement:
                        continue
                    try:
                        conn.execute(text(statement))
                    except Exception as e:
                        # 忽略列已存在、索引已存在、表已存在的错误
                        error_msg = str(e).lower()
                        error_code = getattr(e, 'orig', None)
                        error_code_str = str(error_code) if error_code else ''
                        
                        # 需要忽略的错误类型
                        ignorable_errors = [
                            'duplicate column', 'already exists', 
                            'duplicate key', 'duplicate entry',
                            "doesn't exist",  # 表不存在（基础表可能还未创建）
                            'failed to open the referenced table',  # 外键引用的表不存在
                            'table', 'does not exist'
                        ]
                        
                        if any(keyword in error_msg for keyword in ignorable_errors):
                            print(f"  [跳过] {error_msg[:100]}...")
                        else:
                            print(f"  [错误] {error_msg}")
                            raise
                
                conn.commit()
                print(f"✅ {migration_file} 执行成功")
            except Exception as e:
                print(f"❌ {migration_file} 执行失败: {e}")
                conn.rollback()
                raise
    
    print("\n🎉 所有迁移执行完成!")


if __name__ == "__main__":
    run_migrations()
