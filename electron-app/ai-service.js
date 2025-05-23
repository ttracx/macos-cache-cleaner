const { spawn } = require('child_process');
const EventEmitter = require('events');

class AIService extends EventEmitter {
    constructor() {
        super();
        this.model = 'mistral:latest'; // Using mistral for broad compatibility
        this.baseUrl = 'http://localhost:11434';
        this.systemPrompt = `You are an AI assistant specialized in macOS Silicon system maintenance and disk space optimization. Your role is to:

1. Analyze disk usage patterns and provide intelligent recommendations
2. Identify potential space-saving opportunities specific to macOS
3. Explain what different cache types do and their impact on system performance
4. Provide safety warnings when appropriate
5. Suggest optimal cleaning strategies based on user's system state
6. Help users understand the impact of cleaning different cache types
7. Provide tips for maintaining optimal disk space on Apple Silicon Macs

Key knowledge areas:
- macOS file system structure and cache locations
- Development tool caches (Xcode, npm, Docker, etc.)
- Browser cache management
- System maintenance best practices
- Apple Silicon specific optimizations
- Safe vs aggressive cleaning strategies

Always prioritize data safety and system stability in your recommendations.`;
    }

    async checkOllamaStatus() {
        try {
            const response = await fetch(`${this.baseUrl}/api/version`);
            if (response.ok) {
                return { available: true, version: await response.json() };
            }
            return { available: false, error: 'Ollama not responding' };
        } catch (error) {
            return { available: false, error: error.message };
        }
    }

    async ensureModel() {
        try {
            // Check if model exists
            const response = await fetch(`${this.baseUrl}/api/show`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: this.model })
            });

            if (!response.ok) {
                // Model doesn't exist, try to pull it
                this.emit('status', 'Downloading AI model... This may take a few minutes on first run.');
                await this.pullModel();
            }
            return true;
        } catch (error) {
            console.error('Error ensuring model:', error);
            return false;
        }
    }

    async pullModel() {
        return new Promise((resolve, reject) => {
            const pullProcess = spawn('ollama', ['pull', this.model]);
            
            pullProcess.stdout.on('data', (data) => {
                this.emit('download-progress', data.toString());
            });

            pullProcess.stderr.on('data', (data) => {
                console.error('Pull error:', data.toString());
            });

            pullProcess.on('close', (code) => {
                if (code === 0) {
                    this.emit('status', 'AI model ready!');
                    resolve();
                } else {
                    reject(new Error(`Model pull failed with code ${code}`));
                }
            });
        });
    }

    async generateResponse(prompt, context = {}) {
        try {
            const messages = [
                { role: 'system', content: this.systemPrompt }
            ];

            // Add context if provided
            if (context.diskUsage) {
                messages.push({
                    role: 'system',
                    content: `Current disk usage: ${context.diskUsage.used} used of ${context.diskUsage.total} (${context.diskUsage.percentage}% full)`
                });
            }

            if (context.lastCleanup) {
                messages.push({
                    role: 'system',
                    content: `Last cleanup results: ${context.lastCleanup}`
                });
            }

            messages.push({ role: 'user', content: prompt });

            const response = await fetch(`${this.baseUrl}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: this.model,
                    messages: messages,
                    stream: true
                })
            });

            if (!response.ok) {
                throw new Error('Failed to generate response');
            }

            // Handle streaming response
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let fullResponse = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n').filter(line => line.trim());

                for (const line of lines) {
                    try {
                        const json = JSON.parse(line);
                        if (json.message && json.message.content) {
                            fullResponse += json.message.content;
                            this.emit('chunk', json.message.content);
                        }
                    } catch (e) {
                        // Ignore parsing errors
                    }
                }
            }

            return fullResponse;
        } catch (error) {
            console.error('AI generation error:', error);
            throw error;
        }
    }

    async analyzeCleaningResults(results) {
        const prompt = `Analyze these cache cleaning results and provide insights:

${results}

Please provide:
1. A summary of what was cleaned
2. Why this amount of space was freed
3. Suggestions for additional space savings
4. Any warnings or things to watch out for`;

        return this.generateResponse(prompt);
    }

    async getCleaningRecommendations(diskUsage, userPreferences) {
        const prompt = `Based on the current disk usage (${diskUsage.percentage}% full), recommend an optimal cleaning strategy.

User preferences:
- Safety level: ${userPreferences.safetyLevel || 'balanced'}
- Primary use: ${userPreferences.primaryUse || 'general'}
- Last cleanup: ${userPreferences.lastCleanup || 'unknown'}

Provide specific recommendations for:
1. Which caches are safe to clean
2. Expected space savings
3. Optimal cleaning frequency
4. Any special considerations for Apple Silicon Macs`;

        return this.generateResponse(prompt, { diskUsage });
    }

    async explainCacheType(cacheType) {
        const prompt = `Explain what the ${cacheType} cache does on macOS:

1. What is stored in this cache?
2. Is it safe to delete?
3. What happens after deletion?
4. How quickly does it rebuild?
5. Any performance impact?

Keep the explanation concise and user-friendly.`;

        return this.generateResponse(prompt);
    }

    async troubleshoot(issue) {
        const prompt = `Help troubleshoot this macOS disk space issue:

${issue}

Provide:
1. Possible causes
2. Step-by-step solutions
3. Preventive measures
4. When to be concerned`;

        return this.generateResponse(prompt);
    }
}

module.exports = AIService;