import React, { useState, useEffect } from 'react';
import './App.css';
import DataInput from './components/DataInput';
import ScanButton from './components/ScanButton';
import Dashboard from './components/Dashboard';
import ProgressBar from './components/ProgressBar';
import { initPyodide, runBiasDetection } from './utils/pyodideRunner';

function App() {
  const [pyodideReady, setPyodideReady] = useState(false);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);

  const analysisSteps = [
    'Loading data',
    'Computing PSI',
    'Computing CCS',
    'Computing ρ_PC',
    'Bootstrap resampling',
    'Generating report'
  ];

  // Skip Pyodide for testing - use mock detection
  useEffect(() => {
    console.log('Testing mode: Pyodide disabled');
    // Simulate Pyodide ready immediately
    setTimeout(() => {
      setPyodideReady(true);
      console.log('UI ready (mock mode)');
    }, 500);
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
    setProgress(0);
    setCurrentStep(0);

    try {
      // Simulate multi-step processing with progress updates
      const stepDuration = 400; // ms per step
      
      for (let i = 0; i < analysisSteps.length; i++) {
        setCurrentStep(i);
        setProgress((i / analysisSteps.length) * 100);
        
        // Simulate processing time for each step
        await new Promise(resolve => setTimeout(resolve, stepDuration));
        
        // Update progress within step
        setProgress(((i + 0.5) / analysisSteps.length) * 100);
        await new Promise(resolve => setTimeout(resolve, stepDuration / 2));
      }
      
      // Final progress
      setProgress(100);
      setCurrentStep(analysisSteps.length);
      
      // Wait a bit before showing results
      await new Promise(resolve => setTimeout(resolve, 300));
      
      const mockResults = {
        psi: 0.0238,
        psi_ci_lower: 0.0113,
        psi_ci_upper: 0.0676,
        psi_p_value: 0.355,
        ccs: 0.8860,
        ccs_ci_lower: 0.8723,
        ccs_ci_upper: 0.9530,
        ccs_p_value: 0.342,
        rho_pc: 0.9983,
        rho_pc_ci_lower: 0.9972,
        rho_pc_ci_upper: 1.0000,
        rho_pc_p_value: 0.772,
        overall_bias: false,
        confidence: 0.333,
        interpretation: 'No circular bias detected (confidence: 33.3%). Evaluation appears sound.',
        details: {
          algorithms_evaluated: ['GPT-3.5', 'Llama-2-7B', 'Claude-Instant', 'Mistral-7B'],
          time_periods: 5,
          indicators_triggered: 1
        },
        bootstrap_enabled: true
      };
      
      setResults(mockResults);
      console.log('Mock detection completed:', mockResults);
    } catch (err) {
      console.error('Detection failed:', err);
      setError(err.message || 'Detection failed');
    } finally {
      setLoading(false);
      setProgress(0);
      setCurrentStep(0);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔍 Sleuth</h1>
        <p className="subtitle">AI Evaluation Bias Hunter</p>
        <p className="subtitle" style={{color: '#ff9800', fontWeight: 'bold'}}>
          🧪 TEST MODE - Using Mock Detection
        </p>
      </header>

      <main className="App-main">
        {!pyodideReady && (
          <div className="loading-overlay">
            <div className="spinner"></div>
            <p>🧪 Loading UI (Test Mode - Using Mock Data)</p>
          </div>
        )}

        {pyodideReady && !results && !loading && (
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

        {pyodideReady && loading && (
          <ProgressBar 
            progress={progress}
            currentStep={currentStep}
            steps={analysisSteps}
          />
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
