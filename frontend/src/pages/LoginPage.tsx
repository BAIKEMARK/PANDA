/**
 * 登录页面 - 优化版
 */
import { useEffect, useRef } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { Form, Input, Button, Card, Checkbox, Typography, Space } from 'antd';
import { UserOutlined, LockOutlined, RocketOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import gsap from 'gsap';
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
  
  const logoRef = useRef<HTMLDivElement>(null);
  const cardRef = useRef<HTMLDivElement>(null);
  const particlesRef = useRef<HTMLDivElement>(null);

  const from = (location.state as { from?: string })?.from || '/courses';
  const registeredEmail = (location.state as { registeredEmail?: string })?.registeredEmail;
  const registeredPassword = (location.state as { registeredPassword?: string })?.registeredPassword;

  // GSAP 动画
  useEffect(() => {
    const ctx = gsap.context(() => {
      // Logo 动画
      gsap.from(logoRef.current, {
        y: -50,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out',
      });

      // 卡片动画
      gsap.from(cardRef.current, {
        y: 30,
        opacity: 0,
        duration: 0.8,
        delay: 0.2,
        ease: 'power3.out',
      });

      // 粒子动画
      if (particlesRef.current) {
        const particles = particlesRef.current.children;
        gsap.to(particles, {
          y: 'random(-20, 20)',
          x: 'random(-20, 20)',
          duration: 'random(2, 4)',
          repeat: -1,
          yoyo: true,
          ease: 'sine.inOut',
          stagger: {
            amount: 1,
            from: 'random',
          },
        });
      }
    });

    return () => ctx.revert();
  }, []);

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
      position: 'relative',
      overflow: 'hidden',
    }}>
      {/* 背景粒子 */}
      <div ref={particlesRef} style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        opacity: 0.3,
      }}>
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              width: Math.random() * 10 + 5 + 'px',
              height: Math.random() * 10 + 5 + 'px',
              borderRadius: '50%',
              background: 'rgba(255, 255, 255, 0.5)',
              left: Math.random() * 100 + '%',
              top: Math.random() * 100 + '%',
            }}
          />
        ))}
      </div>

      {/* Logo */}
      <motion.div
        ref={logoRef}
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Space direction="vertical" align="center" size={8} style={{ marginBottom: 32 }}>
          <motion.div
            animate={{
              rotate: [0, 10, -10, 0],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              repeatDelay: 3,
            }}
          >
            <RocketOutlined style={{ fontSize: 48, color: '#fff' }} />
          </motion.div>
          <Title level={1} style={{ 
            color: '#fff', 
            margin: 0, 
            letterSpacing: 4,
            fontWeight: 700,
            textShadow: '0 4px 12px rgba(0,0,0,0.2)',
          }}>
            PANDA
          </Title>
          <Text style={{ 
            color: 'rgba(255,255,255,0.95)', 
            fontSize: 16,
            fontWeight: 300,
            letterSpacing: 1,
          }}>
            围产期抑郁管理智能培训系统
          </Text>
        </Space>
      </motion.div>

      {/* Login Card */}
      <motion.div
        ref={cardRef}
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        style={{ width: '100%', maxWidth: 420 }}
      >
        <Card
          bordered={false}
          className="glass-effect"
          style={{
            borderRadius: 16,
            boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
            backdropFilter: 'blur(10px)',
            background: 'rgba(255, 255, 255, 0.95)',
          }}
          styles={{ body: { padding: '40px 32px 32px' } }}
        >
          <Title level={3} style={{ 
            textAlign: 'center', 
            marginBottom: 32,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 600,
          }}>
            欢迎回来
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
                prefix={<UserOutlined style={{ color: '#999' }} />}
                placeholder="邮箱地址"
                disabled={isLoading}
                style={{
                  borderRadius: 8,
                  padding: '12px 16px',
                  fontSize: 15,
                }}
              />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[{ required: true, message: '请输入密码' }]}
            >
              <Input.Password
                prefix={<LockOutlined style={{ color: '#999' }} />}
                placeholder="密码"
                disabled={isLoading}
                style={{
                  borderRadius: 8,
                  padding: '12px 16px',
                  fontSize: 15,
                }}
              />
            </Form.Item>

            <Form.Item style={{ marginBottom: 24 }}>
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

            <Form.Item style={{ marginBottom: 20 }}>
              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={isLoading}
                  block
                  style={{ 
                    height: 48,
                    borderRadius: 8,
                    fontSize: 16,
                    fontWeight: 500,
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    border: 'none',
                    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)',
                  }}
                >
                  登 录
                </Button>
              </motion.div>
            </Form.Item>

            <div style={{ textAlign: 'center' }}>
              <Text type="secondary">还没有账号？</Text>
              <Link to="/register" style={{ 
                marginLeft: 8,
                fontWeight: 500,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}>
                立即注册
              </Link>
            </div>
          </Form>
        </Card>
      </motion.div>

      {/* Footer */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <Text style={{ 
          color: 'rgba(255,255,255,0.7)', 
          fontSize: 13, 
          marginTop: 32,
          fontWeight: 300,
        }}>
          © 2026 PANDA Training System
        </Text>
      </motion.div>
    </div>
  );
};
