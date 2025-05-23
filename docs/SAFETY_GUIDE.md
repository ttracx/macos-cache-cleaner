# Safety Guide

This comprehensive guide explains the safety mechanisms built into the macOS Cache Cleaner and helps you understand what's safe to clean on your system.

## Table of Contents

1. [Safety Overview](#safety-overview)
2. [Protected Directories](#protected-directories)
3. [Cache Types Explained](#cache-types-explained)
4. [Risk Levels](#risk-levels)
5. [Recovery Procedures](#recovery-procedures)
6. [Best Practices](#best-practices)
7. [What NOT to Clean](#what-not-to-clean)

## Safety Overview

The macOS Cache Cleaner is designed with multiple layers of safety:

### Built-in Protections

1. **Protected Directory List**: Critical system directories are never touched
2. **Age-Based Cleaning**: Only removes files older than 7 days from most caches
3. **Dry Run Mode**: Preview all operations before execution
4. **Permission Handling**: Gracefully handles files it cannot access
5. **Intelligent Exclusions**: Skips essential system caches automatically

### Safety Features by Design

```python
# Core safety checks in the code
def is_safe_to_delete(self, path: Path) -> bool:
    """Never deletes these critical paths"""
    critical_paths = [
        '/System',      # macOS system files
        '/usr',         # Unix system resources
        '/bin',         # Essential binaries
        '/sbin',        # System binaries
        '/etc',         # System configuration
        '/Applications', # Installed applications
        '/Library/Frameworks',  # System frameworks
        '/Library/Extensions',  # Kernel extensions
    ]
```

## Protected Directories

### Never Touched (Critical System)

| Directory | Purpose | Why Protected |
|-----------|---------|---------------|
| `/System` | Core macOS files | System will not boot without these |
| `/usr` | Unix utilities | Required for basic operations |
| `/bin`, `/sbin` | System binaries | Essential commands |
| `/etc` | System configuration | Contains critical settings |
| `/Library/Frameworks` | System frameworks | Apps depend on these |
| `/Library/Extensions` | Kernel extensions | Hardware drivers |

### Partially Protected (Selective Cleaning)

| Directory | What's Cleaned | What's Protected |
|-----------|---------------|------------------|
| `~/Library/Caches` | Old cache files | Active app caches |
| `/Library/Caches` | Shared caches | System-critical caches |
| `/var/folders` | Temp files >7 days | Recent temp files |

### User-Controlled (Optional Cleaning)

| Directory | Default Action | User Control |
|-----------|---------------|--------------|
| `~/.Trash` | Not cleaned | `--skip-trash` flag |
| Development caches | Cleaned if found | Can be excluded |
| Browser data | Cleaned | Per-browser control |

## Cache Types Explained

### 1. System Caches

**Location**: `~/Library/Caches/*`

**What they contain**:
- Application temporary data
- Downloaded updates
- Thumbnail previews
- Quick access data

**Safe to delete?**: ✅ Yes (with age check)

**Impact of deletion**:
- Apps may launch slower initially
- Thumbnails regenerate on demand
- No data loss

**Rebuild time**: Automatic, varies by app

### 2. Browser Caches

#### Safari
**Location**: `~/Library/Caches/com.apple.Safari`

**Contains**:
- Cached websites
- Favicons
- Preview images

**Safe to delete?**: ✅ Yes

**Impact**:
- Websites load slower initially
- Need to re-download resources
- Does NOT affect bookmarks or passwords

#### Chrome
**Location**: `~/Library/Caches/com.google.Chrome`

**Contains**:
- Web content cache
- Service worker data
- GPU shader cache

**Safe to delete?**: ✅ Yes

**Impact**:
- Initial page loads slower
- May need to re-login to some sites
- Extensions remain intact

### 3. Development Caches

#### npm
**Location**: `~/.npm/_cacache`

**Contains**:
- Downloaded packages
- Package metadata
- Tarball cache

**Safe to delete?**: ✅ Yes

**Impact**:
- Next `npm install` re-downloads packages
- No project impact

#### Xcode DerivedData
**Location**: `~/Library/Developer/Xcode/DerivedData`

**Contains**:
- Build artifacts
- Intermediate files
- Module caches

**Safe to delete?**: ✅ Yes

**Impact**:
- Next build takes longer
- No source code affected

#### Docker
**Location**: `~/Library/Containers/com.docker.docker/Data`

**Contains**:
- Image layers
- Build cache
- Volumes (if unused)

**Safe to delete?**: ⚠️ Caution

**Impact**:
- Need to re-pull images
- Lose build cache efficiency
- Check running containers first

### 4. Application Support Files

**Location**: `~/Library/Application Support/*`

**Contains**:
- App preferences
- User data
- Plugins
- Databases

**Safe to delete?**: ❌ No (by default)

**Why protected**:
- Contains user data
- App settings and preferences
- Would require app reconfiguration

### 5. Log Files

**Location**: `~/Library/Logs/*`

**Contains**:
- Application logs
- Crash reports
- System diagnostics

**Safe to delete?**: ✅ Yes (old files)

**Age threshold**: 7 days

**Impact**:
- Lose troubleshooting history
- No functionality impact

## Risk Levels

### 🟢 Low Risk (Safe to Clean)

Always safe to clean:
- Browser caches
- npm/yarn caches
- Old log files (>7 days)
- Trash (with user consent)
- `/tmp` files
- Thumbnail caches

### 🟡 Medium Risk (Clean with Caution)

Review before cleaning:
- Docker caches
- Virtual machine files
- Development build caches
- Application caches <7 days old
- Download histories

### 🔴 High Risk (Do Not Clean)

Never automatically cleaned:
- Application Support data
- Preferences
- Keychains
- Mail downloads
- Photo library caches
- Time Machine local snapshots

## Recovery Procedures

### If Something Goes Wrong

#### 1. Application Won't Launch
```bash
# Reset app preferences (example for Safari)
defaults delete com.apple.Safari

# Or restore from backup
cp ~/Library/Preferences/com.apple.Safari.plist.backup \
   ~/Library/Preferences/com.apple.Safari.plist
```

#### 2. Lost Browser Session
- Most browsers auto-save sessions
- Check History → Recently Closed
- Use Time Machine if critical

#### 3. Development Tools Issues

**npm problems**:
```bash
# Clear npm cache properly
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules
npm install
```

**Xcode issues**:
```bash
# Reset Xcode
rm -rf ~/Library/Developer/Xcode/DerivedData
# Xcode will rebuild on next launch
```

#### 4. System Feels Slow
- Normal after cache cleaning
- System rebuilds caches automatically
- Give it 10-15 minutes
- Restart if needed

### Using Time Machine

Before major cleaning:
```bash
# Create local snapshot
tmutil localsnapshot

# List snapshots
tmutil listlocalsnapshots /

# Restore specific file
tmutil restore /path/to/file
```

## Best Practices

### Before Cleaning

1. **Always run dry-run first**
   ```bash
   ./cache_cleaner.py --dry-run --verbose
   ```

2. **Check disk space**
   ```bash
   df -h /
   ```

3. **Close active applications**
   - Prevents file lock issues
   - Ensures clean cache state

4. **Note current disk usage**
   - Compare before/after
   - Track cleaning effectiveness

### During Cleaning

1. **Start conservative**
   - Use safe mode first
   - Increase aggressiveness gradually

2. **Monitor output**
   - Watch for errors
   - Note unusual warnings

3. **Don't interrupt**
   - Let operations complete
   - Interruption may leave partial state

### After Cleaning

1. **Verify system stability**
   - Launch key applications
   - Check system responsiveness

2. **Document results**
   - Note space freed
   - Record any issues

3. **Wait before re-cleaning**
   - Give caches time to stabilize
   - Weekly/monthly is sufficient

## What NOT to Clean

### Never Manually Delete

❌ **System Files**
- `/System/*` - Core OS
- `/private/var/db` - System databases
- `/Library/LaunchDaemons` - System services

❌ **User Data**
- `~/Documents` - Your files
- `~/Library/Mail` - Email
- `~/Library/Messages` - iMessage history
- `~/Photos Library` - Photos

❌ **Security Files**
- `~/Library/Keychains` - Passwords
- `/Library/Security` - Certificates
- `~/.ssh` - SSH keys

❌ **Application Data**
- `~/Library/Application Support/[App]/data`
- Database files (`.db`, `.sqlite`)
- Preference files (`.plist`)

### Special Considerations

#### iCloud Drive
- Don't clean `~/Library/Mobile Documents`
- Contains iCloud synced data
- Would trigger full re-sync

#### Creative Apps
- Adobe cache can be huge but active
- Final Cut Pro render files
- Logic Pro audio files
- Check if projects are active

#### Virtual Machines
- VM disk images look like cache
- Actually contain entire OS
- Can be 50GB+ each

## Emergency Procedures

### If System Won't Boot

1. **Safe Mode**
   - Hold Shift during startup
   - Cleans some caches automatically
   - Bypasses login items

2. **Recovery Mode**
   - Command-R at startup
   - Use Disk Utility
   - Restore from Time Machine

3. **Terminal Recovery**
   ```bash
   # From Recovery Terminal
   cd /Volumes/Macintosh\ HD
   rm -rf Users/[username]/Library/Caches/*
   ```

### Reporting Issues

If you experience problems:

1. **Document the issue**
   - What was cleaned
   - What stopped working
   - Error messages

2. **Check logs**
   ```bash
   # System logs
   log show --last 1h | grep -i error
   
   # Application crash logs
   ls ~/Library/Logs/DiagnosticReports/
   ```

3. **Create GitHub issue**
   - Include cache_cleaner.log
   - System information
   - Steps to reproduce

## FAQ

### Q: Can cleaning caches cause data loss?
**A**: No. Caches only contain temporary data that can be regenerated.

### Q: Will I need to reconfigure apps?
**A**: No. Settings are stored in preferences, not caches.

### Q: Can this brick my Mac?
**A**: No. Critical system files are protected and never touched.

### Q: Is it safe to run with sudo?
**A**: Yes, but only needed for system maintenance tasks. The tool has built-in protections.

### Q: How is this different from CleanMyMac?
**A**: 
- Open source and transparent
- No telemetry or data collection
- More conservative by default
- Free and customizable

### Q: Should I clean before macOS updates?
**A**: Yes, it can help ensure enough space for the update.

## Conclusion

The macOS Cache Cleaner is designed to be safe by default. By understanding what each cache type does and following the best practices in this guide, you can confidently maintain your Mac's storage without risk of data loss or system instability.

Remember: **When in doubt, use dry-run mode first!**

---

For additional safety questions or concerns, please contact: mail@tommytracx.com