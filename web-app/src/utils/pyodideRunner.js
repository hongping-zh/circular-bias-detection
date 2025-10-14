/**
 * PyOdide Runner - Execute Python bias detection in the browser
 */

let pyodide = null;
let pyodideReady = false;

/**
 * Initialize Pyodide and load required packages
 */
export async function initPyodide() {
  if (pyodideReady) return pyodide;

  console.log('Loading Pyodide...');
  
  // Load Pyodide from CDN
  pyodide = await window.loadPyodide({
    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'
  });

  console.log('Loading packages...');
  await pyodide.loadPackage(['numpy', 'pandas', 'scipy']);

  // Load core detection code
  await pyodide.runPythonAsync(`
import numpy as np
import pandas as pd
import io
from scipy import stats

def compute_psi(theta_matrix):
    """Compute Performance-Structure Independence score."""
    T, K = theta_matrix.shape
    if T < 2:
        return 0.0
    
    # Calculate parameter changes over time
    changes = np.diff(theta_matrix, axis=0)
    psi = np.mean(np.abs(changes))
    return float(psi)

def compute_ccs(constraint_matrix):
    """Compute Constraint-Consistency Score."""
    T, p = constraint_matrix.shape
    if T < 2:
        return 1.0
    
    # Normalize constraints
    normalized = (constraint_matrix - constraint_matrix.mean(axis=0)) / (constraint_matrix.std(axis=0) + 1e-10)
    
    # Calculate consistency
    correlations = []
    for i in range(T-1):
        for j in range(i+1, T):
            corr = np.corrcoef(normalized[i], normalized[j])[0, 1]
            if not np.isnan(corr):
                correlations.append(corr)
    
    ccs = np.mean(correlations) if correlations else 1.0
    return float(ccs)

def compute_rho_pc(performance_matrix, constraint_matrix):
    """Compute Performance-Constraint Correlation."""
    # Average performance per time period
    perf_avg = np.mean(performance_matrix, axis=1)
    
    # Average constraints per time period
    const_avg = np.mean(constraint_matrix, axis=1)
    
    # Calculate correlation
    if len(perf_avg) < 2:
        return 0.0
    
    corr, _ = stats.pearsonr(perf_avg, const_avg)
    return float(corr) if not np.isnan(corr) else 0.0

def detect_bias(csv_string, psi_threshold=0.15, ccs_threshold=0.85, rho_pc_threshold=0.5):
    """Run complete bias detection."""
    # Parse CSV
    df = pd.read_csv(io.StringIO(csv_string))
    
    # Prepare matrices
    perf_matrix = df.pivot(
        index='time_period',
        columns='algorithm',
        values='performance'
    ).values
    
    const_matrix = df.groupby('time_period')[[
        'constraint_compute',
        'constraint_memory',
        'constraint_dataset_size'
    ]].first().values
    
    algorithms = df['algorithm'].unique().tolist()
    
    # Compute indicators
    psi = compute_psi(perf_matrix)
    ccs = compute_ccs(const_matrix)
    rho_pc = compute_rho_pc(perf_matrix, const_matrix)
    
    # Determine bias
    psi_detected = psi > psi_threshold
    ccs_detected = ccs < ccs_threshold
    rho_pc_detected = abs(rho_pc) > rho_pc_threshold
    
    indicators_triggered = sum([psi_detected, ccs_detected, rho_pc_detected])
    overall_bias = indicators_triggered >= 2
    confidence = indicators_triggered / 3.0
    
    return {
        'psi': psi,
        'ccs': ccs,
        'rho_pc': rho_pc,
        'overall_bias': overall_bias,
        'confidence': confidence,
        'details': {
            'algorithms_evaluated': algorithms,
            'time_periods': int(perf_matrix.shape[0]),
            'indicators_triggered': int(indicators_triggered)
        }
    }
  `);

  pyodideReady = true;
  console.log('Pyodide ready!');
  return pyodide;
}

/**
 * Run bias detection on CSV data
 * @param {string} csvString - CSV data as string
 * @returns {Promise<object>} Detection results
 */
export async function runBiasDetection(csvString) {
  if (!pyodideReady) {
    throw new Error('Pyodide not initialized');
  }

  try {
    // Set CSV data in Python scope
    pyodide.globals.set('csv_data', csvString);

    // Run detection
    const resultJSON = await pyodide.runPythonAsync(`
import json
result = detect_bias(csv_data)
json.dumps(result)
    `);

    const result = JSON.parse(resultJSON);
    console.log('Detection results:', result);
    return result;

  } catch (error) {
    console.error('Bias detection error:', error);
    throw new Error(`Detection failed: ${error.message}`);
  }
}

/**
 * Check if Pyodide is ready
 */
export function isPyodideReady() {
  return pyodideReady;
}
