import { Commit, RepositoryInfo, TrackingStatus } from '../types'

const API_BASE_URL = '/api'

export const api = {
  // Commit tracking
  async startTracking(): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/tracking/start`, {
      method: 'POST',
    })
    if (!response.ok) {
      throw new Error('Failed to start tracking')
    }
  },

  async stopTracking(): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/tracking/stop`, {
      method: 'POST',
    })
    if (!response.ok) {
      throw new Error('Failed to stop tracking')
    }
  },

  async getTrackingStatus(): Promise<TrackingStatus> {
    const response = await fetch(`${API_BASE_URL}/tracking/status`)
    if (!response.ok) {
      throw new Error('Failed to get tracking status')
    }
    return response.json()
  },

  // Commits
  async fetchLocalCommits(): Promise<Commit[]> {
    const response = await fetch(`${API_BASE_URL}/commits/fetch-local`, {
      method: 'POST',
    })
    if (!response.ok) {
      throw new Error('Failed to fetch local commits')
    }
    return response.json()
  },

  async getCommits(limit?: number): Promise<Commit[]> {
    const params = limit ? `?limit=${limit}` : ''
    const response = await fetch(`${API_BASE_URL}/commits${params}`)
    if (!response.ok) {
      throw new Error('Failed to get commits')
    }
    return response.json()
  },

  async getCommitByHash(hash: string): Promise<Commit> {
    const response = await fetch(`${API_BASE_URL}/commits/${hash}`)
    if (!response.ok) {
      throw new Error('Failed to get commit')
    }
    return response.json()
  },

  // Repository
  async getRepositoryInfo(): Promise<RepositoryInfo> {
    const response = await fetch(`${API_BASE_URL}/repository/info`)
    if (!response.ok) {
      throw new Error('Failed to get repository info')
    }
    return response.json()
  },

  // Analytics
  async analyzeCommits(): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/analytics/analyze`, {
      method: 'POST',
    })
    if (!response.ok) {
      throw new Error('Failed to analyze commits')
    }
    return response.json()
  },
}
