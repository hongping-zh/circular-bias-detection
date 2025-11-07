import { delay } from '../utils/delay';

export type Kpis = {
  psi: number;
  ccs: number;
  rho_pc: number;
  bias_flag: boolean;
  baseline: { psi: number; ccs: number; rho_pc: number };
};

export type TimePoint = { t: string; psi: number; ccs: number; rho_pc: number };
export type Contribution = { group: string; psi_delta: number; ccs_delta: number; rho_pc_delta: number; weight: number };
export type Diversity = { t: string; diversity_score: number };

export type MetricsResponse = {
  kpis: Kpis;
  timeseries: TimePoint[];
  contribution: Contribution[];
  diversity: Diversity[];
};

export type MetricsParams = {
  window: string; // e.g., '30d'
  groupBy: 'user_group' | 'item_category';
  threshold: number; // bias threshold for highlighting
};

const dates = Array.from({ length: 30 }).map((_, i) => {
  const d = new Date();
  d.setDate(d.getDate() - (29 - i));
  return d.toISOString().slice(0, 10);
});

export async function fetchMetrics(params: MetricsParams): Promise<MetricsResponse> {
  await delay(300);
  const timeseries = dates.map((t, idx) => ({
    t,
    psi: 0.1 + 0.02 * Math.sin(idx / 5),
    ccs: 0.9 - 0.03 * Math.sin(idx / 6),
    rho_pc: 0.45 + 0.05 * Math.cos(idx / 7),
  }));
  const last = timeseries[timeseries.length - 1];
  const baseline = { psi: 0.12, ccs: 0.88, rho_pc: 0.42 };
  const kpis: Kpis = {
    psi: last.psi,
    ccs: last.ccs,
    rho_pc: last.rho_pc,
    bias_flag: last.psi > params.threshold || last.ccs < 0.85 || Math.abs(last.rho_pc) > 0.6,
    baseline,
  };
  const contribution: Contribution[] = Array.from({ length: 6 }).map((_, i) => ({
    group: params.groupBy === 'user_group' ? `Group ${i + 1}` : `Category ${i + 1}`,
    psi_delta: (Math.random() - 0.5) * 0.05,
    ccs_delta: (Math.random() - 0.5) * 0.05,
    rho_pc_delta: (Math.random() - 0.5) * 0.1,
    weight: Math.round(5 + Math.random() * 20),
  }));
  const diversity: Diversity[] = dates.map((t, idx) => ({ t, diversity_score: 0.6 + 0.1 * Math.sin(idx / 4) }));
  return { kpis, timeseries, contribution, diversity };
}
