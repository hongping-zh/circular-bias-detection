# Google Analytics - 快速参考

## ✅ 当前状态

- ✅ **代码已准备**: `index.html` 第37-46行（已注释）
- ✅ **文档已完成**: `GOOGLE_ANALYTICS_SETUP.md`
- ⏸️ **等待激活**: 需要 GA Measurement ID

---

## ⚡ 2分钟快速启用

### 步骤 1: 获取 Measurement ID

访问 https://analytics.google.com/ → 创建 GA4 属性 → 复制 ID (格式: `G-XXXXXXXXXX`)

### 步骤 2: 启用代码

编辑 `index.html`，找到第37-46行，删除 `<!--` 和 `-->`：

**之前:**
```html
    <!-- Google Analytics - Replace G-XXXXXXXXXX with your Measurement ID -->
    <!--
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    ...
    -->
```

**之后:**
```html
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-YOUR-REAL-ID"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-YOUR-REAL-ID');
    </script>
```

### 步骤 3: 部署并验证

```bash
npm run build
# 部署到你的平台

# 验证: 访问 GA4 → Realtime，应该看到活跃用户
```

---

## 🎯 配置方案对比

| 方案 | 复杂度 | 灵活性 | 推荐场景 |
|------|--------|--------|----------|
| **直接修改 HTML** | ⭐ 简单 | ⭐ 低 | 快速测试、单一环境 |
| **环境变量** | ⭐⭐ 中等 | ⭐⭐⭐ 高 | 生产部署（推荐） |
| **动态加载** | ⭐⭐⭐ 复杂 | ⭐⭐⭐ 高 | 需要自定义事件追踪 |

---

## 📋 完整实施检查清单

**基础配置:**
- [ ] 创建 GA4 账户和属性
- [ ] 获取 Measurement ID
- [ ] 取消 `index.html` 注释
- [ ] 替换 ID
- [ ] 部署应用
- [ ] 在 GA4 Realtime 中验证

**进阶配置** (可选):
- [ ] 设置环境变量 (开发/生产分离)
- [ ] 添加自定义事件追踪
- [ ] 实施 Cookie 同意横幅
- [ ] 创建自定义报告
- [ ] 设置转化目标

**合规性** (欧盟用户必需):
- [ ] 添加隐私政策
- [ ] 实施 Cookie 同意机制
- [ ] 提供退出选项
- [ ] GDPR 合规审查

---

## 🔗 相关文档

- **完整指南**: `GOOGLE_ANALYTICS_SETUP.md`
- **部署配置**: `DEPLOYMENT_GUIDE.md` (第366-412行)
- **GA4 官方**: https://analytics.google.com/

---

## 💡 推荐追踪的事件

```javascript
// CSV 上传
gtag('event', 'csv_upload', {
  'event_category': 'engagement',
  'file_size': fileSize
});

// 分析完成
gtag('event', 'analysis_complete', {
  'event_category': 'engagement',
  'duration': duration
});

// 发现偏差
gtag('event', 'bias_detected', {
  'event_category': 'insights',
  'bias_type': biasType
});
```

详细实现见 `GOOGLE_ANALYTICS_SETUP.md` 方案3。

---

**需要帮助？** 查看 `GOOGLE_ANALYTICS_SETUP.md` 获取详细说明和故障排查指南。
