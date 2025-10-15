/**
 * Web Worker Manager
 * 
 * Handles communication with the bias detection Web Worker
 * Provides clean API for offloading computation
 */

class WorkerManager {
  constructor() {
    this.worker = null;
    this.progressCallback = null;
    this.completeCallback = null;
    this.errorCallback = null;
  }

  /**
   * Initialize the Web Worker
   */
  async init() {
    if (this.worker) {
      return; // Already initialized
    }

    try {
      // Create worker from file
      // Note: In production, you may need to adjust the path
      this.worker = new Worker(
        new URL('../workers/biasDetection.worker.js', import.meta.url),
        { type: 'module' }
      );

      // Set up message handler
      this.worker.onmessage = (event) => {
        this.handleMessage(event.data);
      };

      this.worker.onerror = (error) => {
        console.error('Worker error:', error);
        if (this.errorCallback) {
          this.errorCallback(error.message);
        }
      };

      // Send initialization message
      this.worker.postMessage({ type: 'INIT' });

      // Wait for initialization to complete
      await this.waitForInit();
      
      console.log('Worker manager initialized');
    } catch (error) {
      console.error('Failed to initialize worker:', error);
      throw error;
    }
  }

  /**
   * Wait for worker initialization
   */
  waitForInit() {
    return new Promise((resolve) => {
      const handler = (event) => {
        if (event.data.type === 'INIT_COMPLETE') {
          this.worker.removeEventListener('message', handler);
          resolve();
        }
      };
      this.worker.addEventListener('message', handler);
    });
  }

  /**
   * Handle messages from worker
   */
  handleMessage(data) {
    switch (data.type) {
      case 'PROGRESS':
        if (this.progressCallback) {
          this.progressCallback({
            step: data.step,
            progress: data.progress,
            message: data.message
          });
        }
        break;

      case 'COMPLETE':
        if (this.completeCallback) {
          this.completeCallback(data.results);
        }
        break;

      case 'ERROR':
        if (this.errorCallback) {
          this.errorCallback(data.error);
        }
        break;

      default:
        console.warn('Unknown message type:', data.type);
    }
  }

  /**
   * Run bias detection analysis
   * @param {Object} csvData - Parsed CSV data
   * @param {Function} onProgress - Progress callback
   * @param {Function} onComplete - Completion callback
   * @param {Function} onError - Error callback
   */
  async analyze(csvData, onProgress, onComplete, onError) {
    if (!this.worker) {
      await this.init();
    }

    this.progressCallback = onProgress;
    this.completeCallback = onComplete;
    this.errorCallback = onError;

    // Send analysis request to worker
    this.worker.postMessage({
      type: 'ANALYZE',
      data: csvData
    });
  }

  /**
   * Terminate the worker
   */
  terminate() {
    if (this.worker) {
      this.worker.terminate();
      this.worker = null;
      console.log('Worker terminated');
    }
  }
}

// Export singleton instance
export const workerManager = new WorkerManager();

/**
 * Helper function to run analysis with worker
 * @param {Object} csvData - Parsed CSV data
 * @returns {Promise} - Resolves with results
 */
export async function runAnalysisWithWorker(csvData, onProgress) {
  return new Promise((resolve, reject) => {
    workerManager.analyze(
      csvData,
      (progress) => {
        if (onProgress) {
          onProgress(progress);
        }
      },
      (results) => {
        resolve(results);
      },
      (error) => {
        reject(new Error(error));
      }
    );
  });
}

/**
 * Check if Web Workers are supported
 */
export function isWorkerSupported() {
  return typeof Worker !== 'undefined';
}
