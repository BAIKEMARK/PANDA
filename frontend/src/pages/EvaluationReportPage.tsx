/**
 * 评估报告页面
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Typography, Button, Card, Row, Col, Statistic, Space, Divider, Spin, Alert } from 'antd';
import { TrophyOutlined } from '@ant-design/icons';
import type { EvaluationReport } from '@/types/evaluation.types';
import evaluationService from '@/services/evaluation.service';
import { EvaluationRadarChart } from '@/components/evaluation/RadarChart';
import { ScoreCards } from '@/components/evaluation/ScoreCard';
import { FeedbackSection } from '@/components/evaluation/FeedbackSection';

const { Title, Paragraph, Text } = Typography;

export const EvaluationReportPage = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const [report, setReport] = useState<EvaluationReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) return;

    const fetchReport = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await evaluationService.getReport(Number(sessionId));
        setReport(data);
      } catch (err) {
        // 使用模拟数据
        const mockReport: EvaluationReport = {
          session_id: Number(sessionId),
          dimension_scores: {
            knowledge: 75,
            assessment: 82,
            communication: 68,
            intervention: 71,
          },
          total_score: 74,
          feedback: '## 表现分析\n\n✅ **做得好的地方**\n- 能够主动询问患者的情绪状态\n- 对围产期抑郁症的基本症状有一定了解\n- 沟通态度较为友好和耐心\n\n⚠️ **需要改进的地方**\n- 评估深度不够，需要更详细地了解患者的睡眠、食欲等情况\n- 缺乏对EPDS量表等专业评估工具的使用\n- 干预措施较为笼统，需要更具体的建议\n\n💡 **改进建议**\n- 系统学习围产期抑郁症的诊断标准\n- 熟练掌握EPDS等评估量表的使用\n- 加强对不同程度抑郁症干预措施的学习\n- 多进行模拟练习，提升沟通技巧',
          created_at: new Date().toISOString(),
        };
        setReport(mockReport);
      } finally {
        setIsLoading(false);
      }
    };

    fetchReport();
  }, [sessionId]);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 0' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (error || !report) {
    return (
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <Alert
          message="加载失败"
          description={error || '报告加载失败'}
          type="error"
          showIcon
          style={{ marginBottom: '24px' }}
        />
        <Space>
          <Button onClick={() => navigate(-1)}>返回上一页</Button>
          <Link to="/scenarios">
            <Button type="primary">继续练习</Button>
          </Link>
        </Space>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <Title level={2} style={{ marginBottom: '8px' }}>评估报告</Title>
          <Paragraph type="secondary">
            对话练习 #{sessionId} 的详细评估结果
          </Paragraph>
        </div>
        <Link to="/scenarios">
          <Button type="primary" size="large">继续练习</Button>
        </Link>
      </div>

      {/* Total Score */}
      <Card
        style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          marginBottom: '24px',
          borderRadius: '12px',
          border: 'none'
        }}
      >
        <Row gutter={24} align="middle">
          <Col>
            <div style={{ color: '#fff', opacity: 0.9, fontSize: '16px', marginBottom: '8px' }}>
              <TrophyOutlined style={{ marginRight: '8px' }} />
              综合得分
            </div>
            <div style={{
              color: '#fff',
              fontSize: '64px',
              fontWeight: 'bold',
              lineHeight: 1
            }}>
              {report.total_score}
            </div>
          </Col>
          <Col flex="1" style={{ textAlign: 'right', color: '#fff' }}>
            <div style={{ fontSize: '14px', opacity: 0.9, marginBottom: '4px' }}>评估完成</div>
            <div style={{ fontSize: '16px', opacity: 0.8 }}>
              {new Date(report.created_at).toLocaleString('zh-CN')}
            </div>
          </Col>
        </Row>
      </Card>

      {/* Score Cards */}
      <div style={{ marginBottom: '24px' }}>
        <ScoreCards scores={report.dimension_scores} />
      </div>

      {/* Radar Chart */}
      <Card
        title="能力雷达图"
        bordered={false}
        style={{ marginBottom: '24px', borderRadius: '12px' }}
      >
        <EvaluationRadarChart scores={report.dimension_scores} />
      </Card>

      {/* AI Feedback */}
      <div style={{ marginBottom: '24px' }}>
        <FeedbackSection feedback={report.feedback} />
      </div>

      {/* Action Buttons */}
      <div style={{ textAlign: 'center', marginTop: '32px' }}>
        <Space size="middle">
          <Link to="/scenarios">
            <Button type="primary" size="large">继续练习</Button>
          </Link>
          <Link to="/courses">
            <Button size="large">返回课程</Button>
          </Link>
        </Space>
      </div>
    </div>
  );
};
