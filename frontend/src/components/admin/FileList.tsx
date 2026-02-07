import { useState, useEffect } from 'react';
import { Table, Button, Space, Tag, message, Popconfirm } from 'antd';
import { EyeOutlined, DeleteOutlined } from '@ant-design/icons';
import fileService from '../../services/file.service';
import { FileViewer } from './FileViewer';
import type { FileInfo } from '../../types/file.types';

interface FileListProps {
  category?: string;
  resourceType?: string;
  resourceId?: string;
  orgId?: string;
  onSelect?: (file: FileInfo) => void;
}

export function FileList({
  category,
  resourceType,
  resourceId,
  orgId,
  onSelect,
}: FileListProps) {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [viewingFileId, setViewingFileId] = useState<string | null>(null);

  useEffect(() => {
    loadFiles();
  }, [category, resourceType, resourceId, orgId]);

  const loadFiles = async () => {
    setLoading(true);
    try {
      const data = await fileService.list(orgId, category, resourceType, resourceId);
      setFiles(data.files);
      setTotal(data.total);
    } catch (error: any) {
      message.error('加载文件列表失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await fileService.delete(id);
      message.success('删除成功');
      loadFiles();
    } catch (error: any) {
      message.error('删除失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return '-';
    if (bytes < 1024) return `${bytes}B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)}KB`;
    return `${(bytes / 1024 / 1024).toFixed(2)}MB`;
  };

  const columns = [
    {
      title: '文件名',
      dataIndex: 'filename',
      key: 'filename',
      render: (text: string, record: FileInfo) => (
        <Button type="link" onClick={() => setViewingFileId(record.id)}>
          {text}
        </Button>
      ),
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      render: (category: string) => <Tag>{category}</Tag>,
    },
    {
      title: '大小',
      dataIndex: 'file_size',
      key: 'file_size',
      render: (size: number) => formatFileSize(size),
    },
    {
      title: '类型',
      dataIndex: 'file_type',
      key: 'file_type',
    },
    {
      title: '上传时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleString('zh-CN'),
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: FileInfo) => (
        <Space>
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => setViewingFileId(record.id)}
          >
            预览
          </Button>
          {onSelect && (
            <Button type="link" onClick={() => onSelect(record)}>
              选择
            </Button>
          )}
          <Popconfirm
            title="确定删除这个文件吗？"
            onConfirm={() => handleDelete(record.id)}
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <>
      <Table
        columns={columns}
        dataSource={files}
        loading={loading}
        rowKey="id"
        pagination={{
          total,
          pageSize: 10,
          showTotal: (total) => `共 ${total} 个文件`,
        }}
      />
      {viewingFileId && (
        <FileViewer
          fileId={viewingFileId}
          visible={!!viewingFileId}
          onClose={() => setViewingFileId(null)}
        />
      )}
    </>
  );
}
