/**
 * Member Context
 * 
 * Global state management for family members:
 * - CRUD operations with loading states
 * - Error handling
 * - Integration with auth context
 * - Support for all family member types
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import memberAPI from '../services/member';
import { useAuth } from './AuthContext';

const MemberContext = createContext();

export const useMember = () => {
  const context = useContext(MemberContext);
  if (!context) {
    throw new Error('useMember must be used within a MemberProvider');
  }
  return context;
};

export const MemberProvider = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [membersList, setMembersList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [options, setOptions] = useState({ interests: [], skills: [] });

  // Load members when user is authenticated
  useEffect(() => {
    if (isAuthenticated) {
      loadMembers();
      loadOptions();
    } else {
      // Clear data when user logs out
      setMembersList([]);
      setOptions({ interests: [], skills: [] });
      setError('');
    }
  }, [isAuthenticated]);

  // Load all members
  const loadMembers = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await memberAPI.getMembers();
      setMembersList(data);
    } catch (err) {
      console.error('Failed to load members:', err);
      setError('Failed to load family members');
    } finally {
      setLoading(false);
    }
  };

  // Load options for interests and skills
  const loadOptions = async () => {
    try {
      const optionsData = await memberAPI.getMemberOptions();
      setOptions(optionsData);
    } catch (err) {
      console.error('Failed to load options:', err);
      // Don't set error for options as it's not critical
    }
  };

  // Get a specific member by ID
  const getMember = async (memberId) => {
    try {
      setError('');
      const member = await memberAPI.getMember(memberId);
      return member;
    } catch (err) {
      console.error('Failed to get member:', err);
      setError('Failed to load member information');
      throw err;
    }
  };

  // Create a new member
  const createMember = async (memberData) => {
    try {
      setError('');
      const newMember = await memberAPI.createMember(memberData);
      setMembersList(prev => [newMember, ...prev]);
      return newMember;
    } catch (err) {
      console.error('Failed to create member:', err);
      setError('Failed to add family member');
      throw err;
    }
  };

  // Update a member
  const updateMember = async (memberId, updateData) => {
    try {
      setError('');
      const updatedMember = await memberAPI.updateMember(memberId, updateData);
      setMembersList(prev => 
        prev.map(member => member.id === memberId ? updatedMember : member)
      );
      return updatedMember;
    } catch (err) {
      console.error('Failed to update member:', err);
      setError('Failed to update family member');
      throw err;
    }
  };

  // Delete a member
  const deleteMember = async (memberId) => {
    try {
      setError('');
      await memberAPI.deleteMember(memberId);
      setMembersList(prev => prev.filter(member => member.id !== memberId));
    } catch (err) {
      console.error('Failed to delete member:', err);
      setError('Failed to remove family member');
      throw err;
    }
  };

  // Get members count
  const getMembersCount = () => {
    return membersList.length;
  };

  // Get members statistics
  const getMembersStats = () => {
    if (membersList.length === 0) {
      return {
        totalMembers: 0,
        averageAge: 0,
        totalInterests: 0,
        totalSkills: 0,
        ageGroups: {
          babies: 0,
          toddlers: 0,
          children: 0,
          teens: 0,
          adults: 0,
          seniors: 0
        }
      };
    }

    const totalInterests = membersList.reduce(
      (sum, member) => sum + (member.interests?.length || 0), 
      0
    );
    
    const totalSkills = membersList.reduce(
      (sum, member) => sum + (member.skills?.length || 0), 
      0
    );

    const averageAge = Math.round(
      membersList.reduce((sum, member) => sum + member.age, 0) / membersList.length
    );

    // Count age groups
    const ageGroups = membersList.reduce((groups, member) => {
      const age = member.age;
      if (age < 2) groups.babies++;
      else if (age < 5) groups.toddlers++;
      else if (age < 13) groups.children++;
      else if (age < 20) groups.teens++;
      else if (age < 65) groups.adults++;
      else groups.seniors++;
      return groups;
    }, { babies: 0, toddlers: 0, children: 0, teens: 0, adults: 0, seniors: 0 });

    return {
      totalMembers: membersList.length,
      averageAge,
      totalInterests,
      totalSkills,
      ageGroups
    };
  };

  // Get all unique interests from all members
  const getAllInterests = () => {
    const allInterests = new Set();
    membersList.forEach(member => {
      if (member.interests) {
        member.interests.forEach(interest => allInterests.add(interest));
      }
    });
    return Array.from(allInterests).sort();
  };

  // Get all unique skills from all members
  const getAllSkills = () => {
    const allSkills = new Set();
    membersList.forEach(member => {
      if (member.skills) {
        member.skills.forEach(skill => allSkills.add(skill));
      }
    });
    return Array.from(allSkills).sort();
  };

  // Filter members by age category
  const getMembersByAgeCategory = (category) => {
    return membersList.filter(member => {
      const ageCategory = memberAPI.getAgeCategory(member.age);
      return ageCategory.toLowerCase() === category.toLowerCase();
    });
  };

  // Get members by specific criteria
  const getFilteredMembers = (filters = {}) => {
    return membersList.filter(member => {
      // Age range filter
      if (filters.minAge !== undefined && member.age < filters.minAge) return false;
      if (filters.maxAge !== undefined && member.age > filters.maxAge) return false;
      
      // Gender filter
      if (filters.gender && member.gender !== filters.gender) return false;
      
      // Interest filter
      if (filters.interest && !member.interests?.includes(filters.interest)) return false;
      
      // Skill filter
      if (filters.skill && !member.skills?.includes(filters.skill)) return false;
      
      return true;
    });
  };

  // Clear error
  const clearError = () => {
    setError('');
  };

  // Refresh members list
  const refreshMembers = () => {
    return loadMembers();
  };

  const value = {
    // State
    members: membersList,
    loading,
    error,
    options,

    // Actions
    loadMembers,
    getMember,
    createMember,
    updateMember,
    deleteMember,
    refreshMembers,
    clearError,

    // Computed values
    getMembersCount,
    getMembersStats,
    getAllInterests,
    getAllSkills,
    getMembersByAgeCategory,
    getFilteredMembers,

    // Legacy aliases for backward compatibility
    children: membersList, // For components that still reference 'children'
    getChildrenCount: getMembersCount,
    getChildrenStats: getMembersStats
  };

  return (
    <MemberContext.Provider value={value}>
      {children}
    </MemberContext.Provider>
  );
};