/**
 * 课程详情页面
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Typography, Button, Card, Tag, Spin, Empty, Breadcrumb, Divider, Alert } from 'antd';
import {
  ArrowLeftOutlined,
  ReadOutlined,
  HomeOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import { useCourseStore } from '@/stores/course.store';
import { useUIStore } from '@/stores/ui.store';
import { CourseLevel } from '@/types/course.types';

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
      // 只有当当前课程不是目标课程时才加载
      if (currentCourse?.id === courseId) return;

      setLoading(true);
      try {
        // ID 是字符串 (e.g., 'c-001')，不要转换为 Number
        await loadCourse(courseId);

        // 恢复阅读进度 (简单的本地存储方案)
        const savedProgress = localStorage.getItem(`course-${courseId}-progress`);
        if (savedProgress) {
          setReadingProgress(parseFloat(savedProgress));
          // 延迟滚动，等待 iframe/内容 加载
          setTimeout(() => {
            window.scrollTo(0, parseFloat(savedProgress));
          }, 500);
        }
      } catch (err) {
        console.error("加载课程失败:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCourse();
  }, [courseId, loadCourse, setLoading, currentCourse?.id]);

  // 监听滚动以保存阅读进度
  useEffect(() => {
    if (!courseId) return;

    const handleScroll = () => {
      const scrollTop = window.scrollY;
      setReadingProgress(scrollTop);
      localStorage.setItem(`course-${courseId}-progress`, scrollTop.toString());
    };

    // 使用 debounce 优化滚动监听可能更好，这里保持简单
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [courseId]);

  if (isLoading && !currentCourse) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 0' }}>
        <Spin size="large" tip="加载课程内容..." />
      </div>
    );
  }

  if (error || (!isLoading && !currentCourse)) {
    return (
      <div style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
        <Empty
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          description={
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', alignItems: 'center' }}>
              <Text type="secondary" style={{ fontSize: '16px' }}>{error || '未找到该课程'}</Text>
              <Button type="primary" onClick={() => navigate('/courses')}>
                返回课程中心
              </Button>
            </div>
          }
        />
      </div>
    );
  }

  // 安全检查
  if (!currentCourse) return null;

  const levelConfig: Record<CourseLevel, { color: string; label: string }> = {
    L1: { color: 'green', label: '一级 (基础)' },
    L2: { color: 'blue', label: '二级 (进阶)' },
    L3: { color: 'orange', label: '三级 (高级)' },
    L4: { color: 'red', label: '四级 (专家)' },
  };

  const levelInfo = levelConfig[currentCourse.level as CourseLevel] || { color: 'default', label: currentCourse.level };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px' }}>
      {/* 导航面包屑 */}
      <Breadcrumb
        items={[
          {
            title: <span style={{ cursor: 'pointer' }} onClick={() => navigate('/')}><HomeOutlined /> 首页</span>,
          },
          {
            title: <span style={{ cursor: 'pointer' }} onClick={() => navigate('/courses')}>课程中心</span>,
          },
          {
            title: currentCourse.title,
          },
        ]}
        style={{ marginBottom: '24px' }}
      />

      {/* 课程头部概览 */}
      <Card bordered={false} style={{ marginBottom: '24px', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ flex: 1, minWidth: '300px' }}>
            <div style={{ marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Tag color={levelInfo.color} style={{ margin: 0, padding: '0 10px', fontSize: '13px', lineHeight: '22px' }}>
                {levelInfo.label}
              </Tag>
              <Text type="secondary" style={{ fontSize: '13px' }}>
                编号: {currentCourse.id}
              </Text>
            </div>

            <Title level={2} style={{ margin: '0 0 16px 0' }}>
              {currentCourse.title}
            </Title>

            <Paragraph type="secondary" style={{ fontSize: '16px', marginBottom: '20px', maxWidth: '800px' }}>
              {currentCourse.description || '暂无课程描述'}
            </Paragraph>

            <div style={{ display: 'flex', gap: '16px', fontSize: '14px', color: '#8c8c8c' }}>
              <span><ClockCircleOutlined /> 预计阅读时间: 15-30 分钟</span>
              <span><ReadOutlined /> 文档类型: PDF</span>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', minWidth: '150px' }}>
            {/* 未来可以集成已学习状态 */}
            <div style={{ textAlign: 'center', background: '#f6ffed', border: '1px solid #b7eb8f', padding: '12px', borderRadius: '8px' }}>
              <CheckCircleOutlined style={{ color: '#52c41a', fontSize: '24px', marginBottom: '4px' }} />
              <div style={{ color: '#52c41a', fontWeight: 500 }}>学习进度记录中</div>
            </div>
          </div>
        </div>
      </Card>

      {/* 课程内容区域 */}
      <Card
        title={<><ReadOutlined /> 课程课件</>}
        bordered={false}
        style={{ borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', minHeight: '800px' }}
        bodyStyle={{ padding: 0, height: '800px' }}
      >
        {(() => {
          const url = currentCourse.content_url;
          // 简单的检查：如果 URL 是相对路径且本地实际上没有这些文件（即开发环境），
          // 这会导致 Vite 返回 index.html，从而在 iframe 里套娃显示网页。
          // 这里我们做一个简单的后缀检查，或者默认显示占位符
          const isPdf = url && url.toLowerCase().endsWith('.pdf');

          // 在开发环境中，如果没有真实部署 PDF，暂时显示 Empty 状态，避免套娃
          // 或者可以使用一个在线的示例 PDF 用于演示
          // const demoPdf = "https://mozilla.github.io/pdf.js/web/compressed.tracemonkey-pldi-09.pdf";

          if (url && isPdf) {
            return (
              <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#f5f5f5' }}>
                {/* 
                   注意：由于本地 public 文件夹下缺少对应的 PDF 文件，直接 iframe 加载会触发 404 -> index.html 回退。
                   为了避免"网页套娃"现象，这里先注释掉 iframe，除非确认文件存在。
                   在生产环境中，应该确保 content_url 指向真实存在的静态资源。
                 */}
                <Empty
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                  description={
                    <div>
                      <Text strong>演示环境：部分课件文件未上传</Text>
                      <br />
                      <Text type="secondary" style={{ fontSize: '12px' }}>
                        目标文件: {url} <br />
                        请在 frontend/public/courses/ 目录下放置对应 PDF 文件
                      </Text>
                    </div>
                  }
                />
                {/* 如果你确实有了文件，取消下面注释即可 */}
                {/* 
                  <iframe
                    src={url}
                    style={{
                      width: '100%',
                      height: '100%',
                      border: 'none',
                    }}
                    title={currentCourse.title}
                  /> 
                  */}
              </div>
            );
          }

          return (
            <div style={{ height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column' }}>
              <Empty description="暂无课件内容 (URL无效或非PDF)" />
            </div>
          );
        })()}
      </Card>

      {/* 底部浮动进度提示 (可选，增强体验) */}
      {readingProgress > 500 && (
        <div style={{
          position: 'fixed',
          bottom: '40px',
          right: '40px',
          background: 'rgba(0,0,0,0.7)',
          color: '#fff',
          padding: '8px 16px',
          borderRadius: '20px',
          fontSize: '12px',
          backdropFilter: 'blur(4px)',
          animation: 'fadeIn 0.3s ease'
        }}>
          已阅读至当前位置
        </div>
      )}
    </div>
  );
};
