/**
 * 评分卡片组件
 */
import { Card, Statistic, Progress } from 'antd';
import type { DimensionScores } from '@/types/evaluation.types';

interface ScoreCardProps {
  title: string;
  score: number;
  icon: React.ReactNode;
  color: string;
}

const getScoreLevel = (score: number): { text: string; color: string } => {
  if (score >= 80) return { text: '优秀', color: '#52c41a' };
  if (score >= 60) return { text: '良好', color: '#1890ff' };
  if (score >= 40) return { text: '及格', color: '#faad14' };
  return { text: '需改进', color: '#ff4d4f' };
};

export const ScoreCard = ({ title, score, icon, color }: ScoreCardProps) => {
  const level = getScoreLevel(score);

  return (
    <Card bordered={false} style={{ borderRadius: '12px' }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '16px' }}>
        <div style={{ fontSize: '32px', marginRight: '12px' }}>{icon}</div>
        <span style={{ fontSize: '16px', fontWeight: 600, color: '#262626' }}>
          {title}
        </span>
      </div>

      <Statistic
        value={score}
        suffix="/ 100"
        valueStyle={{ color: color, fontSize: '36px', fontWeight: 'bold' }}
      />

      <div style={{ marginTop: '12px' }}>
        <span style={{ fontSize: '14px', color: level.color, fontWeight: 500 }}>
          {level.text}
        </span>
      </div>

      <Progress
        percent={Math.min(score, 100)}
        strokeColor={color}
        showInfo={false}
        style={{ marginTop: '16px' }}
      />
    </Card>
  );
};

interface ScoreCardsProps {
  scores: DimensionScores;
}

export const ScoreCards = ({ scores }: ScoreCardsProps) => {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
      <ScoreCard
        title="知识理解"
        score={scores.knowledge}
        icon="📚"
        color="#1890ff"
      />
      <ScoreCard
        title="评估技能"
        score={scores.assessment}
        icon="🔍"
        color="#52c41a"
      />
      <ScoreCard
        title="沟通技能"
        score={scores.communication}
        icon="💬"
        color="#722ed1"
      />
      <ScoreCard
        title="干预决策"
        score={scores.intervention}
        icon="🎯"
        color="#fa8c16"
      />
    </div>
  );
};
