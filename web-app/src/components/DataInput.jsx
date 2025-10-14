import React, { useState } from 'react';
import './DataInput.css';

function DataInput({ onDataLoad }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      alert('Please upload a CSV file');
      return;
    }

    setSelectedFile(file.name);

    const reader = new FileReader();
    reader.onload = (e) => {
      const csvContent = e.target.result;
      onDataLoad(csvContent);
    };
    reader.readAsText(file);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file) {
      const fakeEvent = { target: { files: [file] } };
      handleFileUpload(fakeEvent);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const loadExampleData = () => {
    // Example CSV data
    const exampleCSV = `time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol
1,ResNet,0.72,300,8.0,50000,ImageNet-v1.0
1,VGG,0.68,450,12.0,50000,ImageNet-v1.0
1,DenseNet,0.75,280,9.0,50000,ImageNet-v1.0
1,EfficientNet,0.78,200,6.0,50000,ImageNet-v1.0
2,ResNet,0.73,305,8.2,51000,ImageNet-v1.0
2,VGG,0.69,455,12.1,51000,ImageNet-v1.0
2,DenseNet,0.76,285,9.1,51000,ImageNet-v1.0
2,EfficientNet,0.79,205,6.1,51000,ImageNet-v1.0
3,ResNet,0.74,310,8.4,52000,ImageNet-v1.1
3,VGG,0.70,460,12.2,52000,ImageNet-v1.1
3,DenseNet,0.77,290,9.2,52000,ImageNet-v1.1
3,EfficientNet,0.80,210,6.2,52000,ImageNet-v1.1
4,ResNet,0.75,315,8.6,53000,ImageNet-v1.1
4,VGG,0.71,465,12.3,53000,ImageNet-v1.1
4,DenseNet,0.78,295,9.3,53000,ImageNet-v1.1
4,EfficientNet,0.81,215,6.3,53000,ImageNet-v1.1
5,ResNet,0.76,320,8.8,54000,ImageNet-v1.1
5,VGG,0.72,470,12.4,54000,ImageNet-v1.1
5,DenseNet,0.79,300,9.4,54000,ImageNet-v1.1
5,EfficientNet,0.82,220,6.4,54000,ImageNet-v1.1`;
    
    setSelectedFile('example_data.csv (from Zenodo)');
    onDataLoad(exampleCSV);
  };

  const generateSyntheticData = () => {
    // Simple synthetic data generator
    const timePeriodsCount = 10;
    const algorithms = ['Algo_A', 'Algo_B', 'Algo_C', 'Algo_D'];
    let csv = 'time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol\n';
    
    for (let t = 1; t <= timePeriodsCount; t++) {
      algorithms.forEach((algo, idx) => {
        const performance = 0.6 + Math.random() * 0.3;
        const compute = 200 + Math.random() * 300;
        const memory = 5 + Math.random() * 10;
        const datasetSize = 40000 + Math.random() * 20000;
        csv += `${t},${algo},${performance.toFixed(4)},${compute.toFixed(1)},${memory.toFixed(1)},${Math.floor(datasetSize)},Protocol-v${t}\n`;
      });
    }
    
    setSelectedFile('synthetic_data.csv (generated)');
    onDataLoad(csv);
  };

  return (
    <div className="data-input-container">
      <div 
        className="upload-box"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <input 
          type="file" 
          id="file-upload" 
          accept=".csv"
          onChange={handleFileUpload}
          style={{ display: 'none' }}
        />
        <label htmlFor="file-upload" className="upload-label">
          📁 Upload Your Data
          <span className="upload-hint">
            Drag & drop CSV or click to browse
          </span>
        </label>
        {selectedFile && (
          <div className="selected-file">
            ✓ {selectedFile}
          </div>
        )}
      </div>

      <div className="data-options">
        <span className="or-divider">OR</span>
        
        <div className="option-buttons">
          <button 
            className="option-button"
            onClick={loadExampleData}
          >
            📊 Try Example from Zenodo
          </button>
          
          <button 
            className="option-button"
            onClick={generateSyntheticData}
          >
            🎲 Generate Synthetic Data
          </button>
        </div>
      </div>
    </div>
  );
}

export default DataInput;
