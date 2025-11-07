import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchMetrics } from '../api/mock';
import { useUIStore } from '../store/ui';
import KpiCards from '../components/dashboard/KpiCards';
import TrendChart from '../components/charts/TrendChart';

const ControlsPanel: React.FC = () => {
  const { threshold, window, groupBy, setThreshold, setWindow, setGroupBy } = useUIStore();
  return (
    <div className="p-4 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm text-slate-600 dark:text-slate-300 mb-1">Bias Threshold</label>
          <input
            type="range"
            min={0}
            max={0.5}
            step={0.01}
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value))}
            className="w-full"
          />
          <div className="text-xs text-slate-500 mt-1">{threshold.toFixed(2)}</div>
        </div>
        <div>
          <label className="block text-sm text-slate-600 dark:text-slate-300 mb-1">Time Window</label>
          <select value={window} onChange={(e) => setWindow(e.target.value as any)} className="w-full px-3 py-2 rounded border bg-white dark:bg-slate-800">
            <option value="7d">7 days</option>
            <option value="14d">14 days</option>
            <option value="30d">30 days</option>
            <option value="90d">90 days</option>
          </select>
        </div>
        <div>
          <label className="block text-sm text-slate-600 dark:text-slate-300 mb-1">Group By</label>
          <select value={groupBy} onChange={(e) => setGroupBy(e.target.value as any)} className="w-full px-3 py-2 rounded border bg-white dark:bg-slate-800">
            <option value="user_group">User Group</option>
            <option value="item_category">Item Category</option>
          </select>
        </div>
      </div>
    </div>
  );
};

const Dashboard: React.FC = () => {
  const params = useUIStore((s) => ({ threshold: s.threshold, window: s.window, groupBy: s.groupBy }));

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ['metrics', params],
    queryFn: () => fetchMetrics(params),
    staleTime: 10_000,
  });

  return (
    <div className="space-y-6">
      <ControlsPanel />

      {isLoading && (
        <div className="text-center text-slate-500">Loading metrics...</div>
      )}
      {isError && (
        <div className="text-center text-red-500">Failed to load metrics. <button className="underline" onClick={() => refetch()}>Retry</button></div>
      )}

      {data && (
        <>
          <KpiCards kpis={data.kpis} />
          <div className="grid grid-cols-1 gap-6">
            <TrendChart data={data.timeseries} />
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
