import type { AnalysisResult } from '../types';

// ==============================================================================
// CRITICAL SECURITY NOTE FOR DEPLOYMENT
// ==============================================================================
// The original implementation called the Gemini API directly from the browser.
// This is **UNSAFE** for a live application because it exposes your API key to
// anyone who visits the site.
//
// To secure this, you MUST move the Gemini API call to a server-side environment,
// such as a Google Cloud Function, AWS Lambda, or a simple Node.js server.
//
// The new architecture should be:
// 1.  **Frontend (This App):** Collects the CSV content.
// 2.  **Frontend -> Backend:** Sends the CSV content in a POST request to your
//     secure backend endpoint (e.g., a Cloud Function URL).
// 3.  **Backend (Your Cloud Function):**
//     - Receives the CSV content.
//     - Securely stores and uses your `API_KEY` from an environment variable.
//     - Makes the call to the Gemini API.
//     - Returns the JSON analysis back to the frontend.
//
// The code below has been updated to reflect this new, secure approach.
// You will need to create the backend function yourself.
// ==============================================================================

const MOCK_ANALYSIS_RESULT: AnalysisResult = {
  summary: "This is a sample analysis. The backend service is currently unavailable. The data appears to be a customer dataset with potential indicators for churn prediction.",
  dataQualityInsights: [
    "Column 'last_seen_days_ago' has some missing values (approx. 5%) which should be imputed or handled.",
    "The 'signup_date' column is in a consistent format (YYYY-MM-DD).",
    "No major outliers detected in 'monthly_spend'."
  ],
  biasDetectionInsights: [
    "Potential data leakage detected: The feature 'churn_email_sent' is highly correlated with the likely target 'has_churned'. This feature likely occurs after the churn event and should be excluded from model training.",
    "The feature 'account_age_days' seems appropriate and does not show signs of circular bias."
  ],
  isMock: true,
};


/**
 * Sends CSV data to a secure backend endpoint for analysis by the Gemini API.
 * @param csvContent The raw string content of the uploaded CSV file.
 * @returns A promise that resolves to an AnalysisResult object.
 */
export async function analyzeCsvData(csvContent: string): Promise<AnalysisResult> {
    // PythonAnywhere backend URL
    const analysisEndpoint = 'https://hongpingzhang.pythonanywhere.com/api/analyze-csv'; 

    try {
        const response = await fetch(analysisEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain',
            },
            body: csvContent,
        });

        if (!response.ok) {
            const errorBody = await response.text();
            throw new Error(`Network response was not ok: ${response.status} ${response.statusText}. Body: ${errorBody}`);
        }

        const result: AnalysisResult = await response.json();
        return result;

    } catch (error) {
        console.error('Error fetching analysis from backend:', error);
        // Fallback to mock data if the backend call fails.
        // This provides a "Demo Mode" for users without a configured API key.
        console.log('Falling back to demo mode with mock analysis result.');
        return MOCK_ANALYSIS_RESULT;
    }
}


// ------------------------------------------------------------------------------
// REFERENCE: Original Gemini API call (to be used in your backend function)
// ------------------------------------------------------------------------------
/*
import { GoogleGenAI, Type } from "@google/genai";

// In your backend, initialize with the API key from an environment variable.
// const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

async function getAnalysisFromGemini(csvContent: string): Promise<AnalysisResult> {
    const proModel = 'gemini-2.5-pro';

    const prompt = `You are an expert data analyst specializing in data quality assessment and bias detection for machine learning.
    Analyze the provided CSV data. Your goal is to identify potential issues, anomalies, interesting patterns, and provide a concise summary.

    Here is a sample of the CSV data (up to the first 20 rows):
    ---
    ${csvContent.split('\n').slice(0, 20).join('\n')}
    ---

    Your analysis should cover:
    1.  **Data Quality:** Look for missing values, inconsistent formatting, or data entry errors.
    2.  **Anomalies & Outliers:** Identify rows or values that deviate significantly from the rest of the data.
    3.  **Potential Red Flags:** Look for patterns that might be suspicious, such as high numbers of duplicate entries or unusual value distributions.
    4.  **Key Patterns:** Summarize any interesting trends or correlations you observe.
    5.  **Circular Bias & Data Leakage:** Explicitly look for predictor variables that might be derived from a potential target variable, or any other signs that information from an outcome is leaking into the features. This is critical for preventing overly optimistic model performance. For example, a "days_until_churn" column in a dataset used to predict churn.

    Provide your output as a JSON object with the following structure. Do not include any markdown formatting like \`\`\`json.
    {
      "summary": "A brief, high-level summary of your findings in 2-3 sentences.",
      "dataQualityInsights": ["A list of bullet points highlighting important findings on data quality, anomalies, and patterns."],
      "biasDetectionInsights": ["A list of bullet points specifically identifying potential circular bias, data leakage, or other feature-target relationship issues."]
    }`;

    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
    const response = await ai.models.generateContent({
        model: proModel,
        contents: prompt,
        config: {
            responseMimeType: 'application/json',
            responseSchema: {
                type: Type.OBJECT,
                properties: {
                    summary: { type: Type.STRING },
                    dataQualityInsights: { 
                        type: Type.ARRAY,
                        items: { type: Type.STRING }
                    },
                    biasDetectionInsights: {
                        type: Type.ARRAY,
                        items: { type: Type.STRING }
                    }
                },
                required: ["summary", "dataQualityInsights", "biasDetectionInsights"]
            }
        }
    });

    const jsonString = response.text.trim();
    const result = JSON.parse(jsonString);
    return result;
}
*/