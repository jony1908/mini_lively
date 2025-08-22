import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import { ProfileProvider } from '../contexts/ProfileContext';
import { MemberProvider } from '../contexts/MemberContext';

// Combined provider component for better organization and reduced nesting
const AppProviders = ({ children }) => {
  return (
    <AuthProvider>
      <ProfileProvider>
        <MemberProvider>
          {children}
        </MemberProvider>
      </ProfileProvider>
    </AuthProvider>
  );
};

export default AppProviders;