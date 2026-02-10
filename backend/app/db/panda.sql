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
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_logs` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '日志ID',
  `user_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作用户',
  `org_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '机构ID',
  `action` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作',
  `resource_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '资源类型',
  `resource_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '资源ID',
  `changes` json DEFAULT NULL COMMENT '变更内容',
  `ip_address` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'IP地址',
  `user_agent` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户代理',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_org` (`org_id`),
  KEY `idx_resource` (`resource_type`,`resource_id`),
  KEY `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificate_templates`
--

DROP TABLE IF EXISTS `certificate_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificate_templates` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板ID',
  `org_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '机构ID',
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模板名称',
  `template_config` json DEFAULT NULL COMMENT '模板配置(JSON)',
  `status` enum('active','inactive') COLLATE utf8mb4_unicode_ci DEFAULT 'active' COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_org` (`org_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='证书模板表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificate_templates`
--

LOCK TABLES `certificate_templates` WRITE;
/*!40000 ALTER TABLE `certificate_templates` DISABLE KEYS */;
/*!40000 ALTER TABLE `certificate_templates` ENABLE KEYS */;
UNLOCK TABLES;

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
  `org_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '机构ID',
  `class_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '班级ID',
  `template_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '模板ID',
  `status` enum('valid','revoked') COLLATE utf8mb4_unicode_ci DEFAULT 'valid' COMMENT '状态',
  `revoked_at` datetime DEFAULT NULL COMMENT '撤销时间',
  `revoked_by` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '撤销人',
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
-- Table structure for table `class_students`
--

DROP TABLE IF EXISTS `class_students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_students` (
  `class_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班级ID',
  `user_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '学员ID',
  `joined_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  `status` enum('active','completed','dropped') COLLATE utf8mb4_unicode_ci DEFAULT 'active' COMMENT '状态',
  PRIMARY KEY (`class_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `class_students_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `training_classes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `class_students_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级学员关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_students`
--

LOCK TABLES `class_students` WRITE;
/*!40000 ALTER TABLE `class_students` DISABLE KEYS */;
INSERT INTO `class_students` VALUES ('class-001','u-student-001','2026-02-10 17:59:17','active'),('class-001','u-student-002','2026-02-10 17:59:17','active'),('class-001','u-student-003','2026-02-10 17:59:17','active');
/*!40000 ALTER TABLE `class_students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_tasks`
--

DROP TABLE IF EXISTS `class_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_tasks` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '任务ID',
  `class_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班级ID',
  `resource_type` enum('course','scenario','exam') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '资源类型',
  `resource_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '资源ID',
  `resource_version` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '资源版本',
  `deadline` datetime DEFAULT NULL COMMENT '截止日期',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_class` (`class_id`),
  CONSTRAINT `class_tasks_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `training_classes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='班级任务表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_tasks`
--

LOCK TABLES `class_tasks` WRITE;
/*!40000 ALTER TABLE `class_tasks` DISABLE KEYS */;
INSERT INTO `class_tasks` VALUES ('task-001','class-001','course','c-001','1.0.0','2025-03-10 23:59:59',1,'2026-02-10 17:59:17'),('task-002','class-001','scenario','s-001','1.0.0','2025-03-20 23:59:59',2,'2026-02-10 17:59:17');
/*!40000 ALTER TABLE `class_tasks` ENABLE KEYS */;
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
  `org_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '机构ID',
  `scope` enum('private','platform','shared') COLLATE utf8mb4_unicode_ci DEFAULT 'private' COMMENT '发布范围',
  `version` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '1.0.0' COMMENT '版本号',
  `version_notes` text COLLATE utf8mb4_unicode_ci COMMENT '版本说明',
  `status` enum('draft','pending','published','archived') COLLATE utf8mb4_unicode_ci DEFAULT 'draft' COMMENT '状态',
  `published_at` datetime DEFAULT NULL COMMENT '发布时间',
  `published_by` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发布人',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_level` (`level`),
  KEY `idx_sort` (`sort_order`),
  KEY `idx_courses_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='THP分层课程表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES ('c-001','围产期抑郁概述','/courses/l1-overview.pdf',NULL,1,'L1','了解围产期抑郁的定义、流行病学数据和社会影响','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:55'),('c-002','围产期抑郁的识别与筛查','/courses/l1-screening.pdf',NULL,2,'L1','学习使用EPDS量表进行抑郁筛查的方法和技巧','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:55'),('c-003','基础沟通技巧','/courses/l1-communication.pdf',NULL,3,'L1','掌握与围产期女性沟通的基本原则和技巧','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:55'),('c-004','心理支持技术','/courses/l2-support.pdf',NULL,4,'L2','学习提供情感支持和心理疏导的专业技术','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:55'),('c-005','危机干预基础','/courses/l2-crisis.pdf',NULL,5,'L2','识别自杀风险信号，掌握初步危机干预方法','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:55'),('c-006','家庭支持系统评估','/courses/l2-family.pdf',NULL,6,'L2','评估和动员家庭支持资源的方法','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:55'),('c-007','认知行为疗法入门','/courses/l3-cbt.pdf',NULL,7,'L3','CBT基本原理及在围产期抑郁中的应用','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:55'),('c-008','药物治疗知识','/courses/l3-medication.pdf',NULL,8,'L3','了解围产期抑郁的药物治疗方案和注意事项','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:55'),('c-009','多学科协作','/courses/l4-mdt.pdf',NULL,9,'L4','与精神科、产科等多学科团队协作的方法','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:55'),('c-010','案例督导与反思','/courses/l4-supervision.pdf',NULL,10,'L4','通过案例分析提升临床决策能力','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:55');
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
  `error_message` text COMMENT '错误信息（生成失败时）',
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
INSERT INTO `menus` VALUES ('m-001',NULL,'课程中心','BookOutlined','/courses','CourseListPage',1,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-002',NULL,'情景模拟','SimulationOutlined','/scenarios','ScenarioListPage',2,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-004',NULL,'学习进度','LineChartOutlined','/progress','ProgressPage',4,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-005',NULL,'系统管理','SettingOutlined','/admin','AdminLayout',100,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-005-01','m-005','用户管理','UserOutlined','/admin/users','UserManagePage',1,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-005-02','m-005','角色管理','TeamOutlined','/admin/roles','RoleManagePage',2,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-005-03','m-005','菜单管理','MenuOutlined','/admin/menus','MenuManagePage',3,1,1,'2026-01-27 21:57:47','2026-01-27 21:57:47'),('m-005-04','m-005','机构管理','BankOutlined','/admin/organizations','OrganizationPage',4,1,1,'2026-02-10 17:59:17','2026-02-10 17:59:17'),('m-005-05','m-005','培训班级','TeamOutlined','/admin/classes','TrainingClassPage',5,1,1,'2026-02-10 17:59:17','2026-02-10 17:59:17'),('m-005-06','m-005','题库管理','BookOutlined','/admin/questions','QuestionBankPage',6,1,1,'2026-02-10 17:59:17','2026-02-10 17:59:17'),('m-005-07','m-005','证书管理','TrophyOutlined','/admin/certificates','CertificatePage',7,1,1,'2026-02-10 17:59:17','2026-02-10 17:59:17'),('m-006',NULL,'个人中心','UserOutlined','/profile','ProfilePage',5,1,1,'2026-01-27 22:51:08','2026-01-27 22:51:08');
/*!40000 ALTER TABLE `menus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizations`
--

DROP TABLE IF EXISTS `organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organizations` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '机构ID',
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '机构名称',
  `short_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '简称',
  `logo_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'LOGO',
  `contact_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系人',
  `contact_phone` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系电话',
  `contact_email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系邮箱',
  `valid_until` datetime DEFAULT NULL COMMENT '有效期',
  `status` enum('active','inactive') COLLATE utf8mb4_unicode_ci DEFAULT 'active' COMMENT '状态',
  `config` json DEFAULT NULL COMMENT '机构配置(证书/导出/语音/防作弊开关)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='机构表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizations`
--

LOCK TABLES `organizations` WRITE;
/*!40000 ALTER TABLE `organizations` DISABLE KEYS */;
INSERT INTO `organizations` VALUES ('org-hospital-001','第一人民医院','一院',NULL,'张主任','010-12345678','zhang@hospital1.com',NULL,'active','{\"voice\": true, \"export\": true, \"anti_cheat\": false, \"certificate\": true}','2026-02-10 17:59:16','2026-02-10 17:59:16'),('org-hospital-002','第二人民医院','二院',NULL,'李主任','010-87654321','li@hospital2.com',NULL,'active','{\"voice\": false, \"export\": false, \"anti_cheat\": true, \"certificate\": true}','2026-02-10 17:59:16','2026-02-10 17:59:16'),('org-hospital-003','妇幼保健院','妇幼',NULL,'王主任','010-11223344','wang@mch.com',NULL,'active','{\"voice\": true, \"export\": true, \"anti_cheat\": true, \"certificate\": true}','2026-02-10 17:59:16','2026-02-10 17:59:16'),('org-platform-001','平台机构','平台',NULL,'平台管理员','400-000-0000','platform@panda.com',NULL,'active','{\"voice\": true, \"export\": true, \"anti_cheat\": true, \"certificate\": true}','2026-02-10 17:59:16','2026-02-10 17:59:16');
/*!40000 ALTER TABLE `organizations` ENABLE KEYS */;
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
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限ID',
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限代码',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限名称',
  `module` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模块',
  `action` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '权限说明',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_code` (`code`),
  KEY `idx_module` (`module`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限点表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES ('perm-audit-export','audit:export','导出审计日志','audit','export','导出审计日志','2026-02-10 17:59:17'),('perm-audit-view','audit:view','查看审计日志','audit','view','查看审计日志','2026-02-10 17:59:17'),('perm-certificate-issue','certificate:issue','发放证书','certificate','issue','发放证书','2026-02-10 17:59:17'),('perm-certificate-revoke','certificate:revoke','撤销证书','certificate','revoke','撤销证书','2026-02-10 17:59:17'),('perm-certificate-view','certificate:view','查看证书','certificate','view','查看证书列表','2026-02-10 17:59:17'),('perm-class-create','class:create','创建班级','class','create','创建新班级','2026-02-10 17:59:17'),('perm-class-edit','class:edit','编辑班级','class','edit','编辑班级信息','2026-02-10 17:59:17'),('perm-class-export','class:export','导出班级','class','export','导出班级数据','2026-02-10 17:59:17'),('perm-class-publish','class:publish','发布班级','class','publish','发布班级','2026-02-10 17:59:17'),('perm-class-view','class:view','查看班级','class','view','查看班级列表和信息','2026-02-10 17:59:17'),('perm-course-archive','course:archive','下线课程','course','archive','下线课程','2026-02-10 17:59:17'),('perm-course-create','course:create','创建课程','course','create','创建新课程','2026-02-10 17:59:17'),('perm-course-edit','course:edit','编辑课程','course','edit','编辑课程内容','2026-02-10 17:59:17'),('perm-course-export','course:export','导出课程','course','export','导出课程数据','2026-02-10 17:59:17'),('perm-course-publish','course:publish','发布课程','course','publish','发布课程','2026-02-10 17:59:17'),('perm-course-view','course:view','查看课程','course','view','查看课程列表和详情','2026-02-10 17:59:17'),('perm-evaluation-export','evaluation:export','导出评估','evaluation','export','导出评估数据','2026-02-10 17:59:17'),('perm-evaluation-view','evaluation:view','查看评估','evaluation','view','查看评估报告','2026-02-10 17:59:17'),('perm-org-create','org:create','创建机构','org','create','创建新机构','2026-02-10 17:59:17'),('perm-org-delete','org:delete','删除机构','org','delete','删除机构','2026-02-10 17:59:17'),('perm-org-edit','org:edit','编辑机构','org','edit','编辑机构信息','2026-02-10 17:59:17'),('perm-org-view','org:view','查看机构','org','view','查看机构信息','2026-02-10 17:59:17'),('perm-question-create','question:create','创建题目','question','create','创建新题目','2026-02-10 17:59:17'),('perm-question-delete','question:delete','删除题目','question','delete','删除题目','2026-02-10 17:59:17'),('perm-question-edit','question:edit','编辑题目','question','edit','编辑题目','2026-02-10 17:59:17'),('perm-question-import','question:import','导入题目','question','import','批量导入题目','2026-02-10 17:59:17'),('perm-question-view','question:view','查看题目','question','view','查看题目列表','2026-02-10 17:59:17'),('perm-scenario-archive','scenario:archive','下线场景','scenario','archive','下线场景','2026-02-10 17:59:17'),('perm-scenario-create','scenario:create','创建场景','scenario','create','创建新场景','2026-02-10 17:59:17'),('perm-scenario-edit','scenario:edit','编辑场景','scenario','edit','编辑场景','2026-02-10 17:59:17'),('perm-scenario-publish','scenario:publish','发布场景','scenario','publish','发布场景','2026-02-10 17:59:17'),('perm-scenario-view','scenario:view','查看场景','scenario','view','查看场景列表','2026-02-10 17:59:17'),('perm-user-create','user:create','创建用户','user','create','创建新用户','2026-02-10 17:59:17'),('perm-user-delete','user:delete','删除用户','user','delete','删除用户','2026-02-10 17:59:17'),('perm-user-edit','user:edit','编辑用户','user','edit','编辑用户信息','2026-02-10 17:59:17'),('perm-user-export','user:export','导出用户','user','export','导出用户数据','2026-02-10 17:59:17'),('perm-user-view','user:view','查看用户','user','view','查看用户列表和信息','2026-02-10 17:59:17');
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question_bank`
--

DROP TABLE IF EXISTS `question_bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question_bank` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '题目ID',
  `org_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '机构ID',
  `scope` enum('private','platform','shared') COLLATE utf8mb4_unicode_ci DEFAULT 'private' COMMENT '发布范围',
  `question_type` enum('single','multiple','judge') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '题型',
  `question_text` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '题干',
  `options` json NOT NULL COMMENT '选项',
  `correct_answer` json NOT NULL COMMENT '正确答案',
  `explanation` text COLLATE utf8mb4_unicode_ci COMMENT '解析',
  `difficulty` enum('easy','medium','hard') COLLATE utf8mb4_unicode_ci DEFAULT 'medium' COMMENT '难度',
  `knowledge_tags` json DEFAULT NULL COMMENT '知识点标签',
  `chapter_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '章节归属',
  `status` enum('draft','active','disabled') COLLATE utf8mb4_unicode_ci DEFAULT 'draft' COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_org` (`org_id`),
  KEY `idx_type` (`question_type`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='题库表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question_bank`
--

LOCK TABLES `question_bank` WRITE;
/*!40000 ALTER TABLE `question_bank` DISABLE KEYS */;
/*!40000 ALTER TABLE `question_bank` ENABLE KEYS */;
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
  `role` enum('student','instructor','admin') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色',
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
INSERT INTO `role_menu_permissions` VALUES ('p-001','student','m-001',1,'2026-01-27 21:57:47'),('p-002','student','m-002',1,'2026-01-27 21:57:47'),('p-004','student','m-004',1,'2026-01-27 21:57:47'),('p-005','student','m-006',1,'2026-01-27 22:51:08'),('p-011','instructor','m-001',1,'2026-01-27 21:57:47'),('p-012','instructor','m-002',1,'2026-01-27 21:57:47'),('p-014','instructor','m-004',1,'2026-01-27 21:57:47'),('p-015','instructor','m-006',1,'2026-01-27 22:51:08'),('p-021','admin','m-001',1,'2026-01-27 21:57:47'),('p-022','admin','m-002',1,'2026-01-27 21:57:47'),('p-024','admin','m-004',1,'2026-01-27 21:57:47'),('p-025','admin','m-005',1,'2026-01-27 21:57:47'),('p-026','admin','m-005-01',1,'2026-01-27 21:57:47'),('p-027','admin','m-005-02',1,'2026-01-27 21:57:47'),('p-028','admin','m-005-03',1,'2026-01-27 21:57:47'),('p-029','admin','m-006',1,'2026-01-27 22:51:08'),('rmp-029','admin','m-005-04',1,'2026-02-10 17:59:17'),('rmp-030','admin','m-005-05',1,'2026-02-10 17:59:17'),('rmp-031','admin','m-005-06',1,'2026-02-10 17:59:17'),('rmp-032','admin','m-005-07',1,'2026-02-10 17:59:17');
/*!40000 ALTER TABLE `role_menu_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permissions`
--

DROP TABLE IF EXISTS `role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permissions` (
  `role_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色ID',
  `permission_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '权限ID',
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `role_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `role_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permissions`
--

LOCK TABLES `role_permissions` WRITE;
/*!40000 ALTER TABLE `role_permissions` DISABLE KEYS */;
INSERT INTO `role_permissions` VALUES ('role-auditor','perm-audit-export'),('role-org-admin','perm-audit-export'),('role-super-admin','perm-audit-export'),('role-auditor','perm-audit-view'),('role-org-admin','perm-audit-view'),('role-super-admin','perm-audit-view'),('role-org-admin','perm-certificate-issue'),('role-super-admin','perm-certificate-issue'),('role-trainer','perm-certificate-issue'),('role-org-admin','perm-certificate-revoke'),('role-super-admin','perm-certificate-revoke'),('role-org-admin','perm-certificate-view'),('role-super-admin','perm-certificate-view'),('role-trainer','perm-certificate-view'),('role-org-admin','perm-class-create'),('role-super-admin','perm-class-create'),('role-trainer','perm-class-create'),('role-org-admin','perm-class-edit'),('role-super-admin','perm-class-edit'),('role-trainer','perm-class-edit'),('role-org-admin','perm-class-export'),('role-super-admin','perm-class-export'),('role-org-admin','perm-class-publish'),('role-super-admin','perm-class-publish'),('role-trainer','perm-class-publish'),('role-org-admin','perm-class-view'),('role-super-admin','perm-class-view'),('role-trainer','perm-class-view'),('role-org-admin','perm-course-archive'),('role-super-admin','perm-course-archive'),('role-content-editor','perm-course-create'),('role-org-admin','perm-course-create'),('role-super-admin','perm-course-create'),('role-content-editor','perm-course-edit'),('role-org-admin','perm-course-edit'),('role-super-admin','perm-course-edit'),('role-org-admin','perm-course-export'),('role-super-admin','perm-course-export'),('role-org-admin','perm-course-publish'),('role-super-admin','perm-course-publish'),('role-content-editor','perm-course-view'),('role-org-admin','perm-course-view'),('role-super-admin','perm-course-view'),('role-org-admin','perm-evaluation-export'),('role-super-admin','perm-evaluation-export'),('role-auditor','perm-evaluation-view'),('role-org-admin','perm-evaluation-view'),('role-super-admin','perm-evaluation-view'),('role-trainer','perm-evaluation-view'),('role-super-admin','perm-org-create'),('role-super-admin','perm-org-delete'),('role-org-admin','perm-org-edit'),('role-super-admin','perm-org-edit'),('role-org-admin','perm-org-view'),('role-super-admin','perm-org-view'),('role-content-editor','perm-question-create'),('role-org-admin','perm-question-create'),('role-super-admin','perm-question-create'),('role-org-admin','perm-question-delete'),('role-super-admin','perm-question-delete'),('role-content-editor','perm-question-edit'),('role-org-admin','perm-question-edit'),('role-super-admin','perm-question-edit'),('role-org-admin','perm-question-import'),('role-super-admin','perm-question-import'),('role-content-editor','perm-question-view'),('role-org-admin','perm-question-view'),('role-super-admin','perm-question-view'),('role-org-admin','perm-scenario-archive'),('role-super-admin','perm-scenario-archive'),('role-content-editor','perm-scenario-create'),('role-org-admin','perm-scenario-create'),('role-super-admin','perm-scenario-create'),('role-content-editor','perm-scenario-edit'),('role-org-admin','perm-scenario-edit'),('role-super-admin','perm-scenario-edit'),('role-org-admin','perm-scenario-publish'),('role-super-admin','perm-scenario-publish'),('role-content-editor','perm-scenario-view'),('role-org-admin','perm-scenario-view'),('role-super-admin','perm-scenario-view'),('role-org-admin','perm-user-create'),('role-super-admin','perm-user-create'),('role-org-admin','perm-user-delete'),('role-super-admin','perm-user-delete'),('role-org-admin','perm-user-edit'),('role-super-admin','perm-user-edit'),('role-org-admin','perm-user-export'),('role-super-admin','perm-user-export'),('role-org-admin','perm-user-view'),('role-super-admin','perm-user-view'),('role-trainer','perm-user-view');
/*!40000 ALTER TABLE `role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色ID',
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色代码',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色名称',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '角色说明',
  `scope` enum('system','org') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'org',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES ('role-auditor','auditor','审计/质控','只读查看日志、版本变更、评分命中与复盘报告','org','2026-02-10 17:59:17'),('role-content-editor','content_editor','内容编辑','维护课程/题库/场景脚本/评分规则（只在授权范围内）','org','2026-02-10 17:59:17'),('role-org-admin','org_admin','机构管理员','管理本机构用户、班级、证书、数据导出、机构配置','org','2026-02-10 17:59:17'),('role-super-admin','super_admin','平台超级管理员','管理所有机构、系统级配置、全局模板与字典项','system','2026-02-10 17:59:17'),('role-trainer','trainer','培训导师/带教','建班、分配任务、查看学习与考核结果、点评','org','2026-02-10 17:59:17');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
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
  `org_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '机构ID',
  `scope` enum('private','platform','shared') COLLATE utf8mb4_unicode_ci DEFAULT 'private' COMMENT '发布范围',
  `version` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT '1.0.0' COMMENT '版本号',
  `version_notes` text COLLATE utf8mb4_unicode_ci COMMENT '版本说明',
  `status` enum('draft','pending','published','archived') COLLATE utf8mb4_unicode_ci DEFAULT 'draft' COMMENT '状态',
  `published_at` datetime DEFAULT NULL COMMENT '发布时间',
  `published_by` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发布人',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_difficulty` (`difficulty`),
  KEY `idx_scenarios_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='虚拟患者场景配置表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scenarios`
--

LOCK TABLES `scenarios` WRITE;
/*!40000 ALTER TABLE `scenarios` DISABLE KEYS */;
INSERT INTO `scenarios` VALUES ('s-001','产后情绪低落初筛','模拟与一位产后2周的新妈妈进行首次情绪筛查对话','你是一位产后2周的新妈妈，名叫小美，28岁，第一胎。你最近感觉很疲惫，睡眠不好，有时候会莫名其妙地想哭。你对照顾宝宝感到焦虑，担心自己做得不够好。你愿意和护士交流，但不太确定自己的感受是否正常。请根据护士的问题自然地回应，表达你的真实感受。','小美，28岁，已婚，大学本科学历，会计。丈夫在外地工作，婆婆帮忙照顾月子。顺产，母乳喂养。产前无抑郁史。','EPDS筛查,产后情绪,初次访谈',1,'产后2周','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:56'),('s-002','轻度抑郁情绪支持','模拟与一位EPDS评分12分的产妇进行心理支持对话','你是一位产后6周的妈妈，名叫小丽，32岁。你的EPDS筛查评分是12分。你经常感到疲惫和无助，对很多事情失去兴趣，包括照顾宝宝。你有时会责怪自己不是一个好妈妈。你的丈夫很忙，你感到很孤独。你希望有人能理解你的感受。','小丽，32岁，已婚，研究生学历，教师（产假中）。丈夫是程序员，工作繁忙。剖宫产，混合喂养。孕期有轻度焦虑。','心理支持,情绪疏导,EPDS中度',2,'产后6周','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:56'),('s-003','家庭支持不足的产妇','模拟与一位缺乏家庭支持的产妇进行深入沟通','你是一位产后3个月的单亲妈妈，名叫小芳，26岁。你独自照顾宝宝，父母在外地，前男友不负责任。你感到非常疲惫和绝望，有时候会想\"如果没有我，宝宝会不会过得更好\"。但你很爱宝宝，不想伤害他。你需要帮助但不知道该向谁求助。','小芳，26岁，未婚单亲，高中学历，超市收银员（已辞职）。父母在农村，关系一般。顺产，母乳喂养。经济压力大。','家庭评估,社会支持,单亲妈妈,轻度自杀意念',3,'产后3个月','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:56'),('s-004','拒绝承认问题的产妇','模拟与一位否认自己有问题的产妇进行沟通','你是一位产后2个月的妈妈，名叫小雯，35岁，二胎。你是一个要强的人，认为自己必须做一个完美的妈妈。虽然你经常失眠、食欲不振、对大宝发脾气，但你坚持认为这些都是正常的，不需要帮助。你对护士的关心有些抵触，觉得她们小题大做。','小雯，35岁，已婚，硕士学历，企业高管。丈夫是医生。二胎剖宫产，大宝5岁。追求完美，不愿示弱。','否认心理,动机访谈,完美主义',3,'产后2个月','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:56'),('s-005','严重抑郁伴自杀风险','模拟与一位有自杀意念的产妇进行危机干预','你是一位产后4周的妈妈，名叫小琳，30岁。你感到极度绝望，觉得自己是个失败者，是家人的负担。你已经好几天没有好好吃饭和睡觉了。你有时会想到死亡，觉得如果自己不在了，大家都会轻松一些。你还没有具体的计划，但这些想法越来越频繁。你今天愿意和护士谈谈。','小琳，30岁，已婚，本科学历，全职妈妈。丈夫经常出差。难产后剖宫产，宝宝曾住NICU一周。有产前抑郁史，曾服用抗抑郁药。','危机干预,自杀评估,安全计划,紧急转介',5,'产后4周','2025-01-01 00:00:00',NULL,'private','1.0.0',NULL,'draft',NULL,NULL,'2026-02-10 17:58:56');
/*!40000 ALTER TABLE `scenarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `training_classes`
--

DROP TABLE IF EXISTS `training_classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `training_classes` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班级ID',
  `org_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '机构ID',
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '班级名称',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '描述',
  `start_date` datetime DEFAULT NULL COMMENT '开始时间',
  `end_date` datetime DEFAULT NULL COMMENT '结束时间',
  `trainer_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '负责人ID',
  `credit_rule` json DEFAULT NULL COMMENT '学分规则',
  `completion_rule` json DEFAULT NULL COMMENT '结业标准',
  `status` enum('draft','active','completed','archived') COLLATE utf8mb4_unicode_ci DEFAULT 'draft' COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_org` (`org_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `training_classes_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organizations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='培训班级表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `training_classes`
--

LOCK TABLES `training_classes` WRITE;
/*!40000 ALTER TABLE `training_classes` DISABLE KEYS */;
INSERT INTO `training_classes` VALUES ('class-001','org-hospital-001','2025年第一季度围产期护理培训','面向一院新入职护士的系统培训','2025-03-01 09:00:00','2025-03-31 18:00:00','u-trainer-001',NULL,NULL,'active','2026-02-10 17:59:17','2026-02-10 17:59:17'),('class-002','org-hospital-002','2025年第二季度围产期护理培训','二院季度培训班','2025-04-01 09:00:00','2025-04-30 18:00:00','u-trainer-003',NULL,NULL,'draft','2026-02-10 17:59:17','2026-02-10 17:59:17');
/*!40000 ALTER TABLE `training_classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_organizations`
--

DROP TABLE IF EXISTS `user_organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_organizations` (
  `user_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `org_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '机构ID',
  `role_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色ID',
  `status` enum('active','inactive') COLLATE utf8mb4_unicode_ci DEFAULT 'active' COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`user_id`,`org_id`),
  KEY `role_id` (`role_id`),
  KEY `idx_org` (`org_id`),
  KEY `idx_user` (`user_id`),
  CONSTRAINT `user_organizations_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organizations` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_organizations_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户机构关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_organizations`
--

LOCK TABLES `user_organizations` WRITE;
/*!40000 ALTER TABLE `user_organizations` DISABLE KEYS */;
INSERT INTO `user_organizations` VALUES ('u-admin-001','org-platform-001','role-super-admin','active','2026-02-10 17:59:17'),('u-content-editor-001','org-hospital-001','role-content-editor','active','2026-02-10 17:59:17'),('u-org-admin-001','org-hospital-001','role-org-admin','active','2026-02-10 17:59:17'),('u-org-admin-002','org-hospital-002','role-org-admin','active','2026-02-10 17:59:17'),('u-student-001','org-hospital-001','role-trainer','active','2026-02-10 17:59:17'),('u-student-002','org-hospital-001','role-trainer','active','2026-02-10 17:59:17'),('u-student-003','org-hospital-001','role-trainer','active','2026-02-10 17:59:17'),('u-student-004','org-hospital-002','role-trainer','active','2026-02-10 17:59:17'),('u-student-005','org-hospital-002','role-trainer','active','2026-02-10 17:59:17'),('u-student-006','org-hospital-003','role-trainer','active','2026-02-10 17:59:17'),('u-student-007','org-hospital-003','role-trainer','active','2026-02-10 17:59:17'),('u-super-admin','org-platform-001','role-super-admin','active','2026-02-10 17:59:17'),('u-trainer-001','org-hospital-001','role-trainer','active','2026-02-10 17:59:17'),('u-trainer-002','org-hospital-001','role-trainer','active','2026-02-10 17:59:17'),('u-trainer-003','org-hospital-002','role-trainer','active','2026-02-10 17:59:17');
/*!40000 ALTER TABLE `user_organizations` ENABLE KEYS */;
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
  `role` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'student' COMMENT '角色代码（与 roles.code 对齐）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `org_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '默认机构ID',
  `phone` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '手机号',
  `department` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '科室',
  `title` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '职称',
  `employee_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '工号',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_email` (`email`),
  KEY `idx_role` (`role`),
  KEY `idx_users_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('116704c5-168c-4738-8577-65a316114a40','pandatest@panda.com','$2b$12$B5VSs3gDsnMbfnJEYjf5wOow22Ld4aGdYBztEeRHjTPlyEANQizK6','test112','student','2026-01-27 13:06:44','2026-01-30 17:27:58',NULL,NULL,NULL,NULL,NULL),('u-admin-001','admin@panda.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','系统管理员','admin','2025-01-01 00:00:00','2026-02-10 17:59:17','org-platform-001','13800000002','系统管理部','管理员','EMP002'),('u-content-editor-001','editor1@hospital1.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','编辑员1','instructor','2026-02-10 17:59:17','2026-02-10 17:59:17','org-hospital-001','13800001020','护理部','内容编辑','H001-020'),('u-instructor-001','teacher@panda.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','王老师','instructor','2025-01-01 00:00:00','2026-01-17 01:46:05',NULL,NULL,NULL,NULL,NULL),('u-instructor-002','li.instructor@panda.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','李讲师','instructor','2025-01-02 00:00:00','2026-01-17 01:46:05',NULL,NULL,NULL,NULL,NULL),('u-org-admin-001','orgadmin1@hospital1.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','张主任','admin','2026-02-10 17:59:17','2026-02-10 17:59:17','org-hospital-001','13800001001','护理部','主任','H001-001'),('u-org-admin-002','orgadmin2@hospital2.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','李主任','admin','2026-02-10 17:59:17','2026-02-10 17:59:17','org-hospital-002','13800002001','护理部','主任','H002-001'),('u-student-001','nurse1@hospital.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','张护士','student','2025-01-10 09:00:00','2026-02-10 17:59:17','org-hospital-001','13800001101','产科','护士','H001-101'),('u-student-002','nurse2@hospital.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','刘护士','student','2025-01-10 10:00:00','2026-02-10 17:59:17','org-hospital-001','13800001102','产科','护士','H001-102'),('u-student-003','nurse3@hospital.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','陈护士','student','2025-01-11 08:30:00','2026-02-10 17:59:17','org-hospital-001','13800001103','产科','护士','H001-103'),('u-student-004','test@test.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','测试用户','student','2025-01-15 00:00:00','2026-02-10 17:59:17','org-hospital-002','13800002101','产科','护士','H002-101'),('u-student-005','nurse5@hospital2.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','钱护士','student','2026-02-10 17:59:17','2026-02-10 17:59:17','org-hospital-002','13800002102','产科','护士','H002-102'),('u-student-006','nurse6@mch.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','孙护士','student','2026-02-10 17:59:17','2026-02-10 17:59:17','org-hospital-003','13800003101','产科','护士','MCH-101'),('u-student-007','nurse7@mch.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','周护士','student','2026-02-10 17:59:17','2026-02-10 17:59:17','org-hospital-003','13800003102','产科','护士','MCH-102'),('u-super-admin','superadmin@panda.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','超级管理员','admin','2026-02-10 17:59:17','2026-02-10 17:59:17','org-platform-001','13800000001','平台管理部','系统管理员','EMP001'),('u-trainer-001','trainer1@hospital1.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','王老师','instructor','2026-02-10 17:59:17','2026-02-10 17:59:17','org-hospital-001','13800001010','护理部','培训师','H001-010'),('u-trainer-002','trainer2@hospital1.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','李讲师','instructor','2026-02-10 17:59:17','2026-02-10 17:59:17','org-hospital-001','13800001011','护理部','讲师','H001-011'),('u-trainer-003','trainer3@hospital2.com','$2b$12$NwB3Vo7xBPw8rRjdpWfftOJIOD8QTLFl5H65bgcd6khNoK2cWJT2S','刘老师','instructor','2026-02-10 17:59:17','2026-02-10 17:59:17','org-hospital-002','13800002010','护理部','培训师','H002-010');
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

-- Dump completed on 2026-02-10 20:18:38
