/**
 * 登录页面
 */
import { useEffect } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { Form, Input, Button, Card, Typography, Checkbox } from 'antd';
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

  // 获取登录前想访问的页面
  const from = (location.state as { from?: string })?.from || '/courses';

  // 初始化：读取保存的登录信息
  useEffect(() => {
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

      // 自动登录
      if (autoLogin && savedEmail && savedPassword) {
        handleAutoLogin(savedEmail, savedPassword);
      }
    }
  }, []);

  // 自动登录处理
  const handleAutoLogin = async (email: string, password: string) => {
    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch {
      // 自动登录失败，清除自动登录设置
      localStorage.setItem(AUTO_LOGIN_KEY, 'false');
    }
  };

  const onFinish: FormProps<LoginFormValues>['onFinish'] = async (values) => {
    try {
      await login(values.email, values.password);
      
      // 保存登录选项
      if (values.remember) {
        localStorage.setItem(REMEMBER_KEY, 'true');
        localStorage.setItem(SAVED_EMAIL_KEY, values.email);
        localStorage.setItem(SAVED_PASSWORD_KEY, values.password);
        localStorage.setItem(AUTO_LOGIN_KEY, values.autoLogin ? 'true' : 'false');
      } else {
        // 清除保存的信息
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

  // 记住密码变化时的处理
  const onRememberChange = (e: any) => {
    if (!e.target.checked) {
      // 取消记住密码时，同时取消自动登录
      form.setFieldValue('autoLogin', false);
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
            initialValues={{ remember: false, autoLogin: false }}
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

            <Form.Item style={{ marginBottom: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
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
