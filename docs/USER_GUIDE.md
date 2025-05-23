# User Guide

Welcome to the macOS Cache Cleaner User Guide. This comprehensive guide will help you get the most out of the cache cleaning utility.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Desktop Application](#desktop-application)
3. [Command Line Usage](#command-line-usage)
4. [Understanding Cache Types](#understanding-cache-types)
5. [Cleaning Strategies](#cleaning-strategies)
6. [AI Assistant](#ai-assistant)
7. [Best Practices](#best-practices)
8. [FAQ](#faq)

## Getting Started

### First Time Setup

1. **Download the repository**:
   ```bash
   git clone https://github.com/ttracx/macos-cache-cleaner.git
   cd macos-cache-cleaner
   ```

2. **Choose your interface**:
   - **Desktop App** (Recommended): Modern GUI with AI assistant
   - **Command Line**: Traditional terminal interface
   - **Python GUI**: Simple Tkinter interface

### System Requirements Check

Before running the cleaner, ensure you have:
- ✅ macOS 10.15 or later (optimized for Apple Silicon)
- ✅ At least 10GB free disk space for safe operation
- ✅ Administrator password (for system maintenance tasks)

## Desktop Application

### Launching the App

```bash
cd electron-app
npm install  # First time only
./run.sh
```

### Interface Overview

#### 1. **Disk Usage Panel**
- Real-time disk space visualization
- Shows used, available, and total space
- Interactive donut chart
- Updates automatically after cleaning

#### 2. **Quick Actions**
Three preset cleaning modes for convenience:

- **🔍 Scan Only**: Preview what can be cleaned without deleting
- **✅ Safe Clean**: Conservative cleaning, skips system maintenance
- **🔥 Deep Clean**: Maximum space recovery with all features

#### 3. **Cleaning Options**
Customize your cleaning preferences:

| Option | Description | Default |
|--------|------------|---------|
| Dry Run | Preview without deleting | ✅ On |
| Verbose Output | Show detailed information | ✅ On |
| Skip Trash | Don't empty the trash | ❌ Off |
| Skip Maintenance | Don't run system scripts | ❌ Off |
| Find Large Files | Scan for space hogs | ❌ Off |

#### 4. **Progress Tracking**
- Real-time status updates
- Animated progress bar
- Space freed counter
- Stop button for cancellation

#### 5. **Output Console**
- Color-coded messages (info, success, warning, error)
- Scrollable history
- Export capability for reports
- Clear button to reset

### Using Quick Actions

#### Scan Only Mode
Perfect for first-time users or regular checkups:
1. Click "🔍 Scan Only"
2. Review the output to see potential space savings
3. No files are deleted in this mode

#### Safe Clean Mode
Recommended for regular maintenance:
1. Click "✅ Safe Clean"
2. Removes non-essential files only
3. Preserves trash and skips system maintenance
4. Ideal for weekly/monthly cleaning

#### Deep Clean Mode
For maximum space recovery:
1. Click "🔥 Deep Clean"
2. Confirm the dialog (requires admin privileges)
3. Performs all cleaning operations
4. Use sparingly (e.g., quarterly)

## Command Line Usage

### Basic Commands

```bash
# Simple cleanup with defaults
./cache_cleaner.py

# Preview mode (recommended first)
./cache_cleaner.py --dry-run

# Verbose output for details
./cache_cleaner.py --verbose

# Combine options
./cache_cleaner.py --dry-run --verbose --find-large-files
```

### Command Line Options

| Flag | Long Option | Description |
|------|-------------|-------------|
| `-h` | `--help` | Show help message |
| `-v` | `--verbose` | Show detailed output |
| | `--dry-run` | Preview without deleting |
| | `--skip-trash` | Skip emptying trash |
| | `--skip-maintenance` | Skip system maintenance |
| | `--find-large-files` | Scan for large files |

### Advanced Usage

#### Scheduling Automatic Cleanup

Add to crontab for weekly cleaning:
```bash
# Edit crontab
crontab -e

# Add this line (runs Sundays at 2 AM)
0 2 * * 0 /path/to/cache_cleaner.py --skip-maintenance
```

#### Creating Custom Aliases

Add to `~/.zshrc` or `~/.bash_profile`:
```bash
# Quick scan alias
alias cache-scan="/path/to/cache_cleaner.py --dry-run --verbose"

# Safe clean alias
alias cache-clean="/path/to/cache_cleaner.py --skip-trash"

# Deep clean alias
alias cache-deep="sudo /path/to/cache_cleaner.py"
```

## Understanding Cache Types

### System Caches (`~/Library/Caches`)
- **What**: Application temporary files
- **Safe to delete**: Yes, apps will recreate as needed
- **Impact**: Apps may load slower initially
- **Space savings**: Usually 1-10GB

### Browser Caches
- **What**: Websites, images, scripts
- **Safe to delete**: Yes, but you'll be logged out
- **Impact**: Websites load slower initially
- **Space savings**: 500MB-5GB per browser

### Development Caches
- **npm** (`~/.npm`): Node.js packages
- **pip** (`~/Library/Caches/pip`): Python packages
- **Xcode** (`~/Library/Developer/Xcode/DerivedData`): Build artifacts
- **Docker**: Container and image caches
- **Safe to delete**: Yes, but may need to re-download
- **Space savings**: Can be 10GB+ for developers

### Log Files
- **What**: Application and system logs
- **Safe to delete**: Old logs (>7 days)
- **Impact**: Lose troubleshooting history
- **Space savings**: 100MB-2GB

### Temporary Files
- **What**: System and app temporary data
- **Safe to delete**: Yes for old files
- **Impact**: None for old files
- **Space savings**: Varies widely

## Cleaning Strategies

### Conservative Approach
For users who prioritize stability:
1. Always run dry-run first
2. Use safe clean mode
3. Keep verbose output on
4. Review results before actual cleaning
5. Clean monthly

### Balanced Approach
For most users:
1. Use safe clean weekly
2. Deep clean quarterly
3. Empty trash during cleaning
4. Skip system maintenance unless needed
5. Monitor disk usage trends

### Aggressive Approach
For power users with backups:
1. Deep clean monthly
2. Include system maintenance
3. Regularly scan for large files
4. Automate with cron jobs
5. Clean development caches frequently

## AI Assistant

### Accessing the AI Assistant

1. Click the 🤖 button in the app header
2. Ensure Ollama is installed and running
3. Wait for "AI Assistant Ready" status

### Features

#### 1. Get Recommendations
- Analyzes your current disk usage
- Considers your cleaning history
- Provides personalized suggestions
- Explains reasoning

#### 2. Analyze Results
- Reviews your last cleanup
- Identifies patterns
- Suggests improvements
- Highlights unusual findings

#### 3. Explain Cache Types
- Interactive education
- Safety information
- Performance impacts
- Rebuild times

#### 4. Free Chat
Ask anything about:
- Disk space management
- Specific cache types
- Troubleshooting issues
- Best practices

### Example Questions

```
"Why is my Xcode cache so large?"
"Is it safe to delete Docker images?"
"How often should I clean my Mac?"
"What's using the most space?"
"Help me free up 50GB safely"
```

## Best Practices

### DO's ✅
1. **Always preview first** with dry-run mode
2. **Start conservative** and increase as comfortable
3. **Keep backups** of important data
4. **Monitor results** to understand impact
5. **Use AI recommendations** for guidance
6. **Clean regularly** (weekly/monthly)
7. **Update the app** for latest safety features

### DON'Ts ❌
1. **Don't clean during important work** (updates, renders)
2. **Don't ignore warnings** in verbose output
3. **Don't clean system files** manually
4. **Don't run multiple instances** simultaneously
5. **Don't disable safety features** without understanding
6. **Don't clean if under 10GB** free space
7. **Don't use sudo unnecessarily**

## FAQ

### Q: How much space will I save?
**A**: Typically 2-20GB depending on usage patterns. Developers and heavy browser users save more.

### Q: Is it safe to use?
**A**: Yes, with built-in safety features:
- Protected directory list
- Age-based cleaning (7-day threshold)
- Dry-run mode
- No critical system files touched

### Q: How often should I clean?
**A**: 
- Light users: Monthly
- Regular users: Bi-weekly
- Heavy users/Developers: Weekly

### Q: What if something breaks?
**A**: 
1. Caches rebuild automatically
2. Log out/in to refresh system caches
3. Restart affected applications
4. Check the output log for issues

### Q: Can I undo a cleaning?
**A**: No, but:
- Use dry-run to preview
- Caches regenerate naturally
- Trash items can be restored (if not emptied)

### Q: Why isn't more space freed?
**A**: Possible reasons:
- macOS purgeable space
- APFS snapshots
- Large files in other locations
- System protection preventing deletion

### Q: Is the AI assistant private?
**A**: Yes, completely:
- Runs locally via Ollama
- No internet connection required
- No data sent externally
- Model stored on your machine

## Troubleshooting

### Common Issues

**"Permission denied" errors**:
- Run with `sudo` for system maintenance
- Check file ownership
- Ensure admin privileges

**AI Assistant offline**:
1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
2. Run setup: `./setup-ollama.sh`
3. Check service: `ollama list`

**App won't start**:
1. Check Node.js version: `node --version` (need 16+)
2. Reinstall dependencies: `npm install`
3. Check for port conflicts

**No space freed after cleaning**:
1. Restart Finder
2. Empty trash manually
3. Check for APFS snapshots: `tmutil listlocalsnapshots /`
4. Restart Mac if needed

### Getting Help

1. Check the [FAQ](#faq) section
2. Ask the AI assistant
3. Review verbose output
4. Check [GitHub Issues](https://github.com/ttracx/macos-cache-cleaner/issues)
5. Contact: mail@tommytracx.com