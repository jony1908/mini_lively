import apiClient from './client';

// Profile API service
export const profileAPI = {
  // Get current user's profile
  async getCurrentProfile() {
    try {
      const response = await apiClient.get('/profile/me');
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        // No profile exists yet, return null
        return null;
      }
      throw error;
    }
  },

  // Create new profile
  async createProfile(profileData) {
    try {
      const response = await apiClient.post('/profile', profileData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Update existing profile
  async updateProfile(profileData) {
    try {
      const response = await apiClient.put('/profile/me', profileData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Delete profile
  async deleteProfile() {
    try {
      await apiClient.delete('/profile/me');
      return true;
    } catch (error) {
      throw error;
    }
  },

  // Upload profile picture (placeholder for future implementation)
  async uploadProfilePicture(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      // Note: This endpoint doesn't exist yet in backend
      // This is a placeholder for future file upload implementation
      const response = await apiClient.post('/profile/upload-picture', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default profileAPI;