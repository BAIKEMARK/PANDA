/**
 * 场景列表页面
 */
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Row, Col, Typography, Empty, Spin, message } from 'antd';
import { MessageOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import type { Scenario } from '@/types/scenario.types';
import scenarioService from '@/services/scenario.service';
import { useChatStore } from '@/stores/chat.store';
import { ScenarioCard } from '@/components/scenario/ScenarioCard';

const { Title, Text } = Typography;

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
        message.error('创建会话失败');
        return;
      }
      navigate(`/chat/${session.id}`);
    } catch (err: any) {
      message.error(err.response?.data?.detail || '创建会话失败');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
    >
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.3 }}
        style={{ marginBottom: '24px' }}
      >
        <Title level={4} style={{ marginBottom: '8px', color: '#1a365d', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <motion.span
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
          >
            <MessageOutlined />
          </motion.span>
          情景模拟练习
        </Title>
        <Text type="secondary" style={{ fontSize: '14px' }}>
          与AI模拟患者对话，提升PND识别、沟通支持和初步干预能力
        </Text>
      </motion.div>

      {/* Loading State */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{ textAlign: 'center', padding: '60px 0' }}
        >
          <Spin size="large" />
        </motion.div>
      )}

      {/* Empty State */}
      {!isLoading && !error && scenarios.length === 0 && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
        >
          <Empty description="暂无场景练习" style={{ padding: '60px 0' }} />
        </motion.div>
      )}

      {/* Scenario Grid */}
      {!isLoading && !error && scenarios.length > 0 && (
        <Row gutter={[16, 16]}>
          {scenarios.map((scenario, index) => (
            <Col key={scenario.id} xs={24} sm={12} lg={8} xl={6}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05, duration: 0.3 }}
                whileHover={{ y: -8 }}
              >
                <ScenarioCard
                  scenario={scenario}
                  onStartPractice={handleStartPractice}
                  isLoading={isLoading}
                />
              </motion.div>
            </Col>
          ))}
        </Row>
      )}
    </motion.div>
  );
};
