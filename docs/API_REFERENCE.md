# API Reference

Complete API documentation for the macOS Cache Cleaner, covering command-line usage, Python API, and JavaScript/Electron APIs.

## Table of Contents

1. [Command Line Interface](#command-line-interface)
2. [Python API](#python-api)
3. [Electron/JavaScript API](#electronjavascript-api)
4. [IPC Communication](#ipc-communication)
5. [AI Service API](#ai-service-api)
6. [Plugin API](#plugin-api)

## Command Line Interface

### Basic Usage

```bash
./cache_cleaner.py [OPTIONS]
```

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--help` | `-h` | Show help message and exit | - |
| `--verbose` | `-v` | Show detailed output during cleaning | False |
| `--dry-run` | - | Preview what would be deleted without actually deleting | False |
| `--skip-trash` | - | Skip emptying the trash | False |
| `--skip-maintenance` | - | Skip running macOS maintenance scripts | False |
| `--find-large-files` | - | Scan for files larger than 100MB | False |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Permission denied |
| 3 | Invalid arguments |

### Examples

```bash
# Basic cleanup
./cache_cleaner.py

# Preview with details
./cache_cleaner.py --dry-run --verbose

# Safe cleanup (skip system tasks)
./cache_cleaner.py --skip-trash --skip-maintenance

# Full analysis
./cache_cleaner.py --dry-run --verbose --find-large-files

# Quiet mode (no verbose)
./cache_cleaner.py 2>/dev/null
```

## Python API

### Core Class: MacOSCacheCleaner

```python
from cache_cleaner import MacOSCacheCleaner

# Initialize cleaner
cleaner = MacOSCacheCleaner(dry_run=False, verbose=True)
```

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dry_run` | bool | False | Preview mode without deleting |
| `verbose` | bool | False | Enable detailed output |

#### Properties

```python
cleaner.total_freed      # int: Total bytes freed
cleaner.home_dir        # Path: User's home directory
cleaner.cache_dirs      # list[Path]: Cache directories to clean
cleaner.exclude_dirs    # set: Protected directory names
```

#### Methods

##### run()
```python
def run(self, skip_trash=False, skip_maintenance=False, find_large_files=False):
    """
    Execute the complete cleaning process.
    
    Args:
        skip_trash (bool): Skip emptying trash
        skip_maintenance (bool): Skip system maintenance
        find_large_files (bool): Scan for large files
    
    Returns:
        None (prints results to stdout)
    """
```

##### clean_directory()
```python
def clean_directory(self, cache_dir: Path) -> int:
    """
    Clean a specific cache directory.
    
    Args:
        cache_dir: Path to directory to clean
        
    Returns:
        int: Bytes freed
    """
```

##### get_dir_size()
```python
def get_dir_size(self, path: Path) -> int:
    """
    Calculate total size of directory.
    
    Args:
        path: Directory path
        
    Returns:
        int: Total size in bytes
    """
```

##### is_safe_to_delete()
```python
def is_safe_to_delete(self, path: Path) -> bool:
    """
    Check if path is safe to delete.
    
    Args:
        path: Path to check
        
    Returns:
        bool: True if safe to delete
    """
```

##### format_size()
```python
def format_size(self, size_bytes: int) -> str:
    """
    Format bytes to human readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        str: Formatted string (e.g., "1.5 GB")
    """
```

### Usage Examples

#### As a Library

```python
from cache_cleaner import MacOSCacheCleaner

# Create cleaner instance
cleaner = MacOSCacheCleaner(dry_run=True, verbose=True)

# Get directory sizes before cleaning
cache_sizes = {}
for cache_dir in cleaner.cache_dirs:
    if cache_dir.exists():
        cache_sizes[str(cache_dir)] = cleaner.get_dir_size(cache_dir)

# Run cleaning
cleaner.run(skip_trash=True, skip_maintenance=True)

# Get total freed space
print(f"Total space freed: {cleaner.format_size(cleaner.total_freed)}")
```

#### Custom Integration

```python
import json
from cache_cleaner import MacOSCacheCleaner

def analyze_system():
    """Analyze system without cleaning"""
    cleaner = MacOSCacheCleaner(dry_run=True, verbose=False)
    
    analysis = {
        "cache_locations": [],
        "total_size": 0,
        "safe_to_clean": 0
    }
    
    for cache_dir in cleaner.cache_dirs:
        if cache_dir.exists():
            size = cleaner.get_dir_size(cache_dir)
            is_safe = cleaner.is_safe_to_delete(cache_dir)
            
            analysis["cache_locations"].append({
                "path": str(cache_dir),
                "size": size,
                "size_human": cleaner.format_size(size),
                "safe": is_safe
            })
            
            analysis["total_size"] += size
            if is_safe:
                analysis["safe_to_clean"] += size
    
    return json.dumps(analysis, indent=2)
```

#### Extending the Cleaner

```python
from cache_cleaner import MacOSCacheCleaner
from pathlib import Path

class ExtendedCacheCleaner(MacOSCacheCleaner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom cache directories
        self.cache_dirs.extend([
            Path.home() / "CustomApp/Cache",
            Path("/usr/local/var/cache")
        ])
    
    def clean_custom_cache(self):
        """Clean custom application cache"""
        custom_cache = Path.home() / "CustomApp/Cache"
        if custom_cache.exists():
            freed = self.clean_directory(custom_cache)
            self.total_freed += freed
            return freed
        return 0
```

## Electron/JavaScript API

### Window API (Renderer Process)

All APIs are accessed through `window.electronAPI`:

#### Disk Operations

```javascript
// Get current disk usage
const usage = await window.electronAPI.getDiskUsage();
// Returns: { total: string, used: string, available: string, percentage: number }

// Start cleaning process
const result = await window.electronAPI.startCleaning({
    dryRun: boolean,
    verbose: boolean,
    skipTrash: boolean,
    skipMaintenance: boolean,
    findLargeFiles: boolean
});
// Returns: { success: boolean, output?: string, error?: string }

// Stop cleaning process
const stopped = await window.electronAPI.stopCleaning();
// Returns: boolean
```

#### File Operations

```javascript
// Export cleaning report
const result = await window.electronAPI.exportReport(content);
// Returns: { success: boolean, path?: string, error?: string }

// Open logs directory
await window.electronAPI.openLogs();
// Returns: void
```

#### App Information

```javascript
// Get app information
const info = await window.electronAPI.getAppInfo();
// Returns: {
//   version: string,
//   name: string,
//   electron: string,
//   node: string,
//   platform: string,
//   arch: string
// }
```

#### Event Listeners

```javascript
// Listen for cleaning output
window.electronAPI.onCleaningOutput((data) => {
    console.log('Output:', data);
});

// Listen for cleaning errors
window.electronAPI.onCleaningError((data) => {
    console.error('Error:', data);
});
```

### Main Process API

#### IPC Handlers

```javascript
const { ipcMain } = require('electron');

// Register new handler
ipcMain.handle('custom-operation', async (event, args) => {
    try {
        // Perform operation
        const result = await performOperation(args);
        return { success: true, data: result };
    } catch (error) {
        return { success: false, error: error.message };
    }
});
```

#### Python Script Execution

```javascript
const { spawn } = require('child_process');

function executePythonScript(scriptPath, args = []) {
    return new Promise((resolve, reject) => {
        const python = spawn('python3', [scriptPath, ...args]);
        let output = '';
        let error = '';
        
        python.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        python.stderr.on('data', (data) => {
            error += data.toString();
        });
        
        python.on('close', (code) => {
            if (code === 0) {
                resolve({ success: true, output });
            } else {
                reject({ success: false, error, code });
            }
        });
    });
}
```

## IPC Communication

### Message Format

All IPC messages follow this structure:

```typescript
interface IPCMessage {
    channel: string;
    args: any[];
}

interface IPCResponse {
    success: boolean;
    data?: any;
    error?: string;
}
```

### Available Channels

| Channel | Direction | Description |
|---------|-----------|-------------|
| `get-disk-usage` | Renderer → Main | Request disk usage info |
| `start-cleaning` | Renderer → Main | Start cleaning process |
| `stop-cleaning` | Renderer → Main | Stop cleaning process |
| `cleaning-output` | Main → Renderer | Cleaning process output |
| `cleaning-error` | Main → Renderer | Cleaning process errors |
| `export-report` | Renderer → Main | Export cleaning report |
| `open-logs` | Renderer → Main | Open logs directory |
| `get-app-info` | Renderer → Main | Get app information |

### Custom IPC Implementation

```javascript
// In preload.js
contextBridge.exposeInMainWorld('customAPI', {
    performAction: (data) => ipcRenderer.invoke('custom-action', data),
    onUpdate: (callback) => {
        ipcRenderer.on('custom-update', (event, data) => callback(data));
    }
});

// In main.js
ipcMain.handle('custom-action', async (event, data) => {
    // Process action
    return { success: true, result: processedData };
});

// Send updates
mainWindow.webContents.send('custom-update', updateData);
```

## AI Service API

### Service Initialization

```javascript
const AIService = require('./ai-service');
const aiService = new AIService();
```

### Methods

#### checkOllamaStatus()
```javascript
await aiService.checkOllamaStatus()
// Returns: { available: boolean, version?: object, error?: string }
```

#### ensureModel()
```javascript
await aiService.ensureModel()
// Returns: boolean
```

#### generateResponse()
```javascript
await aiService.generateResponse(prompt, context)
// Parameters:
//   prompt: string - The user's question or request
//   context: object - Optional context data
// Returns: string (response text)
```

#### Specialized Methods

```javascript
// Analyze cleaning results
await aiService.analyzeCleaningResults(results)

// Get cleaning recommendations
await aiService.getCleaningRecommendations(diskUsage, preferences)

// Explain cache type
await aiService.explainCacheType(cacheType)

// Troubleshoot issue
await aiService.troubleshoot(issue)
```

### Events

The AI service extends EventEmitter and emits these events:

```javascript
aiService.on('status', (status) => {
    console.log('AI Status:', status);
});

aiService.on('chunk', (chunk) => {
    // Handle streaming response chunk
});

aiService.on('download-progress', (progress) => {
    console.log('Model download:', progress);
});
```

## Plugin API

### Plugin Structure

```javascript
class CacheCleanerPlugin {
    constructor() {
        this.name = 'Plugin Name';
        this.version = '1.0.0';
        this.description = 'Plugin description';
    }
    
    // Required methods
    async initialize() {}
    async analyze() {}
    async clean(options) {}
    async getInfo() {}
}
```

### Plugin Registration

```javascript
// In plugin manager
class PluginManager {
    constructor() {
        this.plugins = new Map();
    }
    
    register(plugin) {
        if (!plugin.name || !plugin.clean) {
            throw new Error('Invalid plugin structure');
        }
        this.plugins.set(plugin.name, plugin);
    }
    
    async runPlugin(name, options) {
        const plugin = this.plugins.get(name);
        if (!plugin) {
            throw new Error(`Plugin ${name} not found`);
        }
        return await plugin.clean(options);
    }
}
```

### Creating a Plugin

```javascript
const { CacheCleanerPlugin } = require('./plugin-base');

class CustomCachePlugin extends CacheCleanerPlugin {
    constructor() {
        super();
        this.name = 'Custom Cache Cleaner';
        this.version = '1.0.0';
        this.description = 'Cleans custom application caches';
    }
    
    async analyze() {
        // Return analysis of what can be cleaned
        return {
            locations: this.getCacheLocations(),
            estimatedSize: await this.calculateSize(),
            safeToClean: true
        };
    }
    
    async clean(options = {}) {
        const { dryRun = false, verbose = false } = options;
        let totalFreed = 0;
        
        for (const location of this.getCacheLocations()) {
            if (verbose) {
                console.log(`Cleaning: ${location}`);
            }
            
            if (!dryRun) {
                const freed = await this.cleanLocation(location);
                totalFreed += freed;
            }
        }
        
        return {
            success: true,
            bytesFreed: totalFreed,
            locations: this.getCacheLocations()
        };
    }
    
    getCacheLocations() {
        return [
            '/path/to/custom/cache',
            `${process.env.HOME}/Library/CustomApp/Cache`
        ];
    }
}

module.exports = CustomCachePlugin;
```

### Plugin Configuration

```json
{
    "plugins": {
        "custom-cache": {
            "enabled": true,
            "options": {
                "maxAge": 7,
                "excludePatterns": ["*.important"]
            }
        }
    }
}
```

## Error Handling

### Error Types

```javascript
class CacheCleanerError extends Error {
    constructor(message, code) {
        super(message);
        this.name = 'CacheCleanerError';
        this.code = code;
    }
}

// Error codes
const ErrorCodes = {
    PERMISSION_DENIED: 'EPERM',
    PATH_NOT_FOUND: 'ENOENT',
    DISK_FULL: 'ENOSPC',
    INVALID_ARGUMENT: 'EINVAL',
    OPERATION_FAILED: 'EFAIL'
};
```

### Error Handling Examples

```javascript
try {
    const result = await cleaner.clean();
} catch (error) {
    if (error.code === 'EPERM') {
        console.error('Permission denied. Try running with sudo.');
    } else if (error.code === 'ENOSPC') {
        console.error('Not enough disk space to complete operation.');
    } else {
        console.error('Unexpected error:', error.message);
    }
}
```

## Best Practices

### API Usage

1. **Always handle errors gracefully**
2. **Use dry-run mode for testing**
3. **Implement proper logging**
4. **Validate inputs before operations**
5. **Use TypeScript for better type safety**

### Performance

1. **Batch operations when possible**
2. **Use async/await for better flow control**
3. **Implement caching for repeated operations**
4. **Stream large outputs instead of buffering**

### Security

1. **Validate all file paths**
2. **Use path.resolve() to prevent traversal**
3. **Check permissions before operations**
4. **Sanitize user inputs**
5. **Log security-relevant events**

## Version History

| Version | Changes |
|---------|---------|
| 2.0.0 | Added Electron app, AI integration |
| 1.0.0 | Initial Python implementation |

## Support

For API questions or issues:
- Check the examples in this document
- Review the source code
- Create an issue on GitHub
- Email: mail@tommytracx.com