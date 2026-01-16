-- ============================================
-- 数据库建表脚本
-- 医疗培训系统 MVP - MySQL 8.0+
-- 设计原则: 无物理外键，ID使用UUID，JSON存储动态数据
-- ============================================

-- 创建数据库 (如果不存在)
-- CREATE DATABASE IF NOT EXISTS medical_training DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE medical_training;

-- ============================================
-- 1. 用户模块
-- ============================================

-- 用户表
CREATE TABLE IF NOT EXISTS `users` (
    `id` CHAR(36) NOT NULL COMMENT '用户ID',
    `email` VARCHAR(255) NOT NULL COMMENT '邮箱',
    `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
    `name` VARCHAR(100) NOT NULL COMMENT '姓名',
    `role` ENUM('student', 'instructor', 'admin') DEFAULT 'student' COMMENT '角色',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_email` (`email`),
    KEY `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统用户表';

-- ============================================
-- 2. 课程与进度模块
-- ============================================

-- 课程表
CREATE TABLE IF NOT EXISTS `courses` (
    `id` CHAR(36) NOT NULL COMMENT '课程ID',
    `title` VARCHAR(255) NOT NULL COMMENT '课程标题',
    `content_url` TEXT COMMENT '内容URL',
    `sort_order` INT DEFAULT 0 COMMENT '排序顺序',
    `level` ENUM('L1', 'L2', 'L3', 'L4') DEFAULT 'L1' COMMENT 'THP层级',
    `description` TEXT COMMENT '课程描述',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_sort_order` (`sort_order`),
    KEY `idx_level` (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程表';

-- 学习进度表
CREATE TABLE IF NOT EXISTS `user_progress` (
    `id` CHAR(36) NOT NULL COMMENT '进度ID',
    `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
    `course_id` CHAR(36) NOT NULL COMMENT '课程ID',
    `is_completed` TINYINT(1) DEFAULT 0 COMMENT '是否完成',
    `completed_at` DATETIME COMMENT '完成时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_course_id` (`course_id`),
    UNIQUE KEY `uk_user_course` (`user_id`, `course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习进度表';

-- ============================================
-- 3. 情景模拟配置模块
-- ============================================

-- 场景脚本表
CREATE TABLE IF NOT EXISTS `scenarios` (
    `id` CHAR(36) NOT NULL COMMENT '场景ID',
    `title` VARCHAR(255) NOT NULL COMMENT '场景标题',
    `description` TEXT COMMENT '场景描述',
    `system_prompt` TEXT NOT NULL COMMENT 'AI系统提示词',
    `patient_background` TEXT COMMENT '患者背景信息',
    `knowledge_tags` VARCHAR(500) COMMENT '知识点标签',
    `difficulty` INT DEFAULT 1 COMMENT '难度等级(1-5)',
    `time_period` VARCHAR(50) COMMENT '时间节点',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_difficulty` (`difficulty`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='场景脚本表';

-- ============================================
-- 4. 对话交互模块
-- ============================================

-- 会话记录表
CREATE TABLE IF NOT EXISTS `chat_sessions` (
    `id` CHAR(36) NOT NULL COMMENT '会话ID',
    `user_id` CHAR(36) NOT NULL COMMENT '用户ID',
    `scenario_id` CHAR(36) NOT NULL COMMENT '场景ID',
    `status` ENUM('active', 'completed', 'abandoned') DEFAULT 'active' COMMENT '会话状态',
    `start_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
    `end_time` DATETIME COMMENT '结束时间',
    `final_score` INT COMMENT '最终得分',
    `meta_data` JSON COMMENT '会话元数据',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_scenario_id` (`scenario_id`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会话记录表';

-- 消息明细表
CREATE TABLE IF NOT EXISTS `chat_messages` (
    `id` CHAR(36) NOT NULL COMMENT '消息ID',
    `session_id` CHAR(36) NOT NULL COMMENT '会话ID',
    `role` ENUM('user', 'assistant', 'system') NOT NULL COMMENT '角色',
    `content` TEXT NOT NULL COMMENT '消息内容',
    `meta_data` JSON COMMENT '消息元数据',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_session_id` (`session_id`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息明细表';

-- ============================================
-- 5. 评估与反馈模块
-- ============================================

-- 评估报告表
CREATE TABLE IF NOT EXISTS `evaluation_reports` (
    `id` CHAR(36) NOT NULL COMMENT '报告ID',
    `session_id` CHAR(36) NOT NULL COMMENT '会话ID',
    `scores` JSON COMMENT '评分详情(empathy/skill/safety等)',
    `total_score` INT COMMENT '总分',
    `ai_feedback` TEXT COMMENT 'AI反馈建议',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_session_id` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评估报告表';

-- ============================================
-- 数据表关系说明 (逻辑关联，无物理外键)
-- ============================================
-- users.id <- user_progress.user_id
-- courses.id <- user_progress.course_id
-- users.id <- chat_sessions.user_id
-- scenarios.id <- chat_sessions.scenario_id
-- chat_sessions.id <- chat_messages.session_id
-- chat_sessions.id <- evaluation_reports.session_id
-- ============================================
