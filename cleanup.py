#!/usr/bin/env python3
"""
Cleanup script for CrewAI-Backend repository.
Removes temporary files and directories like __pycache__, .pyc files, and other common temp files.
"""

import os
import shutil
import fnmatch
from pathlib import Path
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Clean up temporary files from the repository')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without actually deleting')
    parser.add_argument('--verbose', action='store_true', help='Show detailed information about deleted files')
    return parser.parse_args()

def get_patterns_to_remove():
    """Return patterns of files and directories to remove."""
    return [
        # Python cache files
        '**/__pycache__/',
        '**/*.pyc',
        '**/*.pyo',
        '**/*.pyd',
        '**/.pytest_cache/',
        '**/.coverage',
        '**/.tox/',
        
        # Node.js files
        '**/node_modules/',
        '**/npm-debug.log',
        '**/yarn-error.log',
        
        # Build directories
        '**/build/',
        '**/dist/',
        '**/.next/',
        
        # Environment and IDE files
        '**/.env.local',
        '**/.env.development.local',
        '**/.env.test.local',
        '**/.env.production.local',
        '**/.vscode/',
        '**/.idea/',
        '**/*.swp',
        '**/*.swo',
        
        # OS specific files
        '**/.DS_Store',
        '**/Thumbs.db',
        
        # Log files
        '**/*.log',
        '**/logs/',
        
        # Temporary files
        '**/tmp/',
        '**/temp/',
        '**/*.tmp',
        '**/*.temp',
        
        # Firebase specific
        '**/firebase-debug.log',
        '**/firebase-debug.*.log',
        '**/ui-debug.log',
        '**/ui-debug.*.log',
        '**/pubsub-debug.log',
        '**/pubsub-debug.*.log',
        '**/firestore-debug.log',
        '**/firestore-debug.*.log',
    ]

def find_files_to_remove(base_dir, patterns):
    """Find all files and directories matching the patterns."""
    files_to_remove = []
    dirs_to_remove = []
    
    for pattern in patterns:
        is_dir = pattern.endswith('/')
        if is_dir:
            pattern = pattern[:-1]  # Remove trailing slash
        
        for path in Path(base_dir).glob(pattern):
            if path.is_dir() and is_dir:
                dirs_to_remove.append(path)
            elif path.is_file():
                files_to_remove.append(path)
    
    return files_to_remove, dirs_to_remove

def remove_files(files, dirs, dry_run=False, verbose=False):
    """Remove the specified files and directories."""
    # Sort directories by depth (deepest first) to avoid issues with nested directories
    dirs.sort(key=lambda x: len(str(x).split(os.sep)), reverse=True)
    
    total_files = 0
    total_dirs = 0
    
    # Remove files
    for file_path in files:
        if verbose or dry_run:
            print(f"{'Would remove' if dry_run else 'Removing'} file: {file_path}")
        if not dry_run:
            try:
                os.remove(file_path)
                total_files += 1
            except Exception as e:
                print(f"Error removing file {file_path}: {e}")
    
    # Remove directories
    for dir_path in dirs:
        if verbose or dry_run:
            print(f"{'Would remove' if dry_run else 'Removing'} directory: {dir_path}")
        if not dry_run:
            try:
                shutil.rmtree(dir_path)
                total_dirs += 1
            except Exception as e:
                print(f"Error removing directory {dir_path}: {e}")
    
    return total_files, total_dirs

def main():
    args = parse_args()
    
    # Get the repository root directory (assuming this script is in the root)
    repo_root = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Cleaning up repository: {repo_root}")
    if args.dry_run:
        print("DRY RUN: No files will be deleted")
    
    patterns = get_patterns_to_remove()
    files, dirs = find_files_to_remove(repo_root, patterns)
    
    if not files and not dirs:
        print("No files or directories found to clean up.")
        return
    
    total_files, total_dirs = remove_files(files, dirs, args.dry_run, args.verbose)
    
    if args.dry_run:
        print(f"Would remove {len(files)} files and {len(dirs)} directories")
    else:
        print(f"Removed {total_files} files and {total_dirs} directories")
    
    print("Cleanup complete!")

if __name__ == "__main__":
    main() 