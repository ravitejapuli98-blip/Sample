import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Card, Typography, Space, Tag } from 'antd';
import { EnvironmentOutlined } from '@ant-design/icons';
import { useQuery } from 'react-query';
import { endpoints } from '../../services/api';

const { Text } = Typography;

const CityMap: React.FC = () => {
  const { data: cities, isLoading } = useQuery(
    'cities-map',
    () => endpoints.cities.list().then(res => res.data)
  );

  if (isLoading) {
    return (
      <div style={{ height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Text>Loading map...</Text>
      </div>
    );
  }

  return (
    <div className="map-container">
      <MapContainer
        center={[39.8283, -98.5795]} // Center of US
        zoom={4}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {cities?.map((city: any) => (
          <Marker
            key={city.id}
            position={[city.latitude || 0, city.longitude || 0]}
          >
            <Popup>
              <div>
                <Space direction="vertical" size="small">
                  <div>
                    <EnvironmentOutlined style={{ marginRight: 8 }} />
                    <strong>{city.name}</strong>
                  </div>
                  <Text type="secondary">{city.state}, {city.country}</Text>
                  <div>
                    <Text>Population: {city.population?.toLocaleString() || 'N/A'}</Text>
                  </div>
                  <div>
                    <Text>Area: {city.area_km2 ? `${city.area_km2.toFixed(1)} km²` : 'N/A'}</Text>
                  </div>
                  <div>
                    <Tag color="blue">Active</Tag>
                  </div>
                </Space>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default CityMap;
