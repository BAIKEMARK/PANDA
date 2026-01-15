/**
 * 登录页面
 */
import { useNavigate, Link } from 'react-router-dom';
import { Form, Input, Button, Card, Typography } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useAuthStore } from '@/stores/auth.store';
import type { FormProps } from 'antd';

const { Title, Text } = Typography;

export const LoginPage = () => {
  const navigate = useNavigate();
  const { login, isLoading } = useAuthStore();
  const [form] = Form.useForm();

  const onFinish: FormProps['onFinish'] = async (values) => {
    try {
      await login(values.email, values.password);
      navigate('/courses');
    } catch (error: any) {
      form.setFields([
        {
          name: 'password',
          errors: [error.response?.data?.detail || '登录失败，请检查邮箱和密码'],
        },
      ]);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div style={{ maxWidth: '400px', width: '100%' }}>
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <Title level={2} style={{ color: '#fff', marginBottom: '8px' }}>
            PANDA
          </Title>
          <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: '16px' }}>
            围产期抑郁管理智能培训系统
          </Text>
        </div>

        {/* Login Card */}
        <Card
          bordered={false}
          style={{
            boxShadow: '0 8px 32px rgba(0,0,0,0.12)',
            borderRadius: '16px'
          }}
        >
          <Title level={3} style={{ marginBottom: '24px', textAlign: 'center' }}>
            登录
          </Title>

          <Form
            form={form}
            name="login"
            onFinish={onFinish}
            layout="vertical"
            size="large"
            autoComplete="off"
          >
            <Form.Item
              name="email"
              rules={[
                { required: true, message: '请输入邮箱' },
                { type: 'email', message: '请输入有效的邮箱地址' }
              ]}
            >
              <Input
                prefix={<UserOutlined />}
                placeholder="邮箱地址"
                disabled={isLoading}
              />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[{ required: true, message: '请输入密码' }]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="密码"
                disabled={isLoading}
              />
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                loading={isLoading}
                block
                style={{ height: '44px' }}
              >
                登录
              </Button>
            </Form.Item>
          </Form>

          {/* Register Link */}
          <div style={{ textAlign: 'center', marginTop: '16px' }}>
            <Text>
              还没有账号？{' '}
              <Link to="/register" style={{ color: '#1890ff', fontWeight: 500 }}>
                立即注册
              </Link>
            </Text>
          </div>
        </Card>
      </div>
    </div>
  );
};