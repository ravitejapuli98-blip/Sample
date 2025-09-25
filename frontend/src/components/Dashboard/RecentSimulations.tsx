import React from 'react';
import { List, Typography, Tag, Space, Button } from 'antd';
import { ClockCircleOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { useQuery } from 'react-query';
import { useNavigate } from 'react-router-dom';
import { endpoints } from '../../services/api';

const { Text, Title } = Typography;

const RecentSimulations: React.FC = () => {
  const navigate = useNavigate();
  
  const { data: simulations, isLoading } = useQuery(
    'recent-simulations',
    () => endpoints.simulations.list({ limit: 5 }).then(res => res.data)
  );

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case 'running':
        return <ClockCircleOutlined style={{ color: '#1890ff' }} />;
      case 'failed':
        return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />;
      default:
        return <ClockCircleOutlined style={{ color: '#faad14' }} />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'running':
        return 'processing';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  if (isLoading) {
    return <Text>Loading simulations...</Text>;
  }

  if (!simulations || simulations.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '20px 0' }}>
        <Text type="secondary">No simulations found</Text>
        <br />
        <Button 
          type="link" 
          onClick={() => navigate('/simulations')}
          style={{ marginTop: 8 }}
        >
          Create your first simulation
        </Button>
      </div>
    );
  }

  return (
    <List
      dataSource={simulations}
      renderItem={(simulation: any) => (
        <List.Item
          style={{ 
            padding: '12px 0',
            borderBottom: '1px solid #f0f0f0',
            cursor: 'pointer'
          }}
          onClick={() => navigate(`/simulations/${simulation.id}`)}
        >
          <List.Item.Meta
            avatar={getStatusIcon(simulation.status)}
            title={
              <Space>
                <Text strong>{simulation.name}</Text>
                <Tag color={getStatusColor(simulation.status)}>
                  {simulation.status}
                </Tag>
              </Space>
            }
            description={
              <Space direction="vertical" size="small">
                <Text type="secondary" style={{ fontSize: 12 }}>
                  {simulation.simulation_type} • {simulation.agent_count} agents
                </Text>
                {simulation.progress_percent > 0 && (
                  <div>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      Progress: {simulation.progress_percent.toFixed(1)}%
                    </Text>
                  </div>
                )}
              </Space>
            }
          />
        </List.Item>
      )}
    />
  );
};

export default RecentSimulations;
