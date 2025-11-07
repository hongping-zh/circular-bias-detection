import { create } from 'zustand';

export type Params = {
  threshold: number;
  window: '7d' | '14d' | '30d' | '90d';
  groupBy: 'user_group' | 'item_category';
};

type UIState = Params & {
  setThreshold: (v: number) => void;
  setWindow: (w: Params['window']) => void;
  setGroupBy: (g: Params['groupBy']) => void;
};

export const useUIStore = create<UIState>((set) => ({
  threshold: 0.15,
  window: '30d',
  groupBy: 'user_group',
  setThreshold: (v) => set({ threshold: v }),
  setWindow: (w) => set({ window: w }),
  setGroupBy: (g) => set({ groupBy: g }),
}));
