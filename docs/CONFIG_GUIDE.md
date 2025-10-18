# 配置指南

本项目支持灵活的配置方式，优先级为：**环境变量 > config.yaml > 默认值**

## 快速开始

### 1. 复制环境变量模板

```bash
cp .env.example .env
```

### 2. 编辑 .env 文件

填写必要的配置：

```bash
# 必填项
WEREAD_COOKIE=你的微信读书Cookie
FLOMO_API=https://flomoapp.com/iwh/你的API地址

# 可选项（使用默认值即可）
SYNC_DAYS_LIMIT=100
SYNC_MAX_HIGHLIGHTS=50
```

### 3. 运行同步

```bash
python sync.py
```

## 配置方式详解

### 方式一：使用 .env 文件（推荐）

优点：
- ✅ 敏感信息不会被提交到 Git
- ✅ 不同环境可以使用不同的 .env 文件
- ✅ 配置简单，易于管理

步骤：
1. 复制 `.env.example` 为 `.env`
2. 在 `.env` 中填写配置
3. 运行程序即可

### 方式二：使用 config.yaml 文件

优点：
- ✅ 支持复杂的配置结构（模板、分类规则等）
- ✅ 适合团队共享非敏感配置

步骤：
1. 编辑 `config.yaml`
2. 修改相应配置项
3. 运行程序

**注意**：config.yaml 中的敏感信息（如 API Key）已移除，请使用 .env 文件配置

### 方式三：混合使用

实践建议：
- 敏感信息（Cookie、API Key）→ `.env` 文件
- 业务配置（模板、标签规则）→ `config.yaml` 文件

## 配置项说明

### 必填配置

#### 微信读书 Cookie

**方式 1：直接提供 Cookie（推荐）**

```bash
WEREAD_COOKIE=你的完整Cookie字符串
```

获取方式：参考 [docs/COOKIE_GUIDE.md](./COOKIE_GUIDE.md)

**方式 2：使用 Cookie Cloud**

```bash
CC_URL=你的CookieCloud服务地址
CC_ID=你的用户ID
CC_PASSWORD=你的加密密码
```

获取方式：参考 [docs/COOKIE_CLOUD_GUIDE.md](./COOKIE_CLOUD_GUIDE.md)

#### Flomo API

```bash
FLOMO_API=https://flomoapp.com/iwh/你的API地址
```

获取方式：flomo 网页端 → 设置 → API → 生成 API

### 同步配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| 时间限制 | `SYNC_DAYS_LIMIT` | 100 | 只同步最近X天的划线，0表示全部 |
| 最大划线数 | `SYNC_MAX_HIGHLIGHTS` | 50 | 每次同步的最大划线数 |
| 同步笔记 | `SYNC_REVIEWS` | true | 是否同步笔记（除了划线） |

示例：

```bash
# 只同步最近30天的划线
SYNC_DAYS_LIMIT=30

# 每次最多同步100条
SYNC_MAX_HIGHLIGHTS=100

# 不同步笔记
SYNC_REVIEWS=false
```

### 标签配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| 书名标签 | `ADD_BOOK_TITLE_TAG` | true | 是否添加书名作为标签 |
| 作者标签 | `ADD_AUTHOR_TAG` | false | 是否添加作者作为标签 |
| AI标签 | `ENABLE_AI_TAGS` | false | 是否启用AI自动标签 |
| AI标签数量 | `MAX_AI_TAGS` | 3 | AI标签的最大数量 |

示例：

```bash
# 启用AI标签
ENABLE_AI_TAGS=true

# 最多生成5个AI标签
MAX_AI_TAGS=5
```

### AI 配置

#### AI 服务提供商

```bash
AI_PROVIDER=openai  # 可选: openai, local, none
```

支持所有 OpenAI 兼容格式的 API，包括：
- OpenAI 官方
- Azure OpenAI
- 国内大模型服务（智谱AI、月之暗面、通义千问等）
- 自托管模型（Ollama、LocalAI 等）

#### OpenAI 或兼容服务配置

```bash
# API Key（必填）
AI_API_KEY=sk-你的API密钥

# API Base URL（可选，默认：https://api.openai.com/v1）
AI_API_BASE=https://api.openai.com/v1

# 模型名称（可选，默认：gpt-3.5-turbo）
AI_MODEL=gpt-3.5-turbo
```

**常见服务配置示例**：

1. **OpenAI 官方**
   ```bash
   AI_PROVIDER=openai
   AI_API_KEY=sk-your-openai-key
   AI_API_BASE=https://api.openai.com/v1
   AI_MODEL=gpt-3.5-turbo
   ```

2. **Azure OpenAI**
   ```bash
   AI_PROVIDER=openai
   AI_API_KEY=your-azure-key
   AI_API_BASE=https://your-resource.openai.azure.com
   AI_MODEL=your-deployment-name
   ```

3. **国内服务商（如智谱AI）**
   ```bash
   AI_PROVIDER=openai
   AI_API_KEY=your-api-key
   AI_API_BASE=https://open.bigmodel.cn/api/paas/v4
   AI_MODEL=glm-4
   ```

4. **本地模型（Ollama）**
   ```bash
   AI_PROVIDER=openai
   AI_API_KEY=ollama  # 本地服务可以填任意值
   AI_API_BASE=http://localhost:11434/v1
   AI_MODEL=llama2
   ```

### 模板配置

#### 默认模板选择

```bash
DEFAULT_TEMPLATE=detailed  # 可选: simple, standard, detailed
```

#### 自定义模板

自定义模板需要在 `config.yaml` 中配置：

```yaml
templates:
  my_template:
    name: "我的模板"
    description: "自定义模板说明"
    format: |
      {highlight_text}
      
      来自：《{book_title}》
      {tags}
```

模板支持的变量：
- `{book_title}` - 书名
- `{author}` - 作者
- `{highlight_text}` - 划线内容
- `{chapter_info}` - 章节信息
- `{book_url}` - 书籍链接
- `{note_section}` - 笔记内容
- `{create_time}` - 创建时间
- `{tags}` - 标签

### 高级配置

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| 请求延迟 | `REQUEST_DELAY` | 1.0 | 请求之间的延迟（秒） |
| 日志级别 | `LOG_LEVEL` | INFO | DEBUG, INFO, WARNING, ERROR |
| 重试次数 | `MAX_RETRIES` | 3 | API失败时的重试次数 |

示例：

```bash
# 降低请求频率
REQUEST_DELAY=2.0

# 启用调试日志
LOG_LEVEL=DEBUG
```

## 配置优先级

当同一个配置项在多个地方定义时，优先级为：

1. **环境变量**（最高优先级）
2. **config.yaml 文件**
3. **代码中的默认值**（最低优先级）

示例：

```yaml
# config.yaml
sync:
  days_limit: 100
```

```bash
# .env
SYNC_DAYS_LIMIT=30
```

最终生效的是 `30`（环境变量优先）

## 书籍分类配置

书籍分类配置只能在 `config.yaml` 中设置，用于根据书名/作者自动分类并应用不同的标签和模板。

```yaml
book_categories:
  tech:
    keywords:
      - "编程"
      - "技术"
    tags:
      - "#技术"
    template: "detailed"
```

当书名或作者包含关键词时，会自动：
1. 添加对应的标签
2. 使用对应的模板

## 常见问题

### Q1: 如何修改默认标签？

在 `config.yaml` 中修改：

```yaml
tags:
  default:
    - "#微信读书"
    - "#我的自定义标签"
```

### Q2: 如何禁用书名标签？

在 `.env` 中设置：

```bash
ADD_BOOK_TITLE_TAG=false
```

### Q3: 如何使用代理或国内服务？

在 `.env` 中设置对应的 API 地址：

```bash
# 使用代理
AI_API_BASE=https://你的代理地址/v1

# 或使用国内服务
AI_API_BASE=https://国内服务商的API地址
```

### Q4: 如何查看详细的调试信息？

在 `.env` 中启用调试日志：

```bash
LOG_LEVEL=DEBUG
```

### Q5: 配置修改后需要重启吗？

是的，修改 `.env` 或 `config.yaml` 后需要重新运行程序。

## 最佳实践

1. **敏感信息安全**
   - ✅ 将 Cookie、API Key 等放在 `.env` 文件
   - ✅ 确保 `.env` 在 `.gitignore` 中
   - ✅ 不要将 `.env` 提交到版本控制

2. **配置管理**
   - ✅ 使用 `.env.example` 作为模板
   - ✅ 在团队中共享 `config.yaml`（不含敏感信息）
   - ✅ 文档化自定义配置

3. **性能优化**
   - ✅ 合理设置 `SYNC_DAYS_LIMIT` 避免同步过多历史数据
   - ✅ 调整 `REQUEST_DELAY` 避免触发API限流
   - ✅ 控制 `SYNC_MAX_HIGHLIGHTS` 避免单次运行时间过长

4. **AI 使用**
   - ✅ 先使用 `local` 模式测试
   - ✅ 确认效果后再启用云服务 AI
   - ✅ 控制 `MAX_AI_TAGS` 数量避免过度标注

## 相关文档

- [Cookie 获取指南](./COOKIE_GUIDE.md)
- [Cookie Cloud 配置](./COOKIE_CLOUD_GUIDE.md)
- [快速开始](./QUICKSTART.md)
- [项目导航](./PROJECT_NAVIGATION.md)

