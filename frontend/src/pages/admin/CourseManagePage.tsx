import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Space, Col, Tag } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, CheckCircleOutlined, StopOutlined } from '@ant-design/icons';
import courseAdminService from '../../services/course-admin.service';
import type { Course } from '../../services/course-admin.service';
import organizationService from '../../services/organization.service';
import { FilterForm } from '../../components/admin/FilterForm';
import type { Organization } from '../../types/admin.types';

const { TextArea } = Input;

export function CourseManagePage() {
  const [filteredCourses, setFilteredCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingCourse, setEditingCourse] = useState<Course | null>(null);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [form] = Form.useForm();
  const [filterValues, setFilterValues] = useState<Record<string, any>>({});
  const [pagination, setPagination] = useState({ current: 1, pageSize: 10, total: 0 });

  useEffect(() => {
    loadData();
  }, [pagination.current, pagination.pageSize]);

  const loadData = async () => {
    setLoading(true);
    try {
      // 构建查询参数，包含分页和筛选条件
      const params: Record<string, any> = {
        skip: (pagination.current - 1) * pagination.pageSize,
        limit: pagination.pageSize,
      };
      // 添加筛选条件（后端支持的参数：level, scope, status）
      if (filterValues.level) params.level = filterValues.level;
      if (filterValues.scope) params.scope = filterValues.scope;
      if (filterValues.status) params.status = filterValues.status;

      const [coursesData, orgsData] = await Promise.all([
        courseAdminService.list(params),
        organizationService.list(),
      ]);
      setFilteredCourses(coursesData.courses);
      setOrganizations(orgsData);
      setPagination(prev => ({ ...prev, total: coursesData.total }));
    } catch (error: any) {
      message.error('加载数据失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (values: any) => {
    setFilterValues(values);
    loadData();
  };

  const handleReset = () => {
    setFilterValues({});
    setPagination({ current: 1, pageSize: 10, total: 0 });
    loadData();
  };

  const handleCreate = () => {
    setEditingCourse(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (course: Course) => {
    setEditingCourse(course);
    form.setFieldsValue(course);
    setModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该课程吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await courseAdminService.delete(id);
          message.success('删除成功');
          loadData();
        } catch (error: any) {
          message.error('删除失败: ' + (error.response?.data?.detail || error.message));
        }
      },
    });
  };

  const handlePublish = async (id: string) => {
    try {
      await courseAdminService.publish(id);
      message.success('发布成功');
      loadData();
    } catch (error: any) {
      message.error('发布失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleArchive = async (id: string) => {
    Modal.confirm({
      title: '确认下线',
      content: '确定要下线该课程吗？',
      okText: '下线',
      cancelText: '取消',
      onOk: async () => {
        try {
          await courseAdminService.archive(id);
          message.success('下线成功');
          loadData();
        } catch (error: any) {
          message.error('下线失败: ' + (error.response?.data?.detail || error.message));
        }
      },
    });
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      if (editingCourse) {
        await courseAdminService.update(editingCourse.id, values);
        message.success('更新成功');
      } else {
        await courseAdminService.create(values);
        message.success('创建成功');
      }
      setModalVisible(false);
      loadData();
    } catch (error: any) {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const columns = [
    {
      title: '课程标题',
      dataIndex: 'title',
      key: 'title',
      align: 'center' as const,
    },
    {
      title: 'THP层级',
      dataIndex: 'level',
      key: 'level',
      align: 'center' as const,
      render: (level: string) => <Tag color="blue">{level}</Tag>,
    },
    {
      title: '发布范围',
      dataIndex: 'scope',
      key: 'scope',
      align: 'center' as const,
      render: (scope: string) => {
        const scopeMap: Record<string, { text: string; color: string }> = {
          private: { text: '私有', color: 'default' },
          platform: { text: '平台', color: 'blue' },
          shared: { text: '共享', color: 'green' },
        };
        const item = scopeMap[scope] || { text: scope, color: 'default' };
        return <Tag color={item.color}>{item.text}</Tag>;
      },
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      align: 'center' as const,
      render: (status: string) => {
        const statusMap: Record<string, { text: string; color: string }> = {
          draft: { text: '草稿', color: 'default' },
          pending: { text: '待发布', color: 'orange' },
          published: { text: '已发布', color: 'green' },
          archived: { text: '已下线', color: 'red' },
        };
        const item = statusMap[status] || { text: status, color: 'default' };
        return <Tag color={item.color}>{item.text}</Tag>;
      },
    },
    {
      title: '排序',
      dataIndex: 'sort_order',
      key: 'sort_order',
      align: 'center' as const,
    },
    {
      title: '操作',
      key: 'action',
      align: 'center' as const,
      render: (_: any, record: Course) => (
        <Space>
          <Button type="link" icon={<EditOutlined />} onClick={() => handleEdit(record)}>
            编辑
          </Button>
          {record.status === 'published' ? (
            <Button type="link" danger icon={<StopOutlined />} onClick={() => handleArchive(record.id)}>
              下线
            </Button>
          ) : (
            <Button type="link" icon={<CheckCircleOutlined />} onClick={() => handlePublish(record.id)}>
              发布
            </Button>
          )}
          <Button type="link" danger icon={<DeleteOutlined />} onClick={() => handleDelete(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 600, color: '#1a365d' }}>课程管理</h2>
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
          新建课程
        </Button>
      </div>

      <FilterForm onSearch={handleSearch} onReset={handleReset} loading={loading}>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="level" label="THP层级">
            <Select placeholder="请选择层级" allowClear>
              <Select.Option value="L1">L1</Select.Option>
              <Select.Option value="L2">L2</Select.Option>
              <Select.Option value="L3">L3</Select.Option>
              <Select.Option value="L4">L4</Select.Option>
            </Select>
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="scope" label="发布范围">
            <Select placeholder="请选择范围" allowClear>
              <Select.Option value="private">私有</Select.Option>
              <Select.Option value="platform">平台</Select.Option>
              <Select.Option value="shared">共享</Select.Option>
            </Select>
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="status" label="状态">
            <Select placeholder="请选择状态" allowClear>
              <Select.Option value="draft">草稿</Select.Option>
              <Select.Option value="pending">待发布</Select.Option>
              <Select.Option value="published">已发布</Select.Option>
              <Select.Option value="archived">已下线</Select.Option>
            </Select>
          </Form.Item>
        </Col>
      </FilterForm>

      <Table
        columns={columns}
        dataSource={filteredCourses}
        rowKey="id"
        loading={loading}
        pagination={{
          current: pagination.current,
          pageSize: pagination.pageSize,
          total: pagination.total,
          onChange: (page, pageSize) => {
            setPagination(prev => ({ ...prev, current: page, pageSize: pageSize || 10 }));
          },
        }}
      />

      <Modal
        title={editingCourse ? '编辑课程' : '新建课程'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => setModalVisible(false)}
        width={800}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="title" label="课程标题" rules={[{ required: true, message: '请输入课程标题' }]}>
            <Input placeholder="请输入课程标题" />
          </Form.Item>
          <Form.Item name="level" label="THP层级" rules={[{ required: true, message: '请选择THP层级' }]}>
            <Select placeholder="请选择层级">
              <Select.Option value="L1">L1</Select.Option>
              <Select.Option value="L2">L2</Select.Option>
              <Select.Option value="L3">L3</Select.Option>
              <Select.Option value="L4">L4</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="description" label="课程描述">
            <TextArea rows={4} placeholder="请输入课程描述" />
          </Form.Item>
          <Form.Item name="content_url" label="课件PDF URL">
            <Input placeholder="请输入课件PDF URL" />
          </Form.Item>
          <Form.Item name="video_url" label="视频URL">
            <Input placeholder="请输入视频URL" />
          </Form.Item>
          <Form.Item name="sort_order" label="排序顺序" initialValue={0}>
            <Input type="number" placeholder="请输入排序顺序" />
          </Form.Item>
          <Form.Item name="scope" label="发布范围" initialValue="private">
            <Select>
              <Select.Option value="private">私有</Select.Option>
              <Select.Option value="platform">平台</Select.Option>
              <Select.Option value="shared">共享</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="org_id" label="机构">
            <Select placeholder="请选择机构" allowClear>
              {organizations.map(org => (
                <Select.Option key={org.id} value={org.id}>
                  {org.name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item name="version" label="版本号" initialValue="1.0.0">
            <Input placeholder="请输入版本号" />
          </Form.Item>
          <Form.Item name="version_notes" label="版本说明">
            <TextArea rows={2} placeholder="请输入版本说明" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
