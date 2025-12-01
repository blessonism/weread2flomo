"""
Flomo API 客户端
"""
import os
import time
import requests
import json
from typing import Dict, Optional
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .config_manager import config

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

        # 每日配额和 dry-run
        try:
            self.daily_limit = int(os.getenv("FLOMO_DAILY_LIMIT", "100"))
        except ValueError:
            self.daily_limit = 100
        self.dry_run = str(os.getenv("DRY_RUN", "false")).lower() in ("1", "true", "yes")
        self.request_count = 0

        # 带重试的 Session
        self.session = requests.Session()
        retries = Retry(
            total=config.get_max_retries(),
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retries, pool_connections=5, pool_maxsize=5)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

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

        if self.dry_run:
            self.request_count += 1
            print(f"[DRY-RUN] 模拟发送到 flomo (第 {self.request_count} 次)，长度={len(content)}")
            return True

        data = {"content": content}
        max_retries = max(1, int(config.get_max_retries()))
        backoff = 0.8

        for attempt in range(max_retries):
            try:
                response = self.session.post(
                    self.api_url,
                    headers={"Content-Type": "application/json"},
                    json=data,
                    timeout=10
                )

                # 计数只在请求真正发出时递增
                self.request_count += 1

                if response.ok:
                    print(f"✓ 成功发送笔记到 flomo (第 {self.request_count} 次)")
                    return True

                status = response.status_code
                body_preview = response.text[:200] if response.text else ""
                # 对 429/5xx 做重试
                if status in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                    sleep_s = backoff * (2 ** attempt)
                    print(f"⚠️ flomo 返回 {status}，{sleep_s:.1f}s 后重试... body={body_preview}")
                    time.sleep(sleep_s)
                    continue

                print(f"✗ 发送失败: {status} - {body_preview}")
                return False

            except Exception as e:
                if attempt < max_retries - 1:
                    sleep_s = backoff * (2 ** attempt)
                    print(f"⚠️ 发送异常: {e}，{sleep_s:.1f}s 后重试...")
                    time.sleep(sleep_s)
                    continue
                print(f"✗ 发送笔记时出错: {e}")
                return False

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
