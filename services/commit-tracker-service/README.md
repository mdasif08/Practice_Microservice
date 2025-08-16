# Commit Tracker Service

## Overview

The Commit Tracker Service is responsible for logging Git commits with metadata to help developers track their coding patterns over time.

## User Story 2.1.1 Implementation

**As a user, I want CraftNudge to log every Git commit I make (with metadata), so that I can reflect on my coding patterns over time.**

### Features

- Logs commit hash, author, message, timestamp, and changed files
- Runs on-demand via CLI command
- Stores data in JSONL format for easy processing
- Includes unique ID and UTC timestamp for each entry
- Graceful error handling for non-Git repositories

### File Structure

```
services/commit-tracker-service/
├── src/
│   ├── commit_tracker.py      # Main tracking module
│   ├── git_parser.py          # Git repository parsing utilities
│   └── data_writer.py         # Data storage utilities
├── tests/
│   ├── test_commit_tracker.py
│   ├── test_git_parser.py
│   └── test_data_writer.py
├── requirements.txt           # Service dependencies
├── Dockerfile                # Container configuration
└── README.md                 # This file
```

### CLI Usage

```bash
# Track the latest commit
python track_commit.py

# Track specific commit
python track_commit.py --commit-hash <hash>

# Track all commits in a range
python track_commit.py --since <date> --until <date>
```

### Data Schema

Each commit entry in `data/behaviors/commits.jsonl` will have the following structure:

```json
{
  "id": "unique-uuid",
  "timestamp": "2024-01-01T12:00:00Z",
  "commit_hash": "abc123...",
  "author": "developer@example.com",
  "message": "feat: add new feature",
  "changed_files": ["src/file1.py", "tests/test_file1.py"],
  "insertions": 10,
  "deletions": 5,
  "repository_path": "/path/to/repo"
}
```

### Error Handling

- **No Git Repository**: Graceful error message with instructions
- **Invalid Commit Hash**: Clear error message with valid hash examples
- **Permission Issues**: User-friendly error messages with resolution steps
- **Data Storage Issues**: Fallback mechanisms and error logging

### Integration Points

- **Data Store**: Writes to `shared/data-store/behaviors/commits.jsonl`
- **Analytics Service**: Provides data for pattern analysis
- **Notification Service**: Triggers insights and recommendations
