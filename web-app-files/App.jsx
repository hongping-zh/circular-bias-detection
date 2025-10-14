import React, { useState, useEffect } from 'react';
import './App.css';
import DataInput from './components/DataInput';
import ScanButton from './components/ScanButton';
import Dashboard from './components/Dashboard';
import { initPyodide, runBiasDetection } from './utils/pyodideRunner';

function App() {
  const [pyodideReady, setPyodideReady] = useState(false);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Initialize Pyodide on mount
  useEffect(() => {
    console.log('Initializing Pyodide...');
    initPyodide()
      .then(() => {
        console.log('Pyodide ready!');
        setPyodideReady(true);
      })
      .catch(err => {
        console.error('Pyodide initialization failed:', err);
        setError('Failed to initialize Python engine');
      });
  }, []);

  const handleDataLoad = (csvData) => {
    setData(csvData);
    setResults(null);
    setError(null);
  };

  const handleScan = async () => {
    if (!data) {
      setError('Please load data first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const detectionResults = await runBiasDetection(data);
      setResults(detectionResults);
    } catch (err) {
      console.error('Detection failed:', err);
      setError(err.message || 'Detection failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔍 Circular Bias Scanner</h1>
        <p className="subtitle">Detect evaluation bias in 30 seconds</p>
      </header>

      <main className="App-main">
        {!pyodideReady && (
          <div className="loading-overlay">
            <div className="spinner"></div>
            <p>Loading Python engine... (first time only, ~30 seconds)</p>
          </div>
        )}

        {pyodideReady && !results && (
          <>
            <DataInput onDataLoad={handleDataLoad} />
            
            <ScanButton 
              onClick={handleScan} 
              disabled={!data || loading}
              loading={loading}
            />

            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}

            <div className="features">
              <h3>✨ Features</h3>
              <ul>
                <li>✓ No signup required</li>
                <li>✓ No data uploaded to server</li>
                <li>✓ Results in &lt; 1 minute</li>
                <li>✓ Free and open source</li>
              </ul>
            </div>
          </>
        )}

        {results && (
          <Dashboard 
            results={results} 
            onReset={() => {
              setResults(null);
              setData(null);
            }}
          />
        )}
      </main>

      <footer className="App-footer">
        <p>
          Powered by{' '}
          <a href="https://github.com/hongping-zh/circular-bias-detection" 
             target="_blank" 
             rel="noopener noreferrer">
            Circular Bias Detection Framework
          </a>
          {' | '}
          Dataset:{' '}
          <a href="https://doi.org/10.5281/zenodo.17201032"
             target="_blank"
             rel="noopener noreferrer">
            DOI: 10.5281/zenodo.17201032
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
