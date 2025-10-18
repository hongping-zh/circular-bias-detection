import React from 'react';
import './ValidationMessage.css';
import Icon from './Icon';

function ValidationMessage({ type, title, message, details, onClose }) {
  const getIcon = () => {
    switch (type) {
      case 'success':
        return <Icon name="check" size={20} color="#4caf50" />;
      case 'error':
        return <Icon name="x" size={20} color="#f44336" />;
      case 'warning':
        return <Icon name="warning" size={20} color="#ff9800" />;
      case 'info':
        return <Icon name="info" size={20} color="#2196f3" />;
      default:
        return <Icon name="info" size={20} color="#2196f3" />;
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
