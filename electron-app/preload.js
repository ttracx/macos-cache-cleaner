const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getDiskUsage: () => ipcRenderer.invoke('get-disk-usage'),
  startCleaning: (options) => ipcRenderer.invoke('start-cleaning', options),
  stopCleaning: () => ipcRenderer.invoke('stop-cleaning'),
  exportReport: (content) => ipcRenderer.invoke('export-report', content),
  openLogs: () => ipcRenderer.invoke('open-logs'),
  getAppInfo: () => ipcRenderer.invoke('get-app-info'),
  
  // AI functions
  ai: {
    checkStatus: () => ipcRenderer.invoke('ai-check-status'),
    ensureModel: () => ipcRenderer.invoke('ai-ensure-model'),
    getRecommendations: (diskUsage, preferences) => 
      ipcRenderer.invoke('ai-get-recommendations', diskUsage, preferences),
    analyzeResults: (results) => ipcRenderer.invoke('ai-analyze-results', results),
    explainCache: (cacheType) => ipcRenderer.invoke('ai-explain-cache', cacheType),
    chat: (prompt, context) => ipcRenderer.invoke('ai-chat', prompt, context)
  },
  
  // Event listeners
  onCleaningOutput: (callback) => {
    ipcRenderer.on('cleaning-output', (event, data) => callback(data));
  },
  onCleaningError: (callback) => {
    ipcRenderer.on('cleaning-error', (event, data) => callback(data));
  },
  onAIStatus: (callback) => {
    ipcRenderer.on('ai-status', (event, data) => callback(data));
  },
  onAIResponseChunk: (callback) => {
    ipcRenderer.on('ai-response-chunk', (event, data) => callback(data));
  },
  onAIDownloadProgress: (callback) => {
    ipcRenderer.on('ai-download-progress', (event, data) => callback(data));
  }
});