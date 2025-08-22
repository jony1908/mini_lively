import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ROUTES } from '../constants/routes';

// Layout components
import ProtectedRoute from '../components/ProtectedRoute';
import AuthGuard from '../components/AuthGuard';

// Page components
import LandingPage from '../pages/LandingPage';
import Login from '../components/Login';
import Register from '../components/Register';
import EmailVerification from '../components/EmailVerification';
import AuthCallback from '../components/AuthCallback';
import Dashboard from '../components/Dashboard';

// Profile components
import { ProfileForm, ProfileView } from '../pages/Profile';

// Member components
import ChildrenList from '../components/Children/ChildrenList';
import AddChildForm from '../components/Children/AddChildForm';
import ChildProfileView from '../components/Children/ChildProfileView';
import EditChildForm from '../components/Children/EditChildForm';

// Public routes configuration
const publicRoutes = [
  {
    path: ROUTES.HOME,
    element: <LandingPage />,
  },
  {
    path: ROUTES.VERIFY_EMAIL,
    element: <EmailVerification />,
  },
  {
    path: ROUTES.AUTH_CALLBACK,
    element: <AuthCallback />,
  },
];

// Auth routes (redirects to dashboard if already authenticated)
const authRoutes = [
  {
    path: ROUTES.LOGIN,
    element: <Login />,
  },
  {
    path: ROUTES.REGISTER,
    element: <Register />,
  },
];

// Protected routes configuration
const protectedRoutes = [
  {
    path: ROUTES.DASHBOARD,
    element: <Dashboard />,
  },
  {
    path: ROUTES.PROFILE,
    element: <ProfileView />,
  },
  {
    path: ROUTES.PROFILE_EDIT,
    element: <ProfileForm />,
  },
  {
    path: ROUTES.MEMBERS,
    element: <ChildrenList />,
  },
  {
    path: ROUTES.MEMBERS_ADD,
    element: <AddChildForm />,
  },
  {
    path: ROUTES.MEMBER_DETAIL,
    element: <ChildProfileView />,
  },
  {
    path: ROUTES.MEMBER_EDIT,
    element: <EditChildForm />,
  },
];

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public routes */}
      {publicRoutes.map((route) => (
        <Route
          key={route.path}
          path={route.path}
          element={route.element}
        />
      ))}

      {/* Auth routes with AuthGuard */}
      {authRoutes.map((route) => (
        <Route
          key={route.path}
          path={route.path}
          element={<AuthGuard>{route.element}</AuthGuard>}
        />
      ))}

      {/* Protected routes */}
      {protectedRoutes.map((route) => (
        <Route
          key={route.path}
          path={route.path}
          element={<ProtectedRoute>{route.element}</ProtectedRoute>}
        />
      ))}

      {/* Catch all route */}
      <Route path="*" element={<Navigate to={ROUTES.HOME} replace />} />
    </Routes>
  );
};

export default AppRoutes;