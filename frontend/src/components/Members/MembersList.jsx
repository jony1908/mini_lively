/**
 * MembersList Component
 * 
 * Main family members management interface:
 * - Displays all family members in card format
 * - Add new member button
 * - Edit and delete functionality
 * - Empty state for no members
 * - Enhanced statistics with age groups
 */

import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import MemberCard from './MemberCard';
import { useMember } from '../../contexts/MemberContext';

const MembersList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { members, loading, error, refreshMembers, getMembersStats } = useMember();
  const [successMessage, setSuccessMessage] = useState('');

  // Load members on component mount
  useEffect(() => {
    refreshMembers();
    
    // Check for success message from navigation state
    if (location.state?.message) {
      setSuccessMessage(location.state.message);
      // Clear the message from navigation state
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location.state, navigate, refreshMembers]);

  // Clear success message after 5 seconds
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => {
        setSuccessMessage('');
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  const handleAddMember = () => {
    navigate('/members/add');
  };

  const handleEditMember = (memberId) => {
    navigate(`/members/edit/${memberId}`);
  };

  const handleDeleteMember = async (memberId) => {
    try {
      // This will be handled by the context
      setSuccessMessage('Family member removed successfully');
      await refreshMembers(); // Reload the list
    } catch (err) {
      console.error('Failed to delete member:', err);
    }
  };

  const handleBack = () => {
    navigate('/dashboard');
  };

  const stats = getMembersStats();

  if (loading) {
    return (
      <div className="min-h-screen bg-[#fcfbf8] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#fac638] mx-auto"></div>
          <p className="mt-4 text-[#9e8747]">Loading family members...</p>
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
          Family Members
        </h2>
      </div>

      <div className="max-w-4xl mx-auto px-4 pb-8">
        {/* Success Message */}
        {successMessage && (
          <div className="mb-4 p-3 bg-green-100 border border-green-300 rounded-xl text-green-700 text-sm">
            {successMessage}
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-300 rounded-xl text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Add Member Button */}
        <div className="mb-6">
          <button
            onClick={handleAddMember}
            className="flex items-center gap-2 bg-[#fac638] text-[#1c180d] px-6 py-3 rounded-xl font-medium hover:bg-[#e9b429] transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256">
              <path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path>
            </svg>
            Add Family Member
          </button>
        </div>

        {/* Members Grid */}
        {members.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {members.map((member) => (
              <MemberCard
                key={member.id}
                member={member}
                onEdit={handleEditMember}
                onDelete={handleDeleteMember}
              />
            ))}
          </div>
        ) : (
          /* Empty State */
          <div className="text-center py-12">
            <div className="mb-6">
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                width="64" 
                height="64" 
                fill="#9e8747" 
                viewBox="0 0 256 256"
                className="mx-auto"
              >
                <path d="M230.92,212c-15.23-26.33-38.7-45.21-66.09-54.16a72,72,0,1,0-73.66,0C63.78,166.78,40.31,185.66,25.08,212a8,8,0,1,0,13.85,8c18.84-32.56,52.14-52,89.07-52s70.23,19.44,89.07,52a8,8,0,1,0,13.85-8ZM72,96a56,56,0,1,1,56,56A56.06,56.06,0,0,1,72,96Z"></path>
              </svg>
            </div>
            <h3 className="text-[#1c180d] text-xl font-bold mb-2">No Family Members Added Yet</h3>
            <p className="text-[#9e8747] mb-6 max-w-md mx-auto">
              Start by adding your family members to track their activities and manage schedules together.
            </p>
            <button
              onClick={handleAddMember}
              className="bg-[#fac638] text-[#1c180d] px-8 py-3 rounded-xl font-medium hover:bg-[#e9b429] transition-colors"
            >
              Add Your First Family Member
            </button>
          </div>
        )}

        {/* Enhanced Statistics */}
        {members.length > 0 && (
          <div className="mt-8 bg-[#f4f0e6] rounded-xl p-6">
            <h3 className="text-[#1c180d] text-lg font-bold mb-4">Family Overview</h3>
            
            {/* Basic Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center mb-6">
              <div>
                <div className="text-2xl font-bold text-[#fac638]">{stats.totalMembers}</div>
                <div className="text-[#9e8747] text-sm">
                  {stats.totalMembers === 1 ? 'Member' : 'Members'}
                </div>
              </div>
              <div>
                <div className="text-2xl font-bold text-[#fac638]">{stats.averageAge}</div>
                <div className="text-[#9e8747] text-sm">Avg Age</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-[#fac638]">{stats.totalInterests}</div>
                <div className="text-[#9e8747] text-sm">Total Interests</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-[#fac638]">{stats.totalSkills}</div>
                <div className="text-[#9e8747] text-sm">Total Skills</div>
              </div>
            </div>

            {/* Age Groups */}
            <div className="border-t border-[#d1c9b3] pt-4">
              <h4 className="text-[#1c180d] text-sm font-medium mb-3">Age Groups</h4>
              <div className="grid grid-cols-3 md:grid-cols-6 gap-3 text-center text-xs">
                {stats.ageGroups.babies > 0 && (
                  <div>
                    <div className="text-lg font-bold text-[#fac638]">{stats.ageGroups.babies}</div>
                    <div className="text-[#9e8747]">Babies</div>
                  </div>
                )}
                {stats.ageGroups.toddlers > 0 && (
                  <div>
                    <div className="text-lg font-bold text-[#fac638]">{stats.ageGroups.toddlers}</div>
                    <div className="text-[#9e8747]">Toddlers</div>
                  </div>
                )}
                {stats.ageGroups.children > 0 && (
                  <div>
                    <div className="text-lg font-bold text-[#fac638]">{stats.ageGroups.children}</div>
                    <div className="text-[#9e8747]">Children</div>
                  </div>
                )}
                {stats.ageGroups.teens > 0 && (
                  <div>
                    <div className="text-lg font-bold text-[#fac638]">{stats.ageGroups.teens}</div>
                    <div className="text-[#9e8747]">Teens</div>
                  </div>
                )}
                {stats.ageGroups.adults > 0 && (
                  <div>
                    <div className="text-lg font-bold text-[#fac638]">{stats.ageGroups.adults}</div>
                    <div className="text-[#9e8747]">Adults</div>
                  </div>
                )}
                {stats.ageGroups.seniors > 0 && (
                  <div>
                    <div className="text-lg font-bold text-[#fac638]">{stats.ageGroups.seniors}</div>
                    <div className="text-[#9e8747]">Seniors</div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MembersList;