import React from 'react';
import { Row, Col, Card, Statistic, Typography, Space, Button } from 'antd';
import { 
  EnvironmentOutlined, 
  PolicyOutlined, 
  ExperimentOutlined,
  BarChartOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined
} from '@ant-design/icons';
import { useQuery } from 'react-query';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import CityMap from '../components/Dashboard/CityMap';
import RecentSimulations from '../components/Dashboard/RecentSimulations';
import PolicyRecommendations from '../components/Dashboard/PolicyRecommendations';
import EmissionsChart from '../components/Dashboard/EmissionsChart';
import { api } from '../services/api';

const { Title, Text } = Typography;

const Dashboard: React.FC = () => {
  const navigate = useNavigate();

  // Fetch dashboard data
  const { data: dashboardData, isLoading } = useQuery(
    'dashboard',
    () => api.get('/cities/1/dashboard').then(res => res.data),
    {
      refetchInterval: 30000, // Refetch every 30 seconds
    }
  );

  const { data: cities } = useQuery(
    'cities',
    () => api.get('/cities').then(res => res.data)
  );

  const { data: policies } = useQuery(
    'policies',
    () => api.get('/policies').then(res => res.data)
  );

  const { data: simulations } = useQuery(
    'simulations',
    () => api.get('/simulations').then(res => res.data)
  );

  const stats = [
    {
      title: 'Cities Monitored',
      value: cities?.length || 0,
      icon: <EnvironmentOutlined style={{ fontSize: 24, color: '#1890ff' }} />,
      color: '#1890ff',
    },
    {
      title: 'Active Policies',
      value: policies?.filter((p: any) => p.status === 'active')?.length || 0,
      icon: <PolicyOutlined style={{ fontSize: 24, color: '#52c41a' }} />,
      color: '#52c41a',
    },
    {
      title: 'Simulations Run',
      value: simulations?.length || 0,
      icon: <ExperimentOutlined style={{ fontSize: 24, color: '#faad14' }} />,
      color: '#faad14',
    },
    {
      title: 'CO₂ Reduced (tonnes)',
      value: 1250,
      icon: <BarChartOutlined style={{ fontSize: 24, color: '#722ed1' }} />,
      color: '#722ed1',
      suffix: <ArrowDownOutlined style={{ color: '#52c41a' }} />,
    },
  ];

  return (
    <>
      <Helmet>
        <title>Dashboard - AI Sustainable Cities Planner</title>
      </Helmet>

      <div className="fade-in">
        <div style={{ marginBottom: 24 }}>
          <Title level={2}>Dashboard</Title>
          <Text type="secondary">
            Monitor your cities' sustainability progress and policy impacts
          </Text>
        </div>

        {/* Key Metrics */}
        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          {stats.map((stat, index) => (
            <Col xs={24} sm={12} lg={6} key={index}>
              <Card className="dashboard-card">
                <Statistic
                  title={stat.title}
                  value={stat.value}
                  prefix={stat.icon}
                  suffix={stat.suffix}
                  valueStyle={{ color: stat.color }}
                />
              </Card>
            </Col>
          ))}
        </Row>

        {/* Main Content */}
        <Row gutter={[16, 16]}>
          {/* City Map */}
          <Col xs={24} lg={16}>
            <Card 
              title="City Overview" 
              className="dashboard-card"
              extra={
                <Button 
                  type="primary" 
                  onClick={() => navigate('/cities')}
                >
                  View All Cities
                </Button>
              }
            >
              <CityMap />
            </Card>
          </Col>

          {/* Recent Simulations */}
          <Col xs={24} lg={8}>
            <Card 
              title="Recent Simulations" 
              className="dashboard-card"
              extra={
                <Button 
                  type="link" 
                  onClick={() => navigate('/simulations')}
                >
                  View All
                </Button>
              }
            >
              <RecentSimulations />
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
          {/* Policy Recommendations */}
          <Col xs={24} lg={12}>
            <Card 
              title="Policy Recommendations" 
              className="dashboard-card"
              extra={
                <Button 
                  type="link" 
                  onClick={() => navigate('/policies')}
                >
                  View All
                </Button>
              }
            >
              <PolicyRecommendations />
            </Card>
          </Col>

          {/* Emissions Chart */}
          <Col xs={24} lg={12}>
            <Card 
              title="CO₂ Emissions Trend" 
              className="dashboard-card"
            >
              <EmissionsChart />
            </Card>
          </Col>
        </Row>

        {/* Quick Actions */}
        <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
          <Col xs={24}>
            <Card title="Quick Actions" className="dashboard-card">
              <Space wrap>
                <Button 
                  type="primary" 
                  icon={<EnvironmentOutlined />}
                  onClick={() => navigate('/cities')}
                >
                  Add New City
                </Button>
                <Button 
                  icon={<PolicyOutlined />}
                  onClick={() => navigate('/policies')}
                >
                  Create Policy
                </Button>
                <Button 
                  icon={<ExperimentOutlined />}
                  onClick={() => navigate('/simulations')}
                >
                  Run Simulation
                </Button>
                <Button 
                  icon={<BarChartOutlined />}
                  onClick={() => navigate('/data-upload')}
                >
                  Upload Data
                </Button>
              </Space>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
};

export default Dashboard;
