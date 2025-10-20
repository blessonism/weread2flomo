"""
AI 摘要生成器
为长划线生成一句话摘要
"""
import os
import requests
from typing import Optional
from .config_manager import config


class AISummaryGenerator:
    """AI 摘要生成器"""

    def __init__(self):
        """初始化 AI 摘要生成器"""
        self.provider = config.get_ai_provider()
        self.api_key = config.get_ai_api_key()
        self.api_base = config.get_ai_api_base()
        self.model = config.get_ai_model()
        
        # 摘要启用阈值（字符数）
        self.min_length = config.get('ai.summary_min_length', 100)

    def is_enabled(self) -> bool:
        """检查 AI 摘要是否启用"""
        enable_summary = config.get('ai.enable_summary', False, env_key='ENABLE_AI_SUMMARY')
        return enable_summary and self.provider == 'openai' and bool(self.api_key)

    def should_summarize(self, text: str) -> bool:
        """
        判断是否需要生成摘要
        
        Args:
            text: 文本内容
            
        Returns:
            是否需要生成摘要
        """
        return self.is_enabled() and len(text) >= self.min_length

    def generate_summary(
        self,
        highlight_text: str,
        book_title: Optional[str] = None,
        author: Optional[str] = None
    ) -> Optional[str]:
        """
        生成摘要
        
        Args:
            highlight_text: 划线内容
            book_title: 书名（可选）
            author: 作者（可选）
            
        Returns:
            摘要文本，失败返回None
        """
        if not self.should_summarize(highlight_text):
            return None

        try:
            return self._generate_with_openai(highlight_text, book_title, author)
        except Exception as e:
            print(f"   ⚠️  AI 摘要生成失败: {e}")
            return None

    def _generate_with_openai(
        self,
        highlight_text: str,
        book_title: Optional[str] = None,
        author: Optional[str] = None
    ) -> Optional[str]:
        """使用 OpenAI 格式的 API 生成摘要"""
        if not self.api_key:
            return None

        # 构建提示词
        prompt = config.get('ai.summary_prompt', '').format(
            highlight_text=highlight_text,
            book_title=book_title or '',
            author=author or ''
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
            'max_tokens': 150
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        summary = result['choices'][0]['message']['content'].strip()

        return summary if summary else None


if __name__ == "__main__":
    # 测试 AI 摘要生成器
    print("=== AI 摘要生成器测试 ===\n")

    generator = AISummaryGenerator()

    print(f"AI 提供商: {generator.provider}")
    print(f"AI 摘要已启用: {generator.is_enabled()}")
    print(f"最小长度: {generator.min_length} 字符\n")

    # 测试用例
    test_cases = [
        {
            "book_title": "思考，快与慢",
            "author": "丹尼尔·卡尼曼",
            "text": """系统1的运作是无意识且快速的，不怎么费脑力，没有感觉，完全处于自主控制状态。系统2将注意力转移到需要费脑力的大脑活动上来，例如复杂的运算。系统2的运作通常与行为、选择和专注等主观体验相关联。系统1和系统2的分工是非常高效的：将工作量最小化。通常，系统1自动运行，而系统2则处于不费力的放松状态，运行时只动用一部分能力。系统1不断为系统2提供印象、直觉、意向和感觉等信息。如果系统2接收了这些信息，则会将印象、直觉等转变为信念，将冲动转化为自主行为。"""
        },
        {
            "book_title": "原则",
            "author": "瑞·达利欧",
            "text": "建立清晰的决策原则，可以帮助我们做出更好的选择。"
        },
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"测试 {i}:")
        print(f"书名: 《{case['book_title']}》")
        print(f"文本长度: {len(case['text'])} 字符")
        print(f"需要摘要: {generator.should_summarize(case['text'])}")
        
        if generator.is_enabled():
            summary = generator.generate_summary(
                case['text'],
                case['book_title'],
                case['author']
            )
            if summary:
                print(f"生成的摘要: {summary}")
        else:
            print("AI 摘要未启用（需要设置 ENABLE_AI_SUMMARY=true 和 AI_API_KEY）")
        
        print()


