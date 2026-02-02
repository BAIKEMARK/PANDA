import { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Space, Tag } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import questionService from '../../services/question.service';
import type { Question } from '../../types/admin.types';

export function QuestionBankPage() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState<Question | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    setLoading(true);
    try {
      const data = await questionService.list();
      setQuestions(data);
    } catch (error: any) {
      message.error('加载题目列表失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setEditingQuestion(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (question: Question) => {
    setEditingQuestion(question);
    form.setFieldsValue({
      ...question,
      options: question.options?.join('\n') || '',
      correct_answer: question.correct_answer?.join('\n') || '',
      knowledge_tags: question.knowledge_tags?.join(',') || '',
    });
    setModalVisible(true);
  };

  const handleDelete = async (id: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这道题目吗？',
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
      const submitData = {
        ...values,
        options: values.options.split('\n').filter((s: string) => s.trim()),
        correct_answer: values.correct_answer.split('\n').filter((s: string) => s.trim()),
        knowledge_tags: values.knowledge_tags ? values.knowledge_tags.split(',').map((s: string) => s.trim()) : [],
      };
      
      if (editingQuestion) {
        await questionService.update(editingQuestion.id, submitData);
        message.success('更新成功');
      } else {
        await questionService.create(submitData);
        message.success('创建成功');
      }
      setModalVisible(false);
      loadQuestions();
    } catch (error: any) {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const columns = [
    {
      title: '题型',
      dataIndex: 'question_type',
      key: 'question_type',
      render: (type: string) => {
        const typeMap: Record<string, string> = {
          single: '单选题',
          multiple: '多选题',
          judge: '判断题',
        };
        return <Tag>{typeMap[type] || type}</Tag>;
      },
    },
    {
      title: '题干',
      dataIndex: 'question_text',
      key: 'question_text',
      ellipsis: true,
    },
    {
      title: '难度',
      dataIndex: 'difficulty',
      key: 'difficulty',
      render: (difficulty: string) => {
        const colorMap: Record<string, string> = {
          easy: 'green',
          medium: 'orange',
          hard: 'red',
        };
        const textMap: Record<string, string> = {
          easy: '简单',
          medium: '中等',
          hard: '困难',
        };
        return <Tag color={colorMap[difficulty]}>{textMap[difficulty] || difficulty}</Tag>;
      },
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'default'}>
          {status === 'active' ? '启用' : status === 'draft' ? '草稿' : '禁用'}
        </Tag>
      ),
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

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between' }}>
        <h2>题库管理</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
          新建题目
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={questions}
        loading={loading}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />

      <Modal
        title={editingQuestion ? '编辑题目' : '新建题目'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => setModalVisible(false)}
        width={800}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="question_type" label="题型" rules={[{ required: true }]}>
            <Select>
              <Select.Option value="single">单选题</Select.Option>
              <Select.Option value="multiple">多选题</Select.Option>
              <Select.Option value="judge">判断题</Select.Option>
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
          <Form.Item name="knowledge_tags" label="知识点标签（逗号分隔）">
            <Input placeholder="标签1,标签2,标签3" />
          </Form.Item>
          <Form.Item name="status" label="状态" initialValue="draft">
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
