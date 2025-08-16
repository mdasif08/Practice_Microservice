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
            print(f"  Path: {info.get('repository_path', 'N/A')}")
            print(f"  Remote: {info.get('remote_url', 'N/A')}")
            print(f"  Branch: {info.get('current_branch', 'N/A')}")
            print(f"  Total Commits: {info.get('total_commits', 'N/A')}")
        else:
            print(f"  ❌ Error: {repo_info.get('message', 'Unknown error')}")
            return
        
        # Track latest commit
        print("\n📝 Tracking Latest Commit:")
        result = tracker.log_latest_commit()
        
        if result['status'] == 'success':
            commit_data = result['commit_data']
            print(f"  ✅ Success: {result['message']}")
            print(f"  Hash: {commit_data['hash'][:8]}")
            print(f"  Author: {commit_data['author']}")
            print(f"  Message: {commit_data['message']}")
            print(f"  Date: {commit_data['commit_date']}")
            print(f"  Files Changed: {len(commit_data['changed_files'])}")
            
            if commit_data['changed_files']:
                print("  Changed Files:")
                for file in commit_data['changed_files'][:5]:  # Show first 5 files
                    print(f"    - {file}")
                if len(commit_data['changed_files']) > 5:
                    print(f"    ... and {len(commit_data['changed_files']) - 5} more")
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
