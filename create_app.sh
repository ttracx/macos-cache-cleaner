#!/bin/bash

# Create macOS App Bundle for Cache Cleaner
# This script creates a proper .app bundle for distribution
# 
# Created by: Tommy Xaypanya
# GitHub: https://github.com/ttracx
# Email: mail@tommytracx.com
# Version: 1.0.0

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="Cache Cleaner"
APP_DIR="$SCRIPT_DIR/$APP_NAME.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

echo "🚀 Creating macOS App Bundle for Cache Cleaner"
echo "=============================================="

# Clean up any existing app
if [[ -d "$APP_DIR" ]]; then
    echo "🗑️  Removing existing app bundle..."
    rm -rf "$APP_DIR"
fi

# Create app directory structure
echo "📁 Creating app directory structure..."
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

# Create Info.plist
echo "📝 Creating Info.plist..."
cat > "$CONTENTS_DIR/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Cache Cleaner</string>
    <key>CFBundleDisplayName</key>
    <string>Cache Cleaner</string>
    <key>CFBundleIdentifier</key>
    <string>com.tommytracx.cache-cleaner</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleExecutable</key>
    <string>cache_cleaner_gui</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.utilities</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSSupportsAutomaticGraphicsSwitching</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
    <key>NSHumanReadableCopyright</key>
    <string>© 2025 Tommy Xaypanya. All rights reserved.</string>
    <key>CFBundleDocumentTypes</key>
    <array/>
</dict>
</plist>
EOF

# Create launcher script
echo "🎯 Creating launcher script..."
cat > "$MACOS_DIR/cache_cleaner_gui" << 'EOF'
#!/bin/bash

# Get the directory containing this script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOURCES_DIR="$DIR/../Resources"

# Set PYTHONPATH to include our resources
export PYTHONPATH="$RESOURCES_DIR:$PYTHONPATH"

# Change to resources directory
cd "$RESOURCES_DIR"

# Launch the GUI with Python
if command -v python3 &> /dev/null; then
    python3 cache_cleaner_gui.py "$@"
else
    echo "Error: Python 3 is required but not found"
    exit 1
fi
EOF

chmod +x "$MACOS_DIR/cache_cleaner_gui"

# Copy Python files to Resources
echo "📦 Copying Python files..."
cp "$SCRIPT_DIR/cache_cleaner.py" "$RESOURCES_DIR/"
cp "$SCRIPT_DIR/cache_cleaner_gui.py" "$RESOURCES_DIR/"

# Create a simple icon (using emoji-style)
echo "🎨 Creating app icon..."
cat > "$RESOURCES_DIR/create_icon.py" << 'EOF'
#!/usr/bin/env python3
import tkinter as tk
from tkinter import Canvas
import os

def create_icon():
    # Create a simple icon using tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Create canvas for icon
    canvas = Canvas(root, width=512, height=512, bg='#f8f9fa')
    
    # Draw a cleaning brush icon
    # Handle (brown)
    canvas.create_rectangle(200, 350, 240, 480, fill='#8B4513', outline='')
    
    # Brush bristles (gray)
    for i in range(15):
        x = 160 + i * 12
        canvas.create_rectangle(x, 200, x+8, 360, fill='#696969', outline='')
    
    # Brush ferrule (silver)
    canvas.create_rectangle(160, 340, 340, 370, fill='#C0C0C0', outline='')
    
    # Sparkles (cleaning effect)
    sparkle_coords = [(100, 100), (400, 120), (150, 180), (380, 200), (120, 250)]
    for x, y in sparkle_coords:
        # Create sparkle shape
        points = [x, y-10, x+5, y-3, x+12, y, x+5, y+3, x, y+10, x-5, y+3, x-12, y, x-5, y-3]
        canvas.create_polygon(points, fill='#FFD700', outline='')
    
    # Try to save as PostScript (will need conversion)
    try:
        canvas.postscript(file=f"{os.path.dirname(__file__)}/icon.ps")
        print("Icon template created (requires manual conversion to .icns)")
    except:
        print("Could not create icon file")
    
    root.destroy()

if __name__ == "__main__":
    create_icon()
EOF

python3 "$RESOURCES_DIR/create_icon.py"
rm "$RESOURCES_DIR/create_icon.py"

# Copy the app icon if it exists
echo "🖼️  Adding app icon..."
if [[ -f "$SCRIPT_DIR/AppIcon.icns" ]]; then
    cp "$SCRIPT_DIR/AppIcon.icns" "$RESOURCES_DIR/"
    echo "  ✅ Using existing AppIcon.icns"
elif [[ -f "$SCRIPT_DIR/icon_1024.png" ]]; then
    # Try to create .icns from PNG
    if command -v iconutil &> /dev/null && [[ -d "$SCRIPT_DIR/AppIcon.iconset" ]]; then
        iconutil -c icns "$SCRIPT_DIR/AppIcon.iconset" -o "$RESOURCES_DIR/AppIcon.icns"
        echo "  ✅ Created AppIcon.icns from iconset"
    else
        echo "  ⚠️  PNG icon found but cannot create .icns (run create_icon.py first)"
    fi
else
    echo "  ℹ️  No icon found - run create_icon.py to generate one"
    # Create placeholder
    cat > "$RESOURCES_DIR/AppIcon.txt" << 'EOF'
🧹 Cache Cleaner Icon Placeholder

Run create_icon.py to generate a proper app icon.
EOF
fi

# Create README for the app
echo "📚 Creating app documentation..."
cat > "$RESOURCES_DIR/README.txt" << 'EOF'
Cache Cleaner for macOS
======================

This is a GUI application for cleaning cache and temporary files on macOS.

Features:
- Safe cache cleaning with dry-run mode
- Browser cache cleanup
- Development cache cleanup (npm, yarn, pip, Docker, Xcode)
- System maintenance
- Large file detection

The app requires Python 3 to be installed on the system.

For support, visit: https://github.com/knightdev/macos-cache-cleaner
EOF

# Set proper permissions
echo "🔒 Setting permissions..."
chmod -R 755 "$APP_DIR"
chmod +x "$MACOS_DIR/cache_cleaner_gui"

# Attempt to code sign (will fail without developer certificate, but that's ok)
echo "✍️  Attempting to sign app (may fail without certificate)..."
if command -v codesign &> /dev/null; then
    codesign --force --deep --sign - "$APP_DIR" 2>/dev/null || echo "   Code signing failed (certificate not found - this is normal)"
fi

echo ""
echo "✅ App bundle created successfully!"
echo "📍 Location: $APP_DIR"
echo ""
echo "To use the app:"
echo "1. Double-click '$APP_NAME.app' to launch"
echo "2. Or drag it to /Applications folder for system-wide access"
echo ""
echo "Note: macOS may show a security warning for unsigned apps."
echo "To bypass: Right-click → Open → Open anyway"
echo ""

# Offer to open the app
read -p "Open the app now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open "$APP_DIR"
fi