#!/usr/bin/env python3
"""
Basic Usage Example - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This example demonstrates basic usage of the commit tracking functionality.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.commit_tracker_service.src.commit_tracker import CommitTracker
from shared.utils.logger import setup_logger, get_logger

# Setup logging
setup_logger(log_level="INFO")
logger = get_logger(__name__)


def main():
    """Demonstrate basic commit tracking functionality."""
    
    print("🚀 CraftNudge AI Agent - Commit Tracking Example")
    print("=" * 50)
    
    try:
        # Initialize commit tracker
        tracker = CommitTracker()
        
        # Get repository information
        print("\n📋 Repository Information:")
        repo_info = tracker.get_repository_info()
        
        if repo_info['status'] == 'success':
            info = repo_info['repository_info']
            print(f"  Path: {info.get('repository_path') if info.get('repository_path') is not None else 'N/A'}")
            print(f"  Remote: {info.get('remote_url') if info.get('remote_url') is not None else 'N/A'}")
            print(f"  Branch: {info.get('current_branch') if info.get('current_branch') is not None else 'N/A'}")
            print(f"  Total Commits: {info.get('total_commits') if info.get('total_commits') is not None else 'N/A'}")
        else:
            print(f"  ❌ Error: {repo_info.get('message', 'Unknown error')}")
            return
        
        # Track latest commit
        print("\n📝 Tracking Latest Commit:")
        result = tracker.log_latest_commit()
        
        if result['status'] == 'success':
            commit_data = result['commit_data']
            print(f"  ✅ Success: {result['message']}")
            hash_value = commit_data.get('hash')
            print(f"  Hash: {hash_value[:8] if hash_value else 'N/A'}")
            print(f"  Author: {commit_data.get('author') if commit_data.get('author') is not None else 'N/A'}")
            print(f"  Message: {commit_data.get('message') if commit_data.get('message') is not None else 'N/A'}")
            print(f"  Date: {commit_data.get('commit_date') if commit_data.get('commit_date') is not None else 'N/A'}")
            print(f"  Files Changed: {len(commit_data.get('changed_files') or [])}")
            
            changed_files = commit_data.get('changed_files', [])
            if changed_files:
                print("  Changed Files:")
                for file in changed_files[:5]:  # Show first 5 files
                    print(f"    - {file}")
                if len(changed_files) > 5:
                    print(f"    ... and {len(changed_files) - 5} more")
        else:
            print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
        
        print("\n🎯 Example completed successfully!")
        print("\n💡 Try running: python track_commit.py --help")
        print("   for more CLI options and commands.")
        
    except Exception as e:
        logger.error(f"Example failed: {e}")
        print(f"\n❌ Example failed: {e}")
        print("Make sure you're in a Git repository and have the required dependencies installed.")


if __name__ == "__main__":
    main()
