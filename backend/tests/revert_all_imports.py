"""
将所有 app/ 目录下的文件改回使用 from core 而不是 from app.core
"""
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """修复单个文件的导入"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 恢复所有导入：from app.xxx -> from xxx
    patterns = [
        (r'^from app\.core\.config', 'from core.config'),
        (r'^from app\.core\.proxy', 'from core.proxy'),
        (r'^from app\.core\.security', 'from core.security'),
        (r'^from app\.db\.database', 'from db.database'),
        (r'^from app\.models\.', 'from models.'),
        (r'^from app\.schemas\.', 'from schemas.'),
        (r'^from app\.crud\.', 'from crud.'),
        (r'^from app\.services\.', 'from services.'),
        (r'^from app\.common\.', 'from common.'),
        (r'^from app\.api\.', 'from api.'),
        (r'^from app\.utils\.', 'from utils.'),
        (r'^import app\.crud\.', 'import crud.'),
        (r'^import app\.models\.', 'import models.'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(f'^{pattern}', replacement, content, flags=re.MULTILINE)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def fix_all_imports():
    """修复所有 Python 文件"""
    app_dir = Path(__file__).parent.parent / "app"
    fixed_files = []

    for py_file in app_dir.rglob("*.py"):
        if fix_imports_in_file(py_file):
            fixed_files.append(str(py_file.relative_to(app_dir.parent)))
            print(f"✅ 修复: {py_file.relative_to(app_dir.parent)}")

    if fixed_files:
        print(f"\n共修复 {len(fixed_files)} 个文件")
    else:
        print("\n没有需要修复的文件")

if __name__ == "__main__":
    fix_all_imports()