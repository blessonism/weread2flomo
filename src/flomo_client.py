"""
Flomo API 客户端
"""
import os
import requests
import json
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class FlomoClient:
    """Flomo API 客户端"""

    def __init__(self, api_url: Optional[str] = None):
        """
        初始化 Flomo 客户端

        Args:
            api_url: flomo API 地址，如果不提供则从环境变量读取
        """
        self.api_url = api_url or os.getenv("FLOMO_API")
        if not self.api_url:
            raise ValueError("请设置 FLOMO_API 环境变量或提供 api_url 参数")

        self.daily_limit = 100
        self.request_count = 0

    def send_memo(self, content: str) -> bool:
        """
        发送笔记到 flomo

        Args:
            content: 笔记内容，支持 Markdown 和标签（使用 # 符号）

        Returns:
            bool: 是否成功
        """
        if self.request_count >= self.daily_limit:
            print(f"已达到每日API调用限制（{self.daily_limit}次）")
            return False

        try:
            data = {"content": content}
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=10
            )

            self.request_count += 1

            if response.ok:
                print(f"✓ 成功发送笔记到 flomo (第 {self.request_count} 次)")
                return True
            else:
                print(f"✗ 发送失败: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"✗ 发送笔记时出错: {e}")
            return False

    def send_weread_highlight(
        self,
        book_title: str,
        author: str,
        highlight_text: str,
        chapter_name: str = "",
        book_url: str = "",
        tags: list = None
    ) -> bool:
        """
        发送微信读书划线到 flomo

        Args:
            book_title: 书名
            author: 作者
            highlight_text: 划线内容
            chapter_name: 章节名
            book_url: 书籍链接
            tags: 标签列表

        Returns:
            bool: 是否成功
        """
        # 构建内容
        content_parts = [
            f"📖 《{book_title}》- {author}",
            "",
            f"> {highlight_text}",
            ""
        ]

        # 添加章节信息
        if chapter_name:
            content_parts.append(f"📍 {chapter_name}")

        # 添加链接
        if book_url:
            content_parts.append(f"🔗 {book_url}")

        # 添加标签
        default_tag = os.getenv("DEFAULT_TAG", "#微信读书")
        all_tags = [default_tag]

        if tags:
            all_tags.extend(tags)

        # 添加书名作为标签（处理特殊字符）
        book_tag = f"#{book_title.replace(' ', '_')}"
        all_tags.append(book_tag)

        content_parts.append("")
        content_parts.append(" ".join(all_tags))

        # 合并内容
        content = "\n".join(content_parts)

        return self.send_memo(content)

    def get_request_count(self) -> int:
        """获取当前请求计数"""
        return self.request_count

    def reset_count(self):
        """重置请求计数"""
        self.request_count = 0


if __name__ == "__main__":
    # 测试代码
    client = FlomoClient()

    # 测试发送简单笔记
    # client.send_memo("这是一条测试笔记 #测试")

    # 测试发送微信读书划线
    success = client.send_weread_highlight(
        book_title="示例书名",
        author="示例作者",
        highlight_text="这是一段测试的划线内容",
        chapter_name="第一章·开始",
        book_url="https://weread.qq.com/",
        tags=["#测试", "#示例"]
    )

    print(f"\n发送结果: {'成功' if success else '失败'}")
    print(f"API 调用次数: {client.get_request_count()}/{client.daily_limit}")
