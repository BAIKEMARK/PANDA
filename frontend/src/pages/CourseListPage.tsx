/**
 * 课程列表页面
 */
import { useEffect, useState } from 'react';
import { Row, Col, Typography, Empty, Spin } from 'antd';
import { BookOutlined } from '@ant-design/icons';
import type { CourseLevel } from '@/types/course.types';
import { useCourseStore } from '@/stores/course.store';
import { CourseCard } from '@/components/course/CourseCard';
import { LevelFilter } from '@/components/course/LevelFilter';

const { Title, Text } = Typography;

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
      <div style={{ marginBottom: '20px' }}>
        <Title level={4} style={{ marginBottom: '4px', color: '#1a365d' }}>
          <BookOutlined style={{ marginRight: '8px' }} />
          THP课程学习
        </Title>
        <Text type="secondary">
          基于健康思维计划(THP)的围产期抑郁管理知识体系
        </Text>
      </div>

      {/* Level Filter */}
      <LevelFilter selectedLevel={selectedLevel} onLevelChange={setSelectedLevel} />

      {/* Loading State */}
      {isLoading && (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <Spin size="large" />
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !error && courses.length === 0 && (
        <Empty description="暂无课程内容" style={{ padding: '60px 0' }} />
      )}

      {/* Course Grid */}
      {!isLoading && !error && courses.length > 0 && (
        <Row gutter={[16, 16]}>
          {courses.map((course) => (
            <Col key={course.id} xs={24} sm={12} lg={8} xl={6}>
              <CourseCard course={course} />
            </Col>
          ))}
        </Row>
      )}
    </div>
  );
};
