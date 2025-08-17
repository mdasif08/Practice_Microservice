import { AlertCircle, Download } from 'lucide-react'

interface NoCommitsFoundProps {
  onFetchLocal: () => void
}

const NoCommitsFound = ({ onFetchLocal }: NoCommitsFoundProps) => {
  return (
    <div className="card flex flex-col items-center justify-center py-16">
      <div className="text-center space-y-6">
        <div className="flex justify-center">
          <div className="w-16 h-16 bg-gray-600 rounded-full flex items-center justify-center">
            <AlertCircle size={32} className="text-white" />
          </div>
        </div>
        
        <div>
          <h3 className="text-2xl font-bold text-white mb-2">
            No Commits Found
          </h3>
          <p className="text-gray-400 text-lg">
            Start tracking or fetch local commits to see them here.
          </p>
        </div>
        
        <button 
          onClick={onFetchLocal}
          className="btn-primary flex items-center space-x-2 px-6 py-3 text-lg"
        >
          <Download size={20} />
          <span>Fetch Local Commits</span>
        </button>
      </div>
    </div>
  )
}

export default NoCommitsFound
