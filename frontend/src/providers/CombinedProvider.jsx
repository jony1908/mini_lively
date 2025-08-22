import React, { createContext, useContext, useReducer, useEffect, useRef, useState } from 'react';
import { authAPI } from '../services/auth';
import { profileAPI } from '../services/profile';
import memberAPI from '../services/member';

// Combined context for all app state
const AppContext = createContext();

// Combined reducer for all contexts
const appReducer = (state, action) => {
  switch (action.type) {
    // Auth actions
    case 'AUTH_LOGIN_START':
      return {
        ...state,
        auth: {
          ...state.auth,
          loading: true,
          error: null,
        },
      };
    case 'AUTH_LOGIN_SUCCESS':
      return {
        ...state,
        auth: {
          ...state.auth,
          loading: false,
          isAuthenticated: true,
          user: action.payload.user,
          error: null,
        },
      };
    case 'AUTH_LOGIN_FAILURE':
      return {
        ...state,
        auth: {
          ...state.auth,
          loading: false,
          isAuthenticated: false,
          user: null,
          error: action.payload,
        },
      };
    case 'AUTH_LOGOUT':
      return {
        ...state,
        auth: {
          ...state.auth,
          isAuthenticated: false,
          user: null,
          error: null,
        },
        profile: {
          ...state.profile,
          profile: null,
          error: null,
        },
        members: {
          ...state.members,
          membersList: [],
          error: '',
        },
      };
    case 'AUTH_SET_USER':
      return {
        ...state,
        auth: {
          ...state.auth,
          isAuthenticated: true,
          user: action.payload,
        },
      };
    case 'AUTH_SET_LOADING':
      return {
        ...state,
        auth: {
          ...state.auth,
          loading: action.payload,
        },
      };

    // Profile actions
    case 'PROFILE_SET_LOADING':
      return {
        ...state,
        profile: {
          ...state.profile,
          loading: action.payload,
        },
      };
    case 'PROFILE_SET_PROFILE':
      return {
        ...state,
        profile: {
          ...state.profile,
          profile: action.payload,
          loading: false,
          error: null,
        },
      };
    case 'PROFILE_SET_ERROR':
      return {
        ...state,
        profile: {
          ...state.profile,
          error: action.payload,
          loading: false,
        },
      };
    case 'PROFILE_CLEAR':
      return {
        ...state,
        profile: {
          ...state.profile,
          profile: null,
          error: null,
        },
      };

    // Members actions
    case 'MEMBERS_SET_LOADING':
      return {
        ...state,
        members: {
          ...state.members,
          loading: action.payload,
        },
      };
    case 'MEMBERS_SET_LIST':
      return {
        ...state,
        members: {
          ...state.members,
          membersList: action.payload,
          loading: false,
          error: '',
        },
      };
    case 'MEMBERS_SET_ERROR':
      return {
        ...state,
        members: {
          ...state.members,
          error: action.payload,
          loading: false,
        },
      };
    case 'MEMBERS_ADD':
      return {
        ...state,
        members: {
          ...state.members,
          membersList: [action.payload, ...state.members.membersList],
        },
      };
    case 'MEMBERS_UPDATE':
      return {
        ...state,
        members: {
          ...state.members,
          membersList: state.members.membersList.map(member =>
            member.id === action.payload.id ? action.payload : member
          ),
        },
      };
    case 'MEMBERS_DELETE':
      return {
        ...state,
        members: {
          ...state.members,
          membersList: state.members.membersList.filter(member => member.id !== action.payload),
        },
      };
    case 'MEMBERS_SET_OPTIONS':
      return {
        ...state,
        members: {
          ...state.members,
          options: action.payload,
        },
      };
    case 'MEMBERS_CLEAR':
      return {
        ...state,
        members: {
          ...state.members,
          membersList: [],
          options: { interests: [], skills: [] },
          error: '',
        },
      };

    default:
      return state;
  }
};

// Initial combined state
const initialState = {
  auth: {
    isAuthenticated: false,
    user: null,
    loading: true,
    error: null,
  },
  profile: {
    profile: null,
    loading: false,
    error: null,
  },
  members: {
    membersList: [],
    loading: false,
    error: '',
    options: { interests: [], skills: [] },
  },
};

export const CombinedProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);
  const hasCheckedAuth = useRef(false);

  // Auth methods
  const checkAuth = async () => {
    if (hasCheckedAuth.current) return;
    hasCheckedAuth.current = true;

    const token = localStorage.getItem('accessToken');
    
    if (token) {
      try {
        const user = await authAPI.getCurrentUser();
        dispatch({ type: 'AUTH_SET_USER', payload: user });
      } catch (error) {
        if (error.code !== 'ERR_INSUFFICIENT_RESOURCES' && error.response?.status === 401) {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
        }
      }
    }
    
    dispatch({ type: 'AUTH_SET_LOADING', payload: false });
  };

  const login = async (credentials) => {
    dispatch({ type: 'AUTH_LOGIN_START' });
    
    try {
      const response = await authAPI.login(credentials);
      localStorage.setItem('accessToken', response.tokens.access_token);
      localStorage.setItem('refreshToken', response.tokens.refresh_token);
      dispatch({ type: 'AUTH_LOGIN_SUCCESS', payload: response });
      return response;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Login failed';
      dispatch({ type: 'AUTH_LOGIN_FAILURE', payload: errorMessage });
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    dispatch({ type: 'AUTH_LOGOUT' });
  };

  // Profile methods
  const loadProfile = async () => {
    dispatch({ type: 'PROFILE_SET_LOADING', payload: true });
    
    try {
      const profile = await profileAPI.getCurrentProfile();
      dispatch({ type: 'PROFILE_SET_PROFILE', payload: profile });
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to load profile';
      dispatch({ type: 'PROFILE_SET_ERROR', payload: errorMessage });
    }
  };

  // Members methods
  const loadMembers = async () => {
    try {
      dispatch({ type: 'MEMBERS_SET_LOADING', payload: true });
      const data = await memberAPI.getMembers();
      dispatch({ type: 'MEMBERS_SET_LIST', payload: data });
    } catch (err) {
      dispatch({ type: 'MEMBERS_SET_ERROR', payload: 'Failed to load family members' });
    }
  };

  const loadMemberOptions = async () => {
    try {
      const optionsData = await memberAPI.getMemberOptions();
      dispatch({ type: 'MEMBERS_SET_OPTIONS', payload: optionsData });
    } catch (err) {
      console.error('Failed to load options:', err);
    }
  };

  // Auto-load data when authenticated
  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    if (state.auth.isAuthenticated && state.auth.user) {
      loadProfile();
      loadMembers();
      loadMemberOptions();
    } else {
      dispatch({ type: 'PROFILE_CLEAR' });
      dispatch({ type: 'MEMBERS_CLEAR' });
    }
  }, [state.auth.isAuthenticated, state.auth.user]);

  const value = {
    // Auth state and methods
    auth: {
      ...state.auth,
      login,
      logout,
      setUser: (user) => dispatch({ type: 'AUTH_SET_USER', payload: user }),
    },
    // Profile state and methods
    profile: {
      ...state.profile,
      loadProfile,
    },
    // Members state and methods
    members: {
      ...state.members,
      members: state.members.membersList,
      loadMembers,
      createMember: async (memberData) => {
        const newMember = await memberAPI.createMember(memberData);
        dispatch({ type: 'MEMBERS_ADD', payload: newMember });
        return newMember;
      },
      updateMember: async (memberId, updateData) => {
        const updatedMember = await memberAPI.updateMember(memberId, updateData);
        dispatch({ type: 'MEMBERS_UPDATE', payload: updatedMember });
        return updatedMember;
      },
      deleteMember: async (memberId) => {
        await memberAPI.deleteMember(memberId);
        dispatch({ type: 'MEMBERS_DELETE', payload: memberId });
      },
    },
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

// Specialized hooks for different contexts
export const useAuth = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAuth must be used within a CombinedProvider');
  }
  return context.auth;
};

export const useProfile = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useProfile must be used within a CombinedProvider');
  }
  return context.profile;
};

export const useMember = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useMember must be used within a CombinedProvider');
  }
  return context.members;
};