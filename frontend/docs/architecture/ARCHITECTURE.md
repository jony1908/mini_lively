# ARCHITECTURE.md

## Project Overview
A react mobile first for family activity monitoring platform that allows parents and guardians to track their children's daily activities, manage schedules for recurring activities (like hockey, art, soccer classes), and organize events (like birthday parties).

## Architecture

This is a React frontend application built with Vite as the build tool and development server.

**Entry Point**: `src/main.jsx` renders the root `App` component into the DOM element with id "root"

**Build System**: Vite with React plugin for fast development and optimized production builds

**Styling**: CSS modules approach with component-specific CSS files (`App.css`) and global styles (`index.css`)

The application uses React 19 with modern patterns including hooks (useState) and follows the standard Vite + React project structure.

Folder Structure:

assets/:Static assets that are imported into components and processed by Vite (e.g., images, SVG icons, fonts).

components/: Reusable UI components that are independent of specific features or pages (e.g., Button, Modal, Card).

features/: Contains domain-specific features, each with its own components, hooks, state management, and API calls (e.g., Auth, UserProfile, ProductList).

pages/:Route-level components that represent distinct pages in your application and compose features and components (e.g., HomePage, LoginPage, DashboardPage).

hooks/:Custom React hooks for encapsulating reusable logic (e.g., useAuth, useFormValidation).

utils/:Pure utility functions that perform common tasks and are not tied to specific components or features (e.g., formatDate, debounce).

services/:Files related to interacting with external APIs or services (e.g., api.js, authService.js).

store/:If using a global state management library like Redux or Zustand, this directory would contain related files (e.g., reducers, actions, slices).