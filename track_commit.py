#!/usr/bin/env python3
"""
Main CLI Entry Point - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This is the main entry point for the commit tracking CLI.
Usage: python track_commit.py [options]
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the CLI command
from cli.commands.track_commit import main

if __name__ == "__main__":
    main()
