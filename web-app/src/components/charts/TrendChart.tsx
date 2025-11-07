import React from 'react';
import Plot from 'react-plotly.js';
import type { TimePoint } from '../../api/mock';

const TrendChart: React.FC<{ data: TimePoint[] }> = ({ data }) => {
  const t = data.map(d => d.t);
  const psi = data.map(d => d.psi);
  const ccs = data.map(d => d.ccs);
  const rho = data.map(d => d.rho_pc);

  return (
    <div className="rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-2">
      <Plot
        data={[
          { x: t, y: psi, type: 'scatter', mode: 'lines', name: 'PSI', line: { color: '#ef4444' } },
          { x: t, y: ccs, type: 'scatter', mode: 'lines', name: 'CCS', line: { color: '#10b981' } },
          { x: t, y: rho, type: 'scatter', mode: 'lines', name: 'ρ_PC', line: { color: '#3b82f6' } },
        ]}
        layout={{
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          margin: { t: 32, r: 16, b: 40, l: 48 },
          legend: { orientation: 'h' },
          xaxis: { title: 'Date' },
          yaxis: { title: 'Value' },
          autosize: true,
        }}
        useResizeHandler
        style={{ width: '100%', height: '360px' }}
        config={{ displayModeBar: false, responsive: true }}
      />
    </div>
  );
};

export default TrendChart;
