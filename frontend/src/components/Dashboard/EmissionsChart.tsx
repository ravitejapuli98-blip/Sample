import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Typography, Space, Statistic } from 'antd';
import { ArrowDownOutlined } from '@ant-design/icons';

const { Text } = Typography;

const EmissionsChart: React.FC = () => {
  // Mock data - in production this would come from the API
  const data = [
    { month: 'Jan', emissions: 1200, target: 1000 },
    { month: 'Feb', emissions: 1150, target: 1000 },
    { month: 'Mar', emissions: 1100, target: 1000 },
    { month: 'Apr', emissions: 1050, target: 1000 },
    { month: 'May', emissions: 1000, target: 1000 },
    { month: 'Jun', emissions: 950, target: 1000 },
  ];

  const currentEmissions = data[data.length - 1].emissions;
  const previousEmissions = data[data.length - 2].emissions;
  const reduction = ((previousEmissions - currentEmissions) / previousEmissions) * 100;

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Statistic
          title="Current CO₂ Emissions"
          value={currentEmissions}
          suffix="tonnes"
          valueStyle={{ color: '#52c41a' }}
        />
        <Statistic
          title="Monthly Reduction"
          value={reduction}
          precision={1}
          suffix="%"
          prefix={<ArrowDownOutlined />}
          valueStyle={{ color: '#52c41a' }}
        />
      </Space>
      
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip 
            formatter={(value, name) => [
              `${value} tonnes`, 
              name === 'emissions' ? 'Actual' : 'Target'
            ]}
          />
          <Line 
            type="monotone" 
            dataKey="emissions" 
            stroke="#52c41a" 
            strokeWidth={2}
            dot={{ fill: '#52c41a', strokeWidth: 2, r: 4 }}
          />
          <Line 
            type="monotone" 
            dataKey="target" 
            stroke="#ff4d4f" 
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: '#ff4d4f', strokeWidth: 2, r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
      
      <div style={{ marginTop: 8 }}>
        <Text type="secondary" style={{ fontSize: 12 }}>
          Green line: Actual emissions | Red dashed line: Target
        </Text>
      </div>
    </div>
  );
};

export default EmissionsChart;
