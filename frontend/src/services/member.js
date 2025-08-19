/**
 * Member management service.
 * Handles communication with member API endpoints.
 */

import client from './client';

const memberAPI = {
  /**
   * Get all members for the current user
   * @param {boolean} includeInactive - Include inactive members
   * @returns {Promise<Array>} List of members
   */
  async getMembers(includeInactive = false) {
    const response = await client.get('/members', {
      params: { include_inactive: includeInactive }
    });
    return response.data;
  },

  /**
   * Get a specific member by ID
   * @param {number} memberId - Member ID
   * @returns {Promise<Object>} Member data
   */
  async getMember(memberId) {
    const response = await client.get(`/members/${memberId}`);
    return response.data;
  },

  /**
   * Create a new member profile
   * @param {Object} memberData - Member information
   * @returns {Promise<Object>} Created member data
   */
  async createMember(memberData) {
    const response = await client.post('/members', memberData);
    return response.data;
  },

  /**
   * Update a member's information
   * @param {number} memberId - Member ID
   * @param {Object} updateData - Updated member information
   * @returns {Promise<Object>} Updated member data
   */
  async updateMember(memberId, updateData) {
    const response = await client.put(`/members/${memberId}`, updateData);
    return response.data;
  },

  /**
   * Delete a member (soft delete)
   * @param {number} memberId - Member ID
   * @returns {Promise<void>}
   */
  async deleteMember(memberId) {
    await client.delete(`/members/${memberId}`);
  },

  /**
   * Get predefined options for interests and skills
   * @returns {Promise<Object>} Options with interests and skills arrays
   */
  async getMemberOptions() {
    try {
      const response = await client.get('/members/options');
      return response.data;
    } catch (error) {
      // Fallback to default options if endpoint is not available
      console.warn('Member options endpoint not available, using default options:', error.message);
      return {
        interests: [
          "Sports", "Soccer", "Basketball", "Baseball", "Tennis", "Swimming",
          "Music", "Piano", "Guitar", "Violin", "Singing", "Dancing",
          "Arts & Crafts", "Drawing", "Painting", "Sculpture", "Photography",
          "Science", "Robotics", "Chemistry", "Biology", "Astronomy",
          "Technology", "Coding", "Video Games", "Computer Graphics",
          "Reading", "Writing", "Poetry", "Storytelling",
          "Outdoor Activities", "Hiking", "Camping", "Fishing", "Gardening",
          "Board Games", "Puzzles", "Chess", "Card Games",
          "Drama", "Theater", "Acting", "Public Speaking",
          "Cooking", "Baking", "Martial Arts", "Yoga"
        ].sort(),
        skills: [
          "Swimming", "Cycling", "Running", "Jumping",
          "Piano Playing", "Guitar Playing", "Singing", "Dancing",
          "Drawing", "Painting", "Writing", "Reading",
          "Math", "Problem Solving", "Critical Thinking",
          "Communication", "Public Speaking", "Leadership",
          "Teamwork", "Organization", "Time Management",
          "Computer Skills", "Coding", "Typing",
          "Foreign Languages", "Spanish", "French", "Mandarin",
          "Soccer Skills", "Basketball Skills", "Baseball Skills",
          "Cooking", "Baking", "Gardening",
          "First Aid", "Safety Awareness",
          "Musical Instruments", "Art Techniques",
          "Creative Writing", "Research Skills"
        ].sort()
      };
    }
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
   * Validate member data before submission
   * @param {Object} memberData - Member information to validate
   * @returns {Object} Validation result with isValid and errors
   */
  validateMemberData(memberData) {
    const errors = [];

    // Required fields
    if (!memberData.first_name || memberData.first_name.trim().length === 0) {
      errors.push('First name is required');
    }

    if (!memberData.last_name || memberData.last_name.trim().length === 0) {
      errors.push('Last name is required');
    }

    if (!memberData.date_of_birth) {
      errors.push('Date of birth is required');
    } else {
      // Check if date is not in the future
      const birthDate = new Date(memberData.date_of_birth);
      const today = new Date();
      if (birthDate > today) {
        errors.push('Date of birth cannot be in the future');
      }

      // Allow any age for family members (removed age restriction)
      const age = this.calculateAge(memberData.date_of_birth);
      if (age > 150) { // Reasonable upper limit
        errors.push('Please check the date of birth');
      }
    }

    // Validate interests array
    if (memberData.interests && Array.isArray(memberData.interests)) {
      if (memberData.interests.length > 20) {
        errors.push('Maximum 20 interests allowed');
      }
    }

    // Validate skills array
    if (memberData.skills && Array.isArray(memberData.skills)) {
      if (memberData.skills.length > 15) {
        errors.push('Maximum 15 skills allowed');
      }
    }

    // Name length validation
    if (memberData.first_name && memberData.first_name.length > 50) {
      errors.push('First name must be 50 characters or less');
    }

    if (memberData.last_name && memberData.last_name.length > 50) {
      errors.push('Last name must be 50 characters or less');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  },

  /**
   * Generate age options for dropdown (0-120 years)
   * @returns {Array} Array of age options
   */
  getAgeOptions() {
    const options = [];
    for (let i = 0; i <= 120; i++) {
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
   * Get relationship options with user
   * @returns {Array} Array of relationship options
   */
  getRelationshipOptions() {
    return [
      { value: 'child', label: 'Child' },
      { value: 'spouse', label: 'Spouse' },
      { value: 'parent', label: 'Parent' },
      { value: 'sibling', label: 'Sibling' },
      { value: 'grandparent', label: 'Grandparent' },
      { value: 'grandchild', label: 'Grandchild' },
      { value: 'step_parent', label: 'Step Parent' },
      { value: 'step_child', label: 'Step Child' },
      { value: 'aunt_uncle', label: 'Aunt/Uncle' },
      { value: 'niece_nephew', label: 'Niece/Nephew' },
      { value: 'guardian', label: 'Guardian' },
      { value: 'ward', label: 'Ward' }
    ];
  },

  /**
   * Format member's full name
   * @param {Object} member - Member object
   * @returns {string} Full name
   */
  getMemberFullName(member) {
    return `${member.first_name} ${member.last_name}`.trim();
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
   * Upload avatar for a specific member
   * @param {number} memberId - Member ID
   * @param {File} file - Image file to upload (will be compressed if needed)
   * @returns {Promise<Object>} Upload result with avatar URL
   */
  async uploadMemberAvatar(memberId, file) {
    // Process file (compress if needed)
    const { file: processedFile } = await this.processFileForUpload(file);
    
    const formData = new FormData();
    formData.append('file', processedFile);

    const response = await client.post(`/members/${memberId}/avatar`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data;
  },

  /**
   * Remove avatar for a specific member
   * @param {number} memberId - Member ID
   * @returns {Promise<Object>} Deletion result
   */
  async removeMemberAvatar(memberId) {
    const response = await client.delete(`/members/${memberId}/avatar`);
    return response.data;
  },

  /**
   * Get avatar information for a specific member
   * @param {number} memberId - Member ID
   * @returns {Promise<Object>} Avatar information
   */
  async getMemberAvatarInfo(memberId) {
    const response = await client.get(`/members/${memberId}/avatar`);
    return response.data;
  },

  /**
   * Get default avatar URL for members
   * @returns {string} Default avatar URL (data URL for a simple SVG)
   */
  getDefaultMemberAvatar() {
    // Return a simple SVG avatar as a data URL to avoid file dependency issues
    const svgAvatar = `<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96" fill="none">
      <circle cx="48" cy="48" r="48" fill="#e9e2ce"/>
      <circle cx="48" cy="32" r="12" fill="#9e8747"/>
      <path d="M20 80c0-15.464 12.536-28 28-28s28 12.536 28 28" fill="#9e8747"/>
    </svg>`;
    return `data:image/svg+xml;base64,${btoa(svgAvatar)}`;
  },

  /**
   * Get display avatar URL (returns default if none exists)
   * @param {Object} member - Member object
   * @returns {string} Avatar URL to display
   */
  getDisplayAvatarUrl(member) {
    return member?.avatar_url || this.getDefaultMemberAvatar();
  },

  /**
   * Get age category for display purposes
   * @param {number} age - Age in years
   * @returns {string} Age category
   */
  getAgeCategory(age) {
    if (age < 2) return 'Baby';
    if (age < 5) return 'Toddler';
    if (age < 13) return 'Child';
    if (age < 20) return 'Teen';
    if (age < 65) return 'Adult';
    return 'Senior';
  },

  /**
   * Compress image file to meet size requirements
   * @param {File} file - Image file to compress
   * @param {number} maxSize - Maximum file size in bytes
   * @param {number} quality - Initial quality (0.1 to 1.0)
   * @returns {Promise<File>} Compressed file
   */
  async compressImage(file, maxSize = 2 * 1024 * 1024, quality = 0.8) {
    return new Promise((resolve) => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();
      
      img.onload = () => {
        // Calculate dimensions while maintaining aspect ratio
        const maxDimension = 1024; // Max width/height before compression
        let { width, height } = img;
        
        if (width > maxDimension || height > maxDimension) {
          if (width > height) {
            height = (height * maxDimension) / width;
            width = maxDimension;
          } else {
            width = (width * maxDimension) / height;
            height = maxDimension;
          }
        }
        
        canvas.width = width;
        canvas.height = height;
        
        // Draw and compress
        ctx.drawImage(img, 0, 0, width, height);
        
        const tryCompress = (currentQuality) => {
          canvas.toBlob((blob) => {
            if (blob.size <= maxSize || currentQuality <= 0.1) {
              // Create new file with compressed data
              const compressedFile = new File([blob], file.name, {
                type: 'image/jpeg',
                lastModified: Date.now()
              });
              resolve(compressedFile);
            } else {
              // Try lower quality
              tryCompress(currentQuality - 0.1);
            }
          }, 'image/jpeg', currentQuality);
        };
        
        tryCompress(quality);
      };
      
      img.src = URL.createObjectURL(file);
    });
  },

  /**
   * Validate image file for avatar upload
   * @param {File} file - Image file to validate
   * @returns {Object} Validation result with isValid and error
   */
  validateAvatarFile(file) {
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

    return { isValid: true };
  },

  /**
   * Process file for upload - compress if necessary
   * @param {File} file - Original file
   * @returns {Promise<{file: File, wasCompressed: boolean}>}
   */
  async processFileForUpload(file) {
    const maxSize = 2 * 1024 * 1024; // 2MB
    
    if (file.size <= maxSize) {
      return { file, wasCompressed: false };
    }
    
    const compressedFile = await this.compressImage(file, maxSize);
    return { file: compressedFile, wasCompressed: true };
  },

  /**
   * Create a preview URL for selected image
   * @param {File} file - Image file
   * @returns {string} Preview URL
   */
  createPreviewUrl(file) {
    return URL.createObjectURL(file);
  },

  /**
   * Cleanup preview URL to prevent memory leaks
   * @param {string} url - Preview URL to cleanup
   */
  cleanupPreviewUrl(url) {
    if (url && url.startsWith('blob:')) {
      URL.revokeObjectURL(url);
    }
  }
};

export default memberAPI;