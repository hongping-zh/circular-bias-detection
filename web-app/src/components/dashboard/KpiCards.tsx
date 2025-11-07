import React from 'react';
import type { Kpis } from '../../api/mock';

const StatCard: React.FC<{ title: string; value: string; baseline?: string; highlight?: boolean }> = ({ title, value, baseline, highlight }) => (
  <div className={`p-4 rounded-lg border shadow-sm ${highlight ? 'border-red-300 bg-red-50 dark:bg-red-900/20' : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800'}`}>
    <div className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">{title}</div>
    <div className="text-2xl font-bold text-slate-800 dark:text-slate-100 mt-1">{value}</div>
    {baseline && <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">Baseline: {baseline}</div>}
  </div>
);

const KpiCards: React.FC<{ kpis: Kpis }> = ({ kpis }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      <StatCard title="PSI" value={kpis.psi.toFixed(3)} baseline={kpis.baseline.psi.toFixed(3)} highlight={kpis.psi > kpis.baseline.psi} />
      <StatCard title="CCS" value={kpis.ccs.toFixed(3)} baseline={kpis.baseline.ccs.toFixed(3)} highlight={kpis.ccs < kpis.baseline.ccs} />
      <StatCard title="ρ_PC" value={kpis.rho_pc.toFixed(3)} baseline={kpis.baseline.rho_pc.toFixed(3)} highlight={Math.abs(kpis.rho_pc) > Math.abs(kpis.baseline.rho_pc)} />
      <StatCard title="Bias Flag" value={kpis.bias_flag ? 'Yes' : 'No'} highlight={kpis.bias_flag} />
    </div>
  );
};

export default KpiCards;
