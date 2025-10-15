/**
 * Data Validator
 * 
 * Validates CSV data and provides detailed error messages
 */

/**
 * Required columns for bias detection
 */
const REQUIRED_COLUMNS = [
  'time_period',
  'algorithm',
  'performance'
];

/**
 * Optional constraint columns
 */
const CONSTRAINT_COLUMNS = [
  'constraint_compute',
  'constraint_memory',
  'constraint_dataset_size',
  'max_tokens',
  'temperature',
  'top_p'
];

/**
 * Validate CSV data structure and content
 * @param {string} csvText - Raw CSV text
 * @returns {Object} - { valid: boolean, errors: [], warnings: [], data: [] }
 */
export function validateCSV(csvText) {
  const result = {
    valid: false,
    errors: [],
    warnings: [],
    data: null,
    stats: null
  };

  try {
    // Check if CSV is empty
    if (!csvText || csvText.trim().length === 0) {
      result.errors.push('CSV file is empty');
      return result;
    }

    // Parse CSV
    const lines = csvText.trim().split('\n');
    if (lines.length < 2) {
      result.errors.push('CSV must contain at least a header row and one data row');
      return result;
    }

    // Parse header
    const header = lines[0].split(',').map(col => col.trim());
    
    // Check required columns
    const missingColumns = REQUIRED_COLUMNS.filter(col => !header.includes(col));
    if (missingColumns.length > 0) {
      result.errors.push(
        `Missing required columns: ${missingColumns.join(', ')}\n` +
        `Required columns are: ${REQUIRED_COLUMNS.join(', ')}`
      );
      return result;
    }

    // Parse data rows
    const data = [];
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (line.length === 0) continue;

      const values = line.split(',').map(v => v.trim());
      if (values.length !== header.length) {
        result.errors.push(`Row ${i + 1}: Column count mismatch (expected ${header.length}, got ${values.length})`);
        continue;
      }

      const row = {};
      header.forEach((col, idx) => {
        row[col] = values[idx];
      });
      data.push(row);
    }

    if (data.length === 0) {
      result.errors.push('No valid data rows found');
      return result;
    }

    // Validate data content
    const contentValidation = validateDataContent(data, header);
    result.errors.push(...contentValidation.errors);
    result.warnings.push(...contentValidation.warnings);

    // If there are errors, return
    if (result.errors.length > 0) {
      return result;
    }

    // Calculate statistics
    result.stats = calculateStats(data);
    result.data = data;
    result.valid = true;

    return result;

  } catch (error) {
    result.errors.push(`Failed to parse CSV: ${error.message}`);
    return result;
  }
}

/**
 * Validate data content (values, ranges, consistency)
 */
function validateDataContent(data, header) {
  const errors = [];
  const warnings = [];

  // Check for required fields
  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const rowNum = i + 1;

    // Validate time_period
    const timePeriod = parseInt(row.time_period);
    if (isNaN(timePeriod) || timePeriod < 1) {
      errors.push(`Row ${rowNum}: 'time_period' must be a positive integer (got: "${row.time_period}")`);
    }

    // Validate algorithm
    if (!row.algorithm || row.algorithm.length === 0) {
      errors.push(`Row ${rowNum}: 'algorithm' cannot be empty`);
    }

    // Validate performance
    const performance = parseFloat(row.performance);
    if (isNaN(performance)) {
      errors.push(`Row ${rowNum}: 'performance' must be a number (got: "${row.performance}")`);
    } else if (performance < 0 || performance > 1) {
      warnings.push(`Row ${rowNum}: 'performance' should be between 0 and 1 (got: ${performance})`);
    }

    // Validate constraint columns if present
    CONSTRAINT_COLUMNS.forEach(col => {
      if (header.includes(col) && row[col] && row[col].length > 0) {
        const value = parseFloat(row[col]);
        if (isNaN(value)) {
          errors.push(`Row ${rowNum}: '${col}' must be a number (got: "${row[col]}")`);
        }
      }
    });
  }

  // Check for minimum data requirements
  const uniqueAlgorithms = new Set(data.map(row => row.algorithm));
  const uniquePeriods = new Set(data.map(row => row.time_period));

  if (uniqueAlgorithms.size < 2) {
    errors.push(`At least 2 different algorithms required (found: ${uniqueAlgorithms.size})`);
  }

  if (uniquePeriods.size < 3) {
    warnings.push(
      `Minimum 3 time periods recommended for reliable detection (found: ${uniquePeriods.size}). ` +
      `Results may be less accurate.`
    );
  }

  // Check for at least one constraint column
  const hasConstraints = CONSTRAINT_COLUMNS.some(col => header.includes(col));
  if (!hasConstraints) {
    warnings.push(
      `No constraint columns found. Include at least one constraint column for better analysis:\n` +
      `${CONSTRAINT_COLUMNS.slice(0, 3).join(', ')}, etc.`
    );
  }

  // Check for missing values
  let missingCount = 0;
  data.forEach((row, i) => {
    header.forEach(col => {
      if (!row[col] || row[col].length === 0) {
        missingCount++;
      }
    });
  });

  if (missingCount > 0) {
    warnings.push(`Found ${missingCount} missing values in the dataset`);
  }

  return { errors, warnings };
}

/**
 * Calculate dataset statistics
 */
function calculateStats(data) {
  const algorithms = [...new Set(data.map(row => row.algorithm))];
  const periods = [...new Set(data.map(row => parseInt(row.time_period)))].sort((a, b) => a - b);
  
  const performances = data
    .map(row => parseFloat(row.performance))
    .filter(p => !isNaN(p));

  const stats = {
    totalRows: data.length,
    algorithms: algorithms,
    algorithmCount: algorithms.length,
    timePeriods: periods,
    periodCount: periods.length,
    performance: {
      min: Math.min(...performances),
      max: Math.max(...performances),
      mean: performances.reduce((a, b) => a + b, 0) / performances.length
    }
  };

  return stats;
}

/**
 * Format validation result for display
 */
export function formatValidationMessage(result) {
  if (result.valid) {
    return {
      type: 'success',
      title: '✓ Data Validation Passed',
      message: `Successfully loaded ${result.stats.totalRows} rows with ${result.stats.algorithmCount} algorithms across ${result.stats.periodCount} time periods.`,
      details: result.warnings.length > 0 ? result.warnings : null
    };
  } else {
    return {
      type: 'error',
      title: '✗ Data Validation Failed',
      message: result.errors[0] || 'Invalid CSV format',
      details: result.errors.length > 1 ? result.errors.slice(1) : null
    };
  }
}

/**
 * Get example CSV content for user reference
 */
export function getExampleCSV() {
  return `time_period,algorithm,performance,constraint_compute,constraint_memory,constraint_dataset_size,evaluation_protocol
1,ResNet,0.92,100,8.0,50000,v1.0
1,VGG,0.89,120,10.0,50000,v1.0
1,DenseNet,0.91,110,9.0,50000,v1.0
2,ResNet,0.93,105,8.2,51000,v1.0
2,VGG,0.90,125,10.2,51000,v1.0
2,DenseNet,0.92,115,9.2,51000,v1.0
3,ResNet,0.94,110,8.5,52000,v1.1
3,VGG,0.91,130,10.5,52000,v1.1
3,DenseNet,0.93,120,9.5,52000,v1.1`;
}
