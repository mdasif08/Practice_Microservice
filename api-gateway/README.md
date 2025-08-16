# API Gateway

## Overview

The API Gateway serves as the central entry point for all CraftNudge AI Agent services, providing a unified interface for clients to interact with the microservices.

## Purpose

This service provides:
- Centralized routing to all microservices
- Authentication and authorization
- Rate limiting and throttling
- Request/response transformation
- Service discovery and load balancing

## Features

- **Unified API**: Single entry point for all service interactions
- **Authentication**: JWT-based authentication and authorization
- **Rate Limiting**: Configurable rate limits per user/service
- **Request Routing**: Intelligent routing to appropriate services
- **Response Aggregation**: Combine responses from multiple services
- **Error Handling**: Centralized error handling and logging
- **Monitoring**: Request/response monitoring and metrics

## File Structure

```
api-gateway/
├── src/
│   ├── main.py                    # FastAPI application entry point
│   ├── routes/                    # API route definitions
│   │   ├── commit_tracker.py      # Commit tracking endpoints
│   │   ├── analytics.py           # Analytics endpoints
│   │   ├── notifications.py       # Notification endpoints
│   │   └── health.py              # Health check endpoints
│   ├── middleware/                # Custom middleware
│   │   ├── auth.py                # Authentication middleware
│   │   ├── rate_limit.py          # Rate limiting middleware
│   │   └── logging.py             # Request logging middleware
│   ├── services/                  # Service clients
│   │   ├── commit_tracker_client.py
│   │   ├── analytics_client.py
│   │   └── notification_client.py
│   └── utils/                     # Utility functions
│       ├── config.py              # Configuration management
│       └── response.py            # Response formatting
├── tests/
│   ├── test_routes/
│   ├── test_middleware/
│   └── test_services/
├── requirements.txt               # Service dependencies
├── Dockerfile                    # Container configuration
└── README.md                     # This file
```

## API Endpoints

### Commit Tracker Endpoints
```
POST /api/v1/commits/track          # Track a new commit
GET  /api/v1/commits                # Get commit history
GET  /api/v1/commits/{commit_id}    # Get specific commit
POST /api/v1/commits/batch          # Track multiple commits
```

### Analytics Endpoints
```
GET  /api/v1/analytics/patterns     # Get behavioral patterns
GET  /api/v1/analytics/metrics      # Get productivity metrics
GET  /api/v1/analytics/trends       # Get trend analysis
POST /api/v1/analytics/analyze      # Trigger analysis
```

### Notification Endpoints
```
GET  /api/v1/notifications          # Get user notifications
POST /api/v1/notifications/send     # Send notification
PUT  /api/v1/notifications/preferences # Update preferences
GET  /api/v1/notifications/history  # Get notification history
```

### Health and Status
```
GET  /health                        # Health check
GET  /status                        # Service status
GET  /metrics                       # Prometheus metrics
```

## Authentication

### JWT Authentication
- **Token-based**: JWT tokens for stateless authentication
- **Refresh Tokens**: Automatic token refresh mechanism
- **Role-based Access**: Different permissions for different user roles
- **API Keys**: Support for API key authentication

### Authorization Levels
- **Public**: Health checks and basic status
- **User**: Personal commit tracking and analytics
- **Admin**: System-wide analytics and management
- **Service**: Inter-service communication

## Rate Limiting

### Limits by Endpoint
- **Read Operations**: Higher limits for data retrieval
- **Write Operations**: Lower limits for data modification
- **Analytics**: Separate limits for resource-intensive operations
- **Notifications**: Limits to prevent spam

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## Service Discovery

### Service Registry
- **Dynamic Registration**: Services register themselves
- **Health Checks**: Regular health check monitoring
- **Load Balancing**: Round-robin and weighted load balancing
- **Circuit Breaker**: Automatic failover for unhealthy services

### Service Communication
- **HTTP/HTTPS**: Standard HTTP communication
- **gRPC**: High-performance RPC for internal communication
- **Message Queues**: Asynchronous communication via queues
- **Event Streaming**: Real-time event processing

## Error Handling

### Error Responses
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid commit hash format",
    "details": {
      "field": "commit_hash",
      "value": "abc123",
      "expected": "40-character SHA-1 hash"
    }
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "req-12345"
}
```

### Error Codes
- **400**: Bad Request - Invalid input
- **401**: Unauthorized - Authentication required
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Resource not found
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - Service error
- **503**: Service Unavailable - Service down

## Monitoring and Metrics

### Prometheus Metrics
- **Request Count**: Total requests per endpoint
- **Response Time**: Average response times
- **Error Rate**: Error percentage per endpoint
- **Active Connections**: Current active connections

### Health Checks
- **Liveness Probe**: Service is running
- **Readiness Probe**: Service is ready to handle requests
- **Dependency Checks**: All downstream services are healthy

## Configuration

### Environment Variables
- `GATEWAY_PORT`: Port for the gateway service (default: 8000)
- `JWT_SECRET`: Secret for JWT token signing
- `RATE_LIMIT_DEFAULT`: Default rate limit per minute
- `SERVICE_TIMEOUT`: Timeout for service calls (default: 30s)

### Service Configuration
- **Service URLs**: URLs for each microservice
- **Timeout Settings**: Timeouts for different service calls
- **Retry Logic**: Retry policies for failed requests
- **Circuit Breaker**: Circuit breaker settings for each service
