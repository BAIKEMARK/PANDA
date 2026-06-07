/**
 * 评分卡片组件 - THP五维评分系统
 */
import { Card, Statistic, Progress, Alert } from 'antd';
import type { RadarChart as RadarChartType } from '@/types/evaluation.types';

interface ScoreCardProps {
  title: string;
  score: number;
  icon: React.ReactNode;
  color: string;
  description?: string;  // 维度描述
}

const getScoreLevel = (score: number): { text: string; color: string } => {
  if (score >= 80) return { text: '优秀', color: '#52c41a' };
  if (score >= 60) return { text: '良好', color: '#1890ff' };
  if (score >= 40) return { text: '合格', color: '#faad14' };
  return { text: '需改进', color: '#ff4d4f' };
};

export const ScoreCard = ({ title, score, icon, color, description }: ScoreCardProps) => {
  const level = getScoreLevel(score);

  return (
    <Card variant="borderless" style={{ borderRadius: '12px' }}>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '16px' }}>
        <div style={{ fontSize: '32px', marginRight: '12px' }}>{icon}</div>
        <div>
          <div style={{ fontSize: '16px', fontWeight: 600, color: '#262626' }}>
            {title}
          </div>
          {description && (
            <div style={{ fontSize: '12px', color: '#8c8c8c', marginTop: '2px' }}>
              {description}
            </div>
          )}
        </div>
      </div>

      <Statistic
        value={score}
        suffix="/ 100"
        styles={{ content: { color: color, fontSize: '36px', fontWeight: 'bold' } }}
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
  scores: RadarChartType;
}

export const ScoreCards = ({ scores }: ScoreCardsProps) => {
  // 防御性检查:如果 scores 未定义或为 null,显示警告信息
  if (!scores) {
    return (
      <Alert
        message="评分数据不可用"
        description="评估报告缺少必要的评分数据。请重新生成评估报告或联系管理员。"
        type="warning"
        showIcon
      />
    );
  }

  // 使用可选链和默认值确保数据完整性
  const safeScores = {
    A_risk_identification: scores.A_risk_identification ?? 0,
    B_communication: scores.B_communication ?? 0,
    C_skill_application: scores.C_skill_application ?? 0,
    D_safety_management: scores.D_safety_management ?? 0,
    E_self_efficacy: scores.E_self_efficacy ?? 0,
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
      <ScoreCard
        title="A类-风险识别"
        score={safeScores.A_risk_identification}
        icon="⚠️"
        color="#ff4d4f"
        description="识别睡眠障碍、自杀意念等风险信号"
      />
      <ScoreCard
        title="B类-沟通支持"
        score={safeScores.B_communication}
        icon="💬"
        color="#1890ff"
        description="积极倾听、避免说教打断"
      />
      <ScoreCard
        title="C类-技能应用"
        score={safeScores.C_skill_application}
        icon="🎯"
        color="#52c41a"
        description="THP认知行为干预技巧"
      />
      <ScoreCard
        title="D类-安全管理"
        score={safeScores.D_safety_management}
        icon="🛡️"
        color="#722ed1"
        description="危机识别与转介流程"
      />
      <ScoreCard
        title="E类-自我效能"
        score={safeScores.E_self_efficacy}
        icon="💪"
        color="#fa8c16"
        description="综合胜任感与应对信心"
      />
    </div>
  );
};
