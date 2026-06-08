/**
 * 仪表盘统计卡片
 */
import { Card, Statistic } from 'antd';
import type { ReactNode } from 'react';

interface StatsCardProps {
    title: string;
    value: number | string;
    icon?: ReactNode;
    suffix?: string;
    color?: string;
}

export const StatsCard = ({ title, value, icon, suffix, color = '#1890ff' }: StatsCardProps) => {
    return (
        <Card variant="borderless" style={{ borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Statistic
                    title={<span style={{ fontSize: '14px', color: '#8c8c8c' }}>{title}</span>}
                    value={value}
                    suffix={<span style={{ fontSize: '14px' }}>{suffix}</span>}
                    styles={{ content: { fontWeight: 600, color: '#262626' } }}
                />
                {icon && (
                    <div style={{
                        width: '48px',
                        height: '48px',
                        borderRadius: '12px',
                        background: `${color}15`, // Light opacity background
                        color: color,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '24px'
                    }}>
                        {icon}
                    </div>
                )}
            </div>
        </Card>
    );
};
