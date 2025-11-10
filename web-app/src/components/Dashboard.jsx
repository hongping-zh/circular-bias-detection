import React, { useRef, useState } from 'react';
import './Dashboard.css';
import VisualizationCharts from './VisualizationCharts';
import { saveAs } from 'file-saver';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

function MetricCard({ title, value, threshold, status, description, ciLower, ciUpper, pValue, showBootstrap }) {
  const getStatusColor = () => {
    switch (status) {
      case 'ok': return '#4caf50';
      case 'warning': return '#ff9800';
      case 'danger': return '#f44336';
      default: return '#9e9e9e';
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case 'ok': return '✓';
      case 'warning': return '⚠️';
      case 'danger': return '✗';
      default: return '○';
    }
  };

  return (
    <div className="metric-card" style={{ borderTopColor: getStatusColor() }}>
      <div className="metric-header">
        <h3>{title}</h3>
        <span className="status-icon">{getStatusIcon()}</span>
      </div>
      <div className="metric-value">{value}</div>
      {showBootstrap && ciLower !== undefined && ciUpper !== undefined && (
        <div className="metric-ci">
          95% CI: [{ciLower} - {ciUpper}]
        </div>
      )}
      {showBootstrap && pValue !== undefined && (
        <div className="metric-pvalue" style={{ 
          color: pValue < 0.05 ? '#f44336' : '#666',
          fontWeight: pValue < 0.05 ? 'bold' : 'normal'
        }}>
          p-value: {pValue} {pValue < 0.05 ? '(significant)' : ''}
        </div>
      )}
      <div className="metric-threshold">Threshold: {threshold}</div>
      <div className="metric-description">{description}</div>
    </div>
  );
}

function Dashboard({ results, onReset }) {
  const reportRef = useRef(null);
  const [isExporting, setIsExporting] = useState(false);
  const getPSIStatus = (score) => {
    if (score < 0.10) return 'ok';
    if (score < 0.15) return 'warning';
    return 'danger';
  };

  const getCCSStatus = (score) => {
    if (score >= 0.9) return 'ok';
    if (score >= 0.85) return 'warning';
    return 'danger';
  };

  const getRhoPCStatus = (score) => {
    const abs = Math.abs(score);
    if (abs < 0.3) return 'ok';
    if (abs < 0.5) return 'warning';
    return 'danger';
  };

  const overallBias = results.overall_bias || false;
  const confidence = results.confidence || 0;

  const exportPDF = async () => {
    if (!reportRef.current || isExporting) return;
    setIsExporting(true);
    try {
      const canvas = await html2canvas(reportRef.current, {
        scale: 2,
        backgroundColor: '#ffffff'
      });
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`sleuth-bias-report-${new Date().toISOString().split('T')[0]}.pdf`);
    } catch (err) {
      console.error('PDF export failed:', err);
      alert('Failed to export PDF. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const exportCSV = () => {
    const rows = [
      ['Metric', 'Value', 'Threshold', 'Status'],
      ['PSI Score', results.psi?.toFixed(4) || 'N/A', '0.15', results.psi ? getPSIStatus(results.psi) : 'N/A'],
      ['CCS Score', results.ccs?.toFixed(4) || 'N/A', '0.85', results.ccs ? getCCSStatus(results.ccs) : 'N/A'],
      ['ρ_PC Score', results.rho_pc?.toFixed(4) || 'N/A', '±0.5', results.rho_pc !== undefined ? getRhoPCStatus(results.rho_pc) : 'N/A'],
      ['Overall Bias Detected', overallBias ? 'YES' : 'NO', '', ''],
      ['Confidence', `${(confidence * 100).toFixed(1)}%`, '', ''],
      ['Algorithms Evaluated', results.details?.algorithms_evaluated?.join(', ') || 'N/A', '', ''],
      ['Time Periods', results.details?.time_periods || 'N/A', '', ''],
      ['Indicators Triggered', `${results.details?.indicators_triggered || 0} / 3`, '', '']
    ];
    const csv = rows.map(r => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, `sleuth-bias-data-${new Date().toISOString().split('T')[0]}.csv`);
  };

  return (
    <div className="dashboard" ref={reportRef}>
      <div className="dashboard-header">
        <h2>📊 Bias Detection Results</h2>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button className="reset-button" onClick={onReset}>
            ← New Scan
          </button>
          <button 
            className="reset-button" 
            onClick={exportPDF}
            disabled={isExporting}
            style={{ background: isExporting ? '#ccc' : '#28a745' }}
          >
            {isExporting ? '⏳ Exporting...' : '📄 PDF'}
          </button>
          <button 
            className="reset-button" 
            onClick={exportCSV}
            style={{ background: '#17a2b8' }}
          >
            📊 CSV
          </button>
        </div>
      </div>

      <div className={`overall-status ${overallBias ? 'detected' : 'clean'}`}>
        <div className="status-icon-large">
          {overallBias ? '⚠️' : '✓'}
        </div>
        <div className="status-text">
          <h3>{overallBias ? 'BIAS DETECTED' : 'NO BIAS DETECTED'}</h3>
          <p>Confidence: {(confidence * 100).toFixed(1)}%</p>
        </div>
      </div>

      {results.bootstrap_enabled && (
        <div className="bootstrap-badge">
          ✨ Enhanced with Bootstrap Statistical Analysis (n=1000)
        </div>
      )}

      <div className="metrics-grid">
        <MetricCard
          title="PSI Score"
          value={results.psi?.toFixed(4) || 'N/A'}
          threshold="0.15"
          status={results.psi ? getPSIStatus(results.psi) : 'default'}
          description="Parameter Stability Index"
          ciLower={results.psi_ci_lower?.toFixed(4)}
          ciUpper={results.psi_ci_upper?.toFixed(4)}
          pValue={results.psi_p_value?.toFixed(3)}
          showBootstrap={results.bootstrap_enabled}
        />
        
        <MetricCard
          title="CCS Score"
          value={results.ccs?.toFixed(4) || 'N/A'}
          threshold="0.85"
          status={results.ccs ? getCCSStatus(results.ccs) : 'default'}
          description="Constraint Consistency Score"
          ciLower={results.ccs_ci_lower?.toFixed(4)}
          ciUpper={results.ccs_ci_upper?.toFixed(4)}
          pValue={results.ccs_p_value?.toFixed(3)}
          showBootstrap={results.bootstrap_enabled}
        />
        
        <MetricCard
          title="ρ_PC Score"
          value={results.rho_pc ? (results.rho_pc > 0 ? '+' : '') + results.rho_pc.toFixed(4) : 'N/A'}
          threshold="±0.5"
          status={results.rho_pc !== undefined ? getRhoPCStatus(results.rho_pc) : 'default'}
          description="Performance-Constraint Correlation"
          ciLower={results.rho_pc_ci_lower ? (results.rho_pc_ci_lower > 0 ? '+' : '') + results.rho_pc_ci_lower.toFixed(4) : undefined}
          ciUpper={results.rho_pc_ci_upper ? (results.rho_pc_ci_upper > 0 ? '+' : '') + results.rho_pc_ci_upper.toFixed(4) : undefined}
          pValue={results.rho_pc_p_value?.toFixed(3)}
          showBootstrap={results.bootstrap_enabled}
        />
      </div>

      <div className="interpretation-section">
        <h3>💡 Interpretation</h3>
        <div className="interpretation-box">
          {results.interpretation || getInterpretation(results)}
        </div>
      </div>

      {results.details && results.details.dataStats && (
        <VisualizationCharts results={results} dataStats={results.details.dataStats} />
      )}

      {results.details && (
        <div className="details-section">
          <h3>📋 Details</h3>
          <ul>
            {results.details.algorithms_evaluated && (
              <li><strong>Algorithms:</strong> {results.details.algorithms_evaluated.join(', ')}</li>
            )}
            {results.details.time_periods && (
              <li><strong>Time Periods:</strong> {results.details.time_periods}</li>
            )}
            {results.details.indicators_triggered !== undefined && (
              <li><strong>Indicators Triggered:</strong> {results.details.indicators_triggered} / 3</li>
            )}
          </ul>
        </div>
      )}

      <div className="action-buttons" style={{ display: 'flex', gap: '1rem', marginTop: '2rem', flexWrap: 'wrap' }}>
        <button 
          className="download-button" 
          onClick={exportPDF}
          disabled={isExporting}
        >
          {isExporting ? '⏳ Exporting...' : '📄 Export PDF Report'}
        </button>
        <button 
          className="download-button" 
          onClick={exportCSV}
        >
          📊 Export CSV Data
        </button>
        <button className="download-button" onClick={() => downloadResults(results)}>
          📥 Download JSON
        </button>
        <button className="cite-button" onClick={copyCitation}>
          📋 Copy Citation
        </button>
      </div>
    </div>
  );
}

function getInterpretation(results) {
  if (!results.overall_bias) {
    return "No circular bias detected. The evaluation methodology appears sound with stable parameters, consistent constraints, and independent performance metrics.";
  }

  const issues = [];
  if (results.psi > 0.15) issues.push("parameter instability (PSI)");
  if (results.ccs < 0.85) issues.push("constraint inconsistency (CCS)");
  if (Math.abs(results.rho_pc) > 0.5) issues.push("suspicious performance-constraint correlation (ρ_PC)");

  return `Circular bias detected via ${issues.join(', ')}. This suggests the evaluation methodology may have been manipulated or shows signs of circular reasoning. Review the evaluation process and constraints.`;
}

function downloadResults(results) {
  const dataStr = JSON.stringify(results, null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `bias-detection-results-${new Date().toISOString().split('T')[0]}.json`;
  link.click();
  URL.revokeObjectURL(url);
}

function copyCitation() {
  const citation = `Zhang, H. (2024). Algorithm Benchmark Suite v2.0: Synthetic Dataset for Circular Bias Detection [Data set]. Zenodo. https://doi.org/10.5281/zenodo.17201032`;
  navigator.clipboard.writeText(citation).then(() => {
    alert('Citation copied to clipboard!');
  });
}

export default Dashboard;
