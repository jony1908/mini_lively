# Frontend Development Commands

## Prerequisites
- Node.js (version 16 or higher)
- npm or yarn package manager

## Setup & Installation

### Initial Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Development Commands

### Development Server
```bash
# Start development server with hot module replacement
npm run dev
```
- **Local URL**: `http://localhost:5173`
- **Hot Reload**: Enabled via Vite
- **API Connection**: Connects to backend at `http://localhost:8000`

### Build Commands
```bash
# Build for production
npm run build

# Preview production build locally
npm run preview
```

## Available Scripts

### Core Scripts
- **`npm run dev`** - Start development server with hot module replacement
- **`npm run build`** - Build application for production deployment
- **`npm run preview`** - Preview the production build locally
- **`npm run lint`** - Run ESLint to check code quality (if configured)

### Development Workflow

1. **Start Development**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

2. **Testing Changes**:
   - Make changes to source files
   - Hot reload will automatically update the browser
   - Check console for any errors

3. **Production Build**:
   ```bash
   npm run build
   npm run preview  # Test production build locally
   ```

## Environment Configuration
- Development server runs on `http://localhost:5173`
- API calls are made to backend at `http://localhost:8000`
- Environment variables can be configured in `.env` files

## Build Output
- Production files are generated in the `dist/` directory
- Assets are optimized and minified for production
- Source maps are available for debugging