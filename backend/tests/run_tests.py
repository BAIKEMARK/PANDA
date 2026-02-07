"""
测试运行脚本
快速运行API集成测试
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_api_integration import APITester


def main():
    """运行测试"""
    print("\n" + "="*70)
    print("PANDA 后端API集成测试")
    print("="*70)
    print("\n⚠️  请确保:")
    print("  1. 后端服务已启动 (http://localhost:8000)")
    print("  2. 数据库已初始化")
    print("  3. Redis服务已启动")
    print("\n按 Enter 继续，Ctrl+C 取消...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n\n❌ 测试已取消")
        return
    
    # 运行测试
    tester = APITester()
    try:
        tester.run_all_tests()
        print("\n🎉 测试完成！所有接口工作正常。")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
