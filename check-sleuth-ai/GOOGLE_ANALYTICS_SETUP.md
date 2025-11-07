# Google Analytics 配置指南

## 📊 概述

本指南帮助你为 Check Sleuth AI 配置 Google Analytics 4 (GA4) 用于用户行为分析和产品优化。

---

## 🎯 获取 Google Analytics ID

### 步骤 1: 创建 GA4 账户

1. 访问 https://analytics.google.com/
2. 登录 Google 账号
3. 点击"开始测量"或"Admin"（管理）
4. 创建新的账户和属性

### 步骤 2: 获取测量 ID

1. 在 GA4 属性中，找到"数据流"（Data Streams）
2. 创建新的"网络"数据流
3. 输入网站 URL（例如：`https://your-domain.com`）
4. 复制"测量 ID"（格式：`G-XXXXXXXXXX`）

---

## ⚙️ 配置方案

### 方案 1: 硬编码配置（适合单一部署）

**编辑 `index.html`**（第37-46行）:

```html
<!-- 移除注释标记，替换测量 ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YOUR-ACTUAL-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-YOUR-ACTUAL-ID');
</script>
```

**优点:**
- 简单直接
- 无需额外配置

**缺点:**
- 开发/生产环境使用相同 ID
- 测试数据会混入生产数据

---

### 方案 2: 环境变量配置（推荐 - 灵活）

**步骤 1: 创建环境变量文件**

创建 `.env`:
```bash
VITE_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

创建 `.env.production`:
```bash
VITE_GA_MEASUREMENT_ID=G-PRODUCTION-ID
```

创建 `.env.development`:
```bash
VITE_GA_MEASUREMENT_ID=G-DEVELOPMENT-ID
```

**步骤 2: 更新 `.gitignore`**

确保环境变量文件不被提交:
```
.env
.env.local
.env.*.local
```

**步骤 3: 创建 GA 组件**

创建 `src/components/GoogleAnalytics.tsx`:
```typescript
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
    // 仅在有 ID 且非开发环境时加载
    if (!GA_ID || import.meta.env.DEV) {
      console.log('GA: Skipped (no ID or dev mode)');
      return;
    }

    // 加载 GA 脚本
    const script1 = document.createElement('script');
    script1.async = true;
    script1.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    document.head.appendChild(script1);

    // 初始化 GA
    window.dataLayer = window.dataLayer || [];
    window.gtag = function() {
      window.dataLayer.push(arguments);
    };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, {
      page_path: window.location.pathname,
    });

    console.log('GA: Initialized with ID:', GA_ID);
  }, [GA_ID]);

  return null;
}
```

**步骤 4: 集成到 App**

更新 `App.tsx`:
```typescript
import { GoogleAnalytics } from './components/GoogleAnalytics';

function App() {
  return (
    <>
      <GoogleAnalytics />
      {/* 其他组件... */}
    </>
  );
}
```

**优点:**
- ✅ 开发/生产环境分离
- ✅ 灵活配置
- ✅ 可以在开发环境禁用
- ✅ 符合安全最佳实践

---

### 方案 3: 动态加载（最灵活）

创建 `src/utils/analytics.ts`:
```typescript
interface AnalyticsEvent {
  action: string;
  category: string;
  label?: string;
  value?: number;
}

class Analytics {
  private initialized = false;
  private GA_ID = import.meta.env.VITE_GA_MEASUREMENT_ID;

  init() {
    if (this.initialized || !this.GA_ID || import.meta.env.DEV) {
      return;
    }

    // 加载 GA 脚本
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${this.GA_ID}`;
    document.head.appendChild(script);

    // 初始化
    (window as any).dataLayer = (window as any).dataLayer || [];
    (window as any).gtag = function() {
      (window as any).dataLayer.push(arguments);
    };
    (window as any).gtag('js', new Date());
    (window as any).gtag('config', this.GA_ID);

    this.initialized = true;
    console.log('Analytics initialized');
  }

  // 页面浏览
  pageView(path: string) {
    if (!this.initialized) return;
    (window as any).gtag('config', this.GA_ID, {
      page_path: path,
    });
  }

  // 自定义事件
  event({ action, category, label, value }: AnalyticsEvent) {
    if (!this.initialized) return;
    (window as any).gtag('event', action, {
      event_category: category,
      event_label: label,
      value: value,
    });
  }

  // CSV 上传事件
  trackCsvUpload(fileSize: number) {
    this.event({
      action: 'csv_upload',
      category: 'engagement',
      label: 'file_size',
      value: fileSize,
    });
  }

  // 分析完成事件
  trackAnalysisComplete(duration: number) {
    this.event({
      action: 'analysis_complete',
      category: 'engagement',
      label: 'duration_ms',
      value: duration,
    });
  }

  // 错误追踪
  trackError(error: string) {
    this.event({
      action: 'error',
      category: 'errors',
      label: error,
    });
  }
}

export const analytics = new Analytics();
```

**在应用中使用:**
```typescript
// App.tsx
import { analytics } from './utils/analytics';

useEffect(() => {
  analytics.init();
}, []);

// CSV 上传时
const handleCsvUpload = async (file: File) => {
  analytics.trackCsvUpload(file.size);
  // ... 其他逻辑
};

// 分析完成时
analytics.trackAnalysisComplete(duration);
```

---

## 📈 推荐的追踪事件

### 核心业务指标

```typescript
// 1. CSV 上传
analytics.event({
  action: 'csv_upload',
  category: 'engagement',
  label: fileType,
  value: fileSize
});

// 2. 分析完成
analytics.event({
  action: 'analysis_complete',
  category: 'engagement',
  value: analysisTime
});

// 3. 发现偏差
analytics.event({
  action: 'bias_detected',
  category: 'insights',
  label: biasType
});

// 4. 用户交互
analytics.event({
  action: 'view_details',
  category: 'engagement',
  label: detailType
});
```

### 性能监控

```typescript
// 页面加载时间
analytics.event({
  action: 'page_load',
  category: 'performance',
  value: loadTime
});

// API 响应时间
analytics.event({
  action: 'api_response',
  category: 'performance',
  label: endpoint,
  value: responseTime
});
```

---

## 🔒 隐私与合规

### 1. Cookie 同意横幅

创建 `src/components/CookieConsent.tsx`:
```typescript
import { useState, useEffect } from 'react';
import { analytics } from '../utils/analytics';

export function CookieConsent() {
  const [show, setShow] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem('cookie_consent');
    if (!consent) {
      setShow(true);
    } else if (consent === 'accepted') {
      analytics.init();
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem('cookie_consent', 'accepted');
    analytics.init();
    setShow(false);
  };

  const handleReject = () => {
    localStorage.setItem('cookie_consent', 'rejected');
    setShow(false);
  };

  if (!show) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-slate-800 border-t border-slate-700 p-4 z-50">
      <div className="container mx-auto flex flex-wrap items-center justify-between gap-4">
        <div className="flex-1 min-w-[300px]">
          <p className="text-sm text-slate-300">
            我们使用 cookies 来改善用户体验和分析网站流量。
            <a href="/privacy" className="text-blue-400 hover:underline ml-1">
              隐私政策
            </a>
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleReject}
            className="px-4 py-2 text-sm text-slate-300 hover:text-white"
          >
            拒绝
          </button>
          <button
            onClick={handleAccept}
            className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            接受
          </button>
        </div>
      </div>
    </div>
  );
}
```

### 2. 隐私政策页面

需要包含：
- 收集的数据类型
- 数据使用目的
- 用户权利（删除、访问数据）
- Cookie 列表
- 联系方式

### 3. GDPR 合规

```typescript
// 允许用户选择退出
const optOut = () => {
  document.cookie = `ga-disable-${GA_ID}=true; expires=Thu, 31 Dec 2099 23:59:59 UTC; path=/`;
  window[`ga-disable-${GA_ID}`] = true;
};
```

---

## 🚀 部署配置

### Vercel 部署

在 Vercel Dashboard 中设置环境变量:
```
VITE_GA_MEASUREMENT_ID = G-PRODUCTION-ID
```

或使用 Vercel CLI:
```bash
vercel env add VITE_GA_MEASUREMENT_ID production
# 输入: G-PRODUCTION-ID
```

### Netlify 部署

在 `netlify.toml` 中:
```toml
[build.environment]
  VITE_GA_MEASUREMENT_ID = "G-PRODUCTION-ID"
```

或在 Netlify UI 中: Site settings → Build & deploy → Environment variables

### 构建时注入

在 `package.json` 中:
```json
{
  "scripts": {
    "build": "vite build",
    "build:prod": "VITE_GA_MEASUREMENT_ID=G-PROD-ID vite build"
  }
}
```

---

## 🧪 测试 GA 配置

### 1. 使用 GA 调试插件

安装 Chrome 扩展：
- **Google Analytics Debugger**
- **GA Debugger**

### 2. 实时报告验证

1. 访问 GA4 → Reports → Realtime
2. 在浏览器中访问你的网站
3. 应该能看到活跃用户

### 3. 控制台验证

```typescript
// 在浏览器控制台
window.dataLayer
// 应该看到数据层数组

window.gtag
// 应该是一个函数
```

### 4. 网络请求验证

打开浏览器开发工具 → Network 标签
- 搜索 `google-analytics.com`
- 应该能看到 `collect` 或 `g/collect` 请求

---

## 📊 有用的 GA4 报告

### 推荐设置的自定义报告

1. **CSV 上传漏斗**
   - 页面访问 → CSV 上传 → 分析完成

2. **用户留存**
   - 首次访问 → 第二次访问 → 活跃用户

3. **性能监控**
   - 页面加载时间
   - API 响应时间
   - 错误率

4. **特征使用率**
   - 最常分析的文件类型
   - 平均文件大小
   - 分析耗时分布

---

## ⚠️ 常见问题

### Q: GA 数据不显示？

**检查清单:**
1. ✅ Measurement ID 是否正确?
2. ✅ 脚本是否成功加载? (检查 Network 标签)
3. ✅ Cookie 是否被允许?
4. ✅ 是否在生产环境? (DEV 模式可能禁用)
5. ✅ 浏览器是否有 AdBlock?

### Q: 开发环境也在追踪？

**解决方案:**
```typescript
// 在 GoogleAnalytics 组件中
if (import.meta.env.DEV) {
  console.log('GA disabled in development');
  return null;
}
```

### Q: 如何测试不污染生产数据?

**方案 1:** 使用开发环境 GA ID
```
VITE_GA_MEASUREMENT_ID=G-DEV-ID
```

**方案 2:** 使用 GA4 测试视图（Data Stream）

---

## 🎯 快速实施检查清单

- [ ] 创建 GA4 账户和属性
- [ ] 获取 Measurement ID
- [ ] 选择配置方案（推荐方案 2 或 3）
- [ ] 实施 Cookie 同意机制
- [ ] 设置环境变量
- [ ] 添加核心事件追踪
- [ ] 部署并测试
- [ ] 验证实时数据
- [ ] 创建自定义报告
- [ ] 编写隐私政策

---

## 📚 相关资源

- **GA4 官方文档**: https://developers.google.com/analytics/devguides/collection/ga4
- **React GA4**: https://github.com/PriceRunner/react-ga4
- **GDPR 合规**: https://support.google.com/analytics/answer/9019185
- **Cookie 同意**: https://support.google.com/analytics/answer/9976101

---

**最后更新:** 2025-11-05  
**状态:** 待实施
