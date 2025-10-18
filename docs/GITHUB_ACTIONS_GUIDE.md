# GitHub Actions 自动同步指南

> 本文档说明如何使用 GitHub Actions 实现自动同步，并确保去重机制正常工作

## 🎯 核心原理

### 问题：GitHub Actions 环境的特殊性

每次 GitHub Actions 运行时：
- ✅ 会 checkout 最新的代码
- ❌ 环境是全新的（无本地文件）
- ❌ 运行结束后环境被销毁

如果不做处理：
```
第1次运行: 同步 50 条划线 ✅
第2次运行: 又同步相同的 50 条 ❌ (重复了!)
第3次运行: 继续重复... ❌
很快达到 API 限制 💥
```

### 解决方案：Git 作为持久化存储

将 `synced_bookmarks.json` 提交到 Git 仓库：

```
第1次运行:
  1. 读取 synced_bookmarks.json (空或有旧记录)
  2. 同步新划线
  3. 更新 synced_bookmarks.json
  4. 提交到 Git ✅

第2次运行:
  1. checkout 代码 (包含上次更新的 synced_bookmarks.json)
  2. 读取记录 (有上次的记录) ✅
  3. 只同步新增划线 ✅
  4. 更新并提交 ✅
```

## 📋 完整配置

### 1. 检查 .gitignore

确保 `synced_bookmarks.json` **不被忽略**：

```gitignore
# ❌ 错误 - 会导致去重失效
synced_bookmarks.json

# ✅ 正确 - 允许提交
# synced_bookmarks.json - 注释掉，GitHub Actions 需要提交此文件
```

**已修复**：我已经帮你更新了 `.gitignore` 文件。

### 2. GitHub Actions Workflow

**文件位置**：`.github/workflows/sync.yml`

```yaml
name: Sync WeRead to Flomo

on:
  schedule:
    # 每天 UTC 0:00 运行（北京时间 8:00）
    - cron: "0 0 * * *"
  workflow_dispatch:  # 允许手动触发

jobs:
  sync:
    runs-on: ubuntu-latest

    steps:
      # 1. 检出代码（包含 synced_bookmarks.json）
      - name: Checkout repository
        uses: actions/checkout@v4

      # 2. 设置 Python 环境
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      # 3. 安装依赖
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # 4. 运行同步脚本
      - name: Run sync script
        env:
          WEREAD_COOKIE: ${{ secrets.WEREAD_COOKIE }}
          FLOMO_API: ${{ secrets.FLOMO_API }}
          # 其他环境变量...
        run: |
          python sync.py

      # 5. 提交更新的同步记录 ⭐ 关键步骤
      - name: Commit and push synced records
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add synced_bookmarks.json
          git diff --quiet && git diff --staged --quiet || \
            (git commit -m "🔄 Update synced bookmarks [$(date +'%Y-%m-%d %H:%M:%S')]" && git push)
```

**关键步骤说明**：

第 5 步的命令解析：
```bash
# 配置 Git 用户
git config --local user.email "action@github.com"
git config --local user.name "GitHub Action"

# 添加同步记录文件
git add synced_bookmarks.json

# 如果有更改，则提交并推送
git diff --quiet && git diff --staged --quiet || \
  (git commit -m "🔄 Update synced bookmarks [时间戳]" && git push)
```

**逻辑**：
- `git diff --quiet` - 检查是否有未暂存的更改
- `&&` - 如果没有更改，命令结束
- `||` - 如果有更改，执行括号中的命令（提交并推送）

### 3. 配置 GitHub Secrets

在 GitHub 仓库设置中添加：

1. 进入 `Settings` → `Secrets and variables` → `Actions`

2. 添加 Repository Secrets：

| Secret 名称 | 说明 | 必填 |
|------------|------|------|
| `WEREAD_COOKIE` | 微信读书 Cookie | ✅ |
| `FLOMO_API` | Flomo API 地址 | ✅ |
| `AI_API_KEY` | AI API Key | ❌ |
| `AI_API_BASE` | AI API Base URL | ❌ |
| `AI_PROVIDER` | AI 提供商 | ❌ |

### 4. 初始化同步记录文件

**首次设置时**，需要提交初始的 `synced_bookmarks.json`：

```bash
# 如果文件不存在，创建空记录
echo '{
  "synced_ids": [],
  "last_sync": "2025-01-01T00:00:00",
  "total_synced": 0
}' > synced_bookmarks.json

# 提交到 Git
git add synced_bookmarks.json
git commit -m "📝 Initialize synced bookmarks"
git push
```

**如果已有本地同步记录**，直接提交：

```bash
# 提交现有记录
git add synced_bookmarks.json
git commit -m "📝 Add existing synced bookmarks"
git push
```

## 🔄 完整工作流程

### 初始设置

```
1. Fork/Clone 仓库
   ↓
2. 配置 GitHub Secrets
   ↓
3. 提交 synced_bookmarks.json (空或现有)
   ↓
4. 启用 GitHub Actions
   ↓
5. 完成！
```

### 每次运行

```
触发时间到达（每天8点）
   ↓
GitHub Actions 启动
   ↓
Checkout 代码（包含 synced_bookmarks.json）
   ↓
加载已同步的记录
   ↓
获取微信读书划线
   ↓
过滤：只同步新增的划线 ✅
   ↓
发送到 Flomo
   ↓
更新 synced_bookmarks.json
   ↓
提交并推送到 Git ✅
   ↓
下次运行时能读取到最新记录 ✅
```

## 📊 实际效果演示

### 第一天

```
synced_bookmarks.json (初始):
{
  "synced_ids": [],
  "total_synced": 0
}

运行结果:
- 同步了 5 条新划线 ✅

synced_bookmarks.json (更新后):
{
  "synced_ids": [
    "600196_17_16119-16149",
    "27369030_3_4083-4127",
    "600196_17_13358-13437",
    "27369030_3_1521-1558",
    "600196_17_6163-6205"
  ],
  "last_sync": "2025-10-19T00:00:15",
  "total_synced": 5
}
```

### 第二天

```
synced_bookmarks.json (从 Git 读取):
{
  "synced_ids": [
    "600196_17_16119-16149",
    "27369030_3_4083-4127",
    "600196_17_13358-13437",
    "27369030_3_1521-1558",
    "600196_17_6163-6205"
  ],
  "total_synced": 5
}

运行结果:
- 发现 3 条新划线
- 跳过 5 条已同步 ✅
- 同步了 3 条新划线 ✅

synced_bookmarks.json (更新后):
{
  "synced_ids": [
    "600196_17_16119-16149",
    "27369030_3_4083-4127",
    "600196_17_13358-13437",
    "27369030_3_1521-1558",
    "600196_17_6163-6205",
    "27369030_5_437-507",      # 新增
    "600196_17_8286-8382",      # 新增
    "28456123_2_1234-1290"      # 新增
  ],
  "last_sync": "2025-10-20T00:00:12",
  "total_synced": 8
}
```

## 🎛️ 手动触发

GitHub Actions 支持手动触发：

1. 进入仓库的 `Actions` 标签页
2. 选择 `Sync WeRead to Flomo` workflow
3. 点击 `Run workflow` 按钮
4. 选择分支（通常是 `main` 或 `master`）
5. 点击 `Run workflow`

## 🐛 常见问题

### Q1: GitHub Actions 提交失败

**错误信息**：
```
error: failed to push some refs
```

**原因**：可能有其他提交导致冲突

**解决方案**：
修改 workflow，添加 pull 和 rebase：

```yaml
- name: Commit and push synced records
  run: |
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    git pull --rebase  # 先拉取最新代码
    git add synced_bookmarks.json
    git diff --quiet && git diff --staged --quiet || \
      (git commit -m "🔄 Update synced bookmarks [$(date +'%Y-%m-%d %H:%M:%S')]" && git push)
```

### Q2: synced_bookmarks.json 没有被提交

**检查清单**：

1. ✅ `.gitignore` 中没有忽略该文件
2. ✅ workflow 中有 `git add synced_bookmarks.json`
3. ✅ 文件确实有变化（新增了划线）

**调试方法**：

在 workflow 中添加调试输出：

```yaml
- name: Debug synced records
  run: |
    echo "=== Current synced_bookmarks.json ==="
    cat synced_bookmarks.json
    echo "=== Git status ==="
    git status
```

### Q3: 每次都同步相同的划线

**可能原因**：

1. `synced_bookmarks.json` 被 `.gitignore` 忽略
2. 提交步骤失败（没有推送成功）
3. 读取同步记录失败

**排查步骤**：

```bash
# 1. 检查 .gitignore
cat .gitignore | grep synced_bookmarks.json

# 2. 检查 Git 历史
git log --oneline | grep "synced bookmarks"

# 3. 查看文件内容
cat synced_bookmarks.json
```

### Q4: 本地和 GitHub Actions 不同步

**场景**：本地运行和 GitHub Actions 各自维护一套记录

**解决方案**：

**方式1**：只用 GitHub Actions（推荐）
- 不在本地运行同步
- 所有同步由 GitHub Actions 完成

**方式2**：本地推送到 Git
- 本地运行后，提交 `synced_bookmarks.json`
- GitHub Actions 会读取最新记录

```bash
# 本地同步后
python sync.py

# 提交记录
git add synced_bookmarks.json
git commit -m "🔄 Local sync"
git push
```

### Q5: 如何重新同步所有划线？

**在 GitHub Actions 中**：

1. 直接编辑 `synced_bookmarks.json`，清空记录
2. 提交并推送：

```bash
echo '{
  "synced_ids": [],
  "last_sync": "2025-01-01T00:00:00",
  "total_synced": 0
}' > synced_bookmarks.json

git add synced_bookmarks.json
git commit -m "🔄 Reset synced records"
git push
```

3. 下次运行时会重新同步

**注意**：确保不超过 flomo API 限制（100次/天）

## 📈 监控和日志

### 查看运行记录

1. 进入 `Actions` 标签页
2. 点击任意一次运行
3. 查看详细日志

### 关键日志

运行成功时，你应该看到：

```
⚙️  配置加载:
   - 时间限制: 100天
   - 最大划线数: 50
   - AI标签: 禁用

📚 处理书籍: 《示例书名》- 作者
   ✓ 获取到 15 条划线
   ℹ️  过滤了 10 条划线（已同步或超出时间限制）
   找到 5 条新划线
   ✓ 成功发送笔记到 flomo (第 1 次)
   ✓ 成功发送笔记到 flomo (第 2 次)
   ...

✅ 同步完成!
   处理书籍: 3/5
   本次新同步: 5 条划线
   累计已同步: 120 条划线
```

### 提交记录

查看 Git 提交历史：

```bash
git log --oneline | grep "synced bookmarks"
```

应该看到：
```
a1b2c3d 🔄 Update synced bookmarks [2025-10-20 00:00:15]
d4e5f6g 🔄 Update synced bookmarks [2025-10-19 00:00:12]
g7h8i9j 🔄 Update synced bookmarks [2025-10-18 00:00:08]
```

## 🚀 最佳实践

### 1. 定时策略

**推荐时间**：每天早上（查看昨天的阅读）

```yaml
on:
  schedule:
    # UTC 0:00 = 北京时间 8:00
    - cron: "0 0 * * *"
```

**其他选项**：

```yaml
# 每12小时
- cron: "0 */12 * * *"

# 每周一早上
- cron: "0 0 * * 1"

# 每天早晚两次
- cron: "0 0,12 * * *"
```

### 2. API 限制管理

**flomo API 限制**：100次/天

**配置建议**：

```bash
# .env 或 GitHub Secrets
SYNC_MAX_HIGHLIGHTS=50  # 单次最多50条
SYNC_DAYS_LIMIT=7       # 只同步最近7天
```

### 3. 错误通知

可以添加失败通知：

```yaml
- name: Notify on failure
  if: failure()
  run: |
    echo "Sync failed! Check logs at: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

或集成第三方通知服务（钉钉、企业微信、Telegram等）

### 4. 备份策略

**保留历史记录**：

```yaml
- name: Backup synced records
  run: |
    cp synced_bookmarks.json "backups/synced_$(date +'%Y%m%d').json"
    git add backups/
```

### 5. 安全建议

✅ **使用 GitHub Secrets**：不要在代码中硬编码密钥  
✅ **限制权限**：只给 Actions 需要的最小权限  
✅ **定期更换 Cookie**：微信读书 Cookie 会过期  
✅ **监控运行日志**：及时发现异常

## 📚 相关文档

- [去重机制详解](DEDUPLICATION.md)
- [配置指南](CONFIG_GUIDE.md)
- [快速开始](QUICKSTART.md)

## 🎉 总结

通过将 `synced_bookmarks.json` 提交到 Git 仓库，GitHub Actions 可以：

1. ✅ **持久化存储** - 每次运行都能读取历史记录
2. ✅ **增量同步** - 只同步新增的划线
3. ✅ **自动更新** - 运行后自动提交新记录
4. ✅ **完美去重** - 避免重复同步

**关键点**：
- 不要在 `.gitignore` 中忽略 `synced_bookmarks.json`
- workflow 中包含提交和推送步骤
- 首次使用前提交初始文件

这样就能实现完全自动化的增量同步了！🚀

