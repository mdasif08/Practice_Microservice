"""
Configuration Manager - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This module manages application configuration loading and validation.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path

from ..utils.logger import get_logger
from ..utils.error_handler import ConfigurationError

logger = get_logger(__name__)

_config_cache: Optional[Dict[str, Any]] = None


def get_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Get application configuration, loading from file if not cached.
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        Configuration dictionary
        
    Raises:
        ConfigurationError: If configuration cannot be loaded
    """
    global _config_cache
    
    if _config_cache is not None:
        return _config_cache
    
    if config_path is None:
        # Default config path
        config_path = Path(__file__).parent / 'app_config.yaml'
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        logger.warning(f"Config file not found at {config_path}, creating default config")
        create_default_config(config_path)
    
    try:
        config = load_config_file(config_path)
        validate_config(config)
        _config_cache = config
        logger.info(f"Configuration loaded from {config_path}")
        return config
        
    except Exception as e:
        error_msg = f"Failed to load configuration from {config_path}: {e}"
        logger.error(error_msg)
        raise ConfigurationError(error_msg)


def load_config_file(config_path: Path) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
        
    Raises:
        ConfigurationError: If file cannot be loaded or parsed
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        if not isinstance(config, dict):
            raise ConfigurationError("Configuration file must contain a dictionary")
        
        return config
        
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Invalid YAML in configuration file: {e}")
    except Exception as e:
        raise ConfigurationError(f"Failed to read configuration file: {e}")


def create_default_config(config_path: Path) -> None:
    """
    Create a default configuration file.
    
    Args:
        config_path: Path where to create the config file
    """
    default_config = {
        'app': {
            'name': 'CraftNudge AI Agent',
            'version': '1.0.0',
            'environment': 'development'
        },
        'data_store': {
            'base_path': './shared/data-store',
            'behaviors': {
                'commits_file': 'commits.jsonl',
                'patterns_file': 'patterns.jsonl',
                'insights_file': 'insights.jsonl'
            },
            'analytics': {
                'metrics_file': 'metrics.jsonl',
                'trends_file': 'trends.jsonl'
            },
            'notifications': {
                'sent_file': 'sent.jsonl',
                'preferences_file': 'preferences.jsonl'
            }
        },
        'services': {
            'commit_tracker': {
                'enabled': True,
                'auto_track': False,
                'max_commits_per_run': 100
            },
            'analytics': {
                'enabled': True,
                'batch_size': 50,
                'processing_interval': 300
            },
            'notifications': {
                'enabled': False,
                'providers': ['console', 'email'],
                'email': {
                    'smtp_server': 'localhost',
                    'smtp_port': 587,
                    'use_tls': True
                }
            },
            'api_gateway': {
                'enabled': True,
                'host': '0.0.0.0',
                'port': 8000,
                'cors_origins': ['http://localhost:3000']
            }
        },
        'logging': {
            'level': 'INFO',
            'file': './logs/craftnudge.log',
            'format': '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>',
            'rotation': '10 MB',
            'retention': '7 days'
        },
        'security': {
            'api_key_required': False,
            'rate_limiting': {
                'enabled': True,
                'requests_per_minute': 60
            }
        },
        'performance': {
            'max_workers': 4,
            'timeout': 30,
            'cache_ttl': 300
        }
    }
    
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(default_config, file, default_flow_style=False, indent=2)
        
        logger.info(f"Default configuration created at {config_path}")
        
    except Exception as e:
        raise ConfigurationError(f"Failed to create default configuration: {e}")


def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate configuration structure and values.
    
    Args:
        config: Configuration dictionary to validate
        
    Raises:
        ConfigurationError: If configuration is invalid
    """
    required_sections = ['app', 'data_store', 'services', 'logging']
    
    for section in required_sections:
        if section not in config:
            raise ConfigurationError(f"Missing required configuration section: {section}")
        
        if not isinstance(config[section], dict):
            raise ConfigurationError(f"Configuration section '{section}' must be a dictionary")
    
    # Validate data_store section
    data_store = config['data_store']
    if 'base_path' not in data_store:
        raise ConfigurationError("data_store.base_path is required")
    
    # Validate services section
    services = config['services']
    required_services = ['commit_tracker', 'analytics', 'notifications', 'api_gateway']
    
    for service in required_services:
        if service not in services:
            raise ConfigurationError(f"Missing service configuration: {service}")
        
        if not isinstance(services[service], dict):
            raise ConfigurationError(f"Service configuration '{service}' must be a dictionary")
    
    # Validate logging section
    logging_config = config['logging']
    if 'level' not in logging_config:
        raise ConfigurationError("logging.level is required")
    
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if logging_config['level'] not in valid_levels:
        raise ConfigurationError(f"Invalid logging level. Must be one of: {', '.join(valid_levels)}")


def get_config_value(key_path: str, default: Any = None) -> Any:
    """
    Get a configuration value using dot notation.
    
    Args:
        key_path: Dot-separated path to configuration value (e.g., 'services.commit_tracker.enabled')
        default: Default value if key is not found
        
    Returns:
        Configuration value or default
    """
    config = get_config()
    keys = key_path.split('.')
    
    current = config
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


def reload_config() -> Dict[str, Any]:
    """
    Reload configuration from file, clearing cache.
    
    Returns:
        Updated configuration dictionary
    """
    global _config_cache
    _config_cache = None
    return get_config()


def update_config(updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update configuration with new values.
    
    Args:
        updates: Dictionary of configuration updates
        
    Returns:
        Updated configuration dictionary
    """
    global _config_cache
    
    if _config_cache is None:
        _config_cache = get_config()
    
    _config_cache = deep_merge(_config_cache, updates)
    validate_config(_config_cache)
    
    logger.info("Configuration updated successfully")
    return _config_cache


def deep_merge(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.
    
    Args:
        base: Base dictionary
        updates: Updates to apply
        
    Returns:
        Merged dictionary
    """
    result = base.copy()
    
    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


__all__ = [
    'get_config', 'get_config_value', 'reload_config', 'update_config', 'create_default_config'
]
