import { Github, BarChart3 } from 'lucide-react'

interface HeaderProps {
  isConnected: boolean
}

const Header = ({ isConnected }: HeaderProps) => {
  return (
    <header className="flex justify-between items-start">
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Commit Trail</h1>
        <p className="text-gray-400 text-lg">
          Track and visualize your git commits in real-time
        </p>
      </div>
      
      <div className="flex items-center space-x-3">
        <button className="btn-secondary flex items-center space-x-2">
          <Github size={20} />
          <span>GitHub</span>
        </button>
        
        <button 
          className={`flex items-center space-x-2 px-3 py-2 rounded-lg font-medium ${
            isConnected 
              ? 'bg-green-600 hover:bg-green-700 text-white' 
              : 'bg-red-600 hover:bg-red-700 text-white'
          }`}
        >
          <BarChart3 size={16} />
          <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
        </button>
      </div>
    </header>
  )
}

export default Header
