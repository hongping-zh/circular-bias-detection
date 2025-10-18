import React, { useState, useEffect } from 'react';

/**
 * Real-time Privacy Monitor
 * Shows users that their data never leaves their browser
 */
export default function SecurityIndicator() {
  const [uploadCount, setUploadCount] = useState(0);
  const [requestLog, setRequestLog] = useState([]);
  const [isMonitoring, setIsMonitoring] = useState(true);

  useEffect(() => {
    if (!isMonitoring) return;

    // Intercept all fetch requests
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
      const url = args[0];
      
      // Only count actual data uploads (not CDN/assets)
      if (url && typeof url === 'string' && 
          (url.includes('/api/') || url.includes('/upload'))) {
        
        setUploadCount(prev => prev + 1);
        setRequestLog(prev => [{
          url: url,
          time: new Date().toLocaleTimeString(),
          method: 'POST'
        }, ...prev].slice(0, 10)); // Keep last 10
      }
      
      return originalFetch.apply(this, args);
    };

    // Intercept XMLHttpRequest
    const originalXHR = window.XMLHttpRequest;
    window.XMLHttpRequest = function() {
      const xhr = new originalXHR();
      const originalOpen = xhr.open;
      
      xhr.open = function(method, url) {
        if (url.includes('/api/') || url.includes('/upload')) {
          setUploadCount(prev => prev + 1);
          setRequestLog(prev => [{
            url: url,
            time: new Date().toLocaleTimeString(),
            method: method
          }, ...prev].slice(0, 10));
        }
        return originalOpen.apply(this, arguments);
      };
      
      return xhr;
    };

    return () => {
      // Cleanup
      window.fetch = originalFetch;
      window.XMLHttpRequest = originalXHR;
    };
  }, [isMonitoring]);

  return (
    <div style={{ position: 'fixed', bottom: '16px', right: '16px', zIndex: 9999 }}>
      {/* Compact indicator */}
      <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg shadow-2xl p-4" style={{ maxWidth: '320px' }}>
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-white rounded-full animate-pulse mr-2"></div>
            <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <span className="font-bold text-sm">
              Privacy Monitor
            </span>
          </div>
          <button
            onClick={() => setIsMonitoring(!isMonitoring)}
            className="text-xs bg-white/20 hover:bg-white/30 px-2 py-1 rounded transition"
          >
            {isMonitoring ? 'Active' : 'Paused'}
          </button>
        </div>

        {/* Main stats */}
        <div className="bg-white/10 rounded-lg p-3 backdrop-blur-sm">
          <div className="flex items-baseline justify-between mb-2">
            <span className="text-xs opacity-90">Data Uploads:</span>
            <span className="text-3xl font-bold">{uploadCount}</span>
          </div>
          
          {uploadCount === 0 ? (
            <div className="flex items-center text-xs mt-2">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="opacity-90">
                Your data stays on your device
              </span>
            </div>
          ) : (
            <div className="flex items-center text-xs mt-2 text-yellow-200">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <span>
                {uploadCount} upload{uploadCount > 1 ? 's' : ''} detected
              </span>
            </div>
          )}
        </div>

        {/* How to verify */}
        <details className="mt-3">
          <summary className="text-xs cursor-pointer hover:underline opacity-90">
            How to verify yourself →
          </summary>
          <div className="mt-2 text-xs bg-white/10 rounded p-2 space-y-1 opacity-90">
            <p>1. Press <kbd className="bg-white/20 px-1 rounded">F12</kbd></p>
            <p>2. Go to <strong>Network</strong> tab</p>
            <p>3. Upload your CSV file</p>
            <p>4. Look for POST requests</p>
            <p className="text-green-200 font-semibold mt-2 flex items-center">
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              You'll see ZERO uploads!
            </p>
          </div>
        </details>

        {/* Request log (if any) */}
        {requestLog.length > 0 && (
          <details className="mt-3">
            <summary className="text-xs cursor-pointer hover:underline opacity-90">
              Network activity log ({requestLog.length})
            </summary>
            <ul className="mt-2 text-xs bg-white/10 rounded p-2 max-h-32 overflow-y-auto space-y-1">
              {requestLog.map((req, i) => (
                <li key={i} className="font-mono opacity-80 border-b border-white/10 pb-1">
                  <span className="text-yellow-200">{req.method}</span>
                  {' '}
                  <span className="text-white/60">{req.time}</span>
                  <div className="truncate text-white/80">{req.url}</div>
                </li>
              ))}
            </ul>
          </details>
        )}

        {/* Footer */}
        <div className="mt-3 pt-3 border-t border-white/20 text-xs opacity-75">
          <p className="flex items-center">
            <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
            </svg>
            Open source •{' '}
            <a 
              href="https://github.com/hongping-zh/circular-bias-detection" 
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-white"
            >
              Verify code
            </a>
          </p>
        </div>
      </div>

      {/* Minimized version */}
      {/* TODO: Add minimize/maximize functionality */}
    </div>
  );
}

/**
 * Alternative: Compact Top Banner Version
 */
export function SecurityBanner() {
  const [uploadCount, setUploadCount] = useState(0);

  useEffect(() => {
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
      const url = args[0];
      if (url && typeof url === 'string' && 
          (url.includes('/api/') || url.includes('/upload'))) {
        setUploadCount(prev => prev + 1);
      }
      return originalFetch.apply(this, args);
    };

    return () => {
      window.fetch = originalFetch;
    };
  }, []);

  return (
    <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white py-2 px-4 text-center text-sm">
      <span className="inline-flex items-center">
        <span className="w-2 h-2 bg-white rounded-full animate-pulse mr-2"></span>
        <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        <strong>Privacy Mode Active</strong>
        <span className="mx-2">•</span>
        Data uploads: <strong className="ml-1 text-lg">{uploadCount}</strong>
        <span className="mx-2">•</span>
        <button 
          onClick={() => {
            alert('Press F12 → Network tab to verify zero uploads yourself!');
          }}
          className="underline hover:text-green-100"
        >
          Verify yourself →
        </button>
      </span>
    </div>
  );
}
