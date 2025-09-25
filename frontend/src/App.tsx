import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import { Helmet } from 'react-helmet-async';
import AppHeader from './components/Layout/AppHeader';
import AppSidebar from './components/Layout/AppSidebar';
import Dashboard from './pages/Dashboard';
import Cities from './pages/Cities';
import CityDetail from './pages/CityDetail';
import Policies from './pages/Policies';
import PolicyDetail from './pages/PolicyDetail';
import Simulations from './pages/Simulations';
import SimulationDetail from './pages/SimulationDetail';
import Predictions from './pages/Predictions';
import DataUpload from './pages/DataUpload';
import './App.css';

const { Content } = Layout;

const App: React.FC = () => {
  return (
    <>
      <Helmet>
        <title>AI Sustainable Cities Planner</title>
        <meta name="description" content="Multi-agent simulation and planning tool for sustainable urban development" />
      </Helmet>
      
      <Layout style={{ minHeight: '100vh' }}>
        <AppSidebar />
        <Layout>
          <AppHeader />
          <Content className="app-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/cities" element={<Cities />} />
              <Route path="/cities/:id" element={<CityDetail />} />
              <Route path="/policies" element={<Policies />} />
              <Route path="/policies/:id" element={<PolicyDetail />} />
              <Route path="/simulations" element={<Simulations />} />
              <Route path="/simulations/:id" element={<SimulationDetail />} />
              <Route path="/predictions" element={<Predictions />} />
              <Route path="/data-upload" element={<DataUpload />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </>
  );
};

export default App;
