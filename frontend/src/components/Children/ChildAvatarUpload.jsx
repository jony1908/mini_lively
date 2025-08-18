/**
 * ChildAvatarUpload Component
 * 
 * Handles child avatar upload with:
 * - Image preview with proper scaling
 * - File validation and error handling
 * - Real-time upload progress
 * - Child-specific styling and messaging
 */

import React, { useState, useRef, useEffect } from 'react';
import memberAPI from '../../services/member';

const ChildAvatarUpload = ({ 
  childId, 
  childName, 
  currentAvatarUrl, 
  onAvatarUpdate, 
  className = '',
  compact = false 
}) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(currentAvatarUrl);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [compressionInfo, setCompressionInfo] = useState(null);
  const fileInputRef = useRef(null);

  // Update preview when current avatar changes
  useEffect(() => {
    if (currentAvatarUrl && !selectedFile) {
      setPreviewUrl(currentAvatarUrl);
    }
  }, [currentAvatarUrl, selectedFile]);

  // Cleanup preview URL on unmount
  useEffect(() => {
    return () => {
      if (previewUrl && previewUrl !== currentAvatarUrl) {
        memberAPI.cleanupPreviewUrl(previewUrl);
      }
    };
  }, [previewUrl, currentAvatarUrl]);

  /**
   * Handle file selection
   */
  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file
    const validation = memberAPI.validateAvatarFile(file);
    if (!validation.isValid) {
      setError(validation.error);
      return;
    }

    setError('');
    setProcessing(true);
    setCompressionInfo(null);

    try {
      // Process file (compress if needed)
      const { file: processedFile, wasCompressed } = await memberAPI.processFileForUpload(file);
      
      setSelectedFile(processedFile);
      
      // Set compression info
      if (wasCompressed) {
        const originalSizeMB = (file.size / (1024 * 1024)).toFixed(1);
        const compressedSizeMB = (processedFile.size / (1024 * 1024)).toFixed(1);
        setCompressionInfo({
          original: originalSizeMB,
          compressed: compressedSizeMB
        });
      }
      
      // Create preview
      const newPreviewUrl = memberAPI.createPreviewUrl(processedFile);
      
      // Cleanup old preview if it exists
      if (previewUrl && previewUrl !== currentAvatarUrl) {
        memberAPI.cleanupPreviewUrl(previewUrl);
      }
      
      setPreviewUrl(newPreviewUrl);
    } catch (err) {
      setError('Failed to process image. Please try a different file.');
    } finally {
      setProcessing(false);
    }
  };

  /**
   * Handle avatar upload
   */
  const handleUpload = async () => {
    if (!selectedFile || !childId) return;

    setUploading(true);
    setUploadProgress(0);
    setError('');

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90));
      }, 100);

      const result = await memberAPI.uploadMemberAvatar(childId, selectedFile);
      
      clearInterval(progressInterval);
      setUploadProgress(100);

      // Update parent component with new avatar URL
      if (onAvatarUpdate) {
        onAvatarUpdate(result.avatar_url);
      }

      // Reset state
      setSelectedFile(null);
      setPreviewUrl(result.avatar_url);
      
      // Success feedback
      setTimeout(() => {
        setUploadProgress(0);
      }, 1000);

    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload avatar');
      setUploadProgress(0);
    } finally {
      setUploading(false);
    }
  };

  /**
   * Handle avatar removal
   */
  const handleRemove = async () => {
    if (!currentAvatarUrl || !childId) return;

    try {
      await memberAPI.removeMemberAvatar(childId);
      
      // Update parent component
      if (onAvatarUpdate) {
        onAvatarUpdate(null);
      }

      // Reset state
      setSelectedFile(null);
      setPreviewUrl(null);
      
      // Clear file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }

    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to remove avatar');
    }
  };

  /**
   * Cancel file selection
   */
  const handleCancel = () => {
    if (previewUrl && previewUrl !== currentAvatarUrl) {
      memberAPI.cleanupPreviewUrl(previewUrl);
    }
    
    setSelectedFile(null);
    setPreviewUrl(currentAvatarUrl);
    setError('');
    setCompressionInfo(null);
    
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Compact version for forms
  if (compact) {
    return (
      <div className={`child-avatar-upload-compact ${className}`}>
        <div className="flex items-center gap-4">
          {/* Avatar Preview */}
          <div className="relative">
            <div className="w-16 h-16 rounded-full overflow-hidden bg-[#f4f0e6] border-2 border-[#e9e2ce]">
              {previewUrl ? (
                <img 
                  src={previewUrl} 
                  alt={`${childName} Avatar`} 
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" fill="#9e8747" viewBox="0 0 256 256">
                    <path d="M230.92,212c-15.23-26.33-38.7-45.21-66.09-54.16a72,72,0,1,0-73.66,0C63.78,166.78,40.31,185.66,25.08,212a8,8,0,1,0,13.85,8c18.84-32.56,52.14-52,89.07-52s70.23,19.44,89.07,52a8,8,0,1,0,13.85-8ZM72,96a56,56,0,1,1,56,56A56.06,56.06,0,0,1,72,96Z"></path>
                  </svg>
                </div>
              )}
            </div>
            
            {/* Processing indicator */}
            {processing && (
              <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 bg-blue-500 text-white text-xs px-1 py-0.5 rounded-full">
                Processing...
              </div>
            )}
          </div>

          {/* Controls */}
          <div className="flex-1">
            <p className="text-[#1c180d] text-sm font-medium mb-2">{childName}'s Photo</p>
            
            {!selectedFile ? (
              <div className="flex gap-2">
                <label htmlFor={`child-avatar-${childId}`}>
                  <input
                    id={`child-avatar-${childId}`}
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                  <button
                    type="button"
                    className="text-xs bg-[#fac638] text-[#1c180d] px-3 py-1.5 rounded-lg hover:bg-[#e9b429] transition-colors cursor-pointer font-medium"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    Choose Photo
                  </button>
                </label>
                {currentAvatarUrl && (
                  <button
                    type="button"
                    onClick={handleRemove}
                    className="text-xs bg-red-100 text-red-600 px-3 py-1.5 rounded-lg hover:bg-red-200 transition-colors"
                  >
                    Remove
                  </button>
                )}
              </div>
            ) : (
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={handleUpload}
                  disabled={uploading || processing}
                  className="text-xs bg-[#fac638] text-[#1c180d] px-3 py-1.5 rounded-lg hover:bg-[#f4c232] transition-colors disabled:opacity-50"
                >
                  {uploading ? 'Uploading...' : 'Upload'}
                </button>
                <button
                  type="button"
                  onClick={handleCancel}
                  disabled={uploading || processing}
                  className="text-xs bg-[#f4f0e6] text-[#1c180d] px-3 py-1.5 rounded-lg hover:bg-[#e9e2ce] transition-colors disabled:opacity-50"
                >
                  Cancel
                </button>
              </div>
            )}

            {/* Upload progress */}
            {uploading && (
              <div className="mt-2">
                <div className="w-full bg-[#e9e2ce] rounded-full h-1">
                  <div 
                    className="bg-[#fac638] h-1 rounded-full transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  ></div>
                </div>
              </div>
            )}

            {/* Error message */}
            {error && (
              <p className="text-red-600 text-xs mt-1">{error}</p>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Full version for dedicated avatar upload
  return (
    <div className={`child-avatar-upload ${className}`}>
      <h3 className="text-[#1c180d] text-lg font-bold leading-tight tracking-[-0.015em] pb-2">
        {childName}'s Photo
      </h3>
      
      <div className="flex flex-col items-center gap-6 rounded-xl border-2 border-dashed border-[#e9e2ce] px-6 py-14">
        {/* Avatar Preview */}
        <div className="relative">
          <div className="w-32 h-32 rounded-full overflow-hidden bg-[#f4f0e6] border-4 border-[#e9e2ce]">
            {previewUrl ? (
              <img 
                src={previewUrl} 
                alt={`${childName} Avatar Preview`} 
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="32px" height="32px" fill="#9e8747" viewBox="0 0 256 256">
                  <path d="M230.92,212c-15.23-26.33-38.7-45.21-66.09-54.16a72,72,0,1,0-73.66,0C63.78,166.78,40.31,185.66,25.08,212a8,8,0,1,0,13.85,8c18.84-32.56,52.14-52,89.07-52s70.23,19.44,89.07,52a8,8,0,1,0,13.85-8ZM72,96a56,56,0,1,1,56,56A56.06,56.06,0,0,1,72,96Z"></path>
                </svg>
              </div>
            )}
          </div>
          
          {/* Processing indicator */}
          {processing && (
            <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-blue-500 text-white text-xs px-2 py-1 rounded-full">
              Processing...
            </div>
          )}
          
          {/* Ready indicator for selected file */}
          {selectedFile && !processing && (
            <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-[#fac638] text-[#1c180d] text-xs px-2 py-1 rounded-full">
              Ready to upload
            </div>
          )}
        </div>

        {/* File name and processing info */}
        {selectedFile && !processing && (
          <div className="text-center">
            <p className="text-[#1c180d] text-sm font-medium">
              {selectedFile.name}
            </p>
            <p className="text-[#9e8747] text-xs mt-1">
              Will be resized to 256×256 pixels
            </p>
            {compressionInfo && (
              <p className="text-green-600 text-xs mt-1">
                Compressed from {compressionInfo.original}MB to {compressionInfo.compressed}MB
              </p>
            )}
          </div>
        )}

        {/* Processing feedback */}
        {processing && (
          <div className="text-center">
            <p className="text-blue-600 text-sm font-medium">
              Processing image...
            </p>
            <p className="text-[#9e8747] text-xs mt-1">
              Optimizing file size for faster upload
            </p>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="text-red-600 text-sm text-center max-w-sm">
            {error}
          </div>
        )}

        {/* Upload progress */}
        {uploading && (
          <div className="w-full max-w-xs">
            <div className="flex justify-between text-sm text-[#1c180d] mb-1">
              <span>Uploading...</span>
              <span>{uploadProgress}%</span>
            </div>
            <div className="w-full bg-[#e9e2ce] rounded-full h-2">
              <div 
                className="bg-[#fac638] h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Action buttons */}
        <div className="flex flex-col sm:flex-row gap-3">
          {!selectedFile ? (
            <>
              {/* Select file button */}
              <label htmlFor={`child-avatar-full-${childId}`}>
                <input
                  id={`child-avatar-full-${childId}`}
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <button
                  type="button"
                  className="flex items-center justify-center overflow-hidden rounded-xl h-10 px-6 bg-[#fac638] text-[#1c180d] text-sm font-bold leading-normal tracking-[0.015em] hover:bg-[#e9b429] transition-colors cursor-pointer"
                  onClick={() => fileInputRef.current?.click()}
                >
                  Choose Photo
                </button>
              </label>

              {/* Remove avatar button */}
              {currentAvatarUrl && (
                <button
                  type="button"
                  onClick={handleRemove}
                  className="flex items-center justify-center overflow-hidden rounded-xl h-10 px-6 bg-red-100 text-red-600 text-sm font-bold leading-normal tracking-[0.015em] hover:bg-red-200 transition-colors"
                >
                  Remove
                </button>
              )}
            </>
          ) : (
            <>
              {/* Upload button */}
              <button
                type="button"
                onClick={handleUpload}
                disabled={uploading || processing}
                className="flex items-center justify-center overflow-hidden rounded-xl h-10 px-6 bg-[#fac638] text-[#1c180d] text-sm font-bold leading-normal tracking-[0.015em] hover:bg-[#f4c232] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {uploading ? 'Uploading...' : 'Upload Avatar'}
              </button>

              {/* Cancel button */}
              <button
                type="button"
                onClick={handleCancel}
                disabled={uploading || processing}
                className="flex items-center justify-center overflow-hidden rounded-xl h-10 px-6 bg-[#f4f0e6] text-[#1c180d] text-sm font-bold leading-normal tracking-[0.015em] hover:bg-[#e9e2ce] transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
            </>
          )}
        </div>

        {/* Upload guidelines */}
        <div className="text-center text-xs text-[#9e8747] max-w-sm">
          <p>Large images will be automatically compressed</p>
          <p>Supported formats: JPEG, PNG, WEBP</p>
          <p>Images will be resized to 256×256 pixels</p>
        </div>
      </div>
    </div>
  );
};

export default ChildAvatarUpload;