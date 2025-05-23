#!/usr/bin/env python3
"""
macOS Silicon Cache & Temp File Cleaner Utility
Safely cleans various cache directories to free up disk space

Created by: Tommy Xaypanya
GitHub: https://github.com/ttracx
Email: mail@tommytracx.com
Version: 1.0.0
"""

import os
import shutil
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Tuple
import time

class MacOSCacheCleaner:
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.total_freed = 0
        self.home_dir = Path.home()
        
        # Cache directories to clean
        self.cache_dirs = [
            # User-specific caches
            self.home_dir / "Library/Caches",
            self.home_dir / "Library/Logs",
            self.home_dir / "Library/Application Support/CrashReporter",
            self.home_dir / "Library/Containers",
            
            # System temp directories
            Path("/tmp"),
            Path("/var/tmp"),
            Path("/var/folders"),
            
            # Browser caches
            self.home_dir / "Library/Caches/com.apple.Safari",
            self.home_dir / "Library/Caches/com.google.Chrome",
            self.home_dir / "Library/Caches/org.mozilla.firefox",
            self.home_dir / "Library/Caches/com.microsoft.edgemac",
            
            # Development caches
            self.home_dir / ".npm/_cacache",
            self.home_dir / ".yarn/cache",
            self.home_dir / "Library/Caches/pip",
            self.home_dir / ".cache",
            self.home_dir / "Library/Caches/com.docker.docker",
            self.home_dir / "Library/Developer/Xcode/DerivedData",
            
            # macOS specific
            self.home_dir / "Library/Caches/com.apple.akd",
            self.home_dir / "Library/Caches/com.apple.bird",
            self.home_dir / "Library/Caches/CloudKit",
            self.home_dir / "Library/Caches/com.apple.iTunes",
            self.home_dir / "Library/Caches/com.apple.Music",
        ]
        
        # Files/patterns to specifically target
        self.file_patterns = [
            "*.log",
            "*.crash",
            "*.tmp",
            "*.temp",
            "*.cache",
            ".DS_Store",
            "Thumbs.db",
        ]
        
        # Directories to exclude from cleaning
        self.exclude_dirs = {
            "com.apple.akd",  # Keep some essential system caches
            "com.apple.LaunchServices",
            "com.apple.spotlight",
        }

    def get_dir_size(self, path: Path) -> int:
        """Calculate directory size in bytes"""
        try:
            total = 0
            for entry in path.rglob('*'):
                if entry.is_file():
                    try:
                        total += entry.stat().st_size
                    except (OSError, PermissionError):
                        continue
            return total
        except (OSError, PermissionError):
            return 0

    def format_size(self, size_bytes: int) -> str:
        """Format bytes into human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def is_safe_to_delete(self, path: Path) -> bool:
        """Check if path is safe to delete"""
        path_str = str(path).lower()
        
        # Never delete these critical directories
        critical_paths = [
            '/system', '/usr', '/bin', '/sbin', '/etc',
            '/applications', '/library/frameworks',
            '/library/extensions', '/library/preferences'
        ]
        
        for critical in critical_paths:
            if path_str.startswith(critical):
                return False
                
        # Check exclude list
        for exclude in self.exclude_dirs:
            if exclude in path_str:
                return False
                
        return True

    def clean_directory(self, cache_dir: Path) -> int:
        """Clean a specific cache directory"""
        if not cache_dir.exists():
            if self.verbose:
                print(f"  Directory doesn't exist: {cache_dir}")
            return 0
            
        if not self.is_safe_to_delete(cache_dir):
            if self.verbose:
                print(f"  Skipping protected directory: {cache_dir}")
            return 0

        size_before = self.get_dir_size(cache_dir)
        freed = 0
        
        try:
            print(f"  Cleaning: {cache_dir}")
            
            if cache_dir.name in ['tmp', 'Logs', 'CrashReporter']:
                # For temp and log directories, clean contents but keep directory
                for item in cache_dir.iterdir():
                    try:
                        if item.is_file():
                            if not self.dry_run:
                                item.unlink()
                            freed += item.stat().st_size
                        elif item.is_dir() and self.is_safe_to_delete(item):
                            item_size = self.get_dir_size(item)
                            if not self.dry_run:
                                shutil.rmtree(item)
                            freed += item_size
                    except (OSError, PermissionError) as e:
                        if self.verbose:
                            print(f"    Warning: Could not delete {item}: {e}")
            else:
                # For other cache dirs, clean old files (>7 days)
                cutoff_time = time.time() - (7 * 24 * 3600)  # 7 days ago
                
                for item in cache_dir.rglob('*'):
                    try:
                        if item.is_file() and item.stat().st_mtime < cutoff_time:
                            file_size = item.stat().st_size
                            if not self.dry_run:
                                item.unlink()
                            freed += file_size
                    except (OSError, PermissionError) as e:
                        if self.verbose:
                            print(f"    Warning: Could not delete {item}: {e}")
                            
        except (OSError, PermissionError) as e:
            print(f"  Error accessing {cache_dir}: {e}")
            return 0
            
        if freed > 0:
            print(f"    Freed: {self.format_size(freed)}")
        elif self.verbose:
            print(f"    Nothing to clean")
            
        return freed

    def clean_browser_data(self):
        """Clean browser cache and temporary data"""
        print("\n🌐 Cleaning Browser Data...")
        
        # Safari
        safari_cache = self.home_dir / "Library/Caches/com.apple.Safari"
        if safari_cache.exists():
            freed = self.clean_directory(safari_cache)
            self.total_freed += freed
            
        # Chrome
        chrome_cache = self.home_dir / "Library/Caches/com.google.Chrome"
        if chrome_cache.exists():
            freed = self.clean_directory(chrome_cache)
            self.total_freed += freed

    def clean_system_caches(self):
        """Clean system-level caches"""
        print("\n🖥️  Cleaning System Caches...")
        
        for cache_dir in [d for d in self.cache_dirs if 'Library/Caches' in str(d)]:
            freed = self.clean_directory(cache_dir)
            self.total_freed += freed

    def clean_temp_files(self):
        """Clean temporary files"""
        print("\n🗑️  Cleaning Temporary Files...")
        
        temp_dirs = [Path("/tmp"), Path("/var/tmp")]
        for temp_dir in temp_dirs:
            freed = self.clean_directory(temp_dir)
            self.total_freed += freed

    def clean_development_caches(self):
        """Clean development-related caches"""
        print("\n💻 Cleaning Development Caches...")
        
        dev_caches = [
            self.home_dir / ".npm/_cacache",
            self.home_dir / ".yarn/cache", 
            self.home_dir / "Library/Caches/pip",
            self.home_dir / ".cache",
            self.home_dir / "Library/Developer/Xcode/DerivedData",
        ]
        
        for cache_dir in dev_caches:
            if cache_dir.exists():
                freed = self.clean_directory(cache_dir)
                self.total_freed += freed

    def clean_logs(self):
        """Clean log files"""
        print("\n📋 Cleaning Log Files...")
        
        log_dirs = [
            self.home_dir / "Library/Logs",
            Path("/var/log"),
        ]
        
        for log_dir in log_dirs:
            if log_dir.exists():
                freed = self.clean_directory(log_dir)
                self.total_freed += freed

    def empty_trash(self):
        """Empty the Trash"""
        print("\n🗂️  Emptying Trash...")
        
        try:
            trash_dir = self.home_dir / ".Trash"
            if trash_dir.exists():
                size_before = self.get_dir_size(trash_dir)
                if not self.dry_run:
                    # Use osascript to empty trash safely
                    subprocess.run(['osascript', '-e', 'tell application "Finder" to empty trash'], 
                                 capture_output=True)
                print(f"  Freed: {self.format_size(size_before)}")
                self.total_freed += size_before
        except Exception as e:
            print(f"  Error emptying trash: {e}")

    def run_maintenance_scripts(self):
        """Run built-in macOS maintenance scripts"""
        print("\n🔧 Running macOS Maintenance...")
        
        if not self.dry_run:
            try:
                # Run periodic daily maintenance
                subprocess.run(['sudo', 'periodic', 'daily'], capture_output=True)
                print("  ✓ Daily maintenance completed")
                
                # Rebuild dyld cache
                subprocess.run(['sudo', 'update_dyld_shared_cache', '-force'], capture_output=True)
                print("  ✓ Dynamic linker cache rebuilt")
                
            except Exception as e:
                print(f"  Error running maintenance: {e}")
        else:
            print("  (Dry run - maintenance scripts not executed)")

    def scan_large_files(self, min_size_mb: int = 100):
        """Find large files that could be candidates for deletion"""
        print(f"\n🔍 Scanning for files larger than {min_size_mb}MB...")
        
        large_files = []
        min_size_bytes = min_size_mb * 1024 * 1024
        
        search_dirs = [
            self.home_dir / "Downloads",
            self.home_dir / "Desktop", 
            self.home_dir / "Documents",
            self.home_dir / "Movies",
        ]
        
        for search_dir in search_dirs:
            if search_dir.exists():
                try:
                    for file_path in search_dir.rglob('*'):
                        if file_path.is_file():
                            try:
                                size = file_path.stat().st_size
                                if size > min_size_bytes:
                                    large_files.append((file_path, size))
                            except (OSError, PermissionError):
                                continue
                except (OSError, PermissionError):
                    continue
        
        # Sort by size (largest first)
        large_files.sort(key=lambda x: x[1], reverse=True)
        
        if large_files:
            print(f"  Found {len(large_files)} large files:")
            for file_path, size in large_files[:10]:  # Show top 10
                print(f"    {self.format_size(size)} - {file_path}")
        else:
            print("  No large files found")

    def run(self, skip_trash: bool = False, skip_maintenance: bool = False, 
            find_large_files: bool = False):
        """Run the complete cleaning process"""
        print("🧹 macOS Silicon Cache & Temp File Cleaner")
        print("=" * 50)
        
        if self.dry_run:
            print("🔍 DRY RUN MODE - No files will be deleted")
            print()
        
        # Show initial disk usage
        try:
            result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
            print("💾 Current Disk Usage:")
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                print(f"  {lines[1]}")
            print()
        except:
            pass
        
        self.clean_system_caches()
        self.clean_browser_data()
        self.clean_temp_files()
        self.clean_development_caches()
        self.clean_logs()
        
        if not skip_trash:
            self.empty_trash()
            
        if not skip_maintenance:
            self.run_maintenance_scripts()
            
        if find_large_files:
            self.scan_large_files()
        
        print("\n" + "=" * 50)
        print(f"🎉 Cleaning Complete!")
        print(f"Total space freed: {self.format_size(self.total_freed)}")
        
        if self.dry_run:
            print("(This was a dry run - no files were actually deleted)")


def main():
    parser = argparse.ArgumentParser(description='macOS Silicon Cache & Temp File Cleaner')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be deleted without actually deleting')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output')
    parser.add_argument('--skip-trash', action='store_true',
                       help='Skip emptying the trash')
    parser.add_argument('--skip-maintenance', action='store_true', 
                       help='Skip running macOS maintenance scripts')
    parser.add_argument('--find-large-files', action='store_true',
                       help='Scan for large files that could be deleted')
    
    args = parser.parse_args()
    
    try:
        cleaner = MacOSCacheCleaner(dry_run=args.dry_run, verbose=args.verbose)
        cleaner.run(skip_trash=args.skip_trash, 
                   skip_maintenance=args.skip_maintenance,
                   find_large_files=args.find_large_files)
    except KeyboardInterrupt:
        print("\n❌ Cleaning cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during cleaning: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()