import React from 'react';
import type { CsvRow } from '../types';

interface DataTableProps {
  headers: string[];
  rows: CsvRow[];
  isLoading: boolean;
}

const ShimmerTable: React.FC = () => (
    <div className="animate-pulse">
        <div className="h-12 bg-slate-700/50 rounded-t-lg"></div>
        <div className="space-y-2 mt-2 p-4">
            {[...Array(5)].map((_, i) => (
                <div key={i} className="h-8 bg-slate-700 rounded"></div>
            ))}
        </div>
    </div>
);

export const DataTable: React.FC<DataTableProps> = ({ headers, rows, isLoading }) => {
    if (isLoading) {
        return (
             <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-lg">
                <h2 className="text-2xl font-bold text-slate-300 mb-4 h-8 w-1/2 bg-slate-700 rounded animate-pulse"></h2>
                <ShimmerTable />
            </div>
        )
    }

    if (headers.length === 0) return null;

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 shadow-lg overflow-hidden">
        <h2 className="text-2xl font-bold text-slate-300 p-6">CSV Data Preview</h2>
        <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-700">
                <thead className="bg-slate-700/50">
                <tr>
                    {headers.map((header) => (
                    <th key={header} scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">
                        {header}
                    </th>
                    ))}
                </tr>
                </thead>
                <tbody className="bg-slate-800 divide-y divide-slate-700">
                {rows.slice(0, 20).map((row, rowIndex) => (
                    <tr key={rowIndex} className="hover:bg-slate-700/50 transition-colors duration-150">
                    {headers.map((header) => (
                        <td key={`${rowIndex}-${header}`} className="px-6 py-4 whitespace-nowrap text-sm text-slate-400">
                        {String(row[header] ?? '')}
                        </td>
                    ))}
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
        {rows.length > 20 && (
            <div className="p-4 bg-slate-900/50 text-center text-sm text-slate-400 border-t border-slate-700">
                Showing first 20 of {rows.length} rows.
            </div>
        )}
    </div>
  );
};
