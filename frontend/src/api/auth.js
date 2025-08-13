import apiClient from './client';

export const authAPI = {
  // Register new user
  register: async (userData) => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },

  // Login with email/password
  login: async (credentials) => {
    const response = await apiClient.post('/auth/login', credentials);
    return response.data;
  },

  // Refresh access token
  refreshToken: async (refreshToken) => {
    const response = await apiClient.post('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },

  // Get current user profile
  getCurrentUser: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  // Google OAuth
  googleAuth: () => {
    window.location.href = `${apiClient.defaults.baseURL}/auth/google`;
  },

  // Apple OAuth
  appleAuth: () => {
    window.location.href = `${apiClient.defaults.baseURL}/auth/apple`;
  },
};