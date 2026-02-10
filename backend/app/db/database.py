"""
Database Session Module
数据库会话管理
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

from backend.app.core.config.settings import settings

# 创建ORM基类
Base = declarative_base()

# 同步引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,                    # 连接前检查连接是否有效
    pool_recycle=settings.DB_POOL_RECYCLE, # 连接回收时间（秒）
    pool_size=settings.DB_POOL_SIZE,       # 连接池大小
    max_overflow=settings.DB_MAX_OVERFLOW, # 最大溢出连接数
    pool_timeout=settings.DB_POOL_TIMEOUT, # 获取连接超时时间（秒）
    echo=False,                            # 关闭 SQL 日志，避免干扰调试输出
)

# 同步会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    获取数据库会话的依赖注入函数

    Yields:
        Session: SQLAlchemy会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """初始化数据库连接测试"""
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[OK] 数据库连接成功！")
        return True
    except Exception as e:
        print(f"[ERROR] 数据库连接失败: {e}")
        return False
