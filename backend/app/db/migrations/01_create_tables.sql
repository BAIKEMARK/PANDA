-- 完整建表脚本（适用于空数据库）
-- 包含：基础表 + 管理系统表 + 表扩展
-- 执行方式: mysql -u用户名 -p数据库名 < 01_create_tables.sql

-- ============================================
-- 第一部分：基础表（如果已存在会跳过）
-- ============================================

-- 用户表
CREATE TABLE IF NOT EXISTS `users` (
  `id` CHAR(36) NOT NULL COMMENT '用户唯一标识符(UUID)',
  `email` VARCHAR(255) NOT NULL COMMENT '邮箱',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
  `name` VARCHAR(100) NOT NULL COMMENT '姓名',
  `role` ENUM('student','admin','instructor') NOT NULL DEFAULT 'student' COMMENT '角色',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_email` (`email`),
  KEY `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统用户表';

-- 课程表
CREATE TABLE IF NOT EXISTS `courses` (
  `id` CHAR(36) NOT NULL COMMENT '课程唯一标识符',
  `title` VARCHAR(255) NOT NULL COMMENT '课程标题',
  `content_url` TEXT COMMENT '课程内容URL或路径',
  `sort_order` INT DEFAULT '0' COMMENT '排序顺序',
  `level` ENUM('L1','L2','L3','L4') NOT NULL DEFAULT 'L1' COMMENT 'THP层级',
  `description` TEXT COMMENT '课程描述',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_level` (`level`),
  KEY `idx_sort` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='THP分层课程表';

-- 场景表
CREATE TABLE IF NOT EXISTS `scenarios` (
  `id` CHAR(36) NOT NULL COMMENT '场景唯一标识符',
  `title` VARCHAR(255) NOT NULL COMMENT '场景标题',
  `description` TEXT COMMENT '场景描述',
  `system_prompt` TEXT NOT NULL COMMENT 'AI系统提示词',
  `patient_background` TEXT COMMENT '患者背景信息',
  `knowledge_tags` VARCHAR(500) DEFAULT NULL COMMENT '知识点标签',
  `difficulty` INT DEFAULT '1' COMMENT '难度等级(1-5)',
  `time_period` VARCHAR(50) DEFAULT NULL COMMENT '时间节点(如:产后3天)',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_difficulty` (`difficulty`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='虚拟患者场景配置表';

-- 证书表
CREATE TABLE IF NOT EXISTS `certificates` (
  `id` CHAR(36) NOT NULL COMMENT '证书ID',
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `certificate_number` VARCHAR(100) NOT NULL COMMENT '证书编号',
  `issue_date` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '颁发日期',
  `credit_hours` DECIMAL(4,1) DEFAULT '0.0' COMMENT '学分',
  PRIMARY KEY (`id`),
  UNIQUE KEY `certificate_number` (`certificate_number`),
  KEY `idx_user` (`user_id`),
  KEY `idx_certificate_number` (`certificate_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='培训证书表';

-- 对话会话表
CREATE TABLE IF NOT EXISTS `chat_sessions` (
  `id` CHAR(36) NOT NULL COMMENT '会话ID',
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `scenario_id` CHAR(36) NOT NULL COMMENT '场景ID',
  `status` ENUM('active','completed','abandoned') DEFAULT 'active' COMMENT '会话状态',
  `start_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
  `end_time` DATETIME DEFAULT NULL COMMENT '结束时间',
  `final_score` INT DEFAULT NULL COMMENT '最终得分',
  `meta_data` JSON DEFAULT NULL COMMENT '会话元数据',
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI对话会话记录表';

-- 对话消息表
CREATE TABLE IF NOT EXISTS `chat_messages` (
  `id` CHAR(36) NOT NULL COMMENT '消息ID',
  `session_id` CHAR(36) NOT NULL COMMENT '会话ID',
  `role` ENUM('user','assistant','system') NOT NULL COMMENT '角色',
  `content` TEXT NOT NULL COMMENT '消息内容',
  `meta_data` JSON DEFAULT NULL COMMENT '消息元数据(情绪、评分等)',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_session` (`session_id`),
  KEY `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='对话消息明细表';

-- 评估报告表
CREATE TABLE IF NOT EXISTS `evaluation_reports` (
  `id` CHAR(36) NOT NULL COMMENT '报告ID',
  `session_id` CHAR(36) NOT NULL COMMENT '会话ID',
  `total_score` INT DEFAULT NULL COMMENT '总分 (0-100)',
  `level_assessment` VARCHAR(20) DEFAULT NULL COMMENT '等级评定: 优秀/良好/合格/不合格',
  `radar_a_risk_identification` INT DEFAULT NULL COMMENT 'A类-风险识别能力 (0-100)',
  `radar_b_communication` INT DEFAULT NULL COMMENT 'B类-沟通支持能力 (0-100)',
  `radar_c_skill_application` INT DEFAULT NULL COMMENT 'C类-THP技能应用 (0-100)',
  `radar_d_safety_management` INT DEFAULT NULL COMMENT 'D类-安全管理能力 (0-100)',
  `radar_e_self_efficacy` INT DEFAULT NULL COMMENT 'E类-自我效能感 (0-100)',
  `state_analysis` JSON DEFAULT NULL COMMENT '状态变化分析数据',
  `detailed_feedback` JSON DEFAULT NULL COMMENT '详细反馈列表',
  `technical_guidance` TEXT COMMENT '技术指导建议',
  `meta_data` JSON DEFAULT NULL COMMENT '其他元数据',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_id` (`session_id`),
  KEY `idx_session` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评估报告表';

-- 用户学习进度表
CREATE TABLE IF NOT EXISTS `user_progress` (
  `id` CHAR(36) NOT NULL COMMENT '进度记录ID',
  `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
  `course_id` CHAR(36) NOT NULL COMMENT '课程ID',
  `is_completed` TINYINT(1) DEFAULT '0' COMMENT '是否完成',
  `completed_at` DATETIME DEFAULT NULL COMMENT '完成时间',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_course` (`user_id`,`course_id`),
  KEY `idx_completed` (`is_completed`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户学习进度表';

-- 菜单表
CREATE TABLE IF NOT EXISTS `menus` (
  `id` CHAR(36) NOT NULL COMMENT '菜单ID',
  `parent_id` CHAR(36) DEFAULT NULL COMMENT '父菜单ID，NULL表示顶级菜单',
  `title` VARCHAR(100) NOT NULL COMMENT '菜单标题',
  `icon` VARCHAR(50) DEFAULT NULL COMMENT '图标名称（Ant Design Icons）',
  `path` VARCHAR(200) DEFAULT NULL COMMENT '前端路由路径',
  `component` VARCHAR(200) DEFAULT NULL COMMENT '前端组件路径',
  `sort_order` INT DEFAULT '0' COMMENT '排序序号，数字越小越靠前',
  `is_visible` TINYINT(1) DEFAULT '1' COMMENT '是否可见（1=可见，0=隐藏）',
  `is_enabled` TINYINT(1) DEFAULT '1' COMMENT '是否启用（1=启用，0=禁用）',
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
  `role` ENUM('student','admin','instructor') NOT NULL COMMENT '角色（基于现有users表的role枚举）',
  `menu_id` CHAR(36) NOT NULL COMMENT '菜单ID',
  `can_view` TINYINT(1) DEFAULT '1' COMMENT '是否可查看（1=可查看，0=不可查看）',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_role_menu` (`role`,`menu_id`),
  KEY `idx_role` (`role`),
  KEY `idx_menu` (`menu_id`),
  CONSTRAINT `fk_rmp_menu` FOREIGN KEY (`menu_id`) REFERENCES `menus` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色菜单权限关联表';

-- ============================================
-- 第二部分：后台管理系统新表
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

-- 培训项目/班级表
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

-- 班级学员关联表
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

-- 班级任务表
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

-- 题库表
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
  INDEX `idx_resource` (`resource_type`, `resource_id`),
  INDEX `idx_created` (`created_at`),
  INDEX `idx_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';

-- 证书模板表
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
-- 第三部分：扩展现有表结构
-- ============================================

-- 扩展用户表
-- 注意：如果列已存在，这些语句会报错，迁移脚本会自动忽略
ALTER TABLE `users` 
ADD COLUMN `org_id` CHAR(36) COMMENT '默认机构ID' AFTER `role`,
ADD COLUMN `phone` VARCHAR(50) COMMENT '手机号' AFTER `name`,
ADD COLUMN `department` VARCHAR(100) COMMENT '科室' AFTER `phone`,
ADD COLUMN `title` VARCHAR(100) COMMENT '职称' AFTER `department`,
ADD COLUMN `employee_id` VARCHAR(100) COMMENT '工号' AFTER `title`;

-- 添加索引（如果不存在会报错，迁移脚本会自动忽略）
ALTER TABLE `users` ADD INDEX `idx_org` (`org_id`);

-- 扩展课程表(版本管理)
-- 注意：如果列已存在，这些语句会报错，迁移脚本会自动忽略
ALTER TABLE `courses`
ADD COLUMN `org_id` CHAR(36) COMMENT '机构ID' AFTER `id`,
ADD COLUMN `scope` ENUM('private', 'platform', 'shared') DEFAULT 'private' COMMENT '发布范围' AFTER `org_id`,
ADD COLUMN `version` VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本号' AFTER `scope`,
ADD COLUMN `version_notes` TEXT COMMENT '版本说明' AFTER `version`,
ADD COLUMN `status` ENUM('draft', 'pending', 'published', 'archived') DEFAULT 'draft' COMMENT '状态' AFTER `version_notes`,
ADD COLUMN `published_at` DATETIME COMMENT '发布时间' AFTER `status`,
ADD COLUMN `published_by` CHAR(36) COMMENT '发布人' AFTER `published_at`,
ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' AFTER `created_at`;

-- 添加索引（如果不存在会报错，迁移脚本会自动忽略）
ALTER TABLE `courses` ADD INDEX `idx_org` (`org_id`);
ALTER TABLE `courses` ADD INDEX `idx_status` (`status`);

-- 扩展场景表(版本管理)
-- 注意：如果列已存在，这些语句会报错，迁移脚本会自动忽略
ALTER TABLE `scenarios`
ADD COLUMN `org_id` CHAR(36) COMMENT '机构ID' AFTER `id`,
ADD COLUMN `scope` ENUM('private', 'platform', 'shared') DEFAULT 'private' COMMENT '发布范围' AFTER `org_id`,
ADD COLUMN `version` VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本号' AFTER `scope`,
ADD COLUMN `version_notes` TEXT COMMENT '版本说明' AFTER `version`,
ADD COLUMN `status` ENUM('draft', 'pending', 'published', 'archived') DEFAULT 'draft' COMMENT '状态' AFTER `version_notes`,
ADD COLUMN `published_at` DATETIME COMMENT '发布时间' AFTER `status`,
ADD COLUMN `published_by` CHAR(36) COMMENT '发布人' AFTER `published_at`,
ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' AFTER `created_at`;

-- 添加索引（如果不存在会报错，迁移脚本会自动忽略）
ALTER TABLE `scenarios` ADD INDEX `idx_org` (`org_id`);
ALTER TABLE `scenarios` ADD INDEX `idx_status` (`status`);

-- 扩展证书表
-- 注意：如果列已存在，这些语句会报错，迁移脚本会自动忽略
ALTER TABLE `certificates`
ADD COLUMN `org_id` CHAR(36) COMMENT '机构ID' AFTER `id`,
ADD COLUMN `class_id` CHAR(36) COMMENT '班级ID' AFTER `org_id`,
ADD COLUMN `template_id` CHAR(36) COMMENT '模板ID' AFTER `class_id`,
ADD COLUMN `status` ENUM('valid', 'revoked') DEFAULT 'valid' COMMENT '状态' AFTER `credit_hours`,
ADD COLUMN `revoked_at` DATETIME COMMENT '撤销时间' AFTER `status`,
ADD COLUMN `revoked_by` CHAR(36) COMMENT '撤销人' AFTER `revoked_at`;

-- 添加索引（如果不存在会报错，迁移脚本会自动忽略）
ALTER TABLE `certificates` ADD INDEX `idx_org` (`org_id`);
ALTER TABLE `certificates` ADD INDEX `idx_class` (`class_id`);
