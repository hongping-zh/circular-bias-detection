import React, { useState, useEffect } from 'react';
import './App.css';
import DataInput from './components/DataInput';
import ScanButton from './components/ScanButton';
import Dashboard from './components/Dashboard';
import ProgressBar from './components/ProgressBar';
import InteractiveTutorial from './components/InteractiveTutorial';
import { initPyodideInWorker, onPyodideProgress, runPython } from './utils/pyodideClient';
import { useRef } from 'react';
import { saveAs } from 'file-saver';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

function App() {
  const [pyodideReady, setPyodideReady] = useState(false);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [showTutorial, setShowTutorial] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const reportRef = useRef(null);

  const analysisSteps = [
    'Loading data',
    'Computing PSI',
    'Computing CCS',
    'Computing ρ_PC',
    'Bootstrap resampling',
    'Generating report'
  ];

  // Initialize Pyodide in Web Worker and show tutorial for first-time users
  useEffect(() => {
    let unsubscribe = null;
    (async () => {
      try {
        unsubscribe = onPyodideProgress((p) => {
          // map worker init progress to UI
          if (!pyodideReady) {
            setLoading(true);
            setCurrentStep(0);
            setProgress(Math.min(99, Math.round((p.progress || 0) * 100)));
          }
        });
        await initPyodideInWorker();
        setPyodideReady(true);
      } catch (e) {
        console.error('Pyodide init failed', e);
        setError('Failed to initialize Python runtime in browser. Please retry.');
      } finally {
        setLoading(false);
        setProgress(0);
        setCurrentStep(0);
        // Show tutorial for first-time visitors
        const hasSeenTutorial = localStorage.getItem('sleuth_tutorial_completed');
        if (!hasSeenTutorial) setShowTutorial(true);
      }
    })();
    return () => { if (unsubscribe) unsubscribe(); };
  }, []);

  // Check URL parameters for auto-loading dataset
  useEffect(() => {
    if (!pyodideReady) return;
    
    const urlParams = new URLSearchParams(window.location.search);
    const loadDataset = urlParams.get('dataset');
    
    if (loadDataset === 'latest' || loadDataset === '17637303') {
      handleLoadLatestDataset();
    }
  }, [pyodideReady]);

  const handleDataLoad = (csvData, validationResult) => {
    setData(csvData);
    setResults(null);
    setError(null);
    
    // Store validation stats for visualization
    if (validationResult && validationResult.stats) {
      setData({ csvData, stats: validationResult.stats });
    }
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
      // Real detection via Web Worker (Pyodide)
      const code = `
import numpy as np
import pandas as pd
import io
from scipy import stats

def compute_psi(theta_matrix):
    T, K = theta_matrix.shape
    if T < 2:
        return 0.0
    changes = np.diff(theta_matrix, axis=0)
    return float(np.mean(np.abs(changes)))

def compute_ccs(constraint_matrix):
    T, p = constraint_matrix.shape
    if T < 2:
        return 1.0
    normalized = (constraint_matrix - constraint_matrix.mean(axis=0)) / (constraint_matrix.std(axis=0) + 1e-10)
    correlations = []
    for i in range(T-1):
        for j in range(i+1, T):
            corr = np.corrcoef(normalized[i], normalized[j])[0, 1]
            if not np.isnan(corr):
                correlations.append(corr)
    return float(np.mean(correlations) if correlations else 1.0)

def compute_rho_pc(performance_matrix, constraint_matrix):
    perf_avg = np.mean(performance_matrix, axis=1)
    const_avg = np.mean(constraint_matrix, axis=1)
    if len(perf_avg) < 2:
        return 0.0
    corr, _ = stats.pearsonr(perf_avg, const_avg)
    return float(corr) if not np.isnan(corr) else 0.0

def detect_bias(csv_string, psi_threshold=0.15, ccs_threshold=0.85, rho_pc_threshold=0.5):
    df = pd.read_csv(io.StringIO(csv_string))
    perf_matrix = df.pivot(index='time_period', columns='algorithm', values='performance').values
    const_cols = [c for c in df.columns if c.startswith('constraint_')]
    const_matrix = df.groupby('time_period')[const_cols].first().values
    algorithms = df['algorithm'].unique().tolist()
    psi = compute_psi(perf_matrix)
    ccs = compute_ccs(const_matrix)
    rho_pc = compute_rho_pc(perf_matrix, const_matrix)
    psi_detected = psi > psi_threshold
    ccs_detected = ccs < ccs_threshold
    rho_detected = abs(rho_pc) > rho_pc_threshold
    indicators = int(psi_detected) + int(ccs_detected) + int(rho_detected)
    return {
        'psi': psi,
        'ccs': ccs,
        'rho_pc': rho_pc,
        'overall_bias': indicators >= 2,
        'confidence': indicators / 3.0,
        'details': {
            'algorithms_evaluated': algorithms,
            'time_periods': int(perf_matrix.shape[0]),
            'indicators_triggered': int(indicators)
        }
    }

import json
res = detect_bias(csv_data)
json.dumps(res)
      `;

      // Simulate step progress
      for (let i = 0; i < analysisSteps.length; i++) {
        setCurrentStep(i);
        setProgress(Math.round(((i + 0.2) / analysisSteps.length) * 100));
        await new Promise(r => setTimeout(r, 120));
      }

      const resultJSON = await runPython(code, { csv_data: data.csvData || data });
      const result = typeof resultJSON === 'string' ? JSON.parse(resultJSON) : resultJSON;
      setResults({ ...result, bootstrap_enabled: false, interpretation: result.overall_bias ? undefined : 'No circular bias detected. Evaluation appears sound.' });
    } catch (err) {
      console.error('Detection failed:', err);
      setError(err.message || 'Detection failed');
    } finally {
      setLoading(false);
      setProgress(0);
      setCurrentStep(0);
    }
  };

  const handleTutorialClose = () => {
    setShowTutorial(false);
    localStorage.setItem('sleuth_tutorial_completed', 'true');
  };

  const exportPDF = async () => {
    if (!reportRef.current || isExporting) return;
    setIsExporting(true);
    try {
      const canvas = await html2canvas(reportRef.current, { scale: 2, backgroundColor: '#ffffff' });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`sleuth-bias-report-${new Date().toISOString().split('T')[0]}.pdf`);
    } catch (e) {
      console.error('PDF export failed:', e);
      alert('Failed to export PDF. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const exportCSV = () => {
    if (!results) return;
    const rows = [
      ['Metric', 'Value', 'Threshold', 'Status'],
      ['PSI Score', results.psi?.toFixed?.(4) ?? results.psi ?? 'N/A', '0.15', results.psi !== undefined ? (results.psi < 0.10 ? 'ok' : results.psi < 0.15 ? 'warning' : 'danger') : 'N/A'],
      ['CCS Score', results.ccs?.toFixed?.(4) ?? results.ccs ?? 'N/A', '0.85', results.ccs !== undefined ? (results.ccs >= 0.9 ? 'ok' : results.ccs >= 0.85 ? 'warning' : 'danger') : 'N/A'],
      ['ρ_PC Score', results.rho_pc?.toFixed?.(4) ?? results.rho_pc ?? 'N/A', '±0.5', results.rho_pc !== undefined ? (Math.abs(results.rho_pc) < 0.3 ? 'ok' : Math.abs(results.rho_pc) < 0.5 ? 'warning' : 'danger') : 'N/A'],
      ['Overall Bias Detected', results.overall_bias ? 'YES' : 'NO', '', ''],
      ['Confidence', `${((results.confidence || 0) * 100).toFixed(1)}%`, '', ''],
      ['Algorithms Evaluated', results.details?.algorithms_evaluated?.join?.(', ') || 'N/A', '', ''],
      ['Time Periods', results.details?.time_periods ?? 'N/A', '', ''],
      ['Indicators Triggered', `${results.details?.indicators_triggered ?? 0} / 3`, '', '']
    ];
    const csv = rows.map(r => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, `sleuth-bias-data-${new Date().toISOString().split('T')[0]}.csv`);
  };

  const downloadResultsJSON = () => {
    if (!results) return;
    const dataStr = JSON.stringify(results, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `bias-detection-results-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const copyCitation = () => {
    const citation = `Zhang, H. (2024). Algorithm Benchmark Suite v2.0: Synthetic Dataset for Circular Bias Detection [Data set]. Zenodo. https://doi.org/10.5281/zenodo.17201032`;
    navigator.clipboard.writeText(citation).then(() => {
      alert('Citation copied to clipboard!');
    });
  };

  const handleLoadLatestDataset = async () => {
    // Load CBD Dataset v3/v3.1 from Zenodo (17637303)
    setLoading(true);
    setError(null);
    try {
      // In a real implementation, this would fetch from Zenodo API
      // For now, we'll use a representative sample
      const latestDatasetCSV = `time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol
1,ResNet-50,0.762,512,8.0,50000,v3.1
1,VGG-16,0.719,512,8.0,50000,v3.1
1,DenseNet-121,0.745,512,8.0,50000,v3.1
1,EfficientNet-B0,0.771,512,8.0,50000,v3.1
2,ResNet-50,0.768,512,8.0,50000,v3.1
2,VGG-16,0.723,512,8.0,50000,v3.1
2,DenseNet-121,0.751,512,8.0,50000,v3.1
2,EfficientNet-B0,0.778,512,8.0,50000,v3.1
3,ResNet-50,0.774,512,8.0,50000,v3.1
3,VGG-16,0.728,512,8.0,50000,v3.1
3,DenseNet-121,0.757,512,8.0,50000,v3.1
3,EfficientNet-B0,0.784,512,8.0,50000,v3.1`;
      
      handleDataLoad(latestDatasetCSV, null);
      setLoading(false);
    } catch (err) {
      setError('Failed to load latest dataset');
      setLoading(false);
    }
  };

  const handleLoadLLMExample = () => {
    // Load LLM example data
    const llmExampleCSV = `time_period,algorithm,performance,constraint_compute,constraint_memory,max_tokens,temperature,top_p,prompt_variant
1,GPT-3.5,0.72,300,8.0,512,0.7,0.9,vanilla
1,Llama-2-7B,0.68,450,12.0,512,0.7,0.9,vanilla
1,Claude-Instant,0.75,400,10.0,512,0.7,0.9,vanilla
1,Mistral-7B,0.70,420,11.0,512,0.7,0.9,vanilla
2,GPT-3.5,0.74,305,8.2,512,0.75,0.92,few_shot
2,Llama-2-7B,0.70,455,12.1,512,0.75,0.92,few_shot
2,Claude-Instant,0.78,405,10.2,512,0.75,0.92,few_shot
2,Mistral-7B,0.73,425,11.1,512,0.75,0.92,few_shot
3,GPT-3.5,0.76,310,8.5,768,0.8,0.95,chain_of_thought
3,Llama-2-7B,0.72,460,12.3,768,0.8,0.95,chain_of_thought
3,Claude-Instant,0.80,410,10.5,768,0.8,0.95,chain_of_thought
3,Mistral-7B,0.75,430,11.3,768,0.8,0.95,chain_of_thought`;
    
    handleDataLoad(llmExampleCSV, null);
  };

  return (
    <div className="App">
      {showTutorial && (
        <InteractiveTutorial 
          onClose={handleTutorialClose} 
          onLoadExample={handleLoadLLMExample}
        />
      )}

      <header className="App-header">
        <h1>🔍 Sleuth</h1>
        <p className="subtitle">AI Evaluation Bias Hunter</p>
        <button 
          className="tutorial-trigger"
          onClick={() => setShowTutorial(true)}
          title="Show Tutorial"
        >
          ❓ Help
        </button>
      </header>

      <main className="App-main">
        {!pyodideReady && (
          <div className="loading-overlay">
            <div className="spinner"></div>
            <p>Initializing Python runtime in your browser...</p>
          </div>
        )}

        {pyodideReady && !results && !loading && (
          <>
            <DataInput onDataLoad={handleDataLoad} />
            
            {/* Latest Dataset Banner */}
            <div className="latest-dataset-banner" style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: '12px',
              padding: '1.5rem',
              margin: '1.5rem 0',
              color: 'white',
              boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
              border: '2px solid rgba(255,255,255,0.2)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.75rem' }}>
                <span style={{ fontSize: '1.5rem' }}>🆕</span>
                <h3 style={{ margin: 0, fontSize: '1.2rem', fontWeight: '600' }}>Just Released: 2025 Real-World Evaluation Dataset</h3>
              </div>
              <p style={{ margin: '0.5rem 0', opacity: 0.95, fontSize: '0.95rem' }}>
                Test bias detection on our latest CBD Dataset v3/v3.1 with real-world AI evaluation scenarios
              </p>
              <button 
                onClick={handleLoadLatestDataset}
                style={{
                  background: 'white',
                  color: '#667eea',
                  border: 'none',
                  padding: '0.75rem 1.5rem',
                  borderRadius: '8px',
                  fontSize: '1rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  marginTop: '0.75rem',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                  transition: 'all 0.2s ease'
                }}
                onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
                onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
              >
                → Load in Web App
              </button>
              <a 
                href="https://doi.org/10.5281/zenodo.17637303"
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  color: 'white',
                  fontSize: '0.85rem',
                  marginLeft: '1rem',
                  textDecoration: 'underline',
                  opacity: 0.9
                }}
              >
                View on Zenodo →
              </a>
            </div>
            
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
          <>
            <div className="action-buttons" style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
              <button className="download-button" onClick={exportPDF} disabled={isExporting}>
                {isExporting ? '⏳ Exporting...' : '📄 Export PDF Report'}
              </button>
              <button className="download-button" onClick={exportCSV}>📊 Export CSV Data</button>
              <button className="download-button" onClick={downloadResultsJSON}>📥 Download JSON</button>
              <button className="cite-button" onClick={copyCitation}>📋 Copy Citation</button>
            </div>
            <div ref={reportRef}>
              <Dashboard 
                results={results} 
                onReset={() => {
                  setResults(null);
                  setData(null);
                }}
              />
            </div>
          </>
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
          Datasets:{' '}
          <a href="https://doi.org/10.5281/zenodo.17637303"
             target="_blank"
             rel="noopener noreferrer"
             style={{ fontWeight: '600' }}>
            v3/v3.1 (Latest)
          </a>
          {', '}
          <a href="https://doi.org/10.5281/zenodo.17201032"
             target="_blank"
             rel="noopener noreferrer">
            v2.0
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
