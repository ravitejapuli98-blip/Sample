import React from 'react';
import { Layout, Typography, Space, Button, Dropdown, Avatar } from 'antd';
import { UserOutlined, SettingOutlined, LogoutOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';

const { Header } = Layout;
const { Title } = Typography;

const AppHeader: React.FC = () => {
  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profile',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      danger: true,
    },
  ];

  const handleUserMenuClick: MenuProps['onClick'] = ({ key }) => {
    switch (key) {
      case 'profile':
        console.log('Profile clicked');
        break;
      case 'settings':
        console.log('Settings clicked');
        break;
      case 'logout':
        console.log('Logout clicked');
        break;
    }
  };

  return (
    <Header className="app-header" style={{ 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'space-between',
      padding: '0 24px'
    }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <Title level={3} style={{ color: 'white', margin: 0, marginRight: 24 }}>
          🌱 AI Sustainable Cities Planner
        </Title>
      </div>
      
      <Space size="middle">
        <Button type="text" style={{ color: 'white' }}>
          Documentation
        </Button>
        <Button type="text" style={{ color: 'white' }}>
          Support
        </Button>
        
        <Dropdown
          menu={{ 
            items: userMenuItems,
            onClick: handleUserMenuClick 
          }}
          placement="bottomRight"
          arrow
        >
          <Button type="text" style={{ color: 'white', display: 'flex', alignItems: 'center' }}>
            <Avatar size="small" icon={<UserOutlined />} style={{ marginRight: 8 }} />
            Admin User
          </Button>
        </Dropdown>
      </Space>
    </Header>
  );
};

export default AppHeader;
