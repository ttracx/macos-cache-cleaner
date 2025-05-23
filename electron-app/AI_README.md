# AI Assistant Integration

The Cache Cleaner now includes an AI assistant powered by Ollama to provide intelligent recommendations and assistance for disk space management.

## Features

### 🤖 Intelligent Recommendations
- Analyzes your current disk usage and suggests optimal cleaning strategies
- Considers safety preferences and usage patterns
- Provides personalized advice based on your system state

### 📊 Results Analysis
- Reviews cleaning results and explains what was cleaned
- Identifies additional space-saving opportunities
- Provides insights into disk usage patterns

### ❓ Cache Education
- Explains what different cache types do
- Details the safety of deleting various caches
- Describes performance impacts and rebuild times

### 💬 Interactive Chat
- Ask any question about disk space management
- Get troubleshooting help for disk issues
- Receive tips for maintaining optimal disk space

## Setup

1. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Run the setup script**:
   ```bash
   ./setup-ollama.sh
   ```

3. **Launch the app** and click the 🤖 button to access the AI assistant

## System Instructions

The AI assistant is specifically trained for macOS Silicon maintenance with knowledge of:

- macOS file system structure and cache locations
- Development tool caches (Xcode, npm, Docker, etc.)
- Browser cache management
- System maintenance best practices
- Apple Silicon specific optimizations
- Safe vs aggressive cleaning strategies

## Privacy

All AI processing happens locally on your machine. No data is sent to external servers.

## Models

By default, the app uses Mistral 7B for broad compatibility. You can modify the model in `ai-service.js` if you prefer:

- `mistral:latest` - Default, balanced performance
- `llama2:latest` - Alternative option
- `codellama:latest` - Better for development-related queries

## Troubleshooting

If the AI assistant shows as offline:

1. Ensure Ollama is installed and running
2. Check that port 11434 is not blocked
3. Run `ollama list` to verify models are installed
4. Restart the Ollama service: `ollama serve`

## Usage Tips

- Be specific in your questions for better responses
- Provide context about your primary use case (development, design, etc.)
- Use the quick action buttons for common tasks
- The AI remembers your current disk usage for contextual advice