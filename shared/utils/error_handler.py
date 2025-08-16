"""
Shared Error Handler Utility - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This module provides consistent error handling functionality across all services.
"""

import traceback
import sys
from typing import Dict, Any, Optional, Type
from datetime import datetime, timezone

from .logger import get_logger

logger = get_logger(__name__)


class CraftNudgeError(Exception):
    """Base exception class for CraftNudge AI Agent."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now(timezone.utc).isoformat()


class GitRepositoryError(CraftNudgeError):
    """Raised when Git repository operations fail."""
    pass


class DataStoreError(CraftNudgeError):
    """Raised when data store operations fail."""
    pass


class ValidationError(CraftNudgeError):
    """Raised when data validation fails."""
    pass


class ConfigurationError(CraftNudgeError):
    """Raised when configuration is invalid."""
    pass


def handle_error(
    error: Exception,
    context: str,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Handle and format errors consistently across the application.
    
    Args:
        error: The exception that occurred
        context: Context where the error occurred
        error_code: Optional error code for categorization
        details: Additional error details
        
    Returns:
        Dict containing formatted error information
    """
    error_info = {
        'status': 'error',
        'error': str(error),
        'error_type': type(error).__name__,
        'context': context,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'traceback': traceback.format_exc()
    }
    
    if error_code:
        error_info['error_code'] = error_code
    
    if details:
        error_info['details'] = details
    
    # Add specific error information for known exception types
    if isinstance(error, CraftNudgeError):
        error_info['error_code'] = error.error_code
        error_info['details'] = error.details
        error_info['timestamp'] = error.timestamp
    
    logger.error(f"Error in {context}: {error}")
    logger.debug(f"Error details: {error_info}")
    
    return error_info


def validate_required_fields(data: Dict[str, Any], required_fields: list, context: str) -> None:
    """
    Validate that all required fields are present in the data.
    
    Args:
        data: Data dictionary to validate
        required_fields: List of required field names
        context: Context for error messages
        
    Raises:
        ValidationError: If required fields are missing
    """
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    if missing_fields:
        raise ValidationError(
            f"Missing required fields in {context}: {', '.join(missing_fields)}",
            error_code="MISSING_FIELDS",
            details={'missing_fields': missing_fields, 'context': context}
        )


def validate_field_type(data: Dict[str, Any], field_name: str, expected_type: Type, context: str) -> None:
    """
    Validate that a field has the expected type.
    
    Args:
        data: Data dictionary to validate
        field_name: Name of the field to validate
        expected_type: Expected type for the field
        context: Context for error messages
        
    Raises:
        ValidationError: If field type is incorrect
    """
    if field_name not in data:
        raise ValidationError(
            f"Field '{field_name}' not found in {context}",
            error_code="MISSING_FIELD",
            details={'field_name': field_name, 'context': context}
        )
    
    if not isinstance(data[field_name], expected_type):
        raise ValidationError(
            f"Field '{field_name}' in {context} must be of type {expected_type.__name__}, got {type(data[field_name]).__name__}",
            error_code="INVALID_TYPE",
            details={
                'field_name': field_name,
                'expected_type': expected_type.__name__,
                'actual_type': type(data[field_name]).__name__,
                'context': context
            }
        )


def safe_execute(func, *args, **kwargs) -> Dict[str, Any]:
    """
    Safely execute a function and return the result or error information.
    
    Args:
        func: Function to execute
        *args: Function arguments
        **kwargs: Function keyword arguments
        
    Returns:
        Dict containing either success result or error information
    """
    try:
        result = func(*args, **kwargs)
        return {
            'status': 'success',
            'result': result
        }
    except Exception as e:
        return handle_error(e, f"safe_execute({func.__name__})")


def retry_on_error(
    func,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    *args,
    **kwargs
) -> Dict[str, Any]:
    """
    Execute a function with retry logic on failure.
    
    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay on each retry
        *args: Function arguments
        **kwargs: Function keyword arguments
        
    Returns:
        Dict containing either success result or error information
    """
    import time
    
    last_error = None
    current_delay = delay
    
    for attempt in range(max_retries + 1):
        try:
            result = func(*args, **kwargs)
            return {
                'status': 'success',
                'result': result,
                'attempts': attempt + 1
            }
        except Exception as e:
            last_error = e
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries:
                logger.info(f"Retrying in {current_delay} seconds...")
                time.sleep(current_delay)
                current_delay *= backoff_factor
            else:
                logger.error(f"All {max_retries + 1} attempts failed")
    
    return handle_error(
        last_error,
        f"retry_on_error({func.__name__})",
        error_code="MAX_RETRIES_EXCEEDED",
        details={'max_retries': max_retries, 'attempts': max_retries + 1}
    )


__all__ = [
    'CraftNudgeError', 'GitRepositoryError', 'DataStoreError', 'ValidationError',
    'ConfigurationError', 'handle_error', 'validate_required_fields',
    'validate_field_type', 'safe_execute', 'retry_on_error'
]
