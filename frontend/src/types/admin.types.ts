export interface Organization {
  id: string;
  name: string;
  short_name?: string;
  logo_url?: string;
  contact_name?: string;
  contact_phone?: string;
  contact_email?: string;
  valid_until?: string;
  status: 'active' | 'inactive' | 'expired';
  config?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface Role {
  id: string;
  code: string;
  name: string;
  description?: string;
  scope: 'system' | 'org';
  is_enabled?: boolean;
  created_at: string;
  permissions?: Permission[];
}

export type RoleScope = Role['scope'];

export interface Permission {
  id: string;
  code: string;
  name: string;
  module: string;
  action: string;
  description?: string;
}

export interface TrainingClass {
  id: string;
  org_id: string;
  name: string;
  description?: string;
  start_date: string;
  end_date: string;
  trainer_id?: string;
  owner_id?: string;
  credit_rule?: Record<string, unknown>;
  completion_rule?: Record<string, unknown>;
  status: 'draft' | 'active' | 'completed' | 'archived';
  created_at: string;
  updated_at: string;
}

export interface ClassStudent {
  class_id: string;
  user_id: string;
  joined_at: string;
  status: 'active' | 'completed' | 'dropped';
}

export interface ClassTask {
  id: string;
  class_id: string;
  resource_type: 'course' | 'scenario' | 'exam';
  resource_id: string;
  resource_version?: string;
  deadline?: string;
  sort_order: number;
  created_at: string;
}

export interface UserOrgAssign {
  org_id: string;
  role_id: string;
}

export interface UserListResponse {
  users: User[];
  total: number;
  skip: number;
  limit: number;
}

export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  org_id?: string;
  phone?: string;
  department?: string;
  title?: string;
  employee_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Certificate {
  id: string;
  user_id: string;
  certificate_number: string;
  issue_date: string;
  credit_hours: number;
  org_id?: string;
  class_id?: string;
  template_id?: string;
  status: 'valid' | 'revoked';
  revoked_at?: string;
  revoked_by?: string;
}

export interface CertificateTemplate {
  id: string;
  org_id: string;
  name: string;
  template_config?: Record<string, unknown>;
  status: 'active' | 'inactive';
  created_at: string;
  updated_at: string;
}

export interface Question {
  id: string;
  org_id?: string;
  scope: 'private' | 'platform' | 'shared';
  question_type: 'single' | 'multiple' | 'judge';
  question_text: string;
  options: string[];
  correct_answer: string[];
  explanation?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  knowledge_tags?: string[];
  chapter_id?: string;
  status: 'draft' | 'active' | 'disabled';
  created_at: string;
  updated_at: string;
}

export type ContentType = 'course' | 'question_bank' | 'scenario' | 'scoring_rule' | 'certificate_template' | 'exam';
export type ContentScope = 'private' | 'platform' | 'shared';
export type ContentStatus = 'active' | 'inactive' | 'draft' | 'pending' | 'published' | 'archived';
export type ContentVersionStatus = 'draft' | 'pending' | 'approved' | 'rejected' | 'published' | 'archived';

export interface ContentItem {
  id: string;
  type: ContentType;
  title: string;
  scope: ContentScope;
  owner_org_id?: string;
  status: ContentStatus;
  created_at?: string;
  updated_at?: string;
}

export interface ContentVersion {
  id: string;
  content_id: string;
  version_label: string;
  change_log?: string;
  data?: unknown;
  status: ContentVersionStatus;
  created_at?: string;
  updated_at?: string;
}

export interface ExportJob {
  id: string;
  org_id: string;
  requested_by: string;
  export_type: string;
  filter_data?: unknown;
  file_format?: string;
  status: string;
  created_at?: string;
}

export interface AuditLog {
  id: string;
  user_id?: string;
  org_id?: string;
  action: string;
  resource_type?: string;
  resource_id?: string;
  changes?: unknown;
  created_at?: string;
}
