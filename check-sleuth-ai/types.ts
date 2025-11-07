export type CsvRow = Record<string, string | number>;

export interface AnalysisResult {
  summary: string;
  dataQualityInsights: string[];
  biasDetectionInsights: string[];
  isMock?: boolean;
}

// Fix: Added missing CheckData type
export interface CheckData {
  payee: string;
  amountNumeric: string;
  amountText: string;
  date: string;
  memo: string;
  routingNumber: string;
  accountNumber: string;
  checkNumber: string;
  signatureDetected: boolean;
}
