import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const Register = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  
  const { register, loading, error } = useAuth();
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
    
    if (!formData.first_name.trim()) {
      errors.first_name = 'First name is required';
    }
    
    if (!formData.last_name.trim()) {
      errors.last_name = 'Last name is required';
    }
    
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }
    
    try {
      const registrationData = {
        first_name: formData.first_name,
        last_name: formData.last_name,
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
      className="relative flex size-full min-h-screen flex-col bg-[#f8f9fc] justify-between group/design-root overflow-x-hidden"
      style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}
    >
      <div>
        <div className="flex items-center bg-[#f8f9fc] p-4 pb-2 justify-between">
          <div 
            className="text-[#0d131c] flex size-12 shrink-0 items-center cursor-pointer" 
            onClick={() => navigate('/login')}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
              <path d="M224,128a8,8,0,0,1-8,8H59.31l58.35,58.34a8,8,0,0,1-11.32,11.32l-72-72a8,8,0,0,1,0-11.32l72-72a8,8,0,0,1,11.32,11.32L59.31,120H216A8,8,0,0,1,224,128Z"></path>
            </svg>
          </div>
          <h2 className="text-[#0d131c] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">
            Create Account
          </h2>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="text"
                name="first_name"
                placeholder="First Name"
                value={formData.first_name}
                onChange={handleInputChange}
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d131c] focus:outline-0 focus:ring-0 border-none bg-[#e7ecf4] focus:border-none h-14 placeholder:text-[#49699c] p-4 text-base font-normal leading-normal"
              />
              {formErrors.first_name && (
                <span className="text-red-500 text-xs mt-1 px-4">{formErrors.first_name}</span>
              )}
            </label>
          </div>

          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="text"
                name="last_name"
                placeholder="Last Name"
                value={formData.last_name}
                onChange={handleInputChange}
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d131c] focus:outline-0 focus:ring-0 border-none bg-[#e7ecf4] focus:border-none h-14 placeholder:text-[#49699c] p-4 text-base font-normal leading-normal"
              />
              {formErrors.last_name && (
                <span className="text-red-500 text-xs mt-1 px-4">{formErrors.last_name}</span>
              )}
            </label>
          </div>

          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type="email"
                name="email"
                placeholder="Email Address"
                value={formData.email}
                onChange={handleInputChange}
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d131c] focus:outline-0 focus:ring-0 border-none bg-[#e7ecf4] focus:border-none h-14 placeholder:text-[#49699c] p-4 text-base font-normal leading-normal"
              />
              {formErrors.email && (
                <span className="text-red-500 text-xs mt-1 px-4">{formErrors.email}</span>
              )}
            </label>
          </div>

          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleInputChange}
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d131c] focus:outline-0 focus:ring-0 border-none bg-[#e7ecf4] focus:border-none h-14 placeholder:text-[#49699c] p-4 text-base font-normal leading-normal"
              />
              {formErrors.password && (
                <span className="text-red-500 text-xs mt-1 px-4">{formErrors.password}</span>
              )}
            </label>
          </div>

          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <input
                type={showPassword ? "text" : "password"}
                name="confirmPassword"
                placeholder="Confirm Password"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d131c] focus:outline-0 focus:ring-0 border-none bg-[#e7ecf4] focus:border-none h-14 placeholder:text-[#49699c] p-4 text-base font-normal leading-normal"
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

          <div className="flex justify-center">
            <div className="flex flex-1 gap-3 max-w-[480px] flex-col items-stretch px-4 py-3">
              <button
                type="submit"
                disabled={loading}
                className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 bg-[#2071f3] text-[#f8f9fc] text-base font-bold leading-normal tracking-[0.015em] w-full disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span className="truncate">
                  {loading ? 'Creating Account...' : 'Create Account'}
                </span>
              </button>
              <button
                type="button"
                onClick={() => navigate('/add-child')}
                className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 bg-[#e7ecf4] text-[#0d131c] text-base font-bold leading-normal tracking-[0.015em] w-full"
              >
                <span className="truncate">Add a Child</span>
              </button>
            </div>
          </div>
        </form>

        <div className="flex justify-center px-4 py-3">
          <p className="text-[#49699c] text-sm">
            Already have an account? {' '}
            <Link to="/login" className="text-[#2071f3] underline">
              Log In
            </Link>
          </p>
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

export default Register;