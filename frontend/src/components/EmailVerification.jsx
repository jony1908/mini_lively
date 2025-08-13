import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import apiClient from '../services/client';

const EmailVerification = () => {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState('verifying'); // 'verifying', 'success', 'error'
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = searchParams.get('token');
    
    if (!token) {
      setStatus('error');
      setMessage('Invalid verification link. No token provided.');
      return;
    }

    verifyEmail(token);
  }, [searchParams]);

  const verifyEmail = async (token) => {
    try {
      const response = await apiClient.post('/auth/verify-email', null, {
        params: { token }
      });
      
      setStatus('success');
      setMessage(response.data.message || 'Email verified successfully!');
      
      // Redirect to login after 3 seconds
      setTimeout(() => {
        navigate('/login');
      }, 3000);
      
    } catch (error) {
      setStatus('error');
      setMessage(
        error.response?.data?.detail || 
        'Failed to verify email. The link may be expired or invalid.'
      );
    }
  };

  const handleResendVerification = async () => {
    try {
      await apiClient.post('/auth/resend-verification');
      setMessage('Verification email sent! Please check your inbox.');
    } catch (error) {
      setMessage(
        error.response?.data?.detail || 
        'Failed to resend verification email.'
      );
    }
  };

  return (
    <div 
      className="relative flex size-full min-h-screen flex-col bg-[#f8f9fc] justify-center items-center overflow-x-hidden"
      style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}
    >
      <div className="max-w-md w-full bg-white rounded-xl shadow-sm p-8 text-center">
        {status === 'verifying' && (
          <>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#2071f3] mx-auto mb-4"></div>
            <h2 className="text-xl font-bold text-[#0d131c] mb-4">Verifying Email...</h2>
            <p className="text-[#49699c]">Please wait while we verify your email address.</p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h2 className="text-xl font-bold text-[#0d131c] mb-4">Email Verified!</h2>
            <p className="text-[#49699c] mb-4">{message}</p>
            <p className="text-sm text-[#49699c]">Redirecting to login page...</p>
          </>
        )}

        {status === 'error' && (
          <>
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </div>
            <h2 className="text-xl font-bold text-[#0d131c] mb-4">Verification Failed</h2>
            <p className="text-[#49699c] mb-6">{message}</p>
            
            <div className="space-y-3">
              <button
                onClick={handleResendVerification}
                className="w-full px-4 py-2 bg-[#2071f3] text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
              >
                Resend Verification Email
              </button>
              
              <button
                onClick={() => navigate('/login')}
                className="w-full px-4 py-2 bg-[#e7ecf4] text-[#0d131c] rounded-lg font-medium hover:bg-gray-200 transition-colors"
              >
                Back to Login
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default EmailVerification;