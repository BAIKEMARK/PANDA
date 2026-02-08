-- 管理后台扩展表结构（不影响 panda.sql）
-- 用途：补齐用户扩展字段 + 管理后台相关表
-- 执行方式: mysql -u用户名 -p数据库名 < 20260204_admin_full.sql

SET NAMES utf8mb4;

-- ============================================
-- 1) 扩展用户表字段（用于机构/人员管理）
--    注意：采用动态判断，避免重复执行时报错
-- ============================================
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' AND COLUMN_NAME = 'org_id'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `users` ADD COLUMN `org_id` CHAR(36) NULL COMMENT ''默认机构ID''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 将 users.role 从枚举迁移为通用字符串，以支持动态角色编码
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' AND COLUMN_NAME = 'role'
);
SET @sql := IF(@col_exists = 1,
  'ALTER TABLE `users` MODIFY COLUMN `role` VARCHAR(100) NOT NULL DEFAULT ''student'' COMMENT ''角色代码（与 roles.code 对齐）''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' AND COLUMN_NAME = 'phone'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `users` ADD COLUMN `phone` VARCHAR(50) NULL COMMENT ''手机号''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' AND COLUMN_NAME = 'department'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `users` ADD COLUMN `department` VARCHAR(100) NULL COMMENT ''科室''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' AND COLUMN_NAME = 'title'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `users` ADD COLUMN `title` VARCHAR(100) NULL COMMENT ''职称''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' AND COLUMN_NAME = 'employee_id'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `users` ADD COLUMN `employee_id` VARCHAR(100) NULL COMMENT ''工号''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @idx_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' AND INDEX_NAME = 'idx_users_org_id'
);
SET @sql := IF(@idx_exists = 0,
  'ALTER TABLE `users` ADD INDEX `idx_users_org_id` (`org_id`)',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- ============================================
-- 1.5) 扩展课程表字段（与 Course 模型对齐）
-- ============================================
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courses' AND COLUMN_NAME = 'org_id'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `courses` ADD COLUMN `org_id` CHAR(36) NULL COMMENT ''机构ID''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courses' AND COLUMN_NAME = 'scope'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `courses` ADD COLUMN `scope` ENUM(''private'',''platform'',''shared'') DEFAULT ''private'' COMMENT ''发布范围''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courses' AND COLUMN_NAME = 'version'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `courses` ADD COLUMN `version` VARCHAR(50) DEFAULT ''1.0.0'' COMMENT ''版本号''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courses' AND COLUMN_NAME = 'version_notes'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `courses` ADD COLUMN `version_notes` TEXT NULL COMMENT ''版本说明''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courses' AND COLUMN_NAME = 'status'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `courses` ADD COLUMN `status` ENUM(''draft'',''pending'',''published'',''archived'') DEFAULT ''draft'' COMMENT ''状态''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courses' AND COLUMN_NAME = 'published_at'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `courses` ADD COLUMN `published_at` DATETIME NULL COMMENT ''发布时间''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courses' AND COLUMN_NAME = 'published_by'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `courses` ADD COLUMN `published_by` CHAR(36) NULL COMMENT ''发布人''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courses' AND COLUMN_NAME = 'video_url'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `courses` ADD COLUMN `video_url` TEXT NULL COMMENT ''视频URL''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courses' AND COLUMN_NAME = 'updated_at'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `courses` ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT ''更新时间''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @idx_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'courses' AND INDEX_NAME = 'idx_courses_org_id'
);
SET @sql := IF(@idx_exists = 0,
  'ALTER TABLE `courses` ADD INDEX `idx_courses_org_id` (`org_id`)',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- ============================================
-- 1.6) 扩展场景表字段（与 Scenario 模型对齐）
-- ============================================
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'scenarios' AND COLUMN_NAME = 'org_id'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `scenarios` ADD COLUMN `org_id` CHAR(36) NULL COMMENT ''机构ID''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'scenarios' AND COLUMN_NAME = 'scope'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `scenarios` ADD COLUMN `scope` ENUM(''private'',''platform'',''shared'') DEFAULT ''private'' COMMENT ''发布范围''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'scenarios' AND COLUMN_NAME = 'version'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `scenarios` ADD COLUMN `version` VARCHAR(50) DEFAULT ''1.0.0'' COMMENT ''版本号''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'scenarios' AND COLUMN_NAME = 'version_notes'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `scenarios` ADD COLUMN `version_notes` TEXT NULL COMMENT ''版本说明''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'scenarios' AND COLUMN_NAME = 'status'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `scenarios` ADD COLUMN `status` ENUM(''draft'',''pending'',''published'',''archived'') DEFAULT ''draft'' COMMENT ''状态''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'scenarios' AND COLUMN_NAME = 'published_at'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `scenarios` ADD COLUMN `published_at` DATETIME NULL COMMENT ''发布时间''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'scenarios' AND COLUMN_NAME = 'published_by'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `scenarios` ADD COLUMN `published_by` CHAR(36) NULL COMMENT ''发布人''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'scenarios' AND COLUMN_NAME = 'updated_at'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `scenarios` ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT ''更新时间''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @idx_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'scenarios' AND INDEX_NAME = 'idx_scenarios_org_id'
);
SET @sql := IF(@idx_exists = 0,
  'ALTER TABLE `scenarios` ADD INDEX `idx_scenarios_org_id` (`org_id`)',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- ============================================
-- 1.7) 扩展对话会话表字段（与 ChatSession 模型对齐）
-- ============================================
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'chat_sessions' AND COLUMN_NAME = 'has_suicide_risk'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `chat_sessions` ADD COLUMN `has_suicide_risk` TINYINT(1) DEFAULT 0 COMMENT ''会话中是否检测到自杀倾向''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'chat_sessions' AND COLUMN_NAME = 'suicide_risk_alerted'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `chat_sessions` ADD COLUMN `suicide_risk_alerted` TINYINT(1) DEFAULT 0 COMMENT ''用户是否点击了报警按钮''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'chat_sessions' AND COLUMN_NAME = 'suicide_risk_alert_time'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `chat_sessions` ADD COLUMN `suicide_risk_alert_time` DATETIME NULL COMMENT ''报警时间''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'chat_sessions' AND COLUMN_NAME = 'suicide_risk_first_detected'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `chat_sessions` ADD COLUMN `suicide_risk_first_detected` DATETIME NULL COMMENT ''首次检测到自杀倾向的时间''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- ============================================
-- 2) 管理后台表结构（如已存在会跳过）
-- ============================================

-- 机构表
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

-- 兼容已有 organizations 表结构：补齐 valid_until / config
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'organizations' AND COLUMN_NAME = 'valid_until'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `organizations` ADD COLUMN `valid_until` DATETIME NULL COMMENT ''有效期''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'organizations' AND COLUMN_NAME = 'config'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `organizations` ADD COLUMN `config` JSON NULL COMMENT ''机构配置(证书/导出/语音/防作弊开关)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 角色表
CREATE TABLE IF NOT EXISTS `roles` (
  `id` CHAR(36) PRIMARY KEY COMMENT '角色ID',
  `code` VARCHAR(50) UNIQUE NOT NULL COMMENT '角色代码',
  `name` VARCHAR(100) NOT NULL COMMENT '角色名称',
  `description` TEXT COMMENT '角色说明',
  `scope` ENUM('system', 'org') DEFAULT 'org' COMMENT '作用域',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- 兼容已有 roles 表结构：补齐 description，并修正 scope 枚举
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'roles' AND COLUMN_NAME = 'description'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `roles` ADD COLUMN `description` TEXT NULL COMMENT ''角色说明''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 允许 platform -> system 的转换（先扩展枚举，再更新，再收敛）
SET @sql := 'ALTER TABLE `roles` MODIFY COLUMN `scope` ENUM(''platform'',''system'',''org'') NOT NULL DEFAULT ''org''';
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
UPDATE `roles` SET `scope`='system' WHERE `scope`='platform';
SET @sql := 'ALTER TABLE `roles` MODIFY COLUMN `scope` ENUM(''system'',''org'') NOT NULL DEFAULT ''org''';
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 权限点表
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

-- 兼容已有 permissions 表结构：补齐 description
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'permissions' AND COLUMN_NAME = 'description'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `permissions` ADD COLUMN `description` TEXT NULL COMMENT ''权限说明''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 角色权限关联表
CREATE TABLE IF NOT EXISTS `role_permissions` (
  `role_id` CHAR(36) NOT NULL COMMENT '角色ID',
  `permission_id` CHAR(36) NOT NULL COMMENT '权限ID',
  PRIMARY KEY (`role_id`, `permission_id`),
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`permission_id`) REFERENCES `permissions`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- 用户机构关联表
CREATE TABLE IF NOT EXISTS `user_organizations` (
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `org_id` CHAR(36) NOT NULL COMMENT '机构ID',
  `role_id` CHAR(36) NOT NULL COMMENT '角色ID',
  `status` ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`user_id`, `org_id`),
  FOREIGN KEY (`org_id`) REFERENCES `organizations`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`),
  INDEX `idx_org` (`org_id`),
  INDEX `idx_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户机构关联表';

-- 培训班级表
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

-- 兼容已有 training_classes 表结构：补齐 trainer_id，调整时间字段类型
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'training_classes' AND COLUMN_NAME = 'trainer_id'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `training_classes` ADD COLUMN `trainer_id` CHAR(36) NULL COMMENT ''负责人ID''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @sql := 'ALTER TABLE `training_classes` MODIFY COLUMN `start_date` DATETIME NULL COMMENT ''开始时间''';
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
SET @sql := 'ALTER TABLE `training_classes` MODIFY COLUMN `end_date` DATETIME NULL COMMENT ''结束时间''';
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'training_classes' AND COLUMN_NAME = 'owner_id'
);
SET @sql := IF(@col_exists = 1,
  'ALTER TABLE `training_classes` MODIFY COLUMN `owner_id` CHAR(36) NULL COMMENT ''负责人ID(兼容旧字段)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 班级学员关联表
CREATE TABLE IF NOT EXISTS `class_students` (
  `class_id` CHAR(36) NOT NULL COMMENT '班级ID',
  `user_id` CHAR(36) NOT NULL COMMENT '学员ID',
  `joined_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  `status` ENUM('active', 'completed', 'dropped') DEFAULT 'active' COMMENT '状态',
  PRIMARY KEY (`class_id`, `user_id`),
  FOREIGN KEY (`class_id`) REFERENCES `training_classes`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级学员关联表';

-- 班级任务表
CREATE TABLE IF NOT EXISTS `class_tasks` (
  `id` CHAR(36) PRIMARY KEY COMMENT '任务ID',
  `class_id` CHAR(36) NOT NULL COMMENT '班级ID',
  `resource_type` ENUM('course', 'scenario', 'exam') NOT NULL COMMENT '资源类型',
  `resource_id` CHAR(36) NOT NULL COMMENT '资源ID',
  `resource_version` VARCHAR(50) COMMENT '资源版本',
  `deadline` DATETIME COMMENT '截止日期',
  `sort_order` INT DEFAULT 0 COMMENT '排序',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_class` (`class_id`),
  FOREIGN KEY (`class_id`) REFERENCES `training_classes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级任务表';

-- 审计日志表
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
  INDEX `idx_org` (`org_id`),
  INDEX `idx_resource` (`resource_type`, `resource_id`),
  INDEX `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';

-- 兼容已有 audit_logs 表结构：从 actor_id/detail 迁移到 user_id/changes
SET @col_user := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'audit_logs' AND COLUMN_NAME = 'user_id'
);
SET @col_actor := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'audit_logs' AND COLUMN_NAME = 'actor_id'
);
SET @sql := IF(@col_user = 0 AND @col_actor = 1,
  'ALTER TABLE `audit_logs` CHANGE COLUMN `actor_id` `user_id` CHAR(36) NULL COMMENT ''操作用户''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_user := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'audit_logs' AND COLUMN_NAME = 'user_id'
);
SET @sql := IF(@col_user = 0,
  'ALTER TABLE `audit_logs` ADD COLUMN `user_id` CHAR(36) NULL COMMENT ''操作用户''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_detail := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'audit_logs' AND COLUMN_NAME = 'detail'
);
SET @col_changes := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'audit_logs' AND COLUMN_NAME = 'changes'
);
SET @sql := IF(@col_changes = 0 AND @col_detail = 1,
  'ALTER TABLE `audit_logs` CHANGE COLUMN `detail` `changes` JSON NULL COMMENT ''变更内容''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_changes := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'audit_logs' AND COLUMN_NAME = 'changes'
);
SET @sql := IF(@col_changes = 0,
  'ALTER TABLE `audit_logs` ADD COLUMN `changes` JSON NULL COMMENT ''变更内容''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 菜单表
CREATE TABLE IF NOT EXISTS `menus` (
  `id` CHAR(36) NOT NULL COMMENT '菜单ID',
  `parent_id` CHAR(36) DEFAULT NULL COMMENT '父菜单ID，NULL表示顶级菜单',
  `title` VARCHAR(100) NOT NULL COMMENT '菜单标题',
  `icon` VARCHAR(50) DEFAULT NULL COMMENT '图标名称',
  `path` VARCHAR(200) DEFAULT NULL COMMENT '前端路由路径',
  `component` VARCHAR(200) DEFAULT NULL COMMENT '前端组件路径',
  `sort_order` INT DEFAULT '0' COMMENT '排序序号',
  `is_visible` TINYINT(1) DEFAULT '1' COMMENT '是否可见',
  `is_enabled` TINYINT(1) DEFAULT '1' COMMENT '是否启用',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent` (`parent_id`),
  KEY `idx_sort` (`sort_order`),
  KEY `idx_enabled` (`is_enabled`),
  CONSTRAINT `fk_menu_parent` FOREIGN KEY (`parent_id`) REFERENCES `menus` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统菜单表';

-- 角色菜单权限关联表
CREATE TABLE IF NOT EXISTS `role_menu_permissions` (
  `id` CHAR(36) NOT NULL COMMENT '权限ID',
  `role` ENUM('student','admin','instructor') NOT NULL COMMENT '角色',
  `menu_id` CHAR(36) NOT NULL COMMENT '菜单ID',
  `can_view` TINYINT(1) DEFAULT '1' COMMENT '是否可查看',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_role_menu` (`role`,`menu_id`),
  KEY `idx_role` (`role`),
  KEY `idx_menu` (`menu_id`),
  CONSTRAINT `fk_rmp_menu` FOREIGN KEY (`menu_id`) REFERENCES `menus` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色菜单权限关联表';

-- ============================================
-- 3) 题库与证书扩展（与现有表兼容）
-- ============================================

-- 题库表（如不存在则创建）
CREATE TABLE IF NOT EXISTS `question_bank` (
  `id` CHAR(36) PRIMARY KEY COMMENT '题目ID',
  `org_id` CHAR(36) COMMENT '机构ID',
  `scope` ENUM('private','platform','shared') DEFAULT 'private' COMMENT '发布范围',
  `question_type` ENUM('single','multiple','judge') NOT NULL COMMENT '题型',
  `question_text` TEXT NOT NULL COMMENT '题干',
  `options` JSON NOT NULL COMMENT '选项',
  `correct_answer` JSON NOT NULL COMMENT '正确答案',
  `explanation` TEXT COMMENT '解析',
  `difficulty` ENUM('easy','medium','hard') DEFAULT 'medium' COMMENT '难度',
  `knowledge_tags` JSON COMMENT '知识点标签',
  `chapter_id` CHAR(36) COMMENT '章节归属',
  `status` ENUM('draft','active','disabled') DEFAULT 'draft' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_org` (`org_id`),
  INDEX `idx_type` (`question_type`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='题库表';

-- 证书模板表（如不存在则创建）
CREATE TABLE IF NOT EXISTS `certificate_templates` (
  `id` CHAR(36) PRIMARY KEY COMMENT '模板ID',
  `org_id` CHAR(36) NOT NULL COMMENT '机构ID',
  `name` VARCHAR(255) NOT NULL COMMENT '模板名称',
  `template_config` JSON COMMENT '模板配置(JSON)',
  `status` ENUM('active','inactive') DEFAULT 'active' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX `idx_org` (`org_id`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证书模板表';

-- 证书表缺失字段补齐
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'certificates' AND COLUMN_NAME = 'org_id'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `certificates` ADD COLUMN `org_id` CHAR(36) NULL COMMENT ''机构ID''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'certificates' AND COLUMN_NAME = 'class_id'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `certificates` ADD COLUMN `class_id` CHAR(36) NULL COMMENT ''班级ID''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'certificates' AND COLUMN_NAME = 'template_id'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `certificates` ADD COLUMN `template_id` CHAR(36) NULL COMMENT ''模板ID''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'certificates' AND COLUMN_NAME = 'status'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `certificates` ADD COLUMN `status` ENUM(''valid'',''revoked'') DEFAULT ''valid'' COMMENT ''状态''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'certificates' AND COLUMN_NAME = 'revoked_at'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `certificates` ADD COLUMN `revoked_at` DATETIME NULL COMMENT ''撤销时间''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'certificates' AND COLUMN_NAME = 'revoked_by'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `certificates` ADD COLUMN `revoked_by` CHAR(36) NULL COMMENT ''撤销人''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- ============================================
-- 4) 核心表对齐（学习进度/评估/患者状态）
--    仅新增字段与修正枚举，不删除任何列
-- ============================================

-- users: updated_at
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'users' AND COLUMN_NAME = 'updated_at'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `users` ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT ''更新时间''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- evaluation_reports: add new columns
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'error_message'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `error_message` TEXT COMMENT ''错误信息（生成失败时）''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'total_score'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `total_score` INT DEFAULT NULL COMMENT ''总分 (0-100)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'level_assessment'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `level_assessment` VARCHAR(20) DEFAULT NULL COMMENT ''等级评定: 优秀/良好/合格/不合格''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'radar_a_risk_identification'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `radar_a_risk_identification` INT DEFAULT NULL COMMENT ''A类-风险识别能力 (0-100)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'radar_b_communication'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `radar_b_communication` INT DEFAULT NULL COMMENT ''B类-沟通支持能力 (0-100)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'radar_c_skill_application'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `radar_c_skill_application` INT DEFAULT NULL COMMENT ''C类-THP技能应用 (0-100)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'radar_d_safety_management'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `radar_d_safety_management` INT DEFAULT NULL COMMENT ''D类-安全管理能力 (0-100)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'radar_e_self_efficacy'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `radar_e_self_efficacy` INT DEFAULT NULL COMMENT ''E类-自我效能感 (0-100)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'state_analysis'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `state_analysis` JSON DEFAULT NULL COMMENT ''状态变化分析数据''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'technical_guidance'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `technical_guidance` TEXT COMMENT ''技术指导建议''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'meta_data'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `meta_data` JSON DEFAULT NULL COMMENT ''其他元数据''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'completed_at'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `evaluation_reports` ADD COLUMN `completed_at` DATETIME DEFAULT NULL COMMENT ''完成时间''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 扩展 status 枚举，兼容 processing/generating
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'evaluation_reports' AND COLUMN_NAME = 'status'
);
SET @sql := IF(@col_exists = 1,
  'ALTER TABLE `evaluation_reports` MODIFY COLUMN `status` ENUM(''pending'',''processing'',''generating'',''completed'',''failed'') NOT NULL DEFAULT ''pending'' COMMENT ''报告生成状态: pending-待生成, generating-生成中, completed-已完成, failed-失败''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- patient_states: add new columns
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'patient_states' AND COLUMN_NAME = 'satisfaction_score'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `patient_states` ADD COLUMN `satisfaction_score` INT DEFAULT 50 COMMENT ''满意度 (0-100)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'patient_states' AND COLUMN_NAME = 'depression_level'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `patient_states` ADD COLUMN `depression_level` INT DEFAULT 50 COMMENT ''抑郁程度 (0-100)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'patient_states' AND COLUMN_NAME = 'rapport_score'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `patient_states` ADD COLUMN `rapport_score` INT DEFAULT 50 COMMENT ''信任度 (0-100)''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'patient_states' AND COLUMN_NAME = 'message_count'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `patient_states` ADD COLUMN `message_count` INT DEFAULT 0 COMMENT ''对话轮次''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 兼容旧字段 trust_level -> rapport_score
SET @col_trust := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'patient_states' AND COLUMN_NAME = 'trust_level'
);
SET @col_rapport := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'patient_states' AND COLUMN_NAME = 'rapport_score'
);
SET @sql := IF(@col_trust = 1 AND @col_rapport = 1,
  'UPDATE `patient_states` SET `rapport_score` = `trust_level` WHERE `rapport_score` IS NULL',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- user_progress: add new columns
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'user_progress' AND COLUMN_NAME = 'course_id'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `user_progress` ADD COLUMN `course_id` CHAR(36) NULL COMMENT ''课程ID''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'user_progress' AND COLUMN_NAME = 'is_completed'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `user_progress` ADD COLUMN `is_completed` TINYINT(1) DEFAULT 0 COMMENT ''是否完成''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'user_progress' AND COLUMN_NAME = 'created_at'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `user_progress` ADD COLUMN `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT ''创建时间''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 兼容旧字段 resource_id -> course_id
SET @col_res := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'user_progress' AND COLUMN_NAME = 'resource_id'
);
SET @col_course := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'user_progress' AND COLUMN_NAME = 'course_id'
);
SET @sql := IF(@col_res = 1 AND @col_course = 1,
  'UPDATE `user_progress` SET `course_id` = `resource_id` WHERE `course_id` IS NULL OR `course_id` = ''''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- 兼容旧字段 status -> is_completed
SET @col_status := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'user_progress' AND COLUMN_NAME = 'status'
);
SET @col_done := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'user_progress' AND COLUMN_NAME = 'is_completed'
);
SET @sql := IF(@col_status = 1 AND @col_done = 1,
  'UPDATE `user_progress` SET `is_completed` = CASE WHEN `status` = ''completed'' THEN 1 ELSE 0 END WHERE `is_completed` IS NULL OR `is_completed` = 0',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- role_menu_permissions: add role column, keep role_code
SET @col_exists := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'role_menu_permissions' AND COLUMN_NAME = 'role'
);
SET @sql := IF(@col_exists = 0,
  'ALTER TABLE `role_menu_permissions` ADD COLUMN `role` ENUM(''student'',''instructor'',''admin'') NULL COMMENT ''角色''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_role := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'role_menu_permissions' AND COLUMN_NAME = 'role'
);
SET @col_role_code := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'role_menu_permissions' AND COLUMN_NAME = 'role_code'
);
SET @sql := IF(@col_role = 1 AND @col_role_code = 1,
  'UPDATE `role_menu_permissions` SET `role` = `role_code` WHERE `role` IS NULL',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_role := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'role_menu_permissions' AND COLUMN_NAME = 'role'
);
SET @sql := IF(@col_role = 1,
  'UPDATE `role_menu_permissions` SET `role` = ''student'' WHERE `role` IS NULL',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SET @col_role := (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'role_menu_permissions' AND COLUMN_NAME = 'role'
);
SET @sql := IF(@col_role = 1,
  'ALTER TABLE `role_menu_permissions` MODIFY COLUMN `role` ENUM(''student'',''instructor'',''admin'') NOT NULL COMMENT ''角色''',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
