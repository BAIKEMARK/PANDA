/**
 * 通用筛选表单组件
 */
import { Form, Row, Col, Button, Space } from 'antd';
import { SearchOutlined, ReloadOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import type { ReactNode } from 'react';

interface FilterFormProps {
  onSearch: (values: any) => void;
  onReset: () => void;
  children: ReactNode;
  loading?: boolean;
}

export function FilterForm({ onSearch, onReset, children, loading = false }: FilterFormProps) {
  const [form] = Form.useForm();

  const handleSearch = () => {
    const values = form.getFieldsValue();
    // 过滤掉空值
    const filteredValues = Object.entries(values).reduce((acc, [key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        acc[key] = value;
      }
      return acc;
    }, {} as any);
    onSearch(filteredValues);
  };

  const handleReset = () => {
    form.resetFields();
    onReset();
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      style={{
        background: 'linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%)',
        padding: '20px',
        borderRadius: '12px',
        marginBottom: '20px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
      }}
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSearch}
      >
        <Row gutter={16}>
          {children}
        </Row>
        <Row>
          <Col span={24} style={{ textAlign: 'right' }}>
            <Space>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  icon={<ReloadOutlined />}
                  onClick={handleReset}
                  style={{ borderRadius: '6px' }}
                >
                  重置
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  type="primary"
                  icon={<SearchOutlined />}
                  htmlType="submit"
                  loading={loading}
                  style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    border: 'none',
                    borderRadius: '6px',
                    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
                  }}
                >
                  查询
                </Button>
              </motion.div>
            </Space>
          </Col>
        </Row>
      </Form>
    </motion.div>
  );
}
