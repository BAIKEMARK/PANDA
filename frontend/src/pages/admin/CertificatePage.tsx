import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, InputNumber, Select, message, Space, Tag, Tabs, Tooltip, Col } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, CheckOutlined, CloseOutlined } from '@ant-design/icons';
import { certificateService, certificateTemplateService } from '../../services/certificate.service';
import { FilterForm } from '../../components/admin/FilterForm';
import { getApiErrorMessage } from '../../utils/error';
import { getFilterText, getFilterValue } from '../../utils/filters';
import type { Certificate, CertificateTemplate } from '../../types/admin.types';

export function CertificatePage() {
  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [filteredCertificates, setFilteredCertificates] = useState<Certificate[]>([]);
  const [templates, setTemplates] = useState<CertificateTemplate[]>([]);
  const [filteredTemplates, setFilteredTemplates] = useState<CertificateTemplate[]>([]);
  const [loading, setLoading] = useState(false);
  const [templateLoading, setTemplateLoading] = useState(false);
  const [certModalVisible, setCertModalVisible] = useState(false);
  const [templateModalVisible, setTemplateModalVisible] = useState(false);
  const [editingCert, setEditingCert] = useState<Certificate | null>(null);
  const [editingTemplate, setEditingTemplate] = useState<CertificateTemplate | null>(null);
  const [certForm] = Form.useForm();
  const [templateForm] = Form.useForm();

  useEffect(() => {
    loadCertificates();
    loadTemplates();
  }, []);

  const loadCertificates = async () => {
    setLoading(true);
    try {
      const data = await certificateService.list();
      setCertificates(data);
      setFilteredCertificates(data);
    } catch (error: unknown) {
      message.error('加载证书列表失败: ' + getApiErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const loadTemplates = async () => {
    setTemplateLoading(true);
    try {
      const data = await certificateTemplateService.list();
      setTemplates(data);
      setFilteredTemplates(data);
    } catch (error: unknown) {
      message.error('加载模板列表失败: ' + getApiErrorMessage(error));
    } finally {
      setTemplateLoading(false);
    }
  };

  const handleCertSearch = (values: Record<string, unknown>) => {
    let filtered = [...certificates];
    const certificateNumber = getFilterText(values, 'certificate_number');
    const userId = getFilterValue(values, 'user_id');
    const status = getFilterValue(values, 'status');
    
    if (certificateNumber) {
      filtered = filtered.filter(cert => 
        cert.certificate_number?.toLowerCase().includes(certificateNumber)
      );
    }
    
    if (userId) {
      filtered = filtered.filter(cert => cert.user_id === userId);
    }
    
    if (status) {
      filtered = filtered.filter(cert => cert.status === status);
    }
    
    setFilteredCertificates(filtered);
  };

  const handleCertReset = () => {
    setFilteredCertificates(certificates);
  };

  const handleTemplateSearch = (values: Record<string, unknown>) => {
    let filtered = [...templates];
    const name = getFilterText(values, 'name');
    const orgId = getFilterValue(values, 'org_id');
    const status = getFilterValue(values, 'status');
    
    if (name) {
      filtered = filtered.filter(tpl => 
        tpl.name?.toLowerCase().includes(name)
      );
    }
    
    if (orgId) {
      filtered = filtered.filter(tpl => tpl.org_id === orgId);
    }
    
    if (status) {
      filtered = filtered.filter(tpl => tpl.status === status);
    }
    
    setFilteredTemplates(filtered);
  };

  const handleTemplateReset = () => {
    setFilteredTemplates(templates);
  };

  const certificatesForOptions = filteredCertificates.length ? filteredCertificates : certificates;
  const availableCertStatuses = new Set(
    certificatesForOptions.map((cert) => cert.status).filter(Boolean),
  );
  const certStatusOptions = [
    { value: 'valid', label: '有效' },
    { value: 'revoked', label: '宸叉挙閿€' },
  ] as const;
  const filteredCertStatusOptions = certStatusOptions.filter(
    (option) => !availableCertStatuses.size || availableCertStatuses.has(option.value),
  );

  const templatesForOptions = filteredTemplates.length ? filteredTemplates : templates;
  const availableTemplateStatuses = new Set(
    templatesForOptions.map((template) => template.status).filter(Boolean),
  );
  const templateStatusOptions = [
    { value: 'active', label: '启用' },
    { value: 'inactive', label: '禁用' },
  ] as const;
  const filteredTemplateStatusOptions = templateStatusOptions.filter(
    (option) => !availableTemplateStatuses.size || availableTemplateStatuses.has(option.value),
  );

  const handleCreateCert = () => {
    setEditingCert(null);
    certForm.resetFields();
    setCertModalVisible(true);
  };

  const handleEditCert = (cert: Certificate) => {
    setEditingCert(cert);
    certForm.setFieldsValue(cert);
    setCertModalVisible(true);
  };

  const handleDeleteCert = async (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该证书吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await certificateService.delete(id);
          message.success('删除成功');
          loadCertificates();
        } catch (error: unknown) {
          message.error('删除失败: ' + getApiErrorMessage(error));
        }
      },
    });
  };

  const handleCertSubmit = async () => {
    try {
      const values = await certForm.validateFields();
      if (editingCert) {
        await certificateService.update(editingCert.id, values);
        message.success('更新成功');
      } else {
        await certificateService.create(values);
        message.success('创建成功');
      }
      setCertModalVisible(false);
      loadCertificates();
    } catch (error: unknown) {
      message.error('操作失败: ' + getApiErrorMessage(error));
    }
  };

  const handleCreateTemplate = () => {
    setEditingTemplate(null);
    templateForm.resetFields();
    setTemplateModalVisible(true);
  };

  const handleEditTemplate = (template: CertificateTemplate) => {
    setEditingTemplate(template);
    templateForm.setFieldsValue(template);
    setTemplateModalVisible(true);
  };

  const handleDeleteTemplate = async (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该模板吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await certificateTemplateService.delete(id);
          message.success('删除成功');
          loadTemplates();
        } catch (error: unknown) {
          message.error('删除失败: ' + getApiErrorMessage(error));
        }
      },
    });
  };

  const handleToggleTemplateStatus = async (template: CertificateTemplate, value: boolean) => {
    try {
      await certificateTemplateService.update(template.id, { status: value ? 'active' : 'inactive' });
      message.success(value ? '已启用' : '已禁用');
      loadTemplates();
    } catch (error: unknown) {
      message.error('更新失败: ' + getApiErrorMessage(error));
    }
  };

  const handleTemplateSubmit = async () => {
    try {
      const values = await templateForm.validateFields();
      if (editingTemplate) {
        await certificateTemplateService.update(editingTemplate.id, values);
        message.success('更新成功');
      } else {
        await certificateTemplateService.create(values);
        message.success('创建成功');
      }
      setTemplateModalVisible(false);
      loadTemplates();
    } catch (error: unknown) {
      message.error('操作失败: ' + getApiErrorMessage(error));
    }
  };

  const baseCertColumns = [
    {
      title: '证书编号',
      dataIndex: 'certificate_number',
      key: 'certificate_number',
    },
    {
      title: '用户编号',
      dataIndex: 'user_id',
      key: 'user_id',
    },
    {
      title: '学分',
      dataIndex: 'credit_hours',
      key: 'credit_hours',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'valid' ? 'green' : 'red'}>{status === 'valid' ? '有效' : '已撤'}</Tag>
      ),
    },
    {
      title: '颁发日期',
      dataIndex: 'issue_date',
      key: 'issue_date',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: unknown, record: Certificate) => (
        <Space>
          <Button type="link" icon={<EditOutlined />} onClick={() => handleEditCert(record)}>
            编辑
          </Button>
          <Button type="link" danger icon={<DeleteOutlined />} onClick={() => handleDeleteCert(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ];
  const certColumns = baseCertColumns.map((col) => ({ ...col, align: 'center' as const }));

  const baseTemplateColumns = [
    {
      title: '模板名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '机构编号',
      dataIndex: 'org_id',
      key: 'org_id',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string, record: CertificateTemplate) => (
        <Tooltip title={status === 'active' ? '点击禁用' : '点击启用'}>
          <Button
            type="text"
            size="small"
            danger={status !== 'active'}
            icon={status === 'active' ? <CheckOutlined /> : <CloseOutlined />}
            onClick={() => handleToggleTemplateStatus(record, status !== 'active')}
          />
        </Tooltip>
      ),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: unknown, record: CertificateTemplate) => (
        <Space>
          <Button type="link" icon={<EditOutlined />} onClick={() => handleEditTemplate(record)}>
            编辑
          </Button>
          <Button type="link" danger icon={<DeleteOutlined />} onClick={() => handleDeleteTemplate(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ];
  const templateColumns = baseTemplateColumns.map((col) => ({ ...col, align: 'center' as const }));

  return (
    <div
      style={{ padding: '24px' }}
    >
      <div
        >
        <h2 style={{ margin: '0 0 20px 0', fontSize: '24px', fontWeight: 600, color: '#1a365d' }}>证书管理</h2>
      </div>
      <Tabs
        items={[
          {
            key: 'certificates',
            label: '证书列表',
            children: (
              <>
                <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'flex-end' }}>
                  <div >
                    <Button
                      type="primary"
                      icon={<PlusOutlined />}
                      onClick={handleCreateCert}
                      style={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        border: 'none',
                        borderRadius: '8px',
                        boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
                      }}
                    >
                      新建证书
                    </Button>
                  </div>
                </div>
                <FilterForm onSearch={handleCertSearch} onReset={handleCertReset} loading={loading}>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="certificate_number" label="证书编号">
                      <Input placeholder="请输入" allowClear />
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="user_id" label="用户编号">
                      <Input placeholder="请输入用户编号" allowClear />
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="status" label="状态">
                      <Select placeholder="请选择" allowClear>
                        {filteredCertStatusOptions.map((option) => (
                          <Select.Option key={option.value} value={option.value}>
                            {option.label}
                          </Select.Option>
                        ))}
                      </Select>
                    </Form.Item>
                  </Col>
                </FilterForm>
                <Table
                  columns={certColumns}
                  dataSource={filteredCertificates}
                  loading={loading}
                  rowKey="id"
                  pagination={{ pageSize: 10, showSizeChanger: true, showTotal: (total) => `共 ${total} 条` }}
                  style={{
                    background: '#fff',
                    borderRadius: '12px',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
                  }}
                />
              </>
            ),
          },
          {
            key: 'templates',
            label: '证书模板',
            children: (
              <>
                <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'flex-end' }}>
                  <div >
                    <Button
                      type="primary"
                      icon={<PlusOutlined />}
                      onClick={handleCreateTemplate}
                      style={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        border: 'none',
                        borderRadius: '8px',
                        boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
                      }}
                    >
                      新建模板
                    </Button>
                  </div>
                </div>
                <FilterForm onSearch={handleTemplateSearch} onReset={handleTemplateReset} loading={templateLoading}>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="name" label="模板名称">
                      <Input placeholder="请输入" allowClear />
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="org_id" label="机构编号">
                      <Input placeholder="请输入机构编号" allowClear />
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="status" label="状态">
                      <Select placeholder="请选择" allowClear>
                        {filteredTemplateStatusOptions.map((option) => (
                          <Select.Option key={option.value} value={option.value}>
                            {option.label}
                          </Select.Option>
                        ))}
                      </Select>
                    </Form.Item>
                  </Col>
                </FilterForm>
                <Table
                  columns={templateColumns}
                  dataSource={filteredTemplates}
                  loading={templateLoading}
                  rowKey="id"
                  pagination={{ pageSize: 10, showSizeChanger: true, showTotal: (total) => `共 ${total} 条` }}
                  style={{
                    background: '#fff',
                    borderRadius: '12px',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
                  }}
                />
              </>
            ),
          },
        ]}
      />

      <Modal
        title={editingCert ? '编辑证书' : '新建证书'}
        open={certModalVisible}
        onOk={handleCertSubmit}
        okText="保存"
        cancelText="取消"
        onCancel={() => setCertModalVisible(false)}
        width={600}
      >
        <Form form={certForm} layout="vertical">
          <Form.Item name="user_id" label="用户编号" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="certificate_number" label="证书编号" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="credit_hours" label="学分" initialValue={0}>
            <InputNumber min={0} step={0.1} />
          </Form.Item>
          <Form.Item name="org_id" label="机构编号">
            <Input />
          </Form.Item>
          <Form.Item name="class_id" label="班级编号">
            <Input />
          </Form.Item>
          <Form.Item name="template_id" label="模板编号">
            <Input />
          </Form.Item>
          <Form.Item name="status" label="状态">
            <Select>
              <Select.Option value="valid">有效</Select.Option>
              <Select.Option value="revoked">宸叉挙閿€</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title={editingTemplate ? '编辑模板' : '新建模板'}
        open={templateModalVisible}
        onOk={handleTemplateSubmit}
        okText="保存"
        cancelText="取消"
        onCancel={() => setTemplateModalVisible(false)}
        width={600}
      >
        <Form form={templateForm} layout="vertical">
          <Form.Item name="org_id" label="机构编号" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="name" label="模板名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}




