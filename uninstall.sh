#!/bin/bash

# macOS Silicon Cache Cleaner - Uninstall Script
#
# Created by: Tommy Xaypanya
# GitHub: https://github.com/ttracx
# Email: mail@tommytracx.com
# Version: 1.0.0

set -e

INSTALL_DIR="/usr/local/bin"
INSTALL_NAME="macos-cleaner"
INSTALL_PATH="$INSTALL_DIR/$INSTALL_NAME"
DESKTOP_SHORTCUT="$HOME/Desktop/Cache Cleaner.command"

echo "🗑️  macOS Silicon Cache Cleaner - Uninstaller"
echo "=============================================="

# Check if installed
if [[ ! -f "$INSTALL_PATH" ]]; then
    echo "ℹ️  Cache cleaner is not installed at $INSTALL_PATH"
else
    echo "🔍 Found installation at $INSTALL_PATH"
    
    # Confirm uninstallation
    read -p "Are you sure you want to uninstall the cache cleaner? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Uninstallation cancelled"
        exit 0
    fi
    
    # Remove the main script
    echo "🗑️  Removing $INSTALL_PATH..."
    sudo rm -f "$INSTALL_PATH"
    
    if [[ ! -f "$INSTALL_PATH" ]]; then
        echo "✅ Main script removed successfully"
    else
        echo "❌ Failed to remove main script"
    fi
fi

# Remove desktop shortcut
if [[ -f "$DESKTOP_SHORTCUT" ]]; then
    echo "🗑️  Removing desktop shortcut..."
    rm -f "$DESKTOP_SHORTCUT"
    echo "✅ Desktop shortcut removed"
fi

# Remove cron job
if crontab -l 2>/dev/null | grep -q "$INSTALL_NAME"; then
    echo "🗑️  Removing scheduled weekly cleanup..."
    crontab -l 2>/dev/null | grep -v "$INSTALL_NAME" | crontab -
    echo "✅ Scheduled cleanup removed"
fi

# Check for any remaining files
echo ""
echo "🔍 Checking for remaining files..."

remaining_files=()

# Check common locations
if [[ -f "$HOME/.local/bin/$INSTALL_NAME" ]]; then
    remaining_files+=("$HOME/.local/bin/$INSTALL_NAME")
fi

if [[ -f "/opt/homebrew/bin/$INSTALL_NAME" ]]; then
    remaining_files+=("/opt/homebrew/bin/$INSTALL_NAME")
fi

# Check for aliases in shell profiles
shell_profiles=("$HOME/.zshrc" "$HOME/.bash_profile" "$HOME/.bashrc" "$HOME/.profile")
for profile in "${shell_profiles[@]}"; do
    if [[ -f "$profile" ]] && grep -q "$INSTALL_NAME\|cache_cleaner\|macos.*clean" "$profile"; then
        echo "⚠️  Found references in $profile"
        echo "   You may want to manually remove any aliases or functions related to the cache cleaner"
    fi
done

if [[ ${#remaining_files[@]} -gt 0 ]]; then
    echo "⚠️  Found additional files:"
    for file in "${remaining_files[@]}"; do
        echo "   $file"
    done
    echo ""
    read -p "Remove these files too? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for file in "${remaining_files[@]}"; do
            rm -f "$file"
            echo "✅ Removed $file"
        done
    fi
fi

echo ""
echo "🎉 Uninstallation complete!"
echo ""
echo "The cache cleaner has been removed from your system."
echo "Any caches that were cleaned are permanently deleted."
echo ""
echo "Thank you for using macOS Silicon Cache Cleaner!"