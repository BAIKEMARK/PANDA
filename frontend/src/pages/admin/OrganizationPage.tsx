import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, message, Space, Tooltip, Select, Col } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, CheckOutlined, CloseOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import organizationService from '../../services/organization.service';
import { FilterForm } from '../../components/admin/FilterForm';
import type { Organization } from '../../types/admin.types';

export function OrganizationPage() {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [filteredOrganizations, setFilteredOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingOrg, setEditingOrg] = useState<Organization | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    loadOrganizations();
  }, []);

  const loadOrganizations = async () => {
    setLoading(true);
    try {
      const data = await organizationService.list();
      setOrganizations(data);
      setFilteredOrganizations(data);
    } catch (error: any) {
      message.error('加载机构列表失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (values: any) => {
    let filtered = [...organizations];
    
    if (values.name) {
      filtered = filtered.filter(org => 
        org.name?.toLowerCase().includes(values.name.toLowerCase())
      );
    }
    
    if (values.short_name) {
      filtered = filtered.filter(org => 
        org.short_name?.toLowerCase().includes(values.short_name.toLowerCase())
      );
    }
    
    if (values.status) {
      filtered = filtered.filter(org => org.status === values.status);
    }
    
    if (values.contact_name) {
      filtered = filtered.filter(org => 
        org.contact_name?.toLowerCase().includes(values.contact_name.toLowerCase())
      );
    }
    
    setFilteredOrganizations(filtered);
  };

  const handleReset = () => {
    setFilteredOrganizations(organizations);
  };

  const handleCreate = () => {
    setEditingOrg(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (org: Organization) => {
    setEditingOrg(org);
    form.setFieldsValue(org);
    setModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个机构吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await organizationService.delete(id);
          message.success('删除成功');
          loadOrganizations();
        } catch (error: any) {
          message.error('删除失败: ' + (error.response?.data?.detail || error.message));
        }
      },
    });
  };

  const handleToggleStatus = async (org: Organization, value: boolean) => {
    try {
      await organizationService.update(org.id, { status: value ? 'active' : 'inactive' });
      message.success(value ? '已启用' : '已禁用');
      loadOrganizations();
    } catch (error: any) {
      message.error('更新失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      if (editingOrg) {
        await organizationService.update(editingOrg.id, values);
        message.success('更新成功');
      } else {
        await organizationService.create(values);
        message.success('创建成功');
      }
      setModalVisible(false);
      loadOrganizations();
    } catch (error: any) {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const baseColumns = [
    {
      title: '机构名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '简称',
      dataIndex: 'short_name',
      key: 'short_name',
    },
    {
      title: '联系人',
      dataIndex: 'contact_name',
      key: 'contact_name',
    },
    {
      title: '联系电话',
      dataIndex: 'contact_phone',
      key: 'contact_phone',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string, record: Organization) => (
        <Tooltip title={status === 'active' ? '点击禁用' : '点击启用'}>
          <Button
            type="text"
            size="small"
            danger={status !== 'active'}
            icon={status === 'active' ? <CheckOutlined /> : <CloseOutlined />}
            onClick={() => handleToggleStatus(record, status !== 'active')}
          />
        </Tooltip>
      ),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Organization) => (
        <Space>
          <Button type="link" icon={<EditOutlined />} onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Button type="link" danger icon={<DeleteOutlined />} onClick={() => handleDelete(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ];
  const columns = baseColumns.map((col) => ({ ...col, align: 'center' as const }));

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
        style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
      >
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 600, color: '#1a365d' }}>机构管理</h2>
        <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleCreate}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
              borderRadius: '8px',
              boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
            }}
          >
            新建机构
          </Button>
        </motion.div>
      </motion.div>

      <FilterForm onSearch={handleSearch} onReset={handleReset} loading={loading}>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="name" label="机构名称">
            <Input placeholder="请输入机构名称" allowClear />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="short_name" label="简称">
            <Input placeholder="请输入简称" allowClear />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="contact_name" label="联系人">
            <Input placeholder="请输入联系人" allowClear />
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
        columns={columns}
        dataSource={filteredOrganizations}
        loading={loading}
        rowKey="id"
        pagination={{ pageSize: 10, showSizeChanger: true, showTotal: (total) => `共 ${total} 条` }}
        style={{
          background: '#fff',
          borderRadius: '12px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
        }}
      />

      <Modal
        title={editingOrg ? '编辑机构' : '新建机构'}
        open={modalVisible}
        onOk={handleSubmit}
        okText="保存"
        cancelText="取消"
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="机构名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="short_name" label="简称">
            <Input />
          </Form.Item>
          <Form.Item name="contact_name" label="联系人">
            <Input />
          </Form.Item>
          <Form.Item name="contact_phone" label="联系电话">
            <Input />
          </Form.Item>
          <Form.Item name="contact_email" label="联系邮箱">
            <Input type="email" />
          </Form.Item>
        </Form>
      </Modal>
    </motion.div>
  );
}
