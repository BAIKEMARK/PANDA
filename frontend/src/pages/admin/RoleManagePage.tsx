import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Space, Tag, Checkbox } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import roleService from '../../services/role.service';
import type { Role, Permission } from '../../types/admin.types';

export function RoleManagePage() {
  const [roles, setRoles] = useState<Role[]>([]);
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
    } catch (error: any) {
      message.error('加载角色列表失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const loadPermissions = async () => {
    try {
      const data = await roleService.listAllPermissions();
      setPermissions(data);
    } catch (error: any) {
      message.error('加载权限列表失败');
    }
  };

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
      content: '确定要删除这个角色吗？',
      onOk: async () => {
        try {
          await roleService.update(id, { status: 'inactive' });
          message.success('删除成功');
          loadRoles();
        } catch (error: any) {
          message.error('删除失败: ' + (error.response?.data?.detail || error.message));
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
    } catch (error: any) {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message));
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
    } catch (error: any) {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const columns = [
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
      title: '作用域',
      dataIndex: 'scope',
      key: 'scope',
      render: (scope: string) => (
        <Tag color={scope === 'system' ? 'red' : 'blue'}>{scope === 'system' ? '系统' : '机构'}</Tag>
      ),
    },
    {
      title: '权限数量',
      key: 'permission_count',
      render: (_: any, record: Role) => record.permissions?.length || 0,
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Role) => (
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

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between' }}>
        <h2>角色管理</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
          新建角色
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={roles}
        loading={loading}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />

      <Modal
        title={editingRole ? '编辑角色' : '新建角色'}
        open={modalVisible}
        onOk={handleSubmit}
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
          <Form.Item name="scope" label="作用域" initialValue="org">
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
