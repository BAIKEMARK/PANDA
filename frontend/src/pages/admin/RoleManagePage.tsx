import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Space, Tag, Checkbox, Col } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import roleService from '../../services/role.service';
import { FilterForm } from '../../components/admin/FilterForm';
import { getApiErrorMessage } from '../../utils/error';
import { getFilterText, getFilterValue } from '../../utils/filters';
import type { Role, Permission } from '../../types/admin.types';

export function RoleManagePage() {
  const [roles, setRoles] = useState<Role[]>([]);
  const [filteredRoles, setFilteredRoles] = useState<Role[]>([]);
  const [permissions, setPermissions] = useState<Permission[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [permissionModalVisible, setPermissionModalVisible] = useState(false);
  const [editingRole, setEditingRole] = useState<Role | null>(null);
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);
  const [form] = Form.useForm();
  const [permissionForm] = Form.useForm();

  useEffect(() => {
    loadRoles();
    loadPermissions();
  }, []);

  const loadRoles = async () => {
    setLoading(true);
    try {
      const data = await roleService.list();
      setRoles(data);
      setFilteredRoles(data);
    } catch (error: unknown) {
      message.error('加载角色列表失败: ' + getApiErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const loadPermissions = async () => {
    try {
      const data = await roleService.listAllPermissions();
      setPermissions(data);
    } catch {
      message.error('加载权限列表失败');
    }
  };

  const handleSearch = (values: Record<string, unknown>) => {
    let filtered = [...roles];
    const code = getFilterText(values, 'code');
    const name = getFilterText(values, 'name');
    const scope = getFilterValue(values, 'scope');
    
    if (code) {
      filtered = filtered.filter(role => 
        role.code?.toLowerCase().includes(code)
      );
    }
    
    if (name) {
      filtered = filtered.filter(role => 
        role.name?.toLowerCase().includes(name)
      );
    }
    
    if (scope) {
      filtered = filtered.filter(role => role.scope === scope);
    }
    
    setFilteredRoles(filtered);
  };

  const handleReset = () => {
    setFilteredRoles(roles);
  };

  const rolesForOptions = filteredRoles.length ? filteredRoles : roles;
  const availableScopes = new Set(
    rolesForOptions.map((role) => role.scope).filter(Boolean),
  );
  const scopeOptions = [
    { value: 'system', label: '系统' },
    { value: 'org', label: '机构' },
  ] as const;
  const filteredScopeOptions = scopeOptions.filter(
    (option) => !availableScopes.size || availableScopes.has(option.value),
  );

  const handleCreate = () => {
    setEditingRole(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (role: Role) => {
    setEditingRole(role);
    form.setFieldsValue(role);
    setModalVisible(true);
  };

  const handleAssignPermissions = (role: Role) => {
    setSelectedRole(role);
    permissionForm.setFieldsValue({
      permission_ids: role.permissions?.map(p => p.id) || []
    });
    setPermissionModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该角色吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await roleService.delete(id);
          message.success('删除成功');
          loadRoles();
        } catch (error: unknown) {
          message.error('删除失败: ' + getApiErrorMessage(error));
        }
      },
    });
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      if (editingRole) {
        await roleService.update(editingRole.id, values);
        message.success('更新成功');
      } else {
        await roleService.create(values);
        message.success('创建成功');
      }
      setModalVisible(false);
      loadRoles();
    } catch (error: unknown) {
      message.error('操作失败: ' + getApiErrorMessage(error));
    }
  };

  const handlePermissionSubmit = async () => {
    try {
      const values = await permissionForm.validateFields();
      if (selectedRole) {
        await roleService.assignPermissions(selectedRole.id, values.permission_ids);
        message.success('权限分配成功');
        setPermissionModalVisible(false);
        loadRoles();
      }
    } catch (error: unknown) {
      message.error('操作失败: ' + getApiErrorMessage(error));
    }
  };

  const baseColumns = [
    {
      title: '角色代码',
      dataIndex: 'code',
      key: 'code',
    },
    {
      title: '角色名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '范围',
      dataIndex: 'scope',
      key: 'scope',
      render: (scope: string) => (
        <Tag color={scope === 'system' ? 'red' : 'blue'}>{scope === 'system' ? '系统' : '机构'}</Tag>
      ),
    },
    {
      title: '权限数量',
      key: 'permission_count',
      render: (_: unknown, record: Role) => record.permissions?.length || 0,
    },
    {
      title: '操作',
      key: 'action',
      render: (_: unknown, record: Role) => (
        <Space>
          <Button type="link" icon={<EditOutlined />} onClick={() => handleEdit(record)}>
            编辑
          </Button>
          <Button type="link" onClick={() => handleAssignPermissions(record)}>
            分配权限
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
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 600, color: '#1a365d' }}>角色管理</h2>
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
            新建角色
          </Button>
        </div>
      </div>

      <FilterForm onSearch={handleSearch} onReset={handleReset} loading={loading}>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="code" label="角色代码">
            <Input placeholder="请输入" allowClear />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="name" label="角色名称">
            <Input placeholder="请输入" allowClear />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="scope" label="范围">
            <Select placeholder="请选择" allowClear>
              {filteredScopeOptions.map((option) => (
                <Select.Option key={option.value} value={option.value}>
                  {option.label}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
      </FilterForm>

      <Table
        columns={columns}
        dataSource={filteredRoles}
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
        title={editingRole ? '编辑角色' : '新建角色'}
        open={modalVisible}
        onOk={handleSubmit}
        okText="保存"
        cancelText="取消"
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="code" label="角色代码" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="name" label="角色名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <Input.TextArea />
          </Form.Item>
          <Form.Item name="scope" label="范围">
            <Select>
              <Select.Option value="system">系统</Select.Option>
              <Select.Option value="org">机构</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="分配权限"
        open={permissionModalVisible}
        onOk={handlePermissionSubmit}
        okText="保存"
        cancelText="取消"
        onCancel={() => setPermissionModalVisible(false)}
        width={600}
      >
        <Form form={permissionForm} layout="vertical">
          <Form.Item name="permission_ids" label="权限列表">
            <Checkbox.Group style={{ width: '100%' }}>
              {permissions.map(perm => (
                <div key={perm.id} style={{ marginBottom: '8px' }}>
                  <Checkbox value={perm.id}>{perm.name} ({perm.code})</Checkbox>
                </div>
              ))}
            </Checkbox.Group>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}



