/**
 * Avatar upload and management service.
 * Handles communication with avatar API endpoints.
 */

import client from './client';

const avatarAPI = {
  /**
   * Upload user avatar image with automatic processing and scaling
   * @param {File} file - Image file to upload
   * @returns {Promise<Object>} Upload result with avatar URL
   */
  async uploadAvatar(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await client.post('/avatar/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    return response.data;
  },

  /**
   * Remove current user's avatar
   * @returns {Promise<Object>} Removal confirmation
   */
  async removeAvatar() {
    const response = await client.delete('/avatar/remove/me');
    return response.data;
  },

  /**
   * Get current user's avatar information
   * @returns {Promise<Object>} Avatar info and upload limits
   */
  async getAvatarInfo() {
    const response = await client.get('/avatar/info/me');
    return response.data;
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
   * Validate image file before upload
   * @param {File} file - File to validate
   * @returns {Object} Validation result
   */
  validateImageFile(file) {
    const supportedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    const errors = [];
    
    if (!file) {
      errors.push('No file selected');
    } else {
      if (!supportedTypes.includes(file.type)) {
        errors.push('Unsupported file type. Please use JPEG, PNG, or WEBP');
      }
      // Remove size check - we'll compress if needed
    }
    
    return {
      isValid: errors.length === 0,
      errors
    };
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
    if (url) {
      URL.revokeObjectURL(url);
    }
  }
};

export default avatarAPI;