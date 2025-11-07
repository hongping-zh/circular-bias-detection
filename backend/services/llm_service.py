"""
LLM Service for multiple AI providers
Supports DeepSeek, Gemini, and Demo mode
"""

import os
import requests
import json
from typing import Dict, Optional

class LLMService:
    """
    Unified LLM service supporting multiple providers
    """
    
    def __init__(self):
        self.deepseek_key = os.environ.get('DEEPSEEK_API_KEY')
        self.gemini_key = os.environ.get('GEMINI_API_KEY')
        
    def analyze_csv(self, csv_content: str, user_api_key: Optional[str] = None) -> Dict:
        """
        Analyze CSV data using available LLM
        
        Priority:
        1. User's Gemini API Key (if provided)
        2. DeepSeek API (default, free tier)
        3. Demo mode (fallback)
        """
        
        # Try user's Gemini key first
        if user_api_key:
            try:
                return self._analyze_with_gemini(csv_content, user_api_key)
            except Exception as e:
                print(f"[LLM] User Gemini API failed: {e}")
                # Fall through to DeepSeek
        
        # Try DeepSeek (default)
        if self.deepseek_key:
            try:
                return self._analyze_with_deepseek(csv_content)
            except Exception as e:
                print(f"[LLM] DeepSeek API failed: {e}")
                # Fall through to demo
        
        # Fallback to demo mode
        print("[LLM] Using demo mode")
        return self._get_demo_data()
    
    def _analyze_with_deepseek(self, csv_content: str) -> Dict:
        """
        Analyze using DeepSeek API
        """
        url = "https://api.deepseek.com/v1/chat/completions"
        
        # Limit CSV content to avoid token limits
        csv_preview = '\n'.join(csv_content.split('\n')[:50])
        
        prompt = f"""You are an expert data analyst specializing in machine learning data quality and bias detection.

Analyze the following CSV data and identify:
1. Data quality issues (missing values, inconsistencies, errors)
2. Potential circular bias and data leakage
3. Feature-target relationships that could indicate leakage

CSV Data (first 50 rows):
---
{csv_preview}
---

Provide your analysis as a JSON object with this exact structure:
{{
  "summary": "Brief 2-3 sentence summary of key findings",
  "dataQualityInsights": [
    "List of data quality observations",
    "Each as a separate string"
  ],
  "biasDetectionInsights": [
    "List of bias and leakage findings",
    "Each as a separate string"
  ]
}}

IMPORTANT: Return ONLY the JSON object, no additional text or markdown formatting."""

        headers = {
            "Authorization": f"Bearer {self.deepseek_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a data analysis expert. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        print("[LLM] Calling DeepSeek API...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Parse JSON response
        analysis = json.loads(content)
        
        # Add metadata
        analysis['provider'] = 'deepseek'
        analysis['isMock'] = False
        
        print(f"[LLM] DeepSeek analysis complete (tokens: {result.get('usage', {}).get('total_tokens', 'N/A')})")
        
        return analysis
    
    def _analyze_with_gemini(self, csv_content: str, api_key: str) -> Dict:
        """
        Analyze using user's Gemini API key
        """
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        csv_preview = '\n'.join(csv_content.split('\n')[:50])
        
        prompt = f"""You are an expert data analyst specializing in machine learning data quality and bias detection.

Analyze the following CSV data and identify:
1. Data quality issues
2. Potential circular bias and data leakage
3. Feature-target relationships

CSV Data:
---
{csv_preview}
---

Return a JSON object with: summary, dataQualityInsights (array), biasDetectionInsights (array)."""

        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'response_mime_type': 'application/json'
            }
        )
        
        analysis = json.loads(response.text)
        analysis['provider'] = 'gemini'
        analysis['isMock'] = False
        
        print("[LLM] Gemini analysis complete")
        return analysis
    
    def _get_demo_data(self) -> Dict:
        """
        Return demo analysis data
        """
        return {
            "summary": "Demo Mode: This is sample analysis. The data appears to be a customer dataset with potential indicators for churn prediction. To get real AI analysis, configure an API key.",
            "dataQualityInsights": [
                "Demo Mode Active: Real analysis requires API key configuration",
                "Column 'last_seen_days_ago' may have missing values (requires real analysis to confirm)",
                "Date columns should be validated for consistency",
                "Numeric columns should be checked for outliers"
            ],
            "biasDetectionInsights": [
                "Demo Mode: Real bias detection requires AI analysis",
                "Potential data leakage: Features that occur after the target event should be excluded",
                "Temporal features should be carefully validated",
                "Recommend real analysis to identify specific leakage issues"
            ],
            "provider": "demo",
            "isMock": True
        }
