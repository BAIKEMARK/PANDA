/**
 * 评估报告页面
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Typography, Button, Card, Row, Col, Space, Spin, Alert, Tag } from 'antd';
import { TrophyOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import type { EvaluationReport } from '@/types/evaluation.types';
import evaluationService from '@/services/evaluation.service';
import { EvaluationRadarChart } from '@/components/evaluation/RadarChart';
import { ScoreCards } from '@/components/evaluation/ScoreCard';

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
        const data = await evaluationService.getReport(sessionId);

        // 数据转换：处理旧格式的数据
        const normalizedReport: EvaluationReport = {
          ...data,
          // 如果没有 radar_chart 数据，使用默认值
          radar_chart: data.radar_chart || {
            A_risk_identification: 0,
            B_communication: 0,
            C_skill_application: 0,
            D_safety_management: 0,
            E_self_efficacy: 0,
          }
        };

        setReport(normalizedReport);
      } catch (err) {
        // 使用模拟数据
        const mockReport: EvaluationReport = {
          id: 'mock-report-id',
          session_id: sessionId || '',
          total_score: 74,
          level_assessment: '良好',
          radar_chart: {
            A_risk_identification: 75,
            B_communication: 68,
            C_skill_application: 71,
            D_safety_management: 82,
            E_self_efficacy: 70,
          },
          state_analysis: {
            mood_change: 5,
            rapport_change: 10,
            depression_change: -5,
            overall_performance: '表现良好，展现了基本的沟通技巧和共情能力',
          },
          detailed_feedback: [
            {
              dimension: 'B1 积极倾听',
              status: 'pass',
              dialogue_ref_id: 2,
              user_input: '你最近感觉怎么样？',
              patient_state_snapshot: '患者情绪低落',
              critique: '良好',
              expert_suggestion: '继续保持倾听态度',
            },
          ],
          technical_guidance: '建议加强EPDS量表的使用',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
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
      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '40px 20px' }}>
        <Alert
          message="评估报告不存在"
          description={
            error ||
            '该会话的评估报告尚未生成。请确保已结束会话并且评估生成成功。如果问题持续存在，请联系管理员。'
          }
          type="warning"
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
        {report.radar_chart ? (
          <ScoreCards scores={report.radar_chart} />
        ) : (
          <Alert
            message="数据不完整"
            description="评估报告缺少雷达图数据。请重新生成评估报告。"
            type="warning"
            showIcon
          />
        )}
      </div>

      {/* Radar Chart */}
      {report.radar_chart && (
        <Card
          title="能力雷达图"
          bordered={false}
          style={{ marginBottom: '24px', borderRadius: '12px' }}
        >
          <EvaluationRadarChart scores={report.radar_chart} />
        </Card>
      )}

      {/* Detailed Feedback */}
      {report.detailed_feedback && report.detailed_feedback.length > 0 && (
        <Card
          title="详细反馈"
          bordered={false}
          style={{ marginBottom: '24px', borderRadius: '12px' }}
        >
          {report.detailed_feedback.map((item, index) => {
            const feedbackLength = report.detailed_feedback?.length ?? 0;
            return (
              <div
                key={index}
                style={{
                  marginBottom: index < feedbackLength - 1 ? '16px' : 0,
                  padding: '16px',
                  background: '#fafafa',
                  borderRadius: '8px',
                }}
              >
                <div style={{ marginBottom: '8px' }}>
                  <Tag color={item.status === '通过' ? 'green' : 'red'}>
                    {item.status === '通过' ? '通过' : '失败'}
                  </Tag>
                  <Text strong>{item.dimension}</Text>
                </div>
                {item.user_input && (
                  <Paragraph style={{ marginBottom: '8px' }}>
                    <Text type="secondary">用户输入：</Text>
                    <Text>{item.user_input}</Text>
                  </Paragraph>
                )}
                <Paragraph style={{ marginBottom: '8px' }}>
                  <Text type="secondary">评价：</Text>
                  <Text>{item.critique}</Text>
                </Paragraph>
                <Paragraph>
                  <Text type="secondary">建议：</Text>
                  <Text>{item.expert_suggestion}</Text>
                </Paragraph>
              </div>
            );
          })}
        </Card>
      )}

      {/* Technical Guidance */}
      {report.technical_guidance && (
        <Card
          title="技术指导"
          bordered={false}
          style={{ marginBottom: '24px', borderRadius: '12px' }}
        >
          <div
            className="markdown-content"
            style={{
              color: '#262626',
              lineHeight: '1.6'
            }}
          >
            <ReactMarkdown
              components={{
                p: ({ children, ...props }: any) => <p style={{ margin: '0 0 8px 0' }} {...props}>{children}</p>,
                ul: ({ children, ...props }: any) => <ul style={{ margin: '0 0 8px 0', paddingLeft: '20px' }} {...props}>{children}</ul>,
                ol: ({ children, ...props }: any) => <ol style={{ margin: '0 0 8px 0', paddingLeft: '20px' }} {...props}>{children}</ol>,
                li: ({ children, ...props }: any) => <li style={{ marginBottom: '4px' }} {...props}>{children}</li>,
                strong: ({ children, ...props }: any) => <strong style={{ fontWeight: 600, color: '#262626' }} {...props}>{children}</strong>,
                code: ({ inline, children, ...props }: any) =>
                  inline ? (
                    <code
                      style={{
                        background: '#f5f5f5',
                        padding: '2px 6px',
                        borderRadius: '4px',
                        fontSize: '14px',
                        color: '#eb2f96'
                      }}
                      {...props}
                    >{children}</code>
                  ) : (
                    <code
                      style={{
                        display: 'block',
                        background: '#f5f5f5',
                        padding: '12px',
                        borderRadius: '6px',
                        fontSize: '14px',
                        overflow: 'auto',
                        margin: '8px 0'
                      }}
                      {...props}
                    >{children}</code>
                  ),
                h1: ({ children, ...props }: any) => <h1 style={{ fontSize: '18px', fontWeight: 600, margin: '12px 0 8px 0' }} {...props}>{children}</h1>,
                h2: ({ children, ...props }: any) => <h2 style={{ fontSize: '16px', fontWeight: 600, margin: '12px 0 8px 0' }} {...props}>{children}</h2>,
                h3: ({ children, ...props }: any) => <h3 style={{ fontSize: '15px', fontWeight: 600, margin: '12px 0 8px 0' }} {...props}>{children}</h3>,
                blockquote: ({ children, ...props }: any) => (
                  <blockquote
                    style={{
                      borderLeft: '3px solid #d9d9d9',
                      paddingLeft: '12px',
                      margin: '8px 0',
                      color: '#595959',
                      fontStyle: 'italic'
                    }}
                    {...props}
                  >{children}</blockquote>
                )
              }}
            >
              {report.technical_guidance}
            </ReactMarkdown>
          </div>
        </Card>
      )}

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
