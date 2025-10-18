import React from 'react';

export default function PrivacyPolicy() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 py-12 px-4">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl p-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🔒 Privacy Policy
          </h1>
          <p className="text-lg text-gray-600">
            Your privacy is our top priority. We believe in transparency.
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Last updated: October 18, 2024
          </p>
        </div>

        {/* Privacy-First Design */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="mr-3">🛡️</span>
            Privacy-First Design
          </h2>
          <div className="bg-green-50 border-l-4 border-green-500 p-6 rounded-r-lg">
            <p className="text-lg font-semibold text-green-900 mb-3">
              Your data NEVER leaves your device by default.
            </p>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✅</span>
                <span>All analysis runs in your browser (client-side processing)</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✅</span>
                <span>No data uploaded to our servers</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✅</span>
                <span>No cookies or tracking by default</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✅</span>
                <span>100% open source - verify yourself</span>
              </li>
            </ul>
          </div>
        </section>

        {/* What We DON'T Collect */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="mr-3">❌</span>
            What We DON'T Collect
          </h2>
          <div className="bg-gray-50 rounded-lg p-6">
            <ul className="space-y-3 text-gray-700">
              <li className="flex items-start">
                <span className="text-red-500 font-bold mr-2">❌</span>
                <span><strong>Your evaluation data</strong> - stays in your browser</span>
              </li>
              <li className="flex items-start">
                <span className="text-red-500 font-bold mr-2">❌</span>
                <span><strong>Your model information</strong> - not transmitted</span>
              </li>
              <li className="flex items-start">
                <span className="text-red-500 font-bold mr-2">❌</span>
                <span><strong>Your IP address</strong> - no server-side logs</span>
              </li>
              <li className="flex items-start">
                <span className="text-red-500 font-bold mr-2">❌</span>
                <span><strong>Personal information</strong> - not required</span>
              </li>
              <li className="flex items-start">
                <span className="text-red-500 font-bold mr-2">❌</span>
                <span><strong>Analytics/tracking cookies</strong> - disabled by default</span>
              </li>
            </ul>
          </div>
        </section>

        {/* Optional Data Sharing */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="mr-3">📊</span>
            Optional: Help Improve Sleuth (Opt-In Only)
          </h2>
          <div className="bg-blue-50 rounded-lg p-6">
            <p className="text-gray-700 mb-4">
              You can <strong>voluntarily</strong> choose to share anonymous statistics to help us improve bias detection accuracy. This is completely optional and can be disabled anytime.
            </p>
            
            <h3 className="font-semibold text-gray-900 mb-2">What you CAN optionally share:</h3>
            <ul className="space-y-2 text-gray-700 mb-4">
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">📈</span>
                <span><strong>Anonymous usage statistics</strong> - e.g., "PSI threshold triggered"</span>
              </li>
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">📊</span>
                <span><strong>Aggregated bias metrics</strong> - statistical summaries only</span>
              </li>
              <li className="flex items-start">
                <span className="text-blue-600 mr-2">🐛</span>
                <span><strong>Error reports</strong> - no personal data included</span>
              </li>
            </ul>

            <h3 className="font-semibold text-gray-900 mb-2">How we protect shared data:</h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <span className="text-green-600 mr-2">🔐</span>
                <span><strong>Differential Privacy</strong> - noise added to prevent re-identification (ε = 1.0)</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">🔢</span>
                <span><strong>Aggregation</strong> - only group statistics (k ≥ 10 users)</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">🔒</span>
                <span><strong>Encrypted transmission</strong> - HTTPS/TLS 1.3</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">🗑️</span>
                <span><strong>Right to deletion</strong> - delete your data anytime</span>
              </li>
            </ul>
          </div>
        </section>

        {/* Technical Details */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="mr-3">⚙️</span>
            Technical Implementation
          </h2>
          <div className="bg-gray-100 rounded-lg p-6 font-mono text-sm">
            <pre className="whitespace-pre-wrap text-gray-800">
{`// All computation happens client-side
import { BiasDetector } from './detector';

// Your data never leaves this function
function analyzeLocally(data) {
  const detector = new BiasDetector();
  const results = detector.detect(data); // Runs in browser
  return results; // Stays local
}

// Optional: Anonymous metrics (opt-in)
function shareAnonymousStats(results) {
  if (userConsent === true) {
    const anonymized = {
      psi_triggered: results.psi > threshold,
      bias_detected: results.has_bias,
      // NO raw data, NO identifiers
    };
    sendSecurely(anonymized); // With DP noise
  }
}`}
            </pre>
          </div>
        </section>

        {/* Data Retention */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="mr-3">⏱️</span>
            Data Retention
          </h2>
          <div className="space-y-3 text-gray-700">
            <p>
              <strong>Client-side data:</strong> Stored only in your browser's memory and cleared when you close the tab. Not persisted.
            </p>
            <p>
              <strong>Optional anonymous statistics:</strong> Retained for 12 months for research purposes, then permanently deleted.
            </p>
            <p>
              <strong>No backup copies:</strong> We don't keep backups of individual user data.
            </p>
          </div>
        </section>

        {/* User Rights */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="mr-3">⚖️</span>
            Your Rights (GDPR/CCPA Compliant)
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Right to Access</h3>
              <p className="text-sm text-gray-600">Request a copy of any data we have about you (likely none).</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Right to Deletion</h3>
              <p className="text-sm text-gray-600">Request deletion of your data anytime.</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Right to Opt-Out</h3>
              <p className="text-sm text-gray-600">Disable optional data sharing at any time.</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Right to Portability</h3>
              <p className="text-sm text-gray-600">Export your data in machine-readable format.</p>
            </div>
          </div>
        </section>

        {/* Future: Federated Learning */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="mr-3">🔮</span>
            Future: Federated Learning (Planned)
          </h2>
          <div className="bg-purple-50 border-l-4 border-purple-500 p-6 rounded-r-lg">
            <p className="text-gray-700 mb-3">
              We're building the world's most privacy-preserving AI bias detection dataset using <strong>Federated Learning</strong>.
            </p>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <span className="text-purple-600 mr-2">🤝</span>
                <span><strong>Collaborative learning</strong> - improve models together</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-600 mr-2">🔐</span>
                <span><strong>Your data stays local</strong> - only model updates shared</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-600 mr-2">🎓</span>
                <span><strong>Advanced privacy</strong> - Fed-CAD (correlation-aware differential privacy)</span>
              </li>
            </ul>
            <p className="text-sm text-gray-600 mt-4">
              <strong>Status:</strong> Research phase. Will require explicit opt-in before launch.
            </p>
          </div>
        </section>

        {/* Contact */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="mr-3">📧</span>
            Contact & Questions
          </h2>
          <div className="bg-gray-50 rounded-lg p-6">
            <p className="text-gray-700 mb-4">
              Have questions about privacy? We're happy to answer.
            </p>
            <ul className="space-y-2 text-gray-700">
              <li>
                <strong>Email:</strong>{' '}
                <a href="mailto:yujjam@uest.edu.gr" className="text-blue-600 hover:underline">
                  yujjam@uest.edu.gr
                </a>
              </li>
              <li>
                <strong>GitHub Issues:</strong>{' '}
                <a 
                  href="https://github.com/hongping-zh/circular-bias-detection/issues" 
                  className="text-blue-600 hover:underline"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Report privacy concerns
                </a>
              </li>
              <li>
                <strong>Documentation:</strong>{' '}
                <a 
                  href="https://github.com/hongping-zh/circular-bias-detection" 
                  className="text-blue-600 hover:underline"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Technical details
                </a>
              </li>
            </ul>
          </div>
        </section>

        {/* Open Source */}
        <section className="mb-10">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <span className="mr-3">💻</span>
            Open Source Transparency
          </h2>
          <div className="bg-gray-50 rounded-lg p-6">
            <p className="text-gray-700 mb-4">
              Our code is open source. You can verify every claim we make about privacy.
            </p>
            <a 
              href="https://github.com/hongping-zh/circular-bias-detection" 
              className="inline-flex items-center px-6 py-3 bg-gray-900 text-white font-semibold rounded-lg hover:bg-gray-800 transition"
              target="_blank"
              rel="noopener noreferrer"
            >
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              View Source Code
            </a>
          </div>
        </section>

        {/* Summary */}
        <div className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-lg p-8 text-center">
          <h2 className="text-2xl font-bold mb-4">Privacy in One Sentence</h2>
          <p className="text-xl">
            Your data stays in your browser. We see nothing unless you explicitly opt-in to share anonymous statistics.
          </p>
        </div>
      </div>
    </div>
  );
}
