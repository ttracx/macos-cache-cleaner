#!/bin/bash

# macOS Silicon Cache Cleaner - Installation Script
# This script installs the cache cleaner as a system utility
#
# Created by: Tommy Xaypanya
# GitHub: https://github.com/ttracx
# Email: mail@tommytracx.com
# Version: 1.0.0

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLEANER_SCRIPT="$SCRIPT_DIR/cache_cleaner.py"
INSTALL_DIR="/usr/local/bin"
INSTALL_NAME="macos-cleaner"
INSTALL_PATH="$INSTALL_DIR/$INSTALL_NAME"

echo "🧹 macOS Silicon Cache Cleaner - Installer"
echo "=========================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This installer is designed for macOS only"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    echo "Please install Python 3 and try again"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if the cleaner script exists
if [[ ! -f "$CLEANER_SCRIPT" ]]; then
    echo "❌ Error: cache_cleaner.py not found in $SCRIPT_DIR"
    exit 1
fi

echo "✅ Cache cleaner script found"

# Check if install directory exists
if [[ ! -d "$INSTALL_DIR" ]]; then
    echo "📁 Creating $INSTALL_DIR directory..."
    sudo mkdir -p "$INSTALL_DIR"
fi

# Check if already installed
if [[ -f "$INSTALL_PATH" ]]; then
    echo "⚠️  Cache cleaner is already installed at $INSTALL_PATH"
    read -p "Do you want to update it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled"
        exit 0
    fi
fi

# Copy the script
echo "📦 Installing cache cleaner to $INSTALL_PATH..."
sudo cp "$CLEANER_SCRIPT" "$INSTALL_PATH"
sudo chmod +x "$INSTALL_PATH"

# Verify installation
if [[ -x "$INSTALL_PATH" ]]; then
    echo "✅ Installation successful!"
    echo ""
    echo "Usage:"
    echo "  $INSTALL_NAME --dry-run          # Test run (recommended first)"
    echo "  $INSTALL_NAME --verbose          # Run with detailed output"
    echo "  $INSTALL_NAME --find-large-files # Find large files to review"
    echo "  $INSTALL_NAME --help             # Show all options"
    echo ""
    echo "Examples:"
    echo "  $INSTALL_NAME --dry-run --verbose"
    echo "  $INSTALL_NAME --skip-trash"
    echo ""
    
    # Test the installation
    echo "🧪 Testing installation..."
    if "$INSTALL_PATH" --help > /dev/null 2>&1; then
        echo "✅ Installation test passed"
    else
        echo "❌ Installation test failed"
        exit 1
    fi
    
    # Offer to create a desktop shortcut
    read -p "Create a desktop shortcut? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        DESKTOP="$HOME/Desktop"
        SHORTCUT="$DESKTOP/Cache Cleaner.command"
        
        cat > "$SHORTCUT" << EOF
#!/bin/bash
echo "🧹 macOS Cache Cleaner"
echo "====================="
echo ""
echo "This will clean cache and temporary files from your Mac."
echo "A dry-run will be performed first to show what would be cleaned."
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo ""
if [[ \$REPLY =~ ^[Yy]\$ ]]; then
    echo ""
    echo "📋 Dry Run (showing what would be cleaned):"
    echo "============================================"
    $INSTALL_PATH --dry-run --verbose
    echo ""
    read -p "Proceed with actual cleanup? (y/N): " -n 1 -r
    echo ""
    if [[ \$REPLY =~ ^[Yy]\$ ]]; then
        echo ""
        echo "🧹 Running cleanup..."
        echo "===================="
        $INSTALL_PATH --verbose
    else
        echo "Cleanup cancelled"
    fi
else
    echo "Cancelled"
fi
echo ""
read -p "Press Enter to close..." 
EOF
        
        chmod +x "$SHORTCUT"
        echo "✅ Desktop shortcut created: $SHORTCUT"
    fi
    
    # Offer to set up weekly cleaning
    read -p "Set up weekly automatic cleaning? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        CRON_JOB="0 2 * * 0 $INSTALL_PATH --skip-maintenance > /dev/null 2>&1"
        
        # Check if cron job already exists
        if crontab -l 2>/dev/null | grep -q "$INSTALL_NAME"; then
            echo "⚠️  Weekly cleanup is already configured"
        else
            # Add to crontab
            (crontab -l 2>/dev/null || true; echo "$CRON_JOB") | crontab -
            echo "✅ Weekly cleanup scheduled for Sundays at 2 AM"
            echo "   To remove: crontab -e and delete the $INSTALL_NAME line"
        fi
    fi
    
    echo ""
    echo "🎉 Installation complete!"
    echo ""
    echo "Quick start:"
    echo "  $INSTALL_NAME --dry-run"
    
else
    echo "❌ Installation failed"
    exit 1
fi