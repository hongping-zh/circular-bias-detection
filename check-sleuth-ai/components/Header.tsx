import React from 'react';
import { MagnifyingGlassIcon } from './icons/MagnifyingGlassIcon';

export const Header: React.FC = () => {
  return (
    <header className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-10">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center gap-3">
          <MagnifyingGlassIcon className="h-8 w-8 text-blue-400" />
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">
            Circular Bias <span className="text-blue-400">Detector</span>
          </h1>
        </div>
      </div>
    </header>
  );
};
