/**
 * 个人中心页面
 */
import { Avatar, Card, Typography, Row, Col, Descriptions, Tag, Alert } from 'antd';
import { UserOutlined } from '@ant-design/icons';
import { useAuthStore } from '@/stores/auth.store';

const { Title, Text } = Typography;

const roleNames = {
  student: '学员',
  instructor: '讲师',
  admin: '管理员',
};

export const ProfilePage = () => {
  const { user } = useAuthStore();

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
              <Tag color="blue">{roleNames[user.role]}</Tag>
              <Tag style={{ marginLeft: '8px' }}>ID: {user.id}</Tag>
            </div>
          </Col>
        </Row>
      </Card>

      {/* Account Details */}
      <Card
        title="账户详情"
        style={{ marginBottom: '24px', borderRadius: '12px' }}
      >
        <Descriptions column={1} bordered>
          <Descriptions.Item label="用户ID">
            {user.id}
          </Descriptions.Item>
          <Descriptions.Item label="姓名">
            {user.name}
          </Descriptions.Item>
          <Descriptions.Item label="邮箱">
            {user.email}
          </Descriptions.Item>
          <Descriptions.Item label="角色">
            <Tag color="blue">{roleNames[user.role]}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="注册时间">
            {new Date(user.created_at).toLocaleDateString('zh-CN')}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* Stats Cards */}
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={8}>
          <Card
            bordered={false}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: '12px',
              color: '#fff'
            }}
          >
            <div style={{ fontSize: '36px', marginBottom: '12px' }}>📚</div>
            <div style={{ fontSize: '14px', opacity: 0.9, marginBottom: '8px' }}>
              课程学习
            </div>
            <div style={{ fontSize: '32px', fontWeight: 'bold' }}>
              -
            </div>
            <div style={{ fontSize: '13px', opacity: 0.8, marginTop: '8px' }}>
              已学习课程
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={8}>
          <Card
            bordered={false}
            style={{
              background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
              borderRadius: '12px',
              color: '#fff'
            }}
          >
            <div style={{ fontSize: '36px', marginBottom: '12px' }}>💬</div>
            <div style={{ fontSize: '14px', opacity: 0.9, marginBottom: '8px' }}>
              对话练习
            </div>
            <div style={{ fontSize: '32px', fontWeight: 'bold' }}>
              -
            </div>
            <div style={{ fontSize: '13px', opacity: 0.8, marginTop: '8px' }}>
              完成会话数
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={8}>
          <Card
            bordered={false}
            style={{
              background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
              borderRadius: '12px',
              color: '#fff'
            }}
          >
            <div style={{ fontSize: '36px', marginBottom: '12px' }}>📊</div>
            <div style={{ fontSize: '14px', opacity: 0.9, marginBottom: '8px' }}>
              平均得分
            </div>
            <div style={{ fontSize: '32px', fontWeight: 'bold' }}>
              -
            </div>
            <div style={{ fontSize: '13px', opacity: 0.8, marginTop: '8px' }}>
              综合评分
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};
