/**
 * 课程层级筛选器
 */
import { Radio, Space } from 'antd';
import type { CourseLevel } from '@/types/course.types';

interface LevelFilterProps {
  selectedLevel: CourseLevel | 'all';
  onLevelChange: (level: CourseLevel | 'all') => void;
}

export const LevelFilter = ({ selectedLevel, onLevelChange }: LevelFilterProps) => {
  return (
    <Space style={{ marginBottom: '24px' }}>
      <span style={{ color: '#595959', fontWeight: 500 }}>课程层级:</span>
      <Radio.Group
        value={selectedLevel}
        onChange={(e) => onLevelChange(e.target.value)}
        buttonStyle="solid"
      >
        <Radio.Button value="all">全部</Radio.Button>
        <Radio.Button value="L1">一级</Radio.Button>
        <Radio.Button value="L2">二级</Radio.Button>
        <Radio.Button value="L3">三级</Radio.Button>
        <Radio.Button value="L4">四级</Radio.Button>
      </Radio.Group>
    </Space>
  );
};
