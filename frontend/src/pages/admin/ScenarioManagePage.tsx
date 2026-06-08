import { useCallback, useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Space, Col, Tag } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, CheckCircleOutlined, StopOutlined } from '@ant-design/icons';
import scenarioAdminService from '../../services/scenario-admin.service';
import type { Scenario } from '../../services/scenario-admin.service';
import organizationService from '../../services/organization.service';
import { FilterForm } from '../../components/admin/FilterForm';
import { getApiErrorMessage } from '../../utils/error';
import { getFilterValue } from '../../utils/filters';
import type { Organization } from '../../types/admin.types';

const { TextArea } = Input;

export function ScenarioManagePage() {
  const [filteredScenarios, setFilteredScenarios] = useState<Scenario[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingScenario, setEditingScenario] = useState<Scenario | null>(null);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [form] = Form.useForm();
  const [filterValues, setFilterValues] = useState<Record<string, unknown>>({});
  const [pagination, setPagination] = useState({ current: 1, pageSize: 10, total: 0 });
  const { current, pageSize } = pagination;

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      // 构建查询参数，包含分页和筛选条件
      const params: Record<string, string | number> = {
        skip: (current - 1) * pageSize,
        limit: pageSize,
      };
      // 添加筛选条件（后端支持的参数：difficulty, scope, status）
      const difficulty = getFilterValue(filterValues, 'difficulty');
      const scope = getFilterValue(filterValues, 'scope');
      const status = getFilterValue(filterValues, 'status');
      if (difficulty) params.difficulty = difficulty;
      if (scope) params.scope = scope;
      if (status) params.status = status;

      const [scenariosData, orgsData] = await Promise.all([
        scenarioAdminService.list(params),
        organizationService.list(),
      ]);
      setFilteredScenarios(scenariosData.scenarios);
      setOrganizations(orgsData);
      setPagination(prev => ({ ...prev, total: scenariosData.total }));
    } catch (error: unknown) {
      message.error('加载数据失败: ' + getApiErrorMessage(error));
    } finally {
      setLoading(false);
    }
  }, [current, filterValues, pageSize]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSearch = (values: Record<string, unknown>) => {
    setFilterValues(values);
    setPagination(prev => ({ ...prev, current: 1 }));
  };

  const handleReset = () => {
    setFilterValues({});
    setPagination({ current: 1, pageSize: 10, total: 0 });
  };

  const handleCreate = () => {
    setEditingScenario(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (scenario: Scenario) => {
    setEditingScenario(scenario);
    form.setFieldsValue(scenario);
    setModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该场景吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await scenarioAdminService.delete(id);
          message.success('删除成功');
          loadData();
        } catch (error: unknown) {
          message.error('删除失败: ' + getApiErrorMessage(error));
        }
      },
    });
  };

  const handlePublish = async (id: string) => {
    try {
      await scenarioAdminService.publish(id);
      message.success('发布成功');
      loadData();
    } catch (error: unknown) {
      message.error('发布失败: ' + getApiErrorMessage(error));
    }
  };

  const handleArchive = async (id: string) => {
    Modal.confirm({
      title: '确认下线',
      content: '确定要下线该场景吗？',
      okText: '下线',
      cancelText: '取消',
      onOk: async () => {
        try {
          await scenarioAdminService.archive(id);
          message.success('下线成功');
          loadData();
        } catch (error: unknown) {
          message.error('下线失败: ' + getApiErrorMessage(error));
        }
      },
    });
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      if (editingScenario) {
        await scenarioAdminService.update(editingScenario.id, values);
        message.success('更新成功');
      } else {
        await scenarioAdminService.create(values);
        message.success('创建成功');
      }
      setModalVisible(false);
      loadData();
    } catch (error: unknown) {
      message.error('操作失败: ' + getApiErrorMessage(error));
    }
  };

  const columns = [
    {
      title: '场景标题',
      dataIndex: 'title',
      key: 'title',
      align: 'center' as const,
    },
    {
      title: '难度等级',
      dataIndex: 'difficulty',
      key: 'difficulty',
      align: 'center' as const,
      render: (difficulty: number) => {
        const colors = ['', 'green', 'blue', 'orange', 'red', 'purple'];
        return <Tag color={colors[difficulty] || 'default'}>{difficulty}</Tag>;
      },
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
      title: '时间节点',
      dataIndex: 'time_period',
      key: 'time_period',
      align: 'center' as const,
    },
    {
      title: '操作',
      key: 'action',
      align: 'center' as const,
      render: (_: unknown, record: Scenario) => (
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
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 600, color: '#1a365d' }}>场景管理</h2>
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
          新建场景
        </Button>
      </div>

      <FilterForm onSearch={handleSearch} onReset={handleReset} loading={loading}>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="difficulty" label="难度等级">
            <Select placeholder="请选择难度" allowClear>
              <Select.Option value={1}>1</Select.Option>
              <Select.Option value={2}>2</Select.Option>
              <Select.Option value={3}>3</Select.Option>
              <Select.Option value={4}>4</Select.Option>
              <Select.Option value={5}>5</Select.Option>
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
        dataSource={filteredScenarios}
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
        title={editingScenario ? '编辑场景' : '新建场景'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => setModalVisible(false)}
        width={800}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="title" label="场景标题" rules={[{ required: true, message: '请输入场景标题' }]}>
            <Input placeholder="请输入场景标题" />
          </Form.Item>
          <Form.Item name="description" label="场景描述">
            <TextArea rows={3} placeholder="请输入场景描述" />
          </Form.Item>
          <Form.Item name="system_prompt" label="AI系统提示词" rules={[{ required: true, message: '请输入AI系统提示词' }]}>
            <TextArea rows={6} placeholder="请输入AI系统提示词" />
          </Form.Item>
          <Form.Item name="patient_background" label="患者背景信息">
            <TextArea rows={4} placeholder="请输入患者背景信息" />
          </Form.Item>
          <Form.Item name="knowledge_tags" label="知识点标签">
            <Input placeholder="请输入知识点标签，多个标签用逗号分隔" />
          </Form.Item>
          <Form.Item name="difficulty" label="难度等级" initialValue={1} rules={[{ required: true, message: '请选择难度等级' }]}>
            <Select>
              <Select.Option value={1}>1</Select.Option>
              <Select.Option value={2}>2</Select.Option>
              <Select.Option value={3}>3</Select.Option>
              <Select.Option value={4}>4</Select.Option>
              <Select.Option value={5}>5</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="time_period" label="时间节点">
            <Input placeholder="例如：产后2周" />
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
