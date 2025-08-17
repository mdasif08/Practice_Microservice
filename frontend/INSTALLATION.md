# Commit Trail Frontend Installation Guide

## Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Git

### Installation Steps

1. **Navigate to the frontend directory:**
   ```bash
   cd craftnudge-ai-agent/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

## Alternative Setup Methods

### Using Setup Scripts

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Manual Setup

If you prefer to set up manually:

1. **Check Node.js version:**
   ```bash
   node --version  # Should be 18+
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Verify installation:**
   ```bash
   npm run build  # Should complete without errors
   ```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Backend Integration

The frontend is configured to communicate with the CraftNudge AI Agent backend running on `http://localhost:8000`. Make sure the backend is running before using the frontend.

### Environment Variables

No environment variables are required for basic development. The API proxy is configured in `vite.config.ts`.

## Troubleshooting

### Common Issues

1. **Node.js version too old:**
   - Install Node.js 18+ from [nodejs.org](https://nodejs.org/)

2. **Port 3000 already in use:**
   - Change the port in `vite.config.ts` or kill the process using port 3000

3. **Backend connection issues:**
   - Ensure the CraftNudge AI Agent backend is running on port 8000
   - Check the API proxy configuration in `vite.config.ts`

4. **Build errors:**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`

### Getting Help

- Check the main README.md for more information
- Review the component documentation in the source code
- Ensure all dependencies are properly installed

## Features

The frontend includes:

- ✅ Real-time commit tracking interface
- ✅ Local commit fetching
- ✅ Live statistics display
- ✅ Modern dark theme UI
- ✅ Responsive design
- ✅ TypeScript support
- ✅ API integration ready
- ✅ Loading states and error handling

## Next Steps

After installation:

1. Start the backend server (if not already running)
2. Open the frontend in your browser
3. Click "Fetch Local Commits" to load your repository data
4. Use "Start Tracking" to begin real-time monitoring
5. Explore the analytics features

Enjoy using Commit Trail! 🚀
