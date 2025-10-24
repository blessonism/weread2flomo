"""
AI 标签生成器
支持多种 AI 服务提供商
"""
import os
import time
import requests
from typing import List, Optional, Tuple
from .config_manager import config


class AITagGenerator:
    """AI 标签生成器"""

    def __init__(self):
        """初始化 AI 标签生成器"""
        self.provider = config.get_ai_provider()
        self.api_key = config.get_ai_api_key()
        self.api_base = config.get_ai_api_base()
        self.model = config.get_ai_model()
        self._cache = {}
        self._max_cache = 200

    def is_enabled(self) -> bool:
        """检查 AI 标签是否启用"""
        return config.should_enable_ai_tags() and self.provider != 'none'

    def generate_tags(
        self,
        book_title: str,
        author: str,
        highlight_text: str
    ) -> List[str]:
        """
        生成标签

        Args:
            book_title: 书名
            author: 作者
            highlight_text: 划线内容

        Returns:
            标签列表
        """
        if not self.is_enabled():
            return []

        cache_key: Tuple[str, str, str] = (book_title, author, highlight_text)
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            if self.provider == 'openai':
                tags = self._generate_with_openai(book_title, author, highlight_text)
            elif self.provider == 'local':
                tags = self._generate_with_local(book_title, author, highlight_text)
            else:
                print(f"⚠️  不支持的 AI 提供商: {self.provider}")
                tags = []
        except Exception as e:
            print(f"⚠️  AI 标签生成失败: {e}")
            tags = []

        # 写入缓存（简单上限控制）
        if tags:
            if len(self._cache) >= self._max_cache:
                self._cache.clear()
            self._cache[cache_key] = tags

        return tags

    def _generate_with_openai(
        self,
        book_title: str,
        author: str,
        highlight_text: str
    ) -> List[str]:
        """使用 OpenAI 格式的 API 生成标签"""
        if not self.api_key:
            print("⚠️  未设置 AI API Key")
            return []

        # 构建提示词
        raw_prompt = config.get('ai.tag_prompt', '')
        if not raw_prompt:
            raw_prompt = (
                '请为以下摘录生成 1-3 个中文标签，以#开头，单个词或短语，贴合主题，空格分隔：\n'
                '书名：{book_title}\n作者：{author}\n摘录：{highlight_text}'
            )
        prompt = raw_prompt.format(
            book_title=book_title,
            author=author,
            highlight_text=highlight_text
        )

        # 调用 OpenAI 格式的 API
        url = f"{self.api_base.rstrip('/')}/chat/completions"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': self.model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 100
        }

        max_retries = max(1, int(config.get_max_retries()))
        backoff = 0.8
        last_err = None
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                response.raise_for_status()
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                tags = self._parse_tags(content)
                return tags[:config.get('tags.max_ai_tags', 3)]
            except Exception as e:
                last_err = e
                if attempt < max_retries - 1:
                    time.sleep(backoff * (2 ** attempt))
                else:
                    raise last_err

    def _generate_with_local(
        self,
        book_title: str,
        author: str,
        highlight_text: str
    ) -> List[str]:
        """使用本地规则生成标签（基于关键词匹配）"""
        tags = []

        # 定义关键词到标签的映射
        keyword_tags = {
            '思维': '#思维模型',
            '认知': '#认知科学',
            '心理': '#心理学',
            '效率': '#效率提升',
            '时间': '#时间管理',
            '习惯': '#习惯养成',
            '沟通': '#沟通技巧',
            '领导': '#领导力',
            '管理': '#管理',
            '创新': '#创新思维',
            '决策': '#决策',
            '学习': '#学习方法',
            '成长': '#个人成长',
            '目标': '#目标管理',
            '专注': '#专注力',
            '情绪': '#情绪管理',
            '关系': '#人际关系',
            '健康': '#健康',
            '财富': '#财富',
            '投资': '#投资理财',
        }

        # 检查文本中的关键词
        text = f"{highlight_text} {book_title}".lower()

        for keyword, tag in keyword_tags.items():
            if keyword in text and tag not in tags:
                tags.append(tag)
                if len(tags) >= config.get('tags.max_ai_tags', 3):
                    break

        return tags

    def _parse_tags(self, content: str) -> List[str]:
        """
        解析 AI 返回的标签文本

        Args:
            content: AI 返回的文本

        Returns:
            标签列表
        """
        tags = []

        # 按行分割
        lines = content.strip().split('\n')

        for line in lines:
            line = line.strip()

            # 跳过空行和说明文字
            if not line or line.startswith('标签') or line.startswith('Tag'):
                continue

            # 提取标签
            if '#' in line:
                # 分割多个标签
                parts = line.split()
                for part in parts:
                    if part.startswith('#'):
                        tags.append(part)

        return tags


if __name__ == "__main__":
    # 测试 AI 标签生成器
    print("=== AI 标签生成器测试 ===\n")

    generator = AITagGenerator()

    print(f"AI 提供商: {generator.provider}")
    print(f"AI 已启用: {generator.is_enabled()}\n")

    # 测试本地规则生成
    if generator.provider == 'local' or generator.provider == 'none':
        print("使用本地规则生成标签...\n")

        test_cases = [
            ("思考，快与慢", "丹尼尔·卡尼曼", "人们总是高估自己的理性，低估直觉的作用"),
            ("原则", "瑞·达利欧", "建立清晰的决策原则，可以帮助我们做出更好的选择"),
            ("深度工作", "卡尔·纽波特", "在没有干扰的状态下专注进行职业活动"),
        ]

        for book_title, author, highlight in test_cases:
            print(f"书名: 《{book_title}》")
            print(f"划线: {highlight}")

            tags = generator.generate_tags(book_title, author, highlight)
            print(f"生成的标签: {tags}\n")
