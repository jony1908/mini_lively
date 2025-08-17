import React, { createContext, useContext, useReducer, useEffect, useRef } from 'react';
import { authAPI } from '../services/auth';

const AuthContext = createContext();

// Auth reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN_START':
      return {
        ...state,
        loading: true,
        error: null,
      };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        loading: false,
        isAuthenticated: true,
        user: action.payload.user,
        error: null,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        loading: false,
        isAuthenticated: false,
        user: null,
        error: action.payload,
      };
    case 'LOGOUT':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        error: null,
      };
    case 'SET_USER':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload,
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
      };
    default:
      return state;
  }
};

// Initial state
const initialState = {
  isAuthenticated: false,
  user: null,
  loading: true,
  error: null,
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);
  const hasCheckedAuth = useRef(false);

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      // Prevent running multiple times
      if (hasCheckedAuth.current) {
        return;
      }
      hasCheckedAuth.current = true;

      const token = localStorage.getItem('accessToken');
      
      if (token) {
        try {
          const user = await authAPI.getCurrentUser();
          dispatch({ type: 'SET_USER', payload: user });
        } catch (error) {
          // Only clear tokens if it's not a network/resource error
          if (error.code !== 'ERR_INSUFFICIENT_RESOURCES' && error.response?.status === 401) {
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
          }
        }
      }
      
      dispatch({ type: 'SET_LOADING', payload: false });
    };

    checkAuth();
  }, []);

  // Login function
  const login = async (credentials) => {
    dispatch({ type: 'LOGIN_START' });
    
    try {
      const response = await authAPI.login(credentials);
      
      // Store tokens
      localStorage.setItem('accessToken', response.tokens.access_token);
      localStorage.setItem('refreshToken', response.tokens.refresh_token);
      
      dispatch({ type: 'LOGIN_SUCCESS', payload: response });
      return response;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Login failed';
      dispatch({ type: 'LOGIN_FAILURE', payload: errorMessage });
      throw error;
    }
  };

  // Register function
  const register = async (userData) => {
    dispatch({ type: 'LOGIN_START' });
    
    try {
      const response = await authAPI.register(userData);
      
      // Store tokens
      localStorage.setItem('accessToken', response.tokens.access_token);
      localStorage.setItem('refreshToken', response.tokens.refresh_token);
      
      dispatch({ type: 'LOGIN_SUCCESS', payload: response });
      return response;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Registration failed';
      dispatch({ type: 'LOGIN_FAILURE', payload: errorMessage });
      throw error;
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    dispatch({ type: 'LOGOUT' });
  };

  // Google OAuth
  const loginWithGoogle = () => {
    authAPI.googleAuth();
  };

  // Apple OAuth
  const loginWithApple = () => {
    authAPI.appleAuth();
  };

  // Handle OAuth tokens directly (for OAuth callback)
  const loginWithTokens = async (tokens) => {
    dispatch({ type: 'LOGIN_START' });
    
    try {
      // Store tokens first
      localStorage.setItem('accessToken', tokens.access_token);
      localStorage.setItem('refreshToken', tokens.refresh_token);
      
      // Get user info immediately for OAuth
      const user = await authAPI.getCurrentUser();
      
      dispatch({ type: 'LOGIN_SUCCESS', payload: { 
        user: user,
        tokens: tokens
      }});
      
      return { user: user, tokens: tokens };
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'OAuth login failed';
      dispatch({ type: 'LOGIN_FAILURE', payload: errorMessage });
      throw error;
    }
  };

  // Update user function
  const setUser = (user) => {
    dispatch({ type: 'SET_USER', payload: user });
  };

  const value = {
    ...state,
    login,
    register,
    logout,
    loginWithGoogle,
    loginWithApple,
    loginWithTokens,
    setUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};