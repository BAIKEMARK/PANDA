-- =====================================================
-- PANDA 围产期抑郁管理智能培训系统
-- 数据库表结构初始化脚本
-- 版本: 1.0.0
-- 说明: 包含所有表结构定义，不含数据
-- =====================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 创建数据库
CREATE DATABASE IF NOT EXISTS `panda` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `panda`;

-- =====================================================
-- 核心业务表
-- =====================================================

-- 用户表
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` CHAR(36) NOT NULL COMMENT '用户ID',
  `email` VARCHAR(255) NOT NULL COMMENT '邮箱',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
  `name` VARCHAR(100) NOT NULL COMMENT '姓名',
  `role` VARCHAR(100) NOT NULL DEFAULT 'student' COMMENT '角色代码',
  `org_id` CHAR(36) NULL COMMENT '默认机构ID',
  `phone` VARCHAR(50) NULL COMMENT '手机号',
  `department` VARCHAR(100) NULL COMMENT '科室',
  `title` VARCHAR(100) NULL COMMENT '职称',
  `employee_id` VARCHAR(100) NULL COMMENT '工号',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  INDEX `idx_role` (`role`),
  INDEX `idx_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 课程表
DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses` (
  `id` CHAR(36) NOT NULL COMMENT '课程ID',
  `title` VARCHAR(255) NOT NULL COMMENT '课程标题',
  `description` TEXT COMMENT '课程描述',
  `content_url` VARCHAR(500) COMMENT '课程内容URL',
  `level` VARCHAR(50) COMMENT '课程级别',
  `sort_order` INT DEFAULT 0 COMMENT '排序',
  `org_id` CHAR(36) NULL COMMENT '机构ID',
  `scope` ENUM('private','platform','shared') DEFAULT 'private' COMMENT '发布范围',
  `version` VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本号',
  `version_notes` TEXT NULL COMMENT '版本说明',
  `status` ENUM('draft','pending','published','archived') DEFAULT 'draft' COMMENT '状态',
  `published_at` DATETIME NULL COMMENT '发布时间',
  `published_by` CHAR(36) NULL COMMENT '发布人',
  `video_url` TEXT NULL COMMENT '视频URL',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_level` (`level`),
  INDEX `idx_status` (`status`),
  INDEX `idx_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程表';

-- 场景表
DROP TABLE IF EXISTS `scenarios`;
CREATE TABLE `scenarios` (
  `id` CHAR(36) NOT NULL COMMENT '场景ID',
  `title` VARCHAR(255) NOT NULL COMMENT '场景标题',
  `description` TEXT COMMENT '场景描述',
  `system_prompt` TEXT COMMENT '系统提示词',
  `patient_background` TEXT COMMENT '患者背景',
  `knowledge_tags` VARCHAR(500) COMMENT '知识点标签',
  `difficulty` INT DEFAULT 1 COMMENT '难度等级',
  `time_period` VARCHAR(100) COMMENT '时间段',
  `org_id` CHAR(36) NULL COMMENT '机构ID',
  `scope` ENUM('private','platform','shared') DEFAULT 'private' COMMENT '发布范围',
  `version` VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本号',
  `version_notes` TEXT NULL COMMENT '版本说明',
  `status` ENUM('draft','pending','published','archived') DEFAULT 'draft' COMMENT '状态',
  `published_at` DATETIME NULL COMMENT '发布时间',
  `published_by` CHAR(36) NULL COMMENT '发布人',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_difficulty` (`difficulty`),
  INDEX `idx_status` (`status`),
  INDEX `idx_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='虚拟患者场景表';

-- 对话会话表
DROP TABLE IF EXISTS `chat_sessions`;
CREATE TABLE `chat_sessions` (
  `id` CHAR(36) NOT NULL COMMENT '会话ID',
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `scenario_id` CHAR(36) NOT NULL COMMENT '场景ID',
  `status` ENUM('active','completed','abandoned') DEFAULT 'active' COMMENT '会话状态',
  `start_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
  `end_time` DATETIME NULL COMMENT '结束时间',
  `final_score` INT NULL COMMENT '最终得分',
  `meta_data` JSON NULL COMMENT '会话元数据',
  `has_suicide_risk` TINYINT(1) DEFAULT 0 COMMENT '是否检测到自杀倾向',
  `suicide_risk_alerted` TINYINT(1) DEFAULT 0 COMMENT '是否点击报警按钮',
  `suicide_risk_alert_time` DATETIME NULL COMMENT '报警时间',
  `suicide_risk_first_detected` DATETIME NULL COMMENT '首次检测到自杀倾向的时间',
  PRIMARY KEY (`id`),
  INDEX `idx_user` (`user_id`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='对话会话表';

-- 对话消息表
DROP TABLE IF EXISTS `chat_messages`;
CREATE TABLE `chat_messages` (
  `id` CHAR(36) NOT NULL COMMENT '消息ID',
  `session_id` CHAR(36) NOT NULL COMMENT '会话ID',
  `role` ENUM('user','assistant','system') NOT NULL COMMENT '角色',
  `content` TEXT NOT NULL COMMENT '消息内容',
  `meta_data` JSON NULL COMMENT '消息元数据',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  INDEX `idx_session` (`session_id`),
  INDEX `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='对话消息表';

-- 评估报告表
DROP TABLE IF EXISTS `evaluation_reports`;
CREATE TABLE `evaluation_reports` (
  `id` CHAR(36) NOT NULL COMMENT '报告ID',
  `session_id` CHAR(36) NOT NULL COMMENT '会话ID',
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `scenario_id` CHAR(36) NOT NULL COMMENT '场景ID',
  `overall_score` INT DEFAULT 0 COMMENT '总分',
  `communication_score` INT DEFAULT 0 COMMENT '沟通技巧得分',
  `empathy_score` INT DEFAULT 0 COMMENT '共情能力得分',
  `assessment_score` INT DEFAULT 0 COMMENT '评估能力得分',
  `intervention_score` INT DEFAULT 0 COMMENT '干预能力得分',
  `strengths` TEXT COMMENT '优势',
  `improvements` TEXT COMMENT '改进建议',
  `detailed_feedback` JSON COMMENT '详细反馈',
  `status` ENUM('pending','processing','completed','failed') DEFAULT 'pending' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_id` (`session_id`),
  INDEX `idx_user` (`user_id`),
  INDEX `idx_status` (`status`),
  INDEX `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评估报告表';

-- 患者状态表
DROP TABLE IF EXISTS `patient_states`;
CREATE TABLE `patient_states` (
  `session_id` CHAR(36) NOT NULL COMMENT '会话ID',
  `mood_score` INT DEFAULT 50 COMMENT '心情指数',
  `trust_level` INT DEFAULT 30 COMMENT '信任度',
  `openness` INT DEFAULT 40 COMMENT '开放度',
  `anxiety_level` INT DEFAULT 60 COMMENT '焦虑水平',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='患者状态表';

-- 用户进度表
DROP TABLE IF EXISTS `user_progress`;
CREATE TABLE `user_progress` (
  `id` CHAR(36) NOT NULL COMMENT '进度ID',
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `resource_type` ENUM('course','scenario') NOT NULL COMMENT '资源类型',
  `resource_id` CHAR(36) NOT NULL COMMENT '资源ID',
  `status` ENUM('not_started','in_progress','completed') DEFAULT 'not_started' COMMENT '状态',
  `progress_percentage` INT DEFAULT 0 COMMENT '进度百分比',
  `last_accessed` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '最后访问时间',
  `completed_at` DATETIME NULL COMMENT '完成时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_resource` (`user_id`, `resource_type`, `resource_id`),
  INDEX `idx_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户进度表';

-- 测验表
DROP TABLE IF EXISTS `quizzes`;
CREATE TABLE `quizzes` (
  `id` CHAR(36) NOT NULL COMMENT '测验ID',
  `course_id` CHAR(36) NULL COMMENT '关联课程ID',
  `title` VARCHAR(255) NOT NULL COMMENT '测验标题',
  `questions` JSON NOT NULL COMMENT '题目列表',
  `passing_score` INT DEFAULT 60 COMMENT '及格分数',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  INDEX `idx_course` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测验表';

-- 测验结果表
DROP TABLE IF EXISTS `quiz_results`;
CREATE TABLE `quiz_results` (
  `id` CHAR(36) NOT NULL COMMENT '结果ID',
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `quiz_id` CHAR(36) NOT NULL COMMENT '测验ID',
  `score` INT NOT NULL COMMENT '得分',
  `answers` JSON NOT NULL COMMENT '答案',
  `passed` TINYINT(1) DEFAULT 0 COMMENT '是否通过',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  INDEX `idx_user` (`user_id`),
  INDEX `idx_quiz` (`quiz_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测验结果表';

-- 证书表
DROP TABLE IF EXISTS `certificates`;
CREATE TABLE `certificates` (
  `id` CHAR(36) NOT NULL COMMENT '证书ID',
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `certificate_number` VARCHAR(100) NOT NULL COMMENT '证书编号',
  `issue_date` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '颁发日期',
  `credit_hours` DECIMAL(4,1) DEFAULT 0.0 COMMENT '学分',
  PRIMARY KEY (`id`),
  UNIQUE KEY `certificate_number` (`certificate_number`),
  INDEX `idx_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证书表';

-- =====================================================
-- 管理后台表
-- =====================================================

-- 机构表
DROP TABLE IF EXISTS `organizations`;
CREATE TABLE `organizations` (
  `id` CHAR(36) NOT NULL COMMENT '机构ID',
  `name` VARCHAR(255) NOT NULL COMMENT '机构名称',
  `short_name` VARCHAR(100) COMMENT '简称',
  `logo_url` VARCHAR(500) COMMENT 'LOGO',
  `contact_name` VARCHAR(100) COMMENT '联系人',
  `contact_phone` VARCHAR(50) COMMENT '联系电话',
  `contact_email` VARCHAR(255) COMMENT '联系邮箱',
  `valid_until` DATETIME COMMENT '有效期',
  `status` ENUM('active','inactive') DEFAULT 'active' COMMENT '状态',
  `config` JSON COMMENT '机构配置',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='机构表';

-- 角色表
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id` CHAR(36) NOT NULL COMMENT '角色ID',
  `code` VARCHAR(50) NOT NULL COMMENT '角色代码',
  `name` VARCHAR(100) NOT NULL COMMENT '角色名称',
  `description` TEXT COMMENT '角色说明',
  `scope` ENUM('system','org') DEFAULT 'org' COMMENT '作用域',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- 权限表
DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions` (
  `id` CHAR(36) NOT NULL COMMENT '权限ID',
  `code` VARCHAR(100) NOT NULL COMMENT '权限代码',
  `name` VARCHAR(100) NOT NULL COMMENT '权限名称',
  `module` VARCHAR(50) NOT NULL COMMENT '模块',
  `action` VARCHAR(50) NOT NULL COMMENT '操作',
  `description` TEXT COMMENT '权限说明',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  INDEX `idx_module` (`module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';

-- 角色权限关联表
DROP TABLE IF EXISTS `role_permissions`;
CREATE TABLE `role_permissions` (
  `role_id` CHAR(36) NOT NULL COMMENT '角色ID',
  `permission_id` CHAR(36) NOT NULL COMMENT '权限ID',
  PRIMARY KEY (`role_id`, `permission_id`),
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`permission_id`) REFERENCES `permissions`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- 用户机构关联表
DROP TABLE IF EXISTS `user_organizations`;
CREATE TABLE `user_organizations` (
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `org_id` CHAR(36) NOT NULL COMMENT '机构ID',
  `role_id` CHAR(36) NOT NULL COMMENT '角色ID',
  `status` ENUM('active','inactive') DEFAULT 'active' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`user_id`, `org_id`),
  FOREIGN KEY (`org_id`) REFERENCES `organizations`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`),
  INDEX `idx_org` (`org_id`),
  INDEX `idx_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户机构关联表';

-- 菜单表
DROP TABLE IF EXISTS `menus`;
CREATE TABLE `menus` (
  `id` CHAR(36) NOT NULL COMMENT '菜单ID',
  `parent_id` CHAR(36) NULL COMMENT '父菜单ID',
  `title` VARCHAR(100) NOT NULL COMMENT '菜单标题',
  `icon` VARCHAR(50) NULL COMMENT '图标',
  `path` VARCHAR(200) NULL COMMENT '路由路径',
  `component` VARCHAR(200) NULL COMMENT '组件路径',
  `sort_order` INT DEFAULT 0 COMMENT '排序',
  `is_visible` TINYINT(1) DEFAULT 1 COMMENT '是否可见',
  `is_enabled` TINYINT(1) DEFAULT 1 COMMENT '是否启用',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_parent` (`parent_id`),
  INDEX `idx_sort` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='菜单表';

-- 角色菜单权限表
DROP TABLE IF EXISTS `role_menu_permissions`;
CREATE TABLE `role_menu_permissions` (
  `id` CHAR(36) NOT NULL COMMENT '权限ID',
  `role_code` VARCHAR(50) NOT NULL COMMENT '角色代码（对应roles.code）',
  `menu_id` CHAR(36) NOT NULL COMMENT '菜单ID',
  `can_view` TINYINT(1) DEFAULT 1 COMMENT '是否可查看',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_role_menu` (`role_code`, `menu_id`),
  INDEX `idx_role_code` (`role_code`),
  INDEX `idx_menu` (`menu_id`),
  FOREIGN KEY (`menu_id`) REFERENCES `menus`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色菜单权限表';

-- 培训班级表
DROP TABLE IF EXISTS `training_classes`;
CREATE TABLE `training_classes` (
  `id` CHAR(36) NOT NULL COMMENT '班级ID',
  `org_id` CHAR(36) NOT NULL COMMENT '机构ID',
  `name` VARCHAR(255) NOT NULL COMMENT '班级名称',
  `description` TEXT COMMENT '描述',
  `start_date` DATETIME NULL COMMENT '开始时间',
  `end_date` DATETIME NULL COMMENT '结束时间',
  `trainer_id` CHAR(36) NULL COMMENT '负责人ID',
  `credit_rule` JSON COMMENT '学分规则',
  `completion_rule` JSON COMMENT '结业标准',
  `status` ENUM('draft','active','completed','archived') DEFAULT 'draft' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_org` (`org_id`),
  INDEX `idx_status` (`status`),
  FOREIGN KEY (`org_id`) REFERENCES `organizations`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='培训班级表';

-- 班级学员关联表
DROP TABLE IF EXISTS `class_students`;
CREATE TABLE `class_students` (
  `class_id` CHAR(36) NOT NULL COMMENT '班级ID',
  `user_id` CHAR(36) NOT NULL COMMENT '学员ID',
  `joined_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  `status` ENUM('active','completed','dropped') DEFAULT 'active' COMMENT '状态',
  PRIMARY KEY (`class_id`, `user_id`),
  FOREIGN KEY (`class_id`) REFERENCES `training_classes`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级学员关联表';

-- 班级任务表
DROP TABLE IF EXISTS `class_tasks`;
CREATE TABLE `class_tasks` (
  `id` CHAR(36) NOT NULL COMMENT '任务ID',
  `class_id` CHAR(36) NOT NULL COMMENT '班级ID',
  `resource_type` ENUM('course','scenario','exam') NOT NULL COMMENT '资源类型',
  `resource_id` CHAR(36) NOT NULL COMMENT '资源ID',
  `resource_version` VARCHAR(50) COMMENT '资源版本',
  `deadline` DATETIME COMMENT '截止日期',
  `sort_order` INT DEFAULT 0 COMMENT '排序',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  INDEX `idx_class` (`class_id`),
  FOREIGN KEY (`class_id`) REFERENCES `training_classes`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级任务表';

-- 题库表
DROP TABLE IF EXISTS `question_bank`;
CREATE TABLE `question_bank` (
  `id` CHAR(36) NOT NULL COMMENT '题目ID',
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
  PRIMARY KEY (`id`),
  INDEX `idx_org` (`org_id`),
  INDEX `idx_type` (`question_type`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='题库表';

-- 证书模板表
DROP TABLE IF EXISTS `certificate_templates`;
CREATE TABLE `certificate_templates` (
  `id` CHAR(36) NOT NULL COMMENT '模板ID',
  `org_id` CHAR(36) NOT NULL COMMENT '机构ID',
  `name` VARCHAR(255) NOT NULL COMMENT '模板名称',
  `template_config` JSON COMMENT '模板配置',
  `status` ENUM('active','inactive') DEFAULT 'active' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_org` (`org_id`),
  FOREIGN KEY (`org_id`) REFERENCES `organizations`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证书模板表';

-- 文件表
DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
  `id` CHAR(36) NOT NULL COMMENT '文件ID',
  `org_id` CHAR(36) COMMENT '机构ID',
  `filename` VARCHAR(255) NOT NULL COMMENT '原始文件名',
  `stored_filename` VARCHAR(255) NOT NULL COMMENT '存储文件名',
  `file_path` VARCHAR(500) NOT NULL COMMENT '文件路径',
  `file_type` VARCHAR(50) COMMENT '文件类型',
  `file_size` INT COMMENT '文件大小',
  `mime_type` VARCHAR(100) COMMENT 'MIME类型',
  `category` VARCHAR(50) DEFAULT 'courseware' COMMENT '文件分类',
  `resource_type` VARCHAR(50) COMMENT '关联资源类型',
  `resource_id` CHAR(36) COMMENT '关联资源ID',
  `uploaded_by` CHAR(36) NOT NULL COMMENT '上传人',
  `description` TEXT COMMENT '文件描述',
  `status` ENUM('active','deleted') DEFAULT 'active' COMMENT '状态',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  INDEX `idx_org` (`org_id`),
  INDEX `idx_resource` (`resource_type`, `resource_id`),
  INDEX `idx_category` (`category`),
  INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文件表';

-- 审计日志表
DROP TABLE IF EXISTS `audit_logs`;
CREATE TABLE `audit_logs` (
  `id` CHAR(36) NOT NULL COMMENT '日志ID',
  `user_id` CHAR(36) COMMENT '操作用户',
  `org_id` CHAR(36) COMMENT '机构ID',
  `action` VARCHAR(100) NOT NULL COMMENT '操作',
  `resource_type` VARCHAR(50) COMMENT '资源类型',
  `resource_id` CHAR(36) COMMENT '资源ID',
  `changes` JSON COMMENT '变更内容',
  `ip_address` VARCHAR(50) COMMENT 'IP地址',
  `user_agent` VARCHAR(500) COMMENT '用户代理',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  INDEX `idx_user` (`user_id`),
  INDEX `idx_org` (`org_id`),
  INDEX `idx_resource` (`resource_type`, `resource_id`),
  INDEX `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';

SET FOREIGN_KEY_CHECKS = 1;

