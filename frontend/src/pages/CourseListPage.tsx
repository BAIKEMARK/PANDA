/**
 * 课程列表页面
 */
import { useEffect, useState } from 'react';
import { Row, Col, Typography, Empty, Spin } from 'antd';
import { BookOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
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
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
    >
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.3 }}
        style={{ marginBottom: '24px' }}
      >
        <Title level={4} style={{ marginBottom: '8px', color: '#1a365d', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <motion.span
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
          >
            <BookOutlined />
          </motion.span>
          THP课程学习
        </Title>
        <Text type="secondary" style={{ fontSize: '14px' }}>
          基于健康思维计划(THP)的围产期抑郁管理知识体系
        </Text>
      </motion.div>

      {/* Level Filter */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.3 }}
      >
        <LevelFilter selectedLevel={selectedLevel} onLevelChange={setSelectedLevel} />
      </motion.div>

      {/* Loading State */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{ textAlign: 'center', padding: '60px 0' }}
        >
          <Spin size="large" />
        </motion.div>
      )}

      {/* Empty State */}
      {!isLoading && !error && courses.length === 0 && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
        >
          <Empty description="暂无课程内容" style={{ padding: '60px 0' }} />
        </motion.div>
      )}

      {/* Course Grid */}
      {!isLoading && !error && courses.length > 0 && (
        <Row gutter={[16, 16]}>
          {courses.map((course, index) => (
            <Col key={course.id} xs={24} sm={12} lg={8} xl={6}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05, duration: 0.3 }}
                whileHover={{ y: -8 }}
              >
                <CourseCard course={course} />
              </motion.div>
            </Col>
          ))}
        </Row>
      )}
    </motion.div>
  );
};
