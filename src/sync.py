"""
微信读书到 Flomo 的同步工具 - 增强版
支持多模板、AI标签、时间筛选等功能
"""
import os
import sys
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional

# 支持两种运行方式：直接运行和作为模块导入
try:
    # 尝试相对导入（作为模块运行）
    from .weread_api import (
        initialize_api,
        get_notebooklist,
        get_bookmark_list,
        get_chapter_info,
        get_bookinfo,
        get_review_list
    )
    from .flomo_client import FlomoClient
    from .config_manager import config
    from .template_renderer import TemplateRenderer, TagGenerator
    from .ai_tags import AITagGenerator
    from .ai_summary import AISummaryGenerator
    from .log_utils import setup_logging
except ImportError:
    # 如果相对导入失败，使用绝对导入（直接运行）
    # 将项目根目录添加到 sys.path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.weread_api import (
        initialize_api,
        get_notebooklist,
        get_bookmark_list,
        get_chapter_info,
        get_bookinfo,
        get_review_list
    )
    from src.flomo_client import FlomoClient
    from src.config_manager import config
    from src.template_renderer import TemplateRenderer, TagGenerator
    from src.ai_tags import AITagGenerator
    from src.ai_summary import AISummaryGenerator
    from src.log_utils import setup_logging


class WeRead2FlomoV2:
    """微信读书到 Flomo 的增强同步器"""

    def __init__(self):
        # 初始化微信读书API（获取cookie并初始化session）
        if not initialize_api():
            raise RuntimeError(
                "❌ 微信读书API初始化失败！\n"
                "请检查以下配置：\n"
                "1. Cookie Cloud配置 (CC_URL, CC_ID, CC_PASSWORD)\n"
                "2. 或手动配置 WEREAD_COOKIE\n"
                "参考文档：README.md 或 COOKIE_CLOUD_GUIDE.md"
            )

        self.flomo_client = FlomoClient()
        self.template_renderer = TemplateRenderer()
        self.tag_generator = TagGenerator()
        self.ai_tag_generator = AITagGenerator()
        self.ai_summary_generator = AISummaryGenerator()

        self.synced_file = "synced_bookmarks.json"
        self.synced_ids = self.load_synced_ids()

        # 配置参数
        self.days_limit = config.get_days_limit()
        self.max_highlights = config.get_max_highlights()
        self.request_delay = config.get_request_delay()

        print(f"\n⚙️  配置加载:")
        print(f"   - 时间限制: {self.days_limit}天" if self.days_limit > 0 else "   - 时间限制: 无")
        print(f"   - 最大划线数: {self.max_highlights}")
        print(f"   - AI标签: {'启用' if self.ai_tag_generator.is_enabled() else '禁用'}")
        print(f"   - AI摘要: {'启用' if self.ai_summary_generator.is_enabled() else '禁用'}")
        print(f"   - 默认模板: {config.get('default_template', 'simple')}\n")

    def load_synced_ids(self) -> Set[str]:
        """加载已同步的划线ID"""
        if os.path.exists(self.synced_file):
            try:
                with open(self.synced_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get("synced_ids", []))
            except Exception as e:
                print(f"⚠️  加载同步记录失败: {e}")
        return set()

    def save_synced_ids(self):
        """保存已同步的划线ID（原子写入）"""
        try:
            import tempfile
            import os as _os
            dir_name = _os.path.dirname(_os.path.abspath(self.synced_file)) or "."
            data = {
                "synced_ids": list(self.synced_ids),
                "last_sync": datetime.now().isoformat(),
                "total_synced": len(self.synced_ids)
            }
            with tempfile.NamedTemporaryFile('w', delete=False, dir=dir_name, encoding='utf-8') as tf:
                json.dump(data, tf, ensure_ascii=False, indent=2)
                temp_name = tf.name
            _os.replace(temp_name, self.synced_file)
        except Exception as e:
            print(f"⚠️  保存同步记录失败: {e}")

    def get_chapter_name(self, chapters: List[Dict], chapterUid: int) -> str:
        """根据章节UID获取章节名称"""
        for chapter in chapters:
            if chapter.get("chapterUid") == chapterUid:
                title = chapter.get("title", "")
                # level 表示层级深度，非章节序号，这里优先使用 chapterIdx
                idx = chapter.get("chapterIdx")
                if title and isinstance(idx, int):
                    return f"第{idx}章 - {title}"
                return title or ""
        return ""

    def should_sync_bookmark(self, bookmark: Dict) -> bool:
        """
        判断是否应该同步该划线

        Args:
            bookmark: 划线信息

        Returns:
            bool: 是否应该同步
        """
        bookmark_id = bookmark.get("bookmarkId")

        # 检查是否已同步
        if bookmark_id in self.synced_ids:
            return False

        # 检查时间限制
        if self.days_limit > 0:
            create_time = bookmark.get("createTime", 0)
            if create_time > 0:
                # 将秒转换为日期
                bookmark_date = datetime.fromtimestamp(create_time)
                cutoff_date = datetime.now() - timedelta(days=self.days_limit)

                if bookmark_date < cutoff_date:
                    return False

        return True

    def sync_book(self, book: Dict, max_count: Optional[int] = None) -> int:
        """
        同步单本书的划线

        Args:
            book: 书籍信息
            max_count: 本次最多同步的划线数（全局配额）

        Returns:
            int: 新同步的划线数量
        """
        bookId = book.get("bookId")
        # 修复：从 book.book 对象中获取标题和作者
        book_info_obj = book.get("book", {})
        book_title = book_info_obj.get("title", "未知书名")
        author = book_info_obj.get("author", "未知作者")

        print(f"\n📚 处理书籍: 《{book_title}》- {author}")

        # 判断书籍分类
        category = config.get_book_category(book_title, author)
        if category:
            print(f"   分类: {category}")

        # 获取适合的模板
        if category:
            template = config.get_category_template(category)
        else:
            template = config.get_template()

        # 获取书籍信息
        book_info = get_bookinfo(bookId)
        book_url = f"https://weread.qq.com/web/reader/{bookId}"

        # ⚠️ 关键修复：先获取划线列表，再获取章节信息
        # 因为 get_chapter_info 会重置 session，影响后续 API 调用
        bookmarks = get_bookmark_list(bookId)
        
        # 获取章节信息（放在划线列表之后）
        chapters = get_chapter_info(bookId)

        if not bookmarks:
            print("   ⚠️  该书没有划线数据")
            return 0
        
        print(f"   ✓ 获取到 {len(bookmarks)} 条划线")

        # 获取笔记（如果启用）
        reviews = {}
        if config.should_sync_reviews():
            review_list = get_review_list(bookId)
            for review in review_list:
                bookmark_id = review.get("bookmarkId")
                if bookmark_id:
                    reviews[bookmark_id] = review.get("content", "")

        # 过滤需要同步的划线
        new_bookmarks = [
            bm for bm in bookmarks
            if self.should_sync_bookmark(bm)
        ]
        
        # 详细输出过滤信息
        filtered_count = len(bookmarks) - len(new_bookmarks)
        if filtered_count > 0:
            print(f"   ℹ️  过滤了 {filtered_count} 条划线（已同步或超出时间限制）")

        if not new_bookmarks:
            print(f"   ⚠️  没有新的划线需要同步")
            return 0

        # 限制数量（使用全局配额或默认限制）
        actual_max = max_count if max_count is not None else self.max_highlights
        if len(new_bookmarks) > actual_max:
            print(f"   划线数量较多，本次同步限制为 {actual_max} 条（全局剩余配额）")
            new_bookmarks = new_bookmarks[:actual_max]
        else:
            print(f"   找到 {len(new_bookmarks)} 条新划线")

        synced_count = 0

        for bookmark in new_bookmarks:
            bookmark_id = bookmark.get("bookmarkId")
            marked_text = bookmark.get("markText", "")
            chapter_uid = bookmark.get("chapterUid", 0)
            create_time = bookmark.get("createTime", 0)

            # 获取章节名称
            chapter_name = self.get_chapter_name(chapters, chapter_uid)

            # 获取笔记
            note_text = reviews.get(bookmark_id, "")

            # 格式化时间
            if create_time > 0:
                create_time_str = datetime.fromtimestamp(create_time).strftime("%Y-%m-%d")
            else:
                create_time_str = datetime.now().strftime("%Y-%m-%d")

            # 生成AI标签
            ai_tags = []
            if self.ai_tag_generator.is_enabled():
                try:
                    ai_tags = self.ai_tag_generator.generate_tags(
                        book_title=book_title,
                        author=author,
                        highlight_text=marked_text
                    )
                except Exception as e:
                    print(f"   ⚠️  AI标签生成失败: {e}")

            # 生成AI摘要
            ai_summary = None
            if self.ai_summary_generator.is_enabled():
                try:
                    ai_summary = self.ai_summary_generator.generate_summary(
                        highlight_text=marked_text,
                        book_title=book_title,
                        author=author
                    )
                    if ai_summary:
                        print(f"   🤖 AI提炼: {ai_summary[:50]}...")
                except Exception as e:
                    print(f"   ⚠️  AI摘要生成失败: {e}")

            # 生成所有标签
            tags = self.tag_generator.generate_tags(
                book_title=book_title,
                author=author,
                highlight_text=marked_text,
                category=category,
                ai_tags=ai_tags
            )

            # 渲染内容（AI 摘要作为独立参数传递）
            content = self.template_renderer.render(
                template=template,
                book_title=book_title,
                author=author,
                highlight_text=marked_text,
                chapter_name=chapter_name,
                book_url=book_url,
                note_text=note_text,
                create_time=create_time_str,
                tags=tags,
                ai_summary=ai_summary or ""
            )

            # 发送到 flomo
            success = self.flomo_client.send_memo(content)

            if success:
                self.synced_ids.add(bookmark_id)
                synced_count += 1
                # 添加延迟
                time.sleep(self.request_delay)
            else:
                print(f"   跳过划线: {marked_text[:30]}...")
                break

            # 检查是否达到每日限制
            if self.flomo_client.get_request_count() >= self.flomo_client.daily_limit:
                print(f"\n⚠️  已达到 flomo 每日API调用限制")
                break

        return synced_count

    def sync_all(self):
        """同步所有书籍的划线"""
        print("=" * 70)
        print("🚀 开始同步微信读书划线到 flomo")
        print("=" * 70)

        # 获取书籍列表
        books = get_notebooklist()

        if not books:
            print("❌ 没有找到任何书籍")
            return

        print(f"\n📖 找到 {len(books)} 本书")

        total_synced = 0
        processed_books = 0
        remaining_quota = self.max_highlights  # 全局剩余配额

        for book in books:
            try:
                # 如果已达到全局限制，停止处理
                if remaining_quota <= 0:
                    print(f"\n⚠️  已达到全局划线限制 ({self.max_highlights} 条)，停止同步")
                    break

                synced_count = self.sync_book(book, max_count=remaining_quota)
                total_synced += synced_count
                remaining_quota -= synced_count
                processed_books += 1

                # 检查是否达到每日限制
                if self.flomo_client.get_request_count() >= self.flomo_client.daily_limit:
                    print(f"\n⚠️  已达到每日同步限制，停止同步")
                    break

                # 书籍之间添加延迟
                if synced_count > 0:
                    time.sleep(2)

            except Exception as e:
                print(f"\n⚠️  处理书籍时出错: {e}")
                continue

        # 保存同步记录
        self.save_synced_ids()

        # 输出统计信息
        print("\n" + "=" * 70)
        print(f"✅ 同步完成!")
        print(f"   处理书籍: {processed_books}/{len(books)}")
        print(f"   本次新同步: {total_synced} 条划线")
        print(f"   累计已同步: {len(self.synced_ids)} 条划线")
        print(f"   API 调用次数: {self.flomo_client.get_request_count()}/{self.flomo_client.daily_limit}")
        print("=" * 70)


def main():
    """主函数"""
    try:
        # 初始化日志
        setup_logging()
        syncer = WeRead2FlomoV2()
        syncer.sync_all()
    except Exception as e:
        print(f"\n❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
