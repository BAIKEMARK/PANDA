-- 合并所有迁移文件，方便一次性执行
-- 执行方式: mysql -u用户名 -p数据库名 < apply_migrations.sql

-- ============================================
-- 001: 创建后台管理基础表
-- ============================================

CREATE TABLE IF NOT EXISTS `organizations` (
  `id` CHAR(36) PRIMARY KEY COMMENT '机构ID',
  `name` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `short_name` VARCHAR(100) COMMENT '简称',
  `logo_url` VARCHAR(500) COMMENT 'LOGO',
  `contact_name` VARCHAR(100) COMMENT '联系人',
  `contact_phone` VARCHAR(50) COMMENT '联系电话',
  `contact_email` VARCHAR(255) COMMENT '联系邮箱',
  `valid_until` DATETIME COMMENT '有效期',
  `status` ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
  `config` JSON COMMENT '机构配置(证书/导出/语音/防作弊开关)',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='机构表';

CREATE TABLE IF NOT EXISTS `roles` (
  `id` CHAR(36) PRIMARY KEY COMMENT '角色ID',
  `code` VARCHAR(50) UNIQUE NOT NULL COMMENT '角色代码',
  `name` VARCHAR(100) NOT NULL COMMENT '角色名称',
  `description` TEXT COMMENT '角色说明',
  `scope` ENUM('system', 'org') DEFAULT 'org' COMMENT '作用域',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

CREATE TABLE IF NOT EXISTS `permissions` (
  `id` CHAR(36) PRIMARY KEY COMMENT '权限ID',
  `code` VARCHAR(100) UNIQUE NOT NULL COMMENT '权限代码',
  `name` VARCHAR(100) NOT NULL COMMENT '权限名称',
  `module` VARCHAR(50) NOT NULL COMMENT '模块',
  `action` VARCHAR(50) NOT NULL COMMENT '操作',
  `description` TEXT COMMENT '权限说明',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_code` (`code`),
  INDEX `idx_module` (`module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限点表';

CREATE TABLE IF NOT EXISTS `role_permissions` (
  `role_id` CHAR(36) NOT NULL COMMENT '角色ID',
  `permission_id` CHAR(36) NOT NULL COMMENT '权限ID',
  PRIMARY KEY (`role_id`, `permission_id`),
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`permission_id`) REFERENCES `permissions`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

CREATE TABLE IF NOT EXISTS `user_organizations` (
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `org_id` CHAR(36) NOT NULL COMMENT '机构ID',
  `role_id` CHAR(36) NOT NULL COMMENT '角色ID',
  `status` ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`user_id`, `org_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`org_id`) REFERENCES `organizations`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`),
  INDEX `idx_org` (`org_id`),
  INDEX `idx_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户机构关联表';

CREATE TABLE IF NOT EXISTS `training_classes` (
  `id` CHAR(36) PRIMARY KEY COMMENT '班级ID',
  `org_id` CHAR(36) NOT NULL COMMENT '机构ID',
  `name` VARCHAR(255) NOT NULL COMMENT '班级名称',
  `description` TEXT COMMENT '描述',
  `start_date` DATETIME NOT NULL COMMENT '开始时间',
  `end_date` DATETIME NOT NULL COMMENT '结束时间',
  `trainer_id` CHAR(36) COMMENT '负责人ID',
  `credit_rule` JSON COMMENT '学分规则',
  `completion_rule` JSON COMMENT '结业标准',
  `status` ENUM('draft', 'active', 'completed', 'archived') DEFAULT 'draft' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_org` (`org_id`),
  INDEX `idx_status` (`status`),
  FOREIGN KEY (`org_id`) REFERENCES `organizations`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='培训班级表';

CREATE TABLE IF NOT EXISTS `class_students` (
  `class_id` CHAR(36) NOT NULL COMMENT '班级ID',
  `user_id` CHAR(36) NOT NULL COMMENT '学员ID',
  `joined_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  `status` ENUM('active', 'completed', 'dropped') DEFAULT 'active' COMMENT '状态',
  PRIMARY KEY (`class_id`, `user_id`),
  FOREIGN KEY (`class_id`) REFERENCES `training_classes`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  INDEX `idx_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级学员表';

CREATE TABLE IF NOT EXISTS `class_tasks` (
  `id` CHAR(36) PRIMARY KEY COMMENT '任务ID',
  `class_id` CHAR(36) NOT NULL COMMENT '班级ID',
  `resource_type` ENUM('course', 'scenario', 'exam') NOT NULL COMMENT '资源类型',
  `resource_id` CHAR(36) NOT NULL COMMENT '资源ID',
  `resource_version` VARCHAR(50) COMMENT '资源版本(锁定)',
  `deadline` DATETIME COMMENT '截止日期',
  `sort_order` INT DEFAULT 0 COMMENT '排序',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_class` (`class_id`),
  FOREIGN KEY (`class_id`) REFERENCES `training_classes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级任务表';

CREATE TABLE IF NOT EXISTS `question_bank` (
  `id` CHAR(36) PRIMARY KEY COMMENT '题目ID',
  `org_id` CHAR(36) COMMENT '机构ID',
  `scope` ENUM('private', 'platform', 'shared') DEFAULT 'private' COMMENT '发布范围',
  `question_type` ENUM('single', 'multiple', 'judge') NOT NULL COMMENT '题型',
  `question_text` TEXT NOT NULL COMMENT '题干',
  `options` JSON NOT NULL COMMENT '选项',
  `correct_answer` JSON NOT NULL COMMENT '正确答案',
  `explanation` TEXT COMMENT '解析',
  `difficulty` ENUM('easy', 'medium', 'hard') DEFAULT 'medium' COMMENT '难度',
  `knowledge_tags` JSON COMMENT '知识点标签',
  `chapter_id` CHAR(36) COMMENT '章节归属',
  `status` ENUM('draft', 'active', 'disabled') DEFAULT 'draft' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_org` (`org_id`),
  INDEX `idx_status` (`status`),
  INDEX `idx_type` (`question_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='题库表';

CREATE TABLE IF NOT EXISTS `audit_logs` (
  `id` CHAR(36) PRIMARY KEY COMMENT '日志ID',
  `user_id` CHAR(36) COMMENT '操作用户',
  `org_id` CHAR(36) COMMENT '机构ID',
  `action` VARCHAR(100) NOT NULL COMMENT '操作',
  `resource_type` VARCHAR(50) COMMENT '资源类型',
  `resource_id` CHAR(36) COMMENT '资源ID',
  `changes` JSON COMMENT '变更内容',
  `ip_address` VARCHAR(50) COMMENT 'IP地址',
  `user_agent` VARCHAR(500) COMMENT '用户代理',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_user` (`user_id`),
  INDEX `idx_resource` (`resource_type`, `resource_id`),
  INDEX `idx_created` (`created_at`),
  INDEX `idx_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';

-- ============================================
-- 002: 扩展现有表结构
-- ============================================

ALTER TABLE `users` 
ADD COLUMN `org_id` CHAR(36) COMMENT '默认机构ID' AFTER `role`,
ADD COLUMN `phone` VARCHAR(50) COMMENT '手机号' AFTER `name`,
ADD COLUMN `department` VARCHAR(100) COMMENT '科室' AFTER `phone`,
ADD COLUMN `title` VARCHAR(100) COMMENT '职称' AFTER `department`,
ADD COLUMN `employee_id` VARCHAR(100) COMMENT '工号' AFTER `title`;

ALTER TABLE `users` ADD INDEX IF NOT EXISTS `idx_org` (`org_id`);

ALTER TABLE `courses`
ADD COLUMN `org_id` CHAR(36) COMMENT '机构ID' AFTER `id`,
ADD COLUMN `scope` ENUM('private', 'platform', 'shared') DEFAULT 'private' COMMENT '发布范围' AFTER `org_id`,
ADD COLUMN `version` VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本号' AFTER `scope`,
ADD COLUMN `version_notes` TEXT COMMENT '版本说明' AFTER `version`,
ADD COLUMN `status` ENUM('draft', 'pending', 'published', 'archived') DEFAULT 'draft' COMMENT '状态' AFTER `version_notes`,
ADD COLUMN `published_at` DATETIME COMMENT '发布时间' AFTER `status`,
ADD COLUMN `published_by` CHAR(36) COMMENT '发布人' AFTER `published_at`,
ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' AFTER `created_at`;

ALTER TABLE `courses` ADD INDEX IF NOT EXISTS `idx_org` (`org_id`);
ALTER TABLE `courses` ADD INDEX IF NOT EXISTS `idx_status` (`status`);

ALTER TABLE `scenarios`
ADD COLUMN `org_id` CHAR(36) COMMENT '机构ID' AFTER `id`,
ADD COLUMN `scope` ENUM('private', 'platform', 'shared') DEFAULT 'private' COMMENT '发布范围' AFTER `org_id`,
ADD COLUMN `version` VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本号' AFTER `scope`,
ADD COLUMN `version_notes` TEXT COMMENT '版本说明' AFTER `version`,
ADD COLUMN `status` ENUM('draft', 'pending', 'published', 'archived') DEFAULT 'draft' COMMENT '状态' AFTER `version_notes`,
ADD COLUMN `published_at` DATETIME COMMENT '发布时间' AFTER `status`,
ADD COLUMN `published_by` CHAR(36) COMMENT '发布人' AFTER `published_at`,
ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' AFTER `created_at`;

ALTER TABLE `scenarios` ADD INDEX IF NOT EXISTS `idx_org` (`org_id`);
ALTER TABLE `scenarios` ADD INDEX IF NOT EXISTS `idx_status` (`status`);

ALTER TABLE `certificates`
ADD COLUMN `org_id` CHAR(36) COMMENT '机构ID' AFTER `id`,
ADD COLUMN `class_id` CHAR(36) COMMENT '班级ID' AFTER `org_id`,
ADD COLUMN `template_id` CHAR(36) COMMENT '模板ID' AFTER `class_id`,
ADD COLUMN `status` ENUM('valid', 'revoked') DEFAULT 'valid' COMMENT '状态' AFTER `credit_hours`,
ADD COLUMN `revoked_at` DATETIME COMMENT '撤销时间' AFTER `status`,
ADD COLUMN `revoked_by` CHAR(36) COMMENT '撤销人' AFTER `revoked_at`;

ALTER TABLE `certificates` ADD INDEX IF NOT EXISTS `idx_org` (`org_id`);
ALTER TABLE `certificates` ADD INDEX IF NOT EXISTS `idx_class` (`class_id`);

CREATE TABLE IF NOT EXISTS `certificate_templates` (
  `id` CHAR(36) PRIMARY KEY COMMENT '模板ID',
  `org_id` CHAR(36) NOT NULL COMMENT '机构ID',
  `name` VARCHAR(255) NOT NULL COMMENT '模板名称',
  `template_config` JSON COMMENT '模板配置(标题/LOGO/编号规则)',
  `status` ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_org` (`org_id`),
  FOREIGN KEY (`org_id`) REFERENCES `organizations`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证书模板表';

-- ============================================
-- 003: 初始化默认数据
-- ============================================

INSERT INTO `organizations` (`id`, `name`, `short_name`, `status`, `config`) 
VALUES ('org-platform-001', '平台机构', '平台', 'active', '{"certificate": true, "export": true, "voice": true, "anti_cheat": true}')
ON DUPLICATE KEY UPDATE `name`=`name`;

INSERT INTO `roles` (`id`, `code`, `name`, `description`, `scope`) VALUES
('role-super-admin', 'super_admin', '平台超级管理员', '管理所有机构、系统级配置、全局模板与字典项', 'system'),
('role-org-admin', 'org_admin', '机构管理员', '管理本机构用户、班级、证书、数据导出、机构配置', 'org'),
('role-content-editor', 'content_editor', '内容编辑', '维护课程/题库/场景脚本/评分规则（只在授权范围内）', 'org'),
('role-trainer', 'trainer', '培训导师/带教', '建班、分配任务、查看学习与考核结果、点评', 'org'),
('role-auditor', 'auditor', '审计/质控', '只读查看日志、版本变更、评分命中与复盘报告', 'org')
ON DUPLICATE KEY UPDATE `name`=`name`;

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
ON DUPLICATE KEY UPDATE `name`=`name`;

INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-super-admin', `id` FROM `permissions`
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

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

INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-content-editor', `id` FROM `permissions` 
WHERE `code` IN (
  'course:view', 'course:create', 'course:edit',
  'question:view', 'question:create', 'question:edit',
  'scenario:view', 'scenario:create', 'scenario:edit'
)
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-trainer', `id` FROM `permissions` 
WHERE `code` IN (
  'class:view', 'class:create', 'class:edit', 'class:publish',
  'user:view',
  'evaluation:view',
  'certificate:view', 'certificate:issue'
)
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-auditor', `id` FROM `permissions` 
WHERE `code` IN (
  'audit:view', 'audit:export',
  'evaluation:view'
)
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;
