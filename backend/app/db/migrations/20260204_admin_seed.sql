-- 管理后台初始化数据（不影响 panda.sql）
-- 用途：机构/角色/权限/用户/菜单/班级数据
-- 执行方式: mysql -u用户名 -p数据库名 < 20260204_admin_seed.sql

SET NAMES utf8mb4;

-- ============================================
-- 1) 机构
-- ============================================
INSERT INTO `organizations` (`id`, `name`, `short_name`, `contact_name`, `contact_phone`, `contact_email`, `status`, `config`) VALUES
('org-platform-001', '平台机构', '平台', '平台管理员', '400-000-0000', 'platform@panda.com', 'active', '{"certificate": true, "export": true, "voice": true, "anti_cheat": true}'),
('org-hospital-001', '第一人民医院', '一院', '张主任', '010-12345678', 'zhang@hospital1.com', 'active', '{"certificate": true, "export": true, "voice": true, "anti_cheat": false}'),
('org-hospital-002', '第二人民医院', '二院', '李主任', '010-87654321', 'li@hospital2.com', 'active', '{"certificate": true, "export": false, "voice": false, "anti_cheat": true}'),
('org-hospital-003', '妇幼保健院', '妇幼', '王主任', '010-11223344', 'wang@mch.com', 'active', '{"certificate": true, "export": true, "voice": true, "anti_cheat": true}')
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`);

-- ============================================
-- 2) 角色
-- ============================================
INSERT INTO `roles` (`id`, `code`, `name`, `description`, `scope`) VALUES
('role-super-admin', 'super_admin', '平台超级管理员', '管理所有机构、系统级配置、全局模板与字典项', 'system'),
('role-org-admin', 'org_admin', '机构管理员', '管理本机构用户、班级、证书、数据导出、机构配置', 'org'),
('role-content-editor', 'content_editor', '内容编辑', '维护课程/题库/场景脚本/评分规则（只在授权范围内）', 'org'),
('role-trainer', 'trainer', '培训导师/带教', '建班、分配任务、查看学习与考核结果、点评', 'org'),
('role-auditor', 'auditor', '审计/质控', '只读查看日志、版本变更、评分命中与复盘报告', 'org')
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`);

-- ============================================
-- 3) 权限
-- ============================================
INSERT INTO `permissions` (`id`, `code`, `name`, `module`, `action`, `description`) VALUES
('perm-org-view', 'org:view', '查看机构', 'org', 'view', '查看机构信息'),
('perm-org-create', 'org:create', '创建机构', 'org', 'create', '创建新机构'),
('perm-org-edit', 'org:edit', '编辑机构', 'org', 'edit', '编辑机构信息'),
('perm-org-delete', 'org:delete', '删除机构', 'org', 'delete', '删除机构'),
('perm-user-view', 'user:view', '查看用户', 'user', 'view', '查看用户列表和信息'),
('perm-user-create', 'user:create', '创建用户', 'user', 'create', '创建新用户'),
('perm-user-edit', 'user:edit', '编辑用户', 'user', 'edit', '编辑用户信息'),
('perm-user-delete', 'user:delete', '删除用户', 'user', 'delete', '删除用户'),
('perm-user-export', 'user:export', '导出用户', 'user', 'export', '导出用户数据'),
('perm-class-view', 'class:view', '查看班级', 'class', 'view', '查看班级列表和信息'),
('perm-class-create', 'class:create', '创建班级', 'class', 'create', '创建新班级'),
('perm-class-edit', 'class:edit', '编辑班级', 'class', 'edit', '编辑班级信息'),
('perm-class-publish', 'class:publish', '发布班级', 'class', 'publish', '发布班级'),
('perm-class-export', 'class:export', '导出班级', 'class', 'export', '导出班级数据'),
('perm-course-view', 'course:view', '查看课程', 'course', 'view', '查看课程列表和详情'),
('perm-course-create', 'course:create', '创建课程', 'course', 'create', '创建新课程'),
('perm-course-edit', 'course:edit', '编辑课程', 'course', 'edit', '编辑课程内容'),
('perm-course-publish', 'course:publish', '发布课程', 'course', 'publish', '发布课程'),
('perm-course-archive', 'course:archive', '下线课程', 'course', 'archive', '下线课程'),
('perm-course-export', 'course:export', '导出课程', 'course', 'export', '导出课程数据'),
('perm-question-view', 'question:view', '查看题目', 'question', 'view', '查看题目列表'),
('perm-question-create', 'question:create', '创建题目', 'question', 'create', '创建新题目'),
('perm-question-edit', 'question:edit', '编辑题目', 'question', 'edit', '编辑题目'),
('perm-question-delete', 'question:delete', '删除题目', 'question', 'delete', '删除题目'),
('perm-question-import', 'question:import', '导入题目', 'question', 'import', '批量导入题目'),
('perm-scenario-view', 'scenario:view', '查看场景', 'scenario', 'view', '查看场景列表'),
('perm-scenario-create', 'scenario:create', '创建场景', 'scenario', 'create', '创建新场景'),
('perm-scenario-edit', 'scenario:edit', '编辑场景', 'scenario', 'edit', '编辑场景'),
('perm-scenario-publish', 'scenario:publish', '发布场景', 'scenario', 'publish', '发布场景'),
('perm-scenario-archive', 'scenario:archive', '下线场景', 'scenario', 'archive', '下线场景'),
('perm-evaluation-view', 'evaluation:view', '查看评估', 'evaluation', 'view', '查看评估报告'),
('perm-evaluation-export', 'evaluation:export', '导出评估', 'evaluation', 'export', '导出评估数据'),
('perm-certificate-view', 'certificate:view', '查看证书', 'certificate', 'view', '查看证书列表'),
('perm-certificate-issue', 'certificate:issue', '发放证书', 'certificate', 'issue', '发放证书'),
('perm-certificate-revoke', 'certificate:revoke', '撤销证书', 'certificate', 'revoke', '撤销证书'),
('perm-audit-view', 'audit:view', '查看审计日志', 'audit', 'view', '查看审计日志'),
('perm-audit-export', 'audit:export', '导出审计日志', 'audit', 'export', '导出审计日志')
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`);

-- ============================================
-- 4) 角色权限分配
-- ============================================
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT r.id, p.id
FROM `roles` r
JOIN `permissions` p ON 1=1
WHERE r.code = 'super_admin'
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT r.id, p.id
FROM `roles` r
JOIN `permissions` p ON p.code IN (
  'org:view', 'org:edit',
  'user:view', 'user:create', 'user:edit', 'user:delete', 'user:export',
  'class:view', 'class:create', 'class:edit', 'class:publish', 'class:export',
  'course:view', 'course:create', 'course:edit', 'course:publish', 'course:archive', 'course:export',
  'question:view', 'question:create', 'question:edit', 'question:delete', 'question:import',
  'scenario:view', 'scenario:create', 'scenario:edit', 'scenario:publish', 'scenario:archive',
  'evaluation:view', 'evaluation:export',
  'certificate:view', 'certificate:issue', 'certificate:revoke',
  'audit:view', 'audit:export'
)
WHERE r.code = 'org_admin'
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT r.id, p.id
FROM `roles` r
JOIN `permissions` p ON p.code IN (
  'course:view', 'course:create', 'course:edit',
  'question:view', 'question:create', 'question:edit',
  'scenario:view', 'scenario:create', 'scenario:edit'
)
WHERE r.code = 'content_editor'
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT r.id, p.id
FROM `roles` r
JOIN `permissions` p ON p.code IN (
  'class:view', 'class:create', 'class:edit', 'class:publish',
  'user:view',
  'evaluation:view',
  'certificate:view', 'certificate:issue'
)
WHERE r.code = 'trainer'
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT r.id, p.id
FROM `roles` r
JOIN `permissions` p ON p.code IN (
  'audit:view', 'audit:export',
  'evaluation:view'
)
WHERE r.code = 'auditor'
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

-- ============================================
-- 5) 用户
-- ============================================
INSERT INTO `users` (`id`, `email`, `password_hash`, `name`, `role`, `org_id`, `phone`, `department`, `title`, `employee_id`) VALUES
('u-super-admin', 'superadmin@panda.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '超级管理员', 'admin', 'org-platform-001', '13800000001', '平台管理部', '系统管理员', 'EMP001'),
('u-admin-001', 'admin@panda.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '系统管理员', 'admin', 'org-platform-001', '13800000002', '系统管理部', '管理员', 'EMP002'),
('u-org-admin-001', 'orgadmin1@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '张主任', 'admin', 'org-hospital-001', '13800001001', '护理部', '主任', 'H001-001'),
('u-org-admin-002', 'orgadmin2@hospital2.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '李主任', 'admin', 'org-hospital-002', '13800002001', '护理部', '主任', 'H002-001'),
('u-trainer-001', 'trainer1@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '王老师', 'instructor', 'org-hospital-001', '13800001010', '护理部', '培训师', 'H001-010'),
('u-trainer-002', 'trainer2@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '李讲师', 'instructor', 'org-hospital-001', '13800001011', '护理部', '讲师', 'H001-011'),
('u-trainer-003', 'trainer3@hospital2.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '刘老师', 'instructor', 'org-hospital-002', '13800002010', '护理部', '培训师', 'H002-010'),
('u-student-001', 'nurse1@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '张护士', 'student', 'org-hospital-001', '13800001101', '产科', '护士', 'H001-101'),
('u-student-002', 'nurse2@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '刘护士', 'student', 'org-hospital-001', '13800001102', '产科', '护士', 'H001-102'),
('u-student-003', 'nurse3@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '陈护士', 'student', 'org-hospital-001', '13800001103', '产科', '护士', 'H001-103'),
('u-student-004', 'nurse4@hospital2.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '赵护士', 'student', 'org-hospital-002', '13800002101', '产科', '护士', 'H002-101'),
('u-student-005', 'nurse5@hospital2.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '钱护士', 'student', 'org-hospital-002', '13800002102', '产科', '护士', 'H002-102'),
('u-student-006', 'nurse6@mch.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '孙护士', 'student', 'org-hospital-003', '13800003101', '产科', '护士', 'MCH-101'),
('u-student-007', 'nurse7@mch.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '周护士', 'student', 'org-hospital-003', '13800003102', '产科', '护士', 'MCH-102'),
('u-content-editor-001', 'editor1@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '编辑员1', 'instructor', 'org-hospital-001', '13800001020', '护理部', '内容编辑', 'H001-020')
ON DUPLICATE KEY UPDATE 
  `org_id`=VALUES(`org_id`),
  `phone`=VALUES(`phone`),
  `department`=VALUES(`department`),
  `title`=VALUES(`title`),
  `employee_id`=VALUES(`employee_id`);

-- ============================================
-- 6) 用户机构关联
-- ============================================
INSERT INTO `user_organizations` (`user_id`, `org_id`, `role_id`, `status`)
SELECT 'u-super-admin', 'org-platform-001', r.id, 'active' FROM `roles` r WHERE r.code='super_admin'
UNION ALL SELECT 'u-admin-001', 'org-platform-001', r.id, 'active' FROM `roles` r WHERE r.code='super_admin'
UNION ALL SELECT 'u-org-admin-001', 'org-hospital-001', r.id, 'active' FROM `roles` r WHERE r.code='org_admin'
UNION ALL SELECT 'u-trainer-001', 'org-hospital-001', r.id, 'active' FROM `roles` r WHERE r.code='trainer'
UNION ALL SELECT 'u-trainer-002', 'org-hospital-001', r.id, 'active' FROM `roles` r WHERE r.code='trainer'
UNION ALL SELECT 'u-content-editor-001', 'org-hospital-001', r.id, 'active' FROM `roles` r WHERE r.code='content_editor'
UNION ALL SELECT 'u-student-001', 'org-hospital-001', r.id, 'active' FROM `roles` r WHERE r.code='trainer'
UNION ALL SELECT 'u-student-002', 'org-hospital-001', r.id, 'active' FROM `roles` r WHERE r.code='trainer'
UNION ALL SELECT 'u-student-003', 'org-hospital-001', r.id, 'active' FROM `roles` r WHERE r.code='trainer'
UNION ALL SELECT 'u-org-admin-002', 'org-hospital-002', r.id, 'active' FROM `roles` r WHERE r.code='org_admin'
UNION ALL SELECT 'u-trainer-003', 'org-hospital-002', r.id, 'active' FROM `roles` r WHERE r.code='trainer'
UNION ALL SELECT 'u-student-004', 'org-hospital-002', r.id, 'active' FROM `roles` r WHERE r.code='trainer'
UNION ALL SELECT 'u-student-005', 'org-hospital-002', r.id, 'active' FROM `roles` r WHERE r.code='trainer'
UNION ALL SELECT 'u-student-006', 'org-hospital-003', r.id, 'active' FROM `roles` r WHERE r.code='trainer'
UNION ALL SELECT 'u-student-007', 'org-hospital-003', r.id, 'active' FROM `roles` r WHERE r.code='trainer'
ON DUPLICATE KEY UPDATE `status`=VALUES(`status`);

-- ============================================
-- 7) 菜单
-- ============================================
INSERT INTO `menus` (`id`, `parent_id`, `title`, `icon`, `path`, `component`, `sort_order`, `is_visible`, `is_enabled`) VALUES
('m-001', NULL, '课程中心', 'BookOutlined', '/courses', 'CourseListPage', 1, 1, 1),
('m-002', NULL, '情景模拟', 'SimulationOutlined', '/scenarios', 'ScenarioListPage', 2, 1, 1),
('m-003', NULL, '对话练习', 'MessageOutlined', '/chat', 'ChatPage', 3, 1, 1),
('m-004', NULL, '学习进度', 'LineChartOutlined', '/progress', 'ProgressPage', 4, 1, 1),
('m-005', NULL, '系统管理', 'SettingOutlined', '/admin', 'AdminLayout', 100, 1, 1),
('m-005-01', 'm-005', '用户管理', 'UserOutlined', '/admin/users', 'UserManagePage', 1, 1, 1),
('m-005-02', 'm-005', '角色管理', 'TeamOutlined', '/admin/roles', 'RoleManagePage', 2, 1, 1),
('m-005-03', 'm-005', '菜单管理', 'MenuOutlined', '/admin/menus', 'MenuManagePage', 3, 1, 1),
('m-005-04', 'm-005', '机构管理', 'BankOutlined', '/admin/organizations', 'OrganizationPage', 4, 1, 1),
('m-005-05', 'm-005', '培训班级', 'TeamOutlined', '/admin/classes', 'TrainingClassPage', 5, 1, 1),
('m-005-06', 'm-005', '题库管理', 'BookOutlined', '/admin/questions', 'QuestionBankPage', 6, 1, 1),
('m-005-07', 'm-005', '证书管理', 'TrophyOutlined', '/admin/certificates', 'CertificatePage', 7, 1, 1),
('m-006', NULL, '个人中心', 'UserOutlined', '/profile', 'ProfilePage', 5, 1, 1)
ON DUPLICATE KEY UPDATE `title`=VALUES(`title`), `path`=VALUES(`path`);

-- ============================================
-- 8) 角色菜单权限
-- ============================================
INSERT INTO `role_menu_permissions` (`id`, `role`, `menu_id`, `can_view`) VALUES
('rmp-001', 'student', 'm-001', 1),
('rmp-002', 'student', 'm-002', 1),
('rmp-003', 'student', 'm-003', 1),
('rmp-004', 'student', 'm-004', 1),
('rmp-005', 'student', 'm-006', 1),
('rmp-011', 'instructor', 'm-001', 1),
('rmp-012', 'instructor', 'm-002', 1),
('rmp-013', 'instructor', 'm-003', 1),
('rmp-014', 'instructor', 'm-004', 1),
('rmp-015', 'instructor', 'm-006', 1),
('rmp-021', 'admin', 'm-001', 1),
('rmp-022', 'admin', 'm-002', 1),
('rmp-023', 'admin', 'm-003', 1),
('rmp-024', 'admin', 'm-004', 1),
('rmp-025', 'admin', 'm-005', 1),
('rmp-026', 'admin', 'm-005-01', 1),
('rmp-027', 'admin', 'm-005-02', 1),
('rmp-028', 'admin', 'm-005-03', 1),
('rmp-029', 'admin', 'm-005-04', 1),
('rmp-030', 'admin', 'm-005-05', 1),
('rmp-031', 'admin', 'm-005-06', 1),
('rmp-032', 'admin', 'm-005-07', 1),
('rmp-033', 'admin', 'm-006', 1)
ON DUPLICATE KEY UPDATE `can_view`=VALUES(`can_view`);

-- ============================================
-- 9) 班级示例
-- ============================================
INSERT INTO `training_classes` (`id`, `org_id`, `name`, `description`, `start_date`, `end_date`, `trainer_id`, `status`) VALUES
('class-001', 'org-hospital-001', '2025年第一季度围产期护理培训', '面向一院新入职护士的系统培训', '2025-03-01 09:00:00', '2025-03-31 18:00:00', 'u-trainer-001', 'active'),
('class-002', 'org-hospital-002', '2025年第二季度围产期护理培训', '二院季度培训班', '2025-04-01 09:00:00', '2025-04-30 18:00:00', 'u-trainer-003', 'draft')
ON DUPLICATE KEY UPDATE `name`=VALUES(`name`), `status`=VALUES(`status`);

INSERT INTO `class_students` (`class_id`, `user_id`, `status`) VALUES
('class-001', 'u-student-001', 'active'),
('class-001', 'u-student-002', 'active'),
('class-001', 'u-student-003', 'active')
ON DUPLICATE KEY UPDATE `status`=VALUES(`status`);

INSERT INTO `class_tasks` (`id`, `class_id`, `resource_type`, `resource_id`, `resource_version`, `deadline`, `sort_order`) VALUES
('task-001', 'class-001', 'course', 'c-001', '1.0.0', '2025-03-10 23:59:59', 1),
('task-002', 'class-001', 'scenario', 's-001', '1.0.0', '2025-03-20 23:59:59', 2)
ON DUPLICATE KEY UPDATE `resource_id`=VALUES(`resource_id`);

-- ============================================
-- 10) 审计日志示例
-- ============================================
INSERT INTO `audit_logs` (`id`, `user_id`, `org_id`, `action`, `resource_type`, `resource_id`, `changes`, `ip_address`) VALUES
('audit-001', 'u-org-admin-001', 'org-hospital-001', 'create_class', 'training_class', 'class-001', '{"name": "2025年第一季度围产期护理培训"}', '192.168.1.100')
ON DUPLICATE KEY UPDATE `action`=`action`;
