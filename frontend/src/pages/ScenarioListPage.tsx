/**
 * 场景列表页面
 */
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Row, Col, Typography, Empty, Spin, Alert, message } from 'antd';
import { BulbOutlined } from '@ant-design/icons';
import type { Scenario } from '@/types/scenario.types';
import scenarioService from '@/services/scenario.service';
import { useChatStore } from '@/stores/chat.store';
import { ScenarioCard } from '@/components/scenario/ScenarioCard';

const { Title, Paragraph } = Typography;

export const ScenarioListPage = () => {
  const navigate = useNavigate();
  const { createSession } = useChatStore();
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchScenarios = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await scenarioService.getScenarios();
        setScenarios(data);
      } catch (err: any) {
        setError(err.message || '加载场景失败');
      } finally {
        setIsLoading(false);
      }
    };

    fetchScenarios();
  }, []);

  const handleStartPractice = async (scenarioId: string) => {
    try {
      const session = await createSession(scenarioId);
      if (!session || !session.id) {
        message.error('创建会话失败：未返回会话ID');
        return;
      }
      navigate(`/chat/${session.id}`);
    } catch (err: any) {
      console.error('创建会话失败:', err);
      message.error(err.response?.data?.detail || err.message || '创建会话失败，请稍后重试');
    }
  };

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <Title level={2} style={{ marginBottom: '8px' }}>
          情景模拟
        </Title>
        <Paragraph type="secondary" style={{ fontSize: '16px' }}>
          通过真实场景对话练习，提升围产期抑郁症识别与干预能力
        </Paragraph>
      </div>

      {/* Info Box */}
      <Alert
        message={
          <div>
            <div style={{ fontWeight: 600, marginBottom: '8px' }}>
              <BulbOutlined style={{ marginRight: '8px' }} />
              练习说明
            </div>
            <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '14px' }}>
              <li>选择一个场景开始对话练习</li>
              <li>与AI模拟的患者进行对话交流</li>
              <li>练习结束后可查看评估报告和能力雷达图</li>
            </ul>
          </div>
        }
        type="info"
        showIcon={false}
        style={{ marginBottom: '24px' }}
      />

      {/* Loading State */}
      {isLoading && (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <Spin size="large" />
        </div>
      )}

      {/* Error State */}
      {error && (
        <Alert
          title="加载失败"
          description={error}
          type="error"
          showIcon
          style={{ marginBottom: '24px' }}
        />
      )}

      {/* Empty State */}
      {!isLoading && !error && scenarios.length === 0 && (
        <Empty
          description="暂无场景练习"
          style={{ padding: '60px 0' }}
        />
      )}

      {/* Scenario Grid */}
      {!isLoading && !error && scenarios.length > 0 && (
        <Row gutter={[16, 16]}>
          {scenarios.map((scenario) => (
            <Col key={scenario.id} xs={24} sm={12} lg={8}>
              <ScenarioCard
                scenario={scenario}
                onStartPractice={handleStartPractice}
                isLoading={isLoading}
              />
            </Col>
          ))}
        </Row>
      )}
    </div>
  );
};
