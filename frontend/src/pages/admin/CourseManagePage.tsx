import { useState, useEffect } from 'react';
import { Card, Tabs, message } from 'antd';
import { FileUpload } from '../../components/admin/FileUpload';
import { FileList } from '../../components/admin/FileList';
import courseService from '../../services/course.service';
import type { Course } from '../../types/course.types';

export function CourseManagePage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourseId, setSelectedCourseId] = useState<string | null>(null);

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      const data = await courseService.getCourses();
      setCourses(data);
    } catch (error: any) {
      message.error('加载课程列表失败');
    }
  };

  const handleFileSelect = (file: any) => {
    if (selectedCourseId) {
      message.info(`已选择文件：${file.filename}`);
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card title="课程课件管理">
        <Tabs
          items={[
            {
              key: 'upload',
              label: '上传课件',
              children: (
              <div>
                <h3>上传新课件</h3>
                  <FileUpload
                    category="courseware"
                    resourceType="course"
                    resourceId={selectedCourseId || undefined}
                  />
                  {selectedCourseId && (
                    <div style={{ marginTop: '16px' }}>
                      <h4>已选课程的文件</h4>
                      <FileList
                        category="courseware"
                        resourceType="course"
                        resourceId={selectedCourseId}
                      />
                    </div>
                  )}
                </div>
              ),
            },
            {
              key: 'list',
              label: '课件列表',
              children: (
                <FileList
                  category="courseware"
                  resourceType="course"
                  onSelect={handleFileSelect}
                />
              ),
            },
          ]}
        />
      </Card>
    </div>
  );
}



