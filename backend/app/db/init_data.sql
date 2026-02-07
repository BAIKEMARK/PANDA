-- =====================================================
-- PANDA 围产期抑郁管理智能培训系统
-- 初始化模拟数据脚本
-- 版本: 1.0.0
-- 说明: 包含测试用户、课程、场景等模拟数据
-- =====================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

USE `panda`;

-- =====================================================
-- 1. 用户数据
-- 默认密码: admin123
-- 密码哈希: $2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S
-- =====================================================

INSERT INTO `users` (`id`, `email`, `password_hash`, `name`, `role`, `created_at`) VALUES
('u-admin-001', 'admin@panda.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '系统管理员', 'admin', NOW()),
('u-instructor-001', 'teacher@panda.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '王老师', 'instructor', NOW()),
('u-student-001', 'nurse1@hospital.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '张护士', 'student', NOW()),
('u-student-002', 'nurse2@hospital.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '刘护士', 'student', NOW()),
('u-student-003', 'test@test.com', '$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S', '测试用户', 'student', NOW());

-- =====================================================
-- 2. 课程数据（THP分层课程体系）
-- =====================================================

INSERT INTO `courses` (`id`, `title`, `content_url`, `sort_order`, `level`, `description`, `status`, `created_at`) VALUES
('c-001', '围产期抑郁概述', '/courses/l1-overview.pdf', 1, 'L1', '了解围产期抑郁的定义、流行病学数据和社会影响', 'published', NOW()),
('c-002', '围产期抑郁的识别与筛查', '/courses/l1-screening.pdf', 2, 'L1', '学习使用EPDS量表进行抑郁筛查的方法和技巧', 'published', NOW()),
('c-003', '基础沟通技巧', '/courses/l1-communication.pdf', 3, 'L1', '掌握与围产期女性沟通的基本原则和技巧', 'published', NOW()),
('c-004', '心理支持技术', '/courses/l2-support.pdf', 4, 'L2', '学习提供情感支持和心理疏导的专业技术', 'published', NOW()),
('c-005', '危机干预基础', '/courses/l2-crisis.pdf', 5, 'L2', '识别自杀风险信号，掌握初步危机干预方法', 'published', NOW()),
('c-006', '家庭支持系统评估', '/courses/l2-family.pdf', 6, 'L2', '评估和动员家庭支持资源的方法', 'published', NOW()),
('c-007', '认知行为疗法入门', '/courses/l3-cbt.pdf', 7, 'L3', 'CBT基本原理及在围产期抑郁中的应用', 'published', NOW()),
('c-008', '药物治疗知识', '/courses/l3-medication.pdf', 8, 'L3', '了解围产期抑郁的药物治疗方案和注意事项', 'published', NOW()),
('c-009', '多学科协作', '/courses/l4-mdt.pdf', 9, 'L4', '与精神科、产科等多学科团队协作的方法', 'published', NOW()),
('c-010', '案例督导与反思', '/courses/l4-supervision.pdf', 10, 'L4', '通过案例分析提升临床决策能力', 'published', NOW());

-- =====================================================
-- 3. 虚拟患者场景数据
-- =====================================================

INSERT INTO `scenarios` (`id`, `title`, `description`, `system_prompt`, `patient_background`, `knowledge_tags`, `difficulty`, `time_period`, `status`, `created_at`) VALUES
('s-001', '产后情绪低落初筛', '模拟与一位产后2周的新妈妈进行首次情绪筛查对话', 
'你是一位产后2周的新妈妈，名叫小美，28岁，第一胎。你最近感觉很疲惫，睡眠不好，有时候会莫名其妙地想哭。你对照顾宝宝感到焦虑，担心自己做得不够好。你愿意和护士交流，但不太确定自己的感受是否正常。请根据护士的问题自然地回应，表达你的真实感受。',
'小美，28岁，已婚，大学本科学历，会计。丈夫在外地工作，婆婆帮忙照顾月子。顺产，母乳喂养。产前无抑郁史。',
'EPDS筛查,产后情绪,初次访谈', 1, '产后2周', 'published', NOW()),

('s-002', '轻度抑郁情绪支持', '模拟与一位EPDS评分12分的产妇进行心理支持对话',
'你是一位产后6周的妈妈，名叫小丽，32岁。你的EPDS筛查评分是12分。你经常感到疲惫和无助，对很多事情失去兴趣，包括照顾宝宝。你有时会责怪自己不是一个好妈妈。你的丈夫很忙，你感到很孤独。你希望有人能理解你的感受。',
'小丽，32岁，已婚，研究生学历，教师（产假中）。丈夫是程序员，工作繁忙。剖宫产，混合喂养。孕期有轻度焦虑。',
'心理支持,情绪疏导,EPDS中度', 2, '产后6周', 'published', NOW()),

('s-003', '家庭支持不足的产妇', '模拟与一位缺乏家庭支持的产妇进行深入沟通',
'你是一位产后3个月的单亲妈妈，名叫小芳，26岁。你独自照顾宝宝，父母在外地，前男友不负责任。你感到非常疲惫和绝望，有时候会想"如果没有我，宝宝会不会过得更好"。但你很爱宝宝，不想伤害他。你需要帮助但不知道该向谁求助。',
'小芳，26岁，未婚单亲，高中学历，超市收银员（已辞职）。父母在农村，关系一般。顺产，母乳喂养。经济压力大。',
'家庭评估,社会支持,单亲妈妈,轻度自杀意念', 3, '产后3个月', 'published', NOW()),

('s-004', '拒绝承认问题的产妇', '模拟与一位否认自己有问题的产妇进行沟通',
'你是一位产后2个月的妈妈，名叫小雯，35岁，二胎。你是一个要强的人，认为自己必须做一个完美的妈妈。虽然你经常失眠、食欲不振、对大宝发脾气，但你坚持认为这些都是正常的，不需要帮助。你对护士的关心有些抵触，觉得她们小题大做。',
'小雯，35岁，已婚，硕士学历，企业高管。丈夫是医生。二胎剖宫产，大宝5岁。追求完美，不愿示弱。',
'否认心理,动机访谈,完美主义', 3, '产后2个月', 'published', NOW()),

('s-005', '严重抑郁伴自杀风险', '模拟与一位有自杀意念的产妇进行危机干预',
'你是一位产后4周的妈妈，名叫小琳，30岁。你感到极度绝望，觉得自己是个失败者，是家人的负担。你已经好几天没有好好吃饭和睡觉了。你有时会想到死亡，觉得如果自己不在了，大家都会轻松一些。你还没有具体的计划，但这些想法越来越频繁。你今天愿意和护士谈谈。',
'小琳，30岁，已婚，本科学历，全职妈妈。丈夫经常出差。难产后剖宫产，宝宝曾住NICU一周。有产前抑郁史，曾服用抗抑郁药。',
'危机干预,自杀评估,安全计划,紧急转介', 5, '产后4周', 'published', NOW());

-- =====================================================
-- 4. 菜单数据
-- =====================================================

INSERT INTO `menus` (`id`, `parent_id`, `title`, `icon`, `path`, `component`, `sort_order`, `is_visible`, `is_enabled`) VALUES
('m-001', NULL, '课程中心', 'BookOutlined', '/courses', 'CourseListPage', 1, 1, 1),
('m-002', NULL, '情景模拟', 'SimulationOutlined', '/scenarios', 'ScenarioListPage', 2, 1, 1),
('m-004', NULL, '学习进度', 'LineChartOutlined', '/progress', 'ProgressPage', 4, 1, 1),
('m-005', NULL, '系统管理', 'SettingOutlined', '/admin', 'AdminLayout', 100, 1, 1),
('m-005-01', 'm-005', '用户管理', 'UserOutlined', '/admin/users', 'UserManagePage', 1, 1, 1),
('m-005-02', 'm-005', '角色管理', 'TeamOutlined', '/admin/roles', 'RoleManagePage', 2, 1, 1),
('m-005-03', 'm-005', '菜单管理', 'MenuOutlined', '/admin/menus', 'MenuManagePage', 3, 1, 1),
('m-005-04', 'm-005', '机构管理', 'BankOutlined', '/admin/organizations', 'OrganizationPage', 4, 1, 1),
('m-005-05', 'm-005', '班级管理', 'TeamOutlined', '/admin/classes', 'TrainingClassPage', 5, 1, 1),
('m-005-06', 'm-005', '题库管理', 'FileTextOutlined', '/admin/questions', 'QuestionBankPage', 6, 1, 1),
('m-005-07', 'm-005', '证书管理', 'TrophyOutlined', '/admin/certificates', 'CertificatePage', 7, 1, 1),
('m-006', NULL, '个人中心', 'UserOutlined', '/profile', 'ProfilePage', 5, 1, 1);

-- =====================================================
-- 5. 角色数据
-- =====================================================

INSERT INTO `roles` (`id`, `code`, `name`, `description`, `scope`, `created_at`) VALUES
('r-001', 'admin', '系统管理员', '拥有系统所有权限，可管理用户、角色、机构等', 'system', NOW()),
('r-002', 'instructor', '讲师', '可查看课程、场景和学员进度，可管理教学内容', 'system', NOW()),
('r-003', 'student', '学员', '可学习课程、进行情景模拟、查看个人进度', 'system', NOW());

-- =====================================================
-- 6. 角色菜单权限数据
-- =====================================================

INSERT INTO `role_menu_permissions` (`id`, `role_code`, `menu_id`, `can_view`) VALUES
-- 学员权限
('p-001', 'student', 'm-001', 1),
('p-002', 'student', 'm-002', 1),
('p-004', 'student', 'm-004', 1),
('p-005', 'student', 'm-006', 1),
-- 讲师权限
('p-011', 'instructor', 'm-001', 1),
('p-012', 'instructor', 'm-002', 1),
('p-014', 'instructor', 'm-004', 1),
('p-015', 'instructor', 'm-006', 1),
-- 管理员权限（全部）
('p-021', 'admin', 'm-001', 1),
('p-022', 'admin', 'm-002', 1),
('p-024', 'admin', 'm-004', 1),
('p-025', 'admin', 'm-005', 1),
('p-026', 'admin', 'm-005-01', 1),
('p-027', 'admin', 'm-005-02', 1),
('p-028', 'admin', 'm-005-03', 1),
('p-029', 'admin', 'm-005-04', 1),
('p-030', 'admin', 'm-005-05', 1),
('p-031', 'admin', 'm-005-06', 1),
('p-032', 'admin', 'm-005-07', 1),
('p-033', 'admin', 'm-006', 1);

SET FOREIGN_KEY_CHECKS = 1;

-- 数据导入完成
SELECT '✅ 模拟数据导入成功！' AS message;
SELECT '用户: 5个, 课程: 10个, 场景: 5个, 菜单: 12个' AS summary;
SELECT '默认账号: admin@panda.com / admin123' AS admin_account;
SELECT '默认账号: teacher@panda.com / admin123' AS teacher_account;
SELECT '默认账号: nurse1@hospital.com / admin123' AS student_account;
