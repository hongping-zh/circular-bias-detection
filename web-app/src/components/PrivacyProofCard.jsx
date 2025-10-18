import React from 'react';

/**
 * Privacy Proof Card - Shows users how to verify privacy claims
 * Perfect for homepage hero section
 */
export default function PrivacyProofCard() {
  return (
    <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-500 rounded-2xl p-8 my-8 shadow-xl">
      {/* Header */}
      <div className="text-center mb-4">
        <div className="text-xl mb-2">🔐</div>
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          Your Data. Your Device. Period.
        </h2>
        <p className="text-lg text-gray-600">
          Don't just take our word for it — <strong className="text-green-700">verify it yourself</strong>
        </p>
      </div>

      {/* Verification Methods */}
      <div className="grid md:grid-cols-3 gap-6 mb-6">
        {/* Method 1: Browser DevTools */}
        <div className="bg-white rounded-lg p-5 shadow-md hover:shadow-lg transition">
          <div className="text-3xl mb-3">🔍</div>
          <h3 className="font-bold text-gray-900 mb-2">
            Method 1: DevTools
          </h3>
          <ol className="text-sm text-gray-700 space-y-1 list-decimal list-inside">
            <li>Press <kbd className="bg-gray-100 px-2 py-1 rounded text-xs">F12</kbd></li>
            <li>Go to <strong>Network</strong> tab</li>
            <li>Upload your CSV</li>
            <li>See <strong className="text-green-600">ZERO</strong> uploads ✅</li>
          </ol>
          <div className="mt-3 text-xs text-gray-500">
            ⏱️ Takes: 30 seconds
          </div>
        </div>

        {/* Method 2: Source Code */}
        <div className="bg-white rounded-lg p-5 shadow-md hover:shadow-lg transition">
          <div className="text-3xl mb-3">💻</div>
          <h3 className="font-bold text-gray-900 mb-2">
            Method 2: Source Code
          </h3>
          <div className="text-sm text-gray-700 space-y-2">
            <p>Audit the code yourself:</p>
            <pre className="bg-gray-100 p-2 rounded text-xs overflow-x-auto">
{`git clone github.com/
  hongping-zh/
  circular-bias-detection
grep -r "fetch" src/`}
            </pre>
            <p className="text-green-600 font-semibold">
              Result: No uploads! ✅
            </p>
          </div>
        </div>

        {/* Method 3: Offline Mode */}
        <div className="bg-white rounded-lg p-5 shadow-md hover:shadow-lg transition">
          <div className="text-3xl mb-3">✈️</div>
          <h3 className="font-bold text-gray-900 mb-2">
            Method 3: Offline Test
          </h3>
          <ol className="text-sm text-gray-700 space-y-1 list-decimal list-inside">
            <li>Download the app</li>
            <li>Disconnect internet</li>
            <li>Run analysis</li>
            <li>Still works! ✅</li>
          </ol>
          <div className="mt-3">
            <a 
              href="https://github.com/hongping-zh/circular-bias-detection/releases" 
              className="text-xs text-blue-600 hover:underline"
            >
              Download offline version →
            </a>
          </div>
        </div>
      </div>

      {/* Video Tutorial */}
      <div className="bg-white rounded-lg p-6 shadow-md">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 text-4xl">📺</div>
          <div className="flex-1">
            <h3 className="font-bold text-gray-900 mb-2">
              🎥 Watch 60-Second Proof Video
            </h3>
            <p className="text-sm text-gray-600 mb-3">
              See live demonstration of network traffic monitoring during analysis
            </p>
            <button 
              onClick={() => alert('Video coming soon! For now, try Method 1 above.')}
              className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-2 rounded-lg font-semibold hover:shadow-lg transition"
            >
              Watch Proof Video →
            </button>
          </div>
        </div>
      </div>

      {/* Trust Indicators */}
      <div className="mt-6 pt-6 border-t border-green-200">
        <div className="flex flex-wrap justify-center items-center gap-6 text-sm text-gray-600">
          <div className="flex items-center">
            <span className="text-xl mr-2">🔓</span>
            <span>100% Open Source</span>
          </div>
          <div className="flex items-center">
            <span className="text-xl mr-2">🇪🇺</span>
            <span>GDPR Compliant</span>
          </div>
          <div className="flex items-center">
            <span className="text-xl mr-2">🛡️</span>
            <span>No Tracking</span>
          </div>
          <div className="flex items-center">
            <span className="text-xl mr-2">🔒</span>
            <span>Client-Side Only</span>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600 italic">
          "We built this tool for researchers who care about data privacy.<br/>
          We don't ask you to trust us. We give you the tools to verify."
        </p>
      </div>
    </div>
  );
}

/**
 * Compact version for smaller spaces
 */
export function PrivacyProofBadge() {
  const [showDetails, setShowDetails] = React.useState(false);

  return (
    <div className="inline-block">
      <button
        onClick={() => setShowDetails(!showDetails)}
        className="bg-green-100 border border-green-500 text-green-800 px-4 py-2 rounded-full text-sm font-semibold hover:bg-green-200 transition flex items-center gap-2"
      >
        <span className="text-lg">🔒</span>
        <span>Privacy Verified</span>
        <svg 
          className={`w-4 h-4 transition-transform ${showDetails ? 'rotate-180' : ''}`}
          fill="currentColor" 
          viewBox="0 0 20 20"
        >
          <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
      </button>

      {showDetails && (
        <div className="mt-2 bg-white border border-green-500 rounded-lg p-4 shadow-lg text-sm">
          <p className="font-semibold text-gray-900 mb-2">
            Verify our privacy claims:
          </p>
          <ul className="space-y-1 text-gray-700">
            <li>✅ Press F12 → Network → Zero uploads</li>
            <li>✅ View source code on GitHub</li>
            <li>✅ Works 100% offline</li>
          </ul>
          <a 
            href="/privacy" 
            className="text-blue-600 hover:underline mt-2 inline-block"
          >
            Learn more →
          </a>
        </div>
      )}
    </div>
  );
}
