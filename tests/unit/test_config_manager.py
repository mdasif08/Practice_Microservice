"""
Unit tests for shared/config/config_manager.py module.

Tests configuration management functionality.
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

# Import the module under test
from shared.config.config_manager import get_config, load_config_file, create_default_config, validate_config, get_config_value, reload_config, update_config, ConfigurationError


class TestConfigManager:
    """Test cases for config manager."""

    def setup_method(self):
        """Setup method to create test instances."""
        pass

    @patch('shared.config.config_manager.yaml.safe_load')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_config_success(self, mock_file, mock_yaml_load):
        """Test get_config with successful execution."""
        # Use the actual config structure from app_config.yaml
        mock_config = {
            'app': {'name': 'CraftNudge AI Agent', 'version': '1.0.0', 'environment': 'development', 'debug': True},
            'data_store': {
                'base_path': 'shared/data-store',
                'behaviors': {
                    'commits_file': 'behaviors/commits.jsonl',
                    'patterns_file': 'behaviors/patterns.jsonl',
                    'insights_file': 'behaviors/insights.jsonl'
                },
                'analytics': {
                    'metrics_file': 'analytics/metrics.jsonl',
                    'trends_file': 'analytics/trends.jsonl'
                },
                'notifications': {
                    'sent_file': 'notifications/sent.jsonl',
                    'preferences_file': 'notifications/preferences.jsonl'
                }
            },
            'services': {
                'commit_tracker': {
                    'enabled': True, 
                    'batch_size': 100, 
                    'max_retries': 3, 
                    'retry_delay': 1.0
                },
                'analytics': {'enabled': True, 'analysis_interval': 'daily'},
                'notifications': {'enabled': True, 'channels': ['email', 'desktop']},
                'api_gateway': {'enabled': True, 'port': 8000, 'host': 'localhost'}
            },
            'commit_tracker': {
                'git': {
                    'max_commit_history': 1000,
                    'supported_formats': ['jsonl'],
                    'backup_enabled': True,
                    'backup_interval': 'daily'
                },
                'validation': {
                    'require_commit_hash': True,
                    'require_author': True,
                    'require_message': True,
                    'max_message_length': 500,
                    'min_message_length': 3
                },
                'error_handling': {
                    'max_retries': 3,
                    'retry_delay': 1.0,
                    'graceful_fallback': True
                }
            },
            'logging': {
                'level': 'INFO',
                'format': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}',
                'file': {
                    'enabled': True,
                    'path': 'logs/craftnudge.log',
                    'max_size': '10MB',
                    'rotation': 'daily',
                    'retention': '30 days'
                },
                'services': {
                    'commit_tracker': 'INFO',
                    'analytics': 'INFO',
                    'notifications': 'INFO',
                    'api_gateway': 'INFO'
                }
            },
            'analytics': {
                'intervals': {'daily': True, 'weekly': True, 'monthly': True},
                'patterns': {
                    'commit_frequency_threshold': 0.1,
                    'message_quality_threshold': 0.7,
                    'productivity_threshold': 0.5
                },
                'metrics': {
                    'activity_score_weight': 0.4,
                    'consistency_score_weight': 0.3,
                    'quality_score_weight': 0.3
                },
                'insights': {
                    'max_insights_per_day': 5,
                    'insight_expiry_days': 30,
                    'personalized_recommendations': True
                }
            },
            'notifications': {
                'channels': {
                    'email': {'enabled': True, 'smtp_server': 'localhost', 'smtp_port': 587, 'use_tls': True},
                    'desktop': {'enabled': True, 'show_duration': 5},
                    'webhook': {'enabled': False, 'endpoints': []}
                },
                'preferences': {
                    'default_frequency': 'daily',
                    'quiet_hours_start': '22:00',
                    'quiet_hours_end': '08:00',
                    'max_notifications_per_day': 10
                },
                'content': {
                    'language': 'en',
                    'tone': 'friendly',
                    'include_insights': True,
                    'include_recommendations': True
                }
            },
            'api_gateway': {
                'server': {'host': '0.0.0.0', 'port': 8000, 'workers': 4},
                'auth': {
                    'jwt_secret': 'your-secret-key-here',
                    'jwt_algorithm': 'HS256',
                    'token_expiry_hours': 24,
                    'refresh_token_expiry_days': 7
                },
                'rate_limiting': {'default_limit': 100, 'default_window': 60, 'burst_limit': 200},
                'cors': {'allowed_origins': ['*'], 'allowed_methods': ['GET', 'POST', 'PUT', 'DELETE'], 'allowed_headers': ['*']}
            },
            'security': {
                'encryption': {'enabled': False, 'algorithm': 'AES-256-GCM', 'key_rotation_days': 90},
                'access_control': {'require_authentication': True, 'allow_anonymous_reads': False, 'admin_roles': ['admin', 'superuser']},
                'privacy': {'anonymize_commits': False, 'retention_days': 365, 'data_export_enabled': True}
            },
            'performance': {
                'cache': {'enabled': True, 'ttl_seconds': 300, 'max_size': 1000},
                'database': {'connection_pool_size': 10, 'query_timeout': 30, 'batch_size': 100},
                'background_tasks': {'max_workers': 4, 'task_timeout': 300, 'retry_attempts': 3}
            }
        }
        mock_yaml_load.return_value = mock_config
        
        result = get_config()
        assert result == mock_config

    @patch('shared.config.config_manager.yaml.safe_load')
    @patch('builtins.open')
    def test_get_config_file_not_found(self, mock_open, mock_yaml_load):
        """Test get_config when config file is not found."""
        mock_open.side_effect = FileNotFoundError("Config file not found")
        
        result = get_config()
        assert result is not None
        assert 'data_store' in result
        assert 'services' in result
        assert 'logging' in result

    def test_get_config_default_values(self):
        """Test get_config returns default values."""
        with patch('shared.config.config_manager.yaml.safe_load') as mock_yaml_load:
            with patch('builtins.open') as mock_open:
                mock_yaml_load.side_effect = Exception("YAML error")
                
                result = get_config()
                assert result is not None
                assert 'data_store' in result
                assert 'services' in result
                assert 'logging' in result

    @patch('shared.config.config_manager.yaml.safe_load')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_config_file_success(self, mock_file, mock_yaml_load):
        """Test load_config_file with successful execution."""
        mock_config = {'test': 'value'}
        mock_yaml_load.return_value = mock_config
        
        result = load_config_file(Path('/test/config.yaml'))
        assert result == mock_config

    @patch('shared.config.config_manager.yaml.safe_load')
    @patch('builtins.open', new_callable=mock_open, read_data="invalid: yaml: content:")
    def test_load_config_file_invalid_yaml(self, mock_file, mock_yaml_load):
        """Test load_config_file with invalid YAML."""
        import yaml
        mock_yaml_load.side_effect = yaml.YAMLError("Invalid YAML")
        
        with pytest.raises(ConfigurationError) as exc_info:
            load_config_file(Path('/test/config.yaml'))
        # Test that a ConfigurationError is raised (the specific message may vary)
        assert "Failed to read configuration file" in str(exc_info.value)

    @patch('shared.config.config_manager.yaml.safe_load')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_config_file_not_dict(self, mock_file, mock_yaml_load):
        """Test load_config_file when YAML doesn't contain a dictionary."""
        mock_yaml_load.return_value = "not a dict"
        
        with pytest.raises(Exception) as exc_info:
            load_config_file(Path('/test/config.yaml'))
        assert "must contain a dictionary" in str(exc_info.value)

    @patch('shared.config.config_manager.yaml.dump')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_create_default_config_success(self, mock_mkdir, mock_file, mock_yaml_dump):
        """Test create_default_config with successful execution."""
        result = create_default_config(Path('/test/config.yaml'))
        
        assert 'app' in result
        assert 'data_store' in result
        assert 'services' in result
        assert 'logging' in result
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_yaml_dump.assert_called_once()

    def test_validate_config_success(self):
        """Test validate_config with valid configuration."""
        valid_config = {
            'app': {'name': 'Test App'},
            'data_store': {'base_path': '/test/path'},
            'services': {
                'commit_tracker': {},
                'analytics': {},
                'notifications': {},
                'api_gateway': {}
            },
            'logging': {'level': 'INFO'}
        }
        
        # Should not raise an exception
        validate_config(valid_config)

    def test_validate_config_missing_section(self):
        """Test validate_config with missing required section."""
        invalid_config = {
            'app': {'name': 'Test App'},
            'data_store': {'base_path': '/test/path'},
            # Missing services and logging
        }
        
        with pytest.raises(Exception) as exc_info:
            validate_config(invalid_config)
        assert "Missing required configuration section" in str(exc_info.value)

    def test_validate_config_invalid_logging_level(self):
        """Test validate_config with invalid logging level."""
        invalid_config = {
            'app': {'name': 'Test App'},
            'data_store': {'base_path': '/test/path'},
            'services': {
                'commit_tracker': {},
                'analytics': {},
                'notifications': {},
                'api_gateway': {}
            },
            'logging': {'level': 'INVALID_LEVEL'}
        }
        
        with pytest.raises(Exception) as exc_info:
            validate_config(invalid_config)
        assert "Invalid logging level" in str(exc_info.value)

    @patch('shared.config.config_manager.get_config')
    def test_get_config_value_success(self, mock_get_config):
        """Test get_config_value with successful execution."""
        mock_config = {
            'services': {
                'commit_tracker': {
                    'enabled': True
                }
            }
        }
        mock_get_config.return_value = mock_config
        
        result = get_config_value('services.commit_tracker.enabled')
        assert result is True

    @patch('shared.config.config_manager.get_config')
    def test_get_config_value_not_found(self, mock_get_config):
        """Test get_config_value when key is not found."""
        mock_config = {'services': {}}
        mock_get_config.return_value = mock_config
        
        result = get_config_value('services.commit_tracker.enabled', default=False)
        assert result is False

    @patch('shared.config.config_manager.get_config')
    def test_reload_config(self, mock_get_config):
        """Test reload_config functionality."""
        mock_config = {'test': 'value'}
        mock_get_config.return_value = mock_config
        
        result = reload_config()
        assert result == mock_config
        assert mock_get_config.call_count == 1

    @patch('shared.config.config_manager.validate_config')
    @patch('shared.config.config_manager.deep_merge')
    @patch('shared.config.config_manager.get_config')
    def test_update_config_success(self, mock_get_config, mock_deep_merge, mock_validate):
        """Test update_config with successful execution."""
        base_config = {'services': {'commit_tracker': {'enabled': False}}}
        updates = {'services': {'commit_tracker': {'enabled': True}}}
        merged_config = {'services': {'commit_tracker': {'enabled': True}}}
        
        mock_get_config.return_value = base_config
        mock_deep_merge.return_value = merged_config
        
        result = update_config(updates)
        
        mock_deep_merge.assert_called_once_with(base_config, updates)
        mock_validate.assert_called_once_with(merged_config)
        assert result == merged_config

    def test_deep_merge_simple(self):
        """Test deep_merge with simple dictionaries."""
        from shared.config.config_manager import deep_merge
        
        base = {'a': 1, 'b': 2}
        updates = {'b': 3, 'c': 4}
        
        result = deep_merge(base, updates)
        expected = {'a': 1, 'b': 3, 'c': 4}
        assert result == expected

    def test_deep_merge_nested(self):
        """Test deep_merge with nested dictionaries."""
        from shared.config.config_manager import deep_merge
        
        base = {'services': {'commit_tracker': {'enabled': False}}}
        updates = {'services': {'commit_tracker': {'enabled': True}}}
        
        result = deep_merge(base, updates)
        expected = {'services': {'commit_tracker': {'enabled': True}}}
        assert result == expected
