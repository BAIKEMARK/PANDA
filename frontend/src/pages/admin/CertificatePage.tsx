import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, InputNumber, Select, message, Space, Tag, Tabs, Tooltip, Col } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, CheckOutlined, CloseOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import { certificateService, certificateTemplateService } from '../../services/certificate.service';
import { FilterForm } from '../../components/admin/FilterForm';
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
    } catch (error: any) {
      message.error('加载证书列表失败: ' + (error.response?.data?.detail || error.message));
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
    } catch (error: any) {
      message.error('加载模板列表失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setTemplateLoading(false);
    }
  };

  const handleCertSearch = (values: any) => {
    let filtered = [...certificates];
    
    if (values.certificate_number) {
      filtered = filtered.filter(cert => 
        cert.certificate_number?.toLowerCase().includes(values.certificate_number.toLowerCase())
      );
    }
    
    if (values.user_id) {
      filtered = filtered.filter(cert => cert.user_id === values.user_id);
    }
    
    if (values.status) {
      filtered = filtered.filter(cert => cert.status === values.status);
    }
    
    setFilteredCertificates(filtered);
  };

  const handleCertReset = () => {
    setFilteredCertificates(certificates);
  };

  const handleTemplateSearch = (values: any) => {
    let filtered = [...templates];
    
    if (values.name) {
      filtered = filtered.filter(tpl => 
        tpl.name?.toLowerCase().includes(values.name.toLowerCase())
      );
    }
    
    if (values.org_id) {
      filtered = filtered.filter(tpl => tpl.org_id === values.org_id);
    }
    
    if (values.status) {
      filtered = filtered.filter(tpl => tpl.status === values.status);
    }
    
    setFilteredTemplates(filtered);
  };

  const handleTemplateReset = () => {
    setFilteredTemplates(templates);
  };

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
      content: '确定要删除这张证书吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await certificateService.delete(id);
          message.success('删除成功');
          loadCertificates();
        } catch (error: any) {
          message.error('删除失败: ' + (error.response?.data?.detail || error.message));
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
    } catch (error: any) {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message));
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
      content: '确定要删除这个模板吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await certificateTemplateService.delete(id);
          message.success('删除成功');
          loadTemplates();
        } catch (error: any) {
          message.error('删除失败: ' + (error.response?.data?.detail || error.message));
        }
      },
    });
  };

  const handleToggleTemplateStatus = async (template: CertificateTemplate, value: boolean) => {
    try {
      await certificateTemplateService.update(template.id, { status: value ? 'active' : 'inactive' });
      message.success(value ? '已启用' : '已禁用');
      loadTemplates();
    } catch (error: any) {
      message.error('更新失败: ' + (error.response?.data?.detail || error.message));
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
    } catch (error: any) {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const baseCertColumns = [
    {
      title: '证书编号',
      dataIndex: 'certificate_number',
      key: 'certificate_number',
    },
    {
      title: '用户ID',
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
        <Tag color={status === 'valid' ? 'green' : 'red'}>{status === 'valid' ? '有效' : '已撤销'}</Tag>
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
      render: (_: any, record: Certificate) => (
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
      title: '机构ID',
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
      render: (_: any, record: CertificateTemplate) => (
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
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      style={{ padding: '24px' }}
    >
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.3 }}
      >
        <h2 style={{ margin: '0 0 20px 0', fontSize: '24px', fontWeight: 600, color: '#1a365d' }}>证书管理</h2>
      </motion.div>
      <Tabs
        items={[
          {
            key: 'certificates',
            label: '证书列表',
            children: (
              <>
                <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'flex-end' }}>
                  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
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
                  </motion.div>
                </div>
                <FilterForm onSearch={handleCertSearch} onReset={handleCertReset} loading={loading}>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="certificate_number" label="证书编号">
                      <Input placeholder="请输入证书编号" allowClear />
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="user_id" label="用户ID">
                      <Input placeholder="请输入用户ID" allowClear />
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="status" label="状态">
                      <Select placeholder="请选择状态" allowClear>
                        <Select.Option value="valid">有效</Select.Option>
                        <Select.Option value="revoked">已撤销</Select.Option>
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
                  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
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
                  </motion.div>
                </div>
                <FilterForm onSearch={handleTemplateSearch} onReset={handleTemplateReset} loading={templateLoading}>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="name" label="模板名称">
                      <Input placeholder="请输入模板名称" allowClear />
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="org_id" label="机构ID">
                      <Input placeholder="请输入机构ID" allowClear />
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12} md={8} lg={6}>
                    <Form.Item name="status" label="状态">
                      <Select placeholder="请选择状态" allowClear>
                        <Select.Option value="active">启用</Select.Option>
                        <Select.Option value="inactive">禁用</Select.Option>
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
          <Form.Item name="user_id" label="用户ID" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="certificate_number" label="证书编号" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="credit_hours" label="学分" initialValue={0}>
            <InputNumber min={0} step={0.1} />
          </Form.Item>
          <Form.Item name="org_id" label="机构ID">
            <Input />
          </Form.Item>
          <Form.Item name="class_id" label="班级ID">
            <Input />
          </Form.Item>
          <Form.Item name="template_id" label="模板ID">
            <Input />
          </Form.Item>
          <Form.Item name="status" label="状态" initialValue="valid">
            <Select>
              <Select.Option value="valid">有效</Select.Option>
              <Select.Option value="revoked">已撤销</Select.Option>
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
          <Form.Item name="org_id" label="机构ID" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="name" label="模板名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </motion.div>
  );
}
