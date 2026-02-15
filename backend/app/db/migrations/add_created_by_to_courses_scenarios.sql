-- ============================================================
-- 添加 created_by 字段到 courses 和 scenarios 表
-- 用于记录课程和场景的创建者，实现基于创建者的权限控制
-- 
-- 执行说明：
-- 1. 如果字段已存在，ALTER TABLE 会报错，可以忽略
-- 2. 如果索引已存在，CREATE INDEX 会报错，可以忽略
-- 3. 建议在执行前备份数据库
-- ============================================================

-- ============================================================
-- 1. 为 courses 表添加 created_by 字段
-- ============================================================
ALTER TABLE `courses` 
ADD COLUMN `created_by` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '创建人' 
AFTER `published_by`;

-- 为 courses.created_by 添加索引
CREATE INDEX `idx_courses_created_by` ON `courses` (`created_by`);

-- ============================================================
-- 2. 为 scenarios 表添加 created_by 字段
-- ============================================================
ALTER TABLE `scenarios` 
ADD COLUMN `created_by` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '创建人' 
AFTER `published_by`;

-- 为 scenarios.created_by 添加索引
CREATE INDEX `idx_scenarios_created_by` ON `scenarios` (`created_by`);

-- ============================================================
-- 3. 数据迁移：为已有数据设置 created_by
-- 对于已有记录，如果 published_by 存在则使用 published_by，否则保持 NULL
-- ============================================================

-- 更新 courses 表：将 published_by 的值复制到 created_by（如果 created_by 为 NULL 且 published_by 不为 NULL）
UPDATE `courses` 
SET `created_by` = `published_by` 
WHERE `created_by` IS NULL AND `published_by` IS NOT NULL;

-- 更新 scenarios 表：将 published_by 的值复制到 created_by（如果 created_by 为 NULL 且 published_by 不为 NULL）
UPDATE `scenarios` 
SET `created_by` = `published_by` 
WHERE `created_by` IS NULL AND `published_by` IS NOT NULL;

