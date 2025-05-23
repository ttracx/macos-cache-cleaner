const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs').promises;
const os = require('os');
const AIService = require('./ai-service');

let mainWindow;
let cleanerProcess = null;
let aiService = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    show: false,
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#f5f5f7',
    icon: path.join(__dirname, 'assets', 'icon.png')
  });

  mainWindow.loadFile('index.html');

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
  
  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });
}

app.whenReady().then(() => {
  createWindow();
  
  // Initialize AI service
  aiService = new AIService();
  setupAIHandlers();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC Handlers
ipcMain.handle('get-disk-usage', async () => {
  try {
    const result = await executeCommand('df', ['-H', '/']);
    const lines = result.stdout.split('\n');
    if (lines.length >= 2) {
      const parts = lines[1].split(/\s+/);
      if (parts.length >= 5) {
        return {
          total: parts[1],
          used: parts[2],
          available: parts[3],
          percentage: parseInt(parts[4])
        };
      }
    }
  } catch (error) {
    console.error('Error getting disk usage:', error);
  }
  return null;
});

ipcMain.handle('start-cleaning', async (event, options) => {
  const pythonScript = path.join(__dirname, '..', 'cache_cleaner.py');
  const args = [];
  
  if (options.dryRun) args.push('--dry-run');
  if (options.verbose) args.push('--verbose');
  if (options.skipTrash) args.push('--skip-trash');
  if (options.skipMaintenance) args.push('--skip-maintenance');
  if (options.findLargeFiles) args.push('--find-large-files');

  return new Promise((resolve, reject) => {
    cleanerProcess = spawn('python3', [pythonScript, ...args]);
    let outputData = '';
    let errorData = '';

    cleanerProcess.stdout.on('data', (data) => {
      const text = data.toString();
      outputData += text;
      event.sender.send('cleaning-output', text);
    });

    cleanerProcess.stderr.on('data', (data) => {
      const text = data.toString();
      errorData += text;
      event.sender.send('cleaning-error', text);
    });

    cleanerProcess.on('close', (code) => {
      cleanerProcess = null;
      if (code === 0) {
        resolve({ success: true, output: outputData });
      } else {
        reject({ success: false, error: errorData });
      }
    });

    cleanerProcess.on('error', (error) => {
      cleanerProcess = null;
      reject({ success: false, error: error.message });
    });
  });
});

ipcMain.handle('stop-cleaning', async () => {
  if (cleanerProcess) {
    cleanerProcess.kill('SIGTERM');
    cleanerProcess = null;
    return true;
  }
  return false;
});

ipcMain.handle('export-report', async (event, content) => {
  const result = await dialog.showSaveDialog(mainWindow, {
    defaultPath: `cache-cleaner-report-${new Date().toISOString().split('T')[0]}.txt`,
    filters: [
      { name: 'Text Files', extensions: ['txt'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  });

  if (!result.canceled) {
    try {
      await fs.writeFile(result.filePath, content);
      return { success: true, path: result.filePath };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
  return { success: false, canceled: true };
});

ipcMain.handle('open-logs', async () => {
  const logsPath = path.join(os.homedir(), 'Library', 'Logs');
  shell.openPath(logsPath);
});

ipcMain.handle('get-app-info', async () => {
  return {
    version: app.getVersion(),
    name: app.getName(),
    electron: process.versions.electron,
    node: process.versions.node,
    platform: process.platform,
    arch: process.arch
  };
});

// AI Handlers
function setupAIHandlers() {
  // Check AI status
  ipcMain.handle('ai-check-status', async () => {
    return await aiService.checkOllamaStatus();
  });

  // Ensure AI model is available
  ipcMain.handle('ai-ensure-model', async () => {
    return await aiService.ensureModel();
  });

  // Get AI recommendations
  ipcMain.handle('ai-get-recommendations', async (event, diskUsage, preferences) => {
    try {
      const response = await aiService.getCleaningRecommendations(diskUsage, preferences);
      return { success: true, response };
    } catch (error) {
      return { success: false, error: error.message };
    }
  });

  // Analyze cleaning results
  ipcMain.handle('ai-analyze-results', async (event, results) => {
    try {
      const response = await aiService.analyzeCleaningResults(results);
      return { success: true, response };
    } catch (error) {
      return { success: false, error: error.message };
    }
  });

  // Explain cache type
  ipcMain.handle('ai-explain-cache', async (event, cacheType) => {
    try {
      const response = await aiService.explainCacheType(cacheType);
      return { success: true, response };
    } catch (error) {
      return { success: false, error: error.message };
    }
  });

  // Get AI chat response
  ipcMain.handle('ai-chat', async (event, prompt, context) => {
    try {
      const response = await aiService.generateResponse(prompt, context);
      return { success: true, response };
    } catch (error) {
      return { success: false, error: error.message };
    }
  });

  // Setup AI event listeners
  aiService.on('status', (status) => {
    if (mainWindow) {
      mainWindow.webContents.send('ai-status', status);
    }
  });

  aiService.on('chunk', (chunk) => {
    if (mainWindow) {
      mainWindow.webContents.send('ai-response-chunk', chunk);
    }
  });

  aiService.on('download-progress', (progress) => {
    if (mainWindow) {
      mainWindow.webContents.send('ai-download-progress', progress);
    }
  });
}

// Helper function
function executeCommand(command, args) {
  return new Promise((resolve, reject) => {
    const process = spawn(command, args);
    let stdout = '';
    let stderr = '';

    process.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    process.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    process.on('close', (code) => {
      if (code === 0) {
        resolve({ stdout, stderr });
      } else {
        reject(new Error(`Command failed with code ${code}: ${stderr}`));
      }
    });
  });
}