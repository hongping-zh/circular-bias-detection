import React from 'react';
import './ScanButton.css';

function ScanButton({ onClick, disabled, loading }) {
  return (
    <div className="scan-button-container">
      <button 
        className={`scan-button ${loading ? 'loading' : ''}`}
        onClick={onClick}
        disabled={disabled}
      >
        {loading ? (
          <>
            <span className="spinner-small"></span>
            Scanning...
          </>
        ) : (
          <>
            🔍 Scan for Bias
          </>
        )}
      </button>
      
      {disabled && !loading && (
        <p className="hint">Please load data first</p>
      )}
    </div>
  );
}

export default ScanButton;
