/**
 * 确认对话框组件
 * 统一的确认操作样式
 */
import { Modal } from 'antd';
import { ExclamationCircleOutlined } from '@ant-design/icons';

export interface ConfirmDialogOptions {
  title: string;
  content: string;
  onOk: () => void | Promise<void>;
  onCancel?: () => void;
  okText?: string;
  cancelText?: string;
  type?: 'info' | 'success' | 'error' | 'warning' | 'confirm';
}

export function showConfirmDialog({
  title,
  content,
  onOk,
  onCancel,
  okText = '确定',
  cancelText = '取消',
  type = 'confirm',
}: ConfirmDialogOptions) {
  const config = {
    title,
    content,
    okText,
    cancelText,
    onOk,
    onCancel,
    centered: true,
    icon: <ExclamationCircleOutlined />,
  };

  switch (type) {
    case 'info':
      return Modal.info(config);
    case 'success':
      return Modal.success(config);
    case 'error':
      return Modal.error(config);
    case 'warning':
      return Modal.warning(config);
    default:
      return Modal.confirm(config);
  }
}

// 快捷方法
export const confirmDelete = (
  itemName: string,
  onOk: () => void | Promise<void>
) => {
  return showConfirmDialog({
    title: '确认删除',
    content: `确定要删除"${itemName}"吗？此操作不可撤销。`,
    onOk,
    okText: '删除',
    cancelText: '取消',
    type: 'warning',
  });
};

export const confirmAction = (
  action: string,
  onOk: () => void | Promise<void>
) => {
  return showConfirmDialog({
    title: `确认${action}`,
    content: `确定要${action}吗？`,
    onOk,
    okText: '确定',
    cancelText: '取消',
  });
};
