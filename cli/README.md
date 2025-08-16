# CLI Interface

## Overview

The Command Line Interface (CLI) provides user-friendly access to CraftNudge AI Agent functionality, particularly the Git commit tracking features.

## User Story 2.1.1 CLI Implementation

### Main Command: `track_commit.py`

The primary CLI tool for tracking Git commits as specified in User Story 2.1.1.

#### Usage

```bash
# Track the latest commit in current repository
python track_commit.py

# Track a specific commit by hash
python track_commit.py --commit-hash abc123def456

# Track commits in a date range
python track_commit.py --since "2024-01-01" --until "2024-01-31"

# Track commits with verbose output
python track_commit.py --verbose

# Specify custom data storage location
python track_commit.py --data-path /custom/path/commits.jsonl
```

#### Command Options

- `--commit-hash`: Specific commit hash to track
- `--since`: Start date for commit range (YYYY-MM-DD)
- `--until`: End date for commit range (YYYY-MM-DD)
- `--verbose`: Enable detailed output
- `--data-path`: Custom path for data storage
- `--help`: Show help information

#### Error Handling

The CLI provides user-friendly error messages for common scenarios:

- **No Git Repository**: "Error: No Git repository found in current directory. Please run this command from a Git repository."
- **Invalid Commit Hash**: "Error: Invalid commit hash 'abc123'. Please provide a valid 40-character SHA-1 hash."
- **Permission Issues**: "Error: Cannot access Git repository. Please check file permissions."

### File Structure

```
cli/
├── commands/
│   ├── track_commit.py        # Main commit tracking command
│   ├── analyze_patterns.py    # Pattern analysis command
│   └── show_insights.py       # Display insights command
├── utils/
│   ├── cli_helpers.py         # Common CLI utilities
│   └── error_handler.py       # Error handling utilities
├── requirements.txt           # CLI dependencies
└── README.md                 # This file
```

### Integration

- **Commit Tracker Service**: Direct integration for commit logging
- **Data Store**: Reads/writes to `shared/data-store/behaviors/`
- **Analytics Service**: Triggers pattern analysis
- **User Feedback**: Provides immediate feedback and progress indicators

### Future Commands

- `analyze_patterns.py`: Analyze commit patterns over time
- `show_insights.py`: Display personalized insights and recommendations
- `setup_repository.py`: Initialize CraftNudge for a new repository
- `export_data.py`: Export commit data in various formats
