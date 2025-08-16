# Notification Service

## Overview

The Notification Service sends personalized nudges and recommendations to developers based on insights from the analytics service, helping them maintain good coding habits.

## Purpose

This service processes insights and analytics data to:
- Generate personalized recommendations
- Send notifications via various channels
- Manage user notification preferences
- Track notification effectiveness

## Features

- **Personalized Recommendations**: Tailored insights based on individual patterns
- **Multi-Channel Notifications**: Email, desktop notifications, webhooks
- **Preference Management**: User-configurable notification settings
- **Effectiveness Tracking**: Monitor how notifications impact behavior
- **Smart Timing**: Send notifications at optimal times for engagement

## File Structure

```
services/notification-service/
├── src/
│   ├── notification_engine.py    # Main notification processing
│   ├── recommendation_generator.py # Personalized recommendation creation
│   ├── channel_manager.py        # Multi-channel notification delivery
│   └── preference_manager.py     # User preference management
├── tests/
│   ├── test_notification_engine.py
│   ├── test_recommendation_generator.py
│   ├── test_channel_manager.py
│   └── test_preference_manager.py
├── requirements.txt               # Service dependencies
├── Dockerfile                    # Container configuration
└── README.md                     # This file
```

## Data Flow

### Input
- Insights from `shared/data-store/behaviors/insights.jsonl`
- Analytics data from `shared/data-store/analytics/`
- User preferences from `shared/data-store/notifications/preferences.jsonl`

### Output
- Sent notifications to `shared/data-store/notifications/sent.jsonl`
- Updated preferences and settings
- Notification delivery confirmations

## Notification Types

### Behavioral Nudges
- **Commit Reminders**: Gentle reminders to commit regularly
- **Quality Suggestions**: Tips for better commit messages
- **Pattern Alerts**: Notifications about unusual commit patterns
- **Goal Tracking**: Progress updates on coding habit goals

### Productivity Insights
- **Peak Time Alerts**: Notifications about optimal coding times
- **Focus Recommendations**: Suggestions for file organization
- **Break Reminders**: Encouragement to take breaks when needed
- **Achievement Celebrations**: Recognition of good habits

### Learning Opportunities
- **Best Practice Tips**: Educational content about Git practices
- **Tool Recommendations**: Suggestions for productivity tools
- **Community Insights**: Comparisons with team or community patterns
- **Skill Development**: Recommendations for improving specific areas

## Notification Channels

### Email Notifications
- Daily/weekly summaries
- Important pattern alerts
- Achievement notifications
- Educational content

### Desktop Notifications
- Real-time commit reminders
- Quick productivity tips
- Break reminders
- Pattern alerts

### Webhook Integrations
- Slack notifications
- Discord messages
- Custom webhook endpoints
- API integrations

### In-App Notifications
- CLI feedback
- Web interface notifications
- Mobile app alerts
- Browser extensions

## User Preferences

### Notification Frequency
- **Real-time**: Immediate notifications for important events
- **Daily**: Summary notifications once per day
- **Weekly**: Weekly progress reports
- **On-demand**: Only when explicitly requested

### Channel Preferences
- **Primary Channel**: User's preferred notification method
- **Secondary Channels**: Backup notification methods
- **Quiet Hours**: Times when notifications are muted
- **Urgency Levels**: Different channels for different urgency levels

### Content Preferences
- **Insight Types**: Which types of insights to receive
- **Detail Level**: Simple summaries vs. detailed analysis
- **Language**: Preferred language for notifications
- **Tone**: Formal vs. casual notification style

## Integration Points

- **Analytics Service**: Receives insights and pattern data
- **Data Store**: Reads preferences, writes notification history
- **API Gateway**: Provides notification endpoints
- **CLI Interface**: Shows notification status and preferences

## Configuration

### Environment Variables
- `NOTIFICATION_INTERVAL`: How often to check for new notifications
- `EMAIL_SMTP_SERVER`: SMTP server for email notifications
- `WEBHOOK_ENDPOINTS`: List of webhook URLs
- `DEFAULT_PREFERENCES`: Default user notification preferences

### Notification Settings
- **Delivery Timing**: When to send different types of notifications
- **Retry Logic**: How to handle failed notification delivery
- **Rate Limiting**: Limits on notification frequency
- **Content Templates**: Templates for different notification types
