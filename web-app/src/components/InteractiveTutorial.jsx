import React, { useState } from 'react';
import './InteractiveTutorial.css';

const tutorialSteps = [
  {
    id: 1,
    title: 'Welcome to Sleuth! 👋',
    content: 'Sleuth helps you detect circular reasoning bias in AI algorithm evaluations. Let\'s take a quick tour!',
    icon: '🔍',
    action: 'Start Tutorial'
  },
  {
    id: 2,
    title: 'What is Circular Bias? 🔄',
    content: 'Circular bias occurs when evaluation protocols are manipulated to favor specific algorithms. This happens when:\n\n• Parameters are tuned based on preliminary results\n• Constraints are adjusted mid-evaluation\n• Test sets are cherry-picked to improve scores',
    icon: '⚠️',
    action: 'Next'
  },
  {
    id: 3,
    title: 'Upload Your Data 📁',
    content: 'You can upload your own CSV file, try our example from Zenodo, or generate synthetic data.\n\nRequired columns:\n• time_period\n• algorithm\n• performance\n• constraint columns (e.g., constraint_compute)',
    icon: '📊',
    action: 'Next',
    highlight: 'upload-box'
  },
  {
    id: 4,
    title: 'Three Key Indicators 📈',
    content: 'Sleuth analyzes three indicators:\n\n1. PSI (Performance-Structure Independence)\n   → Measures parameter stability\n\n2. CCS (Constraint-Consistency Score)\n   → Checks constraint consistency\n\n3. ρ_PC (Performance-Constraint Correlation)\n   → Detects suspicious correlations',
    icon: '🎯',
    action: 'Next'
  },
  {
    id: 5,
    title: 'Bootstrap Analysis 📊',
    content: 'For statistical rigor, Sleuth performs:\n\n• 1000 bootstrap resamples\n• 95% confidence intervals\n• P-value significance testing\n\nThis ensures results are reliable and reproducible.',
    icon: '✨',
    action: 'Next'
  },
  {
    id: 6,
    title: 'Interactive Visualizations 📉',
    content: 'After analysis, you\'ll see:\n\n• PSI time series chart\n• ρ_PC scatter plot\n• Indicator comparison bars\n\nThese help you understand the data and spot patterns.',
    icon: '📊',
    action: 'Next'
  },
  {
    id: 7,
    title: 'LLM Example 🤖',
    content: 'Special case: LLM Evaluation Bias\n\nSleuth can detect if:\n• Prompt engineering was iteratively tuned\n• Temperature/top_p adjusted for better scores\n• Max tokens optimized per model\n\nLoad "LLM Eval Sample" to see an example!',
    icon: '🤖',
    action: 'Try It!',
    highlight: 'option-buttons'
  }
];

function InteractiveTutorial({ onClose, onLoadExample }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(true);

  const handleNext = () => {
    if (currentStep < tutorialSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleClose();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSkip = () => {
    handleClose();
  };

  const handleClose = () => {
    setIsVisible(false);
    setTimeout(() => {
      if (onClose) onClose();
    }, 300);
  };

  const handleTryIt = () => {
    if (currentStep === tutorialSteps.length - 1 && onLoadExample) {
      onLoadExample();
    }
    handleClose();
  };

  if (!isVisible) return null;

  const step = tutorialSteps[currentStep];

  return (
    <div className="tutorial-overlay">
      <div className="tutorial-modal">
        <button className="tutorial-close" onClick={handleSkip} aria-label="Close">
          ×
        </button>

        <div className="tutorial-header">
          <div className="tutorial-icon">{step.icon}</div>
          <h2>{step.title}</h2>
        </div>

        <div className="tutorial-content">
          <p>{step.content}</p>
        </div>

        <div className="tutorial-progress">
          {tutorialSteps.map((_, index) => (
            <div
              key={index}
              className={`progress-dot ${index === currentStep ? 'active' : ''} ${index < currentStep ? 'completed' : ''}`}
              onClick={() => setCurrentStep(index)}
            />
          ))}
        </div>

        <div className="tutorial-actions">
          {currentStep > 0 && (
            <button className="tutorial-button secondary" onClick={handlePrevious}>
              ← Previous
            </button>
          )}
          
          <div className="button-spacer"></div>

          {currentStep < tutorialSteps.length - 1 ? (
            <>
              <button className="tutorial-button secondary" onClick={handleSkip}>
                Skip Tutorial
              </button>
              <button className="tutorial-button primary" onClick={handleNext}>
                {step.action} →
              </button>
            </>
          ) : (
            <button className="tutorial-button primary" onClick={handleTryIt}>
              {step.action} 🚀
            </button>
          )}
        </div>

        <div className="tutorial-footer">
          Step {currentStep + 1} of {tutorialSteps.length}
        </div>
      </div>
    </div>
  );
}

export default InteractiveTutorial;
