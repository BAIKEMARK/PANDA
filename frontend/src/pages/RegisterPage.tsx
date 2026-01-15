/**
 * 注册页面
 */
import { useNavigate, Link } from 'react-router-dom';
import { Form, Input, Button, Card, Typography, message } from 'antd';
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
        navigate('/login');
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

        {/* Register Card */}
        <Card
          bordered={false}
          style={{
            boxShadow: '0 8px 32px rgba(0,0,0,0.12)',
            borderRadius: '16px'
          }}
        >
          <Title level={3} style={{ marginBottom: '24px', textAlign: 'center' }}>
            注册
          </Title>

          <Form
            form={form}
            name="register"
            onFinish={onFinish}
            layout="vertical"
            size="large"
            autoComplete="off"
          >
            <Form.Item
              name="name"
              label="姓名"
              rules={[{ required: true, message: '请输入姓名' }]}
            >
              <Input
                prefix={<UserOutlined />}
                placeholder="请输入姓名"
                disabled={isLoading}
              />
            </Form.Item>

            <Form.Item
              name="email"
              label="邮箱"
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
              label="密码"
              rules={[
                { required: true, message: '请输入密码' },
                { min: 6, message: '密码长度至少为6位' }
              ]}
            >
              <Input.Password
                prefix={<LockOutlined />}
                placeholder="至少6位"
                disabled={isLoading}
              />
            </Form.Item>

            <Form.Item
              name="confirm"
              label="确认密码"
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
                placeholder="再次输入密码"
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
                注册
              </Button>
            </Form.Item>
          </Form>

          {/* Login Link */}
          <div style={{ textAlign: 'center', marginTop: '16px' }}>
            <Text>
              已有账号？{' '}
              <Link to="/login" style={{ color: '#1890ff', fontWeight: 500 }}>
                立即登录
              </Link>
            </Text>
          </div>
        </Card>
      </div>
    </div>
    </>
  );
};
