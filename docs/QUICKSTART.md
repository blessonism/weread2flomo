# 快速开始指南

## 📋 准备工作清单

- [ ] 微信读书账号（有划线笔记）
- [ ] flomo PRO 账号（或试用版）
- [ ] Python 3.8+ 环境

## 🚀 5分钟快速上手

### 步骤1：获取微信读书 Cookie

1. 在浏览器中访问 https://weread.qq.com/
2. 登录你的微信读书账号
3. 按 `F12` 打开开发者工具
4. 切换到 `Application` 或 `存储` 标签
5. 找到 `Cookies` → `https://weread.qq.com`
6. 复制所有 Cookie 值，格式类似：
   ```
   wr_vid=xxxxx; wr_skey=xxxxx; wr_gid=xxxxx
   ```

**提示**：完整的 Cookie 字符串很长，确保复制完整！

### 步骤2：获取 flomo API

1. 登录 flomo 网页版
2. 点击右上角头像 → `设置`
3. 找到 `API` 标签
4. 复制 `你的专属记录 API`，格式类似：
   ```
   https://flomoapp.com/iwh/xxxxxxxxxx/
   ```

**注意**：API 地址需要保密，不要分享给他人！

### 步骤3：配置环境变量

在项目根目录创建 `.env` 文件：

```bash
# 必填配置
WEREAD_COOKIE="粘贴你的微信读书Cookie"
FLOMO_API="粘贴你的flomo API地址"

# 可选配置（如果需要AI标签）
# AI_API_KEY="your_api_key"
# AI_API_BASE="https://api.openai.com/v1"
```

### 步骤4：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤5：测试连接

#### 测试1：配置文件
```bash
python config_manager.py
```

应该看到：
```
=== 配置管理器测试 ===

天数限制: 7
默认模板: simple
启用AI标签: False
...
```

#### 测试2：微信读书连接
```bash
python weread_api.py
```

应该看到：
```
获取到 X 本书

书名: 《某本书》
作者: 某作者
划线数量: X
```

如果报错 "没有找到 Cookie"，检查 `.env` 文件配置。

#### 测试3：flomo 连接（谨慎）
```bash
python flomo_client.py
```

这会向 flomo 发送一条测试笔记！如果不想测试可以跳过。

### 步骤6：运行同步（小范围测试）

首先，编辑 `config.yaml` 限制同步数量：

```yaml
sync:
  days_limit: 1  # 只同步昨天的划线
  max_highlights_per_sync: 5  # 最多5条
```

然后运行：

```bash
python sync.py
```

### 步骤7：检查 flomo

打开 flomo App 或网页版，检查是否有新笔记！

## 🎯 测试建议

### 第一次测试（保守）
```yaml
sync:
  days_limit: 1  # 只同步1天
  max_highlights_per_sync: 3  # 只同步3条
```

### 第二次测试（适中）
```yaml
sync:
  days_limit: 7  # 同步最近7天
  max_highlights_per_sync: 20  # 同步20条
```

### 正式使用（全量）
```yaml
sync:
  days_limit: 0  # 同步所有
  max_highlights_per_sync: 50  # 单次最多50条
```

## 🐛 常见问题排查

### 问题1：获取不到书籍
```
❌ 没有找到任何书籍
```

**解决方案**：
1. 检查 Cookie 是否正确
2. 重新登录微信读书获取新 Cookie
3. 确保微信读书账号有笔记本

### 问题2：flomo 发送失败
```
✗ 发送失败: 401 - Unauthorized
```

**解决方案**：
1. 检查 flomo API 地址是否正确
2. 确保 API 地址以 `/` 结尾
3. 检查是否有 PRO 权限

### 问题3：达到每日限制
```
⚠️ 已达到 flomo 每日API调用限制
```

**解决方案**：
- 这是正常的，flomo 限制 100次/天
- 明天自动重置
- 可以调整 `max_highlights_per_sync` 控制数量

### 问题4：没有安装 PyYAML
```
ModuleNotFoundError: No module named 'yaml'
```

**解决方案**：
```bash
pip install pyyaml
```

## 📝 测试检查清单

完成以下测试表示配置成功：

- [ ] 配置管理器测试通过
- [ ] 微信读书 API 能获取书籍列表
- [ ] flomo API 能发送测试笔记（可选）
- [ ] 完整同步至少成功1条划线
- [ ] 在 flomo 中看到了同步的笔记

## 🎨 下一步

配置成功后，你可以：

1. **调整模板**：编辑 `config.yaml` 选择喜欢的模板
2. **启用 AI 标签**：配置 AI API 后设置 `enable_ai_tags: true`
3. **自定义分类**：在 `book_categories` 添加自己的分类
4. **部署自动化**：推送到 GitHub 启用 Actions

## 💡 使用技巧

### 技巧1：查看同步记录
```bash
cat synced_bookmarks.json
```

可以看到已同步的划线 ID 列表。

### 技巧2：重新同步
如果想重新同步某本书的划线：
```bash
# 删除同步记录
rm synced_bookmarks.json
# 重新运行
python sync.py
```

### 技巧3：测试不同模板
修改 `config.yaml`:
```yaml
default_template: detailed  # 改成 simple/standard/detailed
```

然后重新同步查看效果。

## 🆘 需要帮助？

如果遇到问题：
1. 检查 `.env` 文件配置
2. 查看详细错误信息
3. 阅读 README.md 的常见问题部分
4. 在 GitHub 提交 Issue
