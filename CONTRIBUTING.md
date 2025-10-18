# 贡献指南

感谢你对 WeRead2Flomo 的关注！我们欢迎各种形式的贡献。

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [问题反馈](#问题反馈)

## 行为准则

本项目遵循 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。参与此项目即表示你同意遵守其条款。

## 如何贡献

### 🐛 报告 Bug

如果你发现了 Bug，请：

1. 检查 [Issues](https://github.com/blessonism/weread2flomo/issues) 确保问题未被报告
2. 使用 [Bug Report 模板](.github/ISSUE_TEMPLATE/bug_report.md) 创建新 Issue
3. 提供详细的复现步骤和环境信息
4. 如果可能，附上错误日志和截图

### 💡 功能建议

如果你有新功能的想法：

1. 检查 [Issues](https://github.com/blessonism/weread2flomo/issues) 和 [路线图](README.md#-路线图)
2. 使用 [Feature Request 模板](.github/ISSUE_TEMPLATE/feature_request.md) 创建新 Issue
3. 清晰描述功能的使用场景和价值
4. 如果可能，提供实现思路

### 🔧 提交代码

1. **Fork 仓库**
   ```bash
   # Fork 后克隆到本地
   git clone https://github.com/your-username/weread2flomo.git
   cd weread2flomo
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **进行开发**
   - 编写代码
   - 添加测试
   - 更新文档

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建 Pull Request**
   - 前往 GitHub 创建 PR
   - 填写 PR 描述，说明改动内容
   - 等待代码审查

## 开发流程

### 环境设置

```bash
# 1. 克隆仓库
git clone https://github.com/blessonism/weread2flomo.git
cd weread2flomo

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 5. 运行测试
python test_single_highlight.py
```

### 项目结构

```
weread2flomo/
├── src/                    # 源代码
│   ├── sync.py            # 同步主逻辑
│   ├── weread_api.py      # 微信读书 API
│   ├── flomo_client.py    # Flomo 客户端
│   ├── template_renderer.py  # 模板渲染
│   ├── ai_summary.py      # AI 摘要
│   ├── ai_tags.py         # AI 标签
│   └── config_manager.py  # 配置管理
├── tests/                  # 测试文件
├── docs/                   # 文档
├── config.yaml            # 配置文件
└── README.md              # 主文档
```

### 添加新功能

1. **在 `src/` 中添加新模块**
   ```python
   # src/your_module.py
   """
   模块说明
   """
   
   class YourClass:
       """类说明"""
       
       def your_method(self):
           """方法说明"""
           pass
   ```

2. **添加配置项（如需要）**
   ```yaml
   # config.yaml
   your_feature:
     option1: value1
     option2: value2
   ```

3. **添加测试**
   ```python
   # tests/test_your_module.py
   def test_your_feature():
       assert True
   ```

4. **更新文档**
   - 更新 README.md
   - 添加功能说明到 docs/FEATURES.md
   - 如需要，创建独立文档

## 代码规范

### Python 代码风格

遵循 [PEP 8](https://pep8.org/) 规范：

```python
# 好的示例
def sync_highlights(book_id: str, days_limit: int = 100) -> List[Dict]:
    """
    同步书籍划线
    
    Args:
        book_id: 书籍 ID
        days_limit: 时间限制（天）
        
    Returns:
        划线列表
    """
    bookmarks = get_bookmark_list(book_id)
    return filter_bookmarks(bookmarks, days_limit)


# 避免
def sync(bid,dl=100):
    bks=get_bm(bid)
    return filter(bks,dl)
```

### 命名规范

- **函数/方法**: `snake_case`
  ```python
  def get_bookmark_list(): pass
  ```

- **类**: `PascalCase`
  ```python
  class FlomoClient: pass
  ```

- **常量**: `UPPER_SNAKE_CASE`
  ```python
  MAX_RETRIES = 3
  ```

- **私有成员**: 前缀 `_`
  ```python
  def _internal_method(): pass
  ```

### 文档字符串

使用 Google 风格的 docstring：

```python
def generate_summary(text: str, max_length: int = 100) -> str:
    """
    生成文本摘要
    
    Args:
        text: 原始文本
        max_length: 最大长度
        
    Returns:
        摘要文本
        
    Raises:
        ValueError: 如果文本为空
        
    Example:
        >>> summary = generate_summary("很长的文本...")
        >>> print(summary)
        "简短的摘要"
    """
    pass
```

### 类型注解

使用 Python 类型注解：

```python
from typing import List, Dict, Optional

def process_bookmarks(
    bookmarks: List[Dict],
    template: str,
    ai_enabled: bool = False
) -> Optional[str]:
    pass
```

## 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 提交类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构（不是新功能也不是修复）
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 提交格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 示例

```bash
# 新功能
git commit -m "feat(ai): add GPT-4 support for summaries"

# Bug 修复
git commit -m "fix(sync): handle empty bookmark list"

# 文档更新
git commit -m "docs: update configuration guide"

# 重构
git commit -m "refactor(template): simplify template rendering logic"
```

## 问题反馈

### 报告 Bug

使用 [Bug Report 模板](.github/ISSUE_TEMPLATE/bug_report.md)，包括：

- 清晰的标题
- 详细的问题描述
- 复现步骤
- 期望行为 vs 实际行为
- 环境信息（OS、Python 版本等）
- 相关日志和截图

### 功能建议

使用 [Feature Request 模板](.github/ISSUE_TEMPLATE/feature_request.md)，包括：

- 功能描述
- 使用场景
- 预期效果
- 可选的实现思路

## Pull Request 检查清单

提交 PR 前，请确保：

- [ ] 代码遵循项目规范
- [ ] 添加了必要的测试
- [ ] 所有测试通过
- [ ] 更新了相关文档
- [ ] 提交信息符合规范
- [ ] PR 描述清晰，说明了改动内容
- [ ] 关联了相关的 Issue（如果有）

## 代码审查

### 审查流程

1. 提交 PR 后，维护者会进行审查
2. 根据反馈进行修改
3. 所有讨论解决后，PR 会被合并

### 审查标准

- 代码质量和可读性
- 是否遵循项目规范
- 是否有充分的测试
- 文档是否完善
- 是否向后兼容

## 发布流程

由维护者负责：

1. 更新版本号
2. 更新 CHANGELOG
3. 创建 GitHub Release
4. 发布到 PyPI（未来）

## 获得帮助

如果有任何问题：

- 查看 [文档](docs/README.md)
- 搜索 [Issues](https://github.com/blessonism/weread2flomo/issues)
- 创建新 Issue
- 联系维护者

## 致谢

感谢所有贡献者！你们的贡献让这个项目变得更好。

---

再次感谢你的贡献！ ❤️

