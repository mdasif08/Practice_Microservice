# CraftNudge AI Agent - Microservice Architecture

## Overview

CraftNudge AI Agent follows a microservice architecture pattern to provide scalable, maintainable, and loosely coupled services for tracking and analyzing developer behavior patterns.

## Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Interface │    │   API Gateway    │    │  Web Interface  │
└─────────┬───────┘    └──────────┬───────┘    └─────────┬───────┘
          │                       │                      │
          └───────────────────────┼──────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
          ┌─────────▼────────┐    │    ┌────────▼────────┐
          │ Commit Tracker   │    │    │ Behavior        │
          │ Service          │    │    │ Analytics       │
          │                  │    │    │ Service         │
          └─────────┬────────┘    │    └─────────┬────────┘
                    │             │              │
                    └─────────────┼──────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Notification Service      │
                    │                          │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │ Shared Data Store         │
                    │ - behaviors/commits.jsonl │
                    │ - analytics/metrics.jsonl │
                    │ - notifications/sent.jsonl│
                    └───────────────────────────┘
```

## Service Components

### 1. Commit Tracker Service
**Location**: `services/commit-tracker-service/`

**Purpose**: Implements User Story 2.1.1 - Git Commit Logger

**Responsibilities**:
- Parse Git repository information
- Extract commit metadata (hash, author, message, timestamp, changed files)
- Generate unique IDs and UTC timestamps
- Write data to `shared/data-store/behaviors/commits.jsonl`
- Handle errors gracefully (no Git repo, permission issues, etc.)

**Key Files**:
- `src/commit_tracker.py` - Main tracking logic
- `src/git_parser.py` - Git repository parsing
- `src/data_writer.py` - Data storage operations

### 2. Behavior Analytics Service
**Location**: `services/behavior-analytics-service/`

**Purpose**: Analyze commit patterns and generate insights

**Responsibilities**:
- Process commit data from data store
- Identify behavioral patterns
- Calculate productivity metrics
- Generate personalized insights
- Trigger notifications based on patterns

### 3. Notification Service
**Location**: `services/notification-service/`

**Purpose**: Send personalized nudges and recommendations

**Responsibilities**:
- Process insights from analytics service
- Generate personalized recommendations
- Send notifications via various channels
- Manage user notification preferences

### 4. API Gateway
**Location**: `api-gateway/`

**Purpose**: Central entry point for all services

**Responsibilities**:
- Route requests to appropriate services
- Handle authentication and authorization
- Rate limiting and throttling
- Request/response transformation
- Service discovery

### 5. CLI Interface
**Location**: `cli/`

**Purpose**: Command-line access to services

**Responsibilities**:
- Provide `track_commit.py` command (User Story 2.1.1)
- User-friendly error messages
- Command-line argument parsing
- Progress indicators and feedback

## Shared Components

### Data Store
**Location**: `shared/data-store/`

**Purpose**: Centralized data storage

**Key Files**:
- `behaviors/commits.jsonl` - Git commit data (User Story 2.1.1)
- `analytics/metrics.jsonl` - Calculated metrics
- `notifications/sent.jsonl` - Notification history

### Utilities
**Location**: `shared/utils/`

**Purpose**: Common utilities across services

**Components**:
- Data validation utilities
- Logging utilities
- Error handling utilities
- Configuration management

### Configuration
**Location**: `shared/config/`

**Purpose**: Centralized configuration management

**Components**:
- Service configurations
- Environment-specific settings
- Feature flags
- API keys and secrets management

## Data Flow

### Commit Tracking Flow (User Story 2.1.1)

1. **User executes**: `python track_commit.py`
2. **CLI validates**: Current directory is a Git repository
3. **Git Parser extracts**: Commit metadata from repository
4. **Data Writer stores**: Commit data to `commits.jsonl`
5. **User receives**: Success/error feedback

### Analytics Flow

1. **Analytics Service reads**: Commit data from data store
2. **Pattern Analysis**: Identifies behavioral patterns
3. **Insight Generation**: Creates personalized insights
4. **Notification Trigger**: Sends recommendations to notification service

## Communication Patterns

### Synchronous Communication
- CLI to Commit Tracker Service
- API Gateway to individual services
- Direct service-to-service calls for simple operations

### Asynchronous Communication
- Commit Tracker to Analytics Service (event-driven)
- Analytics Service to Notification Service (event-driven)
- Background processing for pattern analysis

## Deployment Architecture

### Development Environment
- Local file-based data storage
- Direct service communication
- Single-node deployment

### Production Environment
- Containerized services (Docker)
- Orchestration (Kubernetes)
- Distributed data storage
- Load balancing and scaling

## Security Considerations

- **Local Data Storage**: All sensitive data stored locally
- **Service Isolation**: Each service runs in isolated containers
- **API Security**: Authentication and authorization at gateway level
- **Data Encryption**: Optional encryption for sensitive data
- **Audit Logging**: Comprehensive logging of all operations

## Scalability Strategy

- **Horizontal Scaling**: Services can be scaled independently
- **Data Partitioning**: Commit data can be partitioned by date/repository
- **Caching**: Redis for frequently accessed data
- **Load Balancing**: Multiple instances of each service
- **Database Scaling**: Migration to distributed databases as needed
