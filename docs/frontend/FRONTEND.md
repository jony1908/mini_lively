# Mini Lively Frontend

## Project Overview
A mobile-first React frontend application that connects to the FastAPI backend. The frontend provides a responsive user interface for parents to track children's activities, manage schedules, and organize family events.

## Tech Stack
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **Routing**: React Router
- **HTTP Client**: Axios
- **Authentication**: JWT tokens

## Key Features
- Mobile-first responsive design
- JWT-based authentication flow
- OAuth 2.0 integration (Google & Apple)
- Protected route handling
- Email verification process
- Real-time API integration
- Context-based state management

## Architecture References

### Core Architecture
- **System Architecture**: `./frontend/architecture/ARCHITECTURE.md`

### Development Resources  
- **Development Commands**: `./frontend/development/COMMAND.md`

### Design Resources
- **Design Prototypes**: `frontend/design/`
  - Login interface: `frontend/design/login_account.html`
  - Registration form: `frontend/design/create_account.html`  
  - Public homepage: `frontend/design/public_home_page.html`

## Authentication System

### Login Methods
The application supports multiple authentication methods:

1. **Email/Password Authentication**
   - Traditional form-based login
   - JWT token-based session management
   - Password validation and error handling

2. **OAuth 2.0 Social Login** 
   - Google OAuth integration
   - Apple OAuth integration
   - Seamless redirect flow with callback handling

### Authentication Flow
1. **Login/Register Pages**: Users can choose email/password or OAuth
2. **OAuth Redirect**: Social login redirects to provider authentication
3. **Callback Processing**: `/auth/callback` route handles OAuth tokens
4. **Token Storage**: JWT tokens stored in localStorage
5. **Protected Routes**: Automatic redirection for authenticated users

### Authentication Components
- **Login** (`components/Login.jsx`): Email/password and OAuth login options
- **Register** (`components/Register.jsx`): Account creation with OAuth alternatives
- **AuthCallback** (`components/AuthCallback.jsx`): OAuth callback processing
- **AuthContext** (`contexts/AuthContext.jsx`): Global authentication state management
- **ProtectedRoute** (`components/ProtectedRoute.jsx`): Route protection wrapper

### OAuth Integration Details
- **Google Login**: Redirects to `/auth/google` backend endpoint
- **Apple Login**: Redirects to `/auth/apple` backend endpoint  
- **Callback URL**: `/auth/callback` processes tokens and completes authentication
- **Error Handling**: Comprehensive error states and user feedback
- **Loading States**: Visual feedback during authentication processes

## Important References

For detailed development commands and setup instructions, see the development documentation.
