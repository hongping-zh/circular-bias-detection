# PythonAnywhere 部署完整指南

## 🎯 为什么选择 PythonAnywhere

- ✅ **完全免费**（不需要信用卡）
- ✅ **Python 专用平台**（无依赖问题）
- ✅ **稳定可靠**（运营多年）
- ✅ **简单配置**（10-15 分钟）

---

## 📋 免费层限制

**可用资源**：
- ✅ 512MB 存储空间
- ✅ 1 个 Web 应用
- ✅ 每天自动重启
- ⚠️ CPU 时间：100 秒/天
- ⚠️ 只能访问白名单外部 API

**适合场景**：
- MVP 测试
- 个人项目
- 学习实验

---

## 🚀 部署步骤

### 第一步：注册账号

1. **访问 PythonAnywhere**：
   ```
   https://www.pythonanywhere.com/
   ```

2. **点击 "Start running Python online in less than a minute!"**

3. **选择 "Beginner" 计划**（免费）

4. **填写注册信息**：
   - Username（用户名）- 记住这个，后续要用！
   - Email
   - Password

5. **确认邮箱**

---

### 第二步：上传代码

#### 方法 A：使用 Git（推荐）

1. **打开 Bash Console**：
   - Dashboard → "New Console" → "Bash"

2. **克隆仓库**：
   ```bash
   git clone https://github.com/hongping-zh/circular-bias-detection.git
   cd circular-bias-detection/backend
   ```

3. **检查文件**：
   ```bash
   ls -la
   ```
   应该看到 `app.py`, `requirements.txt` 等文件

#### 方法 B：手动上传

1. **打开 Files 页面**：
   - Dashboard → Files

2. **创建目录**：
   ```
   /home/你的用户名/circular-bias-detection/backend
   ```

3. **上传文件**：
   - 点击 "Upload a file"
   - 上传 `backend` 文件夹中的所有文件

---

### 第三步：创建虚拟环境

在 Bash Console 中：

```bash
# 进入项目目录
cd ~/circular-bias-detection/backend

# 创建虚拟环境
python3.9 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装依赖（这可能需要几分钟）
pip install -r requirements.txt
```

**注意**：安装过程可能需要 3-5 分钟，请耐心等待。

---

### 第四步：配置 Web 应用

1. **打开 Web 页面**：
   - Dashboard → Web

2. **点击 "Add a new web app"**

3. **选择 Python 版本**：
   - 点击 "Next"
   - 选择 "Manual configuration"
   - 选择 "Python 3.9"
   - 点击 "Next"

4. **配置完成**

---

### 第五步：配置 WSGI 文件

1. **在 Web 页面找到 "Code" 部分**

2. **点击 WSGI configuration file 链接**：
   - 类似：`/var/www/你的用户名_pythonanywhere_com_wsgi.py`

3. **删除所有内容，替换为**：

```python
import sys
import os

# 添加项目路径（修改为你的用户名）
project_home = '/home/你的用户名/circular-bias-detection/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 激活虚拟环境
activate_this = '/home/你的用户名/circular-bias-detection/backend/venv/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# 导入 Flask 应用
from app import app as application

# 设置环境变量（可选）
os.environ['FLASK_ENV'] = 'production'
```

**重要**：将 `你的用户名` 替换为你的 PythonAnywhere 用户名！

4. **点击 "Save"**

---

### 第六步：配置虚拟环境路径

1. **在 Web 页面找到 "Virtualenv" 部分**

2. **输入虚拟环境路径**：
   ```
   /home/你的用户名/circular-bias-detection/backend/venv
   ```

3. **点击勾选标记保存**

---

### 第七步：配置静态文件（可选）

如果你的 Flask 应用有静态文件：

1. **在 "Static files" 部分**
2. **添加映射**：
   - URL: `/static/`
   - Directory: `/home/你的用户名/circular-bias-detection/backend/static`

---

### 第八步：启动应用

1. **滚动到页面顶部**

2. **点击绿色的 "Reload" 按钮**

3. **等待重新加载**（约 10-20 秒）

---

### 第九步：测试应用

1. **你的应用 URL**：
   ```
   https://你的用户名.pythonanywhere.com
   ```

2. **测试 Health Check**：
   ```
   https://你的用户名.pythonanywhere.com/health
   ```

3. **预期响应**：
   ```json
   {
     "status": "ok",
     "service": "Sleuth Bias Detection API",
     "version": "1.0.0"
   }
   ```

✅ 如果看到这个，部署成功！

---

## 🔧 故障排查

### 问题 1：网站显示 "Something went wrong"

**查看错误日志**：
1. Web 页面 → "Log files"
2. 点击 "Error log"
3. 查看最新错误

**常见原因**：
- WSGI 配置错误
- 虚拟环境路径错误
- 依赖未安装

---

### 问题 2：依赖安装失败

**检查 CPU 时间**：
- Dashboard → Account
- 查看 "CPU seconds today"

如果超过限制：
- 等到第二天（UTC 时间重置）
- 或移除不必要的依赖

**简化 requirements.txt**：
```
flask==3.0.0
flask-cors==4.0.0
pandas==2.0.3
numpy==1.24.4
google-generativeai==0.3.2
requests==2.31.0
```

---

### 问题 3：外部 API 访问被阻止

**症状**：无法访问 Gemini API

**解决**：
1. 在 PythonAnywhere 论坛申请白名单
2. 或使用 Demo 模式

**申请白名单**：
- 访问：https://www.pythonanywhere.com/forums/
- 发帖请求添加：`generativelanguage.googleapis.com`

---

### 问题 4：每天自动重启

**免费层特性**：
- 每天 UTC 00:00 自动重启
- 首次访问可能慢

**无法避免**，这是免费层限制。

---

## 🔐 环境变量配置

### 添加环境变量

**方法 1：在 WSGI 文件中**：
```python
os.environ['GEMINI_API_KEY'] = 'your-api-key-here'
os.environ['FLASK_ENV'] = 'production'
```

**方法 2：在 Bash Console 中**：
```bash
# 编辑 ~/.bashrc
nano ~/.bashrc

# 添加：
export GEMINI_API_KEY='your-api-key-here'

# 保存并重新加载
source ~/.bashrc
```

---

## 📊 监控和维护

### 查看日志

**Access Log**（访问日志）：
- Web → Log files → Access log
- 查看所有请求

**Error Log**（错误日志）：
- Web → Log files → Error log
- 查看错误信息

**Server Log**（服务器日志）：
- Web → Log files → Server log
- 查看启动信息

---

### 更新代码

**使用 Git**：
```bash
# 打开 Bash Console
cd ~/circular-bias-detection/backend
git pull origin main

# 重新加载
# 去 Web 页面点击 "Reload"
```

**手动上传**：
- Files 页面
- 上传更新的文件
- Web 页面点击 "Reload"

---

## 💰 成本说明

### 免费层（Beginner）

- **价格**: $0/月
- **存储**: 512MB
- **Web 应用**: 1 个
- **CPU 时间**: 100 秒/天
- **限制**: 
  - 每天重启
  - 白名单外部 API
  - 无自定义域名

### 付费层（Hacker）

- **价格**: $5/月
- **存储**: 1GB
- **Web 应用**: 2 个
- **CPU 时间**: 1000 秒/天
- **优势**:
  - 所有外部 API
  - 自定义域名
  - 无每日重启

---

## 🔗 连接前端

### 更新前端 API URL

**编辑前端代码**（本地）：

1. **找到 API 配置**（如果有专门的配置文件）
2. **或在调用 API 的地方更新 URL**：
   ```typescript
   const API_BASE_URL = 'https://你的用户名.pythonanywhere.com';
   ```

3. **重新部署前端**：
   ```powershell
   cd check-sleuth-ai
   vercel --prod
   ```

---

## ⚡ 性能优化

### 1. 启用 Gzip 压缩

在 `app.py` 添加：
```python
from flask_compress import Compress

app = Flask(__name__)
Compress(app)
```

在 `requirements.txt` 添加：
```
flask-compress==1.14
```

### 2. 添加缓存

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_function(data):
    # 你的逻辑
    pass
```

### 3. 减少依赖

只安装必要的包，减少加载时间。

---

## 📝 部署检查清单

- [ ] PythonAnywhere 账号已创建
- [ ] 用户名已记录：___________
- [ ] 代码已上传
- [ ] 虚拟环境已创建
- [ ] 依赖已安装
- [ ] Web 应用已配置
- [ ] WSGI 文件已修改
- [ ] 虚拟环境路径已设置
- [ ] 应用已 Reload
- [ ] Health check 返回 200
- [ ] 前端 API URL 已更新
- [ ] 前端已重新部署
- [ ] 端到端测试通过

---

## 🎉 部署完成

你现在有：
- ✅ 前端在 Vercel：https://biasdetector-xxx.vercel.app
- ✅ 后端在 PythonAnywhere：https://你的用户名.pythonanywhere.com
- ✅ 完全免费的完整系统
- ✅ 无需信用卡

---

## 📞 获取帮助

- **PythonAnywhere 帮助**: https://help.pythonanywhere.com/
- **论坛**: https://www.pythonanywhere.com/forums/
- **邮件支持**: support@pythonanywhere.com

---

## 🚀 下一步

1. ✅ 测试所有 API 端点
2. ✅ 监控错误日志
3. ✅ 优化性能
4. 考虑付费升级（$5/月）以获得：
   - 无限外部 API 访问
   - 更多 CPU 时间
   - 无每日重启
   - 自定义域名

---

**恭喜！你的应用已完整部署！** 🎉

**前端**: https://biasdetector-xxx.vercel.app  
**后端**: https://你的用户名.pythonanywhere.com

---

**部署日期**: ___________  
**用户名**: ___________  
**状态**: [ ] 完成
