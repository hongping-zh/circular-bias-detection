import React from 'react';
import './ProgressBar.css';
import Icon from './Icon';

function ProgressBar({ progress, currentStep, steps }) {
  return (
    <div className="progress-container">
      <div className="progress-header">
        <h3><Icon name="settings" size={20} /> Analyzing Data...</h3>
        <span className="progress-percentage">{Math.round(progress)}%</span>
      </div>
      
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${progress}%` }}
        >
          <div className="progress-shine"></div>
        </div>
      </div>

      <div className="progress-steps">
        {steps.map((step, index) => {
          const isActive = index === currentStep;
          const isComplete = index < currentStep;
          
          return (
            <div 
              key={index}
              className={`progress-step ${isActive ? 'active' : ''} ${isComplete ? 'complete' : ''}`}
            >
              <div className="step-icon">
                {isComplete ? <Icon name="check" size={16} color="#4caf50" /> : isActive ? <Icon name="settings" size={16} color="#2196f3" /> : <Icon name="circle" size={16} color="#ccc" />}
              </div>
              <div className="step-label">{step}</div>
            </div>
          );
        })}
      </div>

      {currentStep < steps.length && (
        <div className="progress-detail">
          <div className="spinner-small"></div>
          <span>{steps[currentStep]}</span>
        </div>
      )}
    </div>
  );
}

export default ProgressBar;
