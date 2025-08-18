import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useProfile } from '../contexts/ProfileContext';
import { useMember } from '../contexts/MemberContext';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const { profile, getProfileCompletionPercentage } = useProfile();
  const { members, getMembersCount, getMembersStats } = useMember();
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

  const handleManageChildren = () => {
    navigate('/members');
  };

  const handleAddChild = () => {
    navigate('/members/add');
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

        {/* Children Management Section */}
        <div className="bg-[#f4f0e6] rounded-xl p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-[#1c180d]">My Children</h2>
            <div className="flex gap-3">
              <button
                onClick={handleManageChildren}
                className="px-4 py-2 bg-[#fcfbf8] text-[#1c180d] rounded-lg hover:bg-white transition-colors font-medium border border-[#e9e2ce]"
              >
                Manage Children
              </button>
              <button
                onClick={handleAddChild}
                className="px-4 py-2 bg-[#fac638] text-[#1c180d] rounded-lg hover:bg-[#e9b429] transition-colors font-medium"
              >
                Add Child
              </button>
            </div>
          </div>

          {members.length > 0 ? (
            <>
              {/* Children Statistics */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                <div className="text-center p-3 bg-[#fcfbf8] rounded-lg">
                  <div className="text-2xl font-bold text-[#fac638]">{getMembersStats().totalMembers}</div>
                  <div className="text-sm text-[#9e8747]">
                    {getMembersStats().totalMembers === 1 ? 'Member' : 'Members'}
                  </div>
                </div>
                <div className="text-center p-3 bg-[#fcfbf8] rounded-lg">
                  <div className="text-2xl font-bold text-[#fac638]">{getMembersStats().averageAge}</div>
                  <div className="text-sm text-[#9e8747]">Avg Age</div>
                </div>
                <div className="text-center p-3 bg-[#fcfbf8] rounded-lg">
                  <div className="text-2xl font-bold text-[#fac638]">{getMembersStats().totalInterests}</div>
                  <div className="text-sm text-[#9e8747]">Interests</div>
                </div>
                <div className="text-center p-3 bg-[#fcfbf8] rounded-lg">
                  <div className="text-2xl font-bold text-[#fac638]">{getMembersStats().totalSkills}</div>
                  <div className="text-sm text-[#9e8747]">Skills</div>
                </div>
              </div>

              {/* Recent Children Preview */}
              <div className="space-y-3">
                <h3 className="text-[#1c180d] font-medium">Recent Children</h3>
                {members.slice(0, 3).map((member) => (
                  <div key={member.id} className="flex items-center gap-3 p-3 bg-[#fcfbf8] rounded-lg">
                    {/* Child Avatar */}
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 rounded-full overflow-hidden bg-[#e9e2ce] border-2 border-[#d1c9b3]">
                        {member.avatar_url ? (
                          <img 
                            src={member.avatar_url} 
                            alt={`${member.first_name} ${member.last_name} avatar`} 
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
                    </div>

                    {/* Child Info */}
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-[#1c180d]">
                        {member.first_name} {member.last_name}
                      </div>
                      <div className="text-sm text-[#9e8747]">
                        {member.age} years old
                        {member.interests && member.interests.length > 0 && (
                          <span className="ml-2">• {member.interests.length} interests</span>
                        )}
                      </div>
                    </div>

                    {/* Gender Badge */}
                    <div className="flex-shrink-0">
                      {member.gender && (
                        <span className="px-2 py-1 bg-[#e9e2ce] rounded text-xs text-[#9e8747]">
                          {member.gender}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
                {members.length > 3 && (
                  <div className="text-center">
                    <button
                      onClick={handleManageChildren}
                      className="text-[#fac638] hover:underline text-sm font-medium"
                    >
                      View all {members.length} members
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            /* Empty State */
            <div className="text-center py-8">
              <div className="mb-4">
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="48" 
                  height="48" 
                  fill="#9e8747" 
                  viewBox="0 0 256 256"
                  className="mx-auto"
                >
                  <path d="M230.92,212c-15.23-26.33-38.7-45.21-66.09-54.16a72,72,0,1,0-73.66,0C63.78,166.78,40.31,185.66,25.08,212a8,8,0,1,0,13.85,8c18.84-32.56,52.14-52,89.07-52s70.23,19.44,89.07,52a8,8,0,1,0,13.85-8ZM72,96a56,56,0,1,1,56,56A56.06,56.06,0,0,1,72,96Z"></path>
                </svg>
              </div>
              <h3 className="text-[#1c180d] font-medium mb-2">No Children Added</h3>
              <p className="text-[#9e8747] text-sm mb-4">
                Start by adding family members to track their activities and manage their schedules.
              </p>
              <button
                onClick={handleAddChild}
                className="px-6 py-2 bg-[#fac638] text-[#1c180d] rounded-lg hover:bg-[#e9b429] transition-colors font-medium"
              >
                Add Your First Child
              </button>
            </div>
          )}
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