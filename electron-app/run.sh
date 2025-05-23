#!/bin/bash

# Run the Electron app in development mode
echo "🚀 Starting Cache Cleaner Desktop App..."
echo "=================================="

cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "▶️  Launching app..."
npm start