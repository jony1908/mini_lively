import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-[#f8f9fc] p-4">
      <div className="max-w-4xl mx-auto">
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-bold text-[#0d131c]">Welcome to Mini Lively</h1>
            <p className="text-[#49699c]">Hello, {user?.first_name}!</p>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-[#2071f3] text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Logout
          </button>
        </header>

        <div className="bg-white rounded-xl p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-[#0d131c] mb-4">User Profile</h2>
          <div className="space-y-2">
            <p><span className="font-medium">Name:</span> {user?.first_name} {user?.last_name}</p>
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

        <div className="mt-8 bg-white rounded-xl p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-[#0d131c] mb-4">Family Activity Monitoring</h2>
          <p className="text-[#49699c] mb-4">
            Start tracking your family's activities, managing schedules, and organizing events.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 border border-gray-200 rounded-lg">
              <h3 className="font-medium text-[#0d131c]">Activities</h3>
              <p className="text-sm text-[#49699c]">Track daily activities</p>
            </div>
            <div className="p-4 border border-gray-200 rounded-lg">
              <h3 className="font-medium text-[#0d131c]">Schedules</h3>
              <p className="text-sm text-[#49699c]">Manage recurring events</p>
            </div>
            <div className="p-4 border border-gray-200 rounded-lg">
              <h3 className="font-medium text-[#0d131c]">Events</h3>
              <p className="text-sm text-[#49699c]">Organize special occasions</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;