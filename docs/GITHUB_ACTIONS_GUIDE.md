# 🤖 GitHub Actions 自动同步指南

让你的微信读书笔记每天自动同步到 Flomo，无需自己运行脚本！

---

## 📋 前置准备

确保你已经：

- [x] 有 GitHub 账号
- [x] Fork 了本项目到你的账号
- [x] 有 Flomo API（从 [Flomo 网站](https://flomoapp.com/) 获取）
- [x] 有微信读书 Cookie（参考 [Cookie 获取指南](COOKIE_GUIDE.md)）

---

## 🚀 5 步快速配置

### 步骤 1：创建 Workflow 文件（2 分钟）

在你的 Fork 仓库中创建文件：`.github/workflows/sync.yml`

**方式 A：直接在 GitHub 网页创建**（推荐）

1. 进入你 Fork 的仓库
2. 点击 `Add file` → `Create new file`
3. 文件名输入：`.github/workflows/sync.yml`
4. 复制下面的完整配置，粘贴进去
5. 点击底部 `Commit new file`

**方式 B：本地创建并推送**

```bash
# 创建目录和文件
mkdir -p .github/workflows
nano .github/workflows/sync.yml  # 粘贴下面的配置

# 提交并推送
git add .github/workflows/sync.yml
git commit -m "feat: 添加 GitHub Actions 自动同步"
git push
```

**完整配置文件**（直接复制）：

```yaml
name: WeRead to Flomo Sync

on:
  # 定时任务：每天 UTC 00:00（北京时间 08:00）运行
  schedule:
    - cron: '0 0 * * *'
  
  # 允许手动触发
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    
    steps:
    # 步骤 1：检出代码
    - name: 📥 检出代码
      uses: actions/checkout@v4
        
    # 步骤 2：设置 Python 环境
    - name: 🐍 设置 Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.9'
        cache: 'pip'
        
    # 步骤 3：安装依赖
    - name: 📦 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    # 步骤 4：运行同步
    - name: 🔄 运行同步
      env:
        # Cookie Cloud 配置（推荐）
        CC_URL: ${{ secrets.CC_URL }}
        CC_ID: ${{ secrets.CC_ID }}
        CC_PASSWORD: ${{ secrets.CC_PASSWORD }}
        # 或使用手动 Cookie
        WEREAD_COOKIE: ${{ secrets.WEREAD_COOKIE }}
        # Flomo API
        FLOMO_API: ${{ secrets.FLOMO_API }}
        # AI 配置（可选）
        AI_API_KEY: ${{ secrets.AI_API_KEY }}
      run: |
        python sync.py
        
    # 步骤 5：提交同步记录（关键！）
    - name: 💾 保存同步记录
      run: |
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git config --local user.name "github-actions[bot]"
        git add synced_bookmarks.json
        git diff --quiet && git diff --staged --quiet || \
          (git commit -m "chore: 更新同步记录 [skip ci]" && git push)
```

---

### 步骤 2：配置 GitHub Secrets（3 分钟）

**什么是 Secrets？**
- 安全地存储敏感信息（Cookie、API Key）
- 不会出现在代码中
- 只有 Actions 能访问

**操作步骤**：

1. **进入仓库设置**
   - 打开你 Fork 的仓库
   - 点击顶部 `Settings` 标签

2. **进入 Secrets 配置**
   - 左侧菜单找到 `Secrets and variables`
   - 点击 `Actions`

3. **添加 Secrets**
   - 点击 `New repository secret` 按钮
   - 按照下表逐个添加：

| Secret 名称 | 获取方式 | 必填 | 示例值 |
|------------|---------|------|--------|
| `CC_URL` | Cookie Cloud 服务器地址 | ⭐ 推荐 | `https://cc.chenge.ink` |
| `CC_ID` | Cookie Cloud UUID | ⭐ 推荐 | `12345678-abcd-...` |
| `CC_PASSWORD` | Cookie Cloud 密码 | ⭐ 推荐 | `your-password` |
| `WEREAD_COOKIE` | 手动获取微信读书 Cookie | ⭐ 备选 | `wr_vid=123...` |
| `FLOMO_API` | Flomo 网站 → 设置 → API | ✅ 必需 | `https://flomoapp.com/iwh/...` |
| `AI_API_KEY` | AI 服务商提供 | 可选 | `sk-...` |

**推荐配置方式**：

**方案 A：使用 Cookie Cloud（推荐）**
```
CC_URL="https://cc.chenge.ink"
CC_ID="你的UUID"
CC_PASSWORD="你的密码"
FLOMO_API="你的Flomo API"
AI_API_KEY="你的AI Key"（可选）
```

**方案 B：手动 Cookie**
```
WEREAD_COOKIE="你的Cookie"
FLOMO_API="你的Flomo API"
AI_API_KEY="你的AI Key"（可选）
```

> 💡 **提示**：Cookie Cloud 可以自动更新 Cookie，更方便！参考 [Cookie Cloud 配置指南](COOKIE_CLOUD_GUIDE.md)

---

### 步骤 3：初始化同步记录（2 分钟）

**为什么需要这个文件？**
- 记录已同步的划线 ID
- 避免重复同步
- GitHub Actions 每次运行都能读取历史记录

**操作步骤**：

**方式 A：GitHub 网页创建**（推荐，最简单）

1. 进入你的仓库
2. 点击 `Add file` → `Create new file`
3. 文件名输入：`synced_bookmarks.json`
4. 内容复制：
```json
{
  "synced_ids": [],
  "last_sync": "2025-01-01T00:00:00",
  "total_synced": 0
}
```
5. 点击底部 `Commit new file`

**方式 B：本地创建**（如果你已有同步记录）

```bash
# 如果是新的，创建空记录
echo '{
  "synced_ids": [],
  "last_sync": "2025-01-01T00:00:00",
  "total_synced": 0
}' > synced_bookmarks.json

# 提交
git add synced_bookmarks.json
git commit -m "chore: 初始化同步记录"
git push
```

**如果你已经在本地同步过**，直接提交现有文件：

```bash
git add synced_bookmarks.json
git commit -m "chore: 上传已有同步记录"
git push
```

---

### 步骤 4：启用 GitHub Actions（1 分钟）

1. **进入 Actions 页面**
   - 点击仓库顶部的 `Actions` 标签

2. **启用 Workflows**
   - 如果看到 "Workflows aren't being run on this forked repository"
   - 点击绿色按钮 `I understand my workflows, go ahead and enable them`

3. **确认 Workflow 存在**
   - 应该能看到 `WeRead to Flomo Sync` 这个 workflow
   - 如果看不到，检查步骤 1 的文件是否创建成功

---

### 步骤 5：手动运行测试（2 分钟）

**首次运行测试**：

1. 在 `Actions` 页面，点击左侧 `WeRead to Flomo Sync`
2. 右上方点击 `Run workflow` 下拉按钮
3. 选择 `Branch: main`
4. 点击绿色按钮 `Run workflow`
5. 等待几秒，页面会出现新的运行记录
6. 点击进入，查看运行日志

**如何判断成功？**

✅ **成功的标志**：
- 所有步骤都有绿色 ✓
- 在 `运行同步` 步骤看到：
  ```
  ✅ 同步完成!
  本次新同步: X 条划线
  累计已同步: X 条划线
  ```
- `synced_bookmarks.json` 文件被自动更新

❌ **失败的原因**：
- Secrets 配置错误（检查步骤 2）
- Cookie 过期（重新获取）
- Flomo API 无效（检查 API 地址）

---

## ✅ 配置完成检查清单

确认所有步骤都完成：

- [ ] 创建了 `.github/workflows/sync.yml` 文件
- [ ] 配置了所有必需的 GitHub Secrets
- [ ] 创建了 `synced_bookmarks.json` 初始文件
- [ ] 启用了 GitHub Actions
- [ ] 手动运行测试成功
- [ ] 在 Flomo 中看到同步的笔记

**全部完成？恭喜！🎉**

现在每天早上 8 点（北京时间），系统会自动同步你的微信读书笔记到 Flomo！

---

## 🎉 开始使用

### 自动同步

配置完成后，系统会：
- 每天早上 8 点自动运行
- 只同步新增的划线
- 自动更新同步记录
- 完全无需人工干预

### 手动同步

随时想同步：
1. 进入 `Actions` 页面
2. 点击 `WeRead to Flomo Sync`
3. 点击 `Run workflow`
4. 点击 `Run workflow` 按钮

### 查看运行记录

1. 进入 `Actions` 页面
2. 点击任意一次运行
3. 查看详细日志
4. 确认同步成功

---

## 🔧 自定义配置

### 修改运行时间

编辑 `.github/workflows/sync.yml`：

```yaml
# 每天早上 8 点（北京时间）
- cron: '0 0 * * *'

# 改为每天晚上 10 点（北京时间）
- cron: '0 14 * * *'

# 每 12 小时一次
- cron: '0 */12 * * *'

# 每周一早上 8 点
- cron: '0 0 * * 1'
```

### 调整同步数量

在 GitHub Secrets 中添加：

| Secret 名称 | 作用 | 推荐值 |
|------------|------|--------|
| `SYNC_MAX_HIGHLIGHTS` | 每次最多同步几条 | 50 |
| `SYNC_DAYS_LIMIT` | 只同步最近几天 | 100 |

### 启用 AI 功能

添加 AI 相关的 Secrets：

```
AI_API_KEY="你的 AI API Key"
```

其他配置在 `config.yaml` 中设置。

---

## 🎛️ 工作原理

### 为什么不会重复同步？

```
第 1 天运行:
├─ 读取 synced_bookmarks.json (空)
├─ 获取微信读书划线 (50 条)
├─ 全部都是新的，同步 50 条 ✅
├─ 更新 synced_bookmarks.json (记录 50 个 ID)
└─ 提交到 Git ✅

第 2 天运行:
├─ 读取 synced_bookmarks.json (有 50 个 ID)
├─ 获取微信读书划线 (52 条)
├─ 过滤：50 条已同步，2 条是新的
├─ 只同步 2 条新的 ✅
├─ 更新 synced_bookmarks.json (记录 52 个 ID)
└─ 提交到 Git ✅

第 3 天运行:
├─ 读取 synced_bookmarks.json (有 52 个 ID)
├─ 获取微信读书划线 (52 条)
├─ 过滤：全部已同步
├─ 没有新划线，跳过 ✅
└─ 不更新文件
```

**关键点**：
- `synced_bookmarks.json` 存储在 Git 仓库中
- 每次运行都能读取到历史记录
- 只同步新增的划线

---

## ❓ 常见问题

### Q1: Actions 运行失败怎么办？

**检查步骤**：

1. **查看错误日志**
   - 进入 Actions 页面
   - 点击失败的运行
   - 查看红色 X 的步骤
   - 展开查看详细错误信息

2. **常见错误及解决**：

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Cookie invalid` | Cookie 过期 | 重新获取 Cookie 并更新 Secrets |
| `403 Forbidden` | Flomo API 错误 | 检查 FLOMO_API 是否正确 |
| `push rejected` | Git 提交冲突 | 正常，下次运行会自动解决 |
| `Module not found` | 依赖安装失败 | 检查 requirements.txt |

### Q2: 每次都同步相同的划线？

**可能原因**：
1. `synced_bookmarks.json` 没有被提交
2. Workflow 中没有保存同步记录的步骤

**检查方法**：

```bash
# 查看文件是否被提交
git log --oneline | grep "synced"

# 应该看到类似这样的提交
# a1b2c3d chore: 更新同步记录 [skip ci]
```

**解决方案**：
- 确保 workflow 中有 "保存同步记录" 步骤
- 确保 `.gitignore` 没有忽略该文件
- 手动提交一次文件触发更新

### Q3: Cookie 经常过期怎么办？

**推荐方案：使用 Cookie Cloud**

1. 安装 [Cookie Cloud 浏览器插件](https://github.com/easychen/CookieCloud)
2. 配置 Cookie Cloud 服务器
3. 在 GitHub Secrets 中配置：
   - `CC_URL`
   - `CC_ID`
   - `CC_PASSWORD`
4. Cookie 会自动更新，无需手动维护

详见：[Cookie Cloud 配置指南](COOKIE_CLOUD_GUIDE.md)

### Q4: 如何重新同步所有划线？

**方法**：清空同步记录

1. 编辑 `synced_bookmarks.json`：
```json
{
  "synced_ids": [],
  "last_sync": "2025-01-01T00:00:00",
  "total_synced": 0
}
```

2. 提交并推送
3. 手动运行 Workflow

⚠️ **注意**：确保不超过 Flomo API 限制（100次/天）

### Q5: 本地和 GitHub Actions 同步记录不一致？

**推荐方案**：只用一种方式

- **方案 A**：只用 GitHub Actions（推荐）
  - 不在本地运行同步
  - 所有同步由 Actions 完成

- **方案 B**：本地运行后提交
  ```bash
  python sync.py
  git add synced_bookmarks.json
  git commit -m "chore: 本地同步记录"
  git push
  ```

### Q6: 如何调整同步频率？

编辑 `.github/workflows/sync.yml`：

```yaml
on:
  schedule:
    # 每天 1 次
    - cron: '0 0 * * *'
    
    # 每天 2 次（早晚）
    - cron: '0 0,12 * * *'
    
    # 每周一次
    - cron: '0 0 * * 1'
```

**Cron 语法速查**：
```
┌───────────── 分钟 (0 - 59)
│ ┌───────────── 小时 (0 - 23)
│ │ ┌───────────── 日 (1 - 31)
│ │ │ ┌───────────── 月 (1 - 12)
│ │ │ │ ┌───────────── 星期 (0 - 6, 0 = 周日)
│ │ │ │ │
* * * * *
```

---

### 调试技巧

**添加调试输出**：

编辑 workflow，在运行同步后添加：

```yaml
- name: 🔍 调试信息
  if: always()
  run: |
    echo "=== 同步记录内容 ==="
    cat synced_bookmarks.json
    echo "=== Git 状态 ==="
    git status
    echo "=== 最近提交 ==="
    git log --oneline -5
```

---

## 📚 相关文档

- [Cookie Cloud 配置指南](COOKIE_CLOUD_GUIDE.md) - 自动更新 Cookie
- [Cookie 获取指南](COOKIE_GUIDE.md) - 手动获取 Cookie
- [配置指南](CONFIG_GUIDE.md) - 完整配置说明
- [快速开始](QUICKSTART.md) - 新手入门

---

## 💡 最佳实践

### 1. 安全性

- ✅ 使用 GitHub Secrets 存储敏感信息
- ✅ 不要在代码中硬编码 API Key
- ✅ 定期更换 Cookie（或使用 Cookie Cloud）
- ✅ 监控运行日志，及时发现异常

### 2. 性能优化

- ⚙️ 设置合理的同步数量（50条/次）
- ⚙️ 限制时间范围（最近30-100天）
- ⚙️ 避免频繁运行（每天1-2次足够）

### 3. 成本控制

- 💰 GitHub Actions 每月 2000 分钟免费
- 💰 本项目每次运行约 2-3 分钟
- 💰 每天运行 1 次，每月约 60-90 分钟
- 💰 完全在免费额度内

---

## 🎉 总结

### 你已经学会了

- ✅ 配置 GitHub Actions 自动同步
- ✅ 管理 GitHub Secrets
- ✅ 理解同步去重机制
- ✅ 排查常见问题
- ✅ 自定义配置

### 关键要点

1. **synced_bookmarks.json 是核心** - 存储同步记录，实现去重
2. **Secrets 保护隐私** - 安全存储敏感信息
3. **Workflow 自动化** - 无需人工干预
4. **完全免费** - GitHub Actions 免费额度足够使用

### 下一步

- 🎯 配置完成后，等待明天早上 8 点自动运行
- 🎯 随时可以手动触发测试
- 🎯 在 Flomo 中查看同步的笔记
- 🎯 根据需要调整配置

---

**现在，你的微信读书笔记会自动同步到 Flomo 了！** 🎊

有任何问题，查看 [常见问题](#-常见问题) 或 [提交 Issue](https://github.com/blessonism/weread2flomo/issues)。

---

<div align="center">
  <sub>让阅读更有价值，让思考永不丢失 📚 → 💭 → ✨</sub>
</div>

