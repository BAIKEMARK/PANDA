import api from './api';
import type { Certificate, CertificateTemplate } from '../types/admin.types';

class CertificateService {
  async list(userId?: string, orgId?: string, skip = 0, limit = 100): Promise<Certificate[]> {
    const params: any = { skip, limit };
    if (userId) params.user_id = userId;
    if (orgId) params.org_id = orgId;
    const response = await api.get<Certificate[]>('/admin/certificates', { params });
    return response.data;
  }

  async get(id: string): Promise<Certificate> {
    const response = await api.get<Certificate>(`/admin/certificates/${id}`);
    return response.data;
  }

  async create(data: Partial<Certificate>): Promise<Certificate> {
    const response = await api.post<Certificate>('/admin/certificates', data);
    return response.data;
  }

  async update(id: string, data: Partial<Certificate>): Promise<Certificate> {
    const response = await api.put<Certificate>(`/admin/certificates/${id}`, data);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/admin/certificates/${id}`);
  }
}

class CertificateTemplateService {
  async list(orgId?: string, status?: string, skip = 0, limit = 100): Promise<CertificateTemplate[]> {
    const params: any = { skip, limit };
    if (orgId) params.org_id = orgId;
    if (status) params.status = status;
    const response = await api.get<CertificateTemplate[]>('/admin/certificate-templates', { params });
    return response.data;
  }

  async get(id: string): Promise<CertificateTemplate> {
    const response = await api.get<CertificateTemplate>(`/admin/certificate-templates/${id}`);
    return response.data;
  }

  async create(data: Partial<CertificateTemplate>): Promise<CertificateTemplate> {
    const response = await api.post<CertificateTemplate>('/admin/certificate-templates', data);
    return response.data;
  }

  async update(id: string, data: Partial<CertificateTemplate>): Promise<CertificateTemplate> {
    const response = await api.put<CertificateTemplate>(`/admin/certificate-templates/${id}`, data);
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/admin/certificate-templates/${id}`);
  }
}

export const certificateService = new CertificateService();
export const certificateTemplateService = new CertificateTemplateService();
export default certificateService;
