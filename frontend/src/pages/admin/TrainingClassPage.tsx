import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, DatePicker, message, Space, Tag, Col } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { format, parseISO } from 'date-fns';
import dayjs from 'dayjs';
import trainingService from '../../services/training.service';
import organizationService from '../../services/organization.service';
import { FilterForm } from '../../components/admin/FilterForm';
import type { TrainingClass } from '../../types/admin.types';

const applyClassFilters = (list: TrainingClass[], values: Record<string, any>) => {
  let filtered = [...list];

  if (values.name) {
    filtered = filtered.filter((cls) =>
      cls.name?.toLowerCase().includes(values.name.toLowerCase()),
    );
  }

  if (values.org_id) {
    filtered = filtered.filter((cls) => cls.org_id === values.org_id);
  }

  if (values.status) {
    filtered = filtered.filter((cls) => cls.status === values.status);
  }

  return filtered;
};

export function TrainingClassPage() {
  const [classes, setClasses] = useState<TrainingClass[]>([]);
  const [filteredClasses, setFilteredClasses] = useState<TrainingClass[]>([]);
  const [organizations, setOrganizations] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingClass, setEditingClass] = useState<TrainingClass | null>(null);
  const [form] = Form.useForm();
  const [filterValues, setFilterValues] = useState<Record<string, any>>({});

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [classesData, orgsData] = await Promise.all([
        trainingService.list(),
        organizationService.list(),
      ]);
      setClasses(classesData);
      setFilteredClasses(classesData);
      setOrganizations(orgsData);
    } catch (error: any) {
      message.error('加载数据失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (values: any) => {
    setFilterValues(values);
    setFilteredClasses(applyClassFilters(classes, values));
  };

  const handleReset = () => {
    setFilterValues({});
    setFilteredClasses(classes);
  };

  const handleCreate = () => {
    setEditingClass(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (cls: TrainingClass) => {
    setEditingClass(cls);
    form.setFieldsValue({
      ...cls,
      // Ant Design v5 使用 dayjs 作为日期类型
      start_date: cls.start_date ? dayjs(cls.start_date) : null,
      end_date: cls.end_date ? dayjs(cls.end_date) : null,
    });
    setModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该班级吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await trainingService.delete(id);
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
      const submitData = {
        ...values,
        start_date: values.start_date?.toISOString(),
        end_date: values.end_date?.toISOString(),
      };
      if (editingClass) {
        await trainingService.update(editingClass.id, submitData);
        message.success('更新成功');
      } else {
        await trainingService.create(submitData);
        message.success('创建成功');
      }
      setModalVisible(false);
      loadData();
    } catch (error: any) {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const statusMap: Record<string, { text: string; color: string }> = {
    draft: { text: '草稿', color: 'default' },
    active: { text: '进行中', color: 'processing' },
    completed: { text: '已完成', color: 'success' },
    archived: { text: '已归档', color: 'default' },
  };

  const valuesForOrgOptions = { ...filterValues };
  delete valuesForOrgOptions.org_id;
  const classesForOrgOptions = applyClassFilters(classes, valuesForOrgOptions);
  const availableOrgIds = new Set(
    classesForOrgOptions.map((cls) => cls.org_id).filter((orgId): orgId is string => Boolean(orgId)),
  );
  const organizationOptions = availableOrgIds.size
    ? organizations.filter((org) => availableOrgIds.has(org.id))
    : organizations;

  const valuesForStatusOptions = { ...filterValues };
  delete valuesForStatusOptions.status;
  const classesForStatusOptions = applyClassFilters(classes, valuesForStatusOptions);
  const availableStatuses = new Set(
    classesForStatusOptions.map((cls) => cls.status).filter((status): status is string => Boolean(status)),
  );
  const statusOptions = Object.entries(statusMap)
    .filter(([value]) => !availableStatuses.size || availableStatuses.has(value))
    .map(([value, info]) => ({ value, label: info.text }));

  const baseColumns = [
    {
      title: '班级名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '开始日期',
      dataIndex: 'start_date',
      key: 'start_date',
      render: (date: string) => format(parseISO(date), 'yyyy-MM-dd'),
    },
    {
      title: '结束时间',
      dataIndex: 'end_date',
      key: 'end_date',
      render: (date: string) => format(parseISO(date), 'yyyy-MM-dd'),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const statusInfo = statusMap[status] || { text: status, color: 'default' };
        return <Tag color={statusInfo.color}>{statusInfo.text}</Tag>;
      },
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: TrainingClass) => (
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
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 600, color: '#1a365d' }}>班级管理</h2>
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
            新建班级
          </Button>
        </div>
      </div>

      <FilterForm onSearch={handleSearch} onReset={handleReset} loading={loading}>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="name" label="班级名称">
            <Input placeholder="请输入" allowClear />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="org_id" label="机构">
            <Select placeholder="请选择机构" allowClear>
              {organizationOptions.map((org) => (
                <Select.Option key={org.id} value={org.id}>
                  {org.name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="status" label="状态">
            <Select placeholder="请选择" allowClear>
              {statusOptions.map((opt) => (
                <Select.Option key={opt.value} value={opt.value}>
                  {opt.label}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
      </FilterForm>

      <Table
        columns={columns}
        dataSource={filteredClasses}
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
        title={editingClass ? '编辑班级' : '新建班级'}
        open={modalVisible}
        onOk={handleSubmit}
        okText="保存"
        cancelText="取消"
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="org_id" label="机构" rules={[{ required: true }]}>
            <Select>
              {organizations.map((org) => (
                <Select.Option key={org.id} value={org.id}>
                  {org.name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item name="name" label="班级名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="description" label="描述">
            <Input.TextArea rows={3} />
          </Form.Item>
          <Form.Item name="start_date" label="开始日期">
            <DatePicker style={{ width: '100%' }} showTime />
          </Form.Item>
          <Form.Item name="end_date" label="结束时间" rules={[{ required: true }]}>
            <DatePicker style={{ width: '100%' }} showTime />
          </Form.Item>
          <Form.Item name="status" label="状态">
            <Select>
              <Select.Option value="draft">草稿</Select.Option>
              <Select.Option value="active">进行中</Select.Option>
              <Select.Option value="completed">已完成</Select.Option>
              <Select.Option value="archived">已归档</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}




