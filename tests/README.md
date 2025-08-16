# Testing Strategy

## Overview

This directory contains comprehensive tests for the CraftNudge AI Agent, with a focus on testing the Git Commit Logger functionality (User Story 2.1.1).

## Test Structure

```
tests/
├── unit/                          # Unit tests for individual components
│   ├── test_commit_tracker.py     # Commit tracker service tests
│   ├── test_git_parser.py         # Git parsing utility tests
│   └── test_data_writer.py        # Data storage tests
├── integration/                   # Integration tests
│   ├── test_cli_integration.py    # CLI command integration tests
│   └── test_service_integration.py # Service communication tests
├── e2e/                          # End-to-end tests
│   └── test_commit_tracking_e2e.py # Full commit tracking workflow
└── fixtures/                     # Test data and fixtures
    ├── sample_commits.jsonl      # Sample commit data
    └── mock_repositories/        # Mock Git repositories for testing
```

## User Story 2.1.1 Test Cases

### Unit Tests

#### Commit Tracker Service
- Test commit metadata extraction
- Test unique ID generation
- Test UTC timestamp formatting
- Test error handling for non-Git repositories
- Test data validation

#### Git Parser
- Test repository detection
- Test commit hash extraction
- Test author information parsing
- Test changed files detection
- Test commit message parsing

#### Data Writer
- Test JSONL file writing
- Test atomic write operations
- Test data schema validation
- Test error recovery mechanisms

### Integration Tests

#### CLI Integration
- Test `python track_commit.py` command
- Test command-line argument parsing
- Test user feedback and error messages
- Test data storage integration

#### Service Integration
- Test commit tracker to data store communication
- Test error propagation between services
- Test data consistency across services

### End-to-End Tests

#### Complete Workflow
- Test full commit tracking workflow
- Test data persistence and retrieval
- Test error scenarios and recovery
- Test performance with large repositories

## Test Data

### Sample Commits
```json
{
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

### Mock Repositories
- Clean repository with single commit
- Repository with multiple commits
- Repository with merge commits
- Repository with no commits
- Corrupted repository

## Running Tests

### Unit Tests
```bash
# Run all unit tests
pytest tests/unit/

# Run specific service tests
pytest tests/unit/test_commit_tracker.py

# Run with coverage
pytest tests/unit/ --cov=services/commit-tracker-service
```

### Integration Tests
```bash
# Run integration tests
pytest tests/integration/

# Run with verbose output
pytest tests/integration/ -v
```

### End-to-End Tests
```bash
# Run E2E tests
pytest tests/e2e/

# Run with specific markers
pytest tests/e2e/ -m "slow"
```

## Test Configuration

### Environment Variables
- `TEST_DATA_PATH`: Path to test data files
- `TEST_REPO_PATH`: Path to mock repositories
- `TEST_OUTPUT_PATH`: Path for test output files

### Test Dependencies
- `pytest`: Test framework
- `pytest-mock`: Mocking utilities
- `pytest-cov`: Coverage reporting
- `gitpython`: Git repository testing

## Continuous Integration

### GitHub Actions
- Run tests on every commit
- Generate coverage reports
- Validate code quality
- Deploy to staging environment

### Test Reports
- Coverage reports in HTML format
- Test results in JUnit XML format
- Performance benchmarks
- Security scan results
