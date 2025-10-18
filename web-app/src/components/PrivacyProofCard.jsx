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
        {/* SVG Lock Icon - 稳定跨浏览器 */}
        <svg 
          className="w-12 h-12 mx-auto mb-3 text-green-600" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={2} 
            d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" 
          />
        </svg>
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          Your Data. Your Device. Period.
        </h2>
        <p className="text-base text-gray-600">
          Don't just take our word for it — <strong className="text-green-700">verify it yourself</strong>
        </p>
      </div>

      {/* Verification Methods */}
      <div className="grid md:grid-cols-3 gap-6 mb-6">
        {/* Method 1: Browser DevTools */}
        <div className="bg-white rounded-lg p-5 shadow-md hover:shadow-lg transition">
          <svg className="w-10 h-10 mb-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <h3 className="font-bold text-gray-900 mb-2">
            Method 1: DevTools
          </h3>
          <ol className="text-sm text-gray-700 space-y-1 list-decimal list-inside">
            <li>Press <kbd className="bg-gray-100 px-2 py-1 rounded text-xs">F12</kbd></li>
            <li>Go to <strong>Network</strong> tab</li>
            <li>Upload your CSV</li>
            <li>See <strong className="text-green-600">ZERO</strong> uploads ✅</li>
          </ol>
          <div className="mt-3 text-xs text-gray-500 flex items-center">
            <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Takes: 30 seconds
          </div>
        </div>

        {/* Method 2: Source Code */}
        <div className="bg-white rounded-lg p-5 shadow-md hover:shadow-lg transition">
          <svg className="w-10 h-10 mb-3 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
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

        {/* Method 3: Offline Test */}
        <div className="bg-white rounded-lg p-5 shadow-md hover:shadow-lg transition">
          <svg className="w-10 h-10 mb-3 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
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
          <svg className="w-12 h-12 flex-shrink-0 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <div className="flex-1">
            <h3 className="font-bold text-gray-900 mb-2">
              Watch 60-Second Proof Video
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
            <svg className="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
            </svg>
            <span>100% Open Source</span>
          </div>
          <div className="flex items-center">
            <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            <span>GDPR Compliant</span>
          </div>
          <div className="flex items-center">
            <svg className="w-5 h-5 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.618 5.984A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016zM12 9v2m0 4h.01" />
            </svg>
            <span>No Tracking</span>
          </div>
          <div className="flex items-center">
            <svg className="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
            </svg>
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
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
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
