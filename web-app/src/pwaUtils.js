/**
 * PWA Utilities for Sleuth
 * 
 * Handles service worker registration, offline detection,
 * and PWA installation prompts.
 */

/**
 * Register Service Worker
 */
export function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('/service-worker.js')
        .then((registration) => {
          console.log('✅ Service Worker registered:', registration.scope);
          
          // Check for updates periodically
          setInterval(() => {
            registration.update();
          }, 60 * 60 * 1000); // Every hour
          
          // Listen for updates
          registration.addEventListener('updatefound', () => {
            const newWorker = registration.installing;
            
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                // New service worker available
                showUpdateNotification();
              }
            });
          });
        })
        .catch((error) => {
          console.error('❌ Service Worker registration failed:', error);
        });
    });
  }
}

/**
 * Unregister Service Worker (for debugging)
 */
export async function unregisterServiceWorker() {
  if ('serviceWorker' in navigator) {
    const registrations = await navigator.serviceWorker.getRegistrations();
    for (const registration of registrations) {
      await registration.unregister();
    }
    console.log('✅ Service Worker unregistered');
  }
}

/**
 * Show update notification when new version available
 */
function showUpdateNotification() {
  const updateBanner = document.createElement('div');
  updateBanner.style.cssText = `
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: #2563eb;
    color: white;
    padding: 16px 24px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    z-index: 10000;
    display: flex;
    align-items: center;
    gap: 16px;
  `;
  
  updateBanner.innerHTML = `
    <span>New version available!</span>
    <button id="pwa-update-btn" style="
      background: white;
      color: #2563eb;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: bold;
    ">Update Now</button>
  `;
  
  document.body.appendChild(updateBanner);
  
  document.getElementById('pwa-update-btn').addEventListener('click', () => {
    navigator.serviceWorker.controller.postMessage({ type: 'SKIP_WAITING' });
    window.location.reload();
  });
}

/**
 * Handle PWA Install Prompt
 */
let deferredPrompt = null;

export function setupInstallPrompt() {
  window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent automatic prompt
    e.preventDefault();
    deferredPrompt = e;
    
    // Show custom install button
    showInstallButton();
  });
  
  window.addEventListener('appinstalled', () => {
    console.log('✅ PWA installed successfully');
    deferredPrompt = null;
    hideInstallButton();
  });
}

/**
 * Show custom install button
 */
function showInstallButton() {
  const installBtn = document.getElementById('pwa-install-btn');
  if (installBtn) {
    installBtn.style.display = 'block';
  }
}

/**
 * Hide install button
 */
function hideInstallButton() {
  const installBtn = document.getElementById('pwa-install-btn');
  if (installBtn) {
    installBtn.style.display = 'none';
  }
}

/**
 * Trigger PWA install prompt
 */
export async function promptInstall() {
  if (!deferredPrompt) {
    console.warn('Install prompt not available');
    return;
  }
  
  // Show native install prompt
  deferredPrompt.prompt();
  
  // Wait for user response
  const { outcome } = await deferredPrompt.userChoice;
  console.log(`User ${outcome === 'accepted' ? 'accepted' : 'dismissed'} the install prompt`);
  
  deferredPrompt = null;
}

/**
 * Check if app is running as PWA
 */
export function isPWA() {
  return (
    window.matchMedia('(display-mode: standalone)').matches ||
    window.navigator.standalone === true
  );
}

/**
 * Detect online/offline status
 */
export function setupOfflineDetection(onOnline, onOffline) {
  window.addEventListener('online', () => {
    console.log('✅ Back online');
    if (onOnline) onOnline();
  });
  
  window.addEventListener('offline', () => {
    console.log('⚠️ Offline mode');
    if (onOffline) onOffline();
  });
  
  // Check current status
  if (!navigator.onLine && onOffline) {
    onOffline();
  }
}

/**
 * Save data to IndexedDB for offline access
 */
export async function saveOfflineData(key, data) {
  const db = await openDB();
  const transaction = db.transaction(['offline-data'], 'readwrite');
  const store = transaction.objectStore('offline-data');
  
  await store.put({ key, data, timestamp: Date.now() });
  console.log('✅ Data saved for offline access');
}

/**
 * Load data from IndexedDB
 */
export async function loadOfflineData(key) {
  const db = await openDB();
  const transaction = db.transaction(['offline-data'], 'readonly');
  const store = transaction.objectStore('offline-data');
  
  const result = await store.get(key);
  return result ? result.data : null;
}

/**
 * Open IndexedDB
 */
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('sleuth-offline', 1);
    
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      
      if (!db.objectStoreNames.contains('offline-data')) {
        db.createObjectStore('offline-data', { keyPath: 'key' });
      }
      
      if (!db.objectStoreNames.contains('scan-results')) {
        db.createObjectStore('scan-results', { keyPath: 'id', autoIncrement: true });
      }
    };
  });
}

/**
 * Share scan results (Web Share API)
 */
export async function shareResults(results) {
  if (!navigator.share) {
    console.warn('Web Share API not supported');
    return fallbackShare(results);
  }
  
  try {
    await navigator.share({
      title: 'Sleuth Bias Detection Results',
      text: `PSI: ${results.psi_score.toFixed(4)}, CCS: ${results.ccs_score.toFixed(4)}, ρ_PC: ${results.rho_pc_score.toFixed(4)}`,
      url: window.location.href
    });
    
    console.log('✅ Results shared successfully');
  } catch (error) {
    console.error('Share failed:', error);
    fallbackShare(results);
  }
}

/**
 * Fallback share (copy to clipboard)
 */
function fallbackShare(results) {
  const text = `Sleuth Bias Detection Results:\nPSI: ${results.psi_score.toFixed(4)}\nCCS: ${results.ccs_score.toFixed(4)}\nρ_PC: ${results.rho_pc_score.toFixed(4)}`;
  
  navigator.clipboard.writeText(text).then(() => {
    alert('Results copied to clipboard!');
  });
}

/**
 * Generate QR Code for result sharing
 */
export async function generateQRCode(data) {
  // Upload results to temporary storage
  const response = await fetch('/api/results/share', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  
  const { shareUrl } = await response.json();
  
  // Generate QR code
  const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(shareUrl)}`;
  
  return { shareUrl, qrCodeUrl };
}

/**
 * Upload results to Zenodo
 */
export async function uploadToZenodo(results, apiToken) {
  const zenodoUrl = 'https://zenodo.org/api/deposit/depositions';
  
  try {
    // Create deposition
    const createResponse = await fetch(zenodoUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    });
    
    const deposition = await createResponse.json();
    const depositionId = deposition.id;
    
    // Upload file
    const fileBlob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
    const formData = new FormData();
    formData.append('file', fileBlob, 'sleuth_results.json');
    
    await fetch(`${zenodoUrl}/${depositionId}/files`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiToken}`
      },
      body: formData
    });
    
    // Publish
    const publishResponse = await fetch(`${zenodoUrl}/${depositionId}/actions/publish`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiToken}`
      }
    });
    
    const published = await publishResponse.json();
    
    return {
      success: true,
      doi: published.doi,
      url: published.links.record_html
    };
    
  } catch (error) {
    console.error('Zenodo upload failed:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Check PWA capabilities
 */
export function checkPWACapabilities() {
  return {
    serviceWorker: 'serviceWorker' in navigator,
    installPrompt: 'BeforeInstallPromptEvent' in window,
    pushNotifications: 'PushManager' in window,
    backgroundSync: 'sync' in ServiceWorkerRegistration.prototype,
    webShare: 'share' in navigator,
    clipboard: 'clipboard' in navigator,
    indexedDB: 'indexedDB' in window
  };
}
