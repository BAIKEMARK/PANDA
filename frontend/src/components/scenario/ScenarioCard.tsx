/**
 * 场景卡片组件
 */
import { Card, Tag, Typography, Button, Space } from 'antd';
import { MessageOutlined, UserOutlined, CalendarOutlined } from '@ant-design/icons';
import type { Scenario } from '@/types/scenario.types';

const { Text, Title, Paragraph } = Typography;

interface ScenarioCardProps {
  scenario: Scenario;
  onStartPractice: (scenarioId: number) => void;
  isLoading?: boolean;
}

const difficultyStars = {
  1: '⭐',
  2: '⭐⭐',
  3: '⭐⭐⭐',
  4: '⭐⭐⭐⭐',
  5: '⭐⭐⭐⭐⭐',
};

export const ScenarioCard = ({ scenario, onStartPractice, isLoading }: ScenarioCardProps) => {
  const stars = difficultyStars[scenario.difficulty as keyof typeof difficultyStars] || '⭐';

  // 将knowledge_tags从字符串转换为数组（如果是字符串）
  const knowledgeTags = Array.isArray(scenario.knowledge_tags)
    ? scenario.knowledge_tags
    : (scenario.knowledge_tags ? scenario.knowledge_tags.split(',').map((tag: string) => tag.trim()).filter(Boolean) : []);

  return (
    <Card
      hoverable
      cover={
        <div
          style={{
            height: '160px',
            background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            position: 'relative',
          }}
        >
          <MessageOutlined style={{ fontSize: '64px', color: 'rgba(255,255,255,0.8)' }} />
          <div
            style={{
              position: 'absolute',
              top: '16px',
              right: '16px',
              background: 'rgba(255,255,255,0.9)',
              padding: '4px 12px',
              borderRadius: '20px',
              fontSize: '12px',
              fontWeight: 500,
            }}
          >
            {stars}
          </div>
        </div>
      }
      style={{ borderRadius: '12px', overflow: 'hidden' }}
      bodyStyle={{ padding: '20px' }}
    >
      <Title level={5} style={{ marginBottom: '12px' }}>
        {scenario.title}
      </Title>

      {scenario.description && (
        <Paragraph
          type="secondary"
          ellipsis={{ rows: 2 }}
          style={{ marginBottom: '16px' }}
        >
          {scenario.description}
        </Paragraph>
      )}

      {/* Patient Background */}
      {scenario.patient_background && (
        <div style={{ marginBottom: '16px' }}>
          <Space size="small" style={{ marginBottom: '8px' }}>
            <UserOutlined style={{ color: '#8c8c8c' }} />
            <Text type="secondary" style={{ fontSize: '12px' }}>
              患者背景
            </Text>
          </Space>
          <Paragraph
            ellipsis={{ rows: 2 }}
            style={{
              marginBottom: 0,
              paddingLeft: '20px',
              color: '#595959',
              fontSize: '13px',
            }}
          >
            {scenario.patient_background}
          </Paragraph>
        </div>
      )}

      {/* Knowledge Tags */}
      {knowledgeTags.length > 0 && (
        <div style={{ marginBottom: '12px' }}>
          <Space wrap size="small">
            {knowledgeTags.slice(0, 3).map((tag, index) => (
              <Tag key={index} color="blue" style={{ fontSize: '12px' }}>
                {tag}
              </Tag>
            ))}
            {knowledgeTags.length > 3 && (
              <Tag color="default" style={{ fontSize: '12px' }}>
                +{knowledgeTags.length - 3}
              </Tag>
            )}
          </Space>
        </div>
      )}

      {/* Time Period */}
      {scenario.time_period && (
        <div style={{ marginBottom: '16px' }}>
          <Space size="small">
            <CalendarOutlined style={{ color: '#8c8c8c' }} />
            <Text type="secondary" style={{ fontSize: '12px' }}>
              {scenario.time_period}
            </Text>
          </Space>
        </div>
      )}

      {/* Start Button */}
      <Button
        type="primary"
        block
        size="large"
        loading={isLoading}
        onClick={() => onStartPractice(scenario.id)}
        style={{ borderRadius: '8px' }}
      >
        开始练习
      </Button>
    </Card>
  );
};
