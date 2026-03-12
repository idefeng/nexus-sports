import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const activityService = {
  getActivities: async (skip = 0, limit = 200) => {
    const response = await api.get('/activities', { params: { skip, limit } });
    // Returns { total, skip, limit, items }
    return response.data;
  },
  
  getActivity: async (id: number) => {
    const response = await api.get(`/activities/${id}`);
    return response.data;
  },

  deleteActivity: async (id: number) => {
    const response = await api.delete(`/activities/${id}`);
    return response.data;
  },

  updateActivity: async (id: number, data: Record<string, any>) => {
    const response = await api.patch(`/activities/${id}`, data);
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

  getLatestAIReport: async () => {
    const response = await api.get('/agent/latest_activity');
    return response.data;
  },

  getMonthlyAIReport: async (targetMonth?: string) => {
    const params = targetMonth ? { target_month: targetMonth } : {};
    const response = await api.get('/agent/monthly_report', { params });
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
  },

  getOriginalFileUrl: (activityId: number) => `/api/v1/export/original/${activityId}`,
  getGpxExportUrl: (activityId: number) => `/api/v1/export/gpx/${activityId}`,
};

export default api;
