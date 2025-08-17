import { GitBranch, Clock, Activity } from 'lucide-react'

interface StatsPanelProps {
  totalCommits: number
  currentPosition: number
  status: 'idle' | 'tracking' | 'fetching' | 'analyzing'
}

const StatsPanel = ({ totalCommits, currentPosition, status }: StatsPanelProps) => {
  const getStatusText = () => {
    switch (status) {
      case 'tracking':
        return 'Tracking'
      case 'fetching':
        return 'Fetching'
      case 'analyzing':
        return 'Analyzing'
      default:
        return 'Idle'
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="stat-card">
        <div className="p-2 bg-accent-green rounded-lg">
          <GitBranch size={24} className="text-white" />
        </div>
        <div>
          <p className="text-gray-400 text-sm">Total Commits</p>
          <p className="text-2xl font-bold text-white">{totalCommits}</p>
        </div>
      </div>
      
      <div className="stat-card">
        <div className="p-2 bg-accent-green rounded-lg">
          <Clock size={24} className="text-white" />
        </div>
        <div>
          <p className="text-gray-400 text-sm">Current Position</p>
          <p className="text-2xl font-bold text-white">{currentPosition}</p>
        </div>
      </div>
      
      <div className="stat-card">
        <div className="p-2 bg-accent-green rounded-lg">
          <Activity size={24} className="text-white" />
        </div>
        <div>
          <p className="text-gray-400 text-sm">Status</p>
          <p className="text-2xl font-bold text-white">{getStatusText()}</p>
        </div>
      </div>
    </div>
  )
}

export default StatsPanel
