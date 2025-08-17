import { Play, RefreshCw, Download, BarChart3 } from 'lucide-react'

interface CommitTrackingProps {
  onStartTracking: () => void
  onRefresh: () => void
  onFetchLocal: () => void
  onAnalyze: () => void
  status: 'idle' | 'tracking' | 'fetching' | 'analyzing'
  isLoading: boolean
}

const CommitTracking = ({ 
  onStartTracking, 
  onRefresh, 
  onFetchLocal, 
  onAnalyze, 
  status,
  isLoading
}: CommitTrackingProps) => {
  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-white text-center mb-6">
        Commit Tracking
      </h2>
      
      <div className="flex justify-center items-center space-x-4">
        <button 
          onClick={onStartTracking}
          disabled={status === 'tracking' || isLoading}
          className="btn-primary flex items-center space-x-2 px-6 py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Play size={20} />
          <span>Start Tracking</span>
        </button>
        
        <button 
          onClick={onRefresh}
          disabled={status === 'fetching' || isLoading}
          className="btn-secondary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <RefreshCw size={18} />
          <span>Refresh</span>
        </button>
        
        <button 
          onClick={onFetchLocal}
          disabled={status === 'fetching' || isLoading}
          className="btn-secondary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Download size={18} />
          <span>Fetch Local</span>
        </button>
        
        <button 
          onClick={onAnalyze}
          disabled={status === 'analyzing' || isLoading}
          className="btn-secondary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <BarChart3 size={18} />
          <span>Analyze</span>
        </button>
        
        <div className="ml-4">
          <RefreshCw 
            size={20} 
            className={`text-gray-400 ${
              status !== 'idle' || isLoading ? 'animate-spin' : ''
            }`} 
          />
        </div>
      </div>
    </div>
  )
}

export default CommitTracking
