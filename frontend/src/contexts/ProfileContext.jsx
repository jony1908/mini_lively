import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { profileAPI } from '../services/profile';
import { useAuth } from './AuthContext';

const ProfileContext = createContext();

// Profile reducer
const profileReducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
      };
    case 'SET_PROFILE':
      return {
        ...state,
        profile: action.payload,
        loading: false,
        error: null,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        loading: false,
      };
    case 'CREATE_PROFILE_START':
      return {
        ...state,
        loading: true,
        error: null,
      };
    case 'CREATE_PROFILE_SUCCESS':
      return {
        ...state,
        profile: action.payload,
        loading: false,
        error: null,
      };
    case 'UPDATE_PROFILE_START':
      return {
        ...state,
        loading: true,
        error: null,
      };
    case 'UPDATE_PROFILE_SUCCESS':
      return {
        ...state,
        profile: action.payload,
        loading: false,
        error: null,
      };
    case 'CLEAR_PROFILE':
      return {
        ...state,
        profile: null,
        error: null,
      };
    default:
      return state;
  }
};

// Initial state
const initialState = {
  profile: null,
  loading: false,
  error: null,
};

export const ProfileProvider = ({ children }) => {
  const [state, dispatch] = useReducer(profileReducer, initialState);
  const { isAuthenticated, user } = useAuth();

  // Load profile when user is authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      loadProfile();
    } else {
      dispatch({ type: 'CLEAR_PROFILE' });
    }
  }, [isAuthenticated, user]);

  // Load current user's profile
  const loadProfile = async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    
    try {
      const profile = await profileAPI.getCurrentProfile();
      dispatch({ type: 'SET_PROFILE', payload: profile });
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to load profile';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
    }
  };

  // Create new profile
  const createProfile = async (profileData) => {
    dispatch({ type: 'CREATE_PROFILE_START' });
    
    try {
      const newProfile = await profileAPI.createProfile(profileData);
      dispatch({ type: 'CREATE_PROFILE_SUCCESS', payload: newProfile });
      return newProfile;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to create profile';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      throw error;
    }
  };

  // Update existing profile
  const updateProfile = async (profileData) => {
    dispatch({ type: 'UPDATE_PROFILE_START' });
    
    try {
      const updatedProfile = await profileAPI.updateProfile(profileData);
      dispatch({ type: 'UPDATE_PROFILE_SUCCESS', payload: updatedProfile });
      return updatedProfile;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to update profile';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      throw error;
    }
  };

  // Delete profile
  const deleteProfile = async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    
    try {
      await profileAPI.deleteProfile();
      dispatch({ type: 'SET_PROFILE', payload: null });
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to delete profile';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      throw error;
    }
  };

  // Upload profile picture
  const uploadProfilePicture = async (file) => {
    try {
      const result = await profileAPI.uploadProfilePicture(file);
      return result;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to upload profile picture';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      throw error;
    }
  };

  // Check if profile is complete
  const isProfileComplete = () => {
    if (!state.profile) return false;
    
    // Define required fields based on the design
    const requiredFields = ['city', 'state', 'postal_code'];
    return requiredFields.every(field => state.profile[field]);
  };

  // Get profile completion percentage
  const getProfileCompletionPercentage = () => {
    if (!state.profile) return 0;
    
    const allFields = [
      'phone_number',
      'address',
      'city', 
      'state', 
      'postal_code', 
      'country',
      'timezone',
      'profile_picture_url'
    ];
    
    const completedFields = allFields.filter(field => state.profile[field]);
    return Math.round((completedFields.length / allFields.length) * 100);
  };

  const value = {
    ...state,
    loadProfile,
    createProfile,
    updateProfile,
    deleteProfile,
    uploadProfilePicture,
    isProfileComplete,
    getProfileCompletionPercentage,
  };

  return (
    <ProfileContext.Provider value={value}>
      {children}
    </ProfileContext.Provider>
  );
};

// Custom hook to use profile context
export const useProfile = () => {
  const context = useContext(ProfileContext);
  if (!context) {
    throw new Error('useProfile must be used within a ProfileProvider');
  }
  return context;
};

export default ProfileContext;