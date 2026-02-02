-- 全量测试数据初始化脚本
-- 包含：机构、角色、权限、用户、课程、场景、班级、题库、证书等完整测试数据
-- 执行方式: mysql -u用户名 -p数据库名 < 02_init_data.sql

-- ============================================
-- 1. 插入机构数据
-- ============================================
INSERT INTO `organizations` (`id`, `name`, `short_name`, `contact_name`, `contact_phone`, `contact_email`, `status`, `config`) VALUES
('org-platform-001', '平台机构', '平台', '平台管理员', '400-000-0000', 'platform@panda.com', 'active', '{"certificate": true, "export": true, "voice": true, "anti_cheat": true}'),
('org-hospital-001', '第一人民医院', '一院', '张主任', '010-12345678', 'zhang@hospital1.com', 'active', '{"certificate": true, "export": true, "voice": true, "anti_cheat": false}'),
('org-hospital-002', '第二人民医院', '二院', '李主任', '010-87654321', 'li@hospital2.com', 'active', '{"certificate": true, "export": false, "voice": false, "anti_cheat": true}'),
('org-hospital-003', '妇幼保健院', '妇幼', '王主任', '010-11223344', 'wang@mch.com', 'active', '{"certificate": true, "export": true, "voice": true, "anti_cheat": true}')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- ============================================
-- 2. 插入系统角色
-- ============================================
INSERT INTO `roles` (`id`, `code`, `name`, `description`, `scope`) VALUES
('role-super-admin', 'super_admin', '平台超级管理员', '管理所有机构、系统级配置、全局模板与字典项', 'system'),
('role-org-admin', 'org_admin', '机构管理员', '管理本机构用户、班级、证书、数据导出、机构配置', 'org'),
('role-content-editor', 'content_editor', '内容编辑', '维护课程/题库/场景脚本/评分规则（只在授权范围内）', 'org'),
('role-trainer', 'trainer', '培训导师/带教', '建班、分配任务、查看学习与考核结果、点评', 'org'),
('role-auditor', 'auditor', '审计/质控', '只读查看日志、版本变更、评分命中与复盘报告', 'org')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- ============================================
-- 3. 插入权限点
-- ============================================
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

-- ============================================
-- 4. 分配角色权限
-- ============================================

-- 超级管理员角色权限(所有权限)
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-super-admin', `id` FROM `permissions`
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

-- 机构管理员角色权限
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

-- 内容编辑角色权限
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-content-editor', `id` FROM `permissions` 
WHERE `code` IN (
  'course:view', 'course:create', 'course:edit',
  'question:view', 'question:create', 'question:edit',
  'scenario:view', 'scenario:create', 'scenario:edit'
)
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

-- 培训导师角色权限
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-trainer', `id` FROM `permissions` 
WHERE `code` IN (
  'class:view', 'class:create', 'class:edit', 'class:publish',
  'user:view',
  'evaluation:view',
  'certificate:view', 'certificate:issue'
)
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

-- 审计角色权限
INSERT INTO `role_permissions` (`role_id`, `permission_id`)
SELECT 'role-auditor', `id` FROM `permissions` 
WHERE `code` IN (
  'audit:view', 'audit:export',
  'evaluation:view'
)
ON DUPLICATE KEY UPDATE `role_id`=`role_id`;

-- ============================================
-- 5. 插入用户数据（扩展字段）
-- ============================================
-- 注意：如果users表已有数据，这里只更新扩展字段
INSERT INTO `users` (`id`, `email`, `password_hash`, `name`, `role`, `org_id`, `phone`, `department`, `title`, `employee_id`) VALUES
('u-super-admin', 'superadmin@panda.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '超级管理员', 'admin', 'org-platform-001', '13800000001', '平台管理部', '系统管理员', 'EMP001'),
('u-admin-001', 'admin@panda.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '系统管理员', 'admin', 'org-platform-001', '13800000002', '系统管理部', '管理员', 'EMP002'),
('u-org-admin-001', 'orgadmin1@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '张主任', 'admin', 'org-hospital-001', '13800001001', '护理部', '主任', 'H001-001'),
('u-org-admin-002', 'orgadmin2@hospital2.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '李主任', 'admin', 'org-hospital-002', '13800002001', '护理部', '主任', 'H002-001'),
('u-trainer-001', 'trainer1@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '王老师', 'instructor', 'org-hospital-001', '13800001010', '护理部', '培训师', 'H001-010'),
('u-trainer-002', 'trainer2@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '李讲师', 'instructor', 'org-hospital-001', '13800001011', '护理部', '讲师', 'H001-011'),
('u-trainer-003', 'trainer3@hospital2.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '刘老师', 'instructor', 'org-hospital-002', '13800002010', '护理部', '培训师', 'H002-010'),
('u-student-001', 'nurse1@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '张护士', 'student', 'org-hospital-001', '13800001101', '产科', '护士', 'H001-101'),
('u-student-002', 'nurse2@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '刘护士', 'student', 'org-hospital-001', '13800001102', '产科', '护士', 'H001-102'),
('u-student-003', 'nurse3@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '陈护士', 'student', 'org-hospital-001', '13800001103', '产科', '护士', 'H001-103'),
('u-student-004', 'nurse4@hospital2.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '赵护士', 'student', 'org-hospital-002', '13800002101', '产科', '护士', 'H002-101'),
('u-student-005', 'nurse5@hospital2.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '钱护士', 'student', 'org-hospital-002', '13800002102', '产科', '护士', 'H002-102'),
('u-student-006', 'nurse6@mch.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '孙护士', 'student', 'org-hospital-003', '13800003101', '产科', '护士', 'MCH-101'),
('u-student-007', 'nurse7@mch.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '周护士', 'student', 'org-hospital-003', '13800003102', '产科', '护士', 'MCH-102'),
('u-content-editor-001', 'editor1@hospital1.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '编辑员1', 'instructor', 'org-hospital-001', '13800001020', '护理部', '内容编辑', 'H001-020')
ON DUPLICATE KEY UPDATE 
  `org_id`=VALUES(`org_id`),
  `phone`=VALUES(`phone`),
  `department`=VALUES(`department`),
  `title`=VALUES(`title`),
  `employee_id`=VALUES(`employee_id`);

-- ============================================
-- 6. 插入用户机构关联数据
-- ============================================
INSERT INTO `user_organizations` (`user_id`, `org_id`, `role_id`, `status`) VALUES
-- 平台机构用户
('u-super-admin', 'org-platform-001', 'role-super-admin', 'active'),
('u-admin-001', 'org-platform-001', 'role-super-admin', 'active'),
-- 第一人民医院用户
('u-org-admin-001', 'org-hospital-001', 'role-org-admin', 'active'),
('u-trainer-001', 'org-hospital-001', 'role-trainer', 'active'),
('u-trainer-002', 'org-hospital-001', 'role-trainer', 'active'),
('u-content-editor-001', 'org-hospital-001', 'role-content-editor', 'active'),
('u-student-001', 'org-hospital-001', 'role-trainer', 'active'),
('u-student-002', 'org-hospital-001', 'role-trainer', 'active'),
('u-student-003', 'org-hospital-001', 'role-trainer', 'active'),
-- 第二人民医院用户
('u-org-admin-002', 'org-hospital-002', 'role-org-admin', 'active'),
('u-trainer-003', 'org-hospital-002', 'role-trainer', 'active'),
('u-student-004', 'org-hospital-002', 'role-trainer', 'active'),
('u-student-005', 'org-hospital-002', 'role-trainer', 'active'),
-- 妇幼保健院用户
('u-student-006', 'org-hospital-003', 'role-trainer', 'active'),
('u-student-007', 'org-hospital-003', 'role-trainer', 'active')
ON DUPLICATE KEY UPDATE `status`=VALUES(`status`);

-- ============================================
-- 7. 插入课程数据（带版本和机构信息）
-- ============================================
INSERT INTO `courses` (`id`, `title`, `content_url`, `sort_order`, `level`, `description`, `org_id`, `scope`, `version`, `status`, `created_at`) VALUES
('c-001', '围产期抑郁概述', '/courses/l1-overview.pdf', 1, 'L1', '了解围产期抑郁的定义、流行病学数据和社会影响', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('c-002', '围产期抑郁的识别与筛查', '/courses/l1-screening.pdf', 2, 'L1', '学习使用EPDS量表进行抑郁筛查的方法和技巧', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('c-003', '基础沟通技巧', '/courses/l1-communication.pdf', 3, 'L1', '掌握与围产期女性沟通的基本原则和技巧', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('c-004', '心理支持技术', '/courses/l2-support.pdf', 4, 'L2', '学习提供情感支持和心理疏导的专业技术', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('c-005', '危机干预基础', '/courses/l2-crisis.pdf', 5, 'L2', '识别自杀风险信号，掌握初步危机干预方法', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('c-006', '家庭支持系统评估', '/courses/l2-family.pdf', 6, 'L2', '评估和动员家庭支持资源的方法', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('c-007', '认知行为疗法入门', '/courses/l3-cbt.pdf', 7, 'L3', 'CBT基本原理及在围产期抑郁中的应用', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('c-008', '药物治疗知识', '/courses/l3-medication.pdf', 8, 'L3', '了解围产期抑郁的药物治疗方案和注意事项', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('c-009', '多学科协作', '/courses/l4-mdt.pdf', 9, 'L4', '与精神科、产科等多学科团队协作的方法', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('c-010', '案例督导与反思', '/courses/l4-supervision.pdf', 10, 'L4', '通过案例分析提升临床决策能力', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
-- 机构自定义课程
('c-101', '本院特色护理流程', '/courses/hospital1-special.pdf', 1, 'L1', '第一人民医院特色围产期护理流程', 'org-hospital-001', 'private', '1.0.0', 'published', '2025-02-01 00:00:00'),
('c-102', '产后访视规范', '/courses/hospital1-visit.pdf', 2, 'L2', '第一人民医院产后访视标准流程', 'org-hospital-001', 'private', '1.0.0', 'published', '2025-02-01 00:00:00')
ON DUPLICATE KEY UPDATE `title`=`title`;

-- ============================================
-- 8. 插入场景数据（带版本和机构信息）
-- ============================================
INSERT INTO `scenarios` (`id`, `title`, `description`, `system_prompt`, `patient_background`, `knowledge_tags`, `difficulty`, `time_period`, `org_id`, `scope`, `version`, `status`, `created_at`) VALUES
('s-001', '产后情绪低落初筛', '模拟与一位产后2周的新妈妈进行首次情绪筛查对话', '你是一位产后2周的新妈妈，名叫小美，28岁，第一胎。你最近感觉很疲惫，睡眠不好，有时候会莫名其妙地想哭。你对照顾宝宝感到焦虑，担心自己做得不够好。你愿意和护士交流，但不太确定自己的感受是否正常。请根据护士的问题自然地回应，表达你的真实感受。', '小美，28岁，已婚，大学本科学历，会计。丈夫在外地工作，婆婆帮忙照顾月子。顺产，母乳喂养。产前无抑郁史。', 'EPDS筛查,产后情绪,初次访谈', 1, '产后2周', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('s-002', '轻度抑郁情绪支持', '模拟与一位EPDS评分12分的产妇进行心理支持对话', '你是一位产后6周的妈妈，名叫小丽，32岁。你的EPDS筛查评分是12分。你经常感到疲惫和无助，对很多事情失去兴趣，包括照顾宝宝。你有时会责怪自己不是一个好妈妈。你的丈夫很忙，你感到很孤独。你希望有人能理解你的感受。', '小丽，32岁，已婚，研究生学历，教师（产假中）。丈夫是程序员，工作繁忙。剖宫产，混合喂养。孕期有轻度焦虑。', '心理支持,情绪疏导,EPDS中度', 2, '产后6周', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('s-003', '家庭支持不足的产妇', '模拟与一位缺乏家庭支持的产妇进行深入沟通', '你是一位产后3个月的单亲妈妈，名叫小芳，26岁。你独自照顾宝宝，父母在外地，前男友不负责任。你感到非常疲惫和绝望，有时候会想"如果没有我，宝宝会不会过得更好"。但你很爱宝宝，不想伤害他。你需要帮助但不知道该向谁求助。', '小芳，26岁，未婚单亲，高中学历，超市收银员（已辞职）。父母在农村，关系一般。顺产，母乳喂养。经济压力大。', '家庭评估,社会支持,单亲妈妈,轻度自杀意念', 3, '产后3个月', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('s-004', '拒绝承认问题的产妇', '模拟与一位否认自己有问题的产妇进行沟通', '你是一位产后2个月的妈妈，名叫小雯，35岁，二胎。你是一个要强的人，认为自己必须做一个完美的妈妈。虽然你经常失眠、食欲不振、对大宝发脾气，但你坚持认为这些都是正常的，不需要帮助。你对护士的关心有些抵触，觉得她们小题大做。', '小雯，35岁，已婚，硕士学历，企业高管。丈夫是医生。二胎剖宫产，大宝5岁。追求完美，不愿示弱。', '否认心理,动机访谈,完美主义', 3, '产后2个月', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00'),
('s-005', '严重抑郁伴自杀风险', '模拟与一位有自杀意念的产妇进行危机干预', '你是一位产后4周的妈妈，名叫小琳，30岁。你感到极度绝望，觉得自己是个失败者，是家人的负担。你已经好几天没有好好吃饭和睡觉了。你有时会想到死亡，觉得如果自己不在了，大家都会轻松一些。你还没有具体的计划，但这些想法越来越频繁。你今天愿意和护士谈谈。', '小琳，30岁，已婚，本科学历，全职妈妈。丈夫经常出差。难产后剖宫产，宝宝曾住NICU一周。有产前抑郁史，曾服用抗抑郁药。', '危机干预,自杀评估,安全计划,紧急转介', 5, '产后4周', 'org-platform-001', 'platform', '1.0.0', 'published', '2025-01-01 00:00:00')
ON DUPLICATE KEY UPDATE `title`=`title`;

-- ============================================
-- 9. 插入培训班级数据
-- ============================================
INSERT INTO `training_classes` (`id`, `org_id`, `name`, `description`, `start_date`, `end_date`, `trainer_id`, `credit_rule`, `completion_rule`, `status`) VALUES
('class-001', 'org-hospital-001', '2025年第一季度围产期护理培训', '针对产科护士的围产期抑郁管理培训', '2025-03-01 09:00:00', '2025-03-31 18:00:00', 'u-trainer-001', '{"required": 8, "optional": 2}', '{"course_completion": 80, "scenario_practice": 5, "exam_score": 60}', 'active'),
('class-002', 'org-hospital-001', '2025年第二季度围产期护理培训', '第二季度培训班级', '2025-06-01 09:00:00', '2025-06-30 18:00:00', 'u-trainer-002', '{"required": 8, "optional": 2}', '{"course_completion": 80, "scenario_practice": 5, "exam_score": 60}', 'draft'),
('class-003', 'org-hospital-002', '2025年围产期护理基础培训', '基础培训班级', '2025-04-01 09:00:00', '2025-04-30 18:00:00', 'u-trainer-003', '{"required": 6, "optional": 2}', '{"course_completion": 70, "scenario_practice": 3, "exam_score": 60}', 'active'),
('class-004', 'org-hospital-003', '2025年妇幼保健培训', '妇幼保健院专项培训', '2025-05-01 09:00:00', '2025-05-31 18:00:00', 'u-trainer-001', '{"required": 10, "optional": 3}', '{"course_completion": 90, "scenario_practice": 8, "exam_score": 70}', 'draft')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- ============================================
-- 10. 插入班级学员数据
-- ============================================
INSERT INTO `class_students` (`class_id`, `user_id`, `status`) VALUES
-- 班级1的学员
('class-001', 'u-student-001', 'active'),
('class-001', 'u-student-002', 'active'),
('class-001', 'u-student-003', 'active'),
-- 班级2的学员
('class-002', 'u-student-001', 'active'),
('class-002', 'u-student-002', 'active'),
-- 班级3的学员
('class-003', 'u-student-004', 'active'),
('class-003', 'u-student-005', 'active'),
-- 班级4的学员
('class-004', 'u-student-006', 'active'),
('class-004', 'u-student-007', 'active')
ON DUPLICATE KEY UPDATE `status`=VALUES(`status`);

-- ============================================
-- 11. 插入班级任务数据
-- ============================================
INSERT INTO `class_tasks` (`id`, `class_id`, `resource_type`, `resource_id`, `resource_version`, `deadline`, `sort_order`) VALUES
-- 班级1的任务
('task-001', 'class-001', 'course', 'c-001', '1.0.0', '2025-03-10 23:59:59', 1),
('task-002', 'class-001', 'course', 'c-002', '1.0.0', '2025-03-15 23:59:59', 2),
('task-003', 'class-001', 'scenario', 's-001', '1.0.0', '2025-03-20 23:59:59', 3),
('task-004', 'class-001', 'scenario', 's-002', '1.0.0', '2025-03-25 23:59:59', 4),
('task-005', 'class-001', 'course', 'c-003', '1.0.0', '2025-03-31 23:59:59', 5),
-- 班级2的任务
('task-006', 'class-002', 'course', 'c-004', '1.0.0', '2025-06-10 23:59:59', 1),
('task-007', 'class-002', 'scenario', 's-003', '1.0.0', '2025-06-20 23:59:59', 2),
-- 班级3的任务
('task-008', 'class-003', 'course', 'c-001', '1.0.0', '2025-04-10 23:59:59', 1),
('task-009', 'class-003', 'course', 'c-002', '1.0.0', '2025-04-20 23:59:59', 2),
('task-010', 'class-003', 'scenario', 's-001', '1.0.0', '2025-04-30 23:59:59', 3)
ON DUPLICATE KEY UPDATE `deadline`=VALUES(`deadline`);

-- ============================================
-- 12. 插入题库数据
-- ============================================
INSERT INTO `question_bank` (`id`, `org_id`, `scope`, `question_type`, `question_text`, `options`, `correct_answer`, `explanation`, `difficulty`, `knowledge_tags`, `status`) VALUES
-- 平台共享题目
('q-001', 'org-platform-001', 'platform', 'single', 'EPDS量表的评分范围是？', '["0-10分", "0-20分", "0-30分", "0-40分"]', '["0-30分"]', 'EPDS（爱丁堡产后抑郁量表）的评分范围是0-30分，分数越高表示抑郁症状越严重。', 'easy', '["EPDS量表", "筛查工具"]', 'active'),
('q-002', 'org-platform-001', 'platform', 'single', '围产期抑郁的高发期是？', '["孕期", "产后2周", "产后6周", "产后3-6个月"]', '["产后6周"]', '产后6周是围产期抑郁的高发期，需要特别关注。', 'easy', '["流行病学", "高发期"]', 'active'),
('q-003', 'org-platform-001', 'platform', 'multiple', '以下哪些是围产期抑郁的危险因素？', '["既往抑郁史", "家庭支持不足", "经济压力", "完美主义性格"]', '["既往抑郁史", "家庭支持不足", "经济压力", "完美主义性格"]', '这些都是围产期抑郁的常见危险因素。', 'medium', '["危险因素", "风险评估"]', 'active'),
('q-004', 'org-platform-001', 'platform', 'judge', '轻度抑郁可以通过心理支持完全治愈，不需要药物治疗。', '["正确", "错误"]', '["错误"]', '轻度抑郁通常可以通过心理支持改善，但严重情况下仍需要药物治疗。', 'medium', '["治疗原则", "心理支持"]', 'active'),
('q-005', 'org-platform-001', 'platform', 'single', '危机干预的首要原则是？', '["评估风险", "建立信任", "确保安全", "提供支持"]', '["确保安全"]', '危机干预的首要原则是确保患者和他人的人身安全。', 'hard', '["危机干预", "安全原则"]', 'active'),
-- 机构私有题目
('q-101', 'org-hospital-001', 'private', 'single', '本院产后访视的标准时间是？', '["产后3天", "产后7天", "产后14天", "产后28天"]', '["产后7天"]', '第一人民医院标准产后访视时间为产后7天。', 'easy', '["访视规范", "本院流程"]', 'active'),
('q-102', 'org-hospital-001', 'private', 'judge', '本院要求所有产妇在产后42天进行EPDS筛查。', '["正确", "错误"]', '["正确"]', '第一人民医院要求所有产妇在产后42天进行EPDS筛查。', 'easy', '["筛查规范", "本院流程"]', 'active')
ON DUPLICATE KEY UPDATE `question_text`=`question_text`;

-- ============================================
-- 13. 插入证书模板数据
-- ============================================
INSERT INTO `certificate_templates` (`id`, `org_id`, `name`, `template_config`, `status`) VALUES
('cert-tpl-001', 'org-platform-001', '平台标准证书模板', '{"title": "围产期抑郁管理培训证书", "logo_url": "/certificates/logo.png", "number_rule": "CERT-{YYYY}-{MM}-{NO}", "signature": "平台培训中心"}', 'active'),
('cert-tpl-002', 'org-hospital-001', '第一人民医院证书模板', '{"title": "第一人民医院围产期护理培训证书", "logo_url": "/certificates/hospital1-logo.png", "number_rule": "H001-{YYYY}-{NO}", "signature": "第一人民医院护理部"}', 'active'),
('cert-tpl-003', 'org-hospital-002', '第二人民医院证书模板', '{"title": "第二人民医院围产期护理培训证书", "logo_url": "/certificates/hospital2-logo.png", "number_rule": "H002-{YYYY}-{NO}", "signature": "第二人民医院护理部"}', 'active')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- ============================================
-- 14. 插入证书数据
-- ============================================
INSERT INTO `certificates` (`id`, `user_id`, `certificate_number`, `issue_date`, `credit_hours`, `org_id`, `class_id`, `template_id`, `status`) VALUES
('cert-001', 'u-student-001', 'CERT-2025-03-001', '2025-03-31 18:00:00', 8.0, 'org-hospital-001', 'class-001', 'cert-tpl-002', 'valid'),
('cert-002', 'u-student-002', 'CERT-2025-03-002', '2025-03-31 18:00:00', 8.0, 'org-hospital-001', 'class-001', 'cert-tpl-002', 'valid'),
('cert-003', 'u-student-003', 'CERT-2025-03-003', '2025-03-31 18:00:00', 8.0, 'org-hospital-001', 'class-001', 'cert-tpl-002', 'valid'),
('cert-004', 'u-student-004', 'CERT-2025-04-001', '2025-04-30 18:00:00', 6.0, 'org-hospital-002', 'class-003', 'cert-tpl-003', 'valid')
ON DUPLICATE KEY UPDATE `certificate_number`=`certificate_number`;

-- ============================================
-- 15. 插入用户学习进度数据
-- ============================================
INSERT INTO `user_progress` (`id`, `user_id`, `course_id`, `is_completed`, `completed_at`) VALUES
('progress-001', 'u-student-001', 'c-001', 1, '2025-03-05 10:30:00'),
('progress-002', 'u-student-001', 'c-002', 1, '2025-03-12 14:20:00'),
('progress-003', 'u-student-001', 'c-003', 1, '2025-03-18 16:45:00'),
('progress-004', 'u-student-002', 'c-001', 1, '2025-03-06 09:15:00'),
('progress-005', 'u-student-002', 'c-002', 1, '2025-03-13 11:30:00'),
('progress-006', 'u-student-002', 'c-003', 0, NULL),
('progress-007', 'u-student-003', 'c-001', 1, '2025-03-07 15:20:00'),
('progress-008', 'u-student-003', 'c-002', 0, NULL),
('progress-009', 'u-student-004', 'c-001', 1, '2025-04-05 10:00:00'),
('progress-010', 'u-student-004', 'c-002', 1, '2025-04-15 14:30:00')
ON DUPLICATE KEY UPDATE `is_completed`=VALUES(`is_completed`);

-- ============================================
-- 16. 插入对话会话数据
-- ============================================
INSERT INTO `chat_sessions` (`id`, `user_id`, `scenario_id`, `status`, `start_time`, `end_time`, `final_score`) VALUES
('session-001', 'u-student-001', 's-001', 'completed', '2025-03-20 10:00:00', '2025-03-20 10:25:00', 85),
('session-002', 'u-student-001', 's-002', 'completed', '2025-03-25 14:00:00', '2025-03-25 14:30:00', 78),
('session-003', 'u-student-002', 's-001', 'completed', '2025-03-21 09:30:00', '2025-03-21 09:55:00', 82),
('session-004', 'u-student-002', 's-002', 'active', '2025-03-26 15:00:00', NULL, NULL),
('session-005', 'u-student-003', 's-001', 'completed', '2025-03-22 11:00:00', '2025-03-22 11:20:00', 75),
('session-006', 'u-student-004', 's-001', 'completed', '2025-04-10 10:00:00', '2025-04-10 10:28:00', 88)
ON DUPLICATE KEY UPDATE `status`=VALUES(`status`);

-- ============================================
-- 17. 插入对话消息数据（示例）
-- ============================================
INSERT INTO `chat_messages` (`id`, `session_id`, `role`, `content`, `created_at`) VALUES
('msg-001', 'session-001', 'user', '你好，我是来学习围产期护理的护士', '2025-03-20 10:00:00'),
('msg-002', 'session-001', 'assistant', '你好，我是小美，产后2周了，最近感觉有点累', '2025-03-20 10:00:05'),
('msg-003', 'session-001', 'user', '能具体说说你的感受吗？', '2025-03-20 10:02:00'),
('msg-004', 'session-001', 'assistant', '就是睡眠不好，有时候会想哭，担心照顾不好宝宝', '2025-03-20 10:02:10'),
('msg-005', 'session-002', 'user', '你好，我想了解一下你的情况', '2025-03-25 14:00:00'),
('msg-006', 'session-002', 'assistant', '你好，我是小丽，产后6周了，EPDS评分12分', '2025-03-25 14:00:05')
ON DUPLICATE KEY UPDATE `content`=`content`;

-- ============================================
-- 18. 插入评估报告数据
-- ============================================
INSERT INTO `evaluation_reports` (`id`, `session_id`, `total_score`, `level_assessment`, `radar_a_risk_identification`, `radar_b_communication`, `radar_c_skill_application`, `radar_d_safety_management`, `radar_e_self_efficacy`, `technical_guidance`) VALUES
('eval-001', 'session-001', 85, '良好', 88, 82, 85, 90, 80, '风险识别能力较强，能够及时关注患者情绪变化。建议加强沟通技巧的运用，多使用开放式问题。'),
('eval-002', 'session-002', 78, '合格', 75, 80, 75, 85, 75, '沟通能力较好，但在THP技能应用方面需要加强。建议多练习心理支持技术的实际运用。'),
('eval-003', 'session-003', 82, '良好', 85, 80, 82, 88, 75, '整体表现良好，风险识别和安全管理能力突出。建议提升自我效能感，增强自信心。'),
('eval-004', 'session-005', 75, '合格', 70, 75, 75, 80, 75, '基础能力具备，但在各个维度都有提升空间。建议系统学习相关课程，加强实践练习。'),
('eval-005', 'session-006', 88, '优秀', 90, 85, 88, 92, 85, '表现优秀，各项能力均衡发展。建议继续保持，可以尝试更高难度的场景练习。')
ON DUPLICATE KEY UPDATE `total_score`=VALUES(`total_score`);

-- ============================================
-- 19. 插入菜单数据
-- ============================================
INSERT INTO `menus` (`id`, `parent_id`, `title`, `icon`, `path`, `component`, `sort_order`, `is_visible`, `is_enabled`) VALUES
('m-001', NULL, '课程中心', 'BookOutlined', '/courses', 'CourseListPage', 1, 1, 1),
('m-002', NULL, '情景模拟', 'SimulationOutlined', '/scenarios', 'ScenarioListPage', 2, 1, 1),
('m-003', NULL, '对话练习', 'MessageOutlined', '/chat', 'ChatPage', 3, 1, 1),
('m-004', NULL, '学习进度', 'LineChartOutlined', '/progress', 'ProgressPage', 4, 1, 1),
('m-005', NULL, '系统管理', 'SettingOutlined', '/admin', 'AdminLayout', 100, 1, 1),
('m-005-01', 'm-005', '用户管理', 'UserOutlined', '/admin/users', 'UserManagePage', 1, 1, 1),
('m-005-02', 'm-005', '角色管理', 'TeamOutlined', '/admin/roles', 'RoleManagePage', 2, 1, 1),
('m-005-03', 'm-005', '菜单管理', 'MenuOutlined', '/admin/menus', 'MenuManagePage', 3, 1, 1),
('m-005-04', 'm-005', '机构管理', 'BankOutlined', '/admin/organizations', 'OrganizationPage', 4, 1, 1),
('m-005-05', 'm-005', '培训班级', 'TeamOutlined', '/admin/training', 'TrainingClassPage', 5, 1, 1),
('m-006', NULL, '个人中心', 'UserOutlined', '/profile', 'ProfilePage', 5, 1, 1)
ON DUPLICATE KEY UPDATE `title`=`title`;

-- ============================================
-- 20. 插入角色菜单权限数据
-- ============================================
INSERT INTO `role_menu_permissions` (`id`, `role`, `menu_id`, `can_view`) VALUES
-- 学员权限
('p-001', 'student', 'm-001', 1),
('p-002', 'student', 'm-002', 1),
('p-003', 'student', 'm-003', 1),
('p-004', 'student', 'm-004', 1),
('p-005', 'student', 'm-006', 1),
-- 讲师权限
('p-011', 'instructor', 'm-001', 1),
('p-012', 'instructor', 'm-002', 1),
('p-013', 'instructor', 'm-003', 1),
('p-014', 'instructor', 'm-004', 1),
('p-015', 'instructor', 'm-006', 1),
-- 管理员权限
('p-021', 'admin', 'm-001', 1),
('p-022', 'admin', 'm-002', 1),
('p-023', 'admin', 'm-003', 1),
('p-024', 'admin', 'm-004', 1),
('p-025', 'admin', 'm-005', 1),
('p-026', 'admin', 'm-005-01', 1),
('p-027', 'admin', 'm-005-02', 1),
('p-028', 'admin', 'm-005-03', 1),
('p-029', 'admin', 'm-005-04', 1),
('p-030', 'admin', 'm-005-05', 1),
('p-031', 'admin', 'm-006', 1)
ON DUPLICATE KEY UPDATE `can_view`=VALUES(`can_view`);

-- ============================================
-- 21. 插入审计日志数据（示例）
-- ============================================
INSERT INTO `audit_logs` (`id`, `user_id`, `org_id`, `action`, `resource_type`, `resource_id`, `changes`, `ip_address`) VALUES
('audit-001', 'u-org-admin-001', 'org-hospital-001', 'create_class', 'training_class', 'class-001', '{"name": "2025年第一季度围产期护理培训"}', '192.168.1.100'),
('audit-002', 'u-trainer-001', 'org-hospital-001', 'add_student', 'class_student', 'class-001', '{"user_id": "u-student-001"}', '192.168.1.101'),
('audit-003', 'u-content-editor-001', 'org-hospital-001', 'create_course', 'course', 'c-101', '{"title": "本院特色护理流程"}', '192.168.1.102'),
('audit-004', 'u-org-admin-001', 'org-hospital-001', 'issue_certificate', 'certificate', 'cert-001', '{"user_id": "u-student-001", "certificate_number": "CERT-2025-03-001"}', '192.168.1.100'),
('audit-005', 'u-student-001', 'org-hospital-001', 'complete_course', 'course', 'c-001', '{"course_id": "c-001", "completed": true}', '192.168.1.201')
ON DUPLICATE KEY UPDATE `action`=`action`;
