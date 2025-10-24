self.onmessage = async (event) => {
  const { type, payload } = event.data || {};
  try {
    if (type === 'init') {
      self.postMessage({ type: 'progress', payload: { stage: 'downloading', progress: 0.05 } });
      if (!self.loadPyodide) {
        importScripts('https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js');
      }
      self.postMessage({ type: 'progress', payload: { stage: 'initializing', progress: 0.15 } });
      self.pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/' });
      self.postMessage({ type: 'progress', payload: { stage: 'loading-packages', progress: 0.25 } });
      await self.pyodide.loadPackage(['numpy', 'pandas', 'scipy']);
      self.postMessage({ type: 'progress', payload: { stage: 'ready', progress: 1 } });
      self.postMessage({ type: 'ready' });
    } else if (type === 'run') {
      if (!self.pyodide) throw new Error('Pyodide not initialized');
      const { code, variables } = payload || {};
      if (variables) {
        for (const [k, v] of Object.entries(variables)) {
          self.pyodide.globals.set(k, v);
        }
      }
      const result = await self.pyodide.runPythonAsync(code);
      self.postMessage({ type: 'result', payload: result });
    }
  } catch (err) {
    self.postMessage({ type: 'error', payload: String(err && err.message ? err.message : err) });
  }
};
