-- Phase 1: 后台管理系统基础表结构
-- 创建日期: 2026-01-28

-- 1. 机构表
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

-- 2. 角色表
CREATE TABLE IF NOT EXISTS `roles` (
  `id` CHAR(36) PRIMARY KEY COMMENT '角色ID',
  `code` VARCHAR(50) UNIQUE NOT NULL COMMENT '角色代码',
  `name` VARCHAR(100) NOT NULL COMMENT '角色名称',
  `description` TEXT COMMENT '角色说明',
  `scope` ENUM('system', 'org') DEFAULT 'org' COMMENT '作用域',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  INDEX `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- 3. 权限点表
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

-- 4. 角色权限关联表
CREATE TABLE IF NOT EXISTS `role_permissions` (
  `role_id` CHAR(36) NOT NULL COMMENT '角色ID',
  `permission_id` CHAR(36) NOT NULL COMMENT '权限ID',
  PRIMARY KEY (`role_id`, `permission_id`),
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`permission_id`) REFERENCES `permissions`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- 5. 用户机构关联表
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

-- 6. 培训项目/班级表
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

-- 7. 班级学员关联表
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

-- 8. 班级任务表
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

-- 9. 题库表
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

-- 10. 审计日志表
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
