/**
 * ChildrenList Component
 * 
 * Main children management interface:
 * - Displays all children in card format
 * - Add new child button
 * - Edit and delete functionality
 * - Empty state for no children
 */

import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import ChildCard from './ChildCard';
import childAPI from '../../services/child';

const ChildrenList = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [children, setChildren] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Load children on component mount
  useEffect(() => {
    loadChildren();
    
    // Check for success message from navigation state
    if (location.state?.message) {
      setSuccessMessage(location.state.message);
      // Clear the message from navigation state
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location.state, navigate]);

  // Clear success message after 5 seconds
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => {
        setSuccessMessage('');
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  const loadChildren = async () => {
    try {
      setLoading(true);
      setError('');
      const childrenData = await childAPI.getChildren();
      setChildren(childrenData);
    } catch (err) {
      console.error('Failed to load children:', err);
      setError('Failed to load children. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddChild = () => {
    navigate('/children/add');
  };

  const handleEditChild = (childId) => {
    navigate(`/children/edit/${childId}`);
  };

  const handleDeleteChild = async (childId) => {
    try {
      await childAPI.deleteChild(childId);
      setSuccessMessage('Child removed successfully');
      loadChildren(); // Reload the list
    } catch (err) {
      console.error('Failed to delete child:', err);
      setError('Failed to remove child. Please try again.');
    }
  };

  const handleBack = () => {
    navigate('/dashboard');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#fcfbf8] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#fac638] mx-auto"></div>
          <p className="mt-4 text-[#9e8747]">Loading children...</p>
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
          My Children
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

        {/* Add Child Button */}
        <div className="mb-6">
          <button
            onClick={handleAddChild}
            className="flex items-center gap-2 bg-[#fac638] text-[#1c180d] px-6 py-3 rounded-xl font-medium hover:bg-[#e9b429] transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256">
              <path d="M224,128a8,8,0,0,1-8,8H136v80a8,8,0,0,1-16,0V136H40a8,8,0,0,1,0-16h80V40a8,8,0,0,1,16,0v80h80A8,8,0,0,1,224,128Z"></path>
            </svg>
            Add New Child
          </button>
        </div>

        {/* Children Grid */}
        {children.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {children.map((child) => (
              <ChildCard
                key={child.id}
                child={child}
                onEdit={handleEditChild}
                onDelete={handleDeleteChild}
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
            <h3 className="text-[#1c180d] text-xl font-bold mb-2">No Children Added Yet</h3>
            <p className="text-[#9e8747] mb-6 max-w-md mx-auto">
              Start by adding your first child to track their activities and manage their schedules.
            </p>
            <button
              onClick={handleAddChild}
              className="bg-[#fac638] text-[#1c180d] px-8 py-3 rounded-xl font-medium hover:bg-[#e9b429] transition-colors"
            >
              Add Your First Child
            </button>
          </div>
        )}

        {/* Statistics */}
        {children.length > 0 && (
          <div className="mt-8 bg-[#f4f0e6] rounded-xl p-6">
            <h3 className="text-[#1c180d] text-lg font-bold mb-4">Summary</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-[#fac638]">{children.length}</div>
                <div className="text-[#9e8747] text-sm">
                  {children.length === 1 ? 'Child' : 'Children'}
                </div>
              </div>
              <div>
                <div className="text-2xl font-bold text-[#fac638]">
                  {Math.round(children.reduce((sum, child) => sum + child.age, 0) / children.length) || 0}
                </div>
                <div className="text-[#9e8747] text-sm">Avg Age</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-[#fac638]">
                  {children.reduce((sum, child) => sum + (child.interests?.length || 0), 0)}
                </div>
                <div className="text-[#9e8747] text-sm">Total Interests</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-[#fac638]">
                  {children.reduce((sum, child) => sum + (child.skills?.length || 0), 0)}
                </div>
                <div className="text-[#9e8747] text-sm">Total Skills</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChildrenList;