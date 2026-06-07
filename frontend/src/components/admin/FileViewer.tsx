import { useState, useEffect } from 'react';
import { Modal, Spin, message, Button, Space } from 'antd';
import { EyeOutlined, DownloadOutlined } from '@ant-design/icons';
import fileService from '../../services/file.service';
import type { FileInfo } from '../../types/file.types';

interface FileViewerProps {
  fileId: string;
  visible: boolean;
  onClose: () => void;
}

export function FileViewer({ fileId, visible, onClose }: FileViewerProps) {
  const [file, setFile] = useState<FileInfo | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (visible && fileId) {
      loadFile();
    }
  }, [visible, fileId]);

  const loadFile = async () => {
    setLoading(true);
    try {
      const fileData = await fileService.get(fileId);
      setFile(fileData);
    } catch (error: any) {
      message.error('加载文件失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const canPreview = (mimeType?: string) => {
    if (!mimeType) return false;
    return (
      mimeType.startsWith('image/') ||
      mimeType === 'application/pdf' ||
      mimeType.startsWith('text/') ||
      mimeType.includes('video') ||
      mimeType.includes('audio')
    );
  };

  const getPreviewUrl = () => {
    if (!file) return '';
    return fileService.getViewUrl(file.id);
  };

  const handleDownload = () => {
    if (!file) return;
    window.open(fileService.getDownloadUrl(file.id), '_blank');
  };

  if (!file) {
    return (
      <Modal
        title="文件预览"
        open={visible}
        onCancel={onClose}
        footer={null}
        width={800}
      >
        <Spin spinning={loading} />
      </Modal>
    );
  }

  return (
    <Modal
      title={file.filename}
      open={visible}
      onCancel={onClose}
      footer={
        <Space>
          <Button icon={<DownloadOutlined />} onClick={handleDownload}>
            下载
          </Button>
          <Button onClick={onClose}>关闭</Button>
        </Space>
      }
      width={1000}
      style={{ top: 20 }}
    >
      <div style={{ minHeight: '600px' }}>
        {canPreview(file.mime_type) ? (
          <iframe
            src={getPreviewUrl()}
            style={{
              width: '100%',
              height: '600px',
              border: 'none',
            }}
            title={file.filename}
          />
        ) : (
          <div style={{ textAlign: 'center', padding: '100px 0' }}>
            <p>该文件类型不支持在线预览</p>
            <Button type="primary" icon={<DownloadOutlined />} onClick={handleDownload}>
              下载文件
            </Button>
          </div>
        )}
      </div>
    </Modal>
  );
}
