# DeepSeek API 部署指南

## 🎉 你的 API Key

```
DEEPSEEK_API_KEY=alipay8509a3e9943141758593cd69dcb45e77
```

**注意**：此 Key 已集成到代码中，下面的步骤会指导你安全配置。

---

## 🚀 部署到 PythonAnywhere（10 分钟）

### 第一步：配置环境变量

1. **打开 Bash Console**
   - 访问：https://www.pythonanywhere.com/user/hongpingzhang/consoles/
   - 点击现有的 Bash Console 或创建新的

2. **编辑 WSGI 文件**
   - 访问：https://www.pythonanywhere.com/user/hongpingzhang/files/var/www/hongpingzhang_pythonanywhere_com_wsgi.py
   
3. **添加 DeepSeek API Key**
   
   在 WSGI 文件中，找到这一行：
   ```python
   os.environ['FLASK_ENV'] = 'production'
   ```
   
   在它**下面添加**：
   ```python
   os.environ['DEEPSEEK_API_KEY'] = 'alipay8509a3e9943141758593cd69dcb45e77'
   ```
   
   完整示例：
   ```python
   # 导入 Flask 应用
   from app import app as application

   # 设置环境变量
   os.environ['FLASK_ENV'] = 'production'
   os.environ['DEEPSEEK_API_KEY'] = 'alipay8509a3e9943141758593cd69dcb45e77'
   ```

4. **保存文件**（点击 Save）

---

### 第二步：更新代码

1. **打开 Bash Console**

2. **进入项目目录**
   ```bash
   cd ~/circular-bias-detection/backend
   ```

3. **拉取最新代码**
   ```bash
   git pull origin main
   ```
   
   如果提示冲突，运行：
   ```bash
   git stash
   git pull origin main
   ```

4. **检查新文件**
   ```bash
   ls services/
   # 应该看到 llm_service.py 和 __init__.py
   ```

---

### 第三步：重新加载应用

1. **访问 Web 页面**
   ```
   https://www.pythonanywhere.com/user/hongpingzhang/webapps/
   ```

2. **点击绿色的 "Reload" 按钮**
   ```
   Reload hongpingzhang.pythonanywhere.com
   ```

3. **等待 10-20 秒**

---

### 第四步：测试 DeepSeek 集成

#### A. 测试 Health Check

访问：
```
https://hongpingzhang.pythonanywhere.com/health
```

应该返回：
```json
{
  "status": "ok",
  "service": "Sleuth Bias Detection API",
  "version": "1.0.0"
}
```

#### B. 测试 CSV 分析（真实 AI！）

**使用 Postman 或 cURL**：

```bash
curl -X POST https://hongpingzhang.pythonanywhere.com/api/analyze-csv \
  -H "Content-Type: text/plain" \
  --data "name,age,income,has_churned
Alice,25,50000,0
Bob,35,75000,1
Charlie,45,100000,0"
```

**预期响应**：
```json
{
  "summary": "真实的 AI 分析摘要...",
  "dataQualityInsights": ["真实的数据质量洞察..."],
  "biasDetectionInsights": ["真实的偏差检测结果..."],
  "provider": "deepseek",
  "isMock": false
}
```

✅ **如果看到 `"provider": "deepseek"` 和 `"isMock": false`，说明成功！**

---

## 🎯 验证服务层级

### 三层架构已激活

1. **Demo 模式**（如果没有任何 API Key）
   - `provider`: "demo"
   - `isMock`: true

2. **DeepSeek 基础版**（当前配置）✅
   - `provider`: "deepseek"
   - `isMock`: false
   - 真实 AI 分析

3. **Gemini 高级版**（用户自带 Key）
   - 前端发送时添加 header：`X-Gemini-API-Key`
   - `provider`: "gemini"
   - `isMock`: false

---

## 📊 查看日志

### 检查 DeepSeek 是否正常工作

1. **访问错误日志**
   ```
   https://www.pythonanywhere.com/user/hongpingzhang/files/var/log/hongpingzhang.pythonanywhere.com.error.log
   ```

2. **查找以下信息**：
   ```
   ✅ DeepSeek API configured successfully (Primary)
   ```
   
   或在分析请求时：
   ```
   [LLM] Calling DeepSeek API...
   [LLM] DeepSeek analysis complete (tokens: XXX)
   ✅ DEEPSEEK analysis complete
   ```

---

## 🔧 故障排查

### 问题 1：仍然返回 Demo 数据

**症状**：`"provider": "demo"` 和 `"isMock": true`

**解决**：
1. 确认 WSGI 文件中添加了环境变量
2. 确认 Reload 了 Web 应用
3. 检查错误日志

### 问题 2：DeepSeek API 错误

**症状**：日志中看到 `[LLM] DeepSeek API failed`

**可能原因**：
- API Key 无效
- API 额度用完
- 网络连接问题

**解决**：
1. 访问 DeepSeek Dashboard：https://platform.deepseek.com/
2. 检查余额和 API Key
3. 如果需要，充值或重新生成 Key

### 问题 3：请求超时

**症状**：分析请求很久没有响应

**解决**：
- DeepSeek API 通常 5-10 秒响应
- 如果超过 30 秒，检查网络
- 查看 PythonAnywhere 白名单是否需要添加 `api.deepseek.com`

---

## 💰 DeepSeek 成本监控

### 查看使用情况

1. **访问 DeepSeek Dashboard**
   ```
   https://platform.deepseek.com/usage
   ```

2. **查看指标**：
   - 今日请求数
   - Token 使用量
   - 剩余额度

### 预算警报

**建议设置**：
- 每日消费限额：¥1
- 每月消费限额：¥10
- 低余额提醒：¥5

---

## 🌐 前端测试

### 测试真实 AI 分析

1. **访问你的前端**
   ```
   https://biasdetector.vercel.app
   ```

2. **上传测试 CSV**
   ```
   C:\Users\14593\CascadeProjects\circular-bias-detection\check-sleuth-ai\test_sample.csv
   ```

3. **查看分析结果**
   - 应该看到真实的 AI 分析
   - 不再是预设的 Demo 数据
   - 每次分析结果会略有不同

---

## 📈 性能优化

### 缓存策略（未来）

相同的 CSV 内容可以缓存结果：
- 减少 API 调用
- 降低成本
- 提升响应速度

### 限流策略（未来）

防止滥用：
- IP 限制：每 IP 每天 20 次
- 用户限制：每用户每天 50 次

---

## 🎉 完成确认

部署成功后，你应该能够：

- ✅ Health check 正常
- ✅ CSV 分析返回真实 AI 结果
- ✅ 日志显示 DeepSeek 成功
- ✅ `provider`: "deepseek"
- ✅ `isMock`: false

---

## 📝 下一步

### 立即可做

1. ✅ 测试多个 CSV 文件
2. ✅ 监控 DeepSeek 使用情况
3. ✅ 在前端体验真实分析

### 本周可做

1. 添加使用统计
2. 实现缓存策略
3. 添加用户自带 Key UI

### 下月可做

1. 用户认证系统
2. 订阅管理
3. Research 服务

---

## 🆘 需要帮助？

如果遇到问题：

1. **查看错误日志**
   - PythonAnywhere error log
   
2. **检查配置**
   - WSGI 文件的环境变量
   - 代码是否最新
   
3. **联系我**
   - 提供错误日志
   - 描述问题症状

---

**预计完成时间**：10 分钟

**成功标志**：返回真实 AI 分析，`provider: deepseek`

**立即开始吧！** 🚀
