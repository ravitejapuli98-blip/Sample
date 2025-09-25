import React, { useState } from 'react';
import { 
  Layout, Card, Row, Col, Statistic, Typography, Button, 
  Select, Progress, Tag, Space, Divider, Alert, Badge,
  List, Avatar, Modal, Input, Form
} from 'antd';
import { 
  EnvironmentOutlined, CarOutlined, ThunderboltOutlined, CloudOutlined,
  SearchOutlined, BulbOutlined, BarChartOutlined,
  CheckCircleOutlined, ClockCircleOutlined,
  PlusOutlined, EyeOutlined, DownloadOutlined, ShareAltOutlined
} from '@ant-design/icons';
import './App.css';

const { Header, Content, Sider } = Layout;
const { Title, Paragraph, Text } = Typography;
const { Option } = Select;

const App = () => {
  const [selectedCity, setSelectedCity] = useState('Detroit');
  const [selectedPolicy, setSelectedPolicy] = useState('');
  const [showPolicyModal, setShowPolicyModal] = useState(false);

  const cities = [
    // Major Michigan Cities
    { name: 'Detroit', sustainability: 65, population: '639K', emissions: '8.2M tons', state: 'MI' },
    { name: 'Grand Rapids', sustainability: 78, population: '198K', emissions: '2.1M tons', state: 'MI' },
    { name: 'Warren', sustainability: 72, population: '139K', emissions: '1.8M tons', state: 'MI' },
    { name: 'Sterling Heights', sustainability: 75, population: '134K', emissions: '1.6M tons', state: 'MI' },
    { name: 'Lansing', sustainability: 80, population: '118K', emissions: '1.4M tons', state: 'MI' },
    { name: 'Ann Arbor', sustainability: 88, population: '123K', emissions: '1.2M tons', state: 'MI' },
    { name: 'Flint', sustainability: 58, population: '95K', emissions: '1.8M tons', state: 'MI' },
    { name: 'Dearborn', sustainability: 70, population: '109K', emissions: '1.9M tons', state: 'MI' },
    { name: 'Livonia', sustainability: 73, population: '95K', emissions: '1.3M tons', state: 'MI' },
    { name: 'Westland', sustainability: 68, population: '85K', emissions: '1.1M tons', state: 'MI' },
    { name: 'Troy', sustainability: 82, population: '87K', emissions: '1.0M tons', state: 'MI' },
    { name: 'Farmington Hills', sustainability: 85, population: '81K', emissions: '0.9M tons', state: 'MI' },
    { name: 'Kalamazoo', sustainability: 77, population: '76K', emissions: '1.1M tons', state: 'MI' },
    { name: 'Wyoming', sustainability: 71, population: '76K', emissions: '1.2M tons', state: 'MI' },
    { name: 'Southfield', sustainability: 74, population: '76K', emissions: '1.0M tons', state: 'MI' },
    { name: 'Rochester Hills', sustainability: 86, population: '75K', emissions: '0.8M tons', state: 'MI' },
    { name: 'Taylor', sustainability: 66, population: '63K', emissions: '1.1M tons', state: 'MI' },
    { name: 'Pontiac', sustainability: 62, population: '61K', emissions: '1.3M tons', state: 'MI' },
    { name: 'St. Clair Shores', sustainability: 79, population: '59K', emissions: '0.9M tons', state: 'MI' },
    { name: 'Royal Oak', sustainability: 84, population: '58K', emissions: '0.8M tons', state: 'MI' },
    { name: 'Novi', sustainability: 87, population: '66K', emissions: '0.7M tons', state: 'MI' },
    { name: 'Dearborn Heights', sustainability: 69, population: '57K', emissions: '1.0M tons', state: 'MI' },
    { name: 'Battle Creek', sustainability: 70, population: '52K', emissions: '0.9M tons', state: 'MI' },
    { name: 'Saginaw', sustainability: 64, population: '48K', emissions: '1.2M tons', state: 'MI' },
    { name: 'Kentwood', sustainability: 76, population: '51K', emissions: '0.8M tons', state: 'MI' },
    { name: 'East Lansing', sustainability: 89, population: '48K', emissions: '0.6M tons', state: 'MI' },
    { name: 'Roseville', sustainability: 72, population: '47K', emissions: '0.9M tons', state: 'MI' },
    { name: 'Portage', sustainability: 81, population: '48K', emissions: '0.7M tons', state: 'MI' },
    { name: 'Midland', sustainability: 83, population: '42K', emissions: '0.8M tons', state: 'MI' },
    { name: 'Lincoln Park', sustainability: 67, population: '38K', emissions: '0.8M tons', state: 'MI' }
  ];

  const policies = [
    { id: 1, name: 'Bus Lane Expansion', impact: 'High', cost: '$50M', time: '18 months' },
    { id: 2, name: 'EV Charging Network', impact: 'Medium', cost: '$25M', time: '12 months' },
    { id: 3, name: 'Green Building Standards', impact: 'High', cost: '$15M', time: '24 months' },
    { id: 4, name: 'Bike Network Expansion', impact: 'Medium', cost: '$30M', time: '15 months' },
    { id: 5, name: 'Renewable Energy Program', impact: 'High', cost: '$40M', time: '20 months' }
  ];

  const getImpactColor = (impact) => {
    switch (impact) {
      case 'High': return '#52c41a';
      case 'Medium': return '#faad14';
      case 'Low': return '#ff4d4f';
      default: return '#d9d9d9';
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
        padding: '0 24px', 
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)' 
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '100%' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <EnvironmentOutlined style={{ fontSize: '28px', color: '#fff', marginRight: '16px' }} />
            <Title level={3} style={{ margin: 0, color: '#fff' }}>
              AI Sustainable Cities Planner - Michigan Edition
            </Title>
          </div>
          <Space>
            <Button type="primary" ghost icon={<SearchOutlined />}>
              Explore Cities
            </Button>
            <Button type="primary" ghost icon={<BulbOutlined />}>
              Get Recommendations
            </Button>
          </Space>
        </div>
      </Header>

      <Layout>
        <Sider width={300} style={{ background: '#fff', padding: '24px' }}>
          <Title level={4}>Quick Actions</Title>
          <Space direction="vertical" style={{ width: '100%' }} size="middle">
            <Button 
              type="primary" 
              block 
              icon={<PlusOutlined />}
              onClick={() => setShowPolicyModal(true)}
            >
              Analyze New Policy
            </Button>
            <Button block icon={<BarChartOutlined />}>
              View City Dashboard
            </Button>
            <Button block icon={<DownloadOutlined />}>
              Export Report
            </Button>
            <Button block icon={<ShareAltOutlined />}>
              Share Insights
            </Button>
          </Space>

          <Divider />

          <Title level={5}>Select City</Title>
          <Select
            value={selectedCity}
            onChange={setSelectedCity}
            style={{ width: '100%' }}
            size="large"
          >
            {cities.map(city => (
              <Option key={city.name} value={city.name}>
                <Space>
                  <EnvironmentOutlined />
                  {city.name}, {city.state}
                </Space>
              </Option>
            ))}
          </Select>

          <Divider />

          <Title level={5}>City Overview</Title>
          {cities.find(c => c.name === selectedCity) && (
            <Card size="small">
              <Statistic
                title="Sustainability Score"
                value={cities.find(c => c.name === selectedCity)?.sustainability}
                suffix="/100"
                valueStyle={{ color: '#52c41a' }}
              />
              <Progress 
                percent={cities.find(c => c.name === selectedCity)?.sustainability} 
                strokeColor="#52c41a"
                size="small"
                style={{ marginTop: '8px' }}
              />
              <div style={{ marginTop: '12px', fontSize: '12px', color: '#666' }}>
                <div>Population: {cities.find(c => c.name === selectedCity)?.population}</div>
                <div>Annual Emissions: {cities.find(c => c.name === selectedCity)?.emissions}</div>
              </div>
            </Card>
          )}
        </Sider>

        <Content style={{ padding: '24px', background: '#f8f9fa' }}>
          <div style={{ maxWidth: '100%' }}>
            <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
              <Col span={24}>
                <Alert
                  message="Welcome to AI Sustainable Cities Planner - Michigan Edition"
                  description="Get AI-powered insights and recommendations to make Michigan cities more sustainable, efficient, and equitable. Analyze 30+ Michigan cities with real-time data."
                  type="info"
                  showIcon
                  style={{ marginBottom: '24px' }}
                />
              </Col>
            </Row>

            <Row gutter={[16, 16]}>
              <Col xs={24} sm={12} lg={6}>
                <Card hoverable>
                  <Statistic
                    title="Michigan Cities"
                    value={30}
                    prefix={<EnvironmentOutlined style={{ color: '#52c41a' }} />}
                    valueStyle={{ color: '#52c41a' }}
                  />
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    All major MI cities
                  </Text>
                </Card>
              </Col>
              <Col xs={24} sm={12} lg={6}>
                <Card hoverable>
                  <Statistic
                    title="Policies Evaluated"
                    value={5}
                    prefix={<CarOutlined style={{ color: '#1890ff' }} />}
                    valueStyle={{ color: '#1890ff' }}
                  />
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    AI-powered impact analysis
                  </Text>
                </Card>
              </Col>
              <Col xs={24} sm={12} lg={6}>
                <Card hoverable>
                  <Statistic
                    title="Simulations Run"
                    value={12}
                    prefix={<ThunderboltOutlined style={{ color: '#722ed1' }} />}
                    valueStyle={{ color: '#722ed1' }}
                  />
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    Multi-agent modeling
                  </Text>
                </Card>
              </Col>
              <Col xs={24} sm={12} lg={6}>
                <Card hoverable>
                  <Statistic
                    title="CO₂ Reduction"
                    value={18}
                    suffix="%"
                    prefix={<CloudOutlined style={{ color: '#fa541c' }} />}
                    valueStyle={{ color: '#fa541c' }}
                  />
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    Average policy impact
                  </Text>
                </Card>
              </Col>
            </Row>

            <Row gutter={[16, 16]} style={{ marginTop: '24px' }}>
              <Col xs={24} lg={16}>
                <Card title="🚀 Recommended Policies" extra={<Button type="link">View All</Button>}>
                  <List
                    dataSource={policies}
                    renderItem={policy => (
                      <List.Item
                        actions={[
                          <Button type="link" icon={<EyeOutlined />}>Analyze</Button>,
                          <Button type="link" icon={<BulbOutlined />}>Recommend</Button>
                        ]}
                      >
                        <List.Item.Meta
                          avatar={
                            <Avatar 
                              style={{ 
                                backgroundColor: getImpactColor(policy.impact),
                                color: '#fff'
                              }}
                            >
                              {policy.impact[0]}
                            </Avatar>
                          }
                          title={
                            <Space>
                              {policy.name}
                              <Tag color={getImpactColor(policy.impact)}>
                                {policy.impact} Impact
                              </Tag>
                            </Space>
                          }
                          description={
                            <Space split={<Divider type="vertical" />}>
                              <Text type="secondary">
                                <ClockCircleOutlined /> {policy.time}
                              </Text>
                              <Text type="secondary">
                                <span style={{ color: '#52c41a' }}>{policy.cost}</span>
                              </Text>
                            </Space>
                          }
                        />
                      </List.Item>
                    )}
                  />
                </Card>
              </Col>
              <Col xs={24} lg={8}>
                <Card title="📊 Quick Insights" style={{ height: '400px' }}>
                  <Space direction="vertical" style={{ width: '100%' }} size="middle">
                    <div>
                      <Text strong>Air Quality Status</Text>
                      <div style={{ marginTop: '8px' }}>
                        <Badge status="success" text="Good (AQI: 45)" />
                      </div>
                    </div>
                    <div>
                      <Text strong>Traffic Congestion</Text>
                      <div style={{ marginTop: '8px' }}>
                        <Progress percent={35} size="small" strokeColor="#faad14" />
                        <Text type="secondary" style={{ fontSize: '12px' }}>Moderate</Text>
                      </div>
                    </div>
                    <div>
                      <Text strong>Renewable Energy</Text>
                      <div style={{ marginTop: '8px' }}>
                        <Progress percent={28} size="small" strokeColor="#52c41a" />
                        <Text type="secondary" style={{ fontSize: '12px' }}>28% of total</Text>
                      </div>
                    </div>
                    <div>
                      <Text strong>Public Transit Usage</Text>
                      <div style={{ marginTop: '8px' }}>
                        <Progress percent={32} size="small" strokeColor="#1890ff" />
                        <Text type="secondary" style={{ fontSize: '12px' }}>32% of commuters</Text>
                      </div>
                    </div>
                  </Space>
                </Card>
              </Col>
            </Row>

            <Row gutter={[16, 16]} style={{ marginTop: '24px' }}>
              <Col span={24}>
                <Card title="🎯 How It Works" style={{ textAlign: 'center' }}>
                  <Row gutter={[24, 24]}>
                    <Col xs={24} sm={8}>
                      <div style={{ padding: '20px' }}>
                        <div style={{ 
                          width: '60px', 
                          height: '60px', 
                          borderRadius: '50%', 
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          margin: '0 auto 16px',
                          color: '#fff',
                          fontSize: '24px'
                        }}>
                          1
                        </div>
                        <Title level={4}>Select Your City</Title>
                        <Text type="secondary">
                          Choose from our database of Michigan cities with real-time data integration
                        </Text>
                      </div>
                    </Col>
                    <Col xs={24} sm={8}>
                      <div style={{ padding: '20px' }}>
                        <div style={{ 
                          width: '60px', 
                          height: '60px', 
                          borderRadius: '50%', 
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          margin: '0 auto 16px',
                          color: '#fff',
                          fontSize: '24px'
                        }}>
                          2
                        </div>
                        <Title level={4}>Get AI Recommendations</Title>
                        <Text type="secondary">
                          Our AI analyzes your city's data and suggests optimal policies
                        </Text>
                      </div>
                    </Col>
                    <Col xs={24} sm={8}>
                      <div style={{ padding: '20px' }}>
                        <div style={{ 
                          width: '60px', 
                          height: '60px', 
                          borderRadius: '50%', 
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          margin: '0 auto 16px',
                          color: '#fff',
                          fontSize: '24px'
                        }}>
                          3
                        </div>
                        <Title level={4}>Simulate & Implement</Title>
                        <Text type="secondary">
                          Run simulations to see policy impacts before implementation
                        </Text>
                      </div>
                    </Col>
                  </Row>
                </Card>
              </Col>
            </Row>
          </div>
        </Content>
      </Layout>

      <Modal
        title="Analyze New Policy"
        open={showPolicyModal}
        onCancel={() => setShowPolicyModal(false)}
        footer={[
          <Button key="cancel" onClick={() => setShowPolicyModal(false)}>
            Cancel
          </Button>,
          <Button key="analyze" type="primary" icon={<BulbOutlined />}>
            Analyze Policy
          </Button>
        ]}
      >
        <Form layout="vertical">
          <Form.Item label="Policy Type">
            <Select placeholder="Select policy type" size="large">
              <Option value="transportation">Transportation</Option>
              <Option value="energy">Energy</Option>
              <Option value="environmental">Environmental</Option>
              <Option value="housing">Housing</Option>
            </Select>
          </Form.Item>
          <Form.Item label="Policy Description">
            <Input.TextArea 
              rows={4} 
              placeholder="Describe the policy you want to analyze..."
            />
          </Form.Item>
          <Form.Item label="Budget Range">
            <Select placeholder="Select budget range" size="large">
              <Option value="low">Under $10M</Option>
              <Option value="medium">$10M - $50M</Option>
              <Option value="high">$50M - $100M</Option>
              <Option value="very-high">Over $100M</Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </Layout>
  );
};

export default App;
