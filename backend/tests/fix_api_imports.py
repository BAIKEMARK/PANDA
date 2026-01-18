"""
修复 api 目录下的所有导入，改为使用 from app.xxx
"""
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """修复单个文件的导入"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 只处理 api 目录的文件
    if 'app\\api\\' not in str(file_path) and 'app/api/' not in str(file_path):
        return False

    # 修复导入：from xxx -> from app.xxx
    patterns = [
        (r'^from db\.database', 'from app.db.database'),
        (r'^from models\.', 'from app.models.'),
        (r'^from schemas\.', 'from app.schemas.'),
        (r'^from crud\.', 'from app.crud.'),
        (r'^from services\.', 'from app.services.'),
        (r'^from common\.', 'from app.common.'),
        (r'^from core\.', 'from app.core.'),
        (r'^import crud\.', 'import app.crud.'),
        (r'^import models\.', 'import app.models.'),
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