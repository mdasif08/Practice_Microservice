# Behavior Analytics Service

## Overview

The Behavior Analytics Service analyzes Git commit patterns and generates insights to help developers understand their coding habits and improve productivity.

## Purpose

This service processes commit data from the data store to:
- Identify behavioral patterns in commit history
- Calculate productivity metrics
- Generate personalized insights
- Trigger notifications based on patterns

## Features

- **Pattern Analysis**: Identifies commit frequency, timing, and message patterns
- **Productivity Metrics**: Calculates lines of code, commit size, and activity trends
- **Insight Generation**: Creates personalized recommendations based on patterns
- **Trend Analysis**: Tracks changes in behavior over time
- **Alert System**: Triggers notifications for significant pattern changes

## File Structure

```
services/behavior-analytics-service/
├── src/
│   ├── analytics_engine.py      # Main analytics processing
│   ├── pattern_detector.py      # Pattern detection algorithms
│   ├── metrics_calculator.py    # Productivity metrics calculation
│   └── insight_generator.py     # Insight and recommendation generation
├── tests/
│   ├── test_analytics_engine.py
│   ├── test_pattern_detector.py
│   ├── test_metrics_calculator.py
│   └── test_insight_generator.py
├── requirements.txt             # Service dependencies
├── Dockerfile                  # Container configuration
└── README.md                   # This file
```

## Data Flow

### Input
- Commit data from `shared/data-store/behaviors/commits.jsonl`
- User preferences and settings
- Historical analytics data

### Output
- Metrics data to `shared/data-store/analytics/metrics.jsonl`
- Trend analysis to `shared/data-store/analytics/trends.jsonl`
- Insights to `shared/data-store/behaviors/insights.jsonl`
- Notifications to notification service

## Analytics Capabilities

### Commit Pattern Analysis
- **Frequency Analysis**: Commit frequency by time of day, day of week
- **Message Analysis**: Commit message quality and consistency
- **File Analysis**: Most frequently modified files and directories
- **Size Analysis**: Commit size patterns and trends

### Productivity Metrics
- **Lines of Code**: Insertions, deletions, and net changes
- **Activity Score**: Weighted score based on commit frequency and quality
- **Consistency Score**: Regularity of commit patterns
- **Quality Score**: Based on commit message quality and file organization

### Behavioral Insights
- **Peak Hours**: Times when developer is most productive
- **Commit Gaps**: Periods of inactivity that might indicate issues
- **Quality Trends**: Changes in commit message quality over time
- **File Focus**: Concentration on specific files or areas

## Integration Points

- **Data Store**: Reads commit data, writes analytics results
- **Notification Service**: Sends insights and alerts
- **API Gateway**: Provides analytics endpoints
- **CLI Interface**: Exposes analytics commands

## Configuration

### Environment Variables
- `ANALYTICS_INTERVAL`: How often to run analytics (default: daily)
- `PATTERN_THRESHOLDS`: Thresholds for pattern detection
- `INSIGHT_FREQUENCY`: How often to generate insights
- `NOTIFICATION_TRIGGERS`: Conditions for triggering notifications

### Analytics Settings
- **Time Windows**: Daily, weekly, monthly analysis periods
- **Pattern Sensitivity**: Adjustable thresholds for pattern detection
- **Insight Types**: Configurable types of insights to generate
- **Notification Rules**: Customizable notification triggers
