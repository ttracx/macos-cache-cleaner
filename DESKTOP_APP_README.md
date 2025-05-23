# macOS Cache Cleaner - Desktop App

A modern, user-friendly desktop application for cleaning cache and temporary files on macOS. Built with Python and tkinter for a native macOS experience.

**Created by:** Tommy Xaypanya  
**GitHub:** [@ttracx](https://github.com/ttracx)  
**Email:** mail@tommytracx.com  
**Version:** 1.0.0

## 🎯 Features

### Core Functionality
- **🔍 Dry Run Mode**: Preview what will be cleaned before making changes
- **🧹 Safe Cleaning**: Intelligent cache cleaning without touching critical files
- **🌐 Browser Cache Cleanup**: Supports Safari, Chrome, Firefox, and Edge
- **💻 Development Cache Cleanup**: npm, yarn, pip, Docker, Xcode caches
- **📋 Log File Management**: Removes old logs while preserving recent ones
- **🗑️ Trash Management**: Optional trash emptying
- **🔧 System Maintenance**: Runs built-in macOS maintenance scripts

### GUI Features
- **Modern Interface**: Clean, intuitive design with native macOS styling
- **Real-time Progress**: Live updates during cleaning operations
- **Disk Usage Display**: Shows current disk space usage
- **Quick Actions**: Pre-configured cleaning modes (Scan, Safe Clean, Deep Clean)
- **Export Reports**: Save cleaning results to file
- **Threaded Operations**: Non-blocking UI during cleaning

## 🚀 Quick Start

### Option 1: Run Directly
```bash
cd /Users/knightdev/macos-cache-cleaner
python3 cache_cleaner_gui.py
```

### Option 2: Create App Bundle
```bash
cd /Users/knightdev/macos-cache-cleaner
./create_app.sh
```

Then double-click `Cache Cleaner.app` to launch.

### Option 3: Install to Applications
```bash
# After creating the app bundle
mv "Cache Cleaner.app" /Applications/
```

## 🖥️ Interface Overview

### Main Window Sections

1. **Header**: App title and description
2. **Disk Usage**: Current disk space information
3. **Cleaning Options**: Checkboxes for various cleaning preferences
4. **Quick Actions**: 
   - 🔍 **Scan Only**: Dry run with large file detection
   - 🧹 **Safe Clean**: Conservative cleaning (skips trash/maintenance)
   - 🔥 **Deep Clean**: Complete cleaning including trash and maintenance
5. **Action Buttons**: Start/stop controls and utility functions
6. **Progress**: Real-time status and space freed counter
7. **Output**: Detailed cleaning log with color-coded messages
8. **Status Bar**: Current operation status

### Cleaning Options

- **🔍 Dry Run**: Preview mode - shows what would be cleaned without deleting
- **📝 Verbose Output**: Detailed logging of all operations
- **🗑️ Skip Emptying Trash**: Don't empty the Trash during cleaning
- **⚙️ Skip System Maintenance**: Don't run macOS maintenance scripts
- **🔍 Find Large Files**: Scan for files >100MB that could be manually deleted

## 🛡️ Safety Features

### Protected Directories
The app never touches these critical system areas:
- `/System`, `/usr`, `/bin`, `/sbin`, `/etc`
- `/Applications`, `/Library/Frameworks`
- Essential system caches (Spotlight, LaunchServices, etc.)

### Age-Based Cleaning
- Only removes cache files older than 7 days
- Preserves recent files that may still be needed
- Logs and temporary files are cleaned more aggressively

### Dry Run Mode
- **Always recommended first**: See exactly what will be cleaned
- No files are deleted in dry run mode
- Provides size estimates for space that would be freed

## 📁 What Gets Cleaned

### User Caches
- `~/Library/Caches/*` (selective cleaning)
- `~/Library/Logs/*`
- `~/Library/Application Support/CrashReporter/*`
- `~/Library/Containers/*` (old data)

### Browser Caches
- Safari: `~/Library/Caches/com.apple.Safari`
- Chrome: `~/Library/Caches/com.google.Chrome`
- Firefox: `~/Library/Caches/org.mozilla.firefox`
- Edge: `~/Library/Caches/com.microsoft.edgemac`

### Development Tools
- npm: `~/.npm/_cacache`
- Yarn: `~/.yarn/cache`
- pip: `~/Library/Caches/pip`
- Docker: `~/Library/Caches/com.docker.docker`
- Xcode: `~/Library/Developer/Xcode/DerivedData`

### System Files
- `/tmp/*` (temporary files)
- `/var/tmp/*` (system temporary files)
- Old system logs (with proper permissions)

## 🔧 Advanced Usage

### Command Line Integration
The GUI app can also be used alongside the command-line version:

```bash
# Run CLI version for automation
./cache_cleaner.py --dry-run --verbose

# Run GUI for interactive use
python3 cache_cleaner_gui.py
```

### Customization
Edit `cache_cleaner.py` to modify:
- Cache directories to clean
- File age thresholds
- Exclusion patterns
- Cleaning behavior

### Scheduling
Set up automatic cleaning using the command-line version:
```bash
# Add to crontab for weekly cleaning
0 2 * * 0 /Users/knightdev/macos-cache-cleaner/cache_cleaner.py --skip-maintenance
```

## 🚨 Troubleshooting

### App Won't Launch
1. **Security Warning**: Right-click → Open → "Open Anyway"
2. **Python Missing**: Install Python 3 from python.org
3. **Permissions**: Try running from Terminal first

### Cleaning Issues
1. **Permission Denied**: Some system caches require admin rights
2. **Space Not Freed**: Restart Finder or reboot to update disk usage
3. **Slow Scanning**: Large cache directories take time to analyze

### GUI Problems
1. **Window Too Small**: Drag corners to resize
2. **Output Not Updating**: Cleaning operations run in background threads
3. **Stop Button**: Cannot force-stop mid-operation for safety

## 📊 Example Cleaning Results

Typical space savings by category:
- **Browser Caches**: 500MB - 2GB
- **Development Tools**: 1GB - 5GB  
- **System Caches**: 200MB - 1GB
- **Logs & Crash Reports**: 50MB - 500MB
- **Temporary Files**: 100MB - 1GB

**Total typical savings**: 2GB - 10GB

## 🔄 Updates

To update the app:
1. Download new version of `cache_cleaner_gui.py`
2. Run `./create_app.sh` to rebuild the app bundle
3. Replace old app in Applications folder

## 📝 Version History

### v1.0.0 (Current)
- Initial GUI release
- Modern tkinter interface
- Threaded cleaning operations
- Real-time progress updates
- App bundle creation
- Quick action presets

## 🤝 Contributing

The desktop app is built on the command-line utility. To contribute:
1. Test thoroughly in dry-run mode
2. Ensure GUI remains responsive during operations
3. Add appropriate error handling
4. Update documentation

## 📄 License

Provided as-is for educational and personal use. Always backup important data before running any cleaning utility.

## 👨‍💻 Author

**Tommy Xaypanya**  
- GitHub: [@ttracx](https://github.com/ttracx)
- Email: mail@tommytracx.com
- Website: [tommytracx.com](https://tommytracx.com)

If you find this app useful, consider giving it a ⭐ on GitHub!

---

**Note**: This desktop app provides the same safety and functionality as the command-line version but with an intuitive graphical interface perfect for regular users.