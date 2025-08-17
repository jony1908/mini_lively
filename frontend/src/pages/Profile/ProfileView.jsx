import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useProfile } from '../../contexts/ProfileContext';
import { useAuth } from '../../contexts/AuthContext';

const ProfileView = () => {
  const navigate = useNavigate();
  const { profile, loading, error, getProfileCompletionPercentage } = useProfile();
  const { user } = useAuth();

  // Handle back navigation
  const handleBack = () => {
    navigate('/dashboard');
  };

  // Handle edit profile
  const handleEdit = () => {
    navigate('/profile/edit');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#fcfbf8]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#fac638] mx-auto"></div>
          <p className="mt-4 text-[#9e8747]">Loading profile...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#fcfbf8]">
        <div className="text-center px-4">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/profile/edit')}
            className="bg-[#fac638] text-[#1c180d] px-6 py-2 rounded-xl font-bold"
          >
            Create Profile
          </button>
        </div>
      </div>
    );
  }

  const completionPercentage = getProfileCompletionPercentage();

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
            Profile
          </h2>
        </div>

        {/* Profile Picture Section */}
        <div className="flex flex-col items-center py-6">
          <div className="w-24 h-24 rounded-full bg-[#f4f0e6] flex items-center justify-center mb-4">
            {profile?.profile_picture_url ? (
              <img 
                src={profile.profile_picture_url} 
                alt="Profile" 
                className="w-full h-full rounded-full object-cover"
              />
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" width="40px" height="40px" fill="#9e8747" viewBox="0 0 256 256">
                <path d="M230.92,212c-15.23-26.33-38.7-45.21-66.09-54.16a72,72,0,1,0-73.66,0C63.78,166.78,40.31,185.66,25.08,212a8,8,0,1,0,13.85,8c18.84-32.56,52.14-52,89.07-52s70.23,19.44,89.07,52a8,8,0,1,0,13.85-8ZM72,96a56,56,0,1,1,56,56A56.06,56.06,0,0,1,72,96Z"></path>
              </svg>
            )}
          </div>
          <h2 className="text-[#1c180d] text-xl font-bold">
            {user?.first_name} {user?.last_name}
          </h2>
          <p className="text-[#9e8747] text-sm">{user?.email}</p>
        </div>

        {/* Profile Completion */}
        <div className="px-4 py-3">
          <div className="bg-[#f4f0e6] rounded-xl p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-[#1c180d] font-medium">Profile Completion</span>
              <span className="text-[#1c180d] font-bold">{completionPercentage}%</span>
            </div>
            <div className="w-full bg-[#e9e2ce] rounded-full h-2">
              <div 
                className="bg-[#fac638] h-2 rounded-full transition-all duration-300"
                style={{ width: `${completionPercentage}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Profile Information */}
        <div className="px-4 py-3">
          <h3 className="text-[#1c180d] text-lg font-bold mb-4">Profile Information</h3>
          
          {/* Contact Information */}
          <div className="space-y-3">
            <div className="bg-[#f4f0e6] rounded-xl p-4">
              <label className="text-[#9e8747] text-sm font-medium">Phone Number</label>
              <p className="text-[#1c180d] text-base">
                {profile?.phone_number || 'Not provided'}
              </p>
            </div>

            <div className="bg-[#f4f0e6] rounded-xl p-4">
              <label className="text-[#9e8747] text-sm font-medium">Address</label>
              <p className="text-[#1c180d] text-base">
                {profile?.address || 'Not provided'}
              </p>
            </div>

            <div className="bg-[#f4f0e6] rounded-xl p-4">
              <label className="text-[#9e8747] text-sm font-medium">City</label>
              <p className="text-[#1c180d] text-base">
                {profile?.city || 'Not provided'}
              </p>
            </div>

            <div className="bg-[#f4f0e6] rounded-xl p-4">
              <label className="text-[#9e8747] text-sm font-medium">State</label>
              <p className="text-[#1c180d] text-base">
                {profile?.state || 'Not provided'}
              </p>
            </div>

            <div className="bg-[#f4f0e6] rounded-xl p-4">
              <label className="text-[#9e8747] text-sm font-medium">Zip Code</label>
              <p className="text-[#1c180d] text-base">
                {profile?.postal_code || 'Not provided'}
              </p>
            </div>

            <div className="bg-[#f4f0e6] rounded-xl p-4">
              <label className="text-[#9e8747] text-sm font-medium">Country</label>
              <p className="text-[#1c180d] text-base">
                {profile?.country || 'Not provided'}
              </p>
            </div>

            <div className="bg-[#f4f0e6] rounded-xl p-4">
              <label className="text-[#9e8747] text-sm font-medium">Timezone</label>
              <p className="text-[#1c180d] text-base">
                {profile?.timezone || 'Not provided'}
              </p>
            </div>
          </div>
        </div>

        {/* Activity Preferences */}
        {profile?.preferred_activity_types && profile.preferred_activity_types.length > 0 && (
          <div className="px-4 py-3">
            <h3 className="text-[#1c180d] text-lg font-bold mb-4">Activity Preferences</h3>
            <div className="bg-[#f4f0e6] rounded-xl p-4">
              <div className="flex flex-wrap gap-2">
                {profile.preferred_activity_types.map((activity, index) => (
                  <span 
                    key={index}
                    className="bg-[#fac638] text-[#1c180d] px-3 py-1 rounded-full text-sm font-medium"
                  >
                    {activity}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Edit Profile Button */}
        <div className="flex px-4 py-3">
          <button
            onClick={handleEdit}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 flex-1 bg-[#fac638] text-[#1c180d] text-base font-bold leading-normal tracking-[0.015em]"
          >
            <span className="truncate">Edit Profile</span>
          </button>
        </div>
      </div>
      
      {/* Bottom Spacer */}
      <div>
        <div className="h-5 bg-[#fcfbf8]"></div>
      </div>
    </div>
  );
};

export default ProfileView;