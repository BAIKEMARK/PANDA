import { useEffect, useState } from 'react';
import { Card, Table, message, Spin } from 'antd';
import { adminService } from '../services/admin.service';
import type { Organization } from '../types';

export function AdminDashboardPage() {
  const [loading, setLoading] = useState(false);
  const [orgs, setOrgs] = useState<Organization[]>([]);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const res = await adminService.getOrganizations();
        setOrgs(res.data);
      } catch (err) {
        message.error('加载机构列表失败');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <Card title="系统管理 / 机构列表">
      <Spin spinning={loading}>
        <Table
          rowKey="id"
          dataSource={orgs}
          pagination={false}
          columns={[
            { title: '机构名称', dataIndex: 'name' },
            { title: '简称', dataIndex: 'short_name' },
            { title: '状态', dataIndex: 'status' },
            { title: 'ID', dataIndex: 'id' },
          ]}
        />
      </Spin>
    </Card>
  );
}
