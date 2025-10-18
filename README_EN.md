<div align="center">
    <img src="./assets/images/flomo.png" alt="WeRead2Flomo Logo" width="80"/>
    <h1>WeRead2Flomo</h1>
    <h3><em>Transform reading into knowledge, never lose your thoughts</em></h3>
</div>

<p align="center">
    <strong> Sync WeRead highlights to Flomo with AI summaries, smart tags, and multiple templates</strong>
</p>

<p align="center">
    <a href="https://github.com/blessonism/weread2flomo/stargazers"><img src="https://img.shields.io/github/stars/blessonism/weread2flomo?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/blessonism/weread2flomo/blob/main/LICENSE"><img src="https://img.shields.io/github/license/blessonism/weread2flomo" alt="License"/></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python"/></a>
    <a href="https://github.com/blessonism/weread2flomo/issues"><img src="https://img.shields.io/github/issues/blessonism/weread2flomo" alt="Issues"/></a>
</p>

---

[中文文档](README.md) | **English**

---

## Table of Contents

- [✨ Why WeRead2Flomo?](#-why-weread2flomo)
- [🚀 Quick Start](#-quick-start)
- [🎯 Features](#-features)
- [📖 Template Examples](#-template-examples)
- [⚙️ Configuration](#️-configuration)
- [🤖 AI Features](#-ai-features)
- [🔄 Automated Deployment](#-automated-deployment)
- [💡 Use Cases](#-use-cases)
- [📊 API Limits](#-api-limits)
- [🔧 Advanced Usage](#-advanced-usage)
- [❓ FAQ](#-faq)
- [🎨 Roadmap](#-roadmap)
- [🙏 Acknowledgements](#-acknowledgements)
- [📄 License](#-license)

---

## ✨ Why WeRead2Flomo?

Highlighting in WeRead is easy, but these insights are quickly forgotten. WeRead2Flomo helps you:

- 🔄 **Auto Sync** - No manual copying, automatic daily sync of new highlights
- 🤖 **AI Enhanced** - Auto-generate summaries and smart tags for better searchability
- 🎨 **Flexible Templates** - 3 built-in templates + custom options for different scenarios
- 📚 **Smart Categories** - Auto-detect book types and apply corresponding tag systems
- ⚡ **Ready to Use** - Simple setup, start using in 5 minutes
- 🔒 **Privacy First** - All data processed locally, supports private deployment

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- WeRead account
- Flomo account

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/blessonism/weread2flomo.git
cd weread2flomo
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment

Create `.env` file:

```bash
# ==================== Cookie Cloud Config (Recommended) ====================
# Auto-sync browser cookies, no manual updates needed
CC_URL="https://cc.chenge.ink"
CC_ID="your-uuid"
CC_PASSWORD="your-password"

# ==================== Alternative Cookie Config ====================
# If not using Cookie Cloud, configure manually
# WEREAD_COOKIE="your-weread-cookie"

# ==================== Flomo API Config (Required) ====================
FLOMO_API="https://flomoapp.com/iwh/your-api-key/"

# ==================== AI Config (Optional) ====================
# Enable AI summaries and smart tags
AI_API_KEY="your-ai-api-key"

# Other AI configs in config.yaml
```

> 📖 **Detailed Tutorials**:
> - [Cookie Cloud Setup Guide](docs/COOKIE_CLOUD_GUIDE.md) (Recommended, auto-updates)
> - [Manual Cookie Guide](docs/COOKIE_GUIDE.md) (Quick and simple)
> - [Complete Configuration Guide](docs/CONFIG_GUIDE.md)

#### 4. Run Sync

```bash
# Full sync
python sync.py

# Test single highlight (recommended for first use)
python test_single_highlight.py
```

#### 5. Check Results

Open your Flomo and enjoy your auto-synced reading notes!

---

## 🎯 Features

### Core Features

| Feature | Status | Description |
|---------|--------|-------------|
| 📝 **Auto Sync** | ✅ | Scheduled sync of new WeRead highlights to Flomo |
| 🎨 **Multi-Template** | ✅ | Simple/Standard/Detailed templates + custom |
| 🤖 **AI Summaries** | ✅ | Auto-generate one-sentence summaries for long highlights |
| 🏷️ **AI Smart Tags** | ✅ | Auto-extract topics and generate precise tags |
| 📚 **Book Categories** | ✅ | Auto-categorize Work/Growth/Literature/Tech |
| ⏱️ **Time Filter** | ✅ | Sync only recent N days of highlights |
| 🔄 **Incremental Sync** | ✅ | Auto-dedup, sync only new content |
| 🍪 **Cookie Cloud** | ✅ | Auto-sync browser cookies, no manual updates |

### Advanced Features

- ⚙️ **Flexible Config** - Support environment variables and YAML config
- 🔐 **Privacy Protection** - All data processed locally, no third-party uploads
- 📊 **Detailed Logging** - Complete sync records and statistics
- 🔧 **Highly Extensible** - Easy to add new templates and custom logic
- ⚡ **High Performance** - Smart deduplication and caching

---

## 📖 Template Examples

### 📌 Simple Template (Quick Recording)

```
People always overestimate their rationality and underestimate intuition

📖 "Thinking, Fast and Slow" · Daniel Kahneman

📍 Chapter 3 - Heuristics and Biases

✨ AI Summary: The struggle between intuition and rationality in decision-making, rationality is often overrated.

#WeRead/ThinkingFastAndSlow #CognitiveBias #Psychology
```

### 📋 Standard Template (Balanced)

```
📖 "The Pomodoro Technique" - Francesco Cirillo

> Using the Pomodoro Technique, 25 minutes of focus + 5 minutes of rest, can significantly improve work efficiency

📍 Chapter 2 - Basic Principles
🔗 https://weread.qq.com/web/reader/xxx

💭 My thoughts: Could try this for coding, see if it helps with anxiety

#WeRead/PomodoroTechnique #TimeManagement #Productivity #PersonalGrowth
```

### 📑 Detailed Template (Deep Reading)

```
Using the Pomodoro Technique, 25 minutes of focus + 5 minutes of rest, can significantly improve work efficiency

📚 Source: "The Pomodoro Technique" · Francesco Cirillo

📂 Chapter: Chapter 2 - Basic Principles

📅 Time: 2024-10-17

✨ AI Summary: Focus for 25 minutes, rest for 5, Pomodoro Technique doubles efficiency.

💭 My thoughts: Could try this for coding, see if it helps with anxiety

#WeRead/PomodoroTechnique #TimeManagement #EfficiencyBoost #Work
```

---

## ⚙️ Configuration

### Config Priority

**Environment Variables (.env) > YAML Config (config.yaml) > Defaults**

- **`.env`** - Sensitive info (cookies, API keys) and environment configs
- **`config.yaml`** - Business configs (templates, tag rules, categories)

### Core Configurations

#### Required

| Config | Environment Variable | Description |
|--------|---------------------|-------------|
| WeRead Auth | `CC_URL` + `CC_ID` + `CC_PASSWORD`<br/>or `WEREAD_COOKIE` | Cookie Cloud (recommended) or manual cookie |
| Flomo API | `FLOMO_API` | Official Flomo API endpoint |

#### Sync Settings

| Config | Environment Variable | Default | Description |
|--------|---------------------|---------|-------------|
| Time Limit | `SYNC_DAYS_LIMIT` | 100 | Sync only recent N days |
| Max Count | `SYNC_MAX_HIGHLIGHTS` | 50 | Max highlights per sync |
| Sync Reviews | `SYNC_REVIEWS` | true | Sync notes (not just highlights) |

#### AI Settings

| Config | Environment Variable | Description |
|--------|---------------------|-------------|
| AI Provider | `AI_PROVIDER` | `openai` (recommended) / `local` / `none` |
| API Key | `AI_API_KEY` | OpenAI-format API key |
| API Base | `AI_API_BASE` | Supports all OpenAI-compatible services |
| Model Name | `AI_MODEL` | e.g., `gpt-5`, `gpt-4.1` |

> 📖 **Complete Documentation**: [CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md)

---

## 🤖 AI Features

### AI Smart Summaries

**Auto-generate one-sentence summaries for long highlights**

```yaml
# config.yaml
ai:
  enable_summary: true
  summary_min_length: 100  # Minimum characters to trigger
```

**Example:**

Original (171 chars):
> We came to a tropical island, with the help of DDT, we eliminated malaria and saved hundreds of thousands of lives in two or three years. This is obviously good. But these hundreds of thousands of people saved, and the millions of descendants they reproduced, had no clothes to wear, no houses to live in, could not receive education...

AI Summary:
> ✨ **Eliminating malaria was a lifesaving act, but left millions of new people on the island in hunger, crowding, and endless misery.**

### AI Smart Tags

**Auto-extract topics and generate precise tags**

```yaml
# config.yaml
tags:
  enable_ai_tags: true
  max_ai_tags: 3  # Max 3 AI tags
```

**Example:**

Highlight:
> In the pyramid structure, the importance of each level generally decreases from top to bottom, with the top central idea being most important...

AI Generated Tags:
> `#PyramidStructure` `#LogicalThinking` `#CommunicationSkills`

### Supported AI Services

- ✅ **OpenAI** (GPT-4.1, GPT-5, etc.)
- ✅ **All OpenAI-compatible services** (domestic mirrors, private deployments)
- ✅ **Local rule engine** (no API needed, keyword-based)

---

## 🔄 Automated Deployment

### GitHub Actions (Recommended)

**Daily auto-sync, no local running required**

#### Steps:

1️⃣ **Fork this repository**

2️⃣ **Configure Secrets**
   - Go to `Settings` → `Secrets and variables` → `Actions`
   - Add the following Secrets:
     - `CC_URL` (Cookie Cloud URL)
     - `CC_ID` (Cookie Cloud UUID)
     - `CC_PASSWORD` (Cookie Cloud password)
     - `FLOMO_API` (Flomo API endpoint)
     - `AI_API_KEY` (AI API key, optional)

3️⃣ **Enable Actions**
   - Go to `Actions` tab
   - Enable workflows

4️⃣ **Done!**
   - Auto-sync daily at UTC 00:00 (Beijing time 08:00)
   - Manual trigger: `Actions` → `WeRead to Flomo Sync` → `Run workflow`

> 📖 **Detailed Tutorial**: [GitHub Actions Setup Guide](docs/GITHUB_ACTIONS_GUIDE.md)

---

## 💡 Use Cases

### Case 1: Quick Idea Collection

Use **simple template**, focus on highlight content, quickly accumulate ideas.

```yaml
default_template: simple
```

### Case 2: Topic-Based Reading

Enable **AI tags**, auto-extract topics for easier retrieval by theme.

```yaml
tags:
  enable_ai_tags: true
```

### Case 3: Deep Reading Notes

Use **detailed template**, record complete reading context and personal thoughts.

```yaml
default_template: detailed
sync_reviews: true
```

### Case 4: Category Management

Configure **book categories**, different book types auto-use different tags and templates.

```yaml
book_categories:
  work:
    keywords: ["management", "business", "career"]
    tags: ["#Work", "#Career"]
    template: "standard"
```

---

## 📊 API Limits

| Service | Limit | Note |
|---------|-------|------|
| **Flomo** | 100/day | Official API limit |
| **WeRead** | Recommend 1/sec | Avoid rate limiting |
| **OpenAI** | Per plan | Based on account quota |
| **Other AI Services** | Per plan | Based on provider rules |

### Optimization Tips

- Set reasonable `days_limit` (e.g., 30-100 days)
- Control `max_highlights_per_sync` (e.g., 20-50)
- For first sync, batch process to avoid exceeding limits

---

## 🔧 Advanced Usage

### Custom Templates

Add your template in `config.yaml`:

```yaml
templates:
  custom:
    name: "My Template"
    description: "Fits personal style"
    format: |
      💡 {highlight_text}
      
      From "{book_title}" by {author}
      
      {ai_summary_section}{tags}

default_template: custom
```

### Extend Book Categories

Add new category rules:

```yaml
book_categories:
  science:
    keywords:
      - "physics"
      - "chemistry"
      - "biology"
      - "science"
    tags:
      - "#Science"
      - "#Knowledge"
    template: "detailed"
```

### Custom AI Prompts

Modify AI tag or summary generation logic:

```yaml
ai:
  tag_prompt: |
    Generate 1-3 tags for the following highlight...
    
  summary_prompt: |
    Summarize the core idea in one sentence...
```

### Use Local AI (No API)

```yaml
ai:
  provider: local
  
tags:
  enable_ai_tags: true
```

System uses built-in keyword rules to generate tags, fully local.

---

## ❓ FAQ

<details>
<summary><strong>Q: How to get WeRead Cookie?</strong></summary>

**Method 1: Cookie Cloud (Recommended)**
- Install browser extension
- Configure server and credentials
- Auto-sync, no manual updates
- See: [Cookie Cloud Setup Guide](docs/COOKIE_CLOUD_GUIDE.md)

**Method 2: Manual**
1. Visit https://weread.qq.com/ and login
2. Press F12 to open DevTools
3. Go to Application/Storage tab
4. Find Cookies → weread.qq.com
5. Copy all cookie values
- See: [Cookie Guide](docs/COOKIE_GUIDE.md)

</details>

<details>
<summary><strong>Q: Do cookies expire?</strong></summary>

Yes. Traditional cookies have short validity (<2 hours).

**Solutions:**
- Use **Cookie Cloud** (recommended) - Auto-sync browser cookies
- Enable cookie keep-alive
- Use GitHub Actions for scheduled sync

</details>

<details>
<summary><strong>Q: Are AI tags accurate?</strong></summary>

Accuracy depends on AI service:
- **OpenAI GPT-5** - High accuracy (recommended)
- **Local rule engine** - Medium accuracy, keyword-based

Recommend testing for a while and adjusting config based on results.

</details>

---

## 🎨 Roadmap

### Completed ✅

- [x] Basic sync functionality
- [x] Multi-template system
- [x] AI smart tags
- [x] AI smart summaries
- [x] Time filtering
- [x] Book categorization
- [x] Incremental sync
- [x] Cookie Cloud support
- [x] GitHub Actions automation

### In Progress 🚧

- [ ] Web management interface
- [ ] Multi-account support

### Planned 📋

- [ ] Export to Markdown/PDF
- [ ] Support Notion, Obsidian
- [ ] Mobile app
- [ ] More AI model support
- [ ] Note linking and knowledge graph

---

## 🙏 Acknowledgements

Thanks to the following projects and services for inspiration:

- [weread2notion](https://github.com/malinkang/weread2notion) - WeRead sync solution reference
- [Flomo](https://flomoapp.com/) - Excellent note-taking tool
- [Cookie Cloud](https://github.com/easychen/CookieCloud) - Cookie sync solution

---

## 👥 Contributing

Contributions, issues, and feature requests are welcome!

- 🐛 **Report Bugs**: [Submit Issue](https://github.com/blessonism/weread2flomo/issues)
- 💡 **Feature Requests**: [Submit Issue](https://github.com/blessonism/weread2flomo/issues)
- 🔧 **Submit Code**: [Create Pull Request](https://github.com/blessonism/weread2flomo/pulls)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👥 Contributors

Thanks to all developers who contributed to WeRead2Flomo!

<p align="center">
  <a href="https://github.com/blessonism/weread2flomo/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=blessonism/weread2flomo&max=20" alt="Contributors" />
  </a>
</p>

---

## 📊 Star History

<p align="center">
  <a href="https://www.star-history.com/#blessonism/weread2flomo&Date" target="_blank">
    <img src="https://api.star-history.com/svg?repos=blessonism/weread2flomo&type=Date" alt="GitHub Stars Trend" width="600">
  </a>
</p>

---

<div align="center">

**⭐ Star the repo if you like it**

<br/>

[Report Bug](https://github.com/blessonism/weread2flomo/issues) · [Request Feature](https://github.com/blessonism/weread2flomo/issues) · [Documentation](docs/README.md)

<br/>
<br/>

<sub>Made with ❤️ by the WeRead2Flomo community</sub>

</div>

