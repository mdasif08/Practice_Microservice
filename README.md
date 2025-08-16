# CraftNudge AI Agent

An AI Native Agent for tracking and analyzing developer behavior patterns to encourage better coding habits.

## Project Overview

CraftNudge is a microservice-based AI agent that helps developers track their coding patterns and behaviors over time, providing insights to improve productivity and coding practices.

## Architecture

This project follows a microservice architecture with the following components:

- **Commit Tracker Service**: Logs Git commits with metadata
- **Behavior Analytics Service**: Analyzes patterns and provides insights
- **Notification Service**: Sends personalized nudges and recommendations
- **API Gateway**: Central entry point for all services
- **CLI Interface**: Command-line tools for user interaction
- **Shared Components**: Common utilities, data store, and configuration

## User Story 2.1.1: Behavior Tracker – Git Commit Logger

**As a user, I want CraftNudge to log every Git commit I make (with metadata), so that I can reflect on my coding patterns over time.**

### Acceptance Criteria:
- A commit_tracker.py module logs each commit's hash, author, message, timestamp, and changed files
- The tracker runs on-demand via CLI: python track_commit.py
- Logged data is stored locally in data/behaviors/commits.jsonl
- Each entry includes a unique ID and UTC timestamp
- Errors (e.g., no Git repository) are handled gracefully with user feedback

### Behavioral Diagnostics:
- **Tool Present**: The commit_tracker.py CLI is the tool capturing commit data
- **Still Broken Because**: Without logging, developers lack visibility into their commit history and patterns
- **Behavioral Root Cause**: Relying on memory or Git logs manually is tedious, so developers rarely analyze their commit habits
- **✅ Self-Healing Behavior Loop**: Seeing commit history encourages consistent committing and better coding habits over time
- **❌ Reactive Behavior Loop**: Otherwise, developers only review commits when problems occur, rather than proactively observing habits
- **Impacted Level(s)**: Individual (developer self-awareness)
- **💼 Business Value**: Increases developer insight into their productivity trends, which can lead to more consistent version control practices

## Getting Started

[Development setup instructions will be added here]

## Services

### Commit Tracker Service
- Location: `services/commit-tracker-service/`
- Purpose: Log Git commits with metadata
- CLI Command: `python track_commit.py`

### Behavior Analytics Service
- Location: `services/behavior-analytics-service/`
- Purpose: Analyze commit patterns and provide insights

### Notification Service
- Location: `services/notification-service/`
- Purpose: Send personalized recommendations and nudges

## Data Storage

- **Local Storage**: `shared/data-store/behaviors/commits.jsonl`
- **Format**: JSONL (JSON Lines) for easy processing
- **Schema**: Each entry includes unique ID, UTC timestamp, and commit metadata

## Development

[Development guidelines will be added here]

## Deployment

[Deployment instructions will be added here]
