/**
 * 评估报告页面
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Typography, Button, Card, Row, Col, Space, Spin, Alert, Tag } from 'antd';
import { TrophyOutlined, RocketOutlined, BookOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';
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
      } catch (err: any) {
        console.error('获取评估报告失败:', err);
        // 设置错误信息，不再使用模拟数据
        setError(err.message || '获取评估报告失败，请稍后重试');
      } finally {
        setIsLoading(false);
      }
    };

    fetchReport();
  }, [sessionId]);

  if (isLoading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        style={{ textAlign: 'center', padding: '60px 0' }}
      >
        <Spin size="large" />
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          style={{ marginTop: '16px' }}
        >
          <Text type="secondary">正在加载评估报告...</Text>
        </motion.div>
      </motion.div>
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

  // 错误状态
  if (error) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        style={{ textAlign: 'center', padding: '60px 0' }}
      >
        <Alert
          message="获取评估报告失败"
          description={error}
          type="error"
          showIcon
          style={{ maxWidth: '600px', margin: '0 auto', marginBottom: '24px' }}
        />
        <Space>
          <Button onClick={() => window.location.reload()}>重新加载</Button>
          <Button onClick={() => navigate(-1)}>返回上一页</Button>
          <Link to="/scenarios">
            <Button type="primary">继续练习</Button>
          </Link>
        </Space>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      style={{ maxWidth: '1200px', margin: '0 auto' }}
    >
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.3 }}
        style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
      >
        <div>
          <Title level={2} style={{ marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '12px' }}>
            <motion.span
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity, repeatDelay: 2 }}
            >
              <TrophyOutlined style={{ color: '#faad14' }} />
            </motion.span>
            评估报告
          </Title>
          <Paragraph type="secondary">
            对话练习 #{sessionId} 的详细评估结果
          </Paragraph>
        </div>
        <Link to="/scenarios">
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Button
              type="primary"
              size="large"
              icon={<RocketOutlined />}
              style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
              }}
            >
              继续练习
            </Button>
          </motion.div>
        </Link>
      </motion.div>

      {/* Total Score */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2, duration: 0.4 }}
      >
        <Card
          style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            marginBottom: '24px',
            borderRadius: '16px',
            border: 'none',
            boxShadow: '0 8px 24px rgba(102, 126, 234, 0.3)'
          }}
        >
          <Row gutter={24} align="middle">
            <Col>
              <div style={{ color: '#fff', opacity: 0.9, fontSize: '16px', marginBottom: '8px' }}>
                <TrophyOutlined style={{ marginRight: '8px' }} />
                综合得分
              </div>
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.4, type: 'spring', stiffness: 200 }}
                style={{
                  color: '#fff',
                  fontSize: '72px',
                  fontWeight: 'bold',
                  lineHeight: 1
                }}
              >
                {report.total_score}
              </motion.div>
            </Col>
            <Col flex="1" style={{ textAlign: 'right', color: '#fff' }}>
              <div style={{ fontSize: '14px', opacity: 0.9, marginBottom: '4px' }}>评估完成</div>
              <div style={{ fontSize: '16px', opacity: 0.8 }}>
                {new Date(report.created_at).toLocaleString('zh-CN')}
              </div>
            </Col>
          </Row>
        </Card>
      </motion.div>

      {/* Score Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        style={{ marginBottom: '24px' }}
      >
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
      </motion.div>

      {/* Radar Chart */}
      {report.radar_chart && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.4 }}
        >
          <Card
            title="能力雷达图"
            bordered={false}
            style={{ marginBottom: '24px', borderRadius: '16px', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}
          >
            <EvaluationRadarChart scores={report.radar_chart} />
          </Card>
        </motion.div>
      )}

      {/* Detailed Feedback */}
      {report.detailed_feedback && report.detailed_feedback.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.4 }}
        >
          <Card
            title="详细反馈"
            bordered={false}
            style={{ marginBottom: '24px', borderRadius: '16px', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}
          >
            {report.detailed_feedback.map((item, index) => {
              const feedbackLength = report.detailed_feedback?.length ?? 0;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6 + index * 0.05, duration: 0.3 }}
                  style={{
                    marginBottom: index < feedbackLength - 1 ? '16px' : 0,
                    padding: '16px',
                    background: 'linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%)',
                    borderRadius: '12px',
                    border: '1px solid #e8e8e8'
                  }}
                >
                  <div style={{ marginBottom: '8px' }}>
                    <Tag color={item.status === 'pass' ? 'green' : 'red'}>
                      {item.status === 'pass' ? '通过' : '失败'}
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
                </motion.div>
              );
            })}
          </Card>
        </motion.div>
      )}

      {/* Technical Guidance */}
      {report.technical_guidance && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.4 }}
        >
          <Card
            title="技术指导"
            bordered={false}
            style={{ marginBottom: '24px', borderRadius: '16px', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}
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
        </motion.div>
      )}

      {/* Action Buttons */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7, duration: 0.4 }}
        style={{ textAlign: 'center', marginTop: '32px' }}
      >
        <Space size="middle">
          <Link to="/scenarios">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button
                type="primary"
                size="large"
                icon={<RocketOutlined />}
                style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  border: 'none',
                  borderRadius: '8px',
                  boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
                }}
              >
                继续练习
              </Button>
            </motion.div>
          </Link>
          <Link to="/courses">
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button
                size="large"
                icon={<BookOutlined />}
                style={{
                  borderRadius: '8px',
                  border: '1px solid #d9d9d9'
                }}
              >
                返回课程
              </Button>
            </motion.div>
          </Link>
        </Space>
      </motion.div>
    </motion.div>
  );
};
