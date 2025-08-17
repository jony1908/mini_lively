/**
 * Child management service.
 * Handles communication with child API endpoints.
 */

import client from './client';

const childAPI = {
  /**
   * Get all children for the current user
   * @param {boolean} includeInactive - Include inactive children
   * @returns {Promise<Array>} List of children
   */
  async getChildren(includeInactive = false) {
    const response = await client.get('/children', {
      params: { include_inactive: includeInactive }
    });
    return response.data;
  },

  /**
   * Get a specific child by ID
   * @param {number} childId - Child ID
   * @returns {Promise<Object>} Child data
   */
  async getChild(childId) {
    const response = await client.get(`/children/${childId}`);
    return response.data;
  },

  /**
   * Create a new child profile
   * @param {Object} childData - Child information
   * @returns {Promise<Object>} Created child data
   */
  async createChild(childData) {
    const response = await client.post('/children', childData);
    return response.data;
  },

  /**
   * Update a child's information
   * @param {number} childId - Child ID
   * @param {Object} updateData - Updated child information
   * @returns {Promise<Object>} Updated child data
   */
  async updateChild(childId, updateData) {
    const response = await client.put(`/children/${childId}`, updateData);
    return response.data;
  },

  /**
   * Delete a child (soft delete)
   * @param {number} childId - Child ID
   * @returns {Promise<void>}
   */
  async deleteChild(childId) {
    await client.delete(`/children/${childId}`);
  },

  /**
   * Get predefined options for interests and skills
   * @returns {Promise<Object>} Options with interests and skills arrays
   */
  async getChildOptions() {
    const response = await client.get('/children/options');
    return response.data;
  },

  /**
   * Calculate age from date of birth
   * @param {string} dateOfBirth - Date string (YYYY-MM-DD)
   * @returns {number} Age in years
   */
  calculateAge(dateOfBirth) {
    const today = new Date();
    const birthDate = new Date(dateOfBirth);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    
    return age;
  },

  /**
   * Format date for API (YYYY-MM-DD)
   * @param {Date} date - Date object
   * @returns {string} Formatted date string
   */
  formatDateForAPI(date) {
    return date.toISOString().split('T')[0];
  },

  /**
   * Validate child data before submission
   * @param {Object} childData - Child information to validate
   * @returns {Object} Validation result with isValid and errors
   */
  validateChildData(childData) {
    const errors = [];

    // Required fields
    if (!childData.first_name || childData.first_name.trim().length === 0) {
      errors.push('First name is required');
    }

    if (!childData.last_name || childData.last_name.trim().length === 0) {
      errors.push('Last name is required');
    }

    if (!childData.date_of_birth) {
      errors.push('Date of birth is required');
    } else {
      // Check if date is not in the future
      const birthDate = new Date(childData.date_of_birth);
      const today = new Date();
      if (birthDate > today) {
        errors.push('Date of birth cannot be in the future');
      }

      // Check minimum age (optional - could be 0 for babies)
      const age = this.calculateAge(childData.date_of_birth);
      if (age > 18) {
        errors.push('Child must be 18 years old or younger');
      }
    }

    // Validate interests array
    if (childData.interests && Array.isArray(childData.interests)) {
      if (childData.interests.length > 20) {
        errors.push('Maximum 20 interests allowed');
      }
    }

    // Validate skills array
    if (childData.skills && Array.isArray(childData.skills)) {
      if (childData.skills.length > 15) {
        errors.push('Maximum 15 skills allowed');
      }
    }

    // Name length validation
    if (childData.first_name && childData.first_name.length > 50) {
      errors.push('First name must be 50 characters or less');
    }

    if (childData.last_name && childData.last_name.length > 50) {
      errors.push('Last name must be 50 characters or less');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  },

  /**
   * Generate age options for dropdown (0-18 years)
   * @returns {Array} Array of age options
   */
  getAgeOptions() {
    const options = [];
    for (let i = 0; i <= 18; i++) {
      options.push({
        value: i,
        label: i === 0 ? 'Under 1 year' : i === 1 ? '1 year' : `${i} years`
      });
    }
    return options;
  },

  /**
   * Get gender options
   * @returns {Array} Array of gender options
   */
  getGenderOptions() {
    return [
      { value: 'Male', label: 'Male' },
      { value: 'Female', label: 'Female' }
    ];
  },

  /**
   * Format child's full name
   * @param {Object} child - Child object
   * @returns {string} Full name
   */
  getChildFullName(child) {
    return `${child.first_name} ${child.last_name}`.trim();
  },

  /**
   * Get display text for interests/skills
   * @param {Array} items - Array of interests or skills
   * @param {number} maxDisplay - Maximum items to display
   * @returns {string} Display text
   */
  getItemsDisplayText(items, maxDisplay = 3) {
    if (!items || items.length === 0) {
      return 'None specified';
    }

    if (items.length <= maxDisplay) {
      return items.join(', ');
    }

    const displayed = items.slice(0, maxDisplay).join(', ');
    const remaining = items.length - maxDisplay;
    return `${displayed} +${remaining} more`;
  },

  /**
   * Upload avatar for a specific child
   * @param {number} childId - Child ID
   * @param {File} file - Image file to upload
   * @returns {Promise<Object>} Upload result with avatar URL
   */
  async uploadChildAvatar(childId, file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await client.post(`/children/${childId}/avatar`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data;
  },

  /**
   * Remove avatar for a specific child
   * @param {number} childId - Child ID
   * @returns {Promise<Object>} Deletion result
   */
  async removeChildAvatar(childId) {
    const response = await client.delete(`/children/${childId}/avatar`);
    return response.data;
  },

  /**
   * Get avatar information for a specific child
   * @param {number} childId - Child ID
   * @returns {Promise<Object>} Avatar information
   */
  async getChildAvatarInfo(childId) {
    const response = await client.get(`/children/${childId}/avatar`);
    return response.data;
  },

  /**
   * Get default avatar URL for children
   * @returns {string} Default avatar URL
   */
  getDefaultChildAvatar() {
    return '/default-child-avatar.png'; // You can customize this
  },

  /**
   * Get display avatar URL (returns default if none exists)
   * @param {Object} child - Child object
   * @returns {string} Avatar URL to display
   */
  getDisplayAvatarUrl(child) {
    return child?.avatar_url || this.getDefaultChildAvatar();
  },

  /**
   * Validate image file for avatar upload
   * @param {File} file - Image file to validate
   * @returns {Object} Validation result with isValid and error
   */
  validateAvatarFile(file) {
    const maxSize = 2 * 1024 * 1024; // 2MB
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];

    if (!file) {
      return { isValid: false, error: 'No file selected' };
    }

    if (!allowedTypes.includes(file.type)) {
      return { 
        isValid: false, 
        error: 'Please select a JPEG, PNG, or WEBP image file' 
      };
    }

    if (file.size > maxSize) {
      return { 
        isValid: false, 
        error: 'Image must be smaller than 2MB' 
      };
    }

    return { isValid: true };
  }
};

export default childAPI;