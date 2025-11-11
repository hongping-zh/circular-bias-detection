// Mirrors selected assets from the repository into website/public
// Requires Node 18+ (global fetch)
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname } from 'node:path';

const baseRaw = 'https://raw.githubusercontent.com/hongping-zh/circular-bias-detection/main';

const targets = [
  // Figures (PNG)
  {
    src: `${baseRaw}/mvp_case_study_figures/contamination_risk_map.png`,
    dest: 'public/img/flows/contamination_risk_map.png',
  },
  {
    src: `${baseRaw}/mvp_case_study_figures/leakage_type_distribution.png`,
    dest: 'public/img/flows/leakage_type_distribution.png',
  },
  {
    src: `${baseRaw}/mvp_case_study_figures/performance_reality_check.png`,
    dest: 'public/img/flows/performance_reality_check.png',
  },
  {
    src: `${baseRaw}/mvp_case_study_figures/sample_contamination_heatmap.png`,
    dest: 'public/img/flows/sample_contamination_heatmap.png',
  },
  // Data (CSV/JSON)
  {
    src: `${baseRaw}/mvp_case_study_figures/contamination_data.csv`,
    dest: 'public/data/contamination_data.csv',
  },
  {
    src: `${baseRaw}/data/demo_high_bias.csv`,
    dest: 'public/data/demo_high_bias.csv',
  },
  {
    src: `${baseRaw}/data/demo_low_bias.csv`,
    dest: 'public/data/demo_low_bias.csv',
  },
  {
    src: `${baseRaw}/data/llm_eval_sample.csv`,
    dest: 'public/data/llm_eval_sample.csv',
  },
  {
    src: `${baseRaw}/data/mvp_leaked_dataset.csv`,
    dest: 'public/data/mvp_leaked_dataset.csv',
  },
  {
    src: `${baseRaw}/data/sample_data.csv`,
    dest: 'public/data/sample_data.csv',
  },
  {
    src: `${baseRaw}/data/tiny_sample.csv`,
    dest: 'public/data/tiny_sample.csv',
  },
  {
    src: `${baseRaw}/data/schema.json`,
    dest: 'public/data/schema.json',
  },
];

async function ensureDir(path) {
  await mkdir(path, { recursive: true });
}

async function download(src) {
  const res = await fetch(src);
  if (!res.ok) throw new Error(`Failed to fetch ${src}: ${res.status} ${res.statusText}`);
  const buf = Buffer.from(await res.arrayBuffer());
  return buf;
}

async function run() {
  let ok = 0;
  let fail = 0;
  for (const t of targets) {
    try {
      const dir = dirname(t.dest);
      await ensureDir(dir);
      const data = await download(t.src);
      await writeFile(t.dest, data);
      console.log(`Mirrored: ${t.src} -> ${t.dest}`);
      ok++;
    } catch (e) {
      console.warn(`Warn: failed to mirror ${t.src}: ${e.message}`);
      fail++;
    }
  }
  console.log(`Mirror summary: ${ok} succeeded, ${fail} failed`);
}

run().catch((e) => {
  console.warn(`Mirror script encountered an error but will not fail build: ${e.message}`);
});
