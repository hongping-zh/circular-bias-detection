import React, { useState, useCallback } from 'react';
import { UploadIcon } from './icons/UploadIcon';

interface CsvUploaderProps {
  onCsvUpload: (file: File) => void;
  isProcessing: boolean;
}

export const CsvUploader: React.FC<CsvUploaderProps> = ({ onCsvUpload, isProcessing }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragEnter = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onCsvUpload(e.dataTransfer.files[0]);
    }
  }, [onCsvUpload]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onCsvUpload(e.target.files[0]);
    }
  };

  return (
    <div className="max-w-3xl mx-auto text-center">
      <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 shadow-2xl">
        <h2 className="text-3xl font-bold text-slate-100 mb-2">Detect Circular Bias with AI</h2>
        <p className="text-slate-400 mb-6 max-w-2xl mx-auto">
          Circular bias, or data leakage, can invalidate machine learning models by creating overly optimistic results. This tool uses AI to analyze your dataset for subtle signs of leakage, alongside general data quality issues. Protect your models by uploading a CSV to begin.
        </p>
        <div
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          className={`relative border-2 border-dashed rounded-lg p-12 transition-colors duration-200 ${isDragging ? 'border-blue-500 bg-slate-700/50' : 'border-slate-600 hover:border-slate-500'}`}
        >
          <input
            type="file"
            id="file-upload"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={handleFileChange}
            accept=".csv"
            disabled={isProcessing}
          />
          <div className="flex flex-col items-center justify-center space-y-4 text-slate-400">
            <UploadIcon className="h-12 w-12" />
            <p className="font-semibold">
              <span className="text-blue-400">Click to upload</span> or drag and drop
            </p>
            <p className="text-sm">CSV files only</p>
          </div>
        </div>
        {isProcessing && (
          <div className="mt-6 flex items-center justify-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-blue-400 animate-pulse"></div>
            <div className="w-4 h-4 rounded-full bg-blue-400 animate-pulse [animation-delay:0.2s]"></div>
            <div className="w-4 h-4 rounded-full bg-blue-400 animate-pulse [animation-delay:0.4s]"></div>
            <p className="text-slate-300">AI is analyzing your data...</p>
          </div>
        )}
      </div>
    </div>
  );
};