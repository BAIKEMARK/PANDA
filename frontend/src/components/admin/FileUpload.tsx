import { useState } from 'react';
import { Upload, Button, message, Progress, Space } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import type { UploadFile, UploadProps } from 'antd';
import fileService from '../../services/file.service';
import type { FileUploadResponse } from '../../types/file.types';

interface FileUploadProps {
  category?: string;
  orgId?: string;
  resourceType?: string;
  resourceId?: string;
  onSuccess?: (response: FileUploadResponse) => void;
  maxSize?: number;
  accept?: string;
}

export function FileUpload({
  category = 'courseware',
  orgId,
  resourceType,
  resourceId,
  onSuccess,
  maxSize = 100 * 1024 * 1024,
  accept,
}: FileUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleUpload: UploadProps['customRequest'] = async (options) => {
    const { file, onSuccess: onUploadSuccess, onError, onProgress } = options;
    const uploadFile = file as File;

    if (uploadFile.size > maxSize) {
      message.error(`文件大小超过限制: ${(maxSize / 1024 / 1024).toFixed(0)}MB`);
      onError?.(new Error('文件过大'));
      return;
    }

    setUploading(true);
    setProgress(0);

    try {
      const response = await fileService.upload(
        uploadFile,
        category,
        orgId,
        resourceType,
        resourceId
      );

      setProgress(100);
      message.success('上传成功');
      onUploadSuccess?.(response, {} as XMLHttpRequest);
      onSuccess?.(response);
    } catch (error: any) {
      message.error('上传失败: ' + (error.response?.data?.detail || error.message));
      onError?.(error);
    } finally {
      setUploading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  };

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Upload
        customRequest={handleUpload}
        showUploadList={false}
        accept={accept}
        disabled={uploading}
      >
        <Button icon={<UploadOutlined />} loading={uploading} disabled={uploading}>
          {uploading ? '上传中...' : '选择文件'}
        </Button>
      </Upload>
      {uploading && <Progress percent={progress} />}
    </Space>
  );
}
