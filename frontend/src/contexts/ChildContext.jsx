/**
 * Child Context
 * 
 * Global state management for children:
 * - CRUD operations with loading states
 * - Error handling
 * - Integration with auth context
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import childAPI from '../services/child';
import { useAuth } from './AuthContext';

const ChildContext = createContext();

export const useChild = () => {
  const context = useContext(ChildContext);
  if (!context) {
    throw new Error('useChild must be used within a ChildProvider');
  }
  return context;
};

export const ChildProvider = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [childrenList, setChildrenList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [options, setOptions] = useState({ interests: [], skills: [] });

  // Load children when user is authenticated
  useEffect(() => {
    if (isAuthenticated) {
      loadChildren();
      loadOptions();
    } else {
      // Clear data when user logs out
      setChildrenList([]);
      setOptions({ interests: [], skills: [] });
      setError('');
    }
  }, [isAuthenticated]);

  // Load all children
  const loadChildren = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await childAPI.getChildren();
      setChildrenList(data);
    } catch (err) {
      console.error('Failed to load children:', err);
      setError('Failed to load children');
    } finally {
      setLoading(false);
    }
  };

  // Load options for interests and skills
  const loadOptions = async () => {
    try {
      const optionsData = await childAPI.getChildOptions();
      setOptions(optionsData);
    } catch (err) {
      console.error('Failed to load options:', err);
      // Don't set error for options as it's not critical
    }
  };

  // Get a specific child by ID
  const getChild = async (childId) => {
    try {
      setError('');
      const child = await childAPI.getChild(childId);
      return child;
    } catch (err) {
      console.error('Failed to get child:', err);
      setError('Failed to load child information');
      throw err;
    }
  };

  // Create a new child
  const createChild = async (childData) => {
    try {
      setError('');
      const newChild = await childAPI.createChild(childData);
      setChildrenList(prev => [newChild, ...prev]);
      return newChild;
    } catch (err) {
      console.error('Failed to create child:', err);
      setError('Failed to add child');
      throw err;
    }
  };

  // Update a child
  const updateChild = async (childId, updateData) => {
    try {
      setError('');
      const updatedChild = await childAPI.updateChild(childId, updateData);
      setChildrenList(prev => 
        prev.map(child => child.id === childId ? updatedChild : child)
      );
      return updatedChild;
    } catch (err) {
      console.error('Failed to update child:', err);
      setError('Failed to update child');
      throw err;
    }
  };

  // Delete a child
  const deleteChild = async (childId) => {
    try {
      setError('');
      await childAPI.deleteChild(childId);
      setChildrenList(prev => prev.filter(child => child.id !== childId));
    } catch (err) {
      console.error('Failed to delete child:', err);
      setError('Failed to remove child');
      throw err;
    }
  };

  // Get children count
  const getChildrenCount = () => {
    return childrenList.length;
  };

  // Get children statistics
  const getChildrenStats = () => {
    if (childrenList.length === 0) {
      return {
        totalChildren: 0,
        averageAge: 0,
        totalInterests: 0,
        totalSkills: 0
      };
    }

    const totalInterests = childrenList.reduce(
      (sum, child) => sum + (child.interests?.length || 0), 
      0
    );
    
    const totalSkills = childrenList.reduce(
      (sum, child) => sum + (child.skills?.length || 0), 
      0
    );

    const averageAge = Math.round(
      childrenList.reduce((sum, child) => sum + child.age, 0) / childrenList.length
    );

    return {
      totalChildren: childrenList.length,
      averageAge,
      totalInterests,
      totalSkills
    };
  };

  // Get all unique interests from all children
  const getAllInterests = () => {
    const allInterests = new Set();
    childrenList.forEach(child => {
      if (child.interests) {
        child.interests.forEach(interest => allInterests.add(interest));
      }
    });
    return Array.from(allInterests).sort();
  };

  // Get all unique skills from all children
  const getAllSkills = () => {
    const allSkills = new Set();
    childrenList.forEach(child => {
      if (child.skills) {
        child.skills.forEach(skill => allSkills.add(skill));
      }
    });
    return Array.from(allSkills).sort();
  };

  // Clear error
  const clearError = () => {
    setError('');
  };

  // Refresh children list
  const refreshChildren = () => {
    return loadChildren();
  };

  const value = {
    // State
    children: childrenList,
    loading,
    error,
    options,

    // Actions
    loadChildren,
    getChild,
    createChild,
    updateChild,
    deleteChild,
    refreshChildren,
    clearError,

    // Computed values
    getChildrenCount,
    getChildrenStats,
    getAllInterests,
    getAllSkills
  };

  return (
    <ChildContext.Provider value={value}>
      {children}
    </ChildContext.Provider>
  );
};