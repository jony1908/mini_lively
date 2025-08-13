import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import EmailVerification from './components/EmailVerification';
import './App.css';

// Landing page component
const LandingPage = () => {
  const { isAuthenticated } = useAuth();
  const [searchValue, setSearchValue] = React.useState('');

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSearchChange = (e) => {
    setSearchValue(e.target.value);
  };

  const handleLogin = () => {
    window.location.href = '/login';
  };

  const handleCreateAccount = () => {
    window.location.href = '/register';
  };

  return (
    <div 
      className="relative flex size-full min-h-screen flex-col bg-[#f8f9fc] justify-between group/design-root overflow-x-hidden"
      style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}
    >
      <div>
        <div className="@container">
          <div className="@[480px]:px-4 @[480px]:py-3">
            <div
              className="w-full bg-center bg-no-repeat bg-cover flex flex-col justify-end overflow-hidden bg-[#f8f9fc] @[480px]:rounded-xl min-h-80"
              style={{ backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAHYR54xdrHUYgscAf4xlPwBYeB7XD8D_AzRamoPjFYvYixUhN0mzZCXDj1uqP41wVx-yvVX3R8Kxfdquo9pK8MpFstmMGcHEPutr6NMsg_6VJSRj1VAbXGsex4OF5v5OFWtxoQdcdLc6-XkwusrGQdRe9tGTue9Q7U5p6cbdvDinAAa9_pYqbWaD9U6IIFH2brnL76Aq8TErLPt9kCHCoJdxfO_WeotrELBRGkhntGgFJ2T31f5EcAsGxkIr1EOmSYaVhQMFCPW4X8")' }}
            ></div>
          </div>
        </div>
        <h2 className="text-[#0d131c] tracking-light text-[28px] font-bold leading-tight px-4 text-center pb-3 pt-5">
          Discover Amazing Activities Near You
        </h2>
        <div className="px-4 py-3">
          <label className="flex flex-col min-w-40 h-12 w-full">
            <div className="flex w-full flex-1 items-stretch rounded-xl h-full">
              <div
                className="text-[#49699c] flex border-none bg-[#e7ecf4] items-center justify-center pl-4 rounded-l-xl border-r-0"
                data-icon="MagnifyingGlass"
                data-size="24px"
                data-weight="regular"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M229.66,218.34l-50.07-50.06a88.11,88.11,0,1,0-11.31,11.31l50.06,50.07a8,8,0,0,0,11.32-11.32ZM40,112a72,72,0,1,1,72,72A72.08,72.08,0,0,1,40,112Z"></path>
                </svg>
              </div>
              <input
                placeholder="Search activities or locations..."
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-[#0d131c] focus:outline-0 focus:ring-0 border-none bg-[#e7ecf4] focus:border-none h-full placeholder:text-[#49699c] px-4 rounded-l-none border-l-0 pl-2 text-base font-normal leading-normal"
                value={searchValue}
                onChange={handleSearchChange}
              />
            </div>
          </label>
        </div>
        <p className="text-[#0d131c] text-base font-normal leading-normal pb-3 pt-1 px-4 text-center">
          Explore a wide range of fun and educational activities for kids in your area. Find the perfect match for your family's interests and schedule.
        </p>
      </div>
      <div>
        <div className="flex px-4 py-3">
          <button
            onClick={handleLogin}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 flex-1 bg-[#e7ecf4] text-[#0d131c] text-base font-bold leading-normal tracking-[0.015em]"
          >
            <span className="truncate">Log In</span>
          </button>
        </div>
        <div className="flex px-4 py-3">
          <button
            onClick={handleCreateAccount}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-12 px-5 flex-1 bg-[#2071f3] text-[#f8f9fc] text-base font-bold leading-normal tracking-[0.015em]"
          >
            <span className="truncate">Create Account</span>
          </button>
        </div>
        <div className="h-5 bg-[#f8f9fc]"></div>
      </div>
    </div>
  );
};

// Auth guard for login/register pages
const AuthGuard = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#f8f9fc]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#2071f3] mx-auto"></div>
          <p className="mt-4 text-[#49699c]">Loading...</p>
        </div>
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Landing page */}
            <Route path="/" element={<LandingPage />} />
            
            {/* Authentication routes */}
            <Route 
              path="/login" 
              element={
                <AuthGuard>
                  <Login />
                </AuthGuard>
              } 
            />
            <Route 
              path="/register" 
              element={
                <AuthGuard>
                  <Register />
                </AuthGuard>
              } 
            />
            <Route path="/verify-email" element={<EmailVerification />} />
            
            {/* Protected routes */}
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;