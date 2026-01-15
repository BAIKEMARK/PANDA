/**
 * 课程详情页面
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Typography, Button, Card, Tag, Progress, Spin, Empty } from 'antd';
import { ArrowLeftOutlined, BookOutlined } from '@ant-design/icons';
import { useCourseStore } from '@/stores/course.store';
import { useUIStore } from '@/stores/ui.store';

const { Title, Paragraph, Text } = Typography;

export const CourseDetailPage = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const navigate = useNavigate();
  const { currentCourse, isLoading, error, loadCourse } = useCourseStore();
  const { setLoading } = useUIStore();
  const [readingProgress, setReadingProgress] = useState<number>(0);

  useEffect(() => {
    if (!courseId) return;

    const fetchCourse = async () => {
      setLoading(true);
      try {
        await loadCourse(Number(courseId));

        // 恢复阅读进度
        const savedProgress = localStorage.getItem(`course-${courseId}-progress`);
        if (savedProgress) {
          setReadingProgress(parseFloat(savedProgress));
          setTimeout(() => {
            window.scrollTo(0, parseFloat(savedProgress));
          }, 100);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchCourse();
  }, [courseId, loadCourse, setLoading]);

  // 保存阅读进度
  useEffect(() => {
    if (!courseId) return;

    const handleScroll = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = (scrollTop / docHeight) * 100;

      setReadingProgress(scrollTop);
      localStorage.setItem(`course-${courseId}-progress`, scrollTop.toString());
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [courseId]);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 0' }}>
        <Spin size="large" />
      </div>
    );
  }

  if (error || !currentCourse) {
    return (
      <Empty
        description={error || '课程不存在'}
        style={{ padding: '60px 0' }}
      >
        <Button type="primary" onClick={() => navigate('/courses')}>
          返回课程列表
        </Button>
      </Empty>
    );
  }

  const levelColors = {
    L1: 'green',
    L2: 'blue',
    L3: 'orange',
    L4: 'red',
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      {/* Back Button */}
      <Button
        icon={<ArrowLeftOutlined />}
        onClick={() => navigate('/courses')}
        type="text"
        style={{ marginBottom: '24px', paddingLeft: 0 }}
      >
        返回课程列表
      </Button>

      {/* Course Header */}
      <Card style={{ marginBottom: '24px' }}>
        <div style={{ marginBottom: '16px' }}>
          <Tag color={levelColors[currentCourse.level]}>
            {currentCourse.level}
          </Tag>
          <span style={{ marginLeft: '12px', color: '#8c8c8c', fontSize: '14px' }}>
            课程编号: {currentCourse.sort_order}
          </span>
        </div>

        <Title level={2} style={{ marginBottom: '16px' }}>
          {currentCourse.title}
        </Title>

        {currentCourse.description && (
          <Paragraph style={{ fontSize: '16px', color: '#595959' }}>
            {currentCourse.description}
          </Paragraph>
        )}
      </Card>

      {/* Course Content */}
      <Card>
        {currentCourse.content_url ? (
          <iframe
            src={currentCourse.content_url}
            style={{
              width: '100%',
              minHeight: '600px',
              border: 'none',
              borderRadius: '8px'
            }}
            title="课程内容"
          />
        ) : (
          <Empty
            description="课程内容正在准备中..."
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        )}
      </Card>

      {/* Reading Progress Indicator */}
      {readingProgress > 0 && (
        <Card
          style={{
            position: 'fixed',
            bottom: '24px',
            right: '24px',
            minWidth: '200px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
          }}
          bodyStyle={{ padding: '16px' }}
        >
          <div style={{ marginBottom: '8px' }}>
            <Text style={{ fontSize: '12px', color: '#8c8c8c' }}>阅读进度</Text>
          </div>
          <Progress
            percent={Math.min(
              Math.round((readingProgress / (document.documentElement.scrollHeight - window.innerHeight)) * 100),
              100
            )}
            size="small"
          />
        </Card>
      )}
    </div>
  );
};
