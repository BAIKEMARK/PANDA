/**
 * 注册页面
 */
import { useNavigate, Link } from 'react-router-dom';
import { Form, Input, Button, Card, Typography, Space, message } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons';
import { useAuthStore } from '@/stores/auth.store';
import type { FormProps } from 'antd';

const { Title, Text } = Typography;

export const RegisterPage = () => {
  const navigate = useNavigate();
  const { register, isLoading } = useAuthStore();
  const [form] = Form.useForm();
  const [messageApi, contextHolder] = message.useMessage();

  const onFinish: FormProps['onFinish'] = async (values) => {
    try {
      await register(values.email, values.name, values.password);
      messageApi.success('注册成功！请登录');
      setTimeout(() => {
        navigate('/login', { 
          state: { 
            registeredEmail: values.email,
            registeredPassword: values.password 
          } 
        });
      }, 1000);
    } catch (error: any) {
      form.setFields([
        {
          name: 'email',
          errors: [error.response?.data?.detail || '注册失败，请稍后重试'],
        },
      ]);
    }
  };

  return (
    <>
      {contextHolder}
      <div style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '24px 16px',
      }}>
        {/* Logo */}
        <Space direction="vertical" align="center" size={4} style={{ marginBottom: 24 }}>
          <Title level={2} style={{ color: '#fff', margin: 0, letterSpacing: 2 }}>
            PANDA
          </Title>
          <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: 14 }}>
            围产期抑郁管理智能培训系统
          </Text>
        </Space>

        {/* Register Card */}
        <Card
          bordered={false}
          style={{
            width: '100%',
            maxWidth: 380,
            borderRadius: 12,
            boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
          }}
          styles={{ body: { padding: '32px 28px 24px' } }}
        >
          <Title level={4} style={{ textAlign: 'center', marginBottom: 24 }}>
            注册
          </Title>

          <Form
            form={form}
            name="register"
            onFinish={onFinish}
            autoComplete="off"
            size="large"
          >
            <Form.Item
              name="name"
              rules={[
                { required: true, message: '请输入姓名' },
                { min: 2, message: '姓名至少2个字符' }
              ]}
            >
              <Input
                prefix={<UserOutlined />}
                placeholder="姓名"
                disabled={isLoading}
              />
            </Form.Item>

            <Form.Item
              name="email"
              rules={[
                { required: true, message: '请输入邮箱' },
                { type: 'email', message: '请输入有效的邮箱地址' }
              ]}
            >
              <Input
                prefix={<MailOutlined />}
                placeholder="邮箱地址"
                disabled={isLoading}
              />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[
                { required: true, message: '请输入密码' },
                { min: 6, message: '密码至少6位' }
              ]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="密码（至少6位）"
                disabled={isLoading}
              />
            </Form.Item>

            <Form.Item
              name="confirm"
              dependencies={['password']}
              rules={[
                { required: true, message: '请确认密码' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('password') === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('两次输入的密码不一致'));
                  },
                }),
              ]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="确认密码"
                disabled={isLoading}
              />
            </Form.Item>

            <Form.Item style={{ marginBottom: 16 }}>
              <Button
                type="primary"
                htmlType="submit"
                loading={isLoading}
                block
                style={{ height: 44 }}
              >
                注 册
              </Button>
            </Form.Item>

            <div style={{ textAlign: 'center' }}>
              <Text type="secondary">已有账号？</Text>
              <Link to="/login" style={{ marginLeft: 4 }}>立即登录</Link>
            </div>
          </Form>
        </Card>

        {/* Footer */}
        <Text style={{ color: 'rgba(255,255,255,0.6)', fontSize: 12, marginTop: 24 }}>
          © 2025 PANDA Training System
        </Text>
      </div>
    </>
  );
};
