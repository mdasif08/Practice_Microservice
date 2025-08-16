# CraftNudge AI Agent - Project Structure

## Complete Directory Structure

```
craftnudge-ai-agent/
├── README.md                           # Main project documentation
├── architecture.md                     # Microservice architecture details
├── project-structure.md                # This file - complete structure overview
│
├── services/                           # Microservices
│   ├── commit-tracker-service/         # User Story 2.1.1 Implementation
│   │   ├── src/
│   │   │   ├── commit_tracker.py       # Main tracking module
│   │   │   ├── git_parser.py           # Git repository parsing
│   │   │   └── data_writer.py          # Data storage operations
│   │   ├── tests/
│   │   │   ├── test_commit_tracker.py
│   │   │   ├── test_git_parser.py
│   │   │   └── test_data_writer.py
│   │   ├── requirements.txt            # Service dependencies
│   │   ├── Dockerfile                  # Container configuration
│   │   └── README.md                   # Service documentation
│   │
│   ├── behavior-analytics-service/     # Pattern analysis service
│   │   ├── src/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   └── notification-service/           # Notification and nudges service
│       ├── src/
│       ├── tests/
│       ├── requirements.txt
│       ├── Dockerfile
│       └── README.md
│
├── cli/                                # Command Line Interface
│   ├── commands/
│   │   ├── track_commit.py             # Main CLI command (User Story 2.1.1)
│   │   ├── analyze_patterns.py         # Pattern analysis command
│   │   └── show_insights.py            # Display insights command
│   ├── utils/
│   │   ├── cli_helpers.py              # Common CLI utilities
│   │   └── error_handler.py            # Error handling utilities
│   ├── requirements.txt                # CLI dependencies
│   └── README.md                       # CLI documentation
│
├── api-gateway/                        # API Gateway service
│   ├── src/
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── shared/                             # Shared components
│   ├── data-store/                     # Centralized data storage
│   │   ├── behaviors/
│   │   │   └── commits.jsonl           # Git commit data (User Story 2.1.1)
│   │   ├── analytics/
│   │   │   ├── metrics.jsonl           # Calculated metrics
│   │   │   └── trends.jsonl            # Trend analysis data
│   │   ├── notifications/
│   │   │   ├── sent.jsonl              # Sent notifications
│   │   │   └── preferences.jsonl       # User notification preferences
│   │   └── README.md                   # Data store documentation
│   │
│   ├── utils/                          # Common utilities
│   │   ├── data_validator.py           # Data validation utilities
│   │   ├── logger.py                   # Logging utilities
│   │   ├── error_handler.py            # Error handling utilities
│   │   └── config_manager.py           # Configuration management
│   │
│   └── config/                         # Configuration management
│       ├── app_config.yaml             # Application configuration
│       ├── service_config.yaml         # Service-specific configurations
│       └── environment_config.yaml     # Environment-specific settings
│
├── tests/                              # Comprehensive testing
│   ├── unit/                           # Unit tests
│   │   ├── test_commit_tracker.py
│   │   ├── test_git_parser.py
│   │   └── test_data_writer.py
│   ├── integration/                    # Integration tests
│   │   ├── test_cli_integration.py
│   │   └── test_service_integration.py
│   ├── e2e/                           # End-to-end tests
│   │   └── test_commit_tracking_e2e.py
│   ├── fixtures/                       # Test data and fixtures
│   │   ├── sample_commits.jsonl
│   │   └── mock_repositories/
│   └── README.md                       # Testing documentation
│
├── deployment/                         # Deployment configurations
│   ├── docker/                         # Docker configurations
│   │   ├── Dockerfile.commit-tracker   # Commit tracker service
│   │   ├── Dockerfile.analytics        # Analytics service
│   │   ├── Dockerfile.notifications    # Notification service
│   │   ├── Dockerfile.api-gateway      # API Gateway
│   │   └── docker-compose.yml          # Multi-service orchestration
│   │
│   ├── kubernetes/                     # Kubernetes configurations
│   │   ├── commit-tracker-deployment.yaml
│   │   ├── analytics-deployment.yaml
│   │   ├── notifications-deployment.yaml
│   │   ├── api-gateway-deployment.yaml
│   │   └── ingress.yaml                # Ingress configuration
│   │
│   └── scripts/                        # Deployment scripts
│       ├── build.sh                    # Build all services
│       ├── deploy.sh                   # Deploy to environment
│       └── cleanup.sh                  # Cleanup resources
│
├── docs/                               # Documentation
│   ├── api/                            # API documentation
│   │   ├── commit-tracker-api.md
│   │   ├── analytics-api.md
│   │   └── notifications-api.md
│   ├── user-guide/                     # User guides
│   │   ├── getting-started.md
│   │   ├── cli-usage.md
│   │   └── troubleshooting.md
│   ├── developer/                      # Developer documentation
│   │   ├── development-setup.md
│   │   ├── contributing.md
│   │   └── architecture-deep-dive.md
│   └── deployment/                     # Deployment documentation
│       ├── docker-deployment.md
│       ├── kubernetes-deployment.md
│       └── production-checklist.md
│
├── scripts/                            # Utility scripts
│   ├── setup.sh                        # Initial project setup
│   ├── install-dependencies.sh         # Install all dependencies
│   ├── run-tests.sh                    # Run all tests
│   └── generate-docs.sh                # Generate documentation
│
├── .gitignore                          # Git ignore patterns
├── .env.example                        # Environment variables template
├── docker-compose.yml                  # Local development orchestration
├── requirements.txt                    # Root project dependencies
└── pyproject.toml                      # Python project configuration
```

## Key Files for User Story 2.1.1

### Core Implementation Files
- `services/commit-tracker-service/src/commit_tracker.py` - Main tracking logic
- `services/commit-tracker-service/src/git_parser.py` - Git repository parsing
- `services/commit-tracker-service/src/data_writer.py` - Data storage operations
- `cli/commands/track_commit.py` - CLI command implementation
- `shared/data-store/behaviors/commits.jsonl` - Data storage location

### Configuration Files
- `services/commit-tracker-service/requirements.txt` - Service dependencies
- `services/commit-tracker-service/Dockerfile` - Container configuration
- `deployment/kubernetes/commit-tracker-deployment.yaml` - K8s deployment

### Testing Files
- `services/commit-tracker-service/tests/` - Service-specific tests
- `tests/unit/test_commit_tracker.py` - Unit tests
- `tests/integration/test_cli_integration.py` - Integration tests
- `tests/e2e/test_commit_tracking_e2e.py` - End-to-end tests

### Documentation Files
- `README.md` - Main project documentation
- `services/commit-tracker-service/README.md` - Service documentation
- `cli/README.md` - CLI documentation
- `shared/data-store/README.md` - Data store documentation

## Service Dependencies

### Commit Tracker Service
- **Input**: Git repository (local filesystem)
- **Output**: JSONL data to `shared/data-store/behaviors/commits.jsonl`
- **Dependencies**: gitpython, pydantic, jsonlines, loguru

### Behavior Analytics Service
- **Input**: Commit data from data store
- **Output**: Analytics results to `shared/data-store/analytics/`
- **Dependencies**: pandas, numpy, scikit-learn

### Notification Service
- **Input**: Analytics results and user preferences
- **Output**: Notifications to `shared/data-store/notifications/`
- **Dependencies**: smtplib, requests (for webhooks)

### API Gateway
- **Input**: HTTP requests from clients
- **Output**: Routed requests to appropriate services
- **Dependencies**: fastapi, uvicorn, httpx

## Data Flow Architecture

```
User CLI → Commit Tracker Service → Data Store
                                    ↓
Analytics Service ← Data Store ← Commit Data
                                    ↓
Notification Service ← Analytics Results
```

## Development Workflow

1. **Setup**: Run `scripts/setup.sh` to initialize the project
2. **Development**: Work on individual services in `services/`
3. **Testing**: Run `scripts/run-tests.sh` for comprehensive testing
4. **Documentation**: Run `scripts/generate-docs.sh` to update docs
5. **Deployment**: Use `deployment/` configurations for different environments

## Environment Support

- **Development**: Local file-based storage, direct service communication
- **Staging**: Docker containers, shared volumes
- **Production**: Kubernetes orchestration, persistent storage, load balancing
