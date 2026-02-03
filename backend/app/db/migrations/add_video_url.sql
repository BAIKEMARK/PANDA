-- 添加视频URL字段到课程表
-- 执行此脚本前请确保已备份数据库

-- 添加 video_url 列
ALTER TABLE `courses` 
ADD COLUMN `video_url` TEXT NULL COMMENT '视频URL' AFTER `content_url`;

-- 更新注释以区分 content_url 和 video_url
ALTER TABLE `courses` 
MODIFY COLUMN `content_url` TEXT NULL COMMENT '课件PDF URL';
