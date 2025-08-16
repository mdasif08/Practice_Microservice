#!/usr/bin/env python3
"""
Track Commit CLI Command - User Story 2.1.1: Behavior Tracker – Git Commit Logger

This module provides the CLI interface for tracking Git commits.
Usage: python track_commit.py [options]
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.commit_tracker_service.src.commit_tracker import CommitTracker
from shared.utils.logger import get_logger, setup_logger
from shared.utils.error_handler import handle_error

logger = get_logger(__name__)


def main():
    """
    Main CLI entry point for commit tracking.
    """
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_logger(
        log_level=args.log_level,
        log_file=args.log_file
    )
    
    try:
        # Initialize commit tracker
        tracker = CommitTracker(repo_path=args.repo_path)
        
        # Execute command based on subcommand
        if args.command == 'latest':
            result = track_latest_commit(tracker, args)
        elif args.command == 'hash':
            result = track_commit_by_hash(tracker, args)
        elif args.command == 'info':
            result = get_repository_info(tracker, args)
        elif args.command == 'list':
            result = list_commits(tracker, args)
        elif args.command == 'search':
            result = search_commits(tracker, args)
        else:
            parser.print_help()
            sys.exit(1)
        
        # Output result
        output_result(result, args.output_format, args.verbose)
        
        # Exit with appropriate code
        if result.get('status') == 'error':
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        error_result = handle_error(e, "cli.main")
        logger.error(f"CLI error: {error_result['error']}")
        output_result(error_result, args.output_format, args.verbose)
        sys.exit(1)


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Track Git commits for behavioral analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python track_commit.py latest                    # Track latest commit
  python track_commit.py hash abc1234              # Track specific commit
  python track_commit.py info                      # Show repository info
  python track_commit.py list --limit 10           # List recent commits
  python track_commit.py search --author "John"    # Search commits by author
        """
    )
    
    # Global options
    parser.add_argument(
        '--repo-path',
        type=str,
        help='Path to Git repository (default: current directory)'
    )
    parser.add_argument(
        '--output-format',
        choices=['json', 'text', 'table'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    parser.add_argument(
        '--log-file',
        type=str,
        help='Log file path'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )
    
    # Latest commit command
    latest_parser = subparsers.add_parser(
        'latest',
        help='Track the latest commit'
    )
    
    # Hash command
    hash_parser = subparsers.add_parser(
        'hash',
        help='Track a specific commit by hash'
    )
    hash_parser.add_argument(
        'commit_hash',
        type=str,
        help='Git commit hash'
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        'info',
        help='Show repository information'
    )
    
    # List command
    list_parser = subparsers.add_parser(
        'list',
        help='List tracked commits'
    )
    list_parser.add_argument(
        '--limit',
        type=int,
        default=20,
        help='Maximum number of commits to list (default: 20)'
    )
    
    # Search command
    search_parser = subparsers.add_parser(
        'search',
        help='Search tracked commits'
    )
    search_parser.add_argument(
        '--author',
        type=str,
        help='Search by author name or email'
    )
    search_parser.add_argument(
        '--message',
        type=str,
        help='Search by commit message keywords'
    )
    search_parser.add_argument(
        '--date-from',
        type=str,
        help='Search from date (ISO format: YYYY-MM-DD)'
    )
    search_parser.add_argument(
        '--date-to',
        type=str,
        help='Search to date (ISO format: YYYY-MM-DD)'
    )
    search_parser.add_argument(
        '--files',
        type=str,
        help='Search by changed files keywords'
    )
    search_parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='Maximum number of results (default: 50)'
    )
    
    return parser


def track_latest_commit(tracker: CommitTracker, args) -> dict:
    """
    Track the latest commit.
    
    Args:
        tracker: Commit tracker instance
        args: Command line arguments
        
    Returns:
        Result dictionary
    """
    logger.info("Tracking latest commit")
    return tracker.log_latest_commit()


def track_commit_by_hash(tracker: CommitTracker, args) -> dict:
    """
    Track a specific commit by hash.
    
    Args:
        tracker: Commit tracker instance
        args: Command line arguments
        
    Returns:
        Result dictionary
    """
    logger.info(f"Tracking commit by hash: {args.commit_hash}")
    return tracker.log_commit_by_hash(args.commit_hash)


def get_repository_info(tracker: CommitTracker, args) -> dict:
    """
    Get repository information.
    
    Args:
        tracker: Commit tracker instance
        args: Command line arguments
        
    Returns:
        Result dictionary
    """
    logger.info("Getting repository information")
    return tracker.get_repository_info()


def list_commits(tracker: CommitTracker, args) -> dict:
    """
    List tracked commits.
    
    Args:
        tracker: Commit tracker instance
        args: Command line arguments
        
    Returns:
        Result dictionary
    """
    logger.info(f"Listing commits (limit: {args.limit})")
    
    # Import here to avoid circular imports
    from services.commit_tracker_service.src.data_writer import DataWriter
    
    data_writer = DataWriter()
    return data_writer.read_commits(limit=args.limit)


def search_commits(tracker: CommitTracker, args) -> dict:
    """
    Search tracked commits.
    
    Args:
        tracker: Commit tracker instance
        args: Command line arguments
        
    Returns:
        Result dictionary
    """
    logger.info("Searching commits")
    
    # Build search criteria
    criteria = {}
    if args.author:
        criteria['author'] = args.author
    if args.message:
        criteria['message'] = args.message
    if args.date_from:
        criteria['date_from'] = args.date_from
    if args.date_to:
        criteria['date_to'] = args.date_to
    if args.files:
        criteria['files'] = args.files
    
    # Import here to avoid circular imports
    from services.commit_tracker_service.src.data_writer import DataWriter
    
    data_writer = DataWriter()
    result = data_writer.search_commits(criteria)
    
    # Apply limit to results
    if 'commits' in result and args.limit:
        result['commits'] = result['commits'][:args.limit]
        result['message'] = f"Found {len(result['commits'])} matching commits (limited to {args.limit})"
    
    return result


def output_result(result: dict, output_format: str, verbose: bool):
    """
    Output the result in the specified format.
    
    Args:
        result: Result dictionary
        output_format: Output format (json, text, table)
        verbose: Whether to show verbose output
    """
    if output_format == 'json':
        print(json.dumps(result, indent=2))
    elif output_format == 'text':
        output_text_result(result, verbose)
    elif output_format == 'table':
        output_table_result(result, verbose)
    else:
        print(json.dumps(result, indent=2))


def output_text_result(result: dict, verbose: bool):
    """
    Output result in text format.
    
    Args:
        result: Result dictionary
        verbose: Whether to show verbose output
    """
    if result.get('status') == 'error':
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        if verbose and 'traceback' in result:
            print(f"\nTraceback:\n{result['traceback']}")
        return
    
    # Handle different result types
    if 'commit_data' in result:
        # Single commit result
        commit = result['commit_data']
        print(f"✅ {result.get('message', 'Commit tracked successfully')}")
        print(f"Hash: {commit.get('hash', 'N/A')}")
        print(f"Author: {commit.get('author', 'N/A')}")
        print(f"Message: {commit.get('message', 'N/A')}")
        print(f"Date: {commit.get('commit_date', 'N/A')}")
        print(f"Files: {len(commit.get('changed_files', []))} files changed")
        
        if verbose:
            print(f"ID: {commit.get('id', 'N/A')}")
            print(f"Email: {commit.get('author_email', 'N/A')}")
            print(f"Body: {commit.get('body', 'N/A')}")
            print(f"Insertions: {commit.get('insertions', 0)}")
            print(f"Deletions: {commit.get('deletions', 0)}")
            if commit.get('changed_files'):
                print("Changed files:")
                for file in commit['changed_files']:
                    print(f"  - {file}")
    
    elif 'repository_info' in result:
        # Repository info result
        info = result['repository_info']
        print(f"✅ {result.get('message', 'Repository information retrieved')}")
        print(f"Path: {info.get('repository_path', 'N/A')}")
        print(f"Remote: {info.get('remote_url', 'N/A')}")
        print(f"Branch: {info.get('current_branch', 'N/A')}")
        print(f"Total commits: {info.get('total_commits', 'N/A')}")
        print(f"Last commit: {info.get('last_commit_date', 'N/A')}")
    
    elif 'commits' in result:
        # Multiple commits result
        commits = result['commits']
        print(f"✅ {result.get('message', f'Found {len(commits)} commits')}")
        
        if not commits:
            print("No commits found.")
            return
        
        for i, commit in enumerate(commits, 1):
            print(f"\n{i}. Commit: {commit.get('hash', 'N/A')[:8]}")
            print(f"   Author: {commit.get('author', 'N/A')}")
            print(f"   Message: {commit.get('message', 'N/A')}")
            print(f"   Date: {commit.get('commit_date', 'N/A')}")
            print(f"   Files: {len(commit.get('changed_files', []))} files changed")
            
            if verbose:
                print(f"   ID: {commit.get('id', 'N/A')}")
                print(f"   Email: {commit.get('author_email', 'N/A')}")
                print(f"   Insertions: {commit.get('insertions', 0)}")
                print(f"   Deletions: {commit.get('deletions', 0)}")
    
    else:
        # Generic result
        print(f"✅ {result.get('message', 'Operation completed successfully')}")
        if verbose:
            print(json.dumps(result, indent=2))


def output_table_result(result: dict, verbose: bool):
    """
    Output result in table format.
    
    Args:
        result: Result dictionary
        verbose: Whether to show verbose output
    """
    try:
        from tabulate import tabulate
    except ImportError:
        print("❌ Error: tabulate package not installed. Install with: pip install tabulate")
        output_text_result(result, verbose)
        return
    
    if result.get('status') == 'error':
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        return
    
    # Handle different result types
    if 'commits' in result and result['commits']:
        # Multiple commits result
        commits = result['commits']
        
        # Prepare table data
        headers = ['Hash', 'Author', 'Message', 'Date', 'Files']
        if verbose:
            headers.extend(['Email', 'Insertions', 'Deletions'])
        
        table_data = []
        for commit in commits:
            row = [
                commit.get('hash', 'N/A')[:8],
                commit.get('author', 'N/A'),
                commit.get('message', 'N/A')[:50] + '...' if len(commit.get('message', '')) > 50 else commit.get('message', 'N/A'),
                commit.get('commit_date', 'N/A')[:10] if commit.get('commit_date') else 'N/A',
                len(commit.get('changed_files', []))
            ]
            
            if verbose:
                row.extend([
                    commit.get('author_email', 'N/A'),
                    commit.get('insertions', 0),
                    commit.get('deletions', 0)
                ])
            
            table_data.append(row)
        
        print(f"✅ {result.get('message', f'Found {len(commits)} commits')}")
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    else:
        # Fallback to text format for other result types
        output_text_result(result, verbose)


if __name__ == "__main__":
    main()
