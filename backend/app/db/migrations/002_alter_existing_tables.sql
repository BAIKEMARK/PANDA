-- Phase 1: 扩展现有表结构
-- 创建日期: 2026-01-28

-- 1. 扩展用户表(添加机构关联字段，保留向后兼容)
ALTER TABLE `users` 
ADD COLUMN IF NOT EXISTS `org_id` CHAR(36) COMMENT '默认机构ID' AFTER `role`,
ADD COLUMN IF NOT EXISTS `phone` VARCHAR(50) COMMENT '手机号' AFTER `name`,
ADD COLUMN IF NOT EXISTS `department` VARCHAR(100) COMMENT '科室' AFTER `phone`,
ADD COLUMN IF NOT EXISTS `title` VARCHAR(100) COMMENT '职称' AFTER `department`,
ADD COLUMN IF NOT EXISTS `employee_id` VARCHAR(100) COMMENT '工号' AFTER `title`,
ADD INDEX IF NOT EXISTS `idx_org` (`org_id`);

-- 2. 扩展课程表(版本管理)
ALTER TABLE `courses`
ADD COLUMN IF NOT EXISTS `org_id` CHAR(36) COMMENT '机构ID' AFTER `id`,
ADD COLUMN IF NOT EXISTS `scope` ENUM('private', 'platform', 'shared') DEFAULT 'private' COMMENT '发布范围' AFTER `org_id`,
ADD COLUMN IF NOT EXISTS `version` VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本号' AFTER `scope`,
ADD COLUMN IF NOT EXISTS `version_notes` TEXT COMMENT '版本说明' AFTER `version`,
ADD COLUMN IF NOT EXISTS `status` ENUM('draft', 'pending', 'published', 'archived') DEFAULT 'draft' COMMENT '状态' AFTER `version_notes`,
ADD COLUMN IF NOT EXISTS `published_at` DATETIME COMMENT '发布时间' AFTER `status`,
ADD COLUMN IF NOT EXISTS `published_by` CHAR(36) COMMENT '发布人' AFTER `published_at`,
ADD COLUMN IF NOT EXISTS `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' AFTER `created_at`,
ADD INDEX IF NOT EXISTS `idx_org` (`org_id`),
ADD INDEX IF NOT EXISTS `idx_status` (`status`);

-- 3. 扩展场景表(版本管理)
ALTER TABLE `scenarios`
ADD COLUMN IF NOT EXISTS `org_id` CHAR(36) COMMENT '机构ID' AFTER `id`,
ADD COLUMN IF NOT EXISTS `scope` ENUM('private', 'platform', 'shared') DEFAULT 'private' COMMENT '发布范围' AFTER `org_id`,
ADD COLUMN IF NOT EXISTS `version` VARCHAR(50) DEFAULT '1.0.0' COMMENT '版本号' AFTER `scope`,
ADD COLUMN IF NOT EXISTS `version_notes` TEXT COMMENT '版本说明' AFTER `version`,
ADD COLUMN IF NOT EXISTS `status` ENUM('draft', 'pending', 'published', 'archived') DEFAULT 'draft' COMMENT '状态' AFTER `version_notes`,
ADD COLUMN IF NOT EXISTS `published_at` DATETIME COMMENT '发布时间' AFTER `status`,
ADD COLUMN IF NOT EXISTS `published_by` CHAR(36) COMMENT '发布人' AFTER `published_at`,
ADD COLUMN IF NOT EXISTS `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间' AFTER `created_at`,
ADD INDEX IF NOT EXISTS `idx_org` (`org_id`),
ADD INDEX IF NOT EXISTS `idx_status` (`status`);

-- 4. 扩展证书表
ALTER TABLE `certificates`
ADD COLUMN IF NOT EXISTS `org_id` CHAR(36) COMMENT '机构ID' AFTER `id`,
ADD COLUMN IF NOT EXISTS `class_id` CHAR(36) COMMENT '班级ID' AFTER `org_id`,
ADD COLUMN IF NOT EXISTS `template_id` CHAR(36) COMMENT '模板ID' AFTER `class_id`,
ADD COLUMN IF NOT EXISTS `status` ENUM('valid', 'revoked') DEFAULT 'valid' COMMENT '状态' AFTER `credit_hours`,
ADD COLUMN IF NOT EXISTS `revoked_at` DATETIME COMMENT '撤销时间' AFTER `status`,
ADD COLUMN IF NOT EXISTS `revoked_by` CHAR(36) COMMENT '撤销人' AFTER `revoked_at`,
ADD INDEX IF NOT EXISTS `idx_org` (`org_id`),
ADD INDEX IF NOT EXISTS `idx_class` (`class_id`);

-- 5. 创建证书模板表
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
