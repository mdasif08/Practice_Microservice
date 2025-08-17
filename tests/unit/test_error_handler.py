"""
Unit tests for shared/utils/error_handler.py module.

Tests error handling functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
import traceback

# Import the module under test
from shared.utils.error_handler import (
    handle_error, validate_required_fields, validate_field_type,
    safe_execute, retry_on_error, CraftNudgeError, GitRepositoryError,
    DataStoreError, ValidationError, ConfigurationError
)


class TestErrorHandler:
    """Test cases for error handler."""

    def setup_method(self):
        """Setup method to create test instances."""
        pass

    def test_handle_error_with_exception(self):
        """Test handle_error with exception."""
        test_exception = ValueError("Test error")
        result = handle_error(test_exception, "test_function")
        
        assert result['status'] == 'error'
        assert 'error' in result
        assert 'Test error' in result['error']
        assert result['error_type'] == 'ValueError'
        assert result['context'] == 'test_function'
        assert 'timestamp' in result
        assert 'traceback' in result

    def test_handle_error_with_string(self):
        """Test handle_error with string error."""
        test_error = "Test error message"
        result = handle_error(test_error, "test_function")
        
        assert result['status'] == 'error'
        assert 'error' in result
        assert 'Test error message' in result['error']
        assert result['error_type'] == 'str'
        assert result['context'] == 'test_function'

    def test_handle_error_with_context(self):
        """Test handle_error with context information."""
        test_exception = Exception("Test exception")
        result = handle_error(test_exception, "test_function", "test_context")
        
        assert result['status'] == 'error'
        assert 'error' in result
        assert 'Test exception' in result['error']
        assert result['context'] == 'test_function'

    def test_handle_error_with_error_code_and_details(self):
        """Test handle_error with error code and details."""
        test_exception = Exception("Test exception")
        details = {'key': 'value'}
        result = handle_error(test_exception, "test_function", "TEST_ERROR", details)
        
        assert result['status'] == 'error'
        assert result['error_code'] == 'TEST_ERROR'
        assert result['details'] == details

    def test_handle_error_with_craftnudge_error(self):
        """Test handle_error with CraftNudgeError."""
        test_error = CraftNudgeError("Test error", "TEST_CODE", {'detail': 'value'})
        result = handle_error(test_error, "test_function")
        
        assert result['status'] == 'error'
        assert result['error_code'] == 'TEST_CODE'
        assert result['details'] == {'detail': 'value'}
        assert result['timestamp'] == test_error.timestamp

    def test_validate_required_fields_success(self):
        """Test validate_required_fields with valid data."""
        data = {'field1': 'value1', 'field2': 'value2'}
        required_fields = ['field1', 'field2']
        
        # Should not raise an exception
        validate_required_fields(data, required_fields, "test_context")

    def test_validate_required_fields_missing_field(self):
        """Test validate_required_fields with missing field."""
        data = {'field1': 'value1'}
        required_fields = ['field1', 'field2']
        
        with pytest.raises(ValidationError) as exc_info:
            validate_required_fields(data, required_fields, "test_context")
        
        assert "Missing required fields" in str(exc_info.value)
        assert exc_info.value.error_code == "MISSING_FIELDS"
        assert exc_info.value.details['missing_fields'] == ['field2']

    def test_validate_required_fields_none_field(self):
        """Test validate_required_fields with None field."""
        data = {'field1': 'value1', 'field2': None}
        required_fields = ['field1', 'field2']
        
        with pytest.raises(ValidationError) as exc_info:
            validate_required_fields(data, required_fields, "test_context")
        
        assert "Missing required fields" in str(exc_info.value)
        assert 'field2' in exc_info.value.details['missing_fields']

    def test_validate_field_type_success(self):
        """Test validate_field_type with correct type."""
        data = {'field1': 'string_value', 'field2': 123}
        
        # Should not raise an exception
        validate_field_type(data, 'field1', str, "test_context")
        validate_field_type(data, 'field2', int, "test_context")

    def test_validate_field_type_missing_field(self):
        """Test validate_field_type with missing field."""
        data = {'field1': 'value1'}
        
        with pytest.raises(ValidationError) as exc_info:
            validate_field_type(data, 'field2', str, "test_context")
        
        assert "Field 'field2' not found" in str(exc_info.value)
        assert exc_info.value.error_code == "MISSING_FIELD"

    def test_validate_field_type_wrong_type(self):
        """Test validate_field_type with wrong type."""
        data = {'field1': 'string_value'}
        
        with pytest.raises(ValidationError) as exc_info:
            validate_field_type(data, 'field1', int, "test_context")
        
        assert "must be of type int" in str(exc_info.value)
        assert exc_info.value.error_code == "INVALID_TYPE"
        assert exc_info.value.details['expected_type'] == 'int'
        assert exc_info.value.details['actual_type'] == 'str'

    def test_safe_execute_success(self):
        """Test safe_execute with successful execution."""
        def test_func(x, y):
            return x + y
        
        result = safe_execute(test_func, 2, 3)
        
        assert result['status'] == 'success'
        assert result['result'] == 5

    def test_safe_execute_error(self):
        """Test safe_execute with error."""
        def test_func():
            raise ValueError("Test error")
        
        result = safe_execute(test_func)
        
        assert result['status'] == 'error'
        assert 'Test error' in result['error']
        assert 'safe_execute' in result['context']

    @patch('time.sleep')
    def test_retry_on_error_success_first_attempt(self, mock_sleep):
        """Test retry_on_error with success on first attempt."""
        def test_func():
            return "success"
        
        result = retry_on_error(test_func, max_retries=3)
        
        assert result['status'] == 'success'
        assert result['result'] == "success"
        assert result['attempts'] == 1
        mock_sleep.assert_not_called()

    @patch('time.sleep')
    def test_retry_on_error_success_after_retries(self, mock_sleep):
        """Test retry_on_error with success after retries."""
        call_count = 0
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary error")
            return "success"
        
        result = retry_on_error(test_func, max_retries=3, delay=0.1)
        
        assert result['status'] == 'success'
        assert result['result'] == "success"
        assert result['attempts'] == 3
        assert mock_sleep.call_count == 2  # Called twice for retries

    @patch('time.sleep')
    def test_retry_on_error_all_attempts_fail(self, mock_sleep):
        """Test retry_on_error with all attempts failing."""
        def test_func():
            raise ValueError("Persistent error")
        
        result = retry_on_error(test_func, max_retries=2, delay=0.1)
        
        assert result['status'] == 'error'
        assert 'Persistent error' in result['error']
        assert result['error_code'] == 'MAX_RETRIES_EXCEEDED'
        assert result['details']['max_retries'] == 2
        assert result['details']['attempts'] == 3
        assert mock_sleep.call_count == 2

    @patch('time.sleep')
    def test_retry_on_error_backoff_factor(self, mock_sleep):
        """Test retry_on_error with backoff factor."""
        call_count = 0
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary error")
            return "success"
        
        result = retry_on_error(test_func, max_retries=3, delay=1.0, backoff_factor=2.0)
        
        assert result['status'] == 'success'
        # Check that sleep was called with increasing delays
        expected_calls = [((1.0,),), ((2.0,),)]  # 1.0, then 2.0
        assert mock_sleep.call_args_list == expected_calls


class TestCraftNudgeError:
    """Test cases for CraftNudgeError and its subclasses."""

    def test_craftnudge_error_initialization(self):
        """Test CraftNudgeError initialization."""
        error = CraftNudgeError("Test message", "TEST_CODE", {'detail': 'value'})
        
        assert error.message == "Test message"
        assert error.error_code == "TEST_CODE"
        assert error.details == {'detail': 'value'}
        # Check that timestamp is a valid ISO format string
        assert isinstance(error.timestamp, str)
        assert len(error.timestamp) > 0

    def test_craftnudge_error_default_values(self):
        """Test CraftNudgeError with default values."""
        error = CraftNudgeError("Test message")
        
        assert error.message == "Test message"
        assert error.error_code is None
        assert error.details == {}

    def test_git_repository_error(self):
        """Test GitRepositoryError."""
        error = GitRepositoryError("Git error", "GIT_ERROR")
        
        assert isinstance(error, CraftNudgeError)
        assert error.message == "Git error"
        assert error.error_code == "GIT_ERROR"

    def test_data_store_error(self):
        """Test DataStoreError."""
        error = DataStoreError("Data store error", "DATA_ERROR")
        
        assert isinstance(error, CraftNudgeError)
        assert error.message == "Data store error"
        assert error.error_code == "DATA_ERROR"

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("Validation error", "VALIDATION_ERROR")
        
        assert isinstance(error, CraftNudgeError)
        assert error.message == "Validation error"
        assert error.error_code == "VALIDATION_ERROR"

    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError("Config error", "CONFIG_ERROR")
        
        assert isinstance(error, CraftNudgeError)
        assert error.message == "Config error"
        assert error.error_code == "CONFIG_ERROR"
