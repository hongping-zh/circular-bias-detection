import React, { useState } from 'react';

const Tutorial: React.FC = () => {
  const [loaded, setLoaded] = useState(false);

  const loadSample = async () => {
    setLoaded(true);
  };

  return (
    <div className="space-y-4">
      <div className="p-4 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800">
        <h2 className="text-lg font-semibold mb-2">Getting Started</h2>
        <ol className="list-decimal pl-5 space-y-1 text-sm text-slate-600 dark:text-slate-300">
          <li>Open the Dashboard to view KPI cards and trends.</li>
          <li>Adjust bias threshold, time window, and grouping in the controls panel.</li>
          <li>Export results from the Reports page (CSV/PDF).</li>
        </ol>
      </div>
      <div className="p-4 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800">
        <h3 className="font-semibold mb-2">One-click Demo</h3>
        <button onClick={loadSample} className="px-4 py-2 rounded bg-indigo-600 text-white">Load Sample Data</button>
        {loaded && <p className="mt-2 text-sm text-green-600">Sample data loaded. Go to Dashboard to explore.</p>}
      </div>
    </div>
  );
};

export default Tutorial;
