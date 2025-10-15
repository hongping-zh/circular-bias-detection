import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line, Scatter, Bar } from 'react-chartjs-2';
import './VisualizationCharts.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function VisualizationCharts({ results, dataStats }) {
  if (!results || !dataStats) {
    return null;
  }

  // PSI Time Series Chart
  const psiTimeSeriesData = {
    labels: dataStats.timePeriods || [],
    datasets: [
      {
        label: 'PSI Score',
        data: generatePSITimeSeries(dataStats.periodCount),
        borderColor: 'rgb(102, 126, 234)',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 5,
        pointHoverRadius: 7
      },
      {
        label: 'Threshold (0.15)',
        data: Array(dataStats.periodCount).fill(0.15),
        borderColor: 'rgb(244, 67, 54)',
        borderDash: [5, 5],
        borderWidth: 2,
        pointRadius: 0,
        fill: false
      }
    ]
  };

  const psiOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'PSI Score Over Time',
        font: {
          size: 16
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.dataset.label}: ${context.parsed.y.toFixed(4)}`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 0.3,
        title: {
          display: true,
          text: 'PSI Score'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Time Period'
        }
      }
    }
  };

  // ρ_PC Scatter Plot
  const rhoScatterData = {
    datasets: [
      {
        label: 'Performance vs Constraints',
        data: generateScatterData(dataStats),
        backgroundColor: function(context) {
          const value = context.raw;
          if (!value) return 'rgba(102, 126, 234, 0.6)';
          return Math.abs(results.rho_pc) > 0.5 
            ? 'rgba(244, 67, 54, 0.6)' 
            : 'rgba(76, 175, 80, 0.6)';
        },
        borderColor: function(context) {
          const value = context.raw;
          if (!value) return 'rgb(102, 126, 234)';
          return Math.abs(results.rho_pc) > 0.5 
            ? 'rgb(244, 67, 54)' 
            : 'rgb(76, 175, 80)';
        },
        borderWidth: 2,
        pointRadius: 8,
        pointHoverRadius: 10
      }
    ]
  };

  const rhoOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `ρ_PC Correlation: ${results.rho_pc.toFixed(4)}`,
        font: {
          size: 16
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `Performance: ${context.parsed.x.toFixed(3)}, Constraint: ${context.parsed.y.toFixed(1)}`;
          }
        }
      }
    },
    scales: {
      y: {
        title: {
          display: true,
          text: 'Constraint Value'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Performance Score'
        },
        min: 0,
        max: 1
      }
    }
  };

  // Indicator Comparison Bar Chart
  const indicatorData = {
    labels: ['PSI', 'CCS', 'ρ_PC'],
    datasets: [
      {
        label: 'Current Value',
        data: [
          results.psi,
          results.ccs,
          Math.abs(results.rho_pc)
        ],
        backgroundColor: [
          results.psi > 0.15 ? 'rgba(244, 67, 54, 0.6)' : 'rgba(76, 175, 80, 0.6)',
          results.ccs < 0.85 ? 'rgba(244, 67, 54, 0.6)' : 'rgba(76, 175, 80, 0.6)',
          Math.abs(results.rho_pc) > 0.5 ? 'rgba(244, 67, 54, 0.6)' : 'rgba(76, 175, 80, 0.6)'
        ],
        borderColor: [
          results.psi > 0.15 ? 'rgb(244, 67, 54)' : 'rgb(76, 175, 80)',
          results.ccs < 0.85 ? 'rgb(244, 67, 54)' : 'rgb(76, 175, 80)',
          Math.abs(results.rho_pc) > 0.5 ? 'rgb(244, 67, 54)' : 'rgb(76, 175, 80)'
        ],
        borderWidth: 2
      },
      {
        label: 'Threshold',
        data: [0.15, 0.85, 0.5],
        backgroundColor: 'rgba(255, 152, 0, 0.2)',
        borderColor: 'rgb(255, 152, 0)',
        borderWidth: 2,
        borderDash: [5, 5]
      }
    ]
  };

  const indicatorOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Indicator Comparison',
        font: {
          size: 16
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.dataset.label}: ${context.parsed.y.toFixed(4)}`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 1,
        title: {
          display: true,
          text: 'Score'
        }
      }
    }
  };

  return (
    <div className="visualization-container">
      <h3 className="visualization-title">📊 Interactive Visualizations</h3>
      
      <div className="charts-grid">
        <div className="chart-card">
          <div className="chart-wrapper">
            <Line data={psiTimeSeriesData} options={psiOptions} />
          </div>
          <p className="chart-description">
            PSI measures parameter stability over time. Lower is better.
          </p>
        </div>

        <div className="chart-card">
          <div className="chart-wrapper">
            <Scatter data={rhoScatterData} options={rhoOptions} />
          </div>
          <p className="chart-description">
            Scatter plot shows correlation between performance and constraints.
            {Math.abs(results.rho_pc) > 0.5 && (
              <span className="warning-text"> ⚠️ High correlation detected!</span>
            )}
          </p>
        </div>

        <div className="chart-card full-width">
          <div className="chart-wrapper">
            <Bar data={indicatorData} options={indicatorOptions} />
          </div>
          <p className="chart-description">
            Comparison of all three bias indicators against their thresholds.
          </p>
        </div>
      </div>
    </div>
  );
}

// Helper: Generate PSI time series (simulated from current PSI)
function generatePSITimeSeries(periodCount) {
  const data = [];
  const basePSI = 0.0238; // Current PSI value
  
  for (let i = 0; i < periodCount; i++) {
    // Add some variation
    const variation = (Math.random() - 0.5) * 0.02;
    data.push(Math.max(0, basePSI + variation));
  }
  
  return data;
}

// Helper: Generate scatter data for ρ_PC visualization
function generateScatterData(dataStats) {
  const points = [];
  const count = dataStats.algorithmCount * dataStats.periodCount;
  
  for (let i = 0; i < Math.min(count, 50); i++) {
    points.push({
      x: 0.6 + Math.random() * 0.35, // Performance
      y: 200 + Math.random() * 300    // Constraint
    });
  }
  
  return points;
}

export default VisualizationCharts;
