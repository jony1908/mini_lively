/**
 * EditChildForm Component
 * 
 * Form for editing existing child information:
 * - Pre-populated with current child data
 * - Personal information (name, age, gender)
 * - Multi-select interests and skills
 * - Form validation and error handling
 * - Mobile-first responsive design
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import MultiSelect from '../common/MultiSelect';
import DatePicker from '../common/DatePicker';
import ChildAvatarUpload from './ChildAvatarUpload';
import memberAPI from '../../services/member';

const EditChildForm = () => {
  const { memberId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  const [options, setOptions] = useState({ interests: [], skills: [] });
  const [originalChild, setOriginalChild] = useState(null);

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

  // Load child data and options on component mount
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setErrors({});

        // Load child data and options in parallel
        const [childData, optionsData] = await Promise.all([
          memberAPI.getMember(memberId),
          memberAPI.getMemberOptions()
        ]);

        setOriginalChild(childData);
        setOptions(optionsData);

        // Populate form with child data
        setFormData({
          first_name: childData.first_name || '',
          last_name: childData.last_name || '',
          date_of_birth: childData.date_of_birth || '',
          gender: childData.gender || '',
          relationship: childData.relationship || '',
          interests: childData.interests || [],
          skills: childData.skills || [],
          avatar_url: childData.avatar_url || null
        });

      } catch (error) {
        console.error('Failed to load data:', error);
        setErrors({
          general: 'Failed to load child information. Please try again.'
        });
      } finally {
        setLoading(false);
      }
    };

    if (memberId) {
      loadData();
    }
  }, [memberId]);

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

  // Handle avatar update
  const handleAvatarUpdate = (avatarUrl) => {
    setFormData(prev => ({
      ...prev,
      avatar_url: avatarUrl
    }));
  };

  // Check if form has changes
  const hasChanges = () => {
    if (!originalChild) return false;
    
    return (
      formData.first_name !== originalChild.first_name ||
      formData.last_name !== originalChild.last_name ||
      formData.date_of_birth !== originalChild.date_of_birth ||
      formData.gender !== (originalChild.gender || '') ||
      JSON.stringify(formData.interests) !== JSON.stringify(originalChild.interests || []) ||
      JSON.stringify(formData.skills) !== JSON.stringify(originalChild.skills || []) ||
      formData.avatar_url !== (originalChild.avatar_url || null)
    );
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

      // Submit update (excluding avatar_url - it's managed separately)
      const updateData = { ...formData };
      delete updateData.avatar_url;
      
      const updatedMember = await memberAPI.updateMember(memberId, updateData);
      
      // Navigate to child profile with success message
      navigate(`/members/${memberId}`, { 
        state: { 
          message: `${formData.first_name} ${formData.last_name}'s profile has been updated successfully!` 
        }
      });

    } catch (error) {
      console.error('Failed to update child:', error);
      setErrors({
        general: error.response?.data?.detail || 'Failed to update child profile. Please try again.'
      });
    } finally {
      setSubmitting(false);
    }
  };

  // Handle back navigation
  const handleBack = () => {
    if (hasChanges() && !submitting) {
      if (window.confirm('You have unsaved changes. Are you sure you want to leave?')) {
        navigate(`/members/${memberId}`);
      }
    } else {
      navigate(`/members/${memberId}`);
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-[#fcfbf8] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#fac638] mx-auto"></div>
          <p className="mt-4 text-[#9e8747]">Loading child information...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (!originalChild && !loading) {
    return (
      <div className="min-h-screen bg-[#fcfbf8]" style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}>
        <div className="flex items-center bg-[#fcfbf8] p-4 pb-2 justify-between">
          <button 
            onClick={() => navigate('/children')}
            className="text-[#1c180d] flex size-16 shrink-0 items-center cursor-pointer bg-transparent border-none"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path>
            </svg>
          </button>
          <h2 className="text-[#1c180d] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">
            Edit Child
          </h2>
        </div>

        <div className="max-w-2xl mx-auto px-4 py-8">
          <div className="text-center">
            <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-xl text-red-700">
              {errors.general || 'Child not found'}
            </div>
            <button
              onClick={() => navigate('/children')}
              className="bg-[#fac638] text-[#1c180d] px-6 py-3 rounded-xl font-medium hover:bg-[#e9b429] transition-colors"
            >
              Back to Children
            </button>
          </div>
        </div>
      </div>
    );
  }

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
          Edit {originalChild?.first_name || 'Child'}
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

        {/* Avatar Upload */}
        <div className="py-3">
          <p className="text-[#1c180d] text-base font-medium leading-normal pb-3">Profile Photo</p>
          <div className="bg-[#f4f0e6] rounded-xl p-4">
            <ChildAvatarUpload
              memberId={memberId}
              childName={formData.first_name || 'Child'}
              currentAvatarUrl={formData.avatar_url}
              onAvatarUpdate={handleAvatarUpdate}
              compact={false}
            />
          </div>
        </div>

        {/* Submit Buttons */}
        <div className="flex gap-3 px-0 py-6">
          <button
            type="button"
            onClick={handleBack}
            disabled={submitting}
            className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 flex-1 bg-[#f4f0e6] text-[#1c180d] text-base font-medium leading-normal hover:bg-[#e9e2ce] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting || !hasChanges()}
            className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 flex-1 bg-[#fac638] text-[#1c180d] text-base font-bold leading-normal tracking-[0.015em] hover:bg-[#e9b429] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="truncate">
              {submitting ? 'Saving...' : hasChanges() ? 'Save Changes' : 'No Changes'}
            </span>
          </button>
        </div>
      </form>

      <div className="h-5 bg-[#fcfbf8]"></div>
    </div>
  );
};

export default EditChildForm;