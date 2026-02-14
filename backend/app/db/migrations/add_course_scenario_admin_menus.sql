-- 添加课程管理和场景管理菜单项
INSERT INTO `menus` (`id`, `parent_id`, `title`, `icon`, `path`, `component`, `sort_order`, `is_visible`, `is_enabled`, `created_at`, `updated_at`) VALUES
('m-005-08', 'm-005', '课程管理', 'BookOutlined', '/admin/courses', 'CourseManagePage', 8, 1, 1, NOW(), NOW()),
('m-005-09', 'm-005', '场景管理', 'ExperimentOutlined', '/admin/scenarios', 'ScenarioManagePage', 9, 1, 1, NOW(), NOW());

-- 为admin角色分配课程管理和场景管理菜单权限
INSERT INTO `role_menu_permissions` (`id`, `role`, `menu_id`, `can_view`, `created_at`) VALUES
(UUID(), 'admin', 'm-005-08', 1, NOW()),
(UUID(), 'admin', 'm-005-09', 1, NOW());

-- 为content_editor角色分配课程管理和场景管理菜单权限（内容编辑需要管理课程和场景）
INSERT INTO `role_menu_permissions` (`id`, `role`, `menu_id`, `can_view`, `created_at`) VALUES
(UUID(), 'content_editor', 'm-005-08', 1, NOW()),
(UUID(), 'content_editor', 'm-005-09', 1, NOW());

-- 为org_admin角色分配课程管理和场景管理菜单权限（机构管理员需要管理课程和场景）
INSERT INTO `role_menu_permissions` (`id`, `role`, `menu_id`, `can_view`, `created_at`) VALUES
(UUID(), 'org_admin', 'm-005-08', 1, NOW()),
(UUID(), 'org_admin', 'm-005-09', 1, NOW());

-- 为super_admin角色分配课程管理和场景管理菜单权限（平台超级管理员需要管理所有内容）
INSERT INTO `role_menu_permissions` (`id`, `role`, `menu_id`, `can_view`, `created_at`) VALUES
(UUID(), 'super_admin', 'm-005-08', 1, NOW()),
(UUID(), 'super_admin', 'm-005-09', 1, NOW());
