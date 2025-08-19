/**
 * ChildProfileView Component
 * 
 * Displays comprehensive child profile information:
 * - Basic information (name, age, gender)
 * - Avatar with upload functionality
 * - Full interests and skills lists
 * - Edit and delete actions
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ChildAvatarUpload from './ChildAvatarUpload';
import memberAPI from '../../services/member';

const ChildProfileView = () => {
  const { memberId } = useParams();
  const navigate = useNavigate();
  const [child, setChild] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [avatarUpdateTrigger, setAvatarUpdateTrigger] = useState(0);

  // Load child data
  useEffect(() => {
    const loadChild = async () => {
      try {
        setLoading(true);
        setError('');
        const childData = await memberAPI.getMember(memberId);
        setChild(childData);
      } catch (err) {
        console.error('Failed to load child:', err);
        setError('Failed to load child profile. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    if (memberId) {
      loadChild();
    }
  }, [memberId]);

  // Handle avatar update
  const handleAvatarUpdate = (avatarUrl) => {
    setChild(prev => prev ? { ...prev, avatar_url: avatarUrl } : null);
    setAvatarUpdateTrigger(prev => prev + 1);
  };

  // Handle edit child
  const handleEdit = () => {
    navigate(`/members/edit/${memberId}`);
  };

  // Handle delete child
  const handleDelete = async () => {
    if (!child) return;
    
    if (window.confirm(`Are you sure you want to remove ${memberAPI.getMemberFullName(child)}? This action cannot be undone.`)) {
      try {
        await memberAPI.deleteMember(memberId);
        navigate('/members', { 
          state: { 
            message: `${child.first_name} ${child.last_name} has been removed successfully.` 
          }
        });
      } catch (err) {
        console.error('Failed to delete child:', err);
        setError('Failed to remove child. Please try again.');
      }
    }
  };

  // Handle back navigation
  const handleBack = () => {
    navigate('/members');
  };

  // Calculate age display
  const getAgeDisplay = (dateOfBirth, age) => {
    if (age === 0) return 'Under 1 year old';
    return `${age} year${age === 1 ? '' : 's'} old`;
  };

  // Format date for display
  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#fcfbf8] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#fac638] mx-auto"></div>
          <p className="mt-4 text-[#9e8747]">Loading child profile...</p>
        </div>
      </div>
    );
  }

  if (error || !child) {
    return (
      <div className="min-h-screen bg-[#fcfbf8]" style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}>
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
            Child Profile
          </h2>
        </div>

        <div className="max-w-2xl mx-auto px-4 py-8">
          <div className="text-center">
            <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-xl text-red-700">
              {error || 'Child not found'}
            </div>
            <button
              onClick={handleBack}
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
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
            <path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path>
          </svg>
        </button>
        <h2 className="text-[#1c180d] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">
          {memberAPI.getMemberFullName(child)}
        </h2>
      </div>

      <div className="max-w-2xl mx-auto px-4 pb-8">
        {/* Error Message */}
        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-300 rounded-xl text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Profile Card */}
        <div className="bg-[#f4f0e6] rounded-xl p-6 mb-6">
          {/* Header with avatar and basic info */}
          <div className="flex items-start gap-6 mb-6">
            {/* Avatar Section */}
            <div className="flex-shrink-0">
              <div className="w-24 h-24 rounded-full overflow-hidden bg-[#e9e2ce] border-2 border-[#d1c9b3] mb-4">
                <img 
                  src={memberAPI.getDisplayAvatarUrl(child)} 
                  alt={`${memberAPI.getMemberFullName(child)} avatar`} 
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    console.log('Avatar load error:', e.target.src);
                    e.target.style.display = 'none';
                    e.target.nextElementSibling.style.display = 'flex';
                  }}
                />
                <div className="w-full h-full flex items-center justify-center" style={{ display: child.avatar_url ? 'none' : 'flex' }}>
                  <svg xmlns="http://www.w3.org/2000/svg" width="32px" height="32px" fill="#9e8747" viewBox="0 0 256 256">
                    <path d="M230.92,212c-15.23-26.33-38.7-45.21-66.09-54.16a72,72,0,1,0-73.66,0C63.78,166.78,40.31,185.66,25.08,212a8,8,0,1,0,13.85,8c18.84-32.56,52.14-52,89.07-52s70.23,19.44,89.07,52a8,8,0,1,0,13.85-8ZM72,96a56,56,0,1,1,56,56A56.06,56.06,0,0,1,72,96Z"></path>
                  </svg>
                </div>
              </div>
              
              {/* Avatar Upload */}
              <ChildAvatarUpload
                memberId={child.id}
                childName={child.first_name}
                currentAvatarUrl={child.avatar_url}
                onAvatarUpdate={handleAvatarUpdate}
                compact={true}
                key={avatarUpdateTrigger}
              />
            </div>

            {/* Basic Information */}
            <div className="flex-1">
              <h1 className="text-[#1c180d] text-2xl font-bold leading-tight mb-2">
                {memberAPI.getMemberFullName(child)}
              </h1>
              
              <div className="space-y-2 text-[#9e8747]">
                <p className="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256">
                    <path d="M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM112,184a8,8,0,0,1-16,0V168H72a8,8,0,0,1,0-16H96V136a8,8,0,0,1,16,0v48Zm32-48a8,8,0,0,1-8,8,20,20,0,0,1-20-20V112a20,20,0,0,1,40,0,8,8,0,0,1-16,0,4,4,0,0,0-8,0v12A4,4,0,0,0,136,128,8,8,0,0,1,144,136Zm40,32a8,8,0,0,1-8,8H160a8,8,0,0,1-8-8V112a8,8,0,0,1,8-8h16a20,20,0,0,1,20,20v12A20,20,0,0,1,176,156Zm0-32V124a4,4,0,0,0-8,0v12a4,4,0,0,0,8,0Z"></path>
                  </svg>
                  <strong>{getAgeDisplay(child.date_of_birth, child.age)}</strong>
                </p>
                
                <p className="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256">
                    <path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM72,112a8,8,0,0,1,8-8H96a8,8,0,0,1,8,8v8a8,8,0,0,1-8,8H80a8,8,0,0,1-8-8Zm0,48a8,8,0,0,1,8-8H96a8,8,0,0,1,8,8v8a8,8,0,0,1-8,8H80a8,8,0,0,1-8-8Zm48-48a8,8,0,0,1,8-8h16a8,8,0,0,1,8,8v8a8,8,0,0,1-8,8H128a8,8,0,0,1-8-8Zm0,48a8,8,0,0,1,8-8h16a8,8,0,0,1,8,8v8a8,8,0,0,1-8,8H128a8,8,0,0,1-8-8Zm56-48a8,8,0,0,1,8-8h16a8,8,0,0,1,8,8v8a8,8,0,0,1-8,8H184a8,8,0,0,1-8-8Z"></path>
                  </svg>
                  Born {formatDate(child.date_of_birth)}
                </p>
                
                {child.gender && (
                  <p className="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256">
                      <path d="M230.92,212c-15.23-26.33-38.7-45.21-66.09-54.16a72,72,0,1,0-73.66,0C63.78,166.78,40.31,185.66,25.08,212a8,8,0,1,0,13.85,8c18.84-32.56,52.14-52,89.07-52s70.23,19.44,89.07,52a8,8,0,1,0,13.85-8ZM72,96a56,56,0,1,1,56,56A56.06,56.06,0,0,1,72,96Z"></path>
                    </svg>
                    {child.gender}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 mb-6">
            <button
              onClick={handleEdit}
              className="flex items-center gap-2 bg-[#fac638] text-[#1c180d] px-4 py-2 rounded-lg font-medium hover:bg-[#e9b429] transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256">
                <path d="M227.31,73.37,182.63,28.69a16,16,0,0,0-22.63,0L36.69,152A15.86,15.86,0,0,0,32,163.31V208a16,16,0,0,0,16,16H92.69A15.86,15.86,0,0,0,104,219.31L227.31,96A16,16,0,0,0,227.31,73.37ZM92.69,208H48V163.31l88-88L180.69,120ZM192,108.69,147.31,64l24-24L216,84.69Z"></path>
              </svg>
              Edit Profile
            </button>
            <button
              onClick={handleDelete}
              className="flex items-center gap-2 bg-red-100 text-red-600 px-4 py-2 rounded-lg font-medium hover:bg-red-200 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256">
                <path d="M216,48H176V40a24,24,0,0,0-24-24H104A24,24,0,0,0,80,40v8H40a8,8,0,0,0,0,16h8V208a16,16,0,0,0,16,16H192a16,16,0,0,0,16-16V64h8a8,8,0,0,0,0-16ZM96,40a8,8,0,0,1,8-8h48a8,8,0,0,1,8,8v8H96Zm96,168H64V64H192ZM112,104v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Zm48,0v64a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Z"></path>
              </svg>
              Remove
            </button>
          </div>

          {/* Interests Section */}
          <div className="mb-6">
            <h3 className="text-[#1c180d] text-lg font-bold mb-3">Interests</h3>
            {child.interests && child.interests.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {child.interests.map((interest, index) => (
                  <span
                    key={index}
                    className="inline-block bg-[#fac638] text-[#1c180d] text-sm px-3 py-1.5 rounded-lg font-medium"
                  >
                    {interest}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-[#9e8747] text-sm italic">No interests added yet</p>
            )}
          </div>

          {/* Skills Section */}
          <div>
            <h3 className="text-[#1c180d] text-lg font-bold mb-3">Skills</h3>
            {child.skills && child.skills.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {child.skills.map((skill, index) => (
                  <span
                    key={index}
                    className="inline-block bg-[#e9e2ce] text-[#1c180d] text-sm px-3 py-1.5 rounded-lg font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-[#9e8747] text-sm italic">No skills added yet</p>
            )}
          </div>
        </div>

        {/* Profile Statistics */}
        <div className="bg-[#f4f0e6] rounded-xl p-6">
          <h3 className="text-[#1c180d] text-lg font-bold mb-4">Profile Summary</h3>
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <div className="text-xl font-bold text-[#fac638]">
                {child.interests?.length || 0}
              </div>
              <div className="text-[#9e8747] text-sm">
                Interest{child.interests?.length === 1 ? '' : 's'}
              </div>
            </div>
            <div>
              <div className="text-xl font-bold text-[#fac638]">
                {child.skills?.length || 0}
              </div>
              <div className="text-[#9e8747] text-sm">
                Skill{child.skills?.length === 1 ? '' : 's'}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChildProfileView;