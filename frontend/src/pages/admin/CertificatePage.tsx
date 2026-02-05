import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, InputNumber, Select, message, Space, Tag, Tabs } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { certificateService, certificateTemplateService } from '../../services/certificate.service';
import type { Certificate, CertificateTemplate } from '../../types/admin.types';

export function CertificatePage() {
  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [templates, setTemplates] = useState<CertificateTemplate[]>([]);
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
    } catch (error: any) {
      message.error('加载模板列表失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setTemplateLoading(false);
    }
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
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'red'}>{status === 'active' ? '启用' : '禁用'}</Tag>
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
    <div style={{ padding: '24px' }}>
      <h2>证书管理</h2>
      <Tabs
        items={[
          {
            key: 'certificates',
            label: '证书列表',
            children: (
              <>
                <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'flex-end' }}>
                  <Button type="primary" icon={<PlusOutlined />} onClick={handleCreateCert}>
                    新建证书
                  </Button>
                </div>
                <Table
                  columns={certColumns}
                  dataSource={certificates}
                  loading={loading}
                  rowKey="id"
                  pagination={{ pageSize: 10 }}
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
                  <Button type="primary" icon={<PlusOutlined />} onClick={handleCreateTemplate}>
                    新建模板
                  </Button>
                </div>
                <Table
                  columns={templateColumns}
                  dataSource={templates}
                  loading={templateLoading}
                  rowKey="id"
                  pagination={{ pageSize: 10 }}
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
          <Form.Item name="status" label="状态" initialValue="active">
            <Select>
              <Select.Option value="active">启用</Select.Option>
              <Select.Option value="inactive">禁用</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
