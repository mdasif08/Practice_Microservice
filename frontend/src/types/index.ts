export interface Commit {
  id: string
  hash: string
  author: string
  author_email: string
  message: string
  body?: string
  commit_date: string
  timestamp: string
  changed_files: string[]
  insertions: number
  deletions: number
}

export interface RepositoryInfo {
  name: string
  url: string
  branch: string
  total_commits: number
  last_commit_date: string
}

export interface TrackingStatus {
  isTracking: boolean
  totalCommits: number
  currentPosition: number
  status: 'idle' | 'tracking' | 'fetching' | 'analyzing'
}
