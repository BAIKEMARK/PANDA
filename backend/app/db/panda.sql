-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: panda
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `certificates`
--

DROP TABLE IF EXISTS `certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificates` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '证书ID',
  `user_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `certificate_number` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '证书编号',
  `issue_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '颁发日期',
  `credit_hours` decimal(4,1) DEFAULT '0.0' COMMENT '学分',
  PRIMARY KEY (`id`),
  UNIQUE KEY `certificate_number` (`certificate_number`),
  KEY `idx_user` (`user_id`),
  KEY `idx_certificate_number` (`certificate_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='培训证书表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificates`
--

LOCK TABLES `certificates` WRITE;
/*!40000 ALTER TABLE `certificates` DISABLE KEYS */;
/*!40000 ALTER TABLE `certificates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_messages`
--

DROP TABLE IF EXISTS `chat_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_messages` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '消息ID',
  `session_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '会话ID',
  `role` enum('user','assistant','system') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '消息内容',
  `meta_data` json DEFAULT NULL COMMENT '消息元数据(情绪、评分等)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_session` (`session_id`),
  KEY `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='对话消息明细表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_messages`
--

LOCK TABLES `chat_messages` WRITE;
/*!40000 ALTER TABLE `chat_messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_sessions`
--

DROP TABLE IF EXISTS `chat_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_sessions` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '会话ID',
  `user_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `scenario_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '场景ID',
  `status` enum('active','completed','abandoned') COLLATE utf8mb4_unicode_ci DEFAULT 'active' COMMENT '会话状态',
  `start_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
  `end_time` datetime DEFAULT NULL COMMENT '结束时间',
  `final_score` int DEFAULT NULL COMMENT '最终得分',
  `meta_data` json DEFAULT NULL COMMENT '会话元数据',
  `has_suicide_risk` tinyint(1) DEFAULT '0' COMMENT '会话中是否检测到自杀倾向',
  `suicide_risk_alerted` tinyint(1) DEFAULT '0' COMMENT '用户是否点击了报警按钮',
  `suicide_risk_alert_time` datetime DEFAULT NULL COMMENT '报警时间',
  `suicide_risk_first_detected` datetime DEFAULT NULL COMMENT '首次检测到自杀倾向的时间',
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI对话会话记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_sessions`
--

LOCK TABLES `chat_sessions` WRITE;
/*!40000 ALTER TABLE `chat_sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '课程唯一标识符',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '课程标题',
  `content_url` text COLLATE utf8mb4_unicode_ci COMMENT '课件PDF URL',
  `video_url` text COLLATE utf8mb4_unicode_ci COMMENT '视频URL',
  `sort_order` int DEFAULT '0' COMMENT '排序顺序',
  `level` enum('L1','L2','L3','L4') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'L1' COMMENT 'THP层级',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '课程描述',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_level` (`level`),
  KEY `idx_sort` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='THP分层课程表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES ('c-001','围产期抑郁概述','/courses/l1-overview.pdf',NULL,1,'L1','了解围产期抑郁的定义、流行病学数据和社会影响','2025-01-01 00:00:00'),('c-002','围产期抑郁的识别与筛查','/courses/l1-screening.pdf',NULL,2,'L1','学习使用EPDS量表进行抑郁筛查的方法和技巧','2025-01-01 00:00:00'),('c-003','基础沟通技巧','/courses/l1-communication.pdf',NULL,3,'L1','掌握与围产期女性沟通的基本原则和技巧','2025-01-01 00:00:00'),('c-004','心理支持技术','/courses/l2-support.pdf',NULL,4,'L2','学习提供情感支持和心理疏导的专业技术','2025-01-01 00:00:00'),('c-005','危机干预基础','/courses/l2-crisis.pdf',NULL,5,'L2','识别自杀风险信号，掌握初步危机干预方法','2025-01-01 00:00:00'),('c-006','家庭支持系统评估','/courses/l2-family.pdf',NULL,6,'L2','评估和动员家庭支持资源的方法','2025-01-01 00:00:00'),('c-007','认知行为疗法入门','/courses/l3-cbt.pdf',NULL,7,'L3','CBT基本原理及在围产期抑郁中的应用','2025-01-01 00:00:00'),('c-008','药物治疗知识','/courses/l3-medication.pdf',NULL,8,'L3','了解围产期抑郁的药物治疗方案和注意事项','2025-01-01 00:00:00'),('c-009','多学科协作','/courses/l4-mdt.pdf',NULL,9,'L4','与精神科、产科等多学科团队协作的方法','2025-01-01 00:00:00'),('c-010','案例督导与反思','/courses/l4-supervision.pdf',NULL,10,'L4','通过案例分析提升临床决策能力','2025-01-01 00:00:00');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluation_reports`
--

DROP TABLE IF EXISTS `evaluation_reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluation_reports` (
  `id` char(36) NOT NULL COMMENT '报告ID',
  `session_id` char(36) NOT NULL COMMENT '会话ID',
  `status` enum('pending','generating','completed','failed') NOT NULL DEFAULT 'completed' COMMENT '报告生成状态: pending-待生成, generating-生成中, completed-已完成, failed-失败',
  `error_message` text COMMENT '错误信息（生成失败时）',
  `total_score` int DEFAULT NULL COMMENT '总分 (0-100)',
  `level_assessment` varchar(20) DEFAULT NULL COMMENT '等级评定: 优秀/良好/合格/不合格',
  `radar_a_risk_identification` int DEFAULT NULL COMMENT 'A类-风险识别能力 (0-100)',
  `radar_b_communication` int DEFAULT NULL COMMENT 'B类-沟通支持能力 (0-100)',
  `radar_c_skill_application` int DEFAULT NULL COMMENT 'C类-THP技能应用 (0-100)',
  `radar_d_safety_management` int DEFAULT NULL COMMENT 'D类-安全管理能力 (0-100)',
  `radar_e_self_efficacy` int DEFAULT NULL COMMENT 'E类-自我效能感 (0-100)',
  `state_analysis` json DEFAULT NULL COMMENT '状态变化分析数据',
  `detailed_feedback` json DEFAULT NULL COMMENT '详细反馈列表',
  `technical_guidance` text COMMENT '技术指导建议',
  `meta_data` json DEFAULT NULL COMMENT '其他元数据',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_id` (`session_id`),
  KEY `idx_session` (`session_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='评估报告表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluation_reports`
--

LOCK TABLES `evaluation_reports` WRITE;
/*!40000 ALTER TABLE `evaluation_reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `evaluation_reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menus`
--

DROP TABLE IF EXISTS `menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menus` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '菜单ID',
  `parent_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '父菜单ID，NULL表示顶级菜单',
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '菜单标题',
  `icon` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '图标名称（Ant Design Icons）',
  `path` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '前端路由路径',
  `component` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '前端组件路径',
  `sort_order` int DEFAULT '0' COMMENT '排序序号，数字越小越靠前',
  `is_visible` tinyint(1) DEFAULT '1' COMMENT '是否可见（1=可见，0=隐藏）',
  `is_enabled` tinyint(1) DEFAULT '1' COMMENT '是否启用（1=启用，0=禁用）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent` (`parent_id`),
  KEY `idx_sort` (`sort_order`),
  KEY `idx_enabled` (`is_enabled`),
  CONSTRAINT `fk_menu_parent` FOREIGN KEY (`parent_id`) REFERENCES `menus` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统菜单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menus`
--

LOCK TABLES `menus` WRITE;
/*!40000 ALTER TABLE `menus` DISABLE KEYS */;
INSERT INTO `menus` VALUES ('m-001',NULL,'课程中心','BookOutlined','/courses','CourseListPage',1,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-002',NULL,'情景模拟','SimulationOutlined','/scenarios','ScenarioListPage',2,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-004',NULL,'学习进度','LineChartOutlined','/progress','ProgressPage',4,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-005',NULL,'系统管理','SettingOutlined','/admin','AdminLayout',100,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-005-01','m-005','用户管理','UserOutlined','/admin/users','UserManagePage',1,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-005-02','m-005','角色管理','TeamOutlined','/admin/roles','RoleManagePage',2,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-005-03','m-005','菜单管理','MenuOutlined','/admin/menus','MenuManagePage',3,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-006',NULL,'个人中心','UserOutlined','/profile','ProfilePage',5,1,1,'2026-01-27 22:51:08','2026-01-27 22:51:08');
/*!40000 ALTER TABLE `menus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_states`
--

DROP TABLE IF EXISTS `patient_states`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_states` (
  `session_id` char(36) NOT NULL COMMENT '会话ID',
  `mood_score` int DEFAULT '50' COMMENT '心情指数 (0-100)',
  `satisfaction_score` int DEFAULT '50' COMMENT '满意度 (0-100)',
  `depression_level` int DEFAULT '50' COMMENT '抑郁程度 (0-100)',
  `rapport_score` int DEFAULT '50' COMMENT '信任度 (0-100)',
  `message_count` int DEFAULT '0' COMMENT '对话轮次',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='患者状态表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_states`
--

LOCK TABLES `patient_states` WRITE;
/*!40000 ALTER TABLE `patient_states` DISABLE KEYS */;
/*!40000 ALTER TABLE `patient_states` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_results`
--

DROP TABLE IF EXISTS `quiz_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz_results` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '测验结果ID',
  `user_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `quiz_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '测验ID',
  `score` int NOT NULL COMMENT '得分',
  `answers` json DEFAULT NULL COMMENT '答案记录',
  `completed_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '完成时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_quiz` (`user_id`,`quiz_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测验结果表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_results`
--

LOCK TABLES `quiz_results` WRITE;
/*!40000 ALTER TABLE `quiz_results` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quizzes`
--

DROP TABLE IF EXISTS `quizzes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quizzes` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '测验ID',
  `course_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '关联课程ID',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '测验标题',
  `questions` json NOT NULL COMMENT '题目数据(JSON格式)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测验表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quizzes`
--

LOCK TABLES `quizzes` WRITE;
/*!40000 ALTER TABLE `quizzes` DISABLE KEYS */;
/*!40000 ALTER TABLE `quizzes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_menu_permissions`
--

DROP TABLE IF EXISTS `role_menu_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_menu_permissions` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限ID',
  `role` enum('student','admin','instructor') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色（基于现有users表的role枚举）',
  `menu_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '菜单ID',
  `can_view` tinyint(1) DEFAULT '1' COMMENT '是否可查看（1=可查看，0=不可查看）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_role_menu` (`role`,`menu_id`),
  KEY `idx_role` (`role`),
  KEY `idx_menu` (`menu_id`),
  CONSTRAINT `fk_rmp_menu` FOREIGN KEY (`menu_id`) REFERENCES `menus` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色菜单权限关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_menu_permissions`
--

LOCK TABLES `role_menu_permissions` WRITE;
/*!40000 ALTER TABLE `role_menu_permissions` DISABLE KEYS */;
INSERT INTO `role_menu_permissions` VALUES ('p-001','student','m-001',1,'2026-01-27 21:57:47'),('p-002','student','m-002',1,'2026-01-27 21:57:47'),('p-004','student','m-004',1,'2026-01-27 21:57:47'),('p-005','student','m-006',1,'2026-01-27 22:51:08'),('p-011','instructor','m-001',1,'2026-01-27 21:57:47'),('p-012','instructor','m-002',1,'2026-01-27 21:57:47'),('p-014','instructor','m-004',1,'2026-01-27 21:57:47'),('p-015','instructor','m-006',1,'2026-01-27 22:51:08'),('p-021','admin','m-001',1,'2026-01-27 21:57:47'),('p-022','admin','m-002',1,'2026-01-27 21:57:47'),('p-024','admin','m-004',1,'2026-01-27 21:57:47'),('p-025','admin','m-005',1,'2026-01-27 21:57:47'),('p-026','admin','m-005-01',1,'2026-01-27 21:57:47'),('p-027','admin','m-005-02',1,'2026-01-27 21:57:47'),('p-028','admin','m-005-03',1,'2026-01-27 21:57:47'),('p-029','admin','m-006',1,'2026-01-27 22:51:08');
/*!40000 ALTER TABLE `role_menu_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scenarios`
--

DROP TABLE IF EXISTS `scenarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `scenarios` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '场景唯一标识符',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '场景标题',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '场景描述',
  `system_prompt` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'AI系统提示词',
  `patient_background` text COLLATE utf8mb4_unicode_ci COMMENT '患者背景信息',
  `knowledge_tags` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '知识点标签',
  `difficulty` int DEFAULT '1' COMMENT '难度等级(1-5)',
  `time_period` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '时间节点(如:产后3天)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_difficulty` (`difficulty`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='虚拟患者场景配置表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenarios`
--

LOCK TABLES `scenarios` WRITE;
/*!40000 ALTER TABLE `scenarios` DISABLE KEYS */;
INSERT INTO `scenarios` VALUES ('s-001','产后情绪低落初筛','模拟与一位产后2周的新妈妈进行首次情绪筛查对话','你是一位产后2周的新妈妈，名叫小美，28岁，第一胎。你最近感觉很疲惫，睡眠不好，有时候会莫名其妙地想哭。你对照顾宝宝感到焦虑，担心自己做得不够好。你愿意和护士交流，但不太确定自己的感受是否正常。请根据护士的问题自然地回应，表达你的真实感受。','小美，28岁，已婚，大学本科学历，会计。丈夫在外地工作，婆婆帮忙照顾月子。顺产，母乳喂养。产前无抑郁史。','EPDS筛查,产后情绪,初次访谈',1,'产后2周','2025-01-01 00:00:00'),('s-002','轻度抑郁情绪支持','模拟与一位EPDS评分12分的产妇进行心理支持对话','你是一位产后6周的妈妈，名叫小丽，32岁。你的EPDS筛查评分是12分。你经常感到疲惫和无助，对很多事情失去兴趣，包括照顾宝宝。你有时会责怪自己不是一个好妈妈。你的丈夫很忙，你感到很孤独。你希望有人能理解你的感受。','小丽，32岁，已婚，研究生学历，教师（产假中）。丈夫是程序员，工作繁忙。剖宫产，混合喂养。孕期有轻度焦虑。','心理支持,情绪疏导,EPDS中度',2,'产后6周','2025-01-01 00:00:00'),('s-003','家庭支持不足的产妇','模拟与一位缺乏家庭支持的产妇进行深入沟通','你是一位产后3个月的单亲妈妈，名叫小芳，26岁。你独自照顾宝宝，父母在外地，前男友不负责任。你感到非常疲惫和绝望，有时候会想\"如果没有我，宝宝会不会过得更好\"。但你很爱宝宝，不想伤害他。你需要帮助但不知道该向谁求助。','小芳，26岁，未婚单亲，高中学历，超市收银员（已辞职）。父母在农村，关系一般。顺产，母乳喂养。经济压力大。','家庭评估,社会支持,单亲妈妈,轻度自杀意念',3,'产后3个月','2025-01-01 00:00:00'),('s-004','拒绝承认问题的产妇','模拟与一位否认自己有问题的产妇进行沟通','你是一位产后2个月的妈妈，名叫小雯，35岁，二胎。你是一个要强的人，认为自己必须做一个完美的妈妈。虽然你经常失眠、食欲不振、对大宝发脾气，但你坚持认为这些都是正常的，不需要帮助。你对护士的关心有些抵触，觉得她们小题大做。','小雯，35岁，已婚，硕士学历，企业高管。丈夫是医生。二胎剖宫产，大宝5岁。追求完美，不愿示弱。','否认心理,动机访谈,完美主义',3,'产后2个月','2025-01-01 00:00:00'),('s-005','严重抑郁伴自杀风险','模拟与一位有自杀意念的产妇进行危机干预','你是一位产后4周的妈妈，名叫小琳，30岁。你感到极度绝望，觉得自己是个失败者，是家人的负担。你已经好几天没有好好吃饭和睡觉了。你有时会想到死亡，觉得如果自己不在了，大家都会轻松一些。你还没有具体的计划，但这些想法越来越频繁。你今天愿意和护士谈谈。','小琳，30岁，已婚，本科学历，全职妈妈。丈夫经常出差。难产后剖宫产，宝宝曾住NICU一周。有产前抑郁史，曾服用抗抑郁药。','危机干预,自杀评估,安全计划,紧急转介',5,'产后4周','2025-01-01 00:00:00');
/*!40000 ALTER TABLE `scenarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_progress`
--

DROP TABLE IF EXISTS `user_progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_progress` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '进度记录ID',
  `user_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `course_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '课程ID',
  `is_completed` tinyint(1) DEFAULT '0' COMMENT '是否完成',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_course` (`user_id`,`course_id`),
  KEY `idx_completed` (`is_completed`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户学习进度表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_progress`
--

LOCK TABLES `user_progress` WRITE;
/*!40000 ALTER TABLE `user_progress` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_progress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一标识符(UUID)',
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码哈希',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
  `role` enum('student','admin','instructor') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'student' COMMENT '角色',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_email` (`email`),
  KEY `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('116704c5-168c-4738-8577-65a316114a40','pandatest@panda.com','$2b$12$B5VSs3gDsnMbfnJEYjf5wOow22Ld4aGdYBztEeRHjTPlyEANQizK6','test112','student','2026-01-27 13:06:44','2026-01-30 17:27:58'),('u-admin-001','admin@panda.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','系统管理员','admin','2025-01-01 00:00:00','2026-01-17 01:46:05'),('u-instructor-001','teacher@panda.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','王老师','instructor','2025-01-01 00:00:00','2026-01-17 01:46:05'),('u-instructor-002','li.instructor@panda.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','李讲师','instructor','2025-01-02 00:00:00','2026-01-17 01:46:05'),('u-student-001','nurse1@hospital.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','张护士','student','2025-01-10 09:00:00','2026-01-17 01:46:05'),('u-student-002','nurse2@hospital.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','刘护士','student','2025-01-10 10:00:00','2026-01-17 01:46:05'),('u-student-003','nurse3@hospital.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','陈护士','student','2025-01-11 08:30:00','2026-01-17 01:46:05'),('u-student-004','test@test.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','测试用户','student','2025-01-15 00:00:00','2026-01-17 01:46:05');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-05  2:28:57
