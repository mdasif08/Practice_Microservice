# CraftNudge AI Agent - Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the CraftNudge AI Agent, focusing on User Story 2.1.1: Behavior Tracker – Git Commit Logger.

## Implementation Phases

### Phase 1: Core Infrastructure (Week 1-2)

#### 1.1 Project Setup
```bash
# Clone the repository and run setup
git clone <repository-url>
cd craftnudge-ai-agent
./scripts/setup.sh
```

#### 1.2 Data Store Implementation
- **File**: `shared/data-store/behaviors/commits.jsonl`
- **Schema**: JSONL format with commit metadata
- **Validation**: Pydantic models for data validation

#### 1.3 Shared Utilities
- **Data Validation**: `shared/utils/data_validator.py`
- **Logging**: `shared/utils/logger.py`
- **Error Handling**: `shared/utils/error_handler.py`
- **Configuration**: `shared/utils/config_manager.py`

### Phase 2: Commit Tracker Service (Week 2-3)

#### 2.1 Core Components
- **Git Parser**: `services/commit-tracker-service/src/git_parser.py`
  - Repository detection
  - Commit metadata extraction
  - File change analysis

- **Data Writer**: `services/commit-tracker-service/src/data_writer.py`
  - JSONL file operations
  - Atomic writes
  - Error recovery

- **Commit Tracker**: `services/commit-tracker-service/src/commit_tracker.py`
  - Main orchestration logic
  - Data validation
  - Error handling

#### 2.2 Implementation Steps
1. **Git Repository Detection**
   ```python
   def detect_git_repository(path: str) -> bool:
       """Check if the given path is a Git repository."""
   ```

2. **Commit Metadata Extraction**
   ```python
   def extract_commit_metadata(commit_hash: str) -> CommitData:
       """Extract metadata from a specific commit."""
   ```

3. **Data Storage**
   ```python
   def write_commit_data(data: CommitData, file_path: str) -> bool:
       """Write commit data to JSONL file."""
   ```

#### 2.3 Error Handling
- **No Git Repository**: Graceful error with instructions
- **Invalid Commit Hash**: Validation with helpful messages
- **Permission Issues**: User-friendly error messages
- **Data Storage Issues**: Fallback mechanisms

### Phase 3: CLI Interface (Week 3-4)

#### 3.1 Main Command Implementation
- **File**: `cli/commands/track_commit.py`
- **Framework**: Click or Typer for CLI
- **Features**:
  - Track latest commit
  - Track specific commit by hash
  - Track commits in date range
  - Verbose output option

#### 3.2 CLI Usage Examples
```bash
# Track the latest commit
python track_commit.py

# Track specific commit
python track_commit.py --commit-hash abc123def456

# Track commits in range
python track_commit.py --since "2024-01-01" --until "2024-01-31"

# Verbose output
python track_commit.py --verbose
```

#### 3.3 Error Messages
```python
ERROR_MESSAGES = {
    "no_git_repo": "Error: No Git repository found in current directory. Please run this command from a Git repository.",
    "invalid_hash": "Error: Invalid commit hash '{hash}'. Please provide a valid 40-character SHA-1 hash.",
    "permission_denied": "Error: Cannot access Git repository. Please check file permissions."
}
```

### Phase 4: Testing Implementation (Week 4-5)

#### 4.1 Unit Tests
- **Commit Tracker Tests**: `tests/unit/test_commit_tracker.py`
- **Git Parser Tests**: `tests/unit/test_git_parser.py`
- **Data Writer Tests**: `tests/unit/test_data_writer.py`

#### 4.2 Integration Tests
- **CLI Integration**: `tests/integration/test_cli_integration.py`
- **Service Integration**: `tests/integration/test_service_integration.py`

#### 4.3 End-to-End Tests
- **Full Workflow**: `tests/e2e/test_commit_tracking_e2e.py`

#### 4.4 Test Data
- **Sample Commits**: `tests/fixtures/sample_commits.jsonl`
- **Mock Repositories**: `tests/fixtures/mock_repositories/`

### Phase 5: Documentation and Deployment (Week 5-6)

#### 5.1 Documentation
- **API Documentation**: `docs/api/commit-tracker-api.md`
- **User Guide**: `docs/user-guide/cli-usage.md`
- **Developer Guide**: `docs/developer/development-setup.md`

#### 5.2 Deployment
- **Docker**: `deployment/docker/Dockerfile.commit-tracker`
- **Kubernetes**: `deployment/kubernetes/commit-tracker-deployment.yaml`
- **Local Development**: `docker-compose.yml`

## Data Schema Implementation

### Commit Data Model
```python
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CommitData(BaseModel):
    id: str  # UUID
    timestamp: datetime  # UTC timestamp
    commit_hash: str  # 40-character SHA-1
    author: str  # Email address
    message: str  # Commit message
    changed_files: List[str]  # List of file paths
    insertions: int  # Number of insertions
    deletions: int  # Number of deletions
    repository_path: str  # Absolute path to repository
```

### JSONL File Format
```json
{"id": "uuid-1", "timestamp": "2024-01-01T12:00:00Z", "commit_hash": "abc123...", "author": "dev@example.com", "message": "feat: add feature", "changed_files": ["file1.py"], "insertions": 10, "deletions": 5, "repository_path": "/path/to/repo"}
{"id": "uuid-2", "timestamp": "2024-01-01T13:00:00Z", "commit_hash": "def456...", "author": "dev@example.com", "message": "fix: bug fix", "changed_files": ["file2.py"], "insertions": 3, "deletions": 1, "repository_path": "/path/to/repo"}
```

## Configuration Management

### Environment Variables
```bash
# Commit Tracker Service
COMMIT_TRACKER_DATA_PATH=shared/data-store/behaviors/commits.jsonl
COMMIT_TRACKER_LOG_LEVEL=INFO

# Data Store
DATA_STORE_PATH=shared/data-store

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/craftnudge.log
```

### Configuration Files
- **App Config**: `shared/config/app_config.yaml`
- **Service Config**: `shared/config/service_config.yaml`
- **Environment Config**: `shared/config/environment_config.yaml`

## Error Handling Strategy

### Error Categories
1. **Validation Errors**: Invalid input data
2. **System Errors**: File system, permissions
3. **Git Errors**: Repository issues, commit problems
4. **Data Errors**: Storage, corruption issues

### Error Response Format
```python
class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[dict] = None
    timestamp: datetime
    request_id: str
```

## Testing Strategy

### Test Pyramid
1. **Unit Tests**: 70% - Individual components
2. **Integration Tests**: 20% - Service interactions
3. **End-to-End Tests**: 10% - Full workflows

### Test Coverage Goals
- **Lines of Code**: >90%
- **Branches**: >85%
- **Functions**: >95%

### Mock Data
```python
SAMPLE_COMMIT_DATA = {
    "id": "test-uuid-1",
    "timestamp": "2024-01-01T12:00:00Z",
    "commit_hash": "abc123def456789",
    "author": "test@example.com",
    "message": "feat: add new feature",
    "changed_files": ["src/feature.py", "tests/test_feature.py"],
    "insertions": 50,
    "deletions": 10,
    "repository_path": "/test/repo"
}
```

## Performance Considerations

### Data Storage
- **JSONL Format**: Efficient for streaming and processing
- **Atomic Writes**: Each line written atomically
- **Compression**: Optional for historical data
- **Indexing**: For fast queries (future enhancement)

### Memory Usage
- **Streaming Processing**: Process large files without loading into memory
- **Batch Operations**: Group multiple commits for efficiency
- **Caching**: Cache frequently accessed data

## Security Considerations

### Data Privacy
- **Local Storage**: All data stored locally by default
- **Encryption**: Optional encryption for sensitive data
- **Access Control**: File permissions for multi-user environments
- **Audit Trail**: Logging of data access and modifications

### Input Validation
- **Commit Hash Validation**: Ensure valid SHA-1 format
- **Path Validation**: Prevent path traversal attacks
- **Message Sanitization**: Clean commit messages
- **Size Limits**: Prevent oversized inputs

## Monitoring and Observability

### Logging
- **Structured Logging**: JSON format for easy parsing
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Rotation**: Daily rotation with retention
- **Centralized Logging**: Future integration with ELK stack

### Metrics
- **Commit Count**: Number of commits tracked
- **Error Rate**: Percentage of failed operations
- **Response Time**: Time to process commits
- **Storage Usage**: Data file sizes and growth

## Future Enhancements

### Phase 6: Analytics Service
- Pattern detection algorithms
- Productivity metrics calculation
- Insight generation

### Phase 7: Notification Service
- Personalized recommendations
- Multi-channel notifications
- User preference management

### Phase 8: API Gateway
- RESTful API endpoints
- Authentication and authorization
- Rate limiting and monitoring

## Success Criteria

### User Story 2.1.1 Acceptance Criteria
- ✅ Commit tracker module logs commit metadata
- ✅ CLI command runs on-demand
- ✅ Data stored in JSONL format
- ✅ Unique ID and UTC timestamp included
- ✅ Graceful error handling implemented

### Quality Metrics
- **Code Coverage**: >90%
- **Performance**: <1 second for single commit tracking
- **Reliability**: 99.9% uptime
- **User Experience**: Clear error messages and feedback

## Getting Started

1. **Setup Environment**
   ```bash
   ./scripts/setup.sh
   source venv/bin/activate
   ```

2. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

3. **Test CLI**
   ```bash
   python cli/commands/track_commit.py --help
   ```

4. **Start Development**
   ```bash
   # Make changes to implementation files
   # Run tests to verify changes
   # Commit changes with meaningful messages
   ```

## Support and Resources

- **Documentation**: `docs/` directory
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Contributing**: `CONTRIBUTING.md` for development guidelines
