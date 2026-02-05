import { useCallback, useEffect, useMemo, useState } from 'react';
import { Button, Card, Form, Input, Modal, Popconfirm, Select, Space, Spin, Switch, Table, message } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import type { MenuItem, Organization, Role, Permission, ContentItem, ExportJob, AuditLog, TrainingClass, User } from '../types';
import { adminService } from '../services/admin.service';
import menuService from '../services/menu.service';
import api from '../services/api';

type LoaderResult<T> = { data: T[] } | T[];

function useList<T>(loader: () => Promise<LoaderResult<T>>, deps: unknown[] = []) {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<T[]>([]);
  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const res = await loader();
        setData(Array.isArray(res) ? res : res.data);
      } catch {
        message.error('加载失败');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [loader, ...deps]);
  return { loading, data };
}

const ORG_STATUSES = [
  { label: '启用', value: 'active' },
  { label: '停用', value: 'inactive' },
  { label: '过期', value: 'expired' },
];

const ROLE_SCOPES = [
  { label: '平台', value: 'platform' },
  { label: '机构', value: 'org' },
];

const CONTENT_TYPES = [
  { label: '课程', value: 'course' },
  { label: '题库', value: 'question_bank' },
  { label: '情景', value: 'scenario' },
  { label: '评分规则', value: 'scoring_rule' },
  { label: '证书模板', value: 'certificate_template' },
  { label: '考试', value: 'exam' },
];

const CONTENT_SCOPES = [
  { label: '私有', value: 'private' },
  { label: '平台', value: 'platform' },
  { label: '共享', value: 'shared' },
];

const CONTENT_STATUSES = [
  { label: '启用', value: 'active' },
  { label: '停用', value: 'inactive' },
];

const USER_ROLES = [
  { label: '学员', value: 'student' },
  { label: '讲师', value: 'instructor' },
  { label: '管理员', value: 'admin' },
];

const CLASS_STATUSES = [
  { label: '草稿', value: 'draft' },
  { label: '进行中', value: 'active' },
  { label: '已完成', value: 'completed' },
  { label: '已归档', value: 'archived' },
];

const generateId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `m-${Math.random().toString(36).slice(2, 10)}-${Date.now().toString(36)}`;
};

export function AdminOrgsPage() {
  const loadOrgs = useCallback(() => adminService.getOrganizations(), []);
  const [reloadKey, setReloadKey] = useState(0);
  const { loading, data } = useList<Organization>(loadOrgs, [reloadKey]);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<Organization | null>(null);
  const [form] = Form.useForm();

  const openCreate = () => {
    setEditing(null);
    form.resetFields();
    setOpen(true);
  };

  const openEdit = (record: Organization) => {
    setEditing(record);
    form.setFieldsValue(record);
    setOpen(true);
  };

  const handleSubmit = async (values: Partial<Organization>) => {
    if (editing) {
      await adminService.updateOrganization(editing.id, values);
    } else {
      await adminService.createOrganization(values);
    }
    setOpen(false);
    setEditing(null);
    setReloadKey((k) => k + 1);
  };

  const handleDelete = async (id: string) => {
    await adminService.deleteOrganization(id);
    setReloadKey((k) => k + 1);
  };

  const columns: ColumnsType<Organization> = [
    { title: '名称', dataIndex: 'name' },
    { title: '简称', dataIndex: 'short_name' },
    { title: '状态', dataIndex: 'status' },
    { title: 'ID', dataIndex: 'id' },
    {
      title: '操作',
      render: (_, record) => (
        <Space>
          <Button size="small" onClick={() => openEdit(record)}>
            编辑
          </Button>
          <Popconfirm title="确认删除该机构？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];
  return (
    <Card title="机构管理">
      <Space style={{ marginBottom: 12 }}>
        <Button type="primary" onClick={openCreate}>
          新增机构
        </Button>
      </Space>
      <Spin spinning={loading}>
        <Table rowKey="id" dataSource={data} columns={columns} pagination={false} />
      </Spin>
      <Modal
        title={editing ? '编辑机构' : '新增机构'}
        open={open}
        onCancel={() => setOpen(false)}
        onOk={() => form.submit()}
        destroyOnClose
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="name" label="名称" rules={[{ required: true, message: '请输入名称' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="short_name" label="简称">
            <Input />
          </Form.Item>
          <Form.Item name="status" label="状态" initialValue="active">
            <Select options={ORG_STATUSES} />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
}

export function AdminUsersPage() {
  const loadUsers = useCallback(() => api.get('/users/'), []);
  const [reloadKey, setReloadKey] = useState(0);
  const { loading, data } = useList<User>(loadUsers, [reloadKey]);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<User | null>(null);
  const [form] = Form.useForm();
  const [keyword, setKeyword] = useState('');
  const [roleFilter, setRoleFilter] = useState<string | undefined>();

  const openCreate = () => {
    setEditing(null);
    form.resetFields();
    form.setFieldsValue({ role: 'student' });
    setOpen(true);
  };

  const openEdit = (record: User) => {
    setEditing(record);
    form.setFieldsValue(record);
    setOpen(true);
  };

  const handleSubmit = async (values: Partial<User> & { password?: string }) => {
    if (editing) {
      await api.put(`/users/${editing.id}`, { name: values.name, role: values.role });
    } else {
      await api.post('/users/', {
        email: values.email,
        name: values.name,
        password: values.password,
        role: values.role,
      });
    }
    setOpen(false);
    setEditing(null);
    setReloadKey((k) => k + 1);
  };

  const handleDelete = async (id: string) => {
    await api.delete(`/users/${id}`);
    setReloadKey((k) => k + 1);
  };

  const filteredUsers = useMemo(() => {
    const term = keyword.trim().toLowerCase();
    return data.filter((user) => {
      if (roleFilter && user.role !== roleFilter) return false;
      if (!term) return true;
      return (
        user.name.toLowerCase().includes(term) ||
        user.email.toLowerCase().includes(term) ||
        user.id.toLowerCase().includes(term)
      );
    });
  }, [data, keyword, roleFilter]);

  const columns: ColumnsType<User> = [
    { title: '姓名', dataIndex: 'name' },
    { title: '邮箱', dataIndex: 'email' },
    {
      title: '角色',
      dataIndex: 'role',
      render: (value) => USER_ROLES.find((item) => item.value === value)?.label || value,
    },
    { title: '创建时间', dataIndex: 'created_at' },
    { title: 'ID', dataIndex: 'id' },
    {
      title: '操作',
      render: (_, record) => (
        <Space>
          <Button size="small" onClick={() => openEdit(record)}>
            编辑
          </Button>
          <Popconfirm title="确认删除该用户？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];
  return (
    <Card title="用户管理">
      <Space style={{ marginBottom: 12 }}>
        <Input
          placeholder="搜索姓名/邮箱/ID"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          allowClear
        />
        <Select
          placeholder="角色筛选"
          allowClear
          options={USER_ROLES}
          value={roleFilter}
          onChange={(value) => setRoleFilter(value)}
          style={{ width: 140 }}
        />
        <Button type="primary" onClick={openCreate}>
          新增用户
        </Button>
      </Space>
      <Spin spinning={loading}>
        <Table rowKey="id" dataSource={filteredUsers} columns={columns} pagination={false} />
      </Spin>
      <Modal
        title={editing ? '编辑用户' : '新增用户'}
        open={open}
        onCancel={() => setOpen(false)}
        onOk={() => form.submit()}
        destroyOnClose
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          {!editing && (
            <Form.Item name="email" label="邮箱" rules={[{ required: true, message: '请输入邮箱' }]}>
              <Input />
            </Form.Item>
          )}
          <Form.Item name="name" label="姓名" rules={[{ required: true, message: '请输入姓名' }]}>
            <Input />
          </Form.Item>
          {!editing && (
            <Form.Item name="password" label="密码" rules={[{ required: true, message: '请输入密码' }]}>
              <Input.Password />
            </Form.Item>
          )}
          <Form.Item name="role" label="角色" rules={[{ required: true, message: '请选择角色' }]}>
            <Select options={USER_ROLES} />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
}

export function AdminRolesPage() {
  const loadRoles = useCallback(() => adminService.getRoles(), []);
  const [reloadKey, setReloadKey] = useState(0);
  const { loading, data } = useList<Role>(loadRoles, [reloadKey]);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<Role | null>(null);
  const [form] = Form.useForm();

  const openCreate = () => {
    setEditing(null);
    form.resetFields();
    form.setFieldsValue({ is_enabled: true, scope: 'org' });
    setOpen(true);
  };

  const openEdit = (record: Role) => {
    setEditing(record);
    form.setFieldsValue(record);
    setOpen(true);
  };

  const handleSubmit = async (values: Partial<Role>) => {
    if (editing) {
      await adminService.updateRole(editing.id, values);
    } else {
      await adminService.createRole({
        code: values.code as string,
        name: values.name as string,
        scope: values.scope as any,
        is_enabled: values.is_enabled ?? true,
      });
    }
    setOpen(false);
    setEditing(null);
    setReloadKey((k) => k + 1);
  };

  const handleDelete = async (id: string) => {
    await adminService.deleteRole(id);
    setReloadKey((k) => k + 1);
  };

  const columns: ColumnsType<Role> = [
    { title: '编码', dataIndex: 'code' },
    { title: '名称', dataIndex: 'name' },
    { title: '范围', dataIndex: 'scope' },
    { title: '启用', dataIndex: 'is_enabled' },
    {
      title: '操作',
      render: (_, record) => (
        <Space>
          <Button size="small" onClick={() => openEdit(record)}>
            编辑
          </Button>
          <Popconfirm title="确认删除该角色？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];
  return (
    <Card title="角色管理">
      <Space style={{ marginBottom: 12 }}>
        <Button type="primary" onClick={openCreate}>
          新增角色
        </Button>
      </Space>
      <Spin spinning={loading}>
        <Table rowKey="id" dataSource={data} columns={columns} pagination={false} />
      </Spin>
      <Modal
        title={editing ? '编辑角色' : '新增角色'}
        open={open}
        onCancel={() => setOpen(false)}
        onOk={() => form.submit()}
        destroyOnClose
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          {!editing && (
            <Form.Item name="code" label="编码" rules={[{ required: true, message: '请输入编码' }]}>
              <Input />
            </Form.Item>
          )}
          <Form.Item name="name" label="名称" rules={[{ required: true, message: '请输入名称' }]}>
            <Input />
          </Form.Item>
          {!editing && (
            <Form.Item name="scope" label="范围" rules={[{ required: true, message: '请选择范围' }]}>
              <Select options={ROLE_SCOPES} />
            </Form.Item>
          )}
          <Form.Item name="is_enabled" label="启用" valuePropName="checked" initialValue>
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
}

export function AdminPermissionsPage() {
  const loadPermissions = useCallback(() => adminService.getPermissions(), []);
  const { loading, data } = useList<Permission>(loadPermissions);
  const columns: ColumnsType<Permission> = [
    { title: '模块', dataIndex: 'module' },
    { title: '动作', dataIndex: 'action' },
    { title: '编码', dataIndex: 'code' },
    { title: '名称', dataIndex: 'name' },
  ];
  return (
    <Card title="权限管理">
      <Spin spinning={loading}>
        <Table rowKey="id" dataSource={data} columns={columns} pagination={false} />
      </Spin>
    </Card>
  );
}

export function AdminMenusPage() {
  const loadMenus = useCallback(() => menuService.getMenuTree(), []);
  const [reloadKey, setReloadKey] = useState(0);
  const { loading, data } = useList<MenuItem>(loadMenus, [reloadKey]);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<MenuItem | null>(null);
  const [form] = Form.useForm();

  const menuOptions = useMemo(() => {
    const flatten = (items: MenuItem[], depth = 0): { label: string; value: string }[] =>
      items.flatMap((item) => [
        { label: `${'—'.repeat(depth)} ${item.title}`, value: item.id },
        ...flatten(item.children || [], depth + 1),
      ]);
    return flatten(data);
  }, [data]);

  const openCreate = () => {
    setEditing(null);
    form.resetFields();
    form.setFieldsValue({ is_visible: true, is_enabled: true, sort_order: 0 });
    setOpen(true);
  };

  const openEdit = (record: MenuItem) => {
    setEditing(record);
    form.setFieldsValue({ ...record, parent_id: record.parent_id || undefined });
    setOpen(true);
  };

  const handleSubmit = async (values: Partial<MenuItem>) => {
    const payload = {
      ...values,
      parent_id: values.parent_id || null,
      sort_order: Number(values.sort_order || 0),
      is_visible: values.is_visible ?? true,
      is_enabled: values.is_enabled ?? true,
    };
    if (editing) {
      await menuService.updateMenu(editing.id, payload);
    } else {
      await menuService.createMenu({
        id: generateId(),
        title: payload.title as string,
        ...payload,
      });
    }
    setOpen(false);
    setEditing(null);
    setReloadKey((k) => k + 1);
  };

  const handleDelete = async (id: string) => {
    await menuService.deleteMenu(id);
    setReloadKey((k) => k + 1);
  };

  const columns: ColumnsType<any> = [
    { title: '标题', dataIndex: 'title' },
    { title: '路径', dataIndex: 'path' },
    { title: '图标', dataIndex: 'icon' },
    { title: '排序', dataIndex: 'sort_order' },
    {
      title: '操作',
      render: (_: any, record: MenuItem) => (
        <Space>
          <Button size="small" onClick={() => openEdit(record)}>
            编辑
          </Button>
          <Popconfirm title="确认删除该菜单？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];
  return (
    <Card title="菜单管理">
      <Space style={{ marginBottom: 12 }}>
        <Button type="primary" onClick={openCreate}>
          新增菜单
        </Button>
      </Space>
      <Spin spinning={loading}>
        <Table rowKey="id" dataSource={data as any[]} columns={columns} pagination={false} />
      </Spin>
      <Modal
        title={editing ? '编辑菜单' : '新增菜单'}
        open={open}
        onCancel={() => setOpen(false)}
        onOk={() => form.submit()}
        destroyOnClose
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="title" label="标题" rules={[{ required: true, message: '请输入标题' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="path" label="路径">
            <Input />
          </Form.Item>
          <Form.Item name="icon" label="图标">
            <Input />
          </Form.Item>
          <Form.Item name="component" label="组件">
            <Input />
          </Form.Item>
          <Form.Item name="parent_id" label="父菜单">
            <Select allowClear options={menuOptions} />
          </Form.Item>
          <Form.Item name="sort_order" label="排序">
            <Input type="number" />
          </Form.Item>
          <Form.Item name="is_visible" label="可见" valuePropName="checked">
            <Switch />
          </Form.Item>
          <Form.Item name="is_enabled" label="启用" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
}

export function AdminContentsPage() {
  const loadContents = useCallback(() => adminService.getContents({}), []);
  const [reloadKey, setReloadKey] = useState(0);
  const { loading, data } = useList<ContentItem>(loadContents, [reloadKey]);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<ContentItem | null>(null);
  const [form] = Form.useForm();

  const openCreate = () => {
    setEditing(null);
    form.resetFields();
    form.setFieldsValue({ scope: 'private' });
    setOpen(true);
  };

  const openEdit = (record: ContentItem) => {
    setEditing(record);
    form.setFieldsValue(record);
    setOpen(true);
  };

  const handleSubmit = async (values: Partial<ContentItem>) => {
    if (editing) {
      await adminService.updateContent(editing.id, values);
    } else {
      await adminService.createContent({
        type: values.type as any,
        title: values.title as string,
        scope: values.scope as any,
        owner_org_id: values.owner_org_id,
      });
    }
    setOpen(false);
    setEditing(null);
    setReloadKey((k) => k + 1);
  };

  const handleDelete = async (id: string) => {
    await adminService.deleteContent(id);
    setReloadKey((k) => k + 1);
  };

  const columns: ColumnsType<ContentItem> = [
    { title: '标题', dataIndex: 'title' },
    { title: '类型', dataIndex: 'type' },
    { title: '范围', dataIndex: 'scope' },
    { title: '状态', dataIndex: 'status' },
    {
      title: '操作',
      render: (_, record) => (
        <Space>
          <Button size="small" onClick={() => openEdit(record)}>
            编辑
          </Button>
          <Popconfirm title="确认删除该内容？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];
  return (
    <Card title="内容管理">
      <Space style={{ marginBottom: 12 }}>
        <Button type="primary" onClick={openCreate}>
          新增内容
        </Button>
      </Space>
      <Spin spinning={loading}>
        <Table rowKey="id" dataSource={data} columns={columns} pagination={false} />
      </Spin>
      <Modal
        title={editing ? '编辑内容' : '新增内容'}
        open={open}
        onCancel={() => setOpen(false)}
        onOk={() => form.submit()}
        destroyOnClose
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          {!editing && (
            <Form.Item name="type" label="类型" rules={[{ required: true, message: '请选择类型' }]}>
              <Select options={CONTENT_TYPES} />
            </Form.Item>
          )}
          <Form.Item name="title" label="标题" rules={[{ required: true, message: '请输入标题' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="scope" label="范围">
            <Select options={CONTENT_SCOPES} />
          </Form.Item>
          {editing && (
            <Form.Item name="status" label="状态">
              <Select options={CONTENT_STATUSES} />
            </Form.Item>
          )}
          {!editing && (
            <Form.Item name="owner_org_id" label="所属机构ID">
              <Input />
            </Form.Item>
          )}
        </Form>
      </Modal>
    </Card>
  );
}

export function AdminClassesPage() {
  const loadClasses = useCallback(() => adminService.getClasses(), []);
  const [reloadKey, setReloadKey] = useState(0);
  const { loading, data } = useList<TrainingClass>(loadClasses, [reloadKey]);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<TrainingClass | null>(null);
  const [form] = Form.useForm();

  const openCreate = () => {
    setEditing(null);
    form.resetFields();
    form.setFieldsValue({ status: 'draft' });
    setOpen(true);
  };

  const openEdit = (record: TrainingClass) => {
    setEditing(record);
    form.setFieldsValue(record);
    setOpen(true);
  };

  const handleSubmit = async (values: Partial<TrainingClass>) => {
    if (editing) {
      await adminService.updateClass(editing.id, values);
    } else {
      await adminService.createClass({
        org_id: values.org_id as string,
        owner_id: values.owner_id as string,
        name: values.name as string,
        start_date: values.start_date,
        end_date: values.end_date,
        description: values.description,
      });
    }
    setOpen(false);
    setEditing(null);
    setReloadKey((k) => k + 1);
  };

  const handleDelete = async (id: string) => {
    await adminService.deleteClass(id);
    setReloadKey((k) => k + 1);
  };

  const columns: ColumnsType<TrainingClass> = [
    { title: '名称', dataIndex: 'name' },
    { title: '机构', dataIndex: 'org_id' },
    { title: '状态', dataIndex: 'status' },
    {
      title: '操作',
      render: (_, record) => (
        <Space>
          <Button size="small" onClick={() => openEdit(record)}>
            编辑
          </Button>
          <Popconfirm title="确认删除该班级？" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];
  return (
    <Card title="班级管理">
      <Space style={{ marginBottom: 12 }}>
        <Button type="primary" onClick={openCreate}>
          新增班级
        </Button>
      </Space>
      <Spin spinning={loading}>
        <Table rowKey="id" dataSource={data} columns={columns} pagination={false} />
      </Spin>
      <Modal
        title={editing ? '编辑班级' : '新增班级'}
        open={open}
        onCancel={() => setOpen(false)}
        onOk={() => form.submit()}
        destroyOnClose
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="name" label="名称" rules={[{ required: true, message: '请输入名称' }]}>
            <Input />
          </Form.Item>
          {!editing && (
            <>
              <Form.Item name="org_id" label="机构ID" rules={[{ required: true, message: '请输入机构ID' }]}>
                <Input />
              </Form.Item>
              <Form.Item name="owner_id" label="负责人ID" rules={[{ required: true, message: '请输入负责人ID' }]}>
                <Input />
              </Form.Item>
            </>
          )}
          <Form.Item name="status" label="状态">
            <Select options={CLASS_STATUSES} />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <Input.TextArea rows={3} />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
}

export function AdminExportsPage() {
  const loadExports = useCallback(() => adminService.listExports(), []);
  const { loading, data } = useList<ExportJob>(loadExports);
  const columns: ColumnsType<ExportJob> = [
    { title: '类型', dataIndex: 'export_type' },
    { title: '状态', dataIndex: 'status' },
    { title: '文件', dataIndex: 'file_url' },
  ];
  return (
    <Card title="导出管理">
      <Spin spinning={loading}>
        <Table rowKey="id" dataSource={data} columns={columns} pagination={false} />
      </Spin>
    </Card>
  );
}

export function AdminAuditPage() {
  const loadAuditLogs = useCallback(() => adminService.listAuditLogs(), []);
  const { loading, data } = useList<AuditLog>(loadAuditLogs);
  const columns: ColumnsType<AuditLog> = [
    { title: '动作', dataIndex: 'action' },
    { title: '资源', dataIndex: 'resource_type' },
    { title: '资源ID', dataIndex: 'resource_id' },
    { title: '时间', dataIndex: 'created_at' },
  ];
  return (
    <Card title="审计日志">
      <Spin spinning={loading}>
        <Table rowKey="id" dataSource={data} columns={columns} pagination={false} />
      </Spin>
    </Card>
  );
}

export function AdminSettingsPage() {
  return (
    <Card title="系统配置">
      <div>配置项待接入</div>
    </Card>
  );
}
