import { useState, useEffect } from 'react'
import Header from './components/Header'
import CommitTracking from './components/CommitTracking'
import StatsPanel from './components/StatsPanel'
import NoCommitsFound from './components/NoCommitsFound'
import { api } from './services/api'
import { Commit, TrackingStatus } from './types'

function App() {
  const [isConnected, setIsConnected] = useState(false)
  const [commits, setCommits] = useState<Commit[]>([])
  const [totalCommits, setTotalCommits] = useState(0)
  const [currentPosition, setCurrentPosition] = useState(0)
  const [status, setStatus] = useState<'idle' | 'tracking' | 'fetching' | 'analyzing'>('idle')
  const [isLoading, setIsLoading] = useState(false)

  // Load initial data
  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    try {
      setIsLoading(true)
      const trackingStatus = await api.getTrackingStatus()
      setTotalCommits(trackingStatus.totalCommits)
      setCurrentPosition(trackingStatus.currentPosition)
      setStatus(trackingStatus.status)
      setIsConnected(trackingStatus.isTracking)
      
      // Load commits if available
      if (trackingStatus.totalCommits > 0) {
        const commitsData = await api.getCommits(10)
        setCommits(commitsData)
      }
    } catch (error) {
      console.error('Failed to load initial data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleStartTracking = async () => {
    try {
      setIsLoading(true)
      await api.startTracking()
      setStatus('tracking')
      setIsConnected(true)
      // Refresh data after starting tracking
      await loadInitialData()
    } catch (error) {
      console.error('Failed to start tracking:', error)
      alert('Failed to start tracking. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleRefresh = async () => {
    try {
      setIsLoading(true)
      setStatus('fetching')
      await loadInitialData()
    } catch (error) {
      console.error('Failed to refresh:', error)
      alert('Failed to refresh data. Please try again.')
    } finally {
      setIsLoading(false)
      setStatus('idle')
    }
  }

  const handleFetchLocal = async () => {
    try {
      setIsLoading(true)
      setStatus('fetching')
      const newCommits = await api.fetchLocalCommits()
      setCommits(newCommits)
      setTotalCommits(newCommits.length)
      setCurrentPosition(newCommits.length)
    } catch (error) {
      console.error('Failed to fetch local commits:', error)
      alert('Failed to fetch local commits. Please try again.')
    } finally {
      setIsLoading(false)
      setStatus('idle')
    }
  }

  const handleAnalyze = async () => {
    try {
      setIsLoading(true)
      setStatus('analyzing')
      await api.analyzeCommits()
      // Refresh data after analysis
      await loadInitialData()
    } catch (error) {
      console.error('Failed to analyze commits:', error)
      alert('Failed to analyze commits. Please try again.')
    } finally {
      setIsLoading(false)
      setStatus('idle')
    }
  }

  return (
    <div className="min-h-screen bg-darker-blue">
      <div className="container mx-auto px-4 py-6">
        <Header isConnected={isConnected} />
        
        <div className="mt-8 space-y-6">
          <CommitTracking 
            onStartTracking={handleStartTracking}
            onRefresh={handleRefresh}
            onFetchLocal={handleFetchLocal}
            onAnalyze={handleAnalyze}
            status={status}
            isLoading={isLoading}
          />
          
          <StatsPanel 
            totalCommits={totalCommits}
            currentPosition={currentPosition}
            status={status}
          />
          
          {commits.length === 0 ? (
            <NoCommitsFound onFetchLocal={handleFetchLocal} />
          ) : (
            <div className="card">
              <h3 className="text-xl font-bold text-white mb-4">Recent Commits</h3>
              <div className="space-y-3">
                {commits.slice(0, 5).map((commit) => (
                  <div key={commit.id} className="border border-gray-700 rounded-lg p-4">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <p className="text-white font-medium">{commit.message}</p>
                        <p className="text-gray-400 text-sm mt-1">
                          {commit.author} • {new Date(commit.commit_date).toLocaleDateString()}
                        </p>
                        <p className="text-gray-500 text-xs mt-1">
                          {commit.hash.substring(0, 8)} • {commit.changed_files.length} files changed
                        </p>
                      </div>
                      <div className="text-right text-sm text-gray-400">
                        <div>+{commit.insertions}</div>
                        <div>-{commit.deletions}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
