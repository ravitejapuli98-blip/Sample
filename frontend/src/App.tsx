import React from 'react';
import { Layout, Card, Row, Col, Statistic, Typography } from 'antd';
import { EnvironmentOutlined, CarOutlined, ThunderboltOutlined, CloudOutlined } from '@ant-design/icons';
import './App.css';

const { Header, Content } = Layout;
const { Title, Paragraph } = Typography;

const App: React.FC = () => {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#fff', padding: '0 24px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
        <div style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
          <EnvironmentOutlined style={{ fontSize: '24px', color: '#1890ff', marginRight: '12px' }} />
          <Title level={3} style={{ margin: 0, color: '#1890ff' }}>
            AI Sustainable Cities Planner
          </Title>
        </div>
      </Header>
      
      <Content style={{ padding: '24px', background: '#f5f5f5' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <Title level={2}>Welcome to AI Sustainable Cities Planner</Title>
          <Paragraph style={{ fontSize: '16px', marginBottom: '32px' }}>
            A comprehensive platform for analyzing urban sustainability, optimizing transportation policies, 
            and predicting environmental impacts through advanced AI simulations.
          </Paragraph>
          
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} lg={6}>
              <Card>
                <Statistic
                  title="Cities Analyzed"
                  value={3}
                  prefix={<EnvironmentOutlined />}
                  valueStyle={{ color: '#3f8600' }}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Card>
                <Statistic
                  title="Policies Evaluated"
                  value={5}
                  prefix={<CarOutlined />}
                  valueStyle={{ color: '#1890ff' }}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Card>
                <Statistic
                  title="Simulations Run"
                  value={12}
                  prefix={<ThunderboltOutlined />}
                  valueStyle={{ color: '#722ed1' }}
                />
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Card>
                <Statistic
                  title="CO₂ Reduction"
                  value={18}
                  suffix="%"
                  prefix={<CloudOutlined />}
                  valueStyle={{ color: '#cf1322' }}
                />
              </Card>
            </Col>
          </Row>
          
          <Row gutter={[16, 16]} style={{ marginTop: '24px' }}>
            <Col xs={24} lg={12}>
              <Card title="🌱 Sustainability Features" style={{ height: '300px' }}>
                <ul style={{ fontSize: '16px', lineHeight: '2' }}>
                  <li>Multi-agent urban simulation</li>
                  <li>Policy impact prediction</li>
                  <li>Air quality monitoring</li>
                  <li>Transportation optimization</li>
                  <li>Energy efficiency analysis</li>
                  <li>Equity impact assessment</li>
                </ul>
              </Card>
            </Col>
            <Col xs={24} lg={12}>
              <Card title="🔗 API Endpoints" style={{ height: '300px' }}>
                <div style={{ fontSize: '14px', lineHeight: '2' }}>
                  <div><strong>Health Check:</strong> <code>/health</code></div>
                  <div><strong>Cities Data:</strong> <code>/api/v1/cities</code></div>
                  <div><strong>Policies:</strong> <code>/api/v1/policies</code></div>
                  <div><strong>Simulations:</strong> <code>/api/v1/simulations</code></div>
                  <div><strong>Predictions:</strong> <code>/api/v1/predictions</code></div>
                </div>
                <div style={{ marginTop: '16px', padding: '12px', background: '#f6ffed', border: '1px solid #b7eb8f', borderRadius: '6px' }}>
                  <strong>Backend API:</strong><br />
                  <a href="http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com" target="_blank" rel="noopener noreferrer">
                    http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com
                  </a>
                </div>
              </Card>
            </Col>
          </Row>
        </div>
      </Content>
    </Layout>
  );
};

export default App;