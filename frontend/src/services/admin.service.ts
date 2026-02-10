import api from './api';
import type {
  AuditLog,
  ContentItem,
  ContentScope,
  ContentStatus,
  ContentType,
  ContentVersion,
  ContentVersionStatus,
  ExportJob,
  Organization,
  Role,
  RoleScope,
} from '../types';

export const adminService = {
  getOrganizations: () => api.get<Organization[]>('/admin/orgs'),
  createOrganization: (payload: Partial<Organization>) => api.post<Organization>('/admin/orgs', payload),
  updateOrganization: (id: string, payload: Partial<Organization>) => api.put<Organization>(`/admin/orgs/${id}`, payload),
  deleteOrganization: (id: string) => api.delete(`/admin/orgs/${id}`),

  getRoles: (scope?: RoleScope) => api.get<Role[]>('/admin/roles', { params: { scope } }),
  createRole: (payload: { code: string; name: string; scope: RoleScope; is_enabled?: boolean }) =>
    api.post<Role>('/admin/roles', payload),
  updateRole: (id: string, payload: Partial<Role>) => api.put<Role>(`/admin/roles/${id}`, payload),
  deleteRole: (id: string) => api.delete(`/admin/roles/${id}`),
  getPermissions: () => api.get('/admin/permissions'),
  bindRolePermissions: (roleId: string, permissionIds: string[]) =>
    api.post(`/admin/roles/${roleId}/permissions`, { permission_ids: permissionIds }),

  getContents: (params: { type?: ContentType; scope?: ContentScope; status?: ContentStatus }) =>
    api.get<ContentItem[]>('/admin/contents', { params }),
  createContent: (payload: { type: ContentType; title: string; scope: ContentScope; owner_org_id?: string }) =>
    api.post<ContentItem>('/admin/contents', payload),
  updateContent: (id: string, payload: Partial<ContentItem>) => api.put<ContentItem>(`/admin/contents/${id}`, payload),
  deleteContent: (id: string) => api.delete(`/admin/contents/${id}`),

  getContentVersions: (contentId: string) =>
    api.get<ContentVersion[]>(`/admin/contents/${contentId}/versions`),
  createContentVersion: (contentId: string, payload: { version_label: string; change_log: string; data: unknown }) =>
    api.post<ContentVersion>(`/admin/contents/${contentId}/versions`, payload),
  updateContentVersionStatus: (
    versionId: string,
    payload: { status: ContentVersionStatus; change_log?: string }
  ) => api.put<ContentVersion>(`/admin/content_versions/${versionId}`, payload),
  reviewContentVersion: (versionId: string, payload: { status: 'approved' | 'rejected'; review_comment?: string }) =>
    api.post(`/admin/content_versions/${versionId}/review`, payload),

  getClasses: () => api.get('/admin/classes'),
  createClass: (payload: {
    org_id: string;
    owner_id: string;
    name: string;
    start_date?: string;
    end_date?: string;
    description?: string;
  }) =>
    api.post('/admin/classes', payload),
  updateClass: (id: string, payload: Record<string, unknown>) => api.put(`/admin/classes/${id}`, payload),
  deleteClass: (id: string) => api.delete(`/admin/classes/${id}`),
  getClassTasks: (classId: string) => api.get(`/admin/classes/${classId}/tasks`),
  createClassTask: (
    classId: string,
    payload: {
      name: string;
      task_type: string;
      content_version_id: string;
      required_count?: number;
      rule_config?: unknown;
      due_at?: string;
      order_no?: number;
      status?: string;
    }
  ) => api.post(`/admin/classes/${classId}/tasks`, payload),

  listExports: (params?: { status?: string }) => api.get<ExportJob[]>('/admin/exports', { params }),
  createExport: (payload: { org_id: string; requested_by: string; export_type: string; filter_data?: unknown; file_format?: string }) =>
    api.post<ExportJob>('/admin/exports', payload),

  listAuditLogs: (params?: { action?: string; resource_type?: string; org_id?: string }) =>
    api.get<AuditLog[]>('/admin/audit_logs', { params }),
};
