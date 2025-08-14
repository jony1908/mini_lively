# Frontend Architecture

## Overview
A React mobile-first frontend for the Mini Lively family activity monitoring platform that allows parents and guardians to track their children's daily activities, manage schedules for recurring activities (like hockey, art, soccer classes), and organize events (like birthday parties).

## Technology Stack
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **Routing**: React Router
- **HTTP Client**: Axios
- **Authentication**: JWT tokens

## Application Architecture

### Entry Point
- **Main File**: `src/main.jsx` renders the root `App` component into the DOM element with id "root"
- **Build System**: Vite with React plugin for fast development and optimized production builds
- **Styling Approach**: Tailwind CSS utility classes with component-specific styles

### Project Structure
```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   │   ├── Dashboard.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── EmailVerification.jsx
│   │   └── ProtectedRoute.jsx
│   ├── contexts/       # React Context providers
│   │   └── AuthContext.jsx
│   ├── services/       # API service layer
│   │   ├── auth.js
│   │   └── client.js
│   ├── features/       # Feature-specific components
│   ├── hooks/          # Custom React hooks
│   ├── pages/          # Page components
│   ├── store/          # State management
│   ├── utils/          # Utility functions
│   ├── assets/         # Static assets
│   └── main.jsx        # Application entry point
├── design/             # HTML design prototypes
├── dist/               # Build output
├── index.html          # HTML template
├── package.json        # Dependencies and scripts
├── tailwind.config.js  # Tailwind CSS configuration
└── vite.config.js      # Vite configuration
```

## Directory Structure Details

### `/src/assets/`
Static assets that are imported into components and processed by Vite (e.g., images, SVG icons, fonts).

### `/src/components/`
Reusable UI components that are independent of specific features or pages:
- **Dashboard.jsx**: Main dashboard interface
- **Login.jsx**: User login form
- **Register.jsx**: User registration form  
- **EmailVerification.jsx**: Email verification component
- **ProtectedRoute.jsx**: Route protection wrapper

### `/src/contexts/`
React Context providers for global state management:
- **AuthContext.jsx**: Authentication state and methods

### `/src/services/`
Files related to interacting with external APIs or services:
- **auth.js**: Authentication service methods
- **client.js**: HTTP client configuration

### `/src/features/`
Contains domain-specific features, each with its own components, hooks, state management, and API calls (e.g., Auth, UserProfile, ActivityTracking).

### `/src/pages/`
Route-level components that represent distinct pages in the application and compose features and components (e.g., HomePage, LoginPage, DashboardPage).

### `/src/hooks/`
Custom React hooks for encapsulating reusable logic (e.g., useAuth, useFormValidation).

### `/src/utils/`
Pure utility functions that perform common tasks and are not tied to specific components or features (e.g., formatDate, debounce).

### `/src/store/`
Global state management files. Currently using React Context, but prepared for libraries like Redux or Zustand if needed.

## Authentication Flow
1. JWT token-based authentication
2. Protected routes using ProtectedRoute component
3. Context-based auth state management
4. Automatic token refresh handling
5. Email verification process

## Mobile-First Design
- Responsive design using Tailwind CSS
- Touch-friendly interface elements
- Optimized for various screen sizes
- Progressive enhancement approach