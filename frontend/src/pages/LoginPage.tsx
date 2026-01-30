/**
 * 登录页面
 */
import { useEffect } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { Form, Input, Button, Card, Checkbox, Typography, Space } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useAuthStore } from '@/stores/auth.store';
import type { FormProps } from 'antd';

const { Title, Text } = Typography;

// localStorage keys
const REMEMBER_KEY = 'login_remember';
const AUTO_LOGIN_KEY = 'login_auto';
const SAVED_EMAIL_KEY = 'login_email';
const SAVED_PASSWORD_KEY = 'login_password';

interface LoginFormValues {
  email: string;
  password: string;
  remember: boolean;
  autoLogin: boolean;
}

export const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isLoading } = useAuthStore();
  const [form] = Form.useForm<LoginFormValues>();

  const from = (location.state as { from?: string })?.from || '/courses';
  const registeredEmail = (location.state as { registeredEmail?: string })?.registeredEmail;
  const registeredPassword = (location.state as { registeredPassword?: string })?.registeredPassword;

  useEffect(() => {
    if (registeredEmail && registeredPassword) {
      form.setFieldsValue({
        email: registeredEmail,
        password: registeredPassword,
        remember: false,
        autoLogin: false,
      });
      return;
    }

    const remember = localStorage.getItem(REMEMBER_KEY) === 'true';
    const autoLogin = localStorage.getItem(AUTO_LOGIN_KEY) === 'true';
    
    if (remember) {
      const savedEmail = localStorage.getItem(SAVED_EMAIL_KEY) || '';
      const savedPassword = localStorage.getItem(SAVED_PASSWORD_KEY) || '';
      
      form.setFieldsValue({
        email: savedEmail,
        password: savedPassword,
        remember: true,
        autoLogin: autoLogin,
      });

      if (autoLogin && savedEmail && savedPassword) {
        handleAutoLogin(savedEmail, savedPassword);
      }
    }
  }, []);

  const handleAutoLogin = async (email: string, password: string) => {
    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch {
      localStorage.setItem(AUTO_LOGIN_KEY, 'false');
    }
  };

  const onFinish: FormProps<LoginFormValues>['onFinish'] = async (values) => {
    try {
      await login(values.email, values.password);
      
      if (values.remember) {
        localStorage.setItem(REMEMBER_KEY, 'true');
        localStorage.setItem(SAVED_EMAIL_KEY, values.email);
        localStorage.setItem(SAVED_PASSWORD_KEY, values.password);
        localStorage.setItem(AUTO_LOGIN_KEY, values.autoLogin ? 'true' : 'false');
      } else {
        localStorage.removeItem(REMEMBER_KEY);
        localStorage.removeItem(SAVED_EMAIL_KEY);
        localStorage.removeItem(SAVED_PASSWORD_KEY);
        localStorage.removeItem(AUTO_LOGIN_KEY);
      }

      navigate(from, { replace: true });
    } catch (error: any) {
      form.setFields([
        {
          name: 'password',
          errors: [error.response?.data?.detail || '登录失败，请检查邮箱和密码'],
        },
      ]);
    }
  };

  const onRememberChange = (e: any) => {
    if (!e.target.checked) {
      form.setFieldValue('autoLogin', false);
    }
  };

  return (
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

      {/* Login Card */}
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
          登录
        </Title>

        <Form
          form={form}
          name="login"
          onFinish={onFinish}
          autoComplete="off"
          initialValues={{ remember: false, autoLogin: false }}
          size="large"
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

          <Form.Item style={{ marginBottom: 20 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Form.Item name="remember" valuePropName="checked" noStyle>
                <Checkbox onChange={onRememberChange} disabled={isLoading}>
                  记住密码
                </Checkbox>
              </Form.Item>
              <Form.Item
                noStyle
                shouldUpdate={(prev, cur) => prev.remember !== cur.remember}
              >
                {({ getFieldValue }) => (
                  <Form.Item name="autoLogin" valuePropName="checked" noStyle>
                    <Checkbox disabled={!getFieldValue('remember') || isLoading}>
                      自动登录
                    </Checkbox>
                  </Form.Item>
                )}
              </Form.Item>
            </div>
          </Form.Item>

          <Form.Item style={{ marginBottom: 16 }}>
            <Button
              type="primary"
              htmlType="submit"
              loading={isLoading}
              block
              style={{ height: 44 }}
            >
              登 录
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center' }}>
            <Text type="secondary">还没有账号？</Text>
            <Link to="/register" style={{ marginLeft: 4 }}>立即注册</Link>
          </div>
        </Form>
      </Card>

      {/* Footer */}
      <Text style={{ color: 'rgba(255,255,255,0.6)', fontSize: 12, marginTop: 24 }}>
        © 2026 PANDA Training System
      </Text>
    </div>
  );
};
