-- Phase 1: 初始化默认数据
-- 创建日期: 2026-01-28

-- 1. 插入默认机构(平台机构)
INSERT INTO `organizations` (`id`, `name`, `short_name`, `status`, `config`) 
VALUES ('org-platform-001', '平台机构', '平台', 'active', '{"certificate": true, "export": true, "voice": true, "anti_cheat": true}')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- 2. 插入系统角色
INSERT INTO `roles` (`id`, `code`, `name`, `description`, `scope`) VALUES
('role-super-admin', 'super_admin', '平台超级管理员', '管理所有机构、系统级配置、全局模板与字典项', 'system'),
('role-org-admin', 'org_admin', '机构管理员', '管理本机构用户、班级、证书、数据导出、机构配置', 'org'),
('role-content-editor', 'content_editor', '内容编辑', '维护课程/题库/场景脚本/评分规则（只在授权范围内）', 'org'),
('role-trainer', 'trainer', '培训导师/带教', '建班、分配任务、查看学习与考核结果、点评', 'org'),
('role-auditor', 'auditor', '审计/质控', '只读查看日志、版本变更、评分命中与复盘报告', 'org')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- 3. 插入权限点
INSERT INTO `permissions` (`id`, `code`, `name`, `module`, `action`, `description`) VALUES
-- 机构管理
('perm-org-view', 'org:view', '查看机构', 'org', 'view', '查看机构信息'),
('perm-org-create', 'org:create', '创建机构', 'org', 'create', '创建新机构'),
('perm-org-edit', 'org:edit', '编辑机构', 'org', 'edit', '编辑机构信息'),
('perm-org-delete', 'org:delete', '删除机构', 'org', 'delete', '删除机构'),
-- 用户管理
('perm-user-view', 'user:view', '查看用户', 'user', 'view', '查看用户列表和信息'),
('perm-user-create', 'user:create', '创建用户', 'user', 'create', '创建新用户'),
('perm-user-edit', 'user:edit', '编辑用户', 'user', 'edit', '编辑用户信息'),
('perm-user-delete', 'user:delete', '删除用户', 'user', 'delete', '删除用户'),
('perm-user-export', 'user:export', '导出用户', 'user', 'export', '导出用户数据'),
-- 班级管理
('perm-class-view', 'class:view', '查看班级', 'class', 'view', '查看班级列表和信息'),
('perm-class-create', 'class:create', '创建班级', 'class', 'create', '创建新班级'),
('perm-class-edit', 'class:edit', '编辑班级', 'class', 'edit', '编辑班级信息'),
('perm-class-publish', 'class:publish', '发布班级', 'class', 'publish', '发布班级'),
('perm-class-export', 'class:export', '导出班级', 'class', 'export', '导出班级数据'),
-- 课程管理
('perm-course-view', 'course:view', '查看课程', 'course', 'view', '查看课程列表和详情'),
('perm-course-create', 'course:create', '创建课程', 'course', 'create', '创建新课程'),
('perm-course-edit', 'course:edit', '编辑课程', 'course', 'edit', '编辑课程内容'),
('perm-course-publish', 'course:publish', '发布课程', 'course', 'publish', '发布课程'),
('perm-course-archive', 'course:archive', '下线课程', 'course', 'archive', '下线课程'),
('perm-course-export', 'course:export', '导出课程', 'course', 'export', '导出课程数据'),
-- 题库管理
('perm-question-view', 'question:view', '查看题目', 'question', 'view', '查看题目列表'),
('perm-question-create', 'question:create', '创建题目', 'question', 'create', '创建新题目'),
('perm-question-edit', 'question:edit', '编辑题目', 'question', 'edit', '编辑题目'),
('perm-question-delete', 'question:delete', '删除题目', 'question', 'delete', '删除题目'),
('perm-question-import', 'question:import', '导入题目', 'question', 'import', '批量导入题目'),
-- 场景管理
('perm-scenario-view', 'scenario:view', '查看场景', 'scenario', 'view', '查看场景列表'),
('perm-scenario-create', 'scenario:create', '创建场景', 'scenario', 'create', '创建新场景'),
('perm-scenario-edit', 'scenario:edit', '编辑场景', 'scenario', 'edit', '编辑场景'),
('perm-scenario-publish', 'scenario:publish', '发布场景', 'scenario', 'publish', '发布场景'),
('perm-scenario-archive', 'scenario:archive', '下线场景', 'scenario', 'archive', '下线场景'),
-- 评估管理
('perm-evaluation-view', 'evaluation:view', '查看评估', 'evaluation', 'view', '查看评估报告'),
('perm-evaluation-export', 'evaluation:export', '导出评估', 'evaluation', 'export', '导出评估数据'),
-- 证书管理
('perm-certificate-view', 'certificate:view', '查看证书', 'certificate', 'view', '查看证书列表'),
('perm-certificate-issue', 'certificate:issue', '发放证书', 'certificate', 'issue', '发放证书'),
('perm-certificate-revoke', 'certificate:revoke', '撤销证书', 'certificate', 'revoke', '撤销证书'),
-- 审计日志
('perm-audit-view', 'audit:view', '查看审计日志', 'audit', 'view', '查看审计日志'),
('perm-audit-export', 'audit:export', '导出审计日志', 'audit', 'export', '导出审计日志')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- 4. 超级管理员角色权限(所有权限)
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-super-admin', `id` FROM `permissions`
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

-- 5. 机构管理员角色权限
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-org-admin', `id` FROM `permissions` 
WHERE `code` IN (
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
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

-- 6. 内容编辑角色权限
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-content-editor', `id` FROM `permissions` 
WHERE `code` IN (
  'course:view', 'course:create', 'course:edit',
  'question:view', 'question:create', 'question:edit',
  'scenario:view', 'scenario:create', 'scenario:edit'
)
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

-- 7. 培训导师角色权限
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-trainer', `id` FROM `permissions` 
WHERE `code` IN (
  'class:view', 'class:create', 'class:edit', 'class:publish',
  'user:view',
  'evaluation:view',
  'certificate:view', 'certificate:issue'
)
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

-- 8. 审计角色权限
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-auditor', `id` FROM `permissions` 
WHERE `code` IN (
  'audit:view', 'audit:export',
  'evaluation:view'
)
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;
