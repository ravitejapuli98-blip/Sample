import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://prod-sus-cities-alb-73707419.us-east-1.elb.amazonaws.com';

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const endpoints = {
  // Cities
  cities: {
    list: () => api.get('/cities'),
    get: (id: number) => api.get(`/cities/${id}`),
    create: (data: any) => api.post('/cities', data),
    update: (id: number, data: any) => api.put(`/cities/${id}`, data),
    delete: (id: number) => api.delete(`/cities/${id}`),
    dashboard: (id: number) => api.get(`/cities/${id}/dashboard`),
    mobility: (id: number, params?: any) => api.get(`/cities/${id}/mobility`, { params }),
    airQuality: (id: number, params?: any) => api.get(`/cities/${id}/air-quality`, { params }),
    energy: (id: number, params?: any) => api.get(`/cities/${id}/energy`, { params }),
    neighborhoods: (id: number) => api.get(`/cities/${id}/neighborhoods`),
  },
  
  // Policies
  policies: {
    list: (params?: any) => api.get('/policies', { params }),
    get: (id: number) => api.get(`/policies/${id}`),
    create: (data: any) => api.post('/policies', data),
    update: (id: number, data: any) => api.put(`/policies/${id}`, data),
    delete: (id: number) => api.delete(`/policies/${id}`),
    components: (id: number) => api.get(`/policies/${id}/components`),
    recommendations: (cityId: number, constraints: any) => 
      api.post(`/policies/recommendations/${cityId}`, constraints),
    optimize: (cityId: number, constraints: any) => 
      api.post(`/policies/optimize/${cityId}`, constraints),
  },
  
  // Simulations
  simulations: {
    list: (params?: any) => api.get('/simulations', { params }),
    get: (id: number) => api.get(`/simulations/${id}`),
    create: (data: any) => api.post('/simulations', data),
    run: (id: number) => api.post(`/simulations/${id}/run`),
    results: (id: number) => api.get(`/simulations/${id}/results`),
    runs: (id: number) => api.get(`/simulations/${id}/runs`),
  },
  
  // Predictions
  predictions: {
    list: (params?: any) => api.get('/predictions', { params }),
    get: (id: number) => api.get(`/predictions/${id}`),
    create: (data: any) => api.post('/predictions', data),
    predict: (modelId: number, inputData: any) => 
      api.post(`/predictions/predict/${modelId}`, inputData),
    models: {
      list: (params?: any) => api.get('/predictions/models', { params }),
      get: (id: number) => api.get(`/predictions/models/${id}`),
      create: (data: any) => api.post('/predictions/models', data),
      evaluations: (id: number) => api.get(`/predictions/models/${id}/evaluations`),
    },
  },
  
  // Data
  data: {
    uploadMobility: (cityId: number, file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      return api.post(`/data/upload/mobility/${cityId}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    },
    uploadAirQuality: (cityId: number, file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      return api.post(`/data/upload/air-quality/${cityId}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    },
    uploadEnergy: (cityId: number, file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      return api.post(`/data/upload/energy/${cityId}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    },
    export: (cityId: number, dataType: string, params?: any) => 
      api.get(`/data/export/${cityId}`, { params: { data_type: dataType, ...params } }),
  },
};

export default api;
