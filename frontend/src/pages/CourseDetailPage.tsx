/**
 * 课程详情页面
 */
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Typography, Button, Card, Tag, Spin, Empty, Breadcrumb } from 'antd';
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
  const [pdfUrl, setPdfUrl] = useState<string>('/example.pdf'); // 默认使用 example.pdf

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

  // 检查课程 PDF URL 是否有效，无效则使用 example.pdf
  useEffect(() => {
    const checkPdfUrl = async () => {
      const url = currentCourse?.content_url;

      // 如果 URL 为空、不是 PDF、或者包含 /api/（错误的路径），直接用 example.pdf
      if (!url || !url.toLowerCase().endsWith('.pdf') || url.includes('/api/')) {
        setPdfUrl('/example.pdf');
        return;
      }

      // 对于静态文件路径，尝试 HEAD 请求检测文件是否存在
      // 只检查以 / 开头的相对路径（静态文件）
      if (url.startsWith('/') && !url.startsWith('/api/')) {
        try {
          const response = await fetch(url, { method: 'HEAD' });
          // 检查响应类型是否为 PDF（避免 Vite 返回 index.html）
          const contentType = response.headers.get('content-type');
          if (response.ok && contentType?.includes('application/pdf')) {
            setPdfUrl(url);
            return;
          }
        } catch {
          // 忽略错误，使用默认值
        }
      }

      // 默认使用 example.pdf
      setPdfUrl('/example.pdf');
    };

    if (currentCourse) {
      checkPdfUrl();
    }
  }, [currentCourse]);

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
      {/* 返回按钮 */}
      <Button
        type="link"
        icon={<ArrowLeftOutlined />}
        onClick={() => navigate('/courses')}
        style={{ padding: 0, marginBottom: '16px', color: '#1890ff' }}
      >
        返回课程中心
      </Button>

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

      {/* 视频内容区域（如果有视频） */}
      {currentCourse.video_url && (
        <Card
          title={<><ReadOutlined /> 课程视频</>}
          bordered={false}
          style={{ borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', marginBottom: '24px' }}
          bodyStyle={{ padding: '16px' }}
        >
          <video
            src={currentCourse.video_url}
            controls
            style={{
              width: '100%',
              maxHeight: '600px',
              borderRadius: '8px',
              background: '#000',
            }}
          >
            您的浏览器不支持视频播放
          </video>
        </Card>
      )}

      {/* 课程课件区域 */}
      <Card
        title={<><ReadOutlined /> 课程课件</>}
        bordered={false}
        style={{ borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', minHeight: '800px' }}
        bodyStyle={{ padding: 0, height: '800px' }}
      >
        <iframe
          src={pdfUrl}
          style={{
            width: '100%',
            height: '100%',
            border: 'none',
          }}
          title={currentCourse.title}
        />
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
