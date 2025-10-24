// Client wrapper for Pyodide Web Worker with progress updates
let worker = null;
let readyPromise = null;

export function initPyodideInWorker() {
  if (readyPromise) return readyPromise;
  if (!worker) {
    // Use classic worker because importScripts is used inside the worker
    worker = new Worker(new URL('../workers/pyodide.worker.js', import.meta.url));
  }
  readyPromise = new Promise((resolve, reject) => {
    const onMessage = (e) => {
      const { type } = e.data || {};
      if (type === 'ready') {
        worker.removeEventListener('message', onMessage);
        resolve(true);
      }
    };
    const onError = (err) => {
      reject(err);
    };
    worker.addEventListener('message', onMessage);
    worker.addEventListener('error', onError, { once: true });
    worker.postMessage({ type: 'init' });
  });
  return readyPromise;
}

export function onPyodideProgress(cb) {
  if (!worker) return () => {};
  const handler = (e) => {
    const { type, payload } = e.data || {};
    if (type === 'progress') cb(payload);
  };
  worker.addEventListener('message', handler);
  return () => worker.removeEventListener('message', handler);
}

export async function runPython(code, variables) {
  if (!worker) throw new Error('Worker not initialized');
  return new Promise((resolve, reject) => {
    const handler = (e) => {
      const { type, payload } = e.data || {};
      if (type === 'result') {
        cleanup();
        resolve(payload);
      } else if (type === 'error') {
        cleanup();
        reject(new Error(payload));
      }
    };
    const cleanup = () => worker.removeEventListener('message', handler);
    worker.addEventListener('message', handler);
    worker.postMessage({ type: 'run', payload: { code, variables } });
  });
}
