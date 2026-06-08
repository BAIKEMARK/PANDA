/**
 * 课程卡片组件
 */
import { NavLink } from 'react-router-dom';
import { Card, Tag, Typography, Progress } from 'antd';
import { BookOutlined, ClockCircleOutlined } from '@ant-design/icons';
import type { Course } from '@/types/course.types';

const { Paragraph, Text, Title } = Typography;

interface CourseCardProps {
  course: Course;
  progress?: number;
}

const levelColors = {
  L1: { color: 'green', text: '一级 (基础)' },
  L2: { color: 'blue', text: '二级 (进阶)' },
  L3: { color: 'orange', text: '三级 (高级)' },
  L4: { color: 'red', text: '四级 (专家)' },
};

export const CourseCard = ({ course, progress = 0 }: CourseCardProps) => {
  const levelInfo = levelColors[course.level];

  return (
    <NavLink to={`/courses/${course.id}`}>
      <Card
        hoverable
        cover={
          <div style={{
            height: '180px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            position: 'relative'
          }}>
            <BookOutlined style={{ fontSize: '64px', color: 'rgba(255,255,255,0.8)' }} />
            <Tag
              color={levelInfo.color}
              style={{
                position: 'absolute',
                top: '16px',
                right: '16px'
              }}
            >
              {levelInfo.text}
            </Tag>
          </div>
        }
        style={{ borderRadius: '12px', overflow: 'hidden' }}
        bodyStyle={{ padding: '20px' }}
      >
        <Title level={5} style={{ marginBottom: '12px' }} ellipsis={{ rows: 1 }}>
          {course.title}
        </Title>

        {course.description && (
          <Paragraph
            type="secondary"
            style={{ display: 'block', marginBottom: '16px' }}
            ellipsis={{ rows: 2 }}
          >
            {course.description}
          </Paragraph>
        )}

        {progress > 0 && (
          <div style={{ marginBottom: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <Text type="secondary" style={{ fontSize: '12px' }}>学习进度</Text>
              <Text style={{ fontSize: '12px', fontWeight: 500 }}>{Math.round(progress)}%</Text>
            </div>
            <Progress
              percent={Math.round(progress)}
              size="small"
              strokeColor="#1890ff"
            />
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            <ClockCircleOutlined style={{ marginRight: '4px' }} />
            编号: {course.sort_order}
          </Text>
          <Text style={{ color: '#1890ff', fontSize: '13px', fontWeight: 500 }}>
            查看详情 →
          </Text>
        </div>
      </Card>
    </NavLink>
  );
};
