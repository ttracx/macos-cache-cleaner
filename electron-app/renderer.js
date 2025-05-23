// DOM Elements
const elements = {
    // Disk usage
    diskUsed: document.getElementById('diskUsed'),
    diskAvailable: document.getElementById('diskAvailable'),
    diskTotal: document.getElementById('diskTotal'),
    diskPercentage: document.getElementById('diskPercentage'),
    diskChart: document.getElementById('diskChart'),
    
    // Options
    dryRun: document.getElementById('dryRun'),
    verbose: document.getElementById('verbose'),
    skipTrash: document.getElementById('skipTrash'),
    skipMaintenance: document.getElementById('skipMaintenance'),
    findLargeFiles: document.getElementById('findLargeFiles'),
    
    // Buttons
    scanBtn: document.getElementById('scanBtn'),
    safeBtn: document.getElementById('safeBtn'),
    deepBtn: document.getElementById('deepBtn'),
    startBtn: document.getElementById('startBtn'),
    stopBtn: document.getElementById('stopBtn'),
    logsBtn: document.getElementById('logsBtn'),
    clearBtn: document.getElementById('clearBtn'),
    exportBtn: document.getElementById('exportBtn'),
    aboutBtn: document.getElementById('aboutBtn'),
    closeAboutBtn: document.getElementById('closeAboutBtn'),
    aiBtn: document.getElementById('aiBtn'),
    
    // Progress
    progressCard: document.getElementById('progressCard'),
    progressStatus: document.getElementById('progressStatus'),
    progressFill: document.getElementById('progressFill'),
    spaceFreed: document.getElementById('spaceFreed'),
    
    // Console
    console: document.getElementById('console'),
    
    // Modal
    aboutModal: document.getElementById('aboutModal'),
    appVersion: document.getElementById('appVersion'),
    githubLink: document.getElementById('githubLink'),
    
    // AI Elements
    aiPanel: document.getElementById('aiPanel'),
    closeAIBtn: document.getElementById('closeAIBtn'),
    aiStatus: document.getElementById('aiStatus'),
    aiStatusIndicator: document.getElementById('aiStatusIndicator'),
    aiStatusText: document.getElementById('aiStatusText'),
    aiMessages: document.getElementById('aiMessages'),
    aiInput: document.getElementById('aiInput'),
    aiSendBtn: document.getElementById('aiSendBtn'),
    
    // Loading screen
    loadingScreen: document.getElementById('loadingScreen')
};

// State
let isRunning = false;
let consoleOutput = [];
let totalSpaceFreed = 0;
let currentDiskUsage = null;
let lastCleanupResults = '';
let aiReady = false;

// Initialize
async function init() {
    console.log('Starting initialization...');
    
    try {
        console.log('Setting up event listeners...');
        setupEventListeners();
        
        console.log('Setting up cleaning listeners...');
        setupCleaningListeners();
        
        console.log('Updating disk usage...');
        await updateDiskUsage();
        
        console.log('Setting up AI...');
        setupAI().catch(err => console.warn('AI setup failed:', err));
        
        console.log('Getting app info...');
        const appInfo = await window.electronAPI.getAppInfo();
        elements.appVersion.textContent = `Version ${appInfo.version}`;
        
        console.log('Initialization complete');
        
        // Hide loading screen
        setTimeout(() => {
            elements.loadingScreen.classList.add('hidden');
            setTimeout(() => {
                elements.loadingScreen.style.display = 'none';
            }, 500);
        }, 1000);
        
    } catch (error) {
        console.error('Error during initialization:', error);
        // Hide loading screen even on error
        elements.loadingScreen.classList.add('hidden');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Quick action buttons
    elements.scanBtn.addEventListener('click', () => {
        elements.dryRun.checked = true;
        elements.verbose.checked = true;
        elements.findLargeFiles.checked = true;
        startCleaning();
    });
    
    elements.safeBtn.addEventListener('click', () => {
        elements.dryRun.checked = false;
        elements.skipTrash.checked = true;
        elements.skipMaintenance.checked = true;
        startCleaning();
    });
    
    elements.deepBtn.addEventListener('click', () => {
        if (confirm('Deep Clean will remove all cache files, empty trash, and run system maintenance.\n\nThis is safe but may require administrator privileges.\n\nContinue?')) {
            elements.dryRun.checked = false;
            elements.skipTrash.checked = false;
            elements.skipMaintenance.checked = false;
            startCleaning();
        }
    });
    
    // Main buttons
    elements.startBtn.addEventListener('click', startCleaning);
    elements.stopBtn.addEventListener('click', stopCleaning);
    elements.logsBtn.addEventListener('click', () => window.electronAPI.openLogs());
    
    // Console actions
    elements.clearBtn.addEventListener('click', clearConsole);
    elements.exportBtn.addEventListener('click', exportReport);
    
    // Logo Easter egg
    const logoIcon = document.querySelector('.logo-icon');
    if (logoIcon) {
        logoIcon.addEventListener('click', () => {
            logoIcon.style.animation = 'loading-pulse 0.6s ease-in-out';
            setTimeout(() => {
                logoIcon.style.animation = '';
            }, 600);
        });
    }
    
    // About modal
    elements.aboutBtn.addEventListener('click', () => {
        elements.aboutModal.style.display = 'block';
    });
    
    elements.closeAboutBtn.addEventListener('click', () => {
        elements.aboutModal.style.display = 'none';
    });
    
    elements.githubLink.addEventListener('click', (e) => {
        e.preventDefault();
        window.open('https://github.com/ttracx/macos-cache-cleaner', '_blank');
    });
    
    // Close modal on outside click
    window.addEventListener('click', (e) => {
        if (e.target === elements.aboutModal) {
            elements.aboutModal.style.display = 'none';
        }
    });
}

// Setup cleaning output listeners
function setupCleaningListeners() {
    window.electronAPI.onCleaningOutput((data) => {
        addConsoleOutput(data, 'info');
        parseOutput(data);
    });
    
    window.electronAPI.onCleaningError((data) => {
        addConsoleOutput(data, 'error');
    });
}

// Update disk usage
async function updateDiskUsage() {
    const usage = await window.electronAPI.getDiskUsage();
    if (usage) {
        elements.diskUsed.textContent = usage.used;
        elements.diskAvailable.textContent = usage.available;
        elements.diskTotal.textContent = usage.total;
        elements.diskPercentage.textContent = `${usage.percentage}%`;
        
        drawDiskChart(usage.percentage);
    }
}

// Draw disk usage chart
function drawDiskChart(percentage) {
    const canvas = elements.diskChart;
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 50;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Background circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 10;
    ctx.stroke();
    
    // Progress arc
    const startAngle = -Math.PI / 2;
    const endAngle = startAngle + (2 * Math.PI * percentage / 100);
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, startAngle, endAngle);
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.stroke();
}

// Start cleaning
async function startCleaning() {
    if (isRunning) return;
    
    isRunning = true;
    totalSpaceFreed = 0;
    clearConsole();
    
    // Update UI
    elements.startBtn.disabled = true;
    elements.stopBtn.disabled = false;
    elements.progressCard.style.display = 'block';
    elements.progressStatus.textContent = 'Starting cleanup...';
    elements.progressFill.style.width = '0%';
    elements.spaceFreed.textContent = 'Space freed: 0 B';
    
    // Start progress animation
    animateProgress();
    
    // Get options
    const options = {
        dryRun: elements.dryRun.checked,
        verbose: elements.verbose.checked,
        skipTrash: elements.skipTrash.checked,
        skipMaintenance: elements.skipMaintenance.checked,
        findLargeFiles: elements.findLargeFiles.checked
    };
    
    try {
        const result = await window.electronAPI.startCleaning(options);
        if (result.success) {
            elements.progressStatus.textContent = 'Cleanup complete!';
            elements.progressFill.style.width = '100%';
            addConsoleOutput('\n✅ Cleanup completed successfully!', 'success');
        }
    } catch (error) {
        elements.progressStatus.textContent = 'Cleanup failed';
        addConsoleOutput(`\n❌ Error: ${error.error || error}`, 'error');
    } finally {
        isRunning = false;
        elements.startBtn.disabled = false;
        elements.stopBtn.disabled = true;
        
        // Update disk usage after cleaning
        setTimeout(updateDiskUsage, 1000);
    }
}

// Stop cleaning
async function stopCleaning() {
    if (!isRunning) return;
    
    const stopped = await window.electronAPI.stopCleaning();
    if (stopped) {
        isRunning = false;
        elements.startBtn.disabled = false;
        elements.stopBtn.disabled = true;
        elements.progressStatus.textContent = 'Cleanup stopped';
        addConsoleOutput('\n⚠️ Cleanup was stopped by user', 'warning');
    }
}

// Animate progress bar
function animateProgress() {
    if (!isRunning) return;
    
    const currentWidth = parseFloat(elements.progressFill.style.width) || 0;
    if (currentWidth < 90) {
        elements.progressFill.style.width = `${currentWidth + Math.random() * 5}%`;
    }
    
    setTimeout(animateProgress, 500);
}

// Parse output for progress updates
function parseOutput(data) {
    // Update status based on output
    if (data.includes('Cleaning System Caches')) {
        elements.progressStatus.textContent = 'Cleaning system caches...';
        elements.progressFill.style.width = '20%';
    } else if (data.includes('Cleaning Browser Data')) {
        elements.progressStatus.textContent = 'Cleaning browser data...';
        elements.progressFill.style.width = '40%';
    } else if (data.includes('Cleaning Temporary Files')) {
        elements.progressStatus.textContent = 'Cleaning temporary files...';
        elements.progressFill.style.width = '60%';
    } else if (data.includes('Cleaning Development Caches')) {
        elements.progressStatus.textContent = 'Cleaning development caches...';
        elements.progressFill.style.width = '80%';
    } else if (data.includes('Running macOS Maintenance')) {
        elements.progressStatus.textContent = 'Running system maintenance...';
        elements.progressFill.style.width = '90%';
    }
    
    // Parse freed space
    const freedMatch = data.match(/Freed:\s*([\d.]+\s*[KMGT]?B)/i);
    if (freedMatch) {
        const size = parseSize(freedMatch[1]);
        totalSpaceFreed += size;
        elements.spaceFreed.textContent = `Space freed: ${formatSize(totalSpaceFreed)}`;
    }
    
    // Parse total freed
    const totalMatch = data.match(/Total space freed:\s*([\d.]+\s*[KMGT]?B)/i);
    if (totalMatch) {
        elements.spaceFreed.textContent = `Space freed: ${totalMatch[1]}`;
    }
}

// Add output to console
function addConsoleOutput(text, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const line = { timestamp, text, type };
    consoleOutput.push(line);
    
    // Remove placeholder
    const placeholder = elements.console.querySelector('.console-placeholder');
    if (placeholder) {
        placeholder.remove();
    }
    
    // Add new lines
    const lines = text.split('\n');
    lines.forEach(lineText => {
        if (lineText.trim()) {
            const lineElement = document.createElement('div');
            lineElement.className = `console-line ${type}`;
            lineElement.textContent = lineText;
            elements.console.appendChild(lineElement);
        }
    });
    
    // Scroll to bottom
    elements.console.scrollTop = elements.console.scrollHeight;
}

// Clear console
function clearConsole() {
    consoleOutput = [];
    elements.console.innerHTML = '<div class="console-placeholder">Output will appear here...</div>';
}

// Export report
async function exportReport() {
    if (consoleOutput.length === 0) {
        alert('No output to export');
        return;
    }
    
    let content = 'Cache Cleaner Report\n';
    content += `Generated: ${new Date().toLocaleString()}\n`;
    content += '='.repeat(50) + '\n\n';
    
    consoleOutput.forEach(line => {
        content += `[${line.timestamp}] ${line.text}\n`;
    });
    
    const result = await window.electronAPI.exportReport(content);
    if (result.success) {
        addConsoleOutput(`Report exported to: ${result.path}`, 'success');
    } else if (!result.canceled) {
        alert(`Failed to export report: ${result.error}`);
    }
}

// Helper functions
function parseSize(sizeStr) {
    const match = sizeStr.match(/([\d.]+)\s*([KMGT]?)B/i);
    if (!match) return 0;
    
    const value = parseFloat(match[1]);
    const unit = match[2].toUpperCase();
    
    const multipliers = { '': 1, 'K': 1024, 'M': 1024*1024, 'G': 1024*1024*1024, 'T': 1024*1024*1024*1024 };
    return value * (multipliers[unit] || 1);
}

function formatSize(bytes) {
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let size = bytes;
    let unitIndex = 0;
    
    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }
    
    return `${size.toFixed(1)} ${units[unitIndex]}`;
}

// AI Functions
async function setupAI() {
    // Check AI status
    const status = await window.electronAPI.ai.checkStatus();
    
    if (status.available) {
        elements.aiStatusIndicator.classList.add('connected');
        elements.aiStatusText.textContent = 'AI Assistant Ready';
        aiReady = true;
        
        // Ensure model is available
        await window.electronAPI.ai.ensureModel();
    } else {
        elements.aiStatusIndicator.classList.add('error');
        elements.aiStatusText.textContent = 'AI Offline - Install Ollama to enable';
        aiReady = false;
    }
    
    // Setup AI event listeners
    window.electronAPI.onAIStatus((status) => {
        console.log('AI Status:', status);
    });
    
    window.electronAPI.onAIResponseChunk((chunk) => {
        // Handle streaming responses
        const thinkingElement = elements.aiMessages.querySelector('.ai-thinking');
        if (thinkingElement) {
            thinkingElement.remove();
        }
        
        let lastMessage = elements.aiMessages.lastElementChild;
        if (!lastMessage || !lastMessage.classList.contains('ai-message-assistant')) {
            lastMessage = createAIMessage('', 'assistant');
        }
        
        lastMessage.innerHTML += chunk;
        lastMessage.scrollIntoView({ behavior: 'smooth' });
    });
    
    window.electronAPI.onAIDownloadProgress((progress) => {
        elements.aiStatusText.textContent = `Downloading AI model... ${progress}`;
    });
    
    // AI Panel controls
    elements.aiBtn.addEventListener('click', () => {
        elements.aiPanel.classList.add('active');
    });
    
    elements.closeAIBtn.addEventListener('click', () => {
        elements.aiPanel.classList.remove('active');
    });
    
    // AI quick actions
    document.querySelectorAll('.ai-quick-btn').forEach(btn => {
        btn.addEventListener('click', () => handleAIQuickAction(btn.dataset.action));
    });
    
    // AI chat input
    elements.aiInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendAIMessage();
        }
    });
    
    elements.aiSendBtn.addEventListener('click', sendAIMessage);
}

function createAIMessage(content, type = 'user') {
    const message = document.createElement('div');
    message.className = `ai-message ai-message-${type}`;
    message.innerHTML = content;
    elements.aiMessages.appendChild(message);
    message.scrollIntoView({ behavior: 'smooth' });
    return message;
}

function showAIThinking() {
    const thinking = document.createElement('div');
    thinking.className = 'ai-thinking';
    thinking.innerHTML = '<span></span><span></span><span></span>';
    elements.aiMessages.appendChild(thinking);
    thinking.scrollIntoView({ behavior: 'smooth' });
}

async function handleAIQuickAction(action) {
    if (!aiReady) {
        createAIMessage('AI Assistant is not available. Please install Ollama to enable AI features.', 'system');
        return;
    }
    
    switch (action) {
        case 'recommend':
            await getAIRecommendations();
            break;
        case 'analyze':
            await analyzeLastResults();
            break;
        case 'explain':
            await showCacheExplanation();
            break;
    }
}

async function getAIRecommendations() {
    createAIMessage('What cleaning strategy would you recommend for my current disk usage?', 'user');
    showAIThinking();
    
    try {
        const preferences = {
            safetyLevel: elements.skipTrash.checked ? 'conservative' : 'balanced',
            primaryUse: 'development', // Could be detected or asked
            lastCleanup: lastCleanupResults ? 'recent' : 'unknown'
        };
        
        const result = await window.electronAPI.ai.getRecommendations(currentDiskUsage, preferences);
        
        if (result.success) {
            elements.aiMessages.querySelector('.ai-thinking')?.remove();
            createAIMessage(result.response, 'assistant');
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        elements.aiMessages.querySelector('.ai-thinking')?.remove();
        createAIMessage(`Error: ${error.message}`, 'system');
    }
}

async function analyzeLastResults() {
    if (!lastCleanupResults) {
        createAIMessage('No recent cleanup results to analyze. Run a cleanup first!', 'system');
        return;
    }
    
    createAIMessage('Can you analyze my last cleanup results?', 'user');
    showAIThinking();
    
    try {
        const result = await window.electronAPI.ai.analyzeResults(lastCleanupResults);
        
        if (result.success) {
            elements.aiMessages.querySelector('.ai-thinking')?.remove();
            createAIMessage(result.response, 'assistant');
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        elements.aiMessages.querySelector('.ai-thinking')?.remove();
        createAIMessage(`Error: ${error.message}`, 'system');
    }
}

async function showCacheExplanation() {
    const cacheTypes = [
        'System Caches',
        'Browser Caches',
        'Development Caches (npm, Xcode)',
        'Application Caches'
    ];
    
    const buttons = cacheTypes.map(type => 
        `<button class="ai-quick-btn" onclick="explainCacheType('${type}')" style="margin: 4px">${type}</button>`
    ).join('');
    
    createAIMessage(`Which cache type would you like me to explain?<br><br>${buttons}`, 'assistant');
}

window.explainCacheType = async function(cacheType) {
    createAIMessage(`Explain ${cacheType}`, 'user');
    showAIThinking();
    
    try {
        const result = await window.electronAPI.ai.explainCache(cacheType);
        
        if (result.success) {
            elements.aiMessages.querySelector('.ai-thinking')?.remove();
            createAIMessage(result.response, 'assistant');
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        elements.aiMessages.querySelector('.ai-thinking')?.remove();
        createAIMessage(`Error: ${error.message}`, 'system');
    }
};

async function sendAIMessage() {
    const message = elements.aiInput.value.trim();
    if (!message || !aiReady) return;
    
    createAIMessage(message, 'user');
    elements.aiInput.value = '';
    elements.aiSendBtn.disabled = true;
    showAIThinking();
    
    try {
        const context = {
            diskUsage: currentDiskUsage,
            lastCleanup: lastCleanupResults
        };
        
        const result = await window.electronAPI.ai.chat(message, context);
        
        if (result.success) {
            elements.aiMessages.querySelector('.ai-thinking')?.remove();
            createAIMessage(result.response, 'assistant');
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        elements.aiMessages.querySelector('.ai-thinking')?.remove();
        createAIMessage(`Error: ${error.message}`, 'system');
    } finally {
        elements.aiSendBtn.disabled = false;
    }
}

// Update the updateDiskUsage function to store current usage
const originalUpdateDiskUsage = updateDiskUsage;
async function updateDiskUsage() {
    const usage = await window.electronAPI.getDiskUsage();
    if (usage) {
        currentDiskUsage = usage;
        elements.diskUsed.textContent = usage.used;
        elements.diskAvailable.textContent = usage.available;
        elements.diskTotal.textContent = usage.total;
        elements.diskPercentage.textContent = `${usage.percentage}%`;
        
        drawDiskChart(usage.percentage);
    }
}

// Update the startCleaning function to capture results
const originalStartCleaning = startCleaning;
async function startCleaning() {
    if (isRunning) return;
    
    isRunning = true;
    totalSpaceFreed = 0;
    lastCleanupResults = ''; // Reset results
    clearConsole();
    
    // Update UI
    elements.startBtn.disabled = true;
    elements.stopBtn.disabled = false;
    elements.progressCard.style.display = 'block';
    elements.progressStatus.textContent = 'Starting cleanup...';
    elements.progressFill.style.width = '0%';
    elements.spaceFreed.textContent = 'Space freed: 0 B';
    
    // Start progress animation
    animateProgress();
    
    // Get options
    const options = {
        dryRun: elements.dryRun.checked,
        verbose: elements.verbose.checked,
        skipTrash: elements.skipTrash.checked,
        skipMaintenance: elements.skipMaintenance.checked,
        findLargeFiles: elements.findLargeFiles.checked
    };
    
    try {
        const result = await window.electronAPI.startCleaning(options);
        if (result.success) {
            elements.progressStatus.textContent = 'Cleanup complete!';
            elements.progressFill.style.width = '100%';
            addConsoleOutput('\n✅ Cleanup completed successfully!', 'success');
            lastCleanupResults = result.output; // Store results
        }
    } catch (error) {
        elements.progressStatus.textContent = 'Cleanup failed';
        addConsoleOutput(`\n❌ Error: ${error.error || error}`, 'error');
    } finally {
        isRunning = false;
        elements.startBtn.disabled = false;
        elements.stopBtn.disabled = true;
        
        // Update disk usage after cleaning
        setTimeout(updateDiskUsage, 1000);
    }
}

// Debug logging
console.log('Renderer script loaded');

// Initialize app with error handling
try {
    init();
    console.log('App initialized successfully');
} catch (error) {
    console.error('Failed to initialize app:', error);
}