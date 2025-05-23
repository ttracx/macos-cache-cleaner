#!/bin/bash

# Build the Electron app for distribution
echo "🏗️  Building Cache Cleaner Desktop App..."
echo "======================================="

cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "🔨 Building distributable..."
npm run dist

echo ""
echo "✅ Build complete!"
echo "📍 Output location: ./dist/"
echo ""
echo "The following files were created:"
ls -la dist/

echo ""
echo "To install the app:"
echo "1. Open the .dmg file in ./dist/"
echo "2. Drag Cache Cleaner to Applications"
echo "3. Launch from Applications folder"