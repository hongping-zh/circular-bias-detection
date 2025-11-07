import React from 'react';
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

  return (
    <div className="space-y-4">
      <div className="flex gap-3">
        <button onClick={exportCSV} className="px-4 py-2 rounded bg-indigo-600 text-white">Export CSV</button>
        <button onClick={exportPDF} className="px-4 py-2 rounded bg-slate-700 text-white">Export PDF</button>
      </div>
      <div id="pdf-area" className="p-4 rounded border bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700">
        <h2 className="text-lg font-semibold">Sleuth Bias Analysis Report (Preview)</h2>
        <p className="text-sm text-slate-500">This preview area will be captured into a PDF.</p>
      </div>
    </div>
  );
};

export default Reports;
