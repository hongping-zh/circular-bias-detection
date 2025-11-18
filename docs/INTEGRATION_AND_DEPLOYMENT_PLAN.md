# MVP 整合与部署完整方案

## 📋 目录

1. [当前状态评估](#当前状态评估)
2. [整合 circular-bias-detector](#整合-circular-bias-detector)
3. [配置真实 API Key](#配置真实-api-key)
4. [部署到生产环境](#部署到生产环境)
5. [配置 Google Analytics](#配置-google-analytics)
6. [完整实施清单](#完整实施清单)

---

## 当前状态评估

### ✅ 已完成
- **前端应用**: check-sleuth-ai (React + Vite + TypeScript)
- **后端 API**: backend (Flask + Python)
- **Gemini AI 集成**: CSV 分析功能
- **本地测试**: 功能正常运行

### 📦 代码包结构

```
circular-bias-detection/
├── check-sleuth-ai/          # 前端 (React MVP)
│   ├── components/
│   ├── services/
│   └── ...
│
├── backend/                   # 后端 API (Flask)
│   ├── core/                  # 自定义实现
│   │   ├── bias_scorer.py
│   │   ├── psi_calculator.py
│   │   ├── ccs_calculator.py
│   │   └── rho_pc_calculator.py
│   └── app.py
│
└── circular_bias_detector/    # 完整的 Python 包 (v1.2.0) ⭐ 新增
    ├── core/                  # 核心算法模块
    ├── inference/             # LLM 集成
    ├── detection.py           # BiasDetector 类
    ├── utils.py
    ├── visualization.py
    └── __init__.py
```

### 🔍 差异分析

| 特性 | backend/core | circular_bias_detector |
|------|-------------|------------------------|
| **成熟度** | 基础实现 | 生产级 (v1.2.0) |
| **测试覆盖** | 部分 | 80%+ |
| **文档** | 内联注释 | 完整文档 |
| **配置管理** | 无 | 统一配置 (config.py) |
| **日志系统** | print 语句 | 结构化日志 |
| **异常处理** | 基础 | 完整层次结构 |
| **Bootstrap CI** | 有 | 有 |
| **可视化** | 无 | 完整 |
| **LLM 集成** | 无 | 支持 (vLLM) |
| **包管理** | 无 | PyPI 就绪 |

**建议**: 将 backend/core 迁移到使用 circular_bias_detector 包

---

## 整合 circular-bias-detector

### 方案 A: 渐进式整合（推荐）

保持向后兼容，逐步迁移。

#### 步骤 1: 安装包

```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection

# 开发模式安装（可编辑）
pip install -e .

# 或者正常安装
pip install .
```

#### 步骤 2: 更新 backend/requirements.txt

添加：
```
circular-bias-detector>=1.2.0
```

#### 步骤 3: 创建适配层

创建 `backend/adapters/bias_detector_adapter.py`:

```python
"""
Adapter for circular_bias_detector package
Provides backward-compatible interface for existing API
"""

import pandas as pd
from typing import Dict
from circular_bias_detector import BiasDetector, get_config, set_config
from circular_bias_detector.exceptions import BiasDetectionError

class BiasDetectorAdapter:
    """
    Adapter to integrate circular_bias_detector into existing Flask API
    """
    
    def __init__(self):
        """Initialize with default configuration"""
        self.detector = BiasDetector()
        
        # Configure for API usage
        config = get_config()
        config.log_level = "WARNING"  # Less verbose for API
        config.enable_bootstrap = False  # Default to fast mode
        set_config(config)
    
    def detect_bias_from_dataframe(
        self, 
        df: pd.DataFrame, 
        run_bootstrap: bool = False,
        n_bootstrap: int = 1000
    ) -> Dict:
        """
        Detect bias using circular_bias_detector package
        
        Args:
            df: DataFrame with evaluation data
            run_bootstrap: Whether to compute bootstrap CI
            n_bootstrap: Number of bootstrap iterations
            
        Returns:
            Dictionary with detection results (API-compatible format)
        """
        try:
            # Run detection
            results = self.detector.detect(
                df, 
                return_dict=True,
                compute_bootstrap=run_bootstrap,
                n_bootstrap=n_bootstrap
            )
            
            # Transform to API format
            api_results = self._transform_to_api_format(results)
            
            return api_results
            
        except BiasDetectionError as e:
            raise ValueError(f"Bias detection failed: {str(e)}")
    
    def _transform_to_api_format(self, results: Dict) -> Dict:
        """Transform package results to API format"""
        
        # Extract metrics
        metrics = results.get('metrics', {})
        
        return {
            # Individual indicators
            'psi': {
                'score': metrics.get('psi', 0.0),
                'normalized': metrics.get('psi_normalized', 0.0),
                'threshold': metrics.get('psi_threshold', 0.2),
                'exceeds_threshold': metrics.get('psi_exceeds', False),
                'interpretation': metrics.get('psi_interpretation', '')
            },
            'ccs': {
                'score': metrics.get('ccs', 0.0),
                'normalized': metrics.get('ccs_normalized', 0.0),
                'threshold': metrics.get('ccs_threshold', 0.85),
                'exceeds_threshold': metrics.get('ccs_exceeds', False),
                'interpretation': metrics.get('ccs_interpretation', '')
            },
            'rho_pc': {
                'score': metrics.get('rho_pc', 0.0),
                'normalized': metrics.get('rho_pc_normalized', 0.0),
                'threshold': metrics.get('rho_pc_threshold', 0.5),
                'exceeds_threshold': metrics.get('rho_pc_exceeds', False),
                'p_value': metrics.get('rho_pc_pvalue', 1.0),
                'significant': metrics.get('rho_pc_significant', False),
                'interpretation': metrics.get('rho_pc_interpretation', '')
            },
            
            # CBS composite
            'cbs_score': results.get('cbs_score', 0.0),
            'risk_level': results.get('risk_level', 'Low Risk'),
            'risk_category': results.get('risk_category', 'low'),
            'weights': results.get('weights', [0.33, 0.33, 0.34]),
            
            # Decision
            'bias_detected': results.get('bias_detected', False),
            'indicators_triggered': results.get('indicators_triggered', 0),
            'confidence': results.get('confidence', 0.0),
            
            # Explanations
            'interpretation': results.get('interpretation', ''),
            'recommendations': results.get('recommendations', []),
            
            # Metadata
            'data_stats': results.get('data_stats', {}),
            
            # Bootstrap (if available)
            'bootstrap': results.get('bootstrap', None)
        }


# Convenience function for drop-in replacement
def detect_circular_bias(
    data: pd.DataFrame,
    weights: list = [0.33, 0.33, 0.34],
    run_bootstrap: bool = False,
    n_bootstrap: int = 1000
) -> Dict:
    """
    Drop-in replacement for original detect_circular_bias function
    Now uses circular_bias_detector package
    """
    adapter = BiasDetectorAdapter()
    return adapter.detect_bias_from_dataframe(
        data, 
        run_bootstrap=run_bootstrap,
        n_bootstrap=n_bootstrap
    )
```

#### 步骤 4: 更新 backend/app.py

只需修改 import：

```python
# 旧版本
# from core.bias_scorer import detect_circular_bias

# 新版本
from adapters.bias_detector_adapter import detect_circular_bias
```

#### 步骤 5: 测试

```bash
# 重启后端
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend
python app.py
```

### 方案 B: 完全迁移

直接使用 circular_bias_detector，移除 backend/core。

**优点**: 代码更简洁
**缺点**: 需要更多测试

---

## 配置真实 API Key

### 步骤 1: 获取 Gemini API Key

1. 访问: https://makersuite.google.com/app/apikey
2. 登录 Google 账号
3. 点击 "Create API Key"
4. 复制 API Key (格式: `AIzaSy...`)

### 步骤 2: 本地测试配置

**Windows (PowerShell)**:
```powershell
# 设置环境变量
$env:GEMINI_API_KEY="AIzaSy_your_actual_key_here"

# 验证
echo $env:GEMINI_API_KEY

# 启动后端
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend
python app.py
```

预期输出:
```
✅ Gemini API configured successfully
```

### 步骤 3: 测试 CSV 分析

```powershell
# 在浏览器打开
http://localhost:3000

# 上传 CSV 文件
# 应该看到真实的 AI 分析，不再是 "Demo Mode"
```

### 步骤 4: 持久化配置

#### 方式 A: 系统环境变量（推荐）

1. Windows 搜索: "环境变量"
2. 点击 "编辑系统环境变量"
3. 环境变量 → 新建
4. 变量名: `GEMINI_API_KEY`
5. 变量值: `AIzaSy...`

#### 方式 B: .env 文件

创建 `backend/.env`:
```
GEMINI_API_KEY=AIzaSy_your_actual_key_here
```

安装 python-dotenv:
```bash
pip install python-dotenv
```

更新 `backend/app.py`:
```python
from dotenv import load_dotenv
load_dotenv()  # 在顶部添加
```

---

## 部署到生产环境

### 选项 1: Vercel（推荐 - 最简单）

#### 前置条件
```bash
# 安装 Vercel CLI
npm install -g vercel
```

#### 部署步骤

**1. 准备前端**

创建 `check-sleuth-ai/vercel.json`:
```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "devCommand": "npm run dev",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend-url.vercel.app/api/:path*"
    }
  ]
}
```

**2. 部署前端**

```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection\check-sleuth-ai

# 登录 Vercel
vercel login

# 部署
vercel

# 按提示操作:
# - Set up and deploy? Yes
# - Which scope? (选择你的账号)
# - Link to existing project? No
# - Project name? check-sleuth-ai
# - Directory? ./
# - Override settings? No
```

**3. 准备后端**

创建 `backend/vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

创建 `backend/requirements.txt` (确保完整):
```
flask>=3.0.0
flask-cors>=4.0.0
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
circular-bias-detector>=1.2.0
```

**4. 部署后端**

```bash
cd C:\Users\14593\CascadeProjects\circular-bias-detection\backend

vercel

# 记录部署 URL，例如: https://your-backend-xyz.vercel.app
```

**5. 配置环境变量**

```bash
# 为后端添加 API Key
vercel env add GEMINI_API_KEY production

# 输入你的 API Key
```

**6. 更新前端配置**

更新 `check-sleuth-ai/vercel.json` 中的后端 URL:
```json
"destination": "https://your-backend-xyz.vercel.app/api/:path*"
```

重新部署前端:
```bash
cd check-sleuth-ai
vercel --prod
```

**7. 验证部署**

访问你的前端 URL: `https://check-sleuth-ai-xxx.vercel.app`

---

### 选项 2: Netlify + Vercel

#### 前端 → Netlify

**1. 构建前端**

```bash
cd check-sleuth-ai
npm run build
```

**2. 部署到 Netlify**

方式 A: 拖拽部署
- 访问: https://app.netlify.com/drop
- 拖拽 `dist/` 文件夹

方式 B: CLI 部署
```bash
npm install -g netlify-cli
netlify deploy --prod
```

**3. 配置重定向**

创建 `check-sleuth-ai/dist/_redirects`:
```
/api/*  https://your-backend.vercel.app/api/:splat  200
```

#### 后端 → Vercel

同上（选项 1 的步骤 3-5）

---

### 选项 3: 传统 VPS（Linux）

#### 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 安装 Python
sudo apt install -y python3 python3-pip python3-venv

# 安装 Nginx
sudo apt install -y nginx

# 安装 PM2
sudo npm install -g pm2
```

#### 部署后端

```bash
# 创建目录
sudo mkdir -p /var/www/sleuth-backend
cd /var/www/sleuth-backend

# 克隆代码（或 scp 上传）
# ...

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
sudo nano /etc/environment
# 添加: GEMINI_API_KEY="your-key"

# 使用 PM2 运行
pm2 start app.py --name sleuth-backend --interpreter venv/bin/python
pm2 save
pm2 startup
```

#### 部署前端

```bash
# 构建
cd check-sleuth-ai
npm run build

# 复制到 Nginx
sudo cp -r dist/* /var/www/html/

# 配置 Nginx
sudo nano /etc/nginx/sites-available/default
```

Nginx 配置:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /var/www/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# 重启 Nginx
sudo systemctl restart nginx
```

---

## 配置 Google Analytics

### 步骤 1: 创建 GA4 属性

1. 访问: https://analytics.google.com/
2. 管理 → 创建属性
3. 属性名称: "Check Sleuth AI"
4. 创建数据流 → 网站
5. 网站 URL: `https://your-domain.com`
6. 复制 Measurement ID (格式: `G-XXXXXXXXXX`)

### 步骤 2: 方式 A - 直接添加到 HTML（快速）

编辑 `check-sleuth-ai/index.html`，找到第 37-46 行:

```html
<!-- 取消注释并替换 ID -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YOUR-REAL-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-YOUR-REAL-ID');
</script>
```

### 步骤 3: 方式 B - 使用环境变量（推荐）

**本地开发**:

创建 `.env`:
```
VITE_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

创建 `.env.production`:
```
VITE_GA_MEASUREMENT_ID=G-PRODUCTION-ID
```

**Vercel 部署**:
```bash
vercel env add VITE_GA_MEASUREMENT_ID production
# 输入: G-XXXXXXXXXX
```

**Netlify 部署**:

在 Site settings → Build & deploy → Environment variables:
```
Key: VITE_GA_MEASUREMENT_ID
Value: G-XXXXXXXXXX
```

### 步骤 4: 创建 GA 组件

创建 `check-sleuth-ai/src/components/GoogleAnalytics.tsx`:

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
    if (!GA_ID || import.meta.env.DEV) {
      console.log('GA: Skipped (no ID or dev mode)');
      return;
    }

    // 加载 GA 脚本
    const script1 = document.createElement('script');
    script1.async = true;
    script1.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    document.head.appendChild(script1);

    // 初始化
    window.dataLayer = window.dataLayer || [];
    window.gtag = function() {
      window.dataLayer.push(arguments);
    };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);

    console.log('GA: Initialized', GA_ID);
  }, [GA_ID]);

  return null;
}
```

### 步骤 5: 集成到 App

编辑 `check-sleuth-ai/App.tsx`:

```typescript
import { GoogleAnalytics } from './components/GoogleAnalytics';

function App() {
  return (
    <>
      <GoogleAnalytics />
      {/* 其他组件 */}
    </>
  );
}
```

### 步骤 6: 验证

1. 部署应用
2. 访问网站
3. 打开 GA4 → Reports → Realtime
4. 应该看到活跃用户

---

## 完整实施清单

### Phase 1: 整合 circular-bias-detector（2小时）

- [ ] 安装 circular-bias-detector 包
- [ ] 创建适配层 (bias_detector_adapter.py)
- [ ] 更新 backend/app.py imports
- [ ] 更新 requirements.txt
- [ ] 本地测试后端 API
- [ ] 验证偏差检测功能

### Phase 2: 配置真实 API Key（15分钟）

- [ ] 获取 Gemini API Key
- [ ] 配置环境变量（本地）
- [ ] 测试真实 AI 分析
- [ ] 验证不再显示 "Demo Mode"
- [ ] 测试多个 CSV 文件

### Phase 3: 部署到生产环境（1-2小时）

#### 选择部署方案:
- [ ] 选项 1: Vercel（前端 + 后端）
- [ ] 选项 2: Netlify（前端）+ Vercel（后端）
- [ ] 选项 3: VPS（Linux）

#### 执行部署:
- [ ] 准备配置文件 (vercel.json / netlify.toml)
- [ ] 部署后端
- [ ] 配置生产环境变量
- [ ] 部署前端
- [ ] 更新 API 路由配置
- [ ] 验证前后端通信

#### 测试:
- [ ] CSV 上传功能
- [ ] AI 分析功能
- [ ] 偏差检测功能
- [ ] 移动端体验
- [ ] 性能测试

### Phase 4: 配置 Google Analytics（30分钟）

- [ ] 创建 GA4 属性
- [ ] 获取 Measurement ID
- [ ] 选择集成方式（HTML / 环境变量）
- [ ] 添加 GA 代码
- [ ] 部署更新
- [ ] 验证 Realtime 数据

#### 可选增强:
- [ ] 添加自定义事件（CSV上传、分析完成）
- [ ] 配置转化目标
- [ ] 创建自定义报告
- [ ] 实施 Cookie 同意机制

### Phase 5: 最终验证（30分钟）

- [ ] 端到端测试（上传 → 分析 → 结果）
- [ ] 跨浏览器测试（Chrome、Firefox、Safari）
- [ ] 移动设备测试
- [ ] 性能测试（Lighthouse）
- [ ] SEO 检查
- [ ] 安全审查

---

## 时间估算

| 阶段 | 时间 | 优先级 |
|------|------|--------|
| Phase 1: 整合包 | 2小时 | 中 |
| Phase 2: API Key | 15分钟 | 高 |
| Phase 3: 部署 | 1-2小时 | 高 |
| Phase 4: GA | 30分钟 | 低 |
| Phase 5: 验证 | 30分钟 | 高 |
| **总计** | **4-5小时** | - |

---

## 下一步建议

### 立即执行（高优先级）

1. **配置 API Key**（15分钟）
   - 最快看到真实 AI 效果
   - 验证功能完整性

2. **部署到 Vercel**（1小时）
   - 获得公网访问 URL
   - 展示给其他人

### 稍后执行（中优先级）

3. **整合 circular-bias-detector**（2小时）
   - 提升代码质量
   - 生产级功能

4. **配置 Google Analytics**（30分钟）
   - 了解用户行为
   - 产品优化依据

---

## 需要帮助？

我可以帮你：
1. ✅ 创建适配层代码
2. ✅ 准备部署配置文件
3. ✅ 编写 GA 集成代码
4. ✅ 逐步指导部署流程

**告诉我你想从哪里开始！** 😊
