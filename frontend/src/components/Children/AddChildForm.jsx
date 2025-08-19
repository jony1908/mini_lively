/**
 * AddChildForm Component
 * 
 * Form for adding a new child with:
 * - Personal information (name, age, gender)
 * - Multi-select interests and skills
 * - Form validation and error handling
 * - Mobile-first responsive design matching provided HTML
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import MultiSelect from '../common/MultiSelect';
import DatePicker from '../common/DatePicker';
import memberAPI from '../../services/member';

const AddChildForm = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  const [options, setOptions] = useState({ interests: [], skills: [] });

  // Form data state
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    date_of_birth: '',
    gender: '',
    relationship: '',
    interests: [],
    skills: [],
    avatar_url: null
  });

  // Child ID for avatar upload (set after child creation)
  const [childId, setChildId] = useState(null);
  
  // Track selected avatar file for upload after member creation
  const [selectedAvatarFile, setSelectedAvatarFile] = useState(null);

  // Load options on component mount
  useEffect(() => {
    const loadOptions = async () => {
      try {
        setLoading(true);
        const optionsData = await memberAPI.getMemberOptions();
        setOptions(optionsData);
      } catch (error) {
        console.error('Failed to load options:', error);
      } finally {
        setLoading(false);
      }
    };

    loadOptions();
  }, []);

  // Cleanup preview URL on unmount
  useEffect(() => {
    return () => {
      if (formData.avatar_url && formData.avatar_url.startsWith('blob:')) {
        memberAPI.cleanupPreviewUrl(formData.avatar_url);
      }
    };
  }, [formData.avatar_url]);

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  // Handle gender selection
  const handleGenderChange = (gender) => {
    setFormData(prev => ({
      ...prev,
      gender
    }));
    
    if (errors.gender) {
      setErrors(prev => ({
        ...prev,
        gender: ''
      }));
    }
  };

  // Handle relationship selection
  const handleRelationshipChange = (relationship) => {
    setFormData(prev => ({
      ...prev,
      relationship
    }));
    
    if (errors.relationship) {
      setErrors(prev => ({
        ...prev,
        relationship: ''
      }));
    }
  };

  // Handle interests change
  const handleInterestsChange = (interests) => {
    setFormData(prev => ({
      ...prev,
      interests
    }));
  };

  // Handle skills change
  const handleSkillsChange = (skills) => {
    setFormData(prev => ({
      ...prev,
      skills
    }));
  };

  // Calculate age from date of birth for display
  const getAge = () => {
    if (!formData.date_of_birth) return null;
    return memberAPI.calculateAge(formData.date_of_birth);
  };

  // Get age display text
  const getAgeDisplayText = () => {
    const age = getAge();
    if (age === null) return '';
    if (age === 0) return 'Under 1 year old';
    return `${age} year${age === 1 ? '' : 's'} old`;
  };

  // Handle avatar file selection (for new members)
  const handleAvatarFileSelect = (file) => {
    setSelectedAvatarFile(file);
    // Create preview URL for display
    if (file) {
      const previewUrl = memberAPI.createPreviewUrl(file);
      setFormData(prev => ({
        ...prev,
        avatar_url: previewUrl
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        avatar_url: null
      }));
    }
  };

  // Handle avatar update (for existing members)
  const handleAvatarUpdate = (avatarUrl) => {
    setFormData(prev => ({
      ...prev,
      avatar_url: avatarUrl
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form data (excluding avatar_url from validation)
    const validationData = { ...formData };
    delete validationData.avatar_url;
    
    const validation = memberAPI.validateMemberData(validationData);
    if (!validation.isValid) {
      const newErrors = {};
      validation.errors.forEach(error => {
        if (error.includes('First name')) newErrors.first_name = error;
        else if (error.includes('Last name')) newErrors.last_name = error;
        else if (error.includes('Date of birth')) newErrors.date_of_birth = error;
        else if (error.includes('interests')) newErrors.interests = error;
        else if (error.includes('skills')) newErrors.skills = error;
        else newErrors.general = error;
      });
      setErrors(newErrors);
      return;
    }

    try {
      setSubmitting(true);
      setErrors({});

      // Submit child data (excluding avatar_url - it will be uploaded separately)
      const childData = { ...formData };
      delete childData.avatar_url;
      
      const newMember = await memberAPI.createMember(childData);
      setChildId(newMember.id);
      
      // Upload avatar if one was selected
      if (selectedAvatarFile) {
        try {
          const avatarResult = await memberAPI.uploadMemberAvatar(newMember.id, selectedAvatarFile);
          console.log('Avatar uploaded successfully:', avatarResult);
        } catch (avatarError) {
          console.error('Avatar upload failed:', avatarError);
          // Continue with navigation even if avatar upload fails
        }
      }
      
      // Navigate back to children list with success message
      navigate('/members', { 
        state: { 
          message: `${formData.first_name} ${formData.last_name} has been added successfully!` 
        }
      });

    } catch (error) {
      console.error('Failed to create child:', error);
      setErrors({
        general: error.response?.data?.detail || 'Failed to add child. Please try again.'
      });
    } finally {
      setSubmitting(false);
    }
  };

  // Handle back navigation
  const handleBack = () => {
    navigate('/members');
  };

  return (
    <div className="min-h-screen bg-[#fcfbf8]" style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}>
      {/* Header */}
      <div className="flex items-center bg-[#fcfbf8] p-4 pb-2 justify-between">
        <button 
          onClick={handleBack}
          className="text-[#1c180d] flex size-16 shrink-0 items-center cursor-pointer bg-transparent border-none"
          disabled={submitting}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
            <path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path>
          </svg>
        </button>
        <h2 className="text-[#1c180d] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">
          Add a Child
        </h2>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="max-w-[480px] mx-auto px-4">
        {/* General error message */}
        {errors.general && (
          <div className="mb-4 p-3 bg-red-100 border border-red-300 rounded-xl text-red-700 text-sm">
            {errors.general}
          </div>
        )}

        {/* First Name */}
        <div className="flex flex-wrap items-end gap-4 py-3">
          <label className="flex flex-col min-w-40 flex-1">
            <p className="text-[#1c180d] text-base font-medium leading-normal pb-2">First Name</p>
            <input
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleInputChange}
              placeholder="Enter first name"
              className={`form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal ${
                errors.first_name ? 'border-2 border-red-300' : ''
              }`}
              disabled={submitting}
            />
            {errors.first_name && (
              <p className="text-red-600 text-sm mt-1">{errors.first_name}</p>
            )}
          </label>
        </div>

        {/* Last Name */}
        <div className="flex flex-wrap items-end gap-4 py-3">
          <label className="flex flex-col min-w-40 flex-1">
            <p className="text-[#1c180d] text-base font-medium leading-normal pb-2">Last Name</p>
            <input
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleInputChange}
              placeholder="Enter last name"
              className={`form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal ${
                errors.last_name ? 'border-2 border-red-300' : ''
              }`}
              disabled={submitting}
            />
            {errors.last_name && (
              <p className="text-red-600 text-sm mt-1">{errors.last_name}</p>
            )}
          </label>
        </div>

        {/* Date of Birth */}
        <div className="py-3">
          <DatePicker
            label={`Date of Birth ${getAgeDisplayText() ? `(${getAgeDisplayText()})` : ''}`}
            value={formData.date_of_birth}
            onChange={(date) => setFormData(prev => ({ ...prev, date_of_birth: date }))}
            placeholder="Select date of birth..."
            maxDate={new Date().toISOString().split('T')[0]} // Prevent future dates
            error={errors.date_of_birth}
            className="w-full"
          />
        </div>

        {/* Gender Selection */}
        <div className="py-3">
          <p className="text-[#1c180d] text-base font-medium leading-normal pb-3">Gender</p>
          <div className="flex flex-wrap gap-3">
            {memberAPI.getGenderOptions().map((option) => (
              <label
                key={option.value}
                className={`text-sm font-medium leading-normal flex items-center justify-center rounded-xl border px-4 h-11 cursor-pointer transition-all ${
                  formData.gender === option.value
                    ? 'border-[3px] border-[#fac638] px-3.5 text-[#1c180d]'
                    : 'border-[#e9e2ce] text-[#1c180d]'
                } ${submitting ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {option.label}
                <input
                  type="radio"
                  name="gender"
                  value={option.value}
                  checked={formData.gender === option.value}
                  onChange={() => handleGenderChange(option.value)}
                  className="invisible absolute"
                  disabled={submitting}
                />
              </label>
            ))}
          </div>
          {errors.gender && (
            <p className="text-red-600 text-sm mt-1">{errors.gender}</p>
          )}
        </div>

        {/* Relationship Selection */}
        <div className="py-3">
          <p className="text-[#1c180d] text-base font-medium leading-normal pb-3">Relationship to You</p>
          <select
            name="relationship"
            value={formData.relationship}
            onChange={(e) => handleRelationshipChange(e.target.value)}
            className={`form-select flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal ${
              errors.relationship ? 'border-2 border-red-300' : ''
            }`}
            disabled={submitting}
          >
            <option value="">Select relationship...</option>
            {memberAPI.getRelationshipOptions().map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {errors.relationship && (
            <p className="text-red-600 text-sm mt-1">{errors.relationship}</p>
          )}
        </div>

        {/* Interests Multi-Select */}
        <div className="py-3">
          <MultiSelect
            label="Interests"
            options={options.interests}
            selectedItems={formData.interests}
            onChange={handleInterestsChange}
            placeholder="Select interests..."
            allowCustom={true}
            maxItems={20}
            error={errors.interests}
          />
        </div>

        {/* Skills Multi-Select */}
        <div className="py-3">
          <MultiSelect
            label="Skills"
            options={options.skills}
            selectedItems={formData.skills}
            onChange={handleSkillsChange}
            placeholder="Select skills..."
            allowCustom={true}
            maxItems={15}
            error={errors.skills}
          />
        </div>

        {/* Avatar Upload (Compact) */}
        <div className="py-3">
          <p className="text-[#1c180d] text-base font-medium leading-normal pb-3">Profile Photo (Optional)</p>
          <div className="bg-[#f4f0e6] rounded-xl p-4">
            <div className="flex items-center gap-4">
              {/* Avatar Preview */}
              <div className="w-16 h-16 rounded-full overflow-hidden bg-[#e9e2ce] border-2 border-[#d1c9b3] flex-shrink-0">
                <img 
                  src={formData.avatar_url || memberAPI.getDefaultMemberAvatar()} 
                  alt="Avatar preview" 
                  className="w-full h-full object-cover"
                />
              </div>
              
              {/* File Input */}
              <div className="flex-1">
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  onChange={(e) => {
                    const file = e.target.files[0];
                    if (file) {
                      const validation = memberAPI.validateAvatarFile(file);
                      if (validation.isValid) {
                        handleAvatarFileSelect(file);
                      } else {
                        alert(validation.error);
                        e.target.value = '';
                      }
                    } else {
                      handleAvatarFileSelect(null);
                    }
                  }}
                  className="block w-full text-sm text-[#1c180d] file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-medium file:bg-[#fac638] file:text-[#1c180d] hover:file:bg-[#e9b429] file:cursor-pointer"
                  disabled={submitting}
                />
                {selectedAvatarFile && (
                  <p className="text-[#9e8747] text-xs mt-1">
                    Selected: {selectedAvatarFile.name}
                  </p>
                )}
              </div>
            </div>
            <p className="text-[#9e8747] text-xs mt-2">
              Photo will be uploaded after creating the profile. Supported formats: JPEG, PNG, WEBP
            </p>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex px-0 py-6">
          <button
            type="submit"
            disabled={submitting || loading}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 flex-1 bg-[#fac638] text-[#1c180d] text-base font-bold leading-normal tracking-[0.015em] hover:bg-[#e9b429] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="truncate">
              {submitting ? 'Adding Child...' : 'Add Child'}
            </span>
          </button>
        </div>

        {/* Loading state */}
        {loading && (
          <div className="text-center text-[#9e8747] py-4">
            Loading options...
          </div>
        )}
      </form>

      <div className="h-5 bg-[#fcfbf8]"></div>
    </div>
  );
};

export default AddChildForm;