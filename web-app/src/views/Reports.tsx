import React, { useMemo } from 'react';
import { saveAs } from 'file-saver';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

const Reports: React.FC = () => {
  const exportCSV = () => {
    const rows = [
      ['date', 'psi', 'ccs', 'rho_pc'],
      ['2025-11-01', '0.12', '0.88', '0.44'],
      ['2025-11-02', '0.13', '0.89', '0.45'],
    ];
    const csv = rows.map(r => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, 'sleuth_report.csv');
  };

  const exportPDF = async () => {
    const el = document.getElementById('pdf-area');
    if (!el) return;
    const canvas = await html2canvas(el);
    const img = canvas.toDataURL('image/png');
    const pdf = new jsPDF({ orientation: 'p', unit: 'px', format: 'a4' });
    const pageWidth = pdf.internal.pageSize.getWidth();
    const ratio = pageWidth / canvas.width;
    pdf.addImage(img, 'PNG', 0, 20, pageWidth, canvas.height * ratio);
    pdf.save('sleuth_report.pdf');
  };

  const meta = useMemo(() => {
    try {
      const raw = localStorage.getItem('sleuth_data_meta');
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex gap-3">
        <button onClick={exportCSV} className="px-4 py-2 rounded bg-indigo-600 text-white">Export CSV</button>
        <button onClick={exportPDF} className="px-4 py-2 rounded bg-slate-700 text-white">Export PDF</button>
      </div>
      <div id="pdf-area" className="p-4 rounded border bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700">
        <h2 className="text-lg font-semibold">Sleuth Bias Analysis Report (Preview)</h2>
        <p className="text-sm text-slate-500">This preview area will be captured into a PDF.</p>

        <div className="mt-4 p-3 rounded-md bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-700">
          <h3 className="text-base font-semibold mb-2">Data Source & Limitations / 数据来源与限制</h3>
          <ul className="list-disc pl-5 text-sm text-slate-600 dark:text-slate-300 space-y-1">
            <li>
              <strong>Source 来源:</strong>
              {meta?.dataset_source ? ` ${meta.dataset_source}` : ' Unknown'}
              {meta?.domain ? ` (${meta.domain})` : ''}
            </li>
            <li>
              <strong>Protocol 协议:</strong>
              {meta?.evaluation_protocol ? ` ${meta.evaluation_protocol}` : ' Unknown'}
            </li>
            <li>
              <strong>Rows 行数:</strong>
              {meta?.total_rows ? ` ${meta.total_rows}` : ' Unknown'}
            </li>
            <li>
              <strong>Notice 提示:</strong> If the dataset is synthetic/simulation, detected bias signals may be amplified and are for demonstration only.
              若为合成/模拟数据，检测信号可能被放大，仅用于演示。
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Reports;
