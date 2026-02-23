/**
 * 学习仪表盘页面
 */
import { useEffect, useState } from 'react';
import { Typography, Row, Col, Card, Tag, Spin, Empty, Alert, message } from 'antd';
import {
    TrophyOutlined,
    ReadOutlined,
    ExperimentOutlined,
    ArrowRightOutlined,
    ClockCircleOutlined
} from '@ant-design/icons';
import { Link } from 'react-router-dom';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { useAuthStore } from '@/stores/auth.store';
import api from '@/services/api';
import { StatsCard } from '@/components/dashboard/StatsCard';

const { Title, Text } = Typography;

// 仪表盘数据类型定义
interface RadarData {
    subject: string;
    A: number;
    fullMark: number;
}

interface RecentActivity {
    id: string;
    course_id: string;
    is_completed: boolean;
    completed_at: string | null;
    created_at: string;
}

interface ScenarioHistoryItem {
    session_id: string;
    scenario_name: string;
    total_score: number | null;
    level_assessment: string | null;
    status: string;
    created_at: string;
}

interface DashboardStats {
    total_courses: number;
    completed_courses: number;
    total_scenarios: number;
    avg_score: number;
    radar_data: RadarData[];
    recent_activities: RecentActivity[];
    scenario_history: ScenarioHistoryItem[];
}

export const LearningDashboardPage = () => {
    const { user } = useAuthStore();
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                setLoading(true);
                const response = await api.get('/progress/dashboard');
                setStats(response.data);
            } catch (err) {
                console.error('Failed to fetch dashboard data:', err);
                setError('加载仪表盘数据失败，请稍后重试');
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            fetchDashboardData();
        }
    }, [user]);

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', minHeight: '400px' }}>
                <Spin size="large" tip="加载数据中...">
                    <div style={{ height: '50px' }} />
                </Spin>
            </div>
        );
    }

    if (error) {
        return <Alert message="加载失败" description={error} type="error" showIcon />;
    }

    // 获取等级对应的颜色
    const getLevelColor = (level: string | null) => {
        switch (level) {
            case '优秀': return 'green';
            case '良好': return 'blue';
            case '合格': return 'orange';
            case '不合格': return 'red';
            default: return 'default';
        }
    };

    const recentActivities = stats?.recent_activities || [];
    const scenarioHistory = stats?.scenario_history || [];

    return (
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
            {/* 欢迎头部 */}
            <div style={{ marginBottom: '24px' }}>
                <Title level={2}>
                    欢迎回来，{user?.name} 👋
                </Title>
                <Text type="secondary">这里是您的个人学习仪表盘，实时追踪您的成长轨迹。</Text>
            </div>

            {/* 核心指标卡片 */}
            <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
                <Col xs={24} sm={8}>
                    <StatsCard
                        title="已完成课程"
                        value={stats?.completed_courses || 0}
                        suffix={`/ ${stats?.total_courses || 0}`}
                        icon={<ReadOutlined />}
                        color="#1890ff"
                    />
                </Col>
                <Col xs={24} sm={8}>
                    <StatsCard
                        title="完成模拟训练"
                        value={stats?.total_scenarios || 0}
                        suffix="次"
                        icon={<ExperimentOutlined />}
                        color="#722ed1"
                    />
                </Col>
                <Col xs={24} sm={8}>
                    <StatsCard
                        title="综合平均分"
                        value={stats?.avg_score || 0}
                        suffix="分"
                        icon={<TrophyOutlined />}
                        color="#faad14"
                    />
                </Col>
            </Row>

            <Row gutter={[24, 24]}>
                {/* 左侧：能力雷达图 */}
                <Col xs={24} lg={14}>
                    <Card
                        title="THP 五维能力评估"
                        variant="borderless"
                        style={{ borderRadius: '12px', height: '100%' }}
                    >
                        {stats?.radar_data && stats.radar_data.length > 0 ? (
                            <div style={{ height: '350px', width: '100%' }}>
                                <ResponsiveContainer width="100%" height="100%">
                                    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={stats.radar_data}>
                                        <PolarGrid />
                                        <PolarAngleAxis dataKey="subject" tick={{ fill: '#666', fontSize: 12 }} />
                                        <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} />
                                        <Radar
                                            name="能力评分"
                                            dataKey="A"
                                            stroke="#8884d8"
                                            fill="#8884d8"
                                            fillOpacity={0.6}
                                        />
                                        <Tooltip />
                                    </RadarChart>
                                </ResponsiveContainer>
                            </div>
                        ) : (
                            <Empty description="暂无评估数据，请先完成一次模拟训练" />
                        )}
                    </Card>
                </Col>

                {/* 右侧：最近学习动态 */}
                <Col xs={24} lg={10}>
                    <Card
                        title="最近学习动态"
                        variant="borderless"
                        extra={<Link to="/courses">全部课程 <ArrowRightOutlined /></Link>}
                        style={{ borderRadius: '12px', height: '100%' }}
                    >
                        {recentActivities.length ? (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                {recentActivities.map((item, index) => {
                                    const isLast = index === recentActivities.length - 1;
                                    return (
                                        <div
                                            key={item.id}
                                            style={{
                                                display: 'flex',
                                                gap: '12px',
                                                padding: '8px 0',
                                                borderBottom: isLast ? 'none' : '1px solid #f0f0f0',
                                            }}
                                        >
                                            <div style={{
                                                width: '36px', height: '36px',
                                                background: item.is_completed ? '#f6ffed' : '#e6f7ff',
                                                borderRadius: '50%',
                                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                                color: item.is_completed ? '#52c41a' : '#1890ff'
                                            }}>
                                                {item.is_completed ? <TrophyOutlined /> : <ClockCircleOutlined />}
                                            </div>
                                            <div style={{ flex: 1 }}>
                                                <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px' }}>
                                                    <span style={{ fontWeight: 500 }}>
                                                        课程 ID: {item.course_id.substring(0, 8)}...
                                                    </span>
                                                    <Tag color={item.is_completed ? 'success' : 'processing'}>
                                                        {item.is_completed ? '已完成' : '进行中'}
                                                    </Tag>
                                                </div>
                                                <Text type="secondary" style={{ fontSize: '12px' }}>
                                                    {item.completed_at
                                                        ? `完成于 ${new Date(item.completed_at).toLocaleDateString()}`
                                                        : `开始于 ${new Date(item.created_at).toLocaleDateString()}`
                                                    }
                                                </Text>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        ) : (
                            <Empty description="暂无学习记录" />
                        )}
                    </Card>
                </Col>
            </Row>

            {/* 情景模拟历史记录 */}
            <Row style={{ marginTop: '24px' }}>
                <Col span={24}>
                    <Card
                        title="情景模拟历史记录"
                        variant="borderless"
                        extra={<Link to="/scenarios">进入模拟训练 <ArrowRightOutlined /></Link>}
                        style={{ borderRadius: '12px' }}
                    >
                        {scenarioHistory.length ? (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                                {scenarioHistory.map((item, index) => {
                                    const isLast = index === scenarioHistory.length - 1;
                                    return (
                                        <div
                                            key={item.session_id}
                                            style={{
                                                display: 'flex',
                                                justifyContent: 'space-between',
                                                gap: '16px',
                                                paddingBottom: isLast ? 0 : '16px',
                                                borderBottom: isLast ? 'none' : '1px solid #f0f0f0',
                                            }}
                                        >
                                            <div style={{ display: 'flex', gap: '12px', flex: 1 }}>
                                                <div style={{
                                                    width: '48px', height: '48px',
                                                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                                    borderRadius: '12px',
                                                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                                                    color: '#fff',
                                                    fontSize: '20px'
                                                }}>
                                                    <ExperimentOutlined />
                                                </div>
                                                <div style={{ flex: 1 }}>
                                                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                                        <span style={{ fontWeight: 600, fontSize: '15px' }}>{item.scenario_name}</span>
                                                        {item.level_assessment && (
                                                            <Tag color={getLevelColor(item.level_assessment)}>
                                                                {item.level_assessment}
                                                            </Tag>
                                                        )}
                                                    </div>
                                                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginTop: '4px' }}>
                                                        {item.status === 'completed' && item.total_score !== null && (
                                                            <Text strong style={{ color: '#1890ff' }}>
                                                                得分：{item.total_score} 分
                                                            </Text>
                                                        )}
                                                        {item.status === 'generating' && (
                                                            <Text strong style={{ color: '#faad14' }}>
                                                                <Spin size="small" style={{ marginRight: 8 }} />
                                                                生成报告中...
                                                            </Text>
                                                        )}
                                                        <Text type="secondary" style={{ fontSize: '12px' }}>
                                                            <ClockCircleOutlined style={{ marginRight: '4px' }} />
                                                            {new Date(item.created_at).toLocaleDateString()}
                                                        </Text>
                                                    </div>
                                                </div>
                                            </div>
                                            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                                                {item.status === 'generating' ? (
                                                    <a onClick={(e) => { e.preventDefault(); message.info('报告正在生成中，请耐心等待15秒左右...', 3); }} style={{ color: '#999' }}>查看评估</a>
                                                ) : (
                                                    <Link to={`/evaluation/${item.session_id}`}>查看评估</Link>
                                                )}
                                                <Link to={`/chat/${item.session_id}`} state={{ fromHistory: true }}>
                                                    查看对话
                                                </Link>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        ) : (
                            <Empty description="暂无模拟训练记录，点击右上角开始您的第一次练习！" />
                        )}
                    </Card>
                </Col>
            </Row>
        </div>
    );
};
