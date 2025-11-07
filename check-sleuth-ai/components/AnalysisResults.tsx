import React from 'react';
import type { AnalysisResult } from '../types';
import { SparklesIcon } from './icons/SparklesIcon';

interface AnalysisResultsProps {
  analysis: AnalysisResult | null;
  isLoading: boolean;
}

const InsightSection: React.FC<{title: string; insights: string[]}> = ({ title, insights }) => {
    if (!insights || insights.length === 0) return null;
    return (
        <div className="mt-6 border-t border-slate-700 pt-4">
            <h3 className="font-semibold text-slate-300 text-lg mb-3">{title}</h3>
            <ul className="space-y-2 list-disc list-inside text-slate-400">
                {insights.map((insight, index) => (
                    <li key={index}>
                        {insight}
                    </li>
                ))}
            </ul>
        </div>
    );
};

const DemoModeBanner = () => (
    <div className="mb-6 p-4 bg-gradient-to-r from-blue-900/40 to-indigo-900/40 border border-blue-700/50 rounded-lg">
      <div className="flex items-start">
        <div className="flex-shrink-0 mr-3 mt-1">
          <svg className="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-blue-300 mb-1">
            🎯 Demo Mode - Sample Analysis
          </h3>
          <p className="text-sm text-slate-300 mb-3">
            You're viewing sample results. Want <strong className="text-blue-300">real AI analysis</strong> of YOUR actual data?
          </p>
          <div className="bg-slate-800/50 rounded-md p-3 mb-3 border border-slate-700">
            <p className="text-xs text-slate-400 mb-2">Real AI can:</p>
            <ul className="text-xs text-slate-300 space-y-1">
              <li>✓ Detect specific issues in your columns</li>
              <li>✓ Find hidden correlations and patterns</li>
              <li>✓ Suggest exact fixes for your data</li>
            </ul>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <a 
              href="https://makersuite.google.com/app/apikey" 
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-xs font-medium rounded-md hover:bg-blue-700 transition-colors"
            >
              Get Free API Key (5 min)
            </a>
            <a 
              href="https://github.com/hongping-zh/circular-bias-detection"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-blue-400 hover:text-blue-300 underline"
            >
              Setup Guide
            </a>
          </div>
          <p className="text-xs text-slate-500 mt-2 italic">
            💬 "Setup took 3 minutes, AI found 2 issues I completely missed!" - ML Engineer
          </p>
        </div>
      </div>
    </div>
);

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ analysis, isLoading }) => {
  if (isLoading) {
    return (
        <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-lg animate-pulse">
            <div className="h-8 w-1/2 bg-slate-700 rounded mb-6"></div>
            <div className="space-y-3">
                <div className="h-4 bg-slate-700 rounded w-full mb-4"></div>
                <div className="h-6 w-1/3 bg-slate-700 rounded mb-4"></div>
                <div className="h-4 bg-slate-700 rounded w-full"></div>
                <div className="h-4 bg-slate-700 rounded w-full"></div>
                <div className="h-4 bg-slate-700 rounded w-3/4"></div>
            </div>
        </div>
    );
  }

  if (!analysis) return null;

  return (
    <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-lg">
      {analysis.isMock && <DemoModeBanner />}
      
      <div className="flex items-center gap-2 mb-4">
        <SparklesIcon className="h-6 w-6 text-blue-400" />
        <h2 className="text-2xl font-bold text-slate-300">AI Analysis</h2>
      </div>
      
      <div>
        <h3 className="font-semibold text-slate-300 text-lg mb-2">Summary</h3>
        <p className="text-slate-400 leading-relaxed">{analysis.summary}</p>
      </div>
      
      <InsightSection title="Potential Bias & Data Leakage" insights={analysis.biasDetectionInsights} />
      <InsightSection title="Key Insights & Data Quality" insights={analysis.dataQualityInsights} />

      {/* Call to Action for Demo Mode */}
      {analysis.isMock && (
        <div className="mt-8 p-6 bg-gradient-to-br from-indigo-900/30 via-blue-900/30 to-cyan-900/30 rounded-xl border-2 border-indigo-700/50">
          <div className="text-center">
            <h3 className="text-xl font-bold text-slate-200 mb-2">
              Ready for Real AI Insights?
            </h3>
            <p className="text-sm text-slate-400 mb-4">
              This sample shows what's possible. Get personalized analysis for your actual data.
            </p>
            
            <div className="bg-slate-800/60 rounded-lg p-4 mb-4 inline-block border border-slate-700">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
                <div>
                  <p className="text-xs font-semibold text-slate-500 mb-1">DEMO MODE</p>
                  <p className="text-sm text-slate-400">✓ Sample results</p>
                  <p className="text-sm text-slate-400">✓ General insights</p>
                  <p className="text-sm text-slate-600">✗ Specific to your data</p>
                </div>
                <div>
                  <p className="text-xs font-semibold text-indigo-400 mb-1">WITH API KEY</p>
                  <p className="text-sm text-indigo-300">✓ Real AI analysis</p>
                  <p className="text-sm text-indigo-300">✓ Precise issue detection</p>
                  <p className="text-sm text-indigo-300">✓ Custom recommendations</p>
                </div>
              </div>
            </div>
            
            <div className="flex flex-wrap items-center justify-center gap-3">
              <a 
                href="https://makersuite.google.com/app/apikey" 
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors shadow-md"
              >
                Get Free API Key →
              </a>
              <a 
                href="https://github.com/hongping-zh/circular-bias-detection"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-6 py-3 border-2 border-indigo-600 text-indigo-400 font-medium rounded-lg hover:bg-indigo-900/30 transition-colors"
              >
                Setup Guide
              </a>
            </div>
            
            <p className="text-xs text-slate-500 mt-4">
              Free tier includes 60 analyses per day • Setup takes ~5 minutes
            </p>
          </div>
        </div>
      )}

    </div>
  );
};