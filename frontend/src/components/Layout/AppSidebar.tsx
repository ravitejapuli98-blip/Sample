import React, { useState } from 'react';
import { Layout, Menu } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  EnvironmentOutlined,
  PolicyOutlined,
  ExperimentOutlined,
  BarChartOutlined,
  UploadOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

const { Sider } = Layout;

type MenuItem = Required<MenuProps>['items'][number];

const AppSidebar: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems: MenuItem[] = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/cities',
      icon: <EnvironmentOutlined />,
      label: 'Cities',
    },
    {
      key: '/policies',
      icon: <PolicyOutlined />,
      label: 'Policies',
    },
    {
      key: '/simulations',
      icon: <ExperimentOutlined />,
      label: 'Simulations',
    },
    {
      key: '/predictions',
      icon: <BarChartOutlined />,
      label: 'Predictions',
    },
    {
      key: '/data-upload',
      icon: <UploadOutlined />,
      label: 'Data Upload',
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: 'Settings',
    },
  ];

  const handleMenuClick: MenuProps['onClick'] = ({ key }) => {
    navigate(key);
  };

  return (
    <Sider
      collapsible
      collapsed={collapsed}
      onCollapse={setCollapsed}
      width={250}
      className="app-sidebar"
      style={{
        background: 'white',
        boxShadow: '2px 0 8px rgba(0, 0, 0, 0.1)',
      }}
    >
      <div style={{ 
        height: 64, 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        borderBottom: '1px solid #f0f0f0'
      }}>
        {!collapsed && (
          <div style={{ 
            fontSize: 16, 
            fontWeight: 'bold', 
            color: '#1890ff',
            textAlign: 'center'
          }}>
            Sustainable Cities
          </div>
        )}
        {collapsed && (
          <div style={{ 
            fontSize: 20, 
            color: '#1890ff'
          }}>
            🌱
          </div>
        )}
      </div>
      
      <Menu
        mode="inline"
        selectedKeys={[location.pathname]}
        items={menuItems}
        onClick={handleMenuClick}
        style={{
          borderRight: 0,
          marginTop: 16,
        }}
      />
    </Sider>
  );
};

export default AppSidebar;
