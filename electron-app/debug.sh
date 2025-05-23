#!/bin/bash

echo "🚀 Starting Cache Cleaner in Debug Mode"
echo "======================================"

cd "$(dirname "$0")"

# Check Node.js
echo "Checking Node.js..."
node --version || { echo "❌ Node.js not found"; exit 1; }

# Check npm dependencies
echo "Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Check if preload and main files exist
echo "Checking app files..."
[ -f "main.js" ] && echo "✅ main.js found" || echo "❌ main.js missing"
[ -f "preload.js" ] && echo "✅ preload.js found" || echo "❌ preload.js missing"
[ -f "index.html" ] && echo "✅ index.html found" || echo "❌ index.html missing"
[ -f "styles.css" ] && echo "✅ styles.css found" || echo "❌ styles.css missing"
[ -f "renderer.js" ] && echo "✅ renderer.js found" || echo "❌ renderer.js missing"

echo ""
echo "🎯 Starting app with debug output..."
echo "Press Ctrl+C to exit"
echo ""

NODE_ENV=development npm start