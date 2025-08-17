import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useProfile } from '../../contexts/ProfileContext';
import { useAuth } from '../../contexts/AuthContext';
import { authAPI } from '../../services/auth';
import AvatarUpload from '../../components/Profile/AvatarUpload';

const ProfileForm = () => {
  const navigate = useNavigate();
  const { createProfile, updateProfile, profile, loading, error } = useProfile();
  const { user, setUser } = useAuth();

  // Form state
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    address: '',
    city: '',
    state: '',
    postalCode: '',
    country: '',
  });
  
  // Avatar state
  const [avatarUrl, setAvatarUrl] = useState(null);

  // Initialize form with existing profile data
  useEffect(() => {
    if (profile) {
      setFormData({
        firstName: user?.first_name || '',
        lastName: user?.last_name || '',
        address: profile.address || '',
        city: profile.city || '',
        state: profile.state || '',
        postalCode: profile.postal_code || '',
        country: profile.country || '',
      });
      setAvatarUrl(profile.profile_picture_url);
    } else if (user) {
      setFormData(prev => ({
        ...prev,
        firstName: user.first_name || '',
        lastName: user.last_name || '',
      }));
    }
  }, [profile, user]);

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  // Handle avatar update from AvatarUpload component
  const handleAvatarUpdate = (newAvatarUrl) => {
    setAvatarUrl(newAvatarUrl);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // First, update user's first_name and last_name if they changed
      if (formData.firstName !== user?.first_name || formData.lastName !== user?.last_name) {
        const userData = {
          first_name: formData.firstName || null,
          last_name: formData.lastName || null,
        };
        const updatedUser = await authAPI.updateUser(userData);
        setUser(updatedUser); // Update user in auth context
      }

      // Then, update or create profile data
      const profileData = {
        address: formData.address,
        city: formData.city,
        state: formData.state,
        postal_code: formData.postalCode,
        country: formData.country,
        profile_picture_url: avatarUrl || profile?.profile_picture_url,
      };

      if (profile) {
        await updateProfile(profileData);
      } else {
        await createProfile(profileData);
      }

      // Navigate to dashboard or profile view
      navigate('/dashboard');
    } catch (error) {
      console.error('Failed to save profile:', error);
    }
  };

  // Handle back navigation
  const handleBack = () => {
    navigate(-1);
  };

  // Handle add child (placeholder)
  const handleAddChild = () => {
    // TODO: Implement add child functionality
    console.log('Add child functionality to be implemented');
  };

  return (
    <div 
      className="relative flex size-full min-h-screen flex-col bg-[#fcfbf8] justify-between group/design-root overflow-x-hidden"
      style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}
    >
      <div>
        {/* Header */}
        <div className="flex items-center bg-[#fcfbf8] p-4 pb-2 justify-between">
          <button 
            onClick={handleBack}
            className="text-[#1c180d] flex size-16 shrink-0 items-center cursor-pointer bg-transparent border-none"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path>
            </svg>
          </button>
          <h2 className="text-[#1c180d] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">
            Complete Profile
          </h2>
        </div>

        {/* Welcome Section */}
        <h2 className="text-[#1c180d] tracking-light text-[28px] font-bold leading-tight px-4 text-center pb-3 pt-5">
          Welcome
        </h2>
        <p className="text-[#1c180d] text-base font-normal leading-normal pb-3 pt-1 px-4 text-center">
          Please complete your profile to manage fun activities for yourself and your loved ones.
        </p>

        {/* Error Message */}
        {error && (
          <div className="mx-4 mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-xl">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit}>
          {/* First Name & Last Name */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="text"
                name="firstName"
                placeholder="First Name"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal"
                value={formData.firstName}
                onChange={handleInputChange}
              />
            </label>
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="text"
                name="lastName"
                placeholder="Last Name"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal"
                value={formData.lastName}
                onChange={handleInputChange}
              />
            </label>
          </div>

          {/* Address */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="text"
                name="address"
                placeholder="Address"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal"
                value={formData.address}
                onChange={handleInputChange}
              />
            </label>
          </div>

          {/* City */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="text"
                name="city"
                placeholder="City"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal"
                value={formData.city}
                onChange={handleInputChange}
              />
            </label>
          </div>

          {/* State */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="text"
                name="state"
                placeholder="State"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal"
                value={formData.state}
                onChange={handleInputChange}
              />
            </label>
          </div>

          {/* Zip Code */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="text"
                name="postalCode"
                placeholder="Zip Code"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal"
                value={formData.postalCode}
                onChange={handleInputChange}
              />
            </label>
          </div>

          {/* Country */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="text"
                name="country"
                placeholder="Country"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal"
                value={formData.country}
                onChange={handleInputChange}
              />
            </label>
          </div>

          {/* Avatar Upload */}
          <div className="px-4 py-3">
            <AvatarUpload 
              currentAvatarUrl={avatarUrl}
              onAvatarUpdate={handleAvatarUpdate}
            />
          </div>

          {/* Add Child Button */}
          <div className="flex px-4 py-3 justify-center">
            <button
              type="button"
              onClick={handleAddChild}
              className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 bg-[#f4f0e6] text-[#1c180d] gap-2 pl-5 text-base font-bold leading-normal tracking-[0.015em]"
            >
              <div className="text-[#1c180d]">
                <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M256,136a8,8,0,0,1-8,8H232v16a8,8,0,0,1-16,0V144H200a8,8,0,0,1,0-16h16V112a8,8,0,0,1,16,0v16h16A8,8,0,0,1,256,136Zm-57.87,58.85a8,8,0,0,1-12.26,10.3C165.75,181.19,138.09,168,108,168s-57.75,13.19-77.87,37.15a8,8,0,0,1-12.25-10.3c14.94-17.78,33.52-30.41,54.17-37.17a68,68,0,1,1,71.9,0C164.6,164.44,183.18,177.07,198.13,194.85ZM108,152a52,52,0,1,0-52-52A52.06,52.06,0,0,0,108,152Z"></path>
                </svg>
              </div>
              <span className="truncate">Add Child</span>
            </button>
          </div>

          {/* Complete Profile Button */}
          <div className="flex px-4 py-3">
            <button
              type="submit"
              disabled={loading}
              className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 flex-1 bg-[#fac638] text-[#1c180d] text-base font-bold leading-normal tracking-[0.015em] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span className="truncate">
                {loading ? 'Saving...' : 'Complete Profile'}
              </span>
            </button>
          </div>
        </form>
      </div>
      
      {/* Bottom Spacer */}
      <div>
        <div className="h-5 bg-[#fcfbf8]"></div>
      </div>
    </div>
  );
};

export default ProfileForm;