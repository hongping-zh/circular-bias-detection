import React from 'react';
import './ValidationMessage.css';

function ValidationMessage({ type, title, message, details, onClose }) {
  const getIcon = () => {
    switch (type) {
      case 'success':
        return '✓';
      case 'error':
        return '✗';
      case 'warning':
        return '⚠️';
      case 'info':
        return 'ℹ️';
      default:
        return '○';
    }
  };

  const getClassName = () => {
    return `validation-message validation-${type}`;
  };

  return (
    <div className={getClassName()}>
      <div className="validation-header">
        <div className="validation-icon">{getIcon()}</div>
        <div className="validation-content">
          <h4>{title}</h4>
          <p>{message}</p>
          {details && details.length > 0 && (
            <div className="validation-details">
              <ul>
                {details.map((detail, index) => (
                  <li key={index}>{detail}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
        {onClose && (
          <button className="validation-close" onClick={onClose} aria-label="Close">
            ×
          </button>
        )}
      </div>
    </div>
  );
}

export default ValidationMessage;
