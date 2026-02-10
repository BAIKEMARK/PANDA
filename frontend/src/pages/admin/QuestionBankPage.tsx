import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Space, Tag, Col } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import questionService from '../../services/question.service';
import { FilterForm } from '../../components/admin/FilterForm';
import type { Question } from '../../types/admin.types';

const applyQuestionFilters = (list: Question[], values: Record<string, any>) => {
  let filtered = [...list];

  if (values.question_text) {
    filtered = filtered.filter((question) =>
      question.question_text?.toLowerCase().includes(values.question_text.toLowerCase()),
    );
  }

  if (values.question_type) {
    filtered = filtered.filter((question) => question.question_type === values.question_type);
  }

  if (values.difficulty) {
    filtered = filtered.filter((question) => question.difficulty === values.difficulty);
  }

  if (values.status) {
    filtered = filtered.filter((question) => question.status === values.status);
  }

  return filtered;
};

export function QuestionBankPage() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [filteredQuestions, setFilteredQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState<Question | null>(null);
  const [form] = Form.useForm();
  const [filterValues, setFilterValues] = useState<Record<string, any>>({});

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    setLoading(true);
    try {
      const data = await questionService.list();
      setQuestions(data);
      setFilteredQuestions(data);
    } catch (error: any) {
      message.error('加载题目列表失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (values: any) => {
    setFilterValues(values);
    setFilteredQuestions(applyQuestionFilters(questions, values));
  };

  const handleReset = () => {
    setFilterValues({});
    setFilteredQuestions(questions);
  };

  const valuesForTypeOptions = { ...filterValues };
  delete valuesForTypeOptions.question_type;
  const questionsForTypeOptions = applyQuestionFilters(questions, valuesForTypeOptions);
  const availableTypes = new Set(
    questionsForTypeOptions
      .map((question) => question.question_type)
      .filter((value): value is string => Boolean(value)),
  );
  const valuesForDifficultyOptions = { ...filterValues };
  delete valuesForDifficultyOptions.difficulty;
  const questionsForDifficultyOptions = applyQuestionFilters(questions, valuesForDifficultyOptions);
  const availableDifficulties = new Set(
    questionsForDifficultyOptions
      .map((question) => question.difficulty)
      .filter((value): value is string => Boolean(value)),
  );
  const valuesForStatusOptions = { ...filterValues };
  delete valuesForStatusOptions.status;
  const questionsForStatusOptions = applyQuestionFilters(questions, valuesForStatusOptions);
  const availableStatuses = new Set(
    questionsForStatusOptions.map((question) => question.status).filter((value): value is string => Boolean(value)),
  );
  const typeOptions = [
    { value: 'single', label: '单选' },
    { value: 'multiple', label: '多选' },
    { value: 'judge', label: '判断' },
  ].filter((option) => !availableTypes.size || availableTypes.has(option.value));
  const difficultyOptions = [
    { value: 'easy', label: '简单' },
    { value: 'medium', label: '中等' },
    { value: 'hard', label: '困难' },
  ].filter((option) => !availableDifficulties.size || availableDifficulties.has(option.value));
  const statusOptions = [
    { value: 'draft', label: '草稿' },
    { value: 'active', label: '启用' },
    { value: 'disabled', label: '禁用' },
  ].filter((option) => !availableStatuses.size || availableStatuses.has(option.value));

  const normalizeLines = (value?: string) =>
    (value || '')
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean);

  const normalizeTags = (value?: string) =>
    (value || '')
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);

  const handleCreate = () => {
    setEditingQuestion(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (question: Question) => {
    setEditingQuestion(question);
    form.setFieldsValue({
      ...question,
      options: (question.options || []).join('\n'),
      correct_answer: (question.correct_answer || []).join('\n'),
      knowledge_tags: (question.knowledge_tags || []).join(','),
    });
    setModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除该题目吗？',
      okText: '删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          await questionService.delete(id);
          message.success('删除成功');
          loadQuestions();
        } catch (error: any) {
          message.error('删除失败: ' + (error.response?.data?.detail || error.message));
        }
      },
    });
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      const payload = {
        ...values,
        options: normalizeLines(values.options),
        correct_answer: normalizeLines(values.correct_answer),
        knowledge_tags: values.knowledge_tags ? normalizeTags(values.knowledge_tags) : undefined,
      };
      if (editingQuestion) {
        await questionService.update(editingQuestion.id, payload);
        message.success('更新成功');
      } else {
        await questionService.create(payload);
        message.success('创建成功');
      }
      setModalVisible(false);
      loadQuestions();
    } catch (error: any) {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message));
    }
  };
  const baseColumns = [
    {
      title: '题干',
      dataIndex: 'question_text',
      key: 'question_text',
      ellipsis: true,
    },
    {
      title: '题型',
      dataIndex: 'question_type',
      key: 'question_type',
      render: (value: string) => {
        const map: Record<string, string> = { single: '单选', multiple: '多选', judge: '判断' };
        return map[value] || value;
      },
    },
    {
      title: '难度',
      dataIndex: 'difficulty',
      key: 'difficulty',
      render: (value: string) => {
        const map: Record<string, string> = { easy: '简单', medium: '中等', hard: '困难' };
        return map[value] || value;
      },
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (value: string) => {
        const map: Record<string, string> = { draft: '草稿', active: '启用', disabled: '禁用' };
        const colorMap: Record<string, string> = { draft: 'orange', active: 'green', disabled: 'red' };
        return <Tag color={colorMap[value] || 'default'}>{map[value] || value}</Tag>;
      },
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Question) => (
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
        <h2 style={{ margin: 0, fontSize: '24px', fontWeight: 600, color: '#1a365d' }}>题库管理</h2>
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
            新建题目
          </Button>
        </div>
      </div>

      <FilterForm onSearch={handleSearch} onReset={handleReset} loading={loading}>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="question_text" label="题干">
            <Input placeholder="请输入题干关键词" allowClear />
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="question_type" label="题型">
            <Select placeholder="请选择题型" allowClear>
              {typeOptions.map((option) => (
                <Select.Option key={option.value} value={option.value}>
                  {option.label}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="difficulty" label="难度">
            <Select placeholder="请选择难度" allowClear>
              {difficultyOptions.map((option) => (
                <Select.Option key={option.value} value={option.value}>
                  {option.label}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
        </Col>
        <Col xs={24} sm={12} md={8} lg={6}>
          <Form.Item name="status" label="状态">
            <Select placeholder="请选择" allowClear>
              {statusOptions.map((option) => (
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
        dataSource={filteredQuestions}
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
        title={editingQuestion ? '编辑题目' : '新建题目'}
        open={modalVisible}
        onOk={handleSubmit}
        okText="保存"
        cancelText="取消"
        onCancel={() => setModalVisible(false)}
        width={800}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="question_type" label="题型" rules={[{ required: true }]}>
            <Select>
              <Select.Option value="single">单选</Select.Option>
              <Select.Option value="multiple">多选</Select.Option>
              <Select.Option value="judge">判断</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="question_text" label="题干" rules={[{ required: true }]}>
            <Input.TextArea rows={3} />
          </Form.Item>
          <Form.Item name="options" label="选项（每行一个）" rules={[{ required: true }]}>
            <Input.TextArea rows={4} placeholder="A. 选项1&#10;B. 选项2&#10;C. 选项3" />
          </Form.Item>
          <Form.Item name="correct_answer" label="正确答案（每行一个）" rules={[{ required: true }]}>
            <Input.TextArea rows={2} placeholder="A&#10;B" />
          </Form.Item>
          <Form.Item name="explanation" label="解析">
            <Input.TextArea rows={2} />
          </Form.Item>
          <Form.Item name="difficulty" label="难度" initialValue="medium">
            <Select>
              <Select.Option value="easy">简单</Select.Option>
              <Select.Option value="medium">中等</Select.Option>
              <Select.Option value="hard">困难</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item name="knowledge_tags" label="知识点标签">
            <Input placeholder="标签1,标签2,标签3" />
          </Form.Item>
          <Form.Item name="status" label="状态">
            <Select>
              <Select.Option value="draft">草稿</Select.Option>
              <Select.Option value="active">启用</Select.Option>
              <Select.Option value="disabled">禁用</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}




