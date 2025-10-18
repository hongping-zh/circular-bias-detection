/**
 * Sleuth PWA Service Worker
 * 
 * Provides offline support, caching, and performance optimization.
 * Version: 1.2.0
 */

const CACHE_NAME = 'sleuth-v1.2.0';
const DATA_CACHE_NAME = 'sleuth-data-v1.2.0';

// Assets to cache on install
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icon-192x192.png',
  '/icon-512x512.png'
];

// API endpoints that should be cached
const API_CACHE_URLS = [
  '/api/models/supported',
  '/api/datasets/supported'
];

/**
 * Service Worker Installation
 * Pre-cache static assets
 */
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Pre-caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('[Service Worker] Installed successfully');
        return self.skipWaiting();
      })
  );
});

/**
 * Service Worker Activation
 * Clean up old caches
 */
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME && cacheName !== DATA_CACHE_NAME) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('[Service Worker] Activated successfully');
      return self.clients.claim();
    })
  );
});

/**
 * Fetch Event Handler
 * Implement cache-first strategy for static assets
 * Network-first strategy for API calls
 */
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip cross-origin requests
  if (url.origin !== location.origin) {
    return;
  }
  
  // API requests: Network-first, fallback to cache
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Clone response and cache it
          const responseClone = response.clone();
          caches.open(DATA_CACHE_NAME).then((cache) => {
            cache.put(request, responseClone);
          });
          return response;
        })
        .catch(() => {
          // Network failed, try cache
          return caches.match(request);
        })
    );
    return;
  }
  
  // Static assets: Cache-first, fallback to network
  event.respondWith(
    caches.match(request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          console.log('[Service Worker] Serving from cache:', request.url);
          return cachedResponse;
        }
        
        // Not in cache, fetch from network
        return fetch(request)
          .then((response) => {
            // Cache successful responses
            if (response.status === 200) {
              const responseClone = response.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, responseClone);
              });
            }
            return response;
          });
      })
  );
});

/**
 * Background Sync (for offline data submission)
 */
self.addEventListener('sync', (event) => {
  console.log('[Service Worker] Background sync:', event.tag);
  
  if (event.tag === 'sync-scan-results') {
    event.waitUntil(syncScanResults());
  }
});

/**
 * Push Notifications (future feature)
 */
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  
  const options = {
    body: data.body || 'Scan completed!',
    icon: '/icon-192x192.png',
    badge: '/icon-96x96.png',
    data: data
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title || 'Sleuth', options)
  );
});

/**
 * Notification Click Handler
 */
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow(event.notification.data.url || '/')
  );
});

/**
 * Helper: Sync scan results when back online
 */
async function syncScanResults() {
  try {
    // Get pending results from IndexedDB
    const db = await openIndexedDB();
    const pendingResults = await getPendingResults(db);
    
    // Upload each result
    for (const result of pendingResults) {
      await fetch('/api/results/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(result)
      });
      
      // Mark as synced
      await markAsSynced(db, result.id);
    }
    
    console.log('[Service Worker] Synced', pendingResults.length, 'results');
  } catch (error) {
    console.error('[Service Worker] Sync failed:', error);
  }
}

/**
 * Helper: Open IndexedDB for offline storage
 */
function openIndexedDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('sleuth-offline', 1);
    
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      
      if (!db.objectStoreNames.contains('scan-results')) {
        db.createObjectStore('scan-results', { keyPath: 'id', autoIncrement: true });
      }
    };
  });
}

/**
 * Helper: Get pending results
 */
function getPendingResults(db) {
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(['scan-results'], 'readonly');
    const store = transaction.objectStore('scan-results');
    const request = store.getAll();
    
    request.onsuccess = () => resolve(request.result || []);
    request.onerror = () => reject(request.error);
  });
}

/**
 * Helper: Mark result as synced
 */
function markAsSynced(db, id) {
  return new Promise((resolve, reject) => {
    const transaction = db.transaction(['scan-results'], 'readwrite');
    const store = transaction.objectStore('scan-results');
    const request = store.delete(id);
    
    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
}

/**
 * Message Handler (for communication with app)
 */
self.addEventListener('message', (event) => {
  console.log('[Service Worker] Received message:', event.data);
  
  if (event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(CACHE_NAME).then((cache) => {
        return cache.addAll(event.data.urls);
      })
    );
  }
});

console.log('[Service Worker] Loaded successfully');
