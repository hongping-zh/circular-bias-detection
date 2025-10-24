# 📮 提交后跟进指南

## 🎯 提交后的第一个24小时

### ✅ 立即检查（提交后5分钟）

```markdown
1. [ ] PR成功创建？
   - 访问你的PR: https://github.com/sgl-project/sglang/pull/XXX
   - 确认标题和描述正确
   - 检查文件列表完整

2. [ ] CI开始运行？
   - 查看"Checks"标签
   - 确认CI jobs启动
   - 如果有红叉，准备修复

3. [ ] 通知设置正确？
   - GitHub: Settings → Notifications
   - 确保接收PR更新
   - 考虑启用邮件通知
```

### 📝 记录信息

创建一个跟踪文件:
```markdown
# PR跟踪

**PR编号**: #XXX
**提交日期**: 2024-10-24
**链接**: https://github.com/sgl-project/sglang/pull/XXX
**状态**: Open

## 时间线
- 2024-10-24: PR提交
- [日期]: [事件]

## 待办事项
- [ ] 响应初步评论
- [ ] 修复CI问题（如有）
- [ ] ...

## 笔记
- ...
```

---

## 🔍 前3天

### 每天检查

**早上** (9:00-10:00):
```markdown
1. 检查PR页面
   - 新评论？
   - CI状态？
   - 标签变化？

2. 阅读通知
   - GitHub通知
   - 邮件通知
   - 相关Discussions

3. 快速响应
   - 简单问题立即回答
   - 复杂问题记下待研究
```

**晚上** (21:00-22:00):
```markdown
1. 深度响应
   - 回复复杂评论
   - 推送代码修改
   - 更新文档

2. 记录进展
   - 更新跟踪文件
   - 记录关键决策
   - 计划明天任务
```

### CI失败处理

如果CI失败:

```bash
# 1. 查看CI日志
点击失败的check → Details → 查看日志

# 2. 本地复现
cd <sglang_path>
git pull origin main  # 确保最新
pytest test/srt/test_bias_audit.py -v

# 3. 修复问题
# (修改代码)

# 4. 测试修复
pytest test/srt/test_bias_audit.py -v

# 5. 推送修复
git add .
git commit -m "Fix CI: [简短描述问题]"
git push origin feature/circular-bias-detection
```

**常见CI问题**:
- ✅ 导入错误: 检查依赖
- ✅ 测试失败: 检查环境差异
- ✅ Linting错误: 运行 `flake8` 或 `black`
- ✅ 类型错误: 运行 `mypy`

---

## 💬 回应评论的最佳实践

### 回应模板

#### 1. 感谢反馈
```markdown
Thank you for the detailed review, @reviewer! I appreciate you taking 
the time to look at this.

I'll address your points:
1. [Point 1]: [Your response]
2. [Point 2]: [Your response]

I'll push the changes by [date].
```

#### 2. 请求澄清
```markdown
Thank you for the suggestion, @reviewer! 

I want to make sure I understand correctly: are you suggesting 
[interpretation A] or [interpretation B]?

Once I understand your preference, I'll implement it right away.
```

#### 3. 讨论设计选择
```markdown
Great question, @reviewer! 

The reason I chose [approach A] over [approach B] is:
1. [Reason 1]
2. [Reason 2]

However, I'm open to changing this if you think [approach B] would be 
better for the SGLang ecosystem. What do you think?
```

#### 4. 接受修改
```markdown
Excellent suggestion, @reviewer! You're absolutely right.

I'll make this change and will also:
- Update the tests
- Update the documentation
- Add a note in the docstring

ETA: [1-2 days]
```

#### 5. 解释已有功能
```markdown
Thanks for bringing this up, @reviewer!

Actually, this is already handled in [file:line]. Specifically:
[explanation]

But I agree the documentation could be clearer. I'll add more 
explanation in [location].
```

### ⚠️ 避免的回应

❌ **防御性**:
```markdown
# 不要这样
"This is already documented in the code."
"Other projects do it this way."
"This is not a real problem."
```

❌ **忽略反馈**:
```markdown
# 不要这样
（不回复）
（只说"OK"没有行动）
（争论而不解决）
```

❌ **过度道歉**:
```markdown
# 不要这样
"I'm so sorry, I should have known better..."
"This is probably a stupid question, but..."
（过度道歉显得不专业）
```

✅ **正确方式**:
- 专业、友好、建设性
- 感谢反馈
- 清楚解释或快速修复
- 设置明确的时间预期

---

## 📊 第一周目标

### 优先级清单

**P0 - 必须立即处理**:
- [ ] CI失败
- [ ] 重大bug报告
- [ ] 维护者的直接问题

**P1 - 24小时内处理**:
- [ ] 代码审查评论
- [ ] 文档问题
- [ ] 测试建议

**P2 - 48小时内处理**:
- [ ] API设计讨论
- [ ] 性能问题
- [ ] 扩展功能建议

**P3 - 1周内处理**:
- [ ] 一般性讨论
- [ ] 未来功能想法
- [ ] 文档完善

---

## 🔄 常见审查要求

### 1. 代码风格

**问题**: "Can you run `black` on this?"

**响应**:
```bash
pip install black
cd <sglang_path>
black python/sglang/lang/bias_audit.py
black test/srt/test_bias_audit.py

git add .
git commit -m "Apply black formatting"
git push
```

### 2. 类型检查

**问题**: "Can you add type hints?"

**响应**:
```python
# 检查现有类型
mypy python/sglang/lang/bias_audit.py

# 修复问题并推送
```

### 3. 文档扩展

**问题**: "Can you add more examples?"

**响应**:
```markdown
Sure! I'll add:
1. Example for [scenario A]
2. Example for [scenario B]
3. More inline code comments

ETA: Tomorrow
```

### 4. 测试覆盖

**问题**: "Can you test [edge case]?"

**响应**:
```python
# 添加新测试
def test_edge_case_xxx():
    """Test [description]."""
    # ...

# 确保通过
pytest test/srt/test_bias_audit.py::test_edge_case_xxx -v
```

### 5. 性能优化

**问题**: "This seems slow, can you optimize?"

**响应**:
```markdown
Good catch! I'll profile this and optimize.

Current benchmark: [X]ms
Target: [Y]ms

Will update with results.
```

---

## 📈 审查阶段

### 阶段1: 初步审查 (第1-2周)

**特征**:
- 维护者首次查看
- 高层次反馈
- CI检查
- 代码风格检查

**你应该做**:
- ✅ 快速响应
- ✅ 修复CI问题
- ✅ 回答设计问题
- ✅ 保持积极态度

### 阶段2: 详细审查 (第3-6周)

**特征**:
- 逐行代码审查
- API设计讨论
- 测试覆盖讨论
- 文档完善要求

**你应该做**:
- ✅ 认真对待每条评论
- ✅ 提供详细解释
- ✅ 进行必要修改
- ✅ 记录重大决策

### 阶段3: 最终调整 (第7-10周)

**特征**:
- 最后的小修改
- 文档最终检查
- 等待合并窗口

**你应该做**:
- ✅ 保持耐心
- ✅ 快速响应小改动
- ✅ 准备发布说明
- ✅ 感谢所有人

---

## 🎯 成功指标

### 积极信号 ✅

1. **获得👍或❤️**: 社区认可
2. **被标记为"approved"**: 维护者同意
3. **被添加到milestone**: 计划合并
4. **讨论减少**: 问题已解决
5. **维护者说"LGTM"**: 看起来不错

### 需要注意的信号 ⚠️

1. **长时间无响应**: 可能需要友好提醒
2. **反复修改同一地方**: 可能需要重新设计
3. **被标记为"needs work"**: 需要显著改进
4. **讨论偏离主题**: 需要重新聚焦

### 可能被关闭的信号 ❌

1. **被标记为"wont-fix"**: 不符合项目方向
2. **维护者说"out of scope"**: 范围太大
3. **长期无进展**: 需要重新激活
4. **功能重复**: 已有类似功能

**如果看到这些信号**:
- 礼貌询问原因
- 考虑缩小范围
- 或者接受决定，发布为插件

---

## 🔄 长期跟进 (2-3个月)

### 每周检查

**周一**:
- 回顾上周进展
- 计划本周任务
- 检查PR状态

**周五**:
- 完成pending任务
- 回复所有评论
- 记录周总结

### 月度回顾

每月创建一个总结:
```markdown
## Month X Review

### Progress
- [x] Task 1
- [x] Task 2
- [ ] Task 3 (ongoing)

### Challenges
- Challenge 1: [how addressed]
- Challenge 2: [ongoing]

### Next Month
- Goal 1
- Goal 2

### Notes
- ...
```

---

## 🎓 更新JOSS论文

### 在审查期间

向JOSS审稿人发送更新:

```markdown
Dear Reviewers,

I wanted to share an update on the practical adoption of our framework.

I've submitted a pull request to SGLang (Stanford LMSYS LLM serving system):
- PR: https://github.com/sgl-project/sglang/pull/XXX
- Status: Under review by SGLang maintainers
- Feedback: [Positive / Under discussion]

This demonstrates the framework's practical applicability and potential 
for adoption in production systems.

Best regards,
[Your name]
```

### PR被接受后

更新JOSS论文的"Statement of Need"部分:

```markdown
**Community Adoption**: The framework has been integrated into SGLang, 
a leading LLM serving system from Stanford LMSYS:
- Pull Request: https://github.com/sgl-project/sglang/pull/XXX
- Merged in: v0.X.X (released YYYY-MM-DD)
- Impact: Available to SGLang's user base

This integration validates the practical utility and demonstrates 
real-world applicability of our approach.
```

---

## 🎉 PR被接受后

### 庆祝！🎊

1. **感谢所有人**:
```markdown
Thank you so much to everyone who reviewed this PR! Special thanks to 
@maintainer1, @maintainer2, and the entire SGLang community for the 
valuable feedback and patience throughout the review process.

I'm excited to see this feature help the community detect evaluation 
biases and improve LLM assessment practices!
```

2. **分享成功**:
   - 在Twitter/X上分享
   - 在LinkedIn更新
   - 告诉你的同事/导师
   - 更新你的简历

3. **后续工作**:
   - 监控bug报告
   - 准备后续改进
   - 帮助用户使用
   - 考虑写博客文章

---

## 📝 经验教训记录

创建一个文件记录学到的东西:

```markdown
# PR #XXX 经验教训

## 做得好的
1. [What worked well]
2. [What worked well]

## 可以改进的
1. [What could be better]
2. [What could be better]

## 下次会做的
1. [Future approach]
2. [Future approach]

## 关键见解
- Insight 1
- Insight 2
```

---

## 🆘 如果PR被关闭

### 不要灰心！

**这很正常**:
- 很多优秀的PR被关闭
- 不代表你的工作不好
- 可能只是时机或范围问题

### 建设性响应

```markdown
Thank you for considering this PR and for the valuable feedback 
throughout the review process.

I understand the decision and respect the project's direction. 
I learned a lot from this experience.

I'll explore publishing this as a standalone plugin so users who 
need this functionality can still benefit from it.

Thanks again for your time!
```

### Plan B: 独立插件

1. **创建新仓库**:
   - `sglang-bias-detection`
   - 作为独立PyPI包发布

2. **文档**:
   - 如何与SGLang集成
   - 安装指南
   - 使用示例

3. **推广**:
   - 在SGLang Discussion分享
   - 在JOSS论文中引用
   - 写博客文章

4. **价值**:
   - 仍然有用
   - 仍然是贡献
   - 仍然展示能力

---

## 📞 需要帮助时

### SGLang资源
- Discussions: https://github.com/sgl-project/sglang/discussions
- Issues: https://github.com/sgl-project/sglang/issues
- Discord/Slack: [链接如果有]

### 一般资源
- GitHub Docs: https://docs.github.com
- Open Source Guide: https://opensource.guide

### 保持健康

- 🧘 不要过度检查PR (每天2-3次足够)
- 😊 保持积极心态
- 💪 接受建设性批评
- ⏰ 给自己和他人时间
- 🎯 记住长期目标

---

**🎉 你已经迈出了重要一步！**

无论结果如何，这都是:
- ✅ 学习经验
- ✅ 技能证明
- ✅ 社区贡献
- ✅ 职业发展

**保持耐心，保持专业，享受过程！** 🚀
