/**
 * Common filter form component.
 */
import { Form, Row, Button, Space, Typography } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import { useCallback, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { useDebounce } from '../../hooks/useDebounce';

interface FilterFormProps {
  onSearch: (values: Record<string, unknown>) => void;
  onReset: () => void;
  children: ReactNode;
  loading?: boolean;
}

export function FilterForm({ onSearch, onReset, children }: FilterFormProps) {
  const [form] = Form.useForm();
  const [pendingValues, setPendingValues] = useState<Record<string, unknown>>({});
  const [hasInteracted, setHasInteracted] = useState(false);
  const debouncedValues = useDebounce(pendingValues, 400);

  const buildSearchValues = useCallback((values: Record<string, unknown>) => {
    // Drop empty values.
    return Object.entries(values).reduce((acc, [key, value]) => {
      if (value === undefined || value === null || value === '') {
        return acc;
      }
      if (Array.isArray(value) && value.length === 0) {
        return acc;
      }
      acc[key] = value;
      return acc;
    }, {} as Record<string, unknown>);
  }, []);

  const triggerSearch = useCallback((values?: Record<string, unknown>) => {
    const rawValues = values ?? (form.getFieldsValue() as Record<string, unknown>);
    onSearch(buildSearchValues(rawValues));
  }, [buildSearchValues, form, onSearch]);

  const handleReset = () => {
    form.resetFields();
    setPendingValues({});
    onReset();
  };

  useEffect(() => {
    if (!hasInteracted) {
      return;
    }
    triggerSearch(debouncedValues);
  }, [debouncedValues, hasInteracted, triggerSearch]);

  return (
    <div
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
        onValuesChange={(_, allValues) => {
          if (!hasInteracted) {
            setHasInteracted(true);
          }
          setPendingValues(allValues);
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '12px'
          }}
        >
          <Typography.Text style={{ fontSize: '14px', fontWeight: 600, color: '#1a365d' }}>
            筛选条件
          </Typography.Text>
          <Space>
            <Button
              icon={<ReloadOutlined />}
              onClick={handleReset}
              style={{ borderRadius: '6px' }}
            >
              重置
            </Button>
          </Space>
        </div>
        <Row gutter={16} align="bottom">
          {children}
        </Row>
      </Form>
    </div>
  );
}
