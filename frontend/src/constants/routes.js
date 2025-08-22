// Route constants for the application
export const ROUTES = {
  // Public routes
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  VERIFY_EMAIL: '/verify-email',
  AUTH_CALLBACK: '/auth/callback',
  
  // Protected routes
  DASHBOARD: '/dashboard',
  
  // Profile routes
  PROFILE: '/profile',
  PROFILE_EDIT: '/profile/edit',
  
  // Members routes
  MEMBERS: '/members',
  MEMBERS_ADD: '/members/add',
  MEMBER_DETAIL: '/members/:memberId',
  MEMBER_EDIT: '/members/edit/:memberId',
};

// Helper functions for dynamic routes
export const getRoutes = {
  memberDetail: (memberId) => `/members/${memberId}`,
  memberEdit: (memberId) => `/members/edit/${memberId}`,
};