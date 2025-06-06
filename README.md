# macOS Silicon Cache & Temp File Cleaner

A comprehensive utility designed specifically for macOS Silicon (Apple M1/M2/M3) systems to safely clean cache and temporary files, freeing up valuable disk space. Now featuring an AI assistant powered by local LLM for intelligent cleaning recommendations.

**Created by:** Tommy Xaypanya  
**GitHub:** [@ttracx](https://github.com/ttracx)  
**Email:** mail@tommytracx.com  
**Version:** 2.0.0

## Screenshots

![Cache Cleaner Desktop App](docs/images/app-screenshot.png)
*Modern desktop interface with real-time disk visualization and AI assistant*

## Features

### Core Cleaning Features
- 🧹 **Safe Cache Cleaning**: Intelligently cleans user and system caches without affecting critical system files
- 🌐 **Browser Data Cleanup**: Removes browser caches (Safari, Chrome, Firefox, Edge)
- 💻 **Development Cache Cleanup**: Cleans npm, yarn, pip, Docker, and Xcode caches
- 📋 **Log File Management**: Removes old log files while preserving recent ones
- 🗑️ **Trash Management**: Safely empties the Trash
- 🔧 **System Maintenance**: Runs built-in macOS maintenance scripts
- 🔍 **Large File Scanner**: Identifies large files for manual review
- 🔒 **Safety First**: Dry-run mode and intelligent exclusions prevent accidental deletions

### New in Version 2.0
- 🤖 **AI Assistant**: Local LLM-powered assistant for intelligent cleaning recommendations
- 🎨 **Modern Desktop App**: Beautiful Electron-based GUI with native macOS design
- 📊 **Real-time Disk Visualization**: Interactive disk usage charts and statistics
- ⚡ **Quick Actions**: One-click presets for common cleaning scenarios
- 💬 **Interactive Help**: Ask questions and get personalized advice
- 📱 **Progress Tracking**: Live updates during cleaning operations

## Quick Start

### Option 1: Desktop App (Recommended)
```bash
# Navigate to the electron app directory
cd electron-app

# Install dependencies
npm install

# Launch the app
./run.sh
```

### Option 2: Command Line
```bash
# Make the script executable
chmod +x cache_cleaner.py

# Run a dry-run first (recommended)
./cache_cleaner.py --dry-run --verbose

# Run the actual cleanup
./cache_cleaner.py
```

### Option 3: Python GUI (Legacy)
```bash
# Run the Tkinter-based GUI
python3 cache_cleaner_gui.py
```

## Usage Options

```bash
./cache_cleaner.py [OPTIONS]

Options:
  --dry-run             Show what would be deleted without actually deleting
  --verbose, -v         Show detailed output
  --skip-trash          Skip emptying the trash
  --skip-maintenance    Skip running macOS maintenance scripts
  --find-large-files    Scan for large files that could be deleted
  -h, --help           Show help message
```

## What Gets Cleaned

### User Caches
- `~/Library/Caches/*` (selective cleaning)
- `~/Library/Logs/*`
- `~/Library/Application Support/CrashReporter/*`

### Browser Caches
- Safari cache
- Chrome cache
- Firefox cache
- Microsoft Edge cache

### Development Caches
- npm cache (`~/.npm/_cacache`)
- Yarn cache (`~/.yarn/cache`)
- pip cache (`~/Library/Caches/pip`)
- Docker cache
- Xcode DerivedData

### System Temporary Files
- `/tmp/*`
- `/var/tmp/*`
- Files older than 7 days in cache directories

### Log Files
- User log files
- Old system logs (with appropriate permissions)

## Safety Features

- **Protected Directories**: Never touches critical system directories
- **Age-Based Cleaning**: Only removes files older than 7 days from most cache directories
- **Dry Run Mode**: Test what would be deleted before actual cleanup
- **Permission Handling**: Gracefully handles permission errors
- **Exclusion Lists**: Skips essential system caches

## Installation as System Utility

### Option 1: Add to PATH
```bash
# Copy to a directory in your PATH
sudo cp cache_cleaner.py /usr/local/bin/macos-cleaner
sudo chmod +x /usr/local/bin/macos-cleaner

# Now you can run from anywhere
macos-cleaner --dry-run
```

### Option 2: Create an alias
```bash
# Add to your shell profile (~/.zshrc or ~/.bash_profile)
echo 'alias cleaner="/Users/knightdev/macos-cache-cleaner/cache_cleaner.py"' >> ~/.zshrc
source ~/.zshrc

# Use the alias
cleaner --dry-run
```

### Option 3: Create a scheduled job
```bash
# Run weekly cleanup (add to crontab)
crontab -e

# Add this line to run every Sunday at 2 AM
0 2 * * 0 /Users/knightdev/macos-cache-cleaner/cache_cleaner.py --skip-maintenance
```

## Example Output

```
🧹 macOS Silicon Cache & Temp File Cleaner
==================================================
🔍 DRY RUN MODE - No files will be deleted

💾 Current Disk Usage:
  /dev/disk3s1s1  1.8Ti  234Gi  1.0Ti    19%    /

🖥️  Cleaning System Caches...
  Cleaning: /Users/knightdev/Library/Caches
    Freed: 2.3 GB
  Cleaning: /Users/knightdev/Library/Logs  
    Freed: 125.4 MB

🌐 Cleaning Browser Data...
  Cleaning: /Users/knightdev/Library/Caches/com.apple.Safari
    Freed: 856.2 MB

💻 Cleaning Development Caches...
  Cleaning: /Users/knightdev/.npm/_cacache
    Freed: 1.2 GB

==================================================
🎉 Cleaning Complete!
Total space freed: 4.5 GB
(This was a dry run - no files were actually deleted)
```

## Requirements

### Core Requirements
- macOS (designed for Apple Silicon but works on Intel Macs too)
- Python 3.6 or later
- Administrator privileges (for some system maintenance tasks)

### Desktop App Requirements
- Node.js 16 or later
- npm or yarn

### AI Assistant Requirements (Optional)
- Ollama (for local AI features)
- ~4GB disk space for AI model

## Troubleshooting

### Permission Denied Errors
Some cache directories require elevated permissions. The script handles these gracefully, but you can run with `sudo` if needed:

```bash
sudo ./cache_cleaner.py
```

### Large Cache Directories
If you have very large cache directories, the initial scan might take a while. Use `--verbose` to see progress.

### Disk Space Not Freed Immediately
Some space might not appear freed immediately due to how macOS handles disk space reporting. Restart Finder or reboot if needed.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This utility is provided as-is for educational and personal use. Use at your own risk and always backup important data before running cleanup utilities.

## Author

**Tommy Xaypanya**  
- GitHub: [@ttracx](https://github.com/ttracx)
- Email: mail@tommytracx.com
- Website: [tommytracx.com](https://tommytracx.com)

If you find this utility helpful, consider giving it a ⭐ on GitHub!

## AI Assistant Setup

To enable the AI assistant features:

1. **Install Ollama**:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

2. **Run the setup script**:
```bash
cd electron-app
./setup-ollama.sh
```

3. The AI assistant will be available via the 🤖 button in the desktop app

## Building for Distribution

To create a distributable .dmg file:

```bash
cd electron-app
./build.sh
```

The built application will be in the `electron-app/dist/` directory.

## Documentation

- [User Guide](docs/USER_GUIDE.md) - Detailed usage instructions
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Development and contribution guidelines
- [AI Integration](docs/AI_INTEGRATION.md) - AI assistant features and setup
- [API Reference](docs/API_REFERENCE.md) - Command line and programmatic usage
- [Safety Guide](docs/SAFETY_GUIDE.md) - Understanding what's safe to clean

## Changelog

### v2.0.0 (2024)
- Added modern Electron-based desktop application
- Integrated AI assistant with local LLM support
- New interactive disk visualization
- Quick action presets
- Real-time progress tracking
- Improved safety checks

### v1.0.0 (2024)
- Initial release
- Basic cache and temp file cleaning
- Safety features and dry-run mode
- Browser cache cleaning
- Development cache cleaning
- System maintenance integration