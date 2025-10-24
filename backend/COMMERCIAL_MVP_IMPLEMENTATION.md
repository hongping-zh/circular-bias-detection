# 🚀 商用 MVP 快速实现方案

## 🎯 目标

**30 天内**将现有系统升级为可付费的 API 服务

**验证指标**: 5 个付费用户 = 盈亏平衡点

---

## 📋 完整架构对比

### 当前架构（开发模式）

```
前端 Web App (is.gd/check_sleuth)
       ↓
Flask API (localhost:5000)
       ↓
Zenodo Dataset
```

### 目标架构（商用模式）

```
┌─────────────────────────────────────────────┐
│  前端层                                     │
│  • Web App (免费用户)                       │
│  • 用户 Dashboard                           │
└──────────────┬──────────────────────────────┘
               │ HTTPS + API Key
┌──────────────┴──────────────────────────────┐
│  API Gateway                                 │
│  • API 认证 (API Key)                       │
│  • 速率限制 (Plan-based)                    │
│  • 使用统计                                 │
└──────────────┬──────────────────────────────┘
               │
┌──────────────┴──────────────────────────────┐
│  Flask API (Production)                      │
│  • 偏差检测                                 │
│  • Zenodo 集成                              │
│  • Redis 缓存                               │
└──────────────┬──────────────────────────────┘
               │
┌──────────────┴──────────────────────────────┐
│  数据层                                      │
│  • PostgreSQL (用户/订阅)                   │
│  • Redis (缓存)                             │
│  • S3 (文件存储)                            │
└─────────────────────────────────────────────┘
```

---

## 📦 实现步骤（30 天计划）

### Week 1: 用户系统 + API 认证

#### 1.1 数据库模型

```python
# backend/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import secrets
import hashlib

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    plan = db.Column(db.String(20), default='free')  # free, pro, business, enterprise
    stripe_customer_id = db.Column(db.String(100))
    stripe_subscription_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    api_keys = db.relationship('APIKey', backref='user', lazy=True)
    usage_records = db.relationship('Usage', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'


class APIKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100))  # 用户自定义名称
    key_hash = db.Column(db.String(256), unique=True, nullable=False)
    key_prefix = db.Column(db.String(20))  # 显示前缀，如 "sk_live_abc..."
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime)
    
    @staticmethod
    def generate_key():
        """生成 API Key"""
        key = f"sk_live_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        key_prefix = f"{key[:15]}..."
        return key, key_hash, key_prefix
    
    def __repr__(self):
        return f'<APIKey {self.key_prefix}>'


class Usage(db.Model):
    __tablename__ = 'usage'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    api_key_id = db.Column(db.Integer, db.ForeignKey('api_keys.id'))
    endpoint = db.Column(db.String(100))
    method = db.Column(db.String(10))
    status_code = db.Column(db.Integer)
    processing_time = db.Column(db.Float)  # 秒
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Usage {self.endpoint} at {self.timestamp}>'


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan = db.Column(db.String(20))  # free, pro, business, enterprise
    status = db.Column(db.String(20))  # active, canceled, expired
    current_period_start = db.Column(db.DateTime)
    current_period_end = db.Column(db.DateTime)
    cancel_at_period_end = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

#### 1.2 认证中间件

```python
# backend/auth/middleware.py
from functools import wraps
from flask import request, jsonify, g
from models import APIKey, User
import hashlib

def require_api_key(f):
    """API Key 认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not api_key:
            return jsonify({
                'error': 'Missing API key',
                'message': 'Please provide an API key in X-API-Key header'
            }), 401
        
        # 验证 API Key
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        api_key_obj = APIKey.query.filter_by(key_hash=key_hash, is_active=True).first()
        
        if not api_key_obj:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is invalid or has been revoked'
            }), 401
        
        # 加载用户信息
        user = User.query.get(api_key_obj.user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        # 存储在请求上下文
        g.user = user
        g.api_key = api_key_obj
        
        # 更新最后使用时间
        api_key_obj.last_used_at = datetime.utcnow()
        db.session.commit()
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_plan(min_plan='free'):
    """计划等级检查装饰器"""
    plan_hierarchy = {'free': 0, 'pro': 1, 'business': 2, 'enterprise': 3}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'user'):
                return jsonify({'error': 'Authentication required'}), 401
            
            user_plan_level = plan_hierarchy.get(g.user.plan, 0)
            required_level = plan_hierarchy.get(min_plan, 0)
            
            if user_plan_level < required_level:
                return jsonify({
                    'error': 'Plan upgrade required',
                    'message': f'This feature requires {min_plan} plan or higher',
                    'current_plan': g.user.plan
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
```

#### 1.3 速率限制

```python
# backend/auth/rate_limit.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import g

# 不同计划的速率限制
RATE_LIMITS = {
    'free': {
        'per_minute': '10 per minute',
        'per_day': '100 per day'
    },
    'pro': {
        'per_minute': '60 per minute',
        'per_day': '1000 per day'
    },
    'business': {
        'per_minute': '300 per minute',
        'per_day': '10000 per day'
    },
    'enterprise': {
        'per_minute': '1000 per minute',
        'per_day': 'unlimited'
    }
}

def get_api_key():
    """获取当前用户的 API Key 用于速率限制"""
    return g.get('user', {}).email if hasattr(g, 'user') else get_remote_address()

limiter = Limiter(
    key_func=get_api_key,
    storage_uri="redis://localhost:6379"
)

def get_rate_limit_for_user():
    """根据用户计划返回速率限制"""
    if hasattr(g, 'user'):
        return RATE_LIMITS.get(g.user.plan, RATE_LIMITS['free'])
    return RATE_LIMITS['free']
```

---

### Week 2: Stripe 支付集成

#### 2.1 配置 Stripe

```python
# backend/billing/stripe_config.py
import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# 定价 (使用 Stripe Price IDs)
PLANS = {
    'pro': {
        'name': 'Professional',
        'price': 49,
        'stripe_price_id': 'price_xxx',  # 从 Stripe Dashboard 获取
        'features': [
            '1,000 analyses per month',
            'API access',
            'Email support',
            'Standard cache'
        ]
    },
    'business': {
        'name': 'Business',
        'price': 299,
        'stripe_price_id': 'price_yyy',
        'features': [
            '10,000 analyses per month',
            'Priority API access',
            'Priority support',
            'Advanced cache',
            'Custom integrations'
        ]
    }
}
```

#### 2.2 创建订阅

```python
# backend/billing/subscription.py
import stripe
from models import User, Subscription

def create_checkout_session(user, plan):
    """创建 Stripe Checkout 会话"""
    try:
        session = stripe.checkout.Session.create(
            customer_email=user.email,
            payment_method_types=['card'],
            line_items=[{
                'price': PLANS[plan]['stripe_price_id'],
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f"{os.getenv('FRONTEND_URL')}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/pricing",
            client_reference_id=str(user.id),
            metadata={
                'user_id': user.id,
                'plan': plan
            }
        )
        return session.url
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return None


def handle_webhook(payload, sig_header):
    """处理 Stripe Webhook 事件"""
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
    except Exception as e:
        return {'error': str(e)}, 400
    
    # 处理不同事件
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_canceled(subscription)
    
    return {'status': 'success'}, 200


def handle_successful_payment(session):
    """处理支付成功"""
    user_id = session['metadata']['user_id']
    plan = session['metadata']['plan']
    
    user = User.query.get(user_id)
    user.plan = plan
    user.stripe_customer_id = session['customer']
    user.stripe_subscription_id = session['subscription']
    
    # 创建订阅记录
    subscription = Subscription(
        user_id=user.id,
        plan=plan,
        status='active'
    )
    db.session.add(subscription)
    db.session.commit()
```

---

### Week 3: 用户 Dashboard

#### 3.1 后端 API 端点

```python
# backend/api/dashboard.py
from flask import Blueprint, jsonify, request
from auth.middleware import require_api_key
from models import User, APIKey, Usage
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
@require_api_key
def get_stats():
    """获取用户统计数据"""
    user = g.user
    
    # 本月使用量
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
    monthly_usage = Usage.query.filter(
        Usage.user_id == user.id,
        Usage.timestamp >= month_start
    ).count()
    
    # 总使用量
    total_usage = Usage.query.filter_by(user_id=user.id).count()
    
    # 最近 30 天趋势
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    daily_usage = db.session.query(
        db.func.date(Usage.timestamp).label('date'),
        db.func.count(Usage.id).label('count')
    ).filter(
        Usage.user_id == user.id,
        Usage.timestamp >= thirty_days_ago
    ).group_by('date').all()
    
    return jsonify({
        'plan': user.plan,
        'usage': {
            'monthly': monthly_usage,
            'total': total_usage,
            'daily_trend': [{'date': str(d.date), 'count': d.count} for d in daily_usage]
        }
    })


@dashboard_bp.route('/api/dashboard/keys', methods=['GET'])
@require_api_key
def list_api_keys():
    """列出用户的 API Keys"""
    keys = APIKey.query.filter_by(user_id=g.user.id).all()
    return jsonify({
        'keys': [{
            'id': k.id,
            'name': k.name,
            'prefix': k.key_prefix,
            'created_at': k.created_at.isoformat(),
            'last_used_at': k.last_used_at.isoformat() if k.last_used_at else None,
            'is_active': k.is_active
        } for k in keys]
    })


@dashboard_bp.route('/api/dashboard/keys', methods=['POST'])
@require_api_key
def create_api_key():
    """创建新的 API Key"""
    data = request.get_json()
    name = data.get('name', 'My API Key')
    
    # 生成 Key
    key, key_hash, key_prefix = APIKey.generate_key()
    
    api_key = APIKey(
        user_id=g.user.id,
        name=name,
        key_hash=key_hash,
        key_prefix=key_prefix
    )
    db.session.add(api_key)
    db.session.commit()
    
    return jsonify({
        'key': key,  # 只在创建时返回完整 Key
        'id': api_key.id,
        'name': api_key.name,
        'prefix': api_key.key_prefix,
        'warning': 'Please save this key. It will not be shown again.'
    }), 201


@dashboard_bp.route('/api/dashboard/keys/<int:key_id>', methods=['DELETE'])
@require_api_key
def revoke_api_key(key_id):
    """撤销 API Key"""
    api_key = APIKey.query.filter_by(id=key_id, user_id=g.user.id).first()
    
    if not api_key:
        return jsonify({'error': 'API key not found'}), 404
    
    api_key.is_active = False
    db.session.commit()
    
    return jsonify({'status': 'revoked'})
```

#### 3.2 前端 Dashboard (React)

```jsx
// dashboard/src/components/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [apiKeys, setApiKeys] = useState([]);
  
  useEffect(() => {
    fetchStats();
    fetchApiKeys();
  }, []);
  
  const fetchStats = async () => {
    const response = await fetch('/api/dashboard/stats', {
      headers: { 'X-API-Key': localStorage.getItem('api_key') }
    });
    const data = await response.json();
    setStats(data);
  };
  
  const fetchApiKeys = async () => {
    const response = await fetch('/api/dashboard/keys', {
      headers: { 'X-API-Key': localStorage.getItem('api_key') }
    });
    const data = await response.json();
    setApiKeys(data.keys);
  };
  
  const createApiKey = async () => {
    const name = prompt('Enter a name for this API key:');
    if (!name) return;
    
    const response = await fetch('/api/dashboard/keys', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': localStorage.getItem('api_key')
      },
      body: JSON.stringify({ name })
    });
    
    const data = await response.json();
    alert(`New API Key created!\n\n${data.key}\n\nPlease save it now.`);
    fetchApiKeys();
  };
  
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      {/* 使用统计 */}
      <div className="stats-card">
        <h2>Usage This Month</h2>
        <div className="stat-value">{stats?.usage.monthly || 0}</div>
        <div className="stat-label">API Calls</div>
        
        <h3>30-Day Trend</h3>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={stats?.usage.daily_trend || []}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="count" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      
      {/* API Keys */}
      <div className="keys-card">
        <h2>API Keys</h2>
        <button onClick={createApiKey}>Create New Key</button>
        
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Key</th>
              <th>Created</th>
              <th>Last Used</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {apiKeys.map(key => (
              <tr key={key.id}>
                <td>{key.name}</td>
                <td><code>{key.prefix}</code></td>
                <td>{new Date(key.created_at).toLocaleDateString()}</td>
                <td>{key.last_used_at ? new Date(key.last_used_at).toLocaleDateString() : 'Never'}</td>
                <td>
                  <button onClick={() => revokeKey(key.id)}>Revoke</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;
```

---

### Week 4: 部署和上线

#### 4.1 Docker 容器化

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 运行
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### 4.2 docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/sleuth
      - REDIS_URL=redis://redis:6379
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
      - STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET}
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: sleuth
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

#### 4.3 部署到云端 (AWS)

```bash
# 使用 AWS EB CLI
eb init -p python-3.11 sleuth-api
eb create sleuth-production
eb deploy
```

---

## 💰 定价页面

```html
<!-- pricing.html -->
<div class="pricing">
  <div class="plan">
    <h3>Free</h3>
    <div class="price">$0<span>/mo</span></div>
    <ul>
      <li>100 analyses/month</li>
      <li>API access</li>
      <li>Community support</li>
    </ul>
    <button>Start Free</button>
  </div>
  
  <div class="plan featured">
    <h3>Pro</h3>
    <div class="price">$49<span>/mo</span></div>
    <ul>
      <li>1,000 analyses/month</li>
      <li>Priority API</li>
      <li>Email support</li>
      <li>Advanced features</li>
    </ul>
    <button>Subscribe</button>
  </div>
  
  <div class="plan">
    <h3>Business</h3>
    <div class="price">$299<span>/mo</span></div>
    <ul>
      <li>10,000 analyses/month</li>
      <li>Premium support</li>
      <li>Custom integrations</li>
      <li>SLA guarantee</li>
    </ul>
    <button>Subscribe</button>
  </div>
</div>
```

---

## 📊 成功指标

### 技术指标
- [ ] API 响应时间 < 2s (p95)
- [ ] 可用性 > 99.5%
- [ ] 零安全漏洞

### 业务指标
- [ ] 30 天内 5 个付费用户
- [ ] MRR (月经常性收入) > $200
- [ ] Churn rate < 10%

---

## 🚀 下一步

1. **本周**: 实现用户系统和 API 认证
2. **下周**: 集成 Stripe 支付
3. **第三周**: 构建 Dashboard
4. **第四周**: 部署上线

**我可以帮您逐步实现每个部分！从哪里开始？**
