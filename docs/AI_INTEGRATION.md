# AI Integration Documentation

This document details the AI assistant integration in the macOS Cache Cleaner, powered by Ollama and local LLMs.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Setup Guide](#setup-guide)
4. [Features](#features)
5. [API Reference](#api-reference)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)

## Overview

The AI assistant provides intelligent, context-aware recommendations for disk space management using a locally-run Large Language Model (LLM). All processing happens on your machine, ensuring privacy and offline functionality.

### Key Benefits

- **Privacy-First**: No data leaves your machine
- **Offline Capable**: Works without internet after initial setup
- **Context-Aware**: Understands your specific system state
- **macOS Optimized**: Trained specifically for Apple Silicon systems

## Architecture

### Component Diagram

```
┌─────────────────────┐     ┌─────────────────────┐
│   Electron App      │────▶│    AI Service       │
│   (Frontend)        │     │  (ai-service.js)    │
└─────────────────────┘     └──────────┬──────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │   Ollama Server     │
                            │  (localhost:11434)  │
                            └──────────┬──────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │   Local LLM Model   │
                            │    (Mistral 7B)     │
                            └─────────────────────┘
```

### Communication Flow

1. **User Input** → Electron Renderer Process
2. **IPC Message** → Main Process
3. **AI Service** → Formats request with context
4. **Ollama API** → Processes with local LLM
5. **Streaming Response** → Back to UI

## Setup Guide

### Prerequisites

- macOS 10.15 or later
- 8GB RAM minimum (16GB recommended)
- 4GB free disk space for model

### Installation Steps

#### 1. Install Ollama

```bash
# Official installer
curl -fsSL https://ollama.ai/install.sh | sh

# Or via Homebrew
brew install ollama
```

#### 2. Start Ollama Service

```bash
# Start in background
ollama serve

# Verify it's running
curl http://localhost:11434/api/version
```

#### 3. Install AI Model

```bash
# Automated setup
cd electron-app
./setup-ollama.sh

# Or manual installation
ollama pull mistral:latest
```

#### 4. Verify Installation

```bash
# List installed models
ollama list

# Test model
ollama run mistral "Hello, test message"
```

### Configuration

The AI service can be configured in `ai-service.js`:

```javascript
class AIService extends EventEmitter {
    constructor() {
        super();
        this.model = 'mistral:latest';  // Change model here
        this.baseUrl = 'http://localhost:11434';  // Change port if needed
        this.systemPrompt = `...`;  // Customize instructions
    }
}
```

## Features

### 1. Intelligent Recommendations

The AI analyzes multiple factors to provide personalized cleaning strategies:

```javascript
// Input factors
{
    diskUsage: {
        used: "234GB",
        total: "500GB",
        percentage: 47
    },
    userPreferences: {
        safetyLevel: "balanced",
        primaryUse: "development",
        lastCleanup: "2 weeks ago"
    }
}

// AI provides tailored advice based on:
// - Current disk usage percentage
// - User's safety preferences
// - Primary system usage
// - Time since last cleanup
```

### 2. Cleaning Results Analysis

Post-cleanup analysis helps users understand what happened:

```javascript
// The AI analyzes:
// - Total space freed
// - Which caches were cleaned
// - Unexpected results
// - Future recommendations
```

### 3. Cache Type Education

Interactive explanations for different cache types:

- **System Caches**: What they store, safety, rebuild time
- **Browser Caches**: Impact on browsing, login states
- **Development Caches**: Package managers, build artifacts
- **Application Caches**: App-specific temporary data

### 4. Natural Language Q&A

Users can ask questions in plain English:

```
"Why is my Xcode cache 50GB?"
"Is it safe to delete Docker volumes?"
"What's the difference between npm and yarn cache?"
"How do I free up 20GB safely?"
```

## API Reference

### JavaScript API (Frontend)

```javascript
// Check AI availability
const status = await window.electronAPI.ai.checkStatus();
// Returns: { available: boolean, version?: object, error?: string }

// Get cleaning recommendations
const result = await window.electronAPI.ai.getRecommendations(
    diskUsage,     // Current disk statistics
    preferences    // User preferences object
);
// Returns: { success: boolean, response: string, error?: string }

// Analyze cleaning results
const analysis = await window.electronAPI.ai.analyzeResults(
    cleanupOutput  // String output from cleaning operation
);
// Returns: { success: boolean, response: string, error?: string }

// Explain cache type
const explanation = await window.electronAPI.ai.explainCache(
    cacheType      // String like "Browser Caches"
);
// Returns: { success: boolean, response: string, error?: string }

// General chat
const response = await window.electronAPI.ai.chat(
    prompt,        // User's question
    context        // Optional context object
);
// Returns: { success: boolean, response: string, error?: string }
```

### Event Listeners

```javascript
// AI status updates
window.electronAPI.onAIStatus((status) => {
    console.log('AI Status:', status);
});

// Streaming response chunks
window.electronAPI.onAIResponseChunk((chunk) => {
    // Append chunk to current response
});

// Model download progress
window.electronAPI.onAIDownloadProgress((progress) => {
    console.log('Download progress:', progress);
});
```

### AI Service Methods

```javascript
// In ai-service.js
class AIService {
    // Check Ollama availability
    async checkOllamaStatus()
    
    // Ensure model is downloaded
    async ensureModel()
    
    // Generate response with streaming
    async generateResponse(prompt, context)
    
    // Specific feature methods
    async analyzeCleaningResults(results)
    async getCleaningRecommendations(diskUsage, preferences)
    async explainCacheType(cacheType)
    async troubleshoot(issue)
}
```

## Customization

### Changing the AI Model

1. **Install alternative model**:
```bash
# Larger, more capable model
ollama pull llama2:13b

# Code-specific model
ollama pull codellama:latest

# Smaller, faster model
ollama pull phi:latest
```

2. **Update configuration**:
```javascript
// In ai-service.js
this.model = 'llama2:13b';  // Change to your model
```

### Custom System Instructions

Modify the system prompt for specialized behavior:

```javascript
this.systemPrompt = `You are an AI assistant specialized in:

1. macOS system administration
2. Developer workflows
3. Storage optimization
4. Performance tuning

Additional context:
- Focus on Apple Silicon optimizations
- Prioritize safety over space savings
- Provide command-line alternatives when relevant
- Include time estimates for operations

Always structure responses with:
- Brief summary
- Detailed explanation
- Specific recommendations
- Warnings or caveats`;
```

### Adding New AI Features

1. **Create new method in ai-service.js**:
```javascript
async analyzeDiskTrends(historicalData) {
    const prompt = `Analyze these disk usage trends and provide insights:
    
    ${JSON.stringify(historicalData)}
    
    Identify patterns, predict future usage, and suggest preventive measures.`;
    
    return this.generateResponse(prompt);
}
```

2. **Add IPC handler in main.js**:
```javascript
ipcMain.handle('ai-analyze-trends', async (event, data) => {
    try {
        const response = await aiService.analyzeDiskTrends(data);
        return { success: true, response };
    } catch (error) {
        return { success: false, error: error.message };
    }
});
```

3. **Expose in preload.js**:
```javascript
ai: {
    // ... existing methods
    analyzeTrends: (data) => ipcRenderer.invoke('ai-analyze-trends', data)
}
```

4. **Use in renderer.js**:
```javascript
const trends = await window.electronAPI.ai.analyzeTrends(historicalData);
```

### Response Formatting

Control how AI responses are formatted:

```javascript
// Markdown formatting
const prompt = `Explain cache types. Format your response using:
- **Bold** for important terms
- \`code blocks\` for commands
- Bullet points for lists
- > Quotes for warnings`;

// Structured output
const prompt = `Analyze this data and respond in JSON format:
{
    "summary": "brief overview",
    "findings": ["finding1", "finding2"],
    "recommendations": ["rec1", "rec2"],
    "risk_level": "low|medium|high"
}`;
```

## Troubleshooting

### Common Issues

#### AI Shows as Offline

1. **Check Ollama is running**:
```bash
ps aux | grep ollama
# If not running:
ollama serve
```

2. **Verify port availability**:
```bash
lsof -i :11434
# Should show ollama process
```

3. **Test API directly**:
```bash
curl http://localhost:11434/api/version
```

#### Model Not Found

```bash
# List available models
ollama list

# Pull missing model
ollama pull mistral:latest

# Verify model works
ollama run mistral "test"
```

#### Slow Response Times

1. **Check system resources**:
```bash
# CPU usage
top | grep ollama

# Memory usage
ps aux | grep ollama
```

2. **Use smaller model**:
```javascript
this.model = 'phi:latest';  // 2.7B parameters vs 7B
```

3. **Adjust context window**:
```javascript
const response = await fetch(`${this.baseUrl}/api/chat`, {
    body: JSON.stringify({
        model: this.model,
        messages: messages,
        options: {
            num_ctx: 2048  // Reduce from default 4096
        }
    })
});
```

#### Memory Issues

1. **Limit model memory**:
```bash
# Set environment variable
export OLLAMA_MAX_MEMORY=4GB
ollama serve
```

2. **Unload model when not in use**:
```bash
# Unload model from memory
curl -X DELETE http://localhost:11434/api/generate
```

### Debug Mode

Enable detailed logging:

```javascript
// In ai-service.js
constructor() {
    super();
    this.debug = true;  // Enable debug mode
}

async generateResponse(prompt, context) {
    if (this.debug) {
        console.log('=== AI Debug ===');
        console.log('Prompt:', prompt);
        console.log('Context:', context);
        console.log('Model:', this.model);
    }
    // ... rest of method
}
```

### Performance Optimization

1. **Response Caching**:
```javascript
class AIService {
    constructor() {
        this.responseCache = new Map();
        this.cacheTimeout = 3600000; // 1 hour
    }
    
    async generateResponse(prompt, context) {
        const cacheKey = `${prompt}-${JSON.stringify(context)}`;
        
        if (this.responseCache.has(cacheKey)) {
            const cached = this.responseCache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTimeout) {
                return cached.response;
            }
        }
        
        const response = await this.fetchResponse(prompt, context);
        this.responseCache.set(cacheKey, {
            response,
            timestamp: Date.now()
        });
        
        return response;
    }
}
```

2. **Batch Processing**:
```javascript
async batchAnalyze(items) {
    const batchPrompt = `Analyze these items efficiently:
    ${items.map((item, i) => `${i + 1}. ${item}`).join('\n')}
    
    Provide a consolidated analysis.`;
    
    return this.generateResponse(batchPrompt);
}
```

## Best Practices

### 1. Context Management
- Keep context relevant and concise
- Remove sensitive information
- Update context as system state changes

### 2. Error Handling
- Always provide fallbacks for offline mode
- Show clear error messages
- Log errors for debugging

### 3. User Experience
- Show loading states during AI processing
- Stream responses for better perceived performance
- Provide quick actions for common queries

### 4. Privacy
- Never send file contents to AI
- Anonymize system paths if needed
- Allow users to disable AI features

## Future Enhancements

### Planned Features

1. **Multi-model Support**:
   - Model selection in UI
   - Specialized models for different tasks
   - Model performance comparison

2. **Learning from Usage**:
   - Track successful cleanups
   - Improve recommendations over time
   - User preference learning

3. **Advanced Analytics**:
   - Disk usage predictions
   - Anomaly detection
   - Seasonal patterns

4. **Integration Extensions**:
   - Calendar integration for scheduled cleanups
   - Notification center alerts
   - Command-line AI interface

### Experimental Features

Enable experimental features:

```javascript
// In ai-service.js
this.experimental = {
    multiModal: false,      // Image analysis
    fineTuning: false,      // Custom model training
    plugins: false,         // AI plugin system
    voice: false           // Voice interaction
};
```

## Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Mistral Model Card](https://ollama.ai/library/mistral)
- [LLM Best Practices](https://github.com/brexhq/prompt-engineering)
- [Electron IPC Guide](https://www.electronjs.org/docs/latest/tutorial/ipc)

## Support

For AI-related issues:
- Check the [Troubleshooting](#troubleshooting) section
- Create an issue with the `ai-assistant` label
- Join the Ollama Discord community
- Email: mail@tommytracx.com