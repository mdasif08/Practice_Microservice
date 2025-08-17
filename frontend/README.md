# Commit Trail Frontend

A React + Vite frontend application for the CraftNudge AI Agent that provides a modern, real-time interface for tracking and visualizing Git commits.

## Features

- **Real-time Commit Tracking**: Start, stop, and monitor Git commit tracking
- **Local Commit Fetching**: Fetch and display local repository commits
- **Live Statistics**: View total commits, current position, and tracking status
- **Modern UI**: Dark theme with responsive design
- **GitHub Integration**: Connect to GitHub repositories
- **Analytics**: Analyze commit patterns and trends

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **ESLint** - Code linting

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd craftnudge-ai-agent/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Development

### Project Structure

```
src/
├── components/          # React components
│   ├── Header.tsx      # Application header
│   ├── CommitTracking.tsx # Commit tracking controls
│   ├── StatsPanel.tsx  # Statistics display
│   └── NoCommitsFound.tsx # Empty state
├── services/           # API services
│   └── api.ts         # Backend API integration
├── types/             # TypeScript type definitions
│   └── index.ts       # Common types
├── utils/             # Utility functions
│   └── cn.ts          # Class name utilities
├── App.tsx            # Main application component
├── main.tsx           # Application entry point
└── index.css          # Global styles
```

### API Integration

The frontend communicates with the CraftNudge AI Agent backend through the `/api` proxy configured in `vite.config.ts`. The backend should be running on `http://localhost:8000`.

### Styling

The application uses Tailwind CSS with custom colors defined in `tailwind.config.js`:
- `dark-blue`: Primary background color
- `darker-blue`: Secondary background color  
- `accent-green`: Primary accent color

## Contributing

1. Follow the existing code style and patterns
2. Add TypeScript types for new features
3. Test your changes thoroughly
4. Update documentation as needed

## License

This project is part of the CraftNudge AI Agent and follows the same license terms.
