# API Key 三层架构策略

## 🎯 商业模式设计

### 三层服务架构

```
🆓 Demo 模式
    ↓
💰 DeepSeek 基础版（免费/低价）
    ↓
💎 Gemini 高级版（付费/用户自带 Key）
```

---

## 📊 层级对比

| 功能 | Demo 模式 | DeepSeek 基础版 | Gemini 高级版 |
|------|----------|----------------|--------------|
| **价格** | 完全免费 | 免费或低价订阅 | 订阅或自带 Key |
| **API Key** | 无需 | 使用你的 | 用户自己的 |
| **分析质量** | 预设示例 | 真实 AI 分析 | 高级 AI 分析 |
| **每日限额** | 无限 | 10-50 次 | 无限 |
| **响应速度** | 即时 | 快速（5-10s） | 较快（10-20s） |
| **成本（每次）** | $0 | ~$0.001 | ~$0.01-0.02 |
| **适合用户** | 试用者 | 个人/学习者 | 企业/专业用户 |

---

## 💰 成本分析

### DeepSeek API 成本

**DeepSeek-V3 定价**：
- Input: ¥1/百万 token (~$0.14)
- Output: ¥2/百万 token (~$0.28)

**每次分析预估**：
- Input: ~1000 tokens (CSV 数据)
- Output: ~500 tokens (分析结果)
- **成本**: ~¥0.003 (~$0.0004)

**月度预估**（1000 次分析）：
- **成本**: ~¥3 (~$0.40)
- **非常便宜！**

### Gemini API 成本

**Gemini 2.5 Pro 定价**：
- Input: $0.30/百万 token
- Output: $1.20/百万 token

**每次分析预估**：
- **成本**: ~$0.002-0.005

**月度预估**（1000 次分析）：
- **成本**: ~$3-5

---

## 🚀 实施计划

### Phase 1：添加 DeepSeek 支持（今天）

#### 步骤 1：获取 DeepSeek API Key

1. 访问：https://platform.deepseek.com/
2. 注册账号（支持中国手机号）
3. 获取 API Key
4. 充值最低金额（¥10 可用很久）

#### 步骤 2：修改后端代码

创建统一的 AI 服务接口，支持多个 LLM：
- DeepSeek（默认，免费层）
- Gemini（高级层）
- 支持用户自带 Key

#### 步骤 3：配置环境变量

```python
DEEPSEEK_API_KEY=your_deepseek_key
GEMINI_API_KEY=your_gemini_key  # 可选
```

#### 步骤 4：部署到 PythonAnywhere

---

### Phase 2：用户自带 Key 功能（本周）

#### 前端添加设置页面

- 输入框：Gemini API Key
- 存储在 localStorage
- 发送请求时携带

#### 后端验证用户 Key

- 验证 Key 有效性
- 使用用户的 Key 调用 API
- 成本由用户承担

---

### Phase 3：订阅制（下月）

#### 功能

- 用户注册/登录
- 选择套餐（基础/专业/企业）
- 支付集成（Stripe/支付宝）
- 使用限额管理

#### 套餐设计

**基础版** - ¥0/月
- DeepSeek API
- 10 次/天
- 社区支持

**专业版** - ¥29/月
- DeepSeek API
- 100 次/天
- 邮件支持

**企业版** - ¥199/月
- Gemini 2.5 Pro API
- 无限次数
- 专属支持
- Research 服务

---

## 🔧 技术实现

### 1. 创建 LLM 服务抽象层

```python
# backend/services/llm_service.py

class LLMService:
    def __init__(self, provider='deepseek'):
        self.provider = provider
        
    def analyze(self, csv_content, user_api_key=None):
        if user_api_key:
            # 使用用户的 Gemini Key
            return self._analyze_with_gemini(csv_content, user_api_key)
        elif self.provider == 'deepseek':
            # 使用你的 DeepSeek Key（免费层）
            return self._analyze_with_deepseek(csv_content)
        else:
            # 使用 Demo 数据
            return self._get_mock_data()
    
    def _analyze_with_deepseek(self, csv_content):
        # DeepSeek API 调用
        pass
    
    def _analyze_with_gemini(self, csv_content, api_key):
        # Gemini API 调用
        pass
    
    def _get_mock_data(self):
        # 返回 Demo 数据
        pass
```

### 2. DeepSeek API 集成

```python
import requests

def analyze_with_deepseek(csv_content):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""You are an expert data analyst...
    
    CSV Data:
    {csv_content[:2000]}  # 限制长度
    
    Analyze and return JSON..."""
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### 3. API 端点更新

```python
@app.route('/api/analyze-csv', methods=['POST'])
def analyze_csv():
    csv_content = request.data.decode('utf-8')
    user_api_key = request.headers.get('X-Gemini-API-Key')  # 用户自带 Key
    tier = request.headers.get('X-Service-Tier', 'free')  # free/basic/premium
    
    llm_service = LLMService(provider='deepseek')
    result = llm_service.analyze(csv_content, user_api_key)
    
    return jsonify(result)
```

---

## 📱 前端 UI 设计

### 添加服务层级选择

```typescript
// 在上传页面显示
<div className="service-tiers">
  <div className="tier free">
    🆓 Demo Mode
    <p>Sample analysis</p>
  </div>
  
  <div className="tier basic active">
    ⚡ Basic (Free)
    <p>AI-powered with DeepSeek</p>
    <p>10 analyses/day</p>
  </div>
  
  <div className="tier premium">
    💎 Premium
    <p>Advanced Gemini AI</p>
    <p>Unlimited analyses</p>
    <button>Add API Key</button>
  </div>
</div>
```

### 用户自带 Key 设置

```typescript
// Settings 页面
<div className="api-key-settings">
  <h3>Gemini API Key (Optional)</h3>
  <input 
    type="password" 
    placeholder="Enter your Gemini API Key"
    value={apiKey}
    onChange={(e) => setApiKey(e.target.value)}
  />
  <button onClick={saveApiKey}>Save</button>
  <p className="help-text">
    Get your key from: 
    <a href="https://makersuite.google.com/app/apikey">
      Google AI Studio
    </a>
  </p>
</div>
```

---

## 🎯 推荐实施顺序

### ✅ 今天（Phase 1）

1. **注册 DeepSeek 账号**（10 分钟）
2. **获取 API Key**
3. **在 PythonAnywhere 配置环境变量**
4. **修改后端代码**（我帮你写）
5. **测试 DeepSeek 分析**
6. **重新部署**

**预计时间**: 2-3 小时

---

### 📅 本周（Phase 2）

1. 添加用户自带 Key 功能
2. 前端设置页面
3. 使用限额显示

**预计时间**: 4-6 小时

---

### 📅 下月（Phase 3）

1. 用户认证系统（Supabase）
2. 订阅管理
3. 支付集成
4. Research 服务

**预计时间**: 2-3 周

---

## 💡 额外建议

### 1. 使用限额策略

**免费层（DeepSeek）**：
- IP 限制：每个 IP 每天 10 次
- 或用户注册：每个用户每天 20 次
- 超出提示升级

**高级层（Gemini）**：
- 用户自带 Key：无限
- 订阅用户：根据套餐

### 2. 降级策略

```
Gemini API 失败
    ↓
自动降级到 DeepSeek
    ↓
DeepSeek 失败
    ↓
返回 Demo 数据
```

### 3. 缓存策略

- 相同 CSV 数据缓存结果（24小时）
- 减少 API 调用
- 降低成本

---

## 📊 预期效果

### 用户分布预估

- **Demo 用户**: 70%（试用）
- **DeepSeek 用户**: 25%（免费或低价）
- **Gemini 用户**: 5%（高级用户）

### 月度成本预估（1000 活跃用户）

**场景 1：保守估计**
- DeepSeek 调用：5000 次/月
- 成本：¥15/月（~$2）

**场景 2：增长期**
- DeepSeek 调用：20000 次/月
- 成本：¥60/月（~$8）

**非常可控！**

---

## 🎉 总结

### 你的策略优势

✅ **成本可控**：DeepSeek 非常便宜  
✅ **灵活扩展**：三层架构适应不同用户  
✅ **降低门槛**：免费用户可获得真实 AI  
✅ **商业化路径**：订阅制 + 用户自带 Key  

### 立即行动

**我建议今天就实施 Phase 1**：
1. 注册 DeepSeek
2. 修改后端代码
3. 测试部署

**准备好了吗？我们开始吧！** 🚀
