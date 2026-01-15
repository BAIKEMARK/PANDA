/**
 * 课程列表页面
 */
import { useEffect, useState } from 'react';
import { Row, Col, Typography, Empty, Spin, Alert } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import type { CourseLevel } from '@/types/course.types';
import { useCourseStore } from '@/stores/course.store';
import { CourseCard } from '@/components/course/CourseCard';
import { LevelFilter } from '@/components/course/LevelFilter';

const { Title, Paragraph } = Typography;

export const CourseListPage = () => {
  const { courses, isLoading, error, loadCourses } = useCourseStore();
  const [selectedLevel, setSelectedLevel] = useState<CourseLevel | 'all'>('all');

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        await loadCourses(selectedLevel === 'all' ? undefined : selectedLevel);
      } catch (err) {
        // Error handled by store
      }
    };

    fetchCourses();
  }, [selectedLevel, loadCourses]);

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <Title level={2} style={{ marginBottom: '8px' }}>
          课程学习
        </Title>
        <Paragraph type="secondary" style={{ fontSize: '16px' }}>
          学习围产期抑郁症相关知识，提升专业能力
        </Paragraph>
      </div>

      {/* Level Filter */}
      <LevelFilter selectedLevel={selectedLevel} onLevelChange={setSelectedLevel} />

      {/* Loading State */}
      {isLoading && (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <Spin indicator={<LoadingOutlined style={{ fontSize: '48px' }} spin />} />
          <div style={{ marginTop: '16px', color: '#8c8c8c' }}>加载中...</div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <Alert
          title="加载失败"
          description={error}
          type="error"
          showIcon
          style={{ marginBottom: '24px' }}
        />
      )}

      {/* Empty State */}
      {!isLoading && !error && courses.length === 0 && (
        <Empty
          description="暂无课程内容"
          style={{ padding: '60px 0' }}
        />
      )}

      {/* Course Grid */}
      {!isLoading && !error && courses.length > 0 && (
        <Row gutter={[16, 16]}>
          {courses.map((course) => (
            <Col key={course.id} xs={24} sm={12} lg={8}>
              <CourseCard course={course} />
            </Col>
          ))}
        </Row>
      )}
    </div>
  );
};
