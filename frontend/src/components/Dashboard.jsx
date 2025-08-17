import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useProfile } from '../contexts/ProfileContext';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const { profile, getProfileCompletionPercentage } = useProfile();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleProfileView = () => {
    navigate('/profile');
  };

  const handleProfileEdit = () => {
    navigate('/profile/edit');
  };

  return (
    <div className="min-h-screen bg-[#fcfbf8] p-4" style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}>
      <div className="max-w-4xl mx-auto">
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-bold text-[#1c180d]">Welcome to Mini Lively</h1>
            <p className="text-[#9e8747]">Hello, {user?.first_name || 'User'}!</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-[#fac638] text-[#1c180d] rounded-lg hover:bg-[#e9b429] transition-colors font-medium"
          >
            Logout
          </button>
        </header>

        <div className="bg-[#f4f0e6] rounded-xl p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-[#1c180d]">User Profile</h2>
            <div className="flex gap-3">
              <button
                onClick={handleProfileView}
                className="px-4 py-2 bg-[#fcfbf8] text-[#1c180d] rounded-lg hover:bg-white transition-colors font-medium border border-[#e9e2ce]"
              >
                View Profile
              </button>
              <button
                onClick={handleProfileEdit}
                className="px-4 py-2 bg-[#fac638] text-[#1c180d] rounded-lg hover:bg-[#e9b429] transition-colors font-medium"
              >
                {profile ? 'Edit Profile' : 'Complete Profile'}
              </button>
            </div>
          </div>
          
          {profile && (
            <div className="mb-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-[#1c180d] font-medium">Profile Completion</span>
                <span className="text-[#1c180d] font-bold">{getProfileCompletionPercentage()}%</span>
              </div>
              <div className="w-full bg-[#e9e2ce] rounded-full h-2">
                <div 
                  className="bg-[#fac638] h-2 rounded-full transition-all duration-300"
                  style={{ width: `${getProfileCompletionPercentage()}%` }}
                ></div>
              </div>
            </div>
          )}
          
          <div className="space-y-2 text-[#1c180d]">
            <p><span className="font-medium">Name:</span> {(user?.first_name || user?.last_name) ? `${user?.first_name || ''} ${user?.last_name || ''}`.trim() : 'Not provided'}</p>
            <p><span className="font-medium">Email:</span> {user?.email}</p>
            <p><span className="font-medium">Account Status:</span> 
              <span className={`ml-2 px-2 py-1 rounded text-xs ${user?.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                {user?.is_active ? 'Active' : 'Inactive'}
              </span>
            </p>
            <p><span className="font-medium">Email Verified:</span> 
              <span className={`ml-2 px-2 py-1 rounded text-xs ${user?.is_verified ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                {user?.is_verified ? 'Verified' : 'Pending'}
              </span>
            </p>
            {user?.oauth_provider && (
              <p><span className="font-medium">OAuth Provider:</span> {user.oauth_provider}</p>
            )}
          </div>
        </div>

        <div className="bg-[#f4f0e6] rounded-xl p-6">
          <h2 className="text-xl font-semibold text-[#1c180d] mb-4">Family Activity Monitoring</h2>
          <p className="text-[#9e8747] mb-4">
            Start tracking your family's activities, managing schedules, and organizing events.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 border border-[#e9e2ce] rounded-lg bg-[#fcfbf8] hover:bg-white transition-colors">
              <h3 className="font-medium text-[#1c180d]">Activities</h3>
              <p className="text-sm text-[#9e8747]">Track daily activities</p>
            </div>
            <div className="p-4 border border-[#e9e2ce] rounded-lg bg-[#fcfbf8] hover:bg-white transition-colors">
              <h3 className="font-medium text-[#1c180d]">Schedules</h3>
              <p className="text-sm text-[#9e8747]">Manage recurring events</p>
            </div>
            <div className="p-4 border border-[#e9e2ce] rounded-lg bg-[#fcfbf8] hover:bg-white transition-colors">
              <h3 className="font-medium text-[#1c180d]">Events</h3>
              <p className="text-sm text-[#9e8747]">Organize special occasions</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;