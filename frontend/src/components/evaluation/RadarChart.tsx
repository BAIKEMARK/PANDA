/**
 * 能力雷达图组件
 */
import { useMemo } from 'react';
import type { DimensionScores } from '@/types/evaluation.types';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from 'recharts';

interface RadarChartProps {
  scores: DimensionScores;
}

export const EvaluationRadarChart = ({ scores }: RadarChartProps) => {
  const data = useMemo(
    () => [
      { dimension: '知识理解', score: scores.knowledge, fullMark: 100 },
      { dimension: '评估技能', score: scores.assessment, fullMark: 100 },
      { dimension: '沟通技能', score: scores.communication, fullMark: 100 },
      { dimension: '干预决策', score: scores.intervention, fullMark: 100 },
    ],
    [scores]
  );

  return (
    <div className="w-full h-[400px]">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data}>
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
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
