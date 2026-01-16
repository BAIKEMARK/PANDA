"""
Database Initialization Script
数据库初始化脚本 - 根据ORM模型创建所有表
"""
from backend.app.db.database import engine, Base

# 导入所有模型以确保它们被注册到 Base.metadata
from backend.app.models import (
    User,
    Course,
    UserProgress,
    Scenario,
    ChatSession,
    ChatMessage,
    EvaluationReport,
)


def create_all_tables():
    """创建所有数据库表"""
    print("🔄 开始创建数据库表...")
    
    # 打印将要创建的表
    print("\n📋 将要创建的表:")
    for table_name in Base.metadata.tables.keys():
        print(f"   - {table_name}")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    print("\n✅ 数据库表创建完成!")
    return True


def drop_all_tables():
    """删除所有数据库表 (谨慎使用!)"""
    print("⚠️  警告: 即将删除所有数据库表!")
    confirm = input("确认删除? (输入 'yes' 确认): ")
    if confirm.lower() == 'yes':
        Base.metadata.drop_all(bind=engine)
        print("✅ 所有表已删除")
        return True
    else:
        print("❌ 操作已取消")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_all_tables()
    else:
        create_all_tables()
