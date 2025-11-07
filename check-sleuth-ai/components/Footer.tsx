import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 border-t border-slate-800 mt-12">
      <div className="container mx-auto px-4 py-6 text-center text-slate-500 text-sm">
        <p>
          &copy; {new Date().getFullYear()} CSV Sleuth AI. All rights reserved.
        </p>
        <p className="mt-1">
          Inspired by the{' '}
          <a
            href="https://github.com/hongping-zh/circular-bias-detection"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 hover:text-blue-300 transition-colors"
          >
            Circular Bias Detection project
          </a>
          .
        </p>
      </div>
    </footer>
  );
};
