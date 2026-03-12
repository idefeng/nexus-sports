import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const activityService = {
  getActivities: async () => {
    const response = await api.get('/activities');
    return response.data;
  },
  
  getActivity: async (id: number) => {
    const response = await api.get(`/activities/${id}`);
    return response.data;
  },
  
  getStatsSummary: async () => {
    const response = await api.get('/stats/summary');
    return response.data;
  },
  
  getStatsTrend: async () => {
    const response = await api.get('/stats/trend');
    return response.data;
  },
  
  getStatsDistribution: async () => {
    const response = await api.get('/stats/distribution');
    return response.data;
  },

  uploadFiles: async (files: File[]) => {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
};

export default api;
