# Shared Data Store

## Overview

The shared data store provides centralized data storage for all CraftNudge AI Agent services, with a focus on behavioral data and commit tracking information.

## User Story 2.1.1 Data Storage

### Commit Data Storage

**Location**: `behaviors/commits.jsonl`

This file stores all tracked Git commit data in JSONL (JSON Lines) format, as specified in User Story 2.1.1.

#### File Format

Each line contains a single JSON object representing one commit:

```json
{"id": "uuid-1", "timestamp": "2024-01-01T12:00:00Z", "commit_hash": "abc123...", "author": "dev@example.com", "message": "feat: add feature", "changed_files": ["file1.py"], "insertions": 10, "deletions": 5, "repository_path": "/path/to/repo"}
{"id": "uuid-2", "timestamp": "2024-01-01T13:00:00Z", "commit_hash": "def456...", "author": "dev@example.com", "message": "fix: bug fix", "changed_files": ["file2.py"], "insertions": 3, "deletions": 1, "repository_path": "/path/to/repo"}
```

#### Data Schema

```json
{
  "id": "string (UUID)",
  "timestamp": "string (ISO 8601 UTC)",
  "commit_hash": "string (40-char SHA-1)",
  "author": "string (email)",
  "message": "string (commit message)",
  "changed_files": ["array of file paths"],
  "insertions": "number",
  "deletions": "number",
  "repository_path": "string (absolute path)"
}
```

### Directory Structure

```
shared/data-store/
├── behaviors/
│   ├── commits.jsonl          # Git commit data (User Story 2.1.1)
│   ├── patterns.jsonl         # Behavioral patterns
│   └── insights.jsonl         # Generated insights
├── analytics/
│   ├── metrics.jsonl          # Calculated metrics
│   └── trends.jsonl           # Trend analysis data
├── notifications/
│   ├── sent.jsonl             # Sent notifications
│   └── preferences.jsonl      # User notification preferences
└── README.md                  # This file
```

### Data Access Patterns

#### Reading Data

```python
# Read all commits
with open('behaviors/commits.jsonl', 'r') as f:
    for line in f:
        commit_data = json.loads(line.strip())
        # Process commit data
```

#### Writing Data

```python
# Append new commit
with open('behaviors/commits.jsonl', 'a') as f:
    json.dump(commit_data, f)
    f.write('\n')
```

### Data Integrity

- **Atomic Writes**: Each line is written atomically
- **Backup Strategy**: Regular backups of data files
- **Validation**: JSON schema validation for all entries
- **Error Recovery**: Corrupted lines are logged and skipped

### Performance Considerations

- **JSONL Format**: Efficient for streaming and processing
- **Indexing**: Optional index files for fast queries
- **Compression**: Historical data can be compressed
- **Partitioning**: Data can be partitioned by date ranges

### Security

- **Local Storage**: All data stored locally by default
- **Encryption**: Optional encryption for sensitive data
- **Access Control**: File permissions for multi-user environments
- **Audit Trail**: Logging of data access and modifications
