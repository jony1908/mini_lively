import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  
  const { login, loginWithGoogle, loginWithApple, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(formData);
      navigate('/dashboard');
    } catch (error) {
      // Error is handled by AuthContext
    }
  };

  const handleGoogleLogin = () => {
    loginWithGoogle();
  };

  const handleAppleLogin = () => {
    loginWithApple();
  };

  return (
    <div 
      className="relative flex size-full min-h-screen flex-col bg-[#f8f9fc] justify-between group/design-root overflow-x-hidden"
      style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}
    >
      <div>
        <div className="flex items-center bg-[#f8f9fc] p-4 pb-2 justify-between">
          <div 
            className="text-[#0d131c] flex size-12 shrink-0 items-center cursor-pointer" 
            onClick={() => navigate('/')}
            data-icon="ArrowLeft" 
            data-size="24px" 
            data-weight="regular"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path>
            </svg>
          </div>
          <h2 className="text-[#0d131c] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">Log In</h2>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleInputChange}
                required
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d131c] focus:outline-0 focus:ring-0 border-none bg-[#e7ecf4] focus:border-none h-14 placeholder:text-[#49699c] p-4 text-base font-normal leading-normal"
              />
            </label>
          </div>

          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleInputChange}
                required
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d131c] focus:outline-0 focus:ring-0 border-none bg-[#e7ecf4] focus:border-none h-14 placeholder:text-[#49699c] p-4 text-base font-normal leading-normal"
              />
            </label>
          </div>

          <p className="text-[#49699c] text-sm font-normal leading-normal pb-3 pt-1 px-4 underline cursor-pointer">
            Forgot Password?
          </p>

          {error && (
            <div className="px-4 py-2">
              <p className="text-red-500 text-sm">{error}</p>
            </div>
          )}

          <div className="flex px-4 py-3">
            <button
              type="submit"
              disabled={loading}
              className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 flex-1 bg-[#2071f3] text-[#f8f9fc] text-base font-bold leading-normal tracking-[0.015em] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span className="truncate">
                {loading ? 'Logging In...' : 'Log In'}
              </span>
            </button>
          </div>
        </form>

        <div className="flex justify-center">
          <div className="flex flex-1 gap-3 max-w-[480px] flex-col items-stretch px-4 py-3">
            <button
              type="button"
              onClick={handleGoogleLogin}
              className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 bg-[#e7ecf4] text-[#0d131c] text-base font-bold leading-normal tracking-[0.015em] w-full"
            >
              <span className="truncate">Log In with Gmail</span>
            </button>
            <button
              type="button"
              onClick={handleAppleLogin}
              className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 bg-[#e7ecf4] text-[#0d131c] text-base font-bold leading-normal tracking-[0.015em] w-full"
            >
              <span className="truncate">Log In with Apple</span>
            </button>
          </div>
        </div>
      </div>

      <div>
        <div
          className="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-none group-[:not(.dark)]/design-root:hidden"
          style={{ backgroundImage: 'url("/dark.svg")', aspectRatio: '390 / 320' }}
        ></div>
        <div
          className="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-none group-[.dark]/design-root:hidden"
          style={{ backgroundImage: 'url("/light.svg")', aspectRatio: '390 / 320' }}
        ></div>
      </div>
    </div>
  );
};

export default Login;