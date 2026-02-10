import { useState, useEffect, useMemo } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Space, Col } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import userAdminService from '../../services/user-admin.service';
import organizationService from '../../services/organization.service';
import { FilterForm } from '../../components/admin/FilterForm';
import type { User, Organization } from '../../types/admin.types';

const applyUserFilters = (
  list: User[],
  values: Record<string, any>,
) => {
  let filtered = [...list];

  if (values.name) {
    filtered = filtered.filter((user) =>
      user.name?.toLowerCase().includes(values.name.toLowerCase()),
    );
  }

  if (values.email) {
    filtered = filtered.filter((user) =>
      user.email?.toLowerCase().includes(values.email.toLowerCase()),
    );
  }

  if (values.role) {
    const selectedRole = values.role as string;
    filtered = filtered.filter((user) => user.role === selectedRole);
  }

  if (values.org_id) {
    filtered = filtered.filter((user) => user.org_id === values.org_id);
  }

  if (values.department) {
    filtered = filtered.filter((user) =>
      user.department?.toLowerCase().includes(values.department.toLowerCase()),
    );
  }

  return filtered;
};

const baseRoleOptions = [
  { value: 'student', label: '学员' },
  { value: 'instructor', label: '讲师' },
  { value: 'admin', label: '管理员' },
];

export function UserManagePage() {
  const [users, setUsers] = useState<User[]>([]);
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [form] = Form.useForm();
  const [filterValues, setFilterValues] = useState<Record<string, any>>({});
  const roleLabelByValue = useMemo(
    () => new Map(baseRoleOptions.map((role) => [role.value, role.label])),
    [],
  );
  const userRoleValues = useMemo(
    () => new Set(users.map((user) => user.role).filter((role): role is string => Boolean(role))),
    [users],
  );

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [usersData, orgsData] = await Promise.all([
        userAdminService.list(),
        organizationService.list(),
      ]);
      setUsers(usersData.users);
      setFilteredUsers(usersData.users);
      setOrganizations(orgsData);
    } catch (error: any) {
      message.error('加载数据失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (values: any) => {
    setFilterValues(values);
    setFilteredUsers(applyUserFilters(users, values));
  };

  const handleReset = () => {
    setFilterValues({});
    setFilteredUsers(users);
  };

  const roleOptions = useMemo(() => {
    const values = { ...filterValues };
    delete values.role;
    const candidates = applyUserFilters(users, values);
    const availableRoleValues = new Set(
      candidates.map((user) => user.role).filter((role): role is string => Boolean(role)),
    );
    const options = baseRoleOptions.map((role) => ({
      key: role.value,
      value: role.value,
      label: role.label,
      isAvailable: !availableRoleValues.size || availableRoleValues.has(role.value),
    }));

    // 如果存在非标准角色，保留展示（便于排查数据问题）
    userRoleValues.forEach((value) => {
      if (roleLabelByValue.has(value)) return;
      const isAvailable = !availableRoleValues.size || availableRoleValues.has(value);
      options.push({ key: value, value, label: value, isAvailable });
    });

    return options.sort((a, b) => Number(b.isAvailable) - Number(a.isAvailable));
  }, [users, filterValues, userRoleValues, roleLabelByValue]);

  const organizationOptions = useMemo(() => {
    const values = { ...filterValues };
    delete values.org_id;
    const candidates = applyUserFilters(users, values);
    const availableOrgIds = new Set(
      candidates.map((user) => user.org_id).filter((orgId): orgId is string => Boolean(orgId)),
    );
    return organizations
      .map((org) => ({
        org,
        isAvailable: !availableOrgIds.size || availableOrgIds.has(org.id),
      }))
      .sort((a, b) => Number(b.isAvailable) - Number(a.isAvailable));
  }, [users, organizations, filterValues]);

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
      content: '确定要删除该用户吗？',
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
        return roleLabelByValue.get(role) || role;
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
    <div
      style={{ padding: '24px' }}
    >
      <div
        style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
      >
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 600, color: '#1a365d' }}>用户管理</h2>
        <div >
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
        </div>
      </div>

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
              {roleOptions.map(({ key, value, label, isAvailable }) => (
                <Select.Option key={key} value={value} disabled={!isAvailable}>
                  {label}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="org_id" label="机构">
            <Select placeholder="请选择机构" allowClear>
              {organizationOptions.map(({ org }) => (
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
            <Input placeholder="请输入姓名" allowClear />
          </Form.Item>
          {!editingUser && (
            <>
              <Form.Item name="email" label="邮箱" rules={[{ required: true, type: 'email' }]}>
            <Input placeholder="请输入邮箱" allowClear />
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
              options={baseRoleOptions}
            />
          </Form.Item>
          <Form.Item name="phone" label="Phone">
            <Input />
          </Form.Item>
          <Form.Item name="department" label="科室">
            <Input placeholder="请输入科室" allowClear />
          </Form.Item>
          <Form.Item name="title" label="职称">
            <Input />
          </Form.Item>
          <Form.Item name="employee_id" label="工号">
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}





