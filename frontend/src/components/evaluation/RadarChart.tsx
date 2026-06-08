/**
 * 能力雷达图组件 - THP五维评分系统
 */
import { useMemo } from 'react';
import { Alert } from 'antd';
import type { RadarChart as RadarChartType } from '@/types/evaluation.types';
import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from 'recharts';

interface RadarChartProps {
  scores: RadarChartType;
}

export const EvaluationRadarChart = ({ scores }: RadarChartProps) => {
  const data = useMemo(
    () => [
      {
        dimension: 'A类-风险识别',
        score: scores?.A_risk_identification ?? 0,
        fullMark: 100
      },
      {
        dimension: 'B类-沟通支持',
        score: scores?.B_communication ?? 0,
        fullMark: 100
      },
      {
        dimension: 'C类-技能应用',
        score: scores?.C_skill_application ?? 0,
        fullMark: 100
      },
      {
        dimension: 'D类-安全管理',
        score: scores?.D_safety_management ?? 0,
        fullMark: 100
      },
      {
        dimension: 'E类-自我效能',
        score: scores?.E_self_efficacy ?? 0,
        fullMark: 100
      },
    ],
    [scores]
  );

  // 防御性检查:如果 scores 未定义或为 null,显示警告信息
  if (!scores) {
    return (
      <Alert
        message="雷达图数据不可用"
        description="评估报告缺少必要的雷达图数据。请重新生成评估报告或联系管理员。"
        type="warning"
        showIcon
      />
    );
  }

  return (
    <div style={{ width: '100%', height: '400px', minHeight: '400px' }}>
      <ResponsiveContainer width="100%" height="100%">
        <RechartsRadarChart data={data}>
          <PolarGrid />
          <PolarAngleAxis
            dataKey="dimension"
            className="text-sm font-medium"
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fontSize: 12 }}
          />
          <Radar
            name="能力得分"
            dataKey="score"
            stroke="#3B82F6"
            fill="#3B82F6"
            fillOpacity={0.5}
            strokeWidth={2}
          />
        </RechartsRadarChart>
      </ResponsiveContainer>
    </div>
  );
};
