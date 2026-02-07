"""
初始化测试数据
创建基础的场景、课程等测试数据
"""
import sys
import os
import uuid

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from backend.app.db.database import SessionLocal, init_database
from backend.app.models import Scenario, Course, User
from backend.app.core.config.security import get_password_hash


def create_test_scenarios(db: Session):
    """创建测试场景"""
    print("\n📝 创建测试场景...")
    
    # 检查是否已存在场景
    existing = db.query(Scenario).first()
    if existing:
        print("✅ 场景已存在，跳过创建")
        return
    
    scenarios = [
        {
            "id": str(uuid.uuid4()),
            "title": "产后抑郁初诊场景",
            "description": "一位产后3个月的新妈妈，出现情绪低落、失眠等症状",
            "difficulty": "easy",
            "time_period": "产后3个月",
            "patient_background": "患者李女士，28岁，产后3个月，出现情绪低落、失眠、食欲不振等症状。",
            "system_prompt": "你是一位产后抑郁的患者，需要根据护士的沟通表现出相应的情绪反应。",
            "status": "active"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "孕期焦虑场景",
            "description": "一位孕28周的孕妇，对分娩和育儿感到焦虑",
            "difficulty": "medium",
            "time_period": "孕28周",
            "patient_background": "患者王女士，32岁，孕28周，对即将到来的分娩和育儿感到焦虑。",
            "system_prompt": "你是一位孕期焦虑的患者，表现出对未来的担忧和不安。",
            "status": "active"
        }
    ]
    
    for scenario_data in scenarios:
        scenario = Scenario(**scenario_data)
        db.add(scenario)
    
    db.commit()
    print(f"✅ 创建了 {len(scenarios)} 个测试场景")


def create_test_courses(db: Session):
    """创建测试课程"""
    print("\n📚 创建测试课程...")
    
    # 检查是否已存在课程
    existing = db.query(Course).first()
    if existing:
        print("✅ 课程已存在，跳过创建")
        return
    
    courses = [
        {
            "id": str(uuid.uuid4()),
            "title": "围产期抑郁识别与管理",
            "description": "学习如何识别和管理围产期抑郁症状",
            "content_url": "https://example.com/course1",
            "level": "beginner",
            "status": "published",
            "version": "1.0"
        },
        {
            "id": str(uuid.uuid4()),
            "title": "THP沟通技巧培训",
            "description": "掌握THP标准的沟通技巧和评估方法",
            "content_url": "https://example.com/course2",
            "level": "intermediate",
            "status": "published",
            "version": "1.0"
        }
    ]
    
    for course_data in courses:
        course = Course(**course_data)
        db.add(course)
    
    db.commit()
    print(f"✅ 创建了 {len(courses)} 个测试课程")


def create_admin_user(db: Session):
    """创建管理员用户"""
    print("\n👤 创建管理员用户...")
    
    # 检查是否已存在管理员
    existing = db.query(User).filter(User.email == "admin@panda.com").first()
    if existing:
        print("✅ 管理员已存在，跳过创建")
        return
    
    admin = User(
        id=str(uuid.uuid4()),
        email="admin@panda.com",
        name="系统管理员",
        password_hash=get_password_hash("Admin123456"),
        role="admin"
    )
    
    db.add(admin)
    db.commit()
    print("✅ 创建管理员成功")
    print("   邮箱: admin@panda.com")
    print("   密码: Admin123456")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("PANDA 测试数据初始化")
    print("="*70)
    
    # 测试数据库连接
    if not init_database():
        print("\n❌ 数据库连接失败，请检查配置")
        return
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建测试数据
        create_test_scenarios(db)
        create_test_courses(db)
        create_admin_user(db)
        
        print("\n" + "="*70)
        print("✅ 测试数据初始化完成！")
        print("="*70)
        print("\n可以开始运行测试了:")
        print("  cd backend/tests")
        print("  python run_tests.py")
        print()
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
