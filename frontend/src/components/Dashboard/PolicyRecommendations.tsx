import React from 'react';
import { List, Typography, Tag, Space, Button, Progress } from 'antd';
import { 
  ThunderboltOutlined, 
  ClockCircleOutlined, 
  DollarOutlined,
  EnvironmentOutlined 
} from '@ant-design/icons';
import { useQuery } from 'react-query';
import { useNavigate } from 'react-router-dom';
import { endpoints } from '../../services/api';

const { Text, Title } = Typography;

const PolicyRecommendations: React.FC = () => {
  const navigate = useNavigate();
  
  const { data: recommendations, isLoading } = useQuery(
    'policy-recommendations',
    () => endpoints.policies.recommendations(1, {
      max_budget: 10000000,
      max_timeline_months: 24,
      min_equity_score: 0.5,
      required_co2_reduction: 1000
    }).then(res => res.data.recommendations || []),
    {
      enabled: false, // Disable by default, enable when needed
    }
  );

  const getRecommendationTypeColor = (type: string) => {
    switch (type) {
      case 'quick_win':
        return 'green';
      case 'high_impact':
        return 'red';
      case 'equity_focused':
        return 'blue';
      case 'long_term':
        return 'orange';
      default:
        return 'default';
    }
  };

  const getRecommendationTypeIcon = (type: string) => {
    switch (type) {
      case 'quick_win':
        return <ThunderboltOutlined />;
      case 'high_impact':
        return <EnvironmentOutlined />;
      case 'equity_focused':
        return <DollarOutlined />;
      case 'long_term':
        return <ClockCircleOutlined />;
      default:
        return <ThunderboltOutlined />;
    }
  };

  if (isLoading) {
    return <Text>Loading recommendations...</Text>;
  }

  if (!recommendations || recommendations.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '20px 0' }}>
        <Text type="secondary">No recommendations available</Text>
        <br />
        <Button 
          type="link" 
          onClick={() => navigate('/policies')}
          style={{ marginTop: 8 }}
        >
          Generate recommendations
        </Button>
      </div>
    );
  }

  return (
    <List
      dataSource={recommendations.slice(0, 3)} // Show top 3
      renderItem={(recommendation: any) => (
        <List.Item
          style={{ 
            padding: '12px 0',
            borderBottom: '1px solid #f0f0f0',
            cursor: 'pointer'
          }}
          onClick={() => navigate('/policies')}
        >
          <List.Item.Meta
            avatar={getRecommendationTypeIcon(recommendation.recommendation_type)}
            title={
              <Space>
                <Text strong>{recommendation.title}</Text>
                <Tag color={getRecommendationTypeColor(recommendation.recommendation_type)}>
                  {recommendation.recommendation_type?.replace('_', ' ')}
                </Tag>
              </Space>
            }
            description={
              <Space direction="vertical" size="small">
                <Text type="secondary" style={{ fontSize: 12 }}>
                  {recommendation.description}
                </Text>
                <Space size="small">
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    <DollarOutlined /> ${(recommendation.estimated_cost / 1000000).toFixed(1)}M
                  </Text>
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    <ClockCircleOutlined /> {recommendation.timeline_months}mo
                  </Text>
                </Space>
                <div>
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    Priority: 
                  </Text>
                  <Progress 
                    percent={recommendation.priority_score * 100} 
                    size="small" 
                    showInfo={false}
                    style={{ width: 100, display: 'inline-block', marginLeft: 8 }}
                  />
                </div>
              </Space>
            }
          />
        </List.Item>
      )}
    />
  );
};

export default PolicyRecommendations;
