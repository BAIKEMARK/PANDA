/**
 * 个人中心页面
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Avatar, Card, Typography, Row, Col, Descriptions, Tag, Alert, Button, Modal, Form, Input, message, Space } from 'antd';
import { UserOutlined, EditOutlined, BankOutlined, LogoutOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import { useAuthStore } from '@/stores/auth.store';
import api from '@/services/api';
import { getApiErrorMessage } from '@/utils/error';

const { Title, Text } = Typography;

const roleNames: Record<string, string> = {
  student: '学员',
  instructor: '讲师',
  admin: '管理员',
};

export const ProfilePage = () => {
  const navigate = useNavigate();
  const { user, updateUser, logout } = useAuthStore();
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isPasswordModalOpen, setIsPasswordModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();
  const [passwordForm] = Form.useForm();

  if (!user) {
    return (
      <Alert
        message="未登录"
        description="请先登录"
        type="warning"
        showIcon
      />
    );
  }

  // 打开编辑弹窗
  const handleEditClick = () => {
    form.setFieldsValue({ name: user.name });
    setIsEditModalOpen(true);
  };

  // 保存个人信息
  const handleSaveProfile = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      const response = await api.put(`/users/${user.id}`, { name: values.name });
      updateUser({ ...user, name: response.data.name });
      message.success('个人信息更新成功');
      setIsEditModalOpen(false);
    } catch (error: unknown) {
      message.error(getApiErrorMessage(error, '更新失败，请稍后重试'));
    } finally {
      setLoading(false);
    }
  };

  // 修改密码
  const handleChangePassword = async () => {
    try {
      const values = await passwordForm.validateFields();
      setLoading(true);
      await api.put(`/users/${user.id}/password`, {
        old_password: values.oldPassword,
        new_password: values.newPassword,
      });
      message.success('密码修改成功，请重新登录');
      setIsPasswordModalOpen(false);
      passwordForm.resetFields();

      // 清除记住的密码
      localStorage.removeItem('login_remember');
      localStorage.removeItem('login_email');
      localStorage.removeItem('login_password');
      localStorage.removeItem('login_auto');

      // 登出并跳转到登录页
      logout();
      navigate('/login', { replace: true });
    } catch (error: unknown) {
      message.error(getApiErrorMessage(error, '密码修改失败'));
    } finally {
      setLoading(false);
    }
  };

  // 退出登录
  const handleLogout = () => {
    Modal.confirm({
      title: '确认退出',
      icon: <ExclamationCircleOutlined />,
      content: '您确定要退出登录吗？',
      okText: '确认退出',
      cancelText: '取消',
      okButtonProps: { danger: true },
      onOk: () => {
        logout();
        message.success('已退出登录');
        navigate('/login', { replace: true });
      },
    });
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <Title level={2}>个人中心</Title>
        <Text type="secondary">查看和管理您的个人信息</Text>
      </div>

      {/* Profile Card */}
      <Card style={{ marginBottom: '24px', borderRadius: '12px' }}>
        <Row gutter={24} align="middle">
          <Col>
            <Avatar
              size={80}
              style={{
                backgroundColor: '#1890ff',
                fontSize: '36px'
              }}
              icon={<UserOutlined />}
            >
              {user.name?.[0] || 'U'}
            </Avatar>
          </Col>
          <Col flex="1">
            <Title level={3} style={{ marginBottom: '8px' }}>
              {user.name}
            </Title>
            <Text type="secondary" style={{ fontSize: '15px' }}>
              {user.email}
            </Text>
            <div style={{ marginTop: '12px' }}>
              <Tag color="blue">{roleNames[user.role] || user.role}</Tag>
            </div>
          </Col>
          <Col>
            <Button
              type="primary"
              icon={<EditOutlined />}
              onClick={handleEditClick}
            >
              编辑资料
            </Button>
          </Col>
        </Row>
      </Card>

      {/* Account Details */}
      <Card
        title="账户详情"
        style={{ marginBottom: '24px', borderRadius: '12px' }}
        extra={
          <Button type="link" onClick={() => setIsPasswordModalOpen(true)}>
            修改密码
          </Button>
        }
      >
        <Descriptions column={1} bordered>
          <Descriptions.Item label="姓名">
            {user.name}
          </Descriptions.Item>
          <Descriptions.Item label="邮箱">
            {user.email}
          </Descriptions.Item>
          <Descriptions.Item label="角色">
            <Tag color="blue">{roleNames[user.role] || user.role}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="所属机构">
            {user.organizations && user.organizations.length > 0 ? (
              <Space direction="vertical" size="small">
                {user.organizations.map((org) => (
                  <Tag key={org.id} icon={<BankOutlined />} color="green">
                    {org.short_name || org.name}
                  </Tag>
                ))}
              </Space>
            ) : (
              <Tag color="default">未分配机构</Tag>
            )}
          </Descriptions.Item>
          <Descriptions.Item label="注册时间">
            {new Date(user.created_at).toLocaleDateString('zh-CN', {
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* 账户操作 */}
      <Card title="账户操作" style={{ borderRadius: '12px' }}>
        <Space direction="vertical" style={{ width: '100%' }} size="middle">
          <div style={{ padding: '12px 0', borderBottom: '1px solid #f0f0f0' }}>
            <Button
              type="primary"
              danger
              icon={<LogoutOutlined />}
              size="large"
              block
              onClick={handleLogout}
            >
              退出登录
            </Button>
          </div>
          <Text type="secondary" style={{ fontSize: '13px', textAlign: 'center', display: 'block' }}>
            退出登录后，您需要重新登录才能访问系统功能
          </Text>
        </Space>
      </Card>

      {/* 编辑资料弹窗 */}
      <Modal
        title="编辑个人资料"
        open={isEditModalOpen}
        onOk={handleSaveProfile}
        onCancel={() => setIsEditModalOpen(false)}
        confirmLoading={loading}
        okText="保存"
        cancelText="取消"
      >
        <Form form={form} layout="vertical" style={{ marginTop: '16px' }}>
          <Form.Item
            name="name"
            label="姓名"
            rules={[
              { required: true, message: '请输入姓名' },
              { min: 2, message: '姓名至少2个字符' }
            ]}
          >
            <Input placeholder="请输入姓名" />
          </Form.Item>
          <Form.Item label="邮箱">
            <Input value={user.email} disabled />
            <Text type="secondary" style={{ fontSize: '12px' }}>
              邮箱不可修改
            </Text>
          </Form.Item>
        </Form>
      </Modal>

      {/* 修改密码弹窗 */}
      <Modal
        title="修改密码"
        open={isPasswordModalOpen}
        onOk={handleChangePassword}
        onCancel={() => {
          setIsPasswordModalOpen(false);
          passwordForm.resetFields();
        }}
        confirmLoading={loading}
        okText="确认修改"
        cancelText="取消"
      >
        <Form form={passwordForm} layout="vertical" style={{ marginTop: '16px' }}>
          <Form.Item
            name="oldPassword"
            label="当前密码"
            rules={[{ required: true, message: '请输入当前密码' }]}
          >
            <Input.Password placeholder="请输入当前密码" />
          </Form.Item>
          <Form.Item
            name="newPassword"
            label="新密码"
            rules={[
              { required: true, message: '请输入新密码' },
              { min: 6, message: '密码至少6位' }
            ]}
          >
            <Input.Password placeholder="请输入新密码（至少6位）" />
          </Form.Item>
          <Form.Item
            name="confirmPassword"
            label="确认新密码"
            dependencies={['newPassword']}
            rules={[
              { required: true, message: '请确认新密码' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('newPassword') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('两次输入的密码不一致'));
                },
              }),
            ]}
          >
            <Input.Password placeholder="请再次输入新密码" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};
