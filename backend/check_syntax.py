"""
检查Python语法错误
"""
import py_compile
import sys
import os

files_to_check = [
    "app/modules/admin/api/organization.py",
    "app/modules/admin/api/role.py",
    "app/modules/admin/api/user.py",
    "app/modules/admin/api/training.py",
    "app/modules/admin/services/organization_service.py",
    "app/modules/admin/services/role_service.py",
    "app/modules/admin/services/permission_service.py",
    "app/modules/admin/services/audit_service.py",
    "app/modules/admin/services/user_admin_service.py",
    "app/modules/admin/services/training_service.py",
    "app/common/middleware/permission.py",
    "app/models/organization.py",
    "app/models/training.py",
    "app/models/question.py",
    "app/models/audit.py",
]

errors = []
for file_path in files_to_check:
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    if os.path.exists(full_path):
        try:
            py_compile.compile(full_path, doraise=True)
            print(f"OK: {file_path}")
        except py_compile.PyCompileError as e:
            errors.append((file_path, str(e)))
            print(f"ERROR: {file_path}")
            print(f"  {e}")
    else:
        print(f"NOT FOUND: {file_path}")

if errors:
    print(f"\nFound {len(errors)} syntax errors")
    sys.exit(1)
else:
    print("\nAll files compiled successfully!")
