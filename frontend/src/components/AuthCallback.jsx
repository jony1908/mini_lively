import React, { useEffect, useState, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const AuthCallback = () => {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState('processing'); // 'processing', 'success', 'error'
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const { loginWithTokens } = useAuth();
  const hasProcessed = useRef(false);

  useEffect(() => {
    const processOAuthCallback = async () => {
      // Prevent multiple processing
      if (hasProcessed.current) {
        return;
      }
      hasProcessed.current = true;
      
      try {
        const accessToken = searchParams.get('access_token');
        const refreshToken = searchParams.get('refresh_token');
        const tokenType = searchParams.get('token_type');

        if (!accessToken || !refreshToken) {
          setStatus('error');
          setMessage('Missing authentication tokens. Please try logging in again.');
          return;
        }

        // Create tokens object similar to email login
        const tokens = {
          access_token: accessToken,
          refresh_token: refreshToken,
          token_type: tokenType || 'bearer'
        };

        // Use the loginWithTokens function from AuthContext to handle token storage
        await loginWithTokens(tokens);

        setStatus('success');
        setMessage('Successfully signed in with Google!');

        // Redirect to homepage after a brief delay (homepage will redirect to dashboard)
        setTimeout(() => {
          navigate('/');
        }, 1500);

      } catch (error) {
        setStatus('error');
        setMessage('Failed to complete authentication. Please try again.');
      }
    };

    processOAuthCallback();
  }, []);

  return (
    <div 
      className="relative flex size-full min-h-screen flex-col bg-[#f8f9fc] justify-center items-center overflow-x-hidden"
      style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}
    >
      <div className="max-w-md w-full bg-white rounded-xl shadow-sm p-8 text-center">
        {status === 'processing' && (
          <>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#2071f3] mx-auto mb-4"></div>
            <h2 className="text-xl font-bold text-[#0d131c] mb-4">Completing Sign-in...</h2>
            <p className="text-[#49699c]">Please wait while we complete your authentication.</p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h2 className="text-xl font-bold text-[#0d131c] mb-4">Sign-in Successful!</h2>
            <p className="text-[#49699c] mb-4">{message}</p>
            <p className="text-sm text-[#49699c]">Redirecting to dashboard...</p>
          </>
        )}

        {status === 'error' && (
          <>
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </div>
            <h2 className="text-xl font-bold text-[#0d131c] mb-4">Authentication Failed</h2>
            <p className="text-[#49699c] mb-6">{message}</p>
            
            <div className="space-y-3">
              <button
                onClick={() => navigate('/login')}
                className="w-full px-4 py-2 bg-[#2071f3] text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
              >
                Try Again
              </button>
              
              <button
                onClick={() => navigate('/')}
                className="w-full px-4 py-2 bg-[#e7ecf4] text-[#0d131c] rounded-lg font-medium hover:bg-gray-200 transition-colors"
              >
                Back to Home
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default AuthCallback;