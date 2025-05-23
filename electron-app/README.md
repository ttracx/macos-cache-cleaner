# Cache Cleaner Desktop App

A beautiful, modern desktop application for macOS cache cleaning built with Electron.

## Features

- 🎨 **Modern macOS Design**: Native-looking interface that follows Apple's design guidelines
- 📊 **Real-time Disk Usage**: Visual disk usage display with animated charts
- ⚡ **Quick Actions**: One-click presets for scan, safe clean, and deep clean
- 🎯 **Customizable Options**: Fine-tune cleaning settings to your needs
- 📋 **Live Output Console**: Real-time feedback during cleaning operations
- 💾 **Export Reports**: Save cleaning reports for your records
- 🌓 **Beautiful UI**: Smooth animations and thoughtful interactions

## Development

### Prerequisites

- Node.js 16 or later
- npm or yarn
- Python 3 (for the cache cleaning backend)

### Quick Start

```bash
# Install dependencies
npm install

# Run in development mode
npm start

# Or use the convenience script
./run.sh
```

### Building for Distribution

```bash
# Build distributable app
npm run dist

# Or use the build script
./build.sh
```

This will create a `.dmg` file in the `dist/` directory that can be distributed to users.

## Architecture

The app consists of:

- **Main Process** (`main.js`): Handles system interactions and Python script execution
- **Renderer Process** (`renderer.js`): Manages the UI and user interactions
- **Preload Script** (`preload.js`): Provides secure communication between processes
- **Python Backend**: Uses the existing `cache_cleaner.py` for actual cleaning operations

## Technologies Used

- **Electron**: Cross-platform desktop app framework
- **HTML/CSS/JavaScript**: Modern web technologies for the UI
- **Chart.js**: For the disk usage visualization
- **Python**: Backend cleaning operations

## UI Components

### Quick Actions
- **Scan Only**: Preview mode with verbose output
- **Safe Clean**: Conservative cleaning without system maintenance
- **Deep Clean**: Maximum space recovery with all features enabled

### Cleaning Options
- Dry Run mode for previewing changes
- Verbose output for detailed information
- Skip trash emptying
- Skip system maintenance
- Find large files

### Visual Features
- Animated disk usage chart
- Progress indicators
- Color-coded console output
- Smooth transitions and animations

## Security

The app uses Electron's context isolation and secure IPC communication to ensure safe execution of system commands.

## Author

Created by Tommy Xaypanya ([@ttracx](https://github.com/ttracx))