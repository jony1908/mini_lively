import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { CombinedProvider } from './providers/CombinedProvider';
import AppRoutes from './routes';
import './App.css';

// Alternative App.jsx using the high-performance CombinedProvider
// To use this version, rename this file to App.jsx and rename the current App.jsx to App.standard.jsx
function App() {
  return (
    <CombinedProvider>
      <Router>
        <div className="App">
          <AppRoutes />
        </div>
      </Router>
    </CombinedProvider>
  );
}

export default App;