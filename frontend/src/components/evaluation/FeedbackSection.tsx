/**
 * AI反馈部分组件
 */
import { Card, Typography, Empty } from 'antd';

const { Title, Paragraph, Text } = Typography;

interface FeedbackSectionProps {
  feedback?: string;
}

export const FeedbackSection = ({ feedback }: FeedbackSectionProps) => {
  if (!feedback) {
    return (
      <Card bordered={false} style={{ borderRadius: '12px' }}>
        <Title level={4} style={{ marginBottom: '16px' }}>AI反馈</Title>
        <Empty description="暂无反馈" />
      </Card>
    );
  }

  return (
    <Card bordered={false} style={{ borderRadius: '12px' }}>
      <Title level={4} style={{ marginBottom: '16px' }}>AI反馈</Title>
      <Paragraph style={{
        whiteSpace: 'pre-wrap',
        color: '#595959',
        lineHeight: '1.8',
        fontSize: '15px'
      }}>
        {feedback}
      </Paragraph>
    </Card>
  );
};
