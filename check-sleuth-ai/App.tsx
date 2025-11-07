import React, { useState, useCallback } from 'react';
import { Header } from './components/Header';
import { CsvUploader } from './components/CsvUploader';
import { DataTable } from './components/DataTable';
import { AnalysisResults } from './components/AnalysisResults';
import { analyzeCsvData } from './services/geminiService';
import { Footer } from './components/Footer';
import { GoogleAnalytics, trackCsvUpload, trackAnalysisComplete, trackError } from './src/components/GoogleAnalytics';
import type { AnalysisResult, CsvRow } from './types';

const parseCsv = (text: string): { headers: string[], rows: CsvRow[] } => {
    try {
        const lines = text.trim().replace(/\r\n/g, '\n').split('\n');
        if (lines.length < 1) return { headers: [], rows: [] };

        const headers = lines[0].split(',').map(h => h.trim());
        const rows = lines.slice(1).map(line => {
            // This is a naive parser and will not handle commas within quoted fields.
            const values = line.split(',').map(v => v.trim());
            const rowObject: CsvRow = {};
            headers.forEach((header, index) => {
                rowObject[header] = values[index] || '';
            });
            return rowObject;
        });
        return { headers, rows };
    } catch (e) {
        console.error("CSV Parsing error:", e);
        return { headers: [], rows: [] };
    }
};


const App: React.FC = () => {
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [csvHeaders, setCsvHeaders] = useState<string[]>([]);
  const [csvRows, setCsvRows] = useState<CsvRow[]>([]);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const resetState = () => {
    setCsvFile(null);
    setCsvHeaders([]);
    setCsvRows([]);
    setAnalysis(null);
    setIsProcessing(false);
    setError(null);
  };

  const handleCsvUpload = useCallback(async (file: File) => {
    resetState();
    setIsProcessing(true);
    setCsvFile(file);
    
    // Track CSV upload
    trackCsvUpload(file.size, file.name);

    const reader = new FileReader();
    reader.readAsText(file);
    
    reader.onload = async (e) => {
      try {
        const csvContent = e.target?.result as string;
        if (!csvContent) {
            setError('The CSV file is empty or could not be read.');
            setIsProcessing(false);
            return;
        }

        const { headers, rows } = parseCsv(csvContent);

        if (headers.length === 0 || rows.length === 0) {
            setError('Could not parse the CSV file. Please check its format.');
            setIsProcessing(false);
            return;
        }

        setCsvHeaders(headers);
        setCsvRows(rows);
        
        const startTime = Date.now();
        const analysisResult = await analyzeCsvData(csvContent);
        const duration = Date.now() - startTime;
        
        setAnalysis(analysisResult);
        
        // Track analysis completion
        trackAnalysisComplete(duration, analysisResult.isMock || false);
        
      } catch (e) {
        console.error(e);
        const errorMessage = e instanceof Error ? e.message : 'An unknown error occurred during analysis.';
        setError(`Analysis failed: ${errorMessage}`);
        
        // Track error
        trackError(errorMessage);
      } finally {
        setIsProcessing(false);
      }
    };

    reader.onerror = () => {
      setError('Failed to read the file.');
      setIsProcessing(false);
    };
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 font-sans flex flex-col">
      <GoogleAnalytics />
      <Header />
      <main className="container mx-auto px-4 py-8 flex-grow">
        {!csvFile ? (
          <CsvUploader onCsvUpload={handleCsvUpload} isProcessing={isProcessing} />
        ) : (
          <div className="flex flex-col gap-8">
            <div className="flex flex-wrap justify-between items-center gap-4">
                <h2 className="text-2xl font-bold text-slate-300 truncate">Analysis for: <span className="text-blue-400">{csvFile.name}</span></h2>
                <button
                    onClick={resetState}
                    className="bg-rose-600 hover:bg-rose-700 text-white font-bold py-2 px-4 rounded-md transition-colors duration-200 flex-shrink-0"
                >
                    Analyze Another CSV
                </button>
            </div>

            {error && (
                <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-lg" role="alert">
                    <strong className="font-bold">Error: </strong>
                    <span className="block sm:inline">{error}</span>
                </div>
            )}
            
            <AnalysisResults analysis={analysis} isLoading={isProcessing && !analysis} />
            <DataTable headers={csvHeaders} rows={csvRows} isLoading={isProcessing && csvRows.length === 0} />
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default App;