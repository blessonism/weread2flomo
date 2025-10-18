# weread2flomo - 增强版

自动同步微信读书划线笔记到 flomo，支持多模板、AI标签、智能分类等高级功能

## ✨ 功能特性

### P0 - MVP核心功能（已完成）
- ✅ **自动同步**：每天定时同步微信读书新划线到 flomo
- ✅ **基础模板**：书名 + 划线 + 来源信息 + 基础标签
- ✅ **官方API**：使用 flomo 官方 API，稳定可靠

### P1 - 体验优化（已完成）
- ✅ **多模板选择**：简洁/标准/详细三种模板，适配不同场景
- ✅ **AI智能标签**：自动提取划线主题，生成精准标签
  - 支持 OpenAI、Anthropic API
  - 内置本地规则引擎（无需 API）
- ✅ **时间筛选**：只同步最近X天的划线，避免初次导入过多
- ✅ **书籍分类**：工作类/个人成长/文学/技术 自动分类
- ✅ **智能标签体系**：不同分类使用不同的标签

### P2 - 高级功能（规划中）
- 🔄 AI摘要：对长划线自动生成一句话总结
- 🔄 多账号支持：同时管理多个微信读书账号
- 🔄 Web界面：可视化管理同步记录和设置

## 📖 模板示例

### 模板1：简洁模板（默认）
```
人们总是高估自己的理性，低估直觉的作用

📖 《思考，快与慢》· 丹尼尔·卡尼曼

📍 第三章 - 启发法与偏见

#认知偏差 #心理学 #微信读书 #思考，快与慢
```

### 模板2：标准模板
```
📖 《番茄工作法图解》- Francesco Cirillo

> 采用番茄工作法，25分钟专注+5分钟休息，可以显著提高工作效率

📍 第2章 - 基本原则
🔗 https://weread.qq.com/web/reader/xxx

💭 我的思考：可以试试用来写代码，看能不能对抗焦虑

#时间管理 #效率 #个人成长 #微信读书
```

### 模板3：详细模板
```
采用番茄工作法，25分钟专注+5分钟休息，可以显著提高工作效率

📚 来源：《番茄工作法图解》· Francesco Cirillo

📂 章节：第2章 - 基本原则

📅 时间：2024-10-17

💭 我的思考：可以试试用来写代码，看能不能对抗焦虑

#时间管理 #效率提升 #工作 #微信读书
```

## 🚀 快速开始

### 1. 克隆或下载项目

```bash
git clone https://github.com/your-username/weread2flomo.git
cd weread2flomo
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填入必要配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入必要信息：

```bash
# 必填：微信读书 Cookie（参考 docs/COOKIE_GUIDE.md）
WEREAD_COOKIE=你的Cookie

# 必填：Flomo API（从 flomo 网页端获取）
FLOMO_API=https://flomoapp.com/iwh/你的API

# 可选：同步配置
SYNC_DAYS_LIMIT=100  # 只同步最近100天
SYNC_MAX_HIGHLIGHTS=50  # 每次最多50条
```

**详细配置说明**：参见 [**📖 配置指南**](docs/CONFIG_GUIDE.md)

#### 快速获取 Cookie

**方式 1：Cookie Cloud（推荐，自动更新）**
- 详细教程：[Cookie Cloud 配置指南](docs/COOKIE_CLOUD_GUIDE.md)

**方式 2：手动复制（简单快速）**
- 详细教程：[Cookie 获取指南](docs/COOKIE_GUIDE.md)

### 4. 运行同步

```bash
python sync_v2.py
```

### 5. 使用 GitHub Actions 自动同步（可选）

1. Fork 本仓库到你的 GitHub 账号

2. 在仓库设置中添加 Secrets：
   - `Settings` → `Secrets and variables` → `Actions`
   - 添加 `WEREAD_COOKIE`
   - 添加 `FLOMO_API`
   - （可选）其他配置项

3. 启用 GitHub Actions：
   - 进入 `Actions` 标签页
   - 启用工作流

4. 完成！每天自动同步，也可以手动触发

## ⚙️ 配置说明

### 配置方式

本项目支持灵活的配置方式，优先级为：**环境变量 > config.yaml > 默认值**

- **`.env` 文件**：用于敏感信息（Cookie、API Key）和环境相关配置
- **`config.yaml`**：用于业务配置（模板、标签规则、分类等）

**详细配置说明**：[📖 完整配置指南](docs/CONFIG_GUIDE.md)

### 常用配置项

#### 必填配置

| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| 微信读书 Cookie | `WEREAD_COOKIE` | 认证凭证 |
| Flomo API | `FLOMO_API` | API 地址 |

#### 同步配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| 时间限制 | `SYNC_DAYS_LIMIT` | 100 | 只同步最近X天 |
| 最大划线数 | `SYNC_MAX_HIGHLIGHTS` | 50 | 每次最多同步N条 |
| 同步笔记 | `SYNC_REVIEWS` | true | 是否同步笔记 |

#### AI 配置

| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| AI 提供商 | `AI_PROVIDER` | openai/local/none |
| AI API Key | `AI_API_KEY` | API 密钥（OpenAI 格式） |
| AI API Base | `AI_API_BASE` | API 地址（支持所有 OpenAI 兼容服务） |
| 启用 AI 标签 | `ENABLE_AI_TAGS` | 是否启用 AI 标签 |

更多配置项请查看：[📖 配置指南](docs/CONFIG_GUIDE.md)

## 🎯 使用场景

### 场景1：快速记录灵感
使用**简洁模板**，专注于划线内容本身，快速积累想法。

### 场景2：深度阅读笔记
使用**详细模板**，完整记录书名、章节、时间、个人思考。

### 场景3：主题式阅读
开启 **AI标签**，自动提取主题，方便后续按主题检索。

### 场景4：定期回顾
设置 `days_limit: 30`，每月只同步最近30天的内容，保持信息新鲜度。

### 场景5：分类管理
使用**书籍分类**功能，工作类书籍自动添加 `#工作` 标签，便于分类查看。

## 📊 API 限制

- **flomo API**：100次/天
- **微信读书 API**：建议请求间隔1秒
- **OpenAI API**：根据你的账号配额
- **Anthropic API**：根据你的账号配额

## 🔧 高级用法

### 自定义模板

在 `config.yaml` 中添加你自己的模板：

```yaml
templates:
  custom:
    name: "自定义模板"
    format: |
      💡 {highlight_text}

      from 《{book_title}》

      {tags}
```

然后设置为默认：

```yaml
default_template: custom
```

### 扩展书籍分类

添加新的分类和关键词：

```yaml
book_categories:
  science:  # 科学类
    keywords:
      - "物理"
      - "化学"
      - "生物"
    tags:
      - "#科学"
      - "#知识"
    template: "detailed"
```

### 使用本地AI（无需API）

在 `.env` 中设置：

```bash
AI_PROVIDER=local
ENABLE_AI_TAGS=true
```

系统会根据内置的关键词规则生成标签，无需任何 API。

### 集成 AI 服务

支持所有 OpenAI 兼容格式的 API：

**1. OpenAI 官方**
```bash
AI_PROVIDER=openai
AI_API_KEY=sk-你的密钥
AI_API_BASE=https://api.openai.com/v1
AI_MODEL=gpt-3.5-turbo
ENABLE_AI_TAGS=true
```

**2. Azure OpenAI**
```bash
AI_PROVIDER=openai
AI_API_KEY=你的Azure密钥
AI_API_BASE=https://your-resource.openai.azure.com
AI_MODEL=your-deployment-name
ENABLE_AI_TAGS=true
```

**3. 国内服务（如智谱AI、通义千问等）**
```bash
AI_PROVIDER=openai
AI_API_KEY=你的API密钥
AI_API_BASE=服务商的API地址
AI_MODEL=对应的模型名称
ENABLE_AI_TAGS=true
```

**4. 本地模型（Ollama）**
```bash
AI_PROVIDER=openai
AI_API_KEY=ollama
AI_API_BASE=http://localhost:11434/v1
AI_MODEL=llama2
ENABLE_AI_TAGS=true
```

## 📝 常见问题

### Q: 如何获取微信读书 Cookie？

A:
1. 浏览器访问 https://weread.qq.com/ 并登录
2. 按 F12 打开开发者工具
3. 切换到 Application/存储 标签
4. 找到 Cookies → weread.qq.com
5. 复制所有 Cookie 值，格式如：`key1=value1; key2=value2;`

### Q: Cookie 会过期吗？

A: 会的。如果同步失败，检查 Cookie 是否过期并重新获取。或者使用 Cookie Cloud 服务自动更新。

### Q: AI 标签准确吗？

A:
- 使用 OpenAI/Anthropic API 准确率较高
- 本地规则引擎基于关键词匹配，准确率中等
- 建议开启后观察一段时间，根据效果调整

### Q: 为什么有的划线没有同步？

A: 检查以下几点：
1. 是否达到 flomo API 每日限制（100次）
2. 是否超出时间范围（days_limit 设置）
3. 是否已经同步过（检查 synced_bookmarks.json）

### Q: 如何重新同步所有划线？

A: 删除 `synced_bookmarks.json` 文件，然后重新运行同步脚本。注意 API 限制。

### Q: 可以同步到其他笔记工具吗？

A: 目前只支持 flomo。如果需要其他工具，可以参考代码修改 `flomo_client.py`。

## 🎨 路线图

- [x] 基础同步功能
- [x] 多模板支持
- [x] AI智能标签
- [x] 时间筛选
- [x] 书籍分类
- [ ] AI摘要生成
- [ ] Web管理界面
- [ ] 多账号支持
- [ ] 导出为 Markdown/PDF
- [ ] 支持其他笔记工具（Notion、Obsidian等）

## 📄 License

MIT

## 🙏 致谢

- 参考项目：[weread2notion](https://github.com/malinkang/weread2notion)
- 灵感来源：flomo 社区用户的需求反馈

## 📮 反馈与贡献

欢迎提交 Issue 和 Pull Request！

---

**如果觉得有帮助，请给个 ⭐️ Star！**
