import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  
  const { register, loading, error, loginWithGoogle, loginWithApple } = useAuth();
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear field-specific error when user starts typing
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const errors = {};
    
    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Please enter a valid email';
    }
    
    if (!formData.password) {
      errors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      errors.password = 'Password must be at least 6 characters';
    }
    
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }
    
    return errors;
  };

  const handleGoogleLogin = () => {
    try {
      loginWithGoogle();
    } catch (error) {
      console.error('Google login error:', error);
    }
  };

  const handleAppleLogin = () => {
    try {
      loginWithApple();
    } catch (error) {
      console.error('Apple login error:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }
    
    try {
      const registrationData = {
        email: formData.email,
        password: formData.password,
      };
      
      await register(registrationData);
      navigate('/dashboard'); // Redirect to dashboard after successful registration
    } catch (error) {
      // Error is handled by AuthContext
    }
  };

  return (
    <div 
      className="relative flex size-full min-h-screen flex-col bg-[#fcfbf8] justify-between group/design-root overflow-x-hidden"
      style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}
    >
      <div>
        <div className="flex items-center bg-[#fcfbf8] p-4 pb-2 justify-between">
          <button 
            className="text-[#1c180d] flex size-16 shrink-0 items-center cursor-pointer bg-transparent border-none" 
            onClick={() => navigate('/login')}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path d="M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z"></path>
            </svg>
          </button>
          <h2 className="text-[#1c180d] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">
            Create Account
          </h2>
        </div>

        <button 
          onClick={handleGoogleLogin}
          disabled={loading}
          className="flex items-center gap-4 bg-[#fcfbf8] px-4 min-h-14 w-full hover:bg-[#f4f0e6] active:bg-[#e9e2ce] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <div className="text-[#1c180d] flex items-center justify-center rounded-lg bg-[#f4f0e6] shrink-0 size-10">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path d="M224,128a96,96,0,1,1-21.95-61.09,8,8,0,1,1-12.33,10.18A80,80,0,1,0,207.6,136H128a8,8,0,0,1,0-16h88A8,8,0,0,1,224,128Z"></path>
            </svg>
          </div>
          <p className="text-[#1c180d] text-base font-normal leading-normal flex-1 truncate text-left">Create Account with Gmail</p>
        </button>

        <button 
          onClick={handleAppleLogin}
          disabled={loading}
          className="flex items-center gap-4 bg-[#fcfbf8] px-4 min-h-14 w-full hover:bg-[#f4f0e6] active:bg-[#e9e2ce] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <div className="text-[#1c180d] flex items-center justify-center rounded-lg bg-[#f4f0e6] shrink-0 size-10">
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path d="M223.3,169.59a8.07,8.07,0,0,0-2.8-3.4C203.53,154.53,200,134.64,200,120c0-17.67,13.47-33.06,21.5-40.67a8,8,0,0,0,0-11.62C208.82,55.74,187.82,48,168,48a72.2,72.2,0,0,0-40,12.13,71.56,71.56,0,0,0-90.71,9.09A74.63,74.63,0,0,0,16,123.4a127.06,127.06,0,0,0,40.14,89.73A39.8,39.8,0,0,0,83.59,224h87.68a39.84,39.84,0,0,0,29.12-12.57,125,125,0,0,0,17.82-24.6C225.23,174,224.33,172,223.3,169.59Zm-34.63,30.94a23.76,23.76,0,0,1-17.4,7.47H83.59a23.82,23.82,0,0,1-16.44-6.51A111.14,111.14,0,0,1,32,123A58.5,58.5,0,0,1,48.65,80.47A54.81,54.81,0,0,1,88,64h.78A55.45,55.45,0,0,1,123,76.28a8,8,0,0,0,10,0A55.44,55.44,0,0,1,168,64a70.64,70.64,0,0,1,36,10.35c-13,14.52-20,30.47-20,45.65,0,23.77,7.64,42.73,22.18,55.3A105.82,105.82,0,0,1,188.67,200.53ZM128.23,30A40,40,0,0,1,167,0h1a8,8,0,0,1,0,16h-1a24,24,0,0,0-23.24,18,8,8,0,1,1-15.5-4Z"></path>
            </svg>
          </div>
          <p className="text-[#1c180d] text-base font-normal leading-normal flex-1 truncate text-left">Create Account with Apple</p>
        </button>

        <h2 className="text-[#1c180d] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Or create an account with email</h2>

        <form id="register-form" onSubmit={handleSubmit}>
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <p className="text-[#1c180d] text-base font-medium leading-normal pb-2 text-left">Email Address</p>
              <input
                type="email"
                name="email"
                placeholder="Email Address"
                value={formData.email}
                onChange={handleInputChange}
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal"
              />
              {formErrors.email && (
                <span className="text-red-500 text-xs mt-1 px-4">{formErrors.email}</span>
              )}
            </label>
          </div>

          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <p className="text-[#1c180d] text-base font-medium leading-normal pb-2 text-left">Password</p>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleInputChange}
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal"
              />
              {formErrors.password && (
                <span className="text-red-500 text-xs mt-1 px-4">{formErrors.password}</span>
              )}
            </label>
          </div>

          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <p className="text-[#1c180d] text-base font-medium leading-normal pb-2 text-left">Confirm Password</p>
              <input
                type={showPassword ? "text" : "password"}
                name="confirmPassword"
                placeholder="Confirm Password"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#1c180d] focus:outline-0 focus:ring-0 border-none bg-[#f4f0e6] focus:border-none h-14 placeholder:text-[#9e8747] p-4 text-base font-normal leading-normal"
              />
              {formErrors.confirmPassword && (
                <span className="text-red-500 text-xs mt-1 px-4">{formErrors.confirmPassword}</span>
              )}
            </label>
          </div>

          {error && (
            <div className="px-4 py-2">
              <p className="text-red-500 text-sm">{error}</p>
            </div>
          )}

        </form>
      </div>
      
      <div>
        <div className="flex px-4 py-3">
          <button
            type="submit"
            form="register-form"
            disabled={loading}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 flex-1 bg-[#fac638] text-[#1c180d] text-base font-bold leading-normal tracking-[0.015em] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span className="truncate">
              {loading ? 'Creating Account...' : 'Create Account'}
            </span>
          </button>
        </div>
        <p className="text-[#9e8747] text-sm font-normal leading-normal pb-3 pt-1 px-4 text-center">
          By continuing, you agree to our Terms of Service and Privacy Policy.
        </p>
        <div className="h-5 bg-[#fcfbf8]"></div>
      </div>

    </div>
  );
};

export default Register;