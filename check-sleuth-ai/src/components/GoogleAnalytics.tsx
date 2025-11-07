import { useEffect } from 'react';

declare global {
  interface Window {
    dataLayer: any[];
    gtag: (...args: any[]) => void;
  }
}

export function GoogleAnalytics() {
  const GA_ID = import.meta.env.VITE_GA_MEASUREMENT_ID;

  useEffect(() => {
    // 跳过开发环境
    if (import.meta.env.DEV) {
      console.log('🔍 GA: Skipped in development mode');
      return;
    }

    // 如果没有配置 ID
    if (!GA_ID) {
      console.log('⚠️ GA: No Measurement ID configured');
      return;
    }

    // 加载 GA 脚本
    const script1 = document.createElement('script');
    script1.async = true;
    script1.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    document.head.appendChild(script1);

    // 初始化 Google Analytics
    window.dataLayer = window.dataLayer || [];
    window.gtag = function() {
      window.dataLayer.push(arguments);
    };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, {
      page_path: window.location.pathname,
    });

    console.log('✅ GA: Initialized with ID:', GA_ID);
  }, [GA_ID]);

  return null;
}

// 自定义事件追踪函数
export const trackEvent = (action: string, category: string, label?: string, value?: number) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', action, {
      event_category: category,
      event_label: label,
      value: value,
    });
  }
};

// CSV 上传事件
export const trackCsvUpload = (fileSize: number, fileName: string) => {
  trackEvent('csv_upload', 'engagement', fileName, fileSize);
};

// 分析完成事件
export const trackAnalysisComplete = (duration: number, isMock: boolean) => {
  trackEvent('analysis_complete', 'engagement', isMock ? 'mock' : 'real', duration);
};

// 偏差检测事件
export const trackBiasDetected = (biasType: string) => {
  trackEvent('bias_detected', 'insights', biasType);
};

// 错误追踪
export const trackError = (errorMessage: string) => {
  trackEvent('error', 'errors', errorMessage);
};
