import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Space, Col } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import userAdminService from '../../services/user-admin.service';
import roleService from '../../services/role.service';
import organizationService from '../../services/organization.service';
import { FilterForm } from '../../components/admin/FilterForm';
import type { User, Role, Organization } from '../../types/admin.types';

export function UserManagePage() {
  const [users, setUsers] = useState<User[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [roles, setRoles] = useState<Role[]>([]);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [form] = Form.useForm();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [usersData, rolesData, orgsData] = await Promise.all([
        userAdminService.list(),
        roleService.list(),
        organizationService.list(),
      ]);
      setUsers(usersData.users);
      setFilteredUsers(usersData.users);
      setRoles(rolesData);
      setOrganizations(orgsData);
    } catch (error: any) {
      message.error('加载数据失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (values: any) => {
    let filtered = [...users];
    
    if (values.name) {
      filtered = filtered.filter(user => 
        user.name?.toLowerCase().includes(values.name.toLowerCase())
      );
    }
    
    if (values.email) {
      filtered = filtered.filter(user => 
        user.email?.toLowerCase().includes(values.email.toLowerCase())
      );
    }
    
    if (values.role) {
      filtered = filtered.filter(user => user.role === values.role);
    }
    
    if (values.org_id) {
      filtered = filtered.filter(user => user.org_id === values.org_id);
    }
    
    if (values.department) {
      filtered = filtered.filter(user => 
        user.department?.toLowerCase().includes(values.department.toLowerCase())
      );
    }
    
    setFilteredUsers(filtered);
  };

  const handleReset = () => {
    setFilteredUsers(users);
  };

  const handleCreate = () => {
    setEditingUser(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    form.setFieldsValue(user);
    setModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个用户吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await userAdminService.delete(id);
          message.success('删除成功');
          loadData();
        } catch (error: any) {
          message.error('删除失败: ' + (error.response?.data?.detail || error.message));
        }
      },
    });
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      if (editingUser) {
        await userAdminService.update(editingUser.id, values);
        message.success('更新成功');
      } else {
        await userAdminService.create(values);
        message.success('创建成功');
      }
      setModalVisible(false);
      loadData();
    } catch (error: any) {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const baseColumns = [
    {
      title: '姓名',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '邮箱',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: '角色',
      dataIndex: 'role',
      key: 'role',
      render: (role: string) => {
        const found = roles.find((r) => r.code === role);
        if (found) return found.name;
        const fallbackMap: Record<string, string> = {
          student: '学员',
          instructor: '讲师',
          admin: '管理员',
        };
        return fallbackMap[role] || role;
      },
    },
    {
      title: '科室',
      dataIndex: 'department',
      key: 'department',
    },
    {
      title: '职称',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: User) => (
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
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 600, color: '#1a365d' }}>用户管理</h2>
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
            新建用户
          </Button>
        </motion.div>
      </motion.div>

      <FilterForm onSearch={handleSearch} onReset={handleReset} loading={loading}>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="name" label="姓名">
            <Input placeholder="请输入姓名" allowClear />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="email" label="邮箱">
            <Input placeholder="请输入邮箱" allowClear />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="role" label="角色">
            <Select placeholder="请选择角色" allowClear>
              {roles.map((role) => (
                <Select.Option key={role.code} value={role.code}>
                  {role.name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="org_id" label="机构">
            <Select placeholder="请选择机构" allowClear>
              {organizations.map((org) => (
                <Select.Option key={org.id} value={org.id}>
                  {org.name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="department" label="科室">
            <Input placeholder="请输入科室" allowClear />
          </Form.Item>
        </Col>
      </FilterForm>

      <Table
        columns={columns}
        dataSource={filteredUsers}
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
        title={editingUser ? '编辑用户' : '新建用户'}
        open={modalVisible}
        onOk={handleSubmit}
        okText="保存"
        cancelText="取消"
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="姓名" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          {!editingUser && (
            <>
              <Form.Item name="email" label="邮箱" rules={[{ required: true, type: 'email' }]}>
                <Input type="email" />
              </Form.Item>
              <Form.Item name="password" label="密码" rules={[{ required: true, min: 6 }]}>
                <Input.Password />
              </Form.Item>
            </>
          )}
          <Form.Item name="org_id" label="机构">
            <Select
              allowClear
              placeholder="请选择机构"
              options={organizations.map((org) => ({
                label: org.name,
                value: org.id,
              }))}
            />
          </Form.Item>
          <Form.Item name="role" label="角色" rules={[{ required: true }]}>
            <Select
              placeholder="请选择角色"
              options={roles.map((role) => ({
                label: role.name,
                value: role.code,
              }))}
            />
          </Form.Item>
          <Form.Item name="phone" label="手机号">
            <Input />
          </Form.Item>
          <Form.Item name="department" label="科室">
            <Input />
          </Form.Item>
          <Form.Item name="title" label="职称">
            <Input />
          </Form.Item>
          <Form.Item name="employee_id" label="工号">
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </motion.div>
  );
}
