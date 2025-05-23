#!/bin/bash

# Setup script for Ollama AI integration
echo "🤖 Setting up AI Assistant for Cache Cleaner"
echo "=========================================="

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed."
    echo ""
    echo "To install Ollama, visit: https://ollama.ai"
    echo "Or run: curl -fsSL https://ollama.ai/install.sh | sh"
    echo ""
    echo "After installing Ollama, run this script again."
    exit 1
fi

echo "✅ Ollama is installed"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/version &> /dev/null; then
    echo "🚀 Starting Ollama service..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

echo "✅ Ollama service is running"

# Pull the Mistral model (using mistral as devstral might not be available)
echo "📦 Downloading AI model (this may take a few minutes)..."
ollama pull mistral:latest

if [ $? -eq 0 ]; then
    echo "✅ AI model installed successfully!"
    echo ""
    echo "🎉 AI Assistant is ready to use!"
    echo ""
    echo "Features available:"
    echo "- Intelligent cleaning recommendations based on your disk usage"
    echo "- Analysis of cleaning results"
    echo "- Explanations of different cache types"
    echo "- Tips for maintaining optimal disk space"
    echo ""
    echo "To use: Click the 🤖 button in the Cache Cleaner app"
else
    echo "❌ Failed to download AI model"
    echo "Please check your internet connection and try again"
    exit 1
fi